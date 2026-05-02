import dotenv from "dotenv";

import { createPublicClient, http } from "viem";
import {
  DataBlock,
  Graph,
  Position,
  SystemIds,
  TESTNET_RPC_URL,
  daoSpace,
  getSmartAccountWalletClient,
  personalSpace,
} from "@geoprotocol/geo-sdk";
import { SpaceRegistryAbi } from "@geoprotocol/geo-sdk/abis";
import { TESTNET } from "@geoprotocol/geo-sdk/contracts";

dotenv.config({
  path: new URL("../../.env", import.meta.url),
});

const GEO_PRIVATE_KEY = process.env.GEO_PRIVATE_KEY;
const DRY_RUN = process.env.DRY_RUN === "1";

const TARGET_SPACE_ID = process.env.GEO_TARGET_SPACE_ID;
const TARGET_SPACE_ADDRESS = process.env.GEO_TARGET_SPACE_ADDRESS;
const TARGET_SPACE_ENTITY_ID = process.env.GEO_TARGET_SPACE_ENTITY_ID;
const SPACE_NAME = process.env.GEO_TARGET_SPACE_NAME || "Target space";

if (!GEO_PRIVATE_KEY) throw new Error("Missing GEO_PRIVATE_KEY in environment.");
if (!TARGET_SPACE_ID) throw new Error("Missing GEO_TARGET_SPACE_ID in environment.");
if (!TARGET_SPACE_ADDRESS) {
  throw new Error("Missing GEO_TARGET_SPACE_ADDRESS in environment.");
}
if (!TARGET_SPACE_ENTITY_ID) {
  throw new Error("Missing GEO_TARGET_SPACE_ENTITY_ID in environment.");
}

const TYPE_ENTITY_ID = SystemIds.SCHEMA_TYPE;
const TYPES_RELATION_ID = SystemIds.TYPES_PROPERTY;
const FILTER_PROPERTY_ID = SystemIds.FILTER;

const WEEK_NAME = "Week";
const WEEK_DESCRIPTION =
  "A recurring seven-day unit used to structure a program, sequence, schedule, or planning cycle.";
const TYPES_BLOCK_NAME = "Types";
const TYPES_FILTER = JSON.stringify({
  filter: {
    [TYPES_RELATION_ID]: {
      is: TYPE_ENTITY_ID,
    },
  },
});

function bytes16Hex(id) {
  return `0x${id}`;
}

function opIdToHex(id) {
  if (!id || typeof id !== "object") return null;
  const values = Object.values(id);
  if (values.length !== 16) return null;
  return values.map((value) => Number(value).toString(16).padStart(2, "0")).join("");
}

async function gql(query) {
  const response = await fetch("https://testnet-api.geobrowser.io/graphql", {
    method: "POST",
    headers: {
      "content-type": "application/json",
    },
    body: JSON.stringify({ query }),
  });

  const payload = await response.json();

  if (payload.errors?.length) {
    throw new Error(payload.errors.map((error) => error.message).join("; "));
  }

  return payload.data;
}

async function getSpaceEntities() {
  const data = await gql(`{
    entities(spaceId: "${TARGET_SPACE_ID}", first: 100) {
      id
      name
      typeIds
      description
    }
  }`);

  return data.entities;
}

async function findExistingWeekType() {
  const entities = await getSpaceEntities();
  return entities.find(
    (entity) =>
      entity.name === WEEK_NAME && entity.typeIds?.includes(TYPE_ENTITY_ID)
  );
}

async function findExistingTypesBlock() {
  const entities = await getSpaceEntities();
  return entities.find(
    (entity) =>
      entity.name === TYPES_BLOCK_NAME &&
      entity.typeIds?.includes(SystemIds.DATA_BLOCK)
  );
}

const wallet = await getSmartAccountWalletClient({
  privateKey: GEO_PRIVATE_KEY.startsWith("0x")
    ? GEO_PRIVATE_KEY
    : `0x${GEO_PRIVATE_KEY}`,
});

