# Geo Contributor Starter Instructions

## Scope

This folder is a clean Geo contribution workspace for a new curator.
Use it to query Geo, inspect schemas, and publish entities or relations safely.

## Read First

Before doing anything meaningful in this folder, read:
- `README.md`
- `docs/01_setup_guide.md`
- `docs/03_resources_and_sources.md`
- `docs/04_live_setup_notes.md`
- `.codex/skills/geo-query/SKILL.md`
- `.codex/skills/geo-publish/SKILL.md`

## Local Working Rules

- Never print, paste, or commit secrets from `.env`.
- Always verify `.gitignore` contains `.env`.
- Always run `npm run check:setup` before the first publish attempt on a machine.
- If `GEO_TARGET_SPACE_ID` is configured, run `npm run query:space` before creating new schema or content.
- Before publishing a new type, property, or entity shape, inspect an existing example of the same type first.
- Never guess property IDs, relation IDs, or type IDs.
- If publishing to a DAO space, use the DAO proposal flow.
- If publishing to a personal space, use the personal-space flow.
- Names must not end with a period.
- Descriptions should end with a period.
- After creating data blocks, verify in the Geo UI that the block is scoped to the intended space and not accidentally pointing at the wrong source.
- Prefer a dedicated project folder and clean git history over a giant catch-all repo.

## Environment Convention

This starter standardizes on:
- `GEO_PRIVATE_KEY`
- `GEO_WALLET`
- `GEO_PERSONAL_SPACE_ID`
- `GEO_TARGET_SPACE_ID`
- `GEO_TARGET_SPACE_ADDRESS`
- `GEO_TARGET_SPACE_NAME`
- `GEO_TARGET_SPACE_PAGE_ID`
- `GEO_TARGET_SPACE_ENTITY_ID`
- `GEO_TARGET_PAGE_TYPE_ID`

Some upstream demo materials use:
- `PK_SW`
- `DEMO_SPACE_ID`

Map those into this folder's naming instead of mixing conventions.
