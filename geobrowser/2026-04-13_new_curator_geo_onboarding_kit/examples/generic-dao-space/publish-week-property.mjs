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

const PROPERTY_TYPE_ID = SystemIds.PROPERTY;
const RELATION_DATA_TYPE_ID = SystemIds.RELATION;
const TO_ENTITY_TYPES_RELATION_ID = SystemIds.RELATION_VALUE_RELATIONSHIP_TYPE;
const FILTER_PROPERTY_ID = SystemIds.FILTER;

const WEEK_PROPERTY_NAME = "Week";
const WEEK_PROPERTY_DESCRIPTION =
  "Relation property linking an entity to a Week type within this space.";
const PROPERTIES_BLOCK_NAME = "Properties";
const PROPERTIES_FILTER = JSON.stringify({
  spaceId: {
    in: [TARGET_SPACE_ID],
  },
  filter: {
    [SystemIds.TYPES_PROPERTY]: {
      is: PROPERTY_TYPE_ID,
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
    headers: { "content-type": "application/json" },
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
    }
  }`);
  return data.entities;
}

async function findExistingWeekProperty() {
  const entities = await getSpaceEntities();
  return entities.find(
    (entity) =>
      entity.name === WEEK_PROPERTY_NAME && entity.typeIds?.includes(PROPERTY_TYPE_ID)
  );
}

async function findExistingPropertiesBlock() {
  const entities = await getSpaceEntities();
  return entities.find(
    (entity) =>
      entity.name === PROPERTIES_BLOCK_NAME &&
      entity.typeIds?.includes(SystemIds.DATA_BLOCK)
  );
}

async function findWeekType() {
  const entities = await getSpaceEntities();
  const typeEntityId = SystemIds.SCHEMA_TYPE;
  return entities.find(
    (entity) => entity.name === "Week" && entity.typeIds?.includes(typeEntityId)
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
const existingWeekProperty = await findExistingWeekProperty();
const existingPropertiesBlock = await findExistingPropertiesBlock();
const weekType = await findWeekType();

if (!weekType) {
  throw new Error(
    'Could not find a "Week" type in the target space. Create or identify the Week type first.'
  );
}

if (existingWeekProperty && existingPropertiesBlock) {
  console.log(
    JSON.stringify(
      {
        ok: true,
        skipped: true,
        reason: "Week property and Properties block already exist.",
        weekPropertyId: existingWeekProperty.id,
        propertiesBlockId: existingPropertiesBlock.id,
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

if (!existingWeekProperty) {
  const { ops: propertyOps } = Graph.createEntity({
    name: WEEK_PROPERTY_NAME,
    description: WEEK_PROPERTY_DESCRIPTION,
    types: [PROPERTY_TYPE_ID],
    relations: {
      [SystemIds.DATA_TYPE]: {
        toEntity: RELATION_DATA_TYPE_ID,
      },
      [TO_ENTITY_TYPES_RELATION_ID]: {
        toEntity: weekType.id,
      },
    },
  });
  ops.push(...propertyOps);
}

if (!existingPropertiesBlock) {
  const blockOps = DataBlock.make({
    fromId: TARGET_SPACE_ENTITY_ID,
    sourceType: "QUERY",
    position: Position.generate(),
    name: PROPERTIES_BLOCK_NAME,
  });
  ops.push(...blockOps);

  const blockId = blockOps.find(
    (op) =>
      op.type === "updateEntity" &&
      Array.isArray(op.set) &&
      op.set.some((entry) => opIdToHex(entry.property) === SystemIds.NAME_PROPERTY)
  )?.id;

  if (!blockId) {
    throw new Error("Failed to derive the new Properties block id from block ops.");
  }

  const { ops: filterOps } = Graph.updateEntity({
    id: opIdToHex(blockId),
    values: [
      {
        property: FILTER_PROPERTY_ID,
        type: "text",
        value: PROPERTIES_FILTER,
      },
    ],
  });
  ops.push(...filterOps);
}

const proposalName = "Create Week property and Properties block";
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
