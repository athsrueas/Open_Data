# New Curator Geo Onboarding Kit

This folder is a sanitized, reusable onboarding kit for getting a new curator or contributor set up to work in Geo with Codex and VS Code.

It packages four things together:
- the practical setup flow used in the live session
- the reusable Geo skills for querying and publishing
- the primary Geo source references
- a clean local project shape so Codex can help a new curator query and publish right away

## Quick Start

1. Open this folder in VS Code.
2. Copy `.env.example` to `.env`.
3. Fill `.env` with the curator's own Geo wallet details.
4. Confirm `.gitignore` includes `.env`.
5. Run `npm install`.
6. Run `npm run check:setup`.
7. If the curator already knows the target Geo space, fill the `GEO_TARGET_SPACE_*` values in `.env`.
8. Run `npm run query:space`.
9. Open Codex in this folder and paste the prompt in [PROMPT_TO_PASTE_INTO_CODEX.txt](/Users/Music/Documents/Codex/projects/geo/outputs/2026-04-13_new_curator_geo_onboarding_kit/PROMPT_TO_PASTE_INTO_CODEX.txt).

## Important Security Rule

Each curator should export and use their own wallet and private key on their own machine.
Do not share your own private key with them.
Do not commit `.env`.

## Folder Map

- [AGENTS.md](/Users/Music/Documents/Codex/projects/geo/outputs/2026-04-13_new_curator_geo_onboarding_kit/AGENTS.md): local instructions so Codex behaves correctly in this folder
- [.env.example](/Users/Music/Documents/Codex/projects/geo/outputs/2026-04-13_new_curator_geo_onboarding_kit/.env.example): the environment template a curator should copy locally
- [.gitignore](/Users/Music/Documents/Codex/projects/geo/outputs/2026-04-13_new_curator_geo_onboarding_kit/.gitignore): keeps secrets and generated files out of git
- [PROMPT_TO_PASTE_INTO_CODEX.txt](/Users/Music/Documents/Codex/projects/geo/outputs/2026-04-13_new_curator_geo_onboarding_kit/PROMPT_TO_PASTE_INTO_CODEX.txt): the single copy-paste prompt for Codex
- [docs/01_setup_guide.md](/Users/Music/Documents/Codex/projects/geo/outputs/2026-04-13_new_curator_geo_onboarding_kit/docs/01_setup_guide.md): step-by-step setup in plain English
- [docs/02_codex_boot_prompt.md](/Users/Music/Documents/Codex/projects/geo/outputs/2026-04-13_new_curator_geo_onboarding_kit/docs/02_codex_boot_prompt.md): the same prompt in markdown form
- [docs/03_resources_and_sources.md](/Users/Music/Documents/Codex/projects/geo/outputs/2026-04-13_new_curator_geo_onboarding_kit/docs/03_resources_and_sources.md): the external references and what each is for
- [docs/04_live_setup_notes.md](/Users/Music/Documents/Codex/projects/geo/outputs/2026-04-13_new_curator_geo_onboarding_kit/docs/04_live_setup_notes.md): the reusable lessons from the live setup session
- [docs/05_share_message.md](/Users/Music/Documents/Codex/projects/geo/outputs/2026-04-13_new_curator_geo_onboarding_kit/docs/05_share_message.md): a ready-to-forward note you can send with the zip
- [scripts/check-geo-setup.mjs](/Users/Music/Documents/Codex/projects/geo/outputs/2026-04-13_new_curator_geo_onboarding_kit/scripts/check-geo-setup.mjs): verifies wallet and personal-space readiness
- [scripts/query-space-schema.mjs](/Users/Music/Documents/Codex/projects/geo/outputs/2026-04-13_new_curator_geo_onboarding_kit/scripts/query-space-schema.mjs): summarizes types and properties in a target space
- [.codex/skills/geo-query/SKILL.md](/Users/Music/Documents/Codex/projects/geo/outputs/2026-04-13_new_curator_geo_onboarding_kit/.codex/skills/geo-query/SKILL.md): Geo query skill
- [.codex/skills/geo-publish/SKILL.md](/Users/Music/Documents/Codex/projects/geo/outputs/2026-04-13_new_curator_geo_onboarding_kit/.codex/skills/geo-publish/SKILL.md): Geo publish skill
- [examples/generic-dao-space/README.md](/Users/Music/Documents/Codex/projects/geo/outputs/2026-04-13_new_curator_geo_onboarding_kit/examples/generic-dao-space/README.md): generic publish templates for DAO spaces

## Recommended First Task For A New Curator

Have Codex do this in order:
- verify `.env`
- run `npm install`
- run `npm run check:setup`
- run `npm run query:space`
- inspect one existing entity of the same type they want to create
- only then build and publish the first change
