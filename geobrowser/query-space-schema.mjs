import { fileURLToPath } from "node:url";
import dotenv from "dotenv";

import { SystemIds } from "@geoprotocol/geo-sdk";

dotenv.config({
  path: fileURLToPath(new URL("../.env", import.meta.url)),
});

const targetSpaceId = process.env.GEO_TARGET_SPACE_ID;

if (!targetSpaceId) {
  console.error(
    "Missing GEO_TARGET_SPACE_ID. Add it to .env before querying a target space."
  );
  process.exit(1);
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

const data = await gql(`{
  space(id: "${targetSpaceId}") {
    id
    address
  }
  entities(spaceId: "${targetSpaceId}", first: 300) {
    id
    name
    typeIds
  }
}`);

const entities = data.entities ?? [];

const byType = (typeId) =>
  entities
    .filter((entity) => entity.typeIds?.includes(typeId))
    .map((entity) => ({ id: entity.id, name: entity.name }))
    .sort((a, b) => a.name.localeCompare(b.name));

const types = byType(SystemIds.SCHEMA_TYPE);
const properties = byType(SystemIds.PROPERTY);
const pages = byType(SystemIds.PAGE_TYPE);
const dataBlocks = byType(SystemIds.DATA_BLOCK);

const summary = {
  space: {
    id: data.space?.id ?? targetSpaceId,
    address: data.space?.address ?? null,
    configuredName: process.env.GEO_TARGET_SPACE_NAME || null,
  },
  totals: {
    entities: entities.length,
    types: types.length,
    properties: properties.length,
    pages: pages.length,
    dataBlocks: dataBlocks.length,
  },
  types,
  properties,
  pages,
  dataBlocks,
};

console.log(JSON.stringify(summary, null, 2));
