# Live Setup Notes

This file condenses the practical lessons from the live setup session into a reusable playbook.

## What Was Actually Done In The Session

1. Open Geo and locate the working space.
2. Use `export-wallet`.
3. Create a local `.env`.
4. Create a local `.gitignore`.
5. Put `.env` in `.gitignore`.
6. Put wallet details in `.env`.
7. Add the Geo skills under `.codex/skills/`.
8. Open Codex in the folder.
9. Give Codex the target space ID.
10. Let Codex install the SDK stack and create the first Geo objects.

## The Exact Setup Pattern That Mattered

### 1. The Private Key Lives In `.env`

The private key was intentionally put into `.env` so Codex could use it locally.

Operational rule:
- local only
- never committed
- never shared between people

### 2. `.gitignore` Is Not Optional

The live session explicitly added `.env` to `.gitignore`.

That should always be present before any git commit.

### 3. The Skills Folder Matters

The two key skills were:
- `geo-query`
- `geo-publish`

They were placed under:
- `.codex/skills/geo-query`
- `.codex/skills/geo-publish`

That gave Codex reusable instructions for:
- querying the graph
- discovering schema
- publishing through the Geo SDK

### 4. A Dedicated Project Folder Is Better Than A Giant Catch-All Repo

One strong lesson from the session:
- a giant mixed folder makes git and setup harder
- a small dedicated project folder makes Codex much more reliable

This kit is built around that lesson.

### 5. Give Codex The Space ID, Not Just The Name

The session used the actual target space ID.
That reduced ambiguity and helped Codex wire the scripts correctly.

### 6. The First Useful Publish Sequence Was

- create a `Week` type
- create a `Week` relation property
- create a `Learn` tab with `Courses` and `Lessons` data blocks

That sequence is why the example scripts are included here.

### 7. Data Blocks Need A UI Check

There was a small tweak after publishing:
- the data block source or filter had to be corrected so it pointed to the intended space

Practical rule:
- whenever Codex creates a data block, open the Geo UI and verify it is scoped correctly

### 8. After A Successful Flow, The Instructions Should Be Promoted

The important advice from the session was effectively:
- once the workflow works in a curator's environment, keep the improved instructions
- refine the skills or local guidance so the next run is faster

That is why this kit includes:
- `AGENTS.md`
- skills
- setup scripts
- a Codex boot prompt

## Recommended First Real Use For A New Curator

The best first run is not a large publish.
It is:
- verify the wallet
- verify the personal space
- inspect the target space
- make one small safe contribution
- confirm it in Geo UI
