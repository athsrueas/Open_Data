import dotenv from "dotenv";

import { createPublicClient, http } from "viem";
import {
  DataBlock,
  Graph,
  Position,
  SystemIds,
  TESTNET_RPC_URL,
  TextBlock,
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
const TARGET_PAGE_TYPE_ID = process.env.GEO_TARGET_PAGE_TYPE_ID || null;
const SPACE_NAME = process.env.GEO_TARGET_SPACE_NAME || "Target space";

if (!GEO_PRIVATE_KEY) throw new Error("Missing GEO_PRIVATE_KEY in environment.");
if (!TARGET_SPACE_ID) throw new Error("Missing GEO_TARGET_SPACE_ID in environment.");
if (!TARGET_SPACE_ADDRESS) {
  throw new Error("Missing GEO_TARGET_SPACE_ADDRESS in environment.");
}
if (!TARGET_SPACE_ENTITY_ID) {
  throw new Error("Missing GEO_TARGET_SPACE_ENTITY_ID in environment.");
}

const COURSE_TYPE_ID = "ae724b5687254a098d7ea542bc587ebd";
const LESSON_TYPE_ID = "1baae8e9187041fb8e2a1eb1f84ba0d4";

const LEARN_PAGE_NAME = "Learn";
const LEARN_PAGE_DESCRIPTION =
  "Discover courses and lessons available in this space.";
const INTRO_TEXT =
  "Discover courses and lessons available in this space.";

const COURSES_BLOCK_NAME = "Courses";
const LESSONS_BLOCK_NAME = "Lessons";
const COURSES_FILTER = JSON.stringify({
  spaceId: { in: [TARGET_SPACE_ID] },
  filter: {
    [SystemIds.TYPES_PROPERTY]: { is: COURSE_TYPE_ID },
  },
});
const LESSONS_FILTER = JSON.stringify({
  spaceId: { in: [TARGET_SPACE_ID] },
  filter: {
    [SystemIds.TYPES_PROPERTY]: { is: LESSON_TYPE_ID },
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

async function findPageByName(name) {
  const entities = await getSpaceEntities();
  return entities.find(
    (entity) =>
      entity.name === name && entity.typeIds?.includes(SystemIds.PAGE_TYPE)
  );
}

async function findBlockByName(name) {
  const entities = await getSpaceEntities();
  return entities.find(
    (entity) =>
      entity.name === name && entity.typeIds?.includes(SystemIds.DATA_BLOCK)
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
const existingLearnPage = await findPageByName(LEARN_PAGE_NAME);
const existingCoursesBlock = await findBlockByName(COURSES_BLOCK_NAME);
const existingLessonsBlock = await findBlockByName(LESSONS_BLOCK_NAME);

if (existingLearnPage && existingCoursesBlock && existingLessonsBlock) {
  console.log(
    JSON.stringify(
      {
        ok: true,
        skipped: true,
        reason: "Learn page and both blocks already exist.",
        learnPageId: existingLearnPage.id,
        coursesBlockId: existingCoursesBlock.id,
        lessonsBlockId: existingLessonsBlock.id,
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
let learnPageId = existingLearnPage?.id;
let blockAnchorId = existingLearnPage?.id;

if (!existingLearnPage) {
  const pageRelations = TARGET_PAGE_TYPE_ID
    ? {
        [SystemIds.PAGE_TYPE_PROPERTY]: {
          toEntity: TARGET_PAGE_TYPE_ID,
        },
      }
    : {};

  const { id, ops: pageOps } = Graph.createEntity({
    name: LEARN_PAGE_NAME,
    description: LEARN_PAGE_DESCRIPTION,
    types: [SystemIds.PAGE_TYPE],
    relations: pageRelations,
  });
  learnPageId = id;
  blockAnchorId = id;
  ops.push(...pageOps);

  const { ops: tabOps } = Graph.createRelation({
    fromEntity: TARGET_SPACE_ENTITY_ID,
    toEntity: id,
    type: SystemIds.TABS_PROPERTY,
  });
  ops.push(...tabOps);

  const introOps = TextBlock.make({
    fromId: id,
    text: INTRO_TEXT,
    position: Position.generate(),
  });
  ops.push(...introOps);
}

const blockTargets = [];

if (!existingCoursesBlock) {
  const coursesOps = DataBlock.make({
    fromId: blockAnchorId,
    sourceType: "QUERY",
    position: Position.generate(),
    name: COURSES_BLOCK_NAME,
  });
  ops.push(...coursesOps);

  const coursesId = opIdToHex(
    coursesOps.find(
      (op) =>
        op.type === "updateEntity" &&
        Array.isArray(op.set) &&
        op.set.some((entry) => opIdToHex(entry.property) === SystemIds.NAME_PROPERTY)
    )?.id
  );

  if (!coursesId) throw new Error("Failed to derive Courses block id.");
  blockTargets.push({
    id: coursesId,
    filter: COURSES_FILTER,
  });

  const { ops: galleryOps } = Graph.createRelation({
    fromEntity: coursesId,
    toEntity: SystemIds.GALLERY_VIEW,
    type: SystemIds.VIEW_PROPERTY,
  });
  ops.push(...galleryOps);
}

if (!existingLessonsBlock) {
  const lessonsOps = DataBlock.make({
    fromId: blockAnchorId,
    sourceType: "QUERY",
    position: Position.generate(),
    name: LESSONS_BLOCK_NAME,
  });
  ops.push(...lessonsOps);

  const lessonsId = opIdToHex(
    lessonsOps.find(
      (op) =>
        op.type === "updateEntity" &&
        Array.isArray(op.set) &&
        op.set.some((entry) => opIdToHex(entry.property) === SystemIds.NAME_PROPERTY)
    )?.id
  );

  if (!lessonsId) throw new Error("Failed to derive Lessons block id.");
  blockTargets.push({
    id: lessonsId,
    filter: LESSONS_FILTER,
  });
}

for (const blockTarget of blockTargets) {
  const { ops: filterOps } = Graph.updateEntity({
    id: blockTarget.id,
    values: [
      {
        property: SystemIds.FILTER,
        type: "text",
        value: blockTarget.filter,
      },
    ],
  });
  ops.push(...filterOps);
}

const proposalName = "Create Learn page with Courses and Lessons blocks";
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
        learnPageId,
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
      learnPageId,
    },
    null,
    2
  )
);
