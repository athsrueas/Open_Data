# New Curator Geo Setup Guide

## Goal

Get a new curator to the point where:
- VS Code is set up
- Codex has the Geo skills
- their wallet is available locally through `.env`
- `.env` is safely ignored by git
- they can verify their personal space
- they can inspect a target space before publishing

## Step 1. Use A Clean Folder

Open this starter folder in VS Code.

Why:
- it already contains the Geo skills
- it already contains `.gitignore`
- it already contains Codex instructions in `AGENTS.md`
- it avoids the messy "one giant workspace for everything" problem that came up in the live session

## Step 2. Create `.env`

In VS Code:
1. Duplicate `.env.example`.
2. Rename the duplicate to `.env`.
3. Open `.env`.
4. Fill in the curator's own wallet values.

Minimum required value:
- `GEO_PRIVATE_KEY`

Useful optional values:
- `GEO_WALLET`
- `GEO_PERSONAL_SPACE_ID`
- `GEO_TARGET_SPACE_ID`
- `GEO_TARGET_SPACE_ADDRESS`
- `GEO_TARGET_SPACE_NAME`
- `GEO_TARGET_SPACE_ENTITY_ID`
- `GEO_TARGET_PAGE_TYPE_ID`

## Step 3. Export Wallet From Geo

Use:
- [Geo export-wallet](https://www.geobrowser.io/export-wallet)

What the curator should do:
1. Log into Geo with their own account.
2. Open `export-wallet`.
3. Copy the wallet reference if useful into `GEO_WALLET`.
4. Copy the private key into `GEO_PRIVATE_KEY`.

Important:
- the curator should keep this local on their machine
- they should not send the key in chat
- they should not commit it to GitHub

## Step 4. Confirm `.gitignore`

This folder already ignores `.env`.

Check that `.gitignore` still contains:

```gitignore
.env
```

That is the minimum requirement so the private key is not committed.

## Step 5. Install Dependencies

From the terminal in this folder:

```sh
npm install
```

This installs the same basic SDK stack used in the working Geo setup:
- `@geoprotocol/geo-sdk`
- `@geoprotocol/grc-20`
- `dotenv`
- `viem`

## Step 6. Verify The Wallet And Personal Space

Run:

```sh
npm run check:setup
```

This will:
- normalize the private key
- derive the smart-account address
- check whether a personal space already exists
- derive the personal-space ID if it exists
- print a clean JSON summary

If it says no personal space exists yet, the curator should create one in Geo before trying to publish from Codex.

## Step 7. Add The Target Space

If the curator already knows the space they want to contribute to, fill:
- `GEO_TARGET_SPACE_ID`
- `GEO_TARGET_SPACE_ADDRESS`
- `GEO_TARGET_SPACE_NAME`
- `GEO_TARGET_SPACE_ENTITY_ID`

Optional but helpful:
- `GEO_TARGET_PAGE_TYPE_ID`

Then run:

```sh
npm run query:space
```

This gives Codex a quick summary of:
- the target space
- types found in it
- properties found in it
- pages found in it
- data blocks found in it

That is the right first step before creating new schema or content.

If the curator plans to create pages or data blocks in a DAO space, `GEO_TARGET_SPACE_ENTITY_ID` usually matters as much as `GEO_TARGET_SPACE_ID`.
Codex can often discover it by querying the space first.

## Step 8. Use Codex In This Folder

Open Codex with this folder as the working directory and paste:
- [PROMPT_TO_PASTE_INTO_CODEX.txt](/Users/Music/Documents/Codex/projects/geo/outputs/2026-04-13_new_curator_geo_onboarding_kit/PROMPT_TO_PASTE_INTO_CODEX.txt)

Because this folder also contains:
- `AGENTS.md`
- `.codex/skills/geo-query`
- `.codex/skills/geo-publish`

Codex should be able to handle:
- setup checks
- schema discovery
- query tasks
- publish scripts
- proposal creation

## Step 9. First Real Contribution Pattern

The safest sequence is:
1. inspect existing types and properties in the target space
2. inspect one existing entity of the same type they want to create
3. write the publish script
4. dry-run if possible
5. publish
6. verify in Geo UI
7. if a data block was created, confirm the block source and filter are actually scoped correctly

## Step 10. Git Hygiene

Once setup is done, the curator should commit the starter files without `.env`.

Good rule:
- one clean repo per project or Geo task cluster
- not one giant workspace full of unrelated material
