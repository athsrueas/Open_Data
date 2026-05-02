---
name: geo-publish
description: Publish entities and relations to the Geo knowledge graph via GRC-20. Use when creating, updating, or deleting entities and relations. Triggers on "publish", "create entity", "add person", "add to geo", "submit proposal", "create relation", "update entity".
metadata:
  author: geobrowser
  version: "1.0.0"
---

# Geo Knowledge Graph — Publishing

Create, update, and delete entities and relations in the Geo knowledge graph using the GRC-20 SDK.

## When to Apply

Reference this skill when:
- Creating new entities (people, companies, events, etc.)
- Adding relations between entities (work history, education, speakers, etc.)
- Updating entity properties or relations
- Deleting relations or entities
- Submitting proposals to DAO or personal spaces

## Prerequisites

- `@geoprotocol/geo-sdk` installed
- `GEO_PRIVATE_KEY` env var set (export from https://www.geobrowser.io/export-wallet)
- Wallet must be an editor of the target DAO space

## Publishing workflow

Every publish follows this flow:

```
1. Discover schema (query existing entities of the same type)
2. Build ops (Graph.createEntity, Graph.createRelation, etc.)
3. Submit (daoSpace.publishAndVote or personalSpace.publishAndSend)
```

### Step 1: Discover the schema

Before creating an entity, **query an existing entity of the same type** to learn what properties and relations it uses. This is essential for any type you haven't worked with before.

```typescript
// Fetch an example entity to see its schema
// IMPORTANT: entities() returns a flat array — do NOT use { nodes { ... } }
// typeId/spaceId are top-level args, NOT nested in a filter object
const res = await fetch("https://testnet-api.geobrowser.io/graphql", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ query: `{
    entities(typeId: "TYPE_ID", first: 1) {
      id name
      values(first: 50) { nodes { property { id name } text date boolean decimal } }
      relations(first: 50) { nodes { type { id name } toEntity { id name } } }
    }
  }`}),
});
const { data } = await res.json();
// data.entities is a flat array: data.entities[0].id, data.entities[0].name, etc.
// Read property IDs, relation type IDs, and classification value IDs from the result
```

Use the discovered IDs to build your ops. Don't guess property or relation IDs.

### Step 2: Build ops

```typescript
import { Graph, TextBlock, Position, SystemIds, ContentIds } from "@geoprotocol/geo-sdk";
import type { Op } from "@geoprotocol/grc-20";

const ops: Op[] = [];

// Create an entity
const { id: entityId, ops: entityOps } = Graph.createEntity({
  name: "Entity Name",                    // must NOT end with a period
  description: "What this entity is.",     // MUST end with a period
  types: [typeId],                         // discovered type ID
  values: [
    { property: propertyId, type: "text", value: "some value" },
    { property: datePropertyId, type: "date", value: "2025-01-15" },
    { property: urlPropertyId, type: "url", value: "https://example.com" },
  ],
});
ops.push(...entityOps);

// Create a relation
const { ops: relOps } = Graph.createRelation({
  fromEntity: entityId,
  toEntity: targetEntityId,
  type: relationTypeId,                    // discovered relation type ID
  toSpace: targetSpaceId,                  // if target is in a different space
});
ops.push(...relOps);

// Update an existing entity
const { ops: updateOps } = Graph.updateEntity({
  id: existingEntityId,
  values: [
    { property: propertyId, type: "text", value: "new value" },
  ],
});
ops.push(...updateOps);

// Delete a relation (use edge ID, NOT entity ID)
const { ops: delOps } = Graph.deleteRelation({ id: relationEdgeId });
ops.push(...delOps);
```

### Step 3: Submit

**To a DAO space** (most spaces):

```typescript
import { daoSpace, getSmartAccountWalletClient } from "@geoprotocol/geo-sdk";

const wallet = await getSmartAccountWalletClient({
  privateKey: process.env.GEO_PRIVATE_KEY as `0x${string}`,
});

const { proposalId, proposeTxHash, voteTxHash } = await daoSpace.publishAndVote({
  name: "Description of this edit",
  ops,
  author: wallet.account.address,
  wallet,
  daoSpaceAddress: "0x..." as `0x${string}`,   // space contract address
  callerSpaceId: "0x..." as `0x${string}`,      // your personal space ID hex
  daoSpaceId: "0x..." as `0x${string}`,         // target space ID hex
  votingMode: "FAST",
  network: "TESTNET",
});
```

**To a personal space:**

```typescript
import { personalSpace, getSmartAccountWalletClient } from "@geoprotocol/geo-sdk";

const wallet = await getSmartAccountWalletClient({
  privateKey: process.env.GEO_PRIVATE_KEY as `0x${string}`,
});

const { editId, cid, txHash } = await personalSpace.publishAndSend({
  name: "Description of this edit",
  spaceId: "your-space-id",
  ops,
  author: "your-person-entity-id",
  wallet,
  network: "TESTNET",
});
```

## Entity rules

- **Names** must NOT end with a period
- **Descriptions** MUST end with a period
- **Dates** use type `"date"` with `YYYY-MM-DD` format (year-only: `YYYY-01-01`)
- **URLs** use type `"url"` for website properties, `"text"` for social handles
- **X/Twitter** must be the handle: `handle`
- **Text blocks**: one paragraph per TextBlock (UI drops everything after first `\n\n`)
- **Batch size**: ~10,000 ops per proposal soft limit

## Relation entities

Relations can carry their own properties. This is used for work history, education, etc. The relation itself becomes an entity with values and sub-relations.

```typescript
const relEntityId = `${personId.slice(0, 16)}${companyId.slice(0, 16)}`;

const { ops: workOps } = Graph.createRelation({
  fromEntity: personId,
  toEntity: companyId,
  type: worksAtRelTypeId,           // discovered from schema
  toSpace: targetSpaceId,
  entityId: relEntityId,            // deterministic ID for the relation entity
  entityName: "Role Title at Company",
  entityValues: [
    { property: startDatePropId, type: "date", value: "2022-03-01" },
  ],
  entityRelations: {
    [rolesRelTypeId]: {              // discovered relation type for roles
      toEntity: roleEntityId,        // discovered role classification value
      toSpace: rolesSpaceId,
    },
  },
});
ops.push(...workOps);
```

## Adding images

```typescript
// Upload to IPFS via SDK
const blob = new Blob([imageBuffer], { type: "image/png" });
const { id: imageId, ops: imageOps } = await Graph.createImage({ blob, name: "Avatar" });
ops.push(...imageOps);

// Link as avatar
const { ops: avatarOps } = Graph.createRelation({
  fromEntity: entityId,
  toEntity: imageId,
  type: ContentIds.AVATAR_PROPERTY,
});
ops.push(...avatarOps);
```

## Adding text blocks (bio, body content)

```typescript
const { ops: block1Ops, position: p1 } = TextBlock.make({
  fromId: entityId,
  text: "First paragraph of content.",
  position: Position.default(),
});
ops.push(...block1Ops);

const { ops: block2Ops } = TextBlock.make({
  fromId: entityId,
  text: "Second paragraph of content.",
  position: Position.after(p1),
});
ops.push(...block2Ops);
```

## SDK ID constants

```typescript
import { SystemIds, ContentIds } from "@geoprotocol/geo-sdk";

// Types
SystemIds.PERSON_TYPE
SystemIds.COMPANY_TYPE
SystemIds.PROJECT_TYPE
SystemIds.EVENT_TYPE
SystemIds.INSTITUTION_TYPE
SystemIds.IMAGE_TYPE
SystemIds.VIDEO_TYPE
SystemIds.ROLE_TYPE
ContentIds.ARTICLE_TYPE
ContentIds.TALK_TYPE
ContentIds.PODCAST_TYPE
ContentIds.EPISODE_TYPE
ContentIds.TOPIC_TYPE
ContentIds.SKILL_TYPE

// Properties
ContentIds.WEBSITE_PROPERTY
ContentIds.X_PROPERTY
ContentIds.GITHUB_PROPERTY
ContentIds.LINKEDIN_PROPERTY
ContentIds.WEB_URL_PROPERTY
ContentIds.PUBLISH_DATE_PROPERTY
ContentIds.AVATAR_PROPERTY
SystemIds.COVER_PROPERTY
SystemIds.START_DATE_PROPERTY
SystemIds.END_DATE_PROPERTY
SystemIds.DATE_FOUNDED_PROPERTY
SystemIds.MARKDOWN_CONTENT

// Relations
SystemIds.WORKS_AT_PROPERTY        // Person -> Company (current)
SystemIds.WORKED_AT_PROPERTY       // Person -> Company (past)
SystemIds.STUDIED_AT_PROPERTY      // Person -> Institution
SystemIds.TEAM_MEMBERS_PROPERTY    // Company -> Person
SystemIds.SPEAKERS_PROPERTY        // Talk/Episode -> Person
SystemIds.CREATOR_PROPERTY         // Entity -> Person
ContentIds.AUTHORS_PROPERTY        // Article -> Person
ContentIds.ROLES_PROPERTY          // Work relation -> Role
ContentIds.SKILLS_PROPERTY         // Person -> Skill
ContentIds.TOPICS_PROPERTY         // Entity -> Topic
ContentIds.LOCATION_PROPERTY       // Entity -> Place
```

For domain-specific IDs (individual roles, degrees, spaces with addresses, etc.), see `scripts/lib/geo-ids.ts`.

## Deleting entities

`Graph.deleteEntity()`
`Graph.deleteRelation({ id: edgeId })` for relations (must use the relation **edge ID** from the GraphQL `id` field, NOT the `entityId`).

## Space config

Space addresses and IDs are in `scripts/lib/geo-ids.ts` under `SPACES`. Each space has:
- `SPACE_ID` — 32-char hex (for GraphQL queries)
- `ADDRESS` — `0x...` contract address (for `daoSpaceAddress`)
- `ID_HEX` — `0x...` bytes16 (for `daoSpaceId` and `callerSpaceId`)