const smartAccountAddress = wallet.account.address;
const hasPersonalSpace = await personalSpace.hasSpace({
  address: smartAccountAddress,
});

if (!hasPersonalSpace) {
  throw new Error(
    `No personal space found for smart account ${smartAccountAddress}. Create it in Geo first.`
  );
}

const publicClient = createPublicClient({
  transport: http(TESTNET_RPC_URL),
});

const callerSpaceIdHex = await publicClient.readContract({
  address: TESTNET.SPACE_REGISTRY_ADDRESS,
  abi: SpaceRegistryAbi,
  functionName: "addressToSpaceId",
  args: [smartAccountAddress],
});

const callerSpaceId = String(callerSpaceIdHex).slice(2, 34).toLowerCase();
const existingWeekType = await findExistingWeekType();
const existingTypesBlock = await findExistingTypesBlock();

if (existingWeekType && existingTypesBlock) {
  console.log(
    JSON.stringify(
      {
        ok: true,
        skipped: true,
        reason: "Week type and Types block already exist.",
        weekTypeId: existingWeekType.id,
        typesBlockId: existingTypesBlock.id,
        targetSpaceId: TARGET_SPACE_ID,
        targetSpaceName: SPACE_NAME,
      },
      null,
      2
    )
  );
  process.exit(0);
}

const ops = [];

if (!existingWeekType) {
  const { ops: weekOps } = Graph.createEntity({
    name: WEEK_NAME,
    description: WEEK_DESCRIPTION,
    types: [TYPE_ENTITY_ID],
  });
  ops.push(...weekOps);
}

if (!existingTypesBlock) {
  const blockOps = DataBlock.make({
    fromId: TARGET_SPACE_ENTITY_ID,
    sourceType: "COLLECTION",
    position: Position.generate(),
    name: TYPES_BLOCK_NAME,
  });
  ops.push(...blockOps);

  const blockId = blockOps.find(
    (op) =>
      op.type === "updateEntity" &&
      Array.isArray(op.set) &&
      op.set.some((entry) => opIdToHex(entry.property) === SystemIds.NAME_PROPERTY)
  )?.id;

  if (!blockId) {
    throw new Error("Failed to derive the new Types block id from block ops.");
  }

  const { ops: filterOps } = Graph.updateEntity({
    id: opIdToHex(blockId),
    values: [
      {
        property: FILTER_PROPERTY_ID,
        type: "text",
        value: TYPES_FILTER,
      },
    ],
  });
  ops.push(...filterOps);
}

const proposalName = "Create Week type and Types block";
const proposal = await daoSpace.proposeEdit({
  name: proposalName,
  ops,
  author: callerSpaceId,
  daoSpaceAddress: TARGET_SPACE_ADDRESS,
  callerSpaceId: bytes16Hex(callerSpaceId),
  daoSpaceId: bytes16Hex(TARGET_SPACE_ID),
  votingMode: "FAST",
  network: "TESTNET",
});

if (DRY_RUN) {
  console.log(
    JSON.stringify(
      {
        ok: true,
        dryRun: true,
        proposalName,
        targetSpaceId: TARGET_SPACE_ID,
        targetSpaceName: SPACE_NAME,
        opCount: ops.length,
      },
      null,
      2
    )
  );
  process.exit(0);
}

const txHash = await wallet.sendTransaction({
  account: wallet.account,
  to: proposal.to,
  data: proposal.calldata,
});

const receipt = await publicClient.waitForTransactionReceipt({
  hash: txHash,
});

console.log(
  JSON.stringify(
    {
      ok: receipt.status === "success",
      txHash,
      editId: proposal.editId,
      proposalName,
      targetSpaceId: TARGET_SPACE_ID,
      targetSpaceName: SPACE_NAME,
    },
    null,
    2
  )
);
