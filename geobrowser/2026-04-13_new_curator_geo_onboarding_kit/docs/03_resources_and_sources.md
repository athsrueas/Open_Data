# Resources And Sources

This is the curated source pack behind the onboarding kit.

## 1. Notion Reference Database

Link:
- [All the types and properties](https://www.notion.so/33b273e214eb80f9821eee52035c1315?v=cbff1e8d823641a7b908f1556266e62d)

What it is:
- a Notion database titled `All the types and properties`
- organized by a `Space` field
- includes views for `Geo (Root)`, `Crypto`, `AI`, `Health`, `Podcast`, `Industries`, `Software`, and `Technology`

How to use it:
- use it as a fast browsing and reference surface
- do not treat it as the final source of live IDs
- always verify live IDs in Geo before publishing

## 2. Geo SDK README

Link:
- [geo-sdk README](https://github.com/geobrowser/geo-sdk/blob/main/README.md)

What it gives a new curator:
- the install pattern for `@geoprotocol/geo-sdk`
- the Geo model: spaces, entities, relations, ops, edits
- helper APIs like `Graph.createEntity`, `Graph.createProperty`, `Graph.createType`, `Graph.createImage`
- the smart-account publishing flow
- the `export-wallet` reminder and private-key caution

Most relevant setup takeaway:
- Geo account publishing in code depends on the exported private key and a working smart-account client

## 3. GRC-20 Spec

Link:
- [grc-20 spec](https://github.com/geobrowser/grc-20/blob/main/spec.md)

What it clarifies:
- Geo uses a property-graph model
- relations are first-class and can carry their own attributes
- edits are batches of ops
- spaces are governance containers
- the root vocabulary includes core entity properties, relation semantics, and data-type conventions

Why it matters for a new curator:
- it explains the underlying shape Codex is publishing into
- it makes it easier to understand why querying schema first is important

## 4. Geo Tech Demo Repo

Link:
- [geo_tech_demo](https://github.com/geobrowser/geo_tech_demo)

What it is:
- a public repo described as `Tech demo scripts for Geo Curator program onboarding`

What it contains:
- `.env.example`
- `.gitignore`
- `01_api_demo.ts`
- `02_publish_demo.ts`
- `03_delete_demo.ts`
- a README that walks through overview, publishing, querying, and cleanup

Most relevant takeaway:
- this repo confirms the basic onboarding shape:
  - local `.env`
  - local `.gitignore`
  - SDK install
  - demo query flow
  - demo publish flow

## 5. Live Geo Example Link

Link:
- [Space content policies](https://www.geobrowser.io/space/3be38bb922bc80c6a6503fbbba28d2b0/dd5546417d00442fb353c7b10f8b7163)

How to use it:
- as a live UI example of how a Geo space or page can look
- as a reminder to verify results in the browser after Codex publishes

## 6. Working Local Templates Included In This Kit

Included here:
- [examples/generic-dao-space/publish-week-type.mjs](/Users/Music/Documents/Codex/projects/geo/outputs/2026-04-13_new_curator_geo_onboarding_kit/examples/generic-dao-space/publish-week-type.mjs)
- [examples/generic-dao-space/publish-week-property.mjs](/Users/Music/Documents/Codex/projects/geo/outputs/2026-04-13_new_curator_geo_onboarding_kit/examples/generic-dao-space/publish-week-property.mjs)
- [examples/generic-dao-space/publish-learn-tab.mjs](/Users/Music/Documents/Codex/projects/geo/outputs/2026-04-13_new_curator_geo_onboarding_kit/examples/generic-dao-space/publish-learn-tab.mjs)

What these show:
- a generic DAO-space proposal flow
- a generic type creation example
- a generic relation-property creation example
- a generic page and data-block creation example

## Naming Convention Note

The public demo repo uses:
- `PK_SW`
- `DEMO_SPACE_ID`

This kit uses:
- `GEO_PRIVATE_KEY`
- `GEO_WALLET`
- `GEO_PERSONAL_SPACE_ID`
- `GEO_TARGET_SPACE_ID`

That is intentional.
It keeps the setup clearer while still mapping cleanly to the original demo materials.
