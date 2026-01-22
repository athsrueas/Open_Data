# Public Data Task List

Use this checklist to pick small, discrete tasks inspired by `docs/PD-Initiatives-for-Public-Good.md`.

## Metadata & Cataloging
- [ ] Normalize a dataset catalog to a minimal metadata shape (`id`, `title`, `description`, `license`, `resources`).
- [ ] Build a CSV index of datasets with `id`, `title`, `license`, and resource count.
- [ ] Audit datasets for missing required fields and summarize gaps.

## Health
- [ ] Create a `health_overlay.geojson` by joining disease rates to infrastructure data.
- [ ] Produce a short `health-metadata-audit.md` covering license + update cadence.

## AI
- [ ] Draft a `dataset-card.md` for one open training dataset.
- [ ] Map five datasets to AI use cases in `ai-use-cases.csv`.

## Education
- [ ] Harmonize 10 indicators into `education-indicators.csv`.
- [ ] Visualize access gaps in `access-gaps.png`.
- [ ] Review education facilities datasets (NCES School Locations, NCES CCD, state school facility inventories) and log sources in `education-sources.md`.
- [ ] Gather public construction datasets (USASpending construction awards, State DOT/school capital plans, municipal open data capital project lists) in `construction-sources.md`.

## World Affairs
- [ ] Create `crisis-index.csv` for three humanitarian crises.
- [ ] Audit IATI samples and record missing fields in `aid-audit.md`.

## Politics & Open Government
- [ ] Assemble `budget-index.csv` with year, agency, and license.
- [ ] Summarize policy impacts in `policy-impact.md`.

## Geo Publishing (DataRepublican-style)
- [ ] Download a raw spending or grant dataset and record the source URLs in `geo-sources.md`.
- [ ] Normalize organization names, EINs, and addresses into `orgs-normalized.csv`.
- [ ] Deduplicate recipients by EIN + normalized name, producing `recipients-deduped.csv`.
- [ ] Geocode recipient addresses and export `recipients.geojson` with coordinates + metadata.
- [ ] Join grants to recipients (EIN or name match) and publish `grants-joined.csv`.
- [ ] Build a lightweight inverted index over recipient names and locations in `recipient-index.json`.
- [ ] Export a publish-ready bundle (`recipients.geojson`, `grants-joined.csv`, `recipient-index.json`) in `geo-release/`.

## Crypto & Decentralized Data
- [ ] Build `onchain-index.csv` for 10 public-interest contracts.
- [ ] Summarize DID use cases and risks in `did-summary.md`.
