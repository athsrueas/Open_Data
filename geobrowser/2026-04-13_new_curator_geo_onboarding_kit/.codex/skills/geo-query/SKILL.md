---
name: geo-query
description: Query the Geo knowledge graph via GraphQL. Use when looking up entities, searching by type, exploring relations, discovering schemas, or inspecting entity properties. Triggers on "look up", "find entity", "query geo", "search the graph", "what type is", "show me relations", "get entity".
metadata:
  author: geobrowser
  version: "1.1.0"
---

# Geo Knowledge Graph — Querying

Query and explore entities, types, properties, and relations in the Geo knowledge graph via its GraphQL API.

## When to Apply

Reference this skill when:
- Looking up an entity by ID
- Searching for entities of a given type in a space
- Exploring what properties and relations an entity has
- Discovering the schema for an unfamiliar entity type
- Finding type, property, or relation type IDs

## API

- **Endpoint:** `https://testnet-api.geobrowser.io/graphql`
- **Method:** POST with `Content-Type: application/json`
- **Auth:** None required
- **Browser:** `https://www.geobrowser.io/space/{spaceId}/{entityId}`

## CRITICAL: Correct query patterns

**ALWAYS use `entities` (not `entitiesConnection`) as your default list query.** It returns a **flat array** — do NOT wrap fields in `{ nodes { ... } }`.

**CORRECT:**
```graphql
{ entities(typeId: "TYPE_ID", first: 50) { id name description } }
```
→ Returns: `{ "data": { "entities": [ { "id": "...", "name": "..." } ] } }`

**WRONG — will cause a GraphQL error:**
```graphql
{ entities(typeId: "TYPE_ID", first: 50) { nodes { id name } } }
```

**WRONG — `typeIds` is a top-level arg, not nested in filter:**
```graphql
{ entities(filter: { typeIds: { anyEqualTo: "TYPE_ID" } }, first: 50) { ... } }
```

### `entities` vs `entitiesConnection`

| | `entities` | `entitiesConnection` |
|---|---|---|
| Return shape | flat array | `{ nodes, edges, pageInfo, totalCount }` |
| Pagination | `first` + `offset` only | `first`/`offset` + cursor (`after`/`before`/`last`) |
| Use when | default, simple listing | need `totalCount` or cursor pagination |

Both use the same **top-level args**: `typeId`, `spaceId`, `typeIds`, `spaceIds`, `filter`, `first`, `offset`, `orderBy`.

`entitiesConnection` example:
```graphql
{
  entitiesConnection(typeId: "TYPE_ID", first: 50) {
    totalCount
    nodes { id name description }
    pageInfo { hasNextPage endCursor }
  }
}
```

## Core queries

### Get a single entity (start here for any lookup)

```graphql
{
  entity(id: "ENTITY_ID") {
    id
    name
    description
    spaceIds
    types { id name }
    values(first: 100) {
      nodes {
        property { id name }
        text
        date
        boolean
        decimal
        integer
        float
      }
    }
    relations(first: 100) {
      nodes {
        id          # relation edge ID (for deletion)
        entityId    # relation entity ID (for updating relation properties)
        type { id name }
        toEntity { id name }
      }
    }
  }
}
```

Values come back as typed fields (`text`, `date`, `boolean`, `decimal`, `integer`, `float`) — NOT a single `value` field. Check each field for non-null.

### Search entities by type

```graphql
{
  entities(typeId: "TYPE_ID", first: 50) {
    id name description
  }
}
```

### Search entities by type within a space

```graphql
{
  entities(typeId: "TYPE_ID", spaceId: "SPACE_ID", first: 50) {
    id name description
  }
}
```

### Get a space

```graphql
{
  space(id: "SPACE_ID") { id address }
}
```

## Advanced filtering

The `filter` arg accepts an `EntityFilter` object for field-level conditions:

```graphql
{
  entities(typeId: "TYPE_ID", filter: { name: { startsWithInsensitive: "Bitcoin" } }, first: 20) {
    id name
  }
}
```

Available `EntityFilter` fields:
- `id` — UUIDFilter
- `name` — StringFilter (supports `startsWithInsensitive`, `includesInsensitive`, `equalTo`, etc.)
- `description` — StringFilter
- `createdAt`, `updatedAt` — StringFilter
- `spaceIds` — UUIDListFilter (`anyEqualTo`)
- `typeIds` — UUIDListFilter (`anyEqualTo`)
- `relations`, `backlinks` — EntityToManyRelationFilter
- `values` — EntityToManyValueFilter
- `and`, `or`, `not` — combine filters

## Schema discovery workflow

When you need to publish or understand an entity type you haven't seen before, **inspect an existing entity of that type** to learn the schema:

