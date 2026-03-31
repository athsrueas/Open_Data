# Public Data Task List

Use this checklist to pick small, discrete tasks inspired by `docs/PD-Initiatives-for-Public-Good.md`.

## Active bounty
- [ ] Educational Inequality Map is the active bounty for current research and source discovery.
- [ ] Meet with Armando on March 31, 2026 and get the real ontology before locking the graph model.
- [ ] Keep ontology work provisional until Armando's ontology guidance is captured in-repo.
- [ ] Build `docs/Bounties/educational-inequality-map-sources.md` into a Phase 1 ingest plan.
- [ ] Define the minimum country-year schema for access, funding, literacy, and outcomes.
- [ ] Choose the first comparison-ready indicator set and extraction order.
- [ ] Turn the staged source bundle into a map-ready Phase 1 visualization contract.
- [ ] Define the first country detail and compare-panel UX around Phase 1 metrics.
- [ ] Backfill adult literacy equivalents for major countries still missing direct literacy values in the viewer: Japan, Germany, United Kingdom, France, Canada, Australia, Netherlands, Belgium, Czechia, and Sweden.
- [ ] Stage official adult-skills sources for those countries, starting with OECD PIAAC / Survey of Adult Skills materials and falling back to national statistical agencies where OECD country-level extracts are easier to retrieve.
- [ ] Define one reusable `adult_literacy_equivalent` derivation method for PIAAC-style sources so the USA, Canada, Germany, Japan, France, United Kingdom, Australia, Netherlands, Belgium, Czechia, and Sweden are treated consistently.
- [ ] Add explicit comparability metadata for `adult_literacy_equivalent` so the viewer distinguishes direct literacy rates from adult-skills-based proxies.

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
- [ ] Ingest Giga school map coverage with country and subnational joins.
- [ ] Add UNESCO UIS bulk indicators for literacy, completion, out-of-school, and finance.
- [ ] Add World Bank EdStats indicators for spending, enrollment, pupil-teacher ratio, and context variables.
- [ ] Add OECD PISA and World Bank learning-poverty/HLO sources for outcomes coverage.
- [ ] Add UNICEF MICS-EAGLE or DHS survey sources for equity and within-country disparity slices.
- [ ] Add boundary and school-age population layers for map denominators and choropleths.
- [ ] Evaluate `MapLibre GL JS` + `deck.gl` as the preferred map stack for the Educational Inequality Map.
- [ ] Build a Phase 1 choropleth-first concept with a country detail drawer and compare mode.
- [ ] Decide the first visual metric switcher set for access, funding, outcomes, and context.
- [ ] Add a missing-vs-stale-vs-equivalent legend treatment to the viewer so proxy literacy values and true no-data states are visually distinct.
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
