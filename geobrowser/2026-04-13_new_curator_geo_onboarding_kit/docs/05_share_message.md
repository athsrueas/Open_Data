# Share Message

Hi,

This zip is a clean Geo onboarding kit so your Codex can help you query and publish in Geo with a local setup that is already structured the right way.

Please do this in order:

1. Open the folder in VS Code.
2. Copy `.env.example` to `.env`.
3. In Geo, open [export-wallet](https://www.geobrowser.io/export-wallet).
4. Put your own wallet and private-key values into `.env`.
5. Make sure `.env` stays ignored by git.
6. Run `npm install`.
7. Run `npm run check:setup`.
8. If you already know the space you want to contribute to, fill the `GEO_TARGET_SPACE_*` values in `.env`.
9. Run `npm run query:space`.
10. Open Codex in this folder and paste the prompt from `PROMPT_TO_PASTE_INTO_CODEX.txt`.

Important:
- use your own private key only on your own machine
- do not commit `.env`
- let Codex inspect the existing schema before it publishes anything

The main docs to read are:
- `README.md`
- `docs/01_setup_guide.md`
- `docs/02_codex_boot_prompt.md`
- `docs/03_resources_and_sources.md`

This folder already includes the Geo skills under `.codex/skills/`.