1. **Find entities of the type** — search by type ID
2. **Pick one and fetch it fully** — get all values and relations
3. **Read the property names and relation types** — these tell you the schema
4. **Note the IDs** — property IDs, relation type IDs, and toEntity IDs for classification values

Example: to understand how "Talk" entities work, find one and inspect it:

```graphql
{
  entities(typeId: "86db141cf7cb471194ed39088926adb8", first: 3) {
    id name
    types { id name }
    values(first: 50) { nodes { property { id name } text date } }
    relations(first: 50) { nodes { type { id name } toEntity { id name } } }
  }
}
```

This reveals what properties and relations Talk entities have, their IDs, and example values — everything needed to create new ones.

## Discovering type and property IDs

If you don't know a type ID, search by name among all Type entities:

```graphql
{
  entities(typeId: "e7d737c536764c609fa16aa64a8c90ad", first: 200) {
    id name
  }
}
```

`e7d737c536764c609fa16aa64a8c90ad` is the "Type" type — this returns all type definitions.

To find a specific type by name, add a filter:

```graphql
{
  entities(typeId: "e7d737c536764c609fa16aa64a8c90ad", filter: { name: { includesInsensitive: "article" } }, first: 20) {
    id name
  }
}
```

Similarly, `808a04ceb21c4d888ad12e240613e5ca` is the "Property" type — search it the same way.

For relation types, inspect the relations on an entity that uses them — the `type { id name }` field gives you the relation type ID and name.

## Well-known spaces

| Space | ID |
|-------|-----|
| Root | `a19c345ab9866679b001d7d2138d88a1` |
| Crypto | `c9f267dcb0d270718c2a3c45a64afd32` |
| AI | `41e851610e13a19441c4d980f2f2ce6b` |
| Health | `52c7ae149838b6d47ce0f3b2a5974546` |
| Education | `ec349623f33236aee13c12dcd629ee81` |
| Industries | `d69608290513c2a91102c939b3265bd7` |
| Places | `84a679ce188f061ac9a92380bac2bab5` |
| Technology | `870e3b3068661e6280fad2ab456829bc` |
| Software | `9b611b848b12491b9b6b43f3cf019b8b` |
| Finance | `c5729fc78c2de3a0ae948ca1df489e8d` |

## Well-known type IDs

Available from `@geoprotocol/geo-sdk`:

```typescript
import { SystemIds, ContentIds } from "@geoprotocol/geo-sdk";

SystemIds.PERSON_TYPE       // Person
SystemIds.COMPANY_TYPE      // Company
SystemIds.PROJECT_TYPE      // Project
SystemIds.EVENT_TYPE        // Event
SystemIds.INSTITUTION_TYPE  // Institution (education)
ContentIds.ARTICLE_TYPE     // Article
ContentIds.TALK_TYPE        // Talk
ContentIds.PODCAST_TYPE     // Podcast
ContentIds.EPISODE_TYPE     // Episode
ContentIds.TOPIC_TYPE       // Topic
ContentIds.SKILL_TYPE       // Skill
```

Key type IDs discovered via introspection:
- `e7d737c536764c609fa16aa64a8c90ad` — Type (meta-type for all type definitions)
- `808a04ceb21c4d888ad12e240613e5ca` — Property (meta-type for property definitions)
- `a2a5ed0cacef46b1835de457956ce915` — Articles
- `4e22a7b291e94c9cad90992ccb6f2d6c` — Stories
- `96f859efa1ca4b229372c86ad58b694b` — Claim
- `5ef5a5860f274d8e8f6c59ae5b3e89e2` — Topic
- `4faff0b210cb49958e20109409b8699c` — Person
- `4d0076ff1e824585b03066f6bf6420ce` — Project

For domain-specific IDs not in the SDK, check `scripts/lib/geo-ids.ts`.

## Pagination

Use `first` and `offset` for pagination:

```graphql
{
  entities(typeId: "TYPE_ID", first: 100, offset: 100) {
    id name
  }
}
```

Or use `entitiesConnection` for cursor-based pagination:

```graphql
{
  entitiesConnection(typeId: "TYPE_ID", first: 100, after: "CURSOR") {
    nodes { id name }
    pageInfo { hasNextPage endCursor }
  }
}
```

## curl example

```bash
curl -s --compressed 'https://testnet-api.geobrowser.io/graphql' \
  -H 'Content-Type: application/json' \
  -d '{"query":"{ entities(typeId: \"TYPE_ID\", first: 20) { id name description } }"}' | jq .
```

Full entity lookup:

```bash
curl -s --compressed 'https://testnet-api.geobrowser.io/graphql' \
  -H 'Content-Type: application/json' \
  -d '{"query":"{ entity(id: \"ENTITY_ID\") { id name types { name } values(first: 50) { nodes { property { name } text date } } relations(first: 50) { nodes { type { name } toEntity { name } } } } }"}' | jq .
```
