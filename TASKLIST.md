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

## U.S. Education Initiatives Subspace
- [ ] Implement the stakeholder change plan in `docs/Bounties/education-dashboard-change-requests-2026-05.md` before public launch.
- [ ] Add a publication-readiness gate report that blocks release until indicator coverage and comparability thresholds are met.
- [ ] Redesign viewer UX for journalists/citizens/parents with headline-first storytelling, short map explanations, and evidence callouts.
- [ ] Add side-by-side comparative map views (state vs state, period vs period, and pre/post initiative windows).
- [ ] Add trend-change analysis tied to initiative adoption dates with explicit negative/null finding support.
- [ ] Prepare a dedicated education-data repository split plan from the general open-data repository.
- [ ] Download and organize all identified benchmark/peer datasets (Education Recovery Scorecard, SEDA, Urban Education Data Portal, NAEP state trend tools, SAT/ACT state reports, ECS policy scans, CTE/work-based learning dashboards), and maintain a complete source record (URL, publisher, retrieval date, license/terms, geography, year coverage, and field-level provenance notes) for every ingested file.
- [x] Replace weak seed rows in `Education Initiatives/education_initiatives.csv` with stronger interventions for testing/accountability, work-based learning, outdoor learning, and reduced-tech school policy.
- [ ] Keep `Education Initiatives/initiative_sources.csv` current for every kept or replacement initiative.
- [x] Resolve all `pending_search` official-source rows in the source inventory.
- [x] Pull down the first wave of PDFs and HTML captures into `outputs/us_education_initiatives/sources/`.
- [x] Extract atomic findings into `Education Initiatives/initiative_claims.csv`.
- [x] Upgrade at least five initiative evidence rows out of `seed` in `Education Initiatives/initiative_evidence_reviews.csv`.
- [x] Rebuild the subspace bundle and inspect `outputs/us_education_initiatives/subspace/initiatives.flat.csv` for empty evidence fields.
- [ ] Add longitudinal state performance datasets for reading, math, SAT, and other top score types (ACT, NAEP, AP where available), going as far back as reliable state-level series allow; include source provenance, year coverage metadata, and comparability notes for score-scale differences.

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
