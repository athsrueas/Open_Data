# Codex Boot Prompt For A New Curator

Paste this into Codex when starting in this folder:

```text
Use this folder as my Geo onboarding workspace.

Read first:
- README.md
- AGENTS.md
- docs/01_setup_guide.md
- docs/03_resources_and_sources.md
- docs/04_live_setup_notes.md
- .codex/skills/geo-query/SKILL.md
- .codex/skills/geo-publish/SKILL.md

Working rules:
- Never print or expose secrets from .env.
- Never commit .env.
- Verify setup before publishing anything.
- If dependencies are missing, install them.
- Run npm run check:setup first.
- If GEO_TARGET_SPACE_ID is configured, run npm run query:space next.
- Before creating or publishing a new type, property, or entity, inspect an existing example of the same type in the target space or root space.
- Never guess IDs.
- Use the Geo query skill for discovery and the Geo publish skill for publishing.
- If publishing to a DAO space, use the DAO proposal flow.
- If publishing to a personal space, use the personal-space flow.
- After creating any data block, verify the block filter or data source is scoped to the intended space.

My current task is:
[replace this line with the actual task]
```

## Good First Prompt

If someone just wants to verify setup, they can paste:

```text
Use this Geo starter folder to get me fully set up as a new curator.
Verify the .env, install dependencies if needed, run the setup check, and summarize whether I am ready to query and publish in Geo.
Do not expose any secrets.
```

## Good First Publish Prompt

```text
Use the Geo query and Geo publish skills in this folder.
Inspect the target space schema first, then help me create one safe first contribution.
Show me the exact publish plan before you submit anything onchain.
```
