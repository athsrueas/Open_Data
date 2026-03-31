# Open Data

Tools for collecting, staging, and organizing open datasets for public-interest
projects. The current active bounty is the Educational Inequality Map, with a
focus on building a reusable country-year foundation before the ontology is
finalized.

## Current focus

- Active bounty: Educational Inequality Map
- Goal: build a reusable education-access dataset for global disparity mapping
- Safe work before ontology lock-in: source discovery, raw staging, indicator
  inventory, provisional schema work, and reversible ingestion experiments

Key project references:

- `AGENTS.md`
- `TASKLIST.md`
- `docs/Bounties/educational-inequality-map.md`
- `docs/Bounties/educational-inequality-map-sources.md`
- `docs/Bounties/educational-inequality-map-ontology.md`
- `docs/Bounties/education-knowledge-graph-outline.md`

## What is included

- A JSON schema describing core dataset metadata fields
- Python dataclasses that mirror the schema and provide validation helpers
- A CLI to validate dataset metadata files and print a short summary
- Education-source download scripts for raw landing-zone staging
- A provisional Phase 1 World Bank extract that writes ontology-shaped CSVs
- A first interactive education viewer under `viewer/educational_inequality_map/`

## Education workflows

The repo now has a few concrete scripts under `src/open_data/` for education
source collection:

- `download_education_raw.py`
  - Pulls a small raw World Bank landing zone into
    `outputs/educational_inequality_map/raw/worldbank/<date>/`
- `download_education_raw_stage2.py`
  - Stages additional education sources including UNESCO UIS, Giga, World Bank
    research files, and OECD PISA source manifests into
    `outputs/educational_inequality_map/raw/<date>/`
  - Uses incremental manifests and `.part` files so interrupted runs are easier
    to inspect and resume
- `download_oecd_pisa_raw.py`
  - Downloads OECD PISA 2022 assets into
    `outputs/educational_inequality_map/raw/<date>/oecd_pisa/`
  - Supports smaller download profiles so Phase 1 work can avoid duplicate SAS
    and SPSS payloads
  - Streams large files to disk, retries failures, and resumes from partial
    `.part` downloads
- `fetch_education_phase1.py`
  - Builds a conservative country-year Phase 1 extract from the World Bank API
    into `outputs/educational_inequality_map/phase1_world_bank/`
- `build_education_viewer_data.py`
  - Builds the viewer payload for the education map into
    `viewer/educational_inequality_map/data.js`
  - Merges staged World Bank, World Bank research, Giga, geoBoundaries, NCES
    PIAAC, and provisional adult-skills backfill artifacts
  - Writes a missing-country coverage audit into
    `outputs/educational_inequality_map/research/`

## Try it locally

The commands below assume you are running from the repository root.

Validate the metadata schema tooling:

```bash
python -m src.open_data.validate schemas/dataset.schema.json
```

Stage a small World Bank raw landing zone:

```bash
python src/open_data/download_education_raw.py
```

Stage the broader education source landing zone:

```bash
python src/open_data/download_education_raw_stage2.py
```

Fetch the provisional Phase 1 World Bank extract:

```bash
python src/open_data/fetch_education_phase1.py
```

Build the current education viewer payload and coverage audit:

```bash
python src/open_data/build_education_viewer_data.py
```

Serve the current viewer locally:

```bash
cd viewer/educational_inequality_map
python -m http.server 8787
```

Then open:

```text
http://localhost:8787
```

Download OECD PISA 2022 files with the default Phase 1 profile
(`SAS + docs`, no duplicate SPSS bundle):

```bash
python -u src/open_data/download_oecd_pisa_raw.py --profile phase1 --workers 3
```

Other useful OECD PISA download modes:

```bash
python -u src/open_data/download_oecd_pisa_raw.py --profile docs-only
python -u src/open_data/download_oecd_pisa_raw.py --profile phase1-spss
python -u src/open_data/download_oecd_pisa_raw.py --profile full
```

If the OECD host starts refusing concurrent connections, reduce workers:

```bash
python -u src/open_data/download_oecd_pisa_raw.py --profile phase1 --workers 2
```

## Output locations

Current education outputs are written under:

- `outputs/educational_inequality_map/raw/worldbank/<date>/`
- `outputs/educational_inequality_map/raw/<date>/unesco_uis/`
- `outputs/educational_inequality_map/raw/<date>/giga/`
- `outputs/educational_inequality_map/raw/<date>/geoboundaries/`
- `outputs/educational_inequality_map/raw/<date>/nces_piaac_us/`
- `outputs/educational_inequality_map/raw/<date>/oecd_adult_skills/`
- `outputs/educational_inequality_map/raw/<date>/worldbank_research/`
- `outputs/educational_inequality_map/raw/<date>/oecd_pisa/`
- `outputs/educational_inequality_map/phase1_world_bank/`
- `outputs/educational_inequality_map/research/`
- `viewer/educational_inequality_map/`

Most download scripts write a `manifest.json` alongside staged files so you can
inspect progress and confirm what was fetched.

## Viewer

The repo now includes a real first web viewer for the Educational Inequality
Map in `viewer/educational_inequality_map/`.

Current viewer characteristics:

- Choropleth-first world map
- Country comparison mode for cost, access, funding, and outcomes
- Source notes and caveat-aware literacy handling
- Real staged data from:
  - World Bank EdStats Phase 1 extract
  - World Bank learning poverty and HLO files
  - Giga country metadata
  - geoBoundaries ADM0 geometries
  - NCES PIAAC U.S. literacy equivalent
  - provisional OECD adult-skills equivalents for selected missing countries

The viewer payload now carries:

- `dataModel`
- `coverageSummary`
- `metricCatalog`
- `countries`
- `geojson`
- `graphExamples`
- `sourceNotes`

Key generated viewer artifacts:

- `viewer/educational_inequality_map/data.js`
- `outputs/educational_inequality_map/research/viewer_missing_metrics_audit.csv`
- `outputs/educational_inequality_map/research/viewer_missing_metrics_audit.md`
- `outputs/educational_inequality_map/research/adult_skills_equivalent_backfill_seed.csv`
- `outputs/educational_inequality_map/research/literacy_caveats.csv`

Important caveats:

- School availability is still a proxy based on Giga mapped-school counts.
- Some literacy values are direct World Bank literacy-rate observations, while
  others are explicit `adult literacy equivalent` backfills from adult-skills
  sources and are marked as not directly comparable.
- Some OECD adult-skills country-note pages are protected by Cloudflare, so a
  few backfills are currently seeded from official OECD web results rather than
  fully staged local HTML.

## OECD PISA notes

- `SAS` files are SAS-native packages and typically contain `.sas7bdat` data
  plus SAS format/setup files
- `SPSS` files are the parallel IBM SPSS packaging of similar data
- For Phase 1 work, the default downloader profile prefers one analysis format
  plus documentation to avoid downloading both parallel copies up front
- Large OECD assets can exceed several gigabytes in total, so the downloader is
  optimized for streaming and resume behavior rather than loading files fully
  into memory

## Example data sources

| Name | URL | Type | Domains | Scope | Geography | Short description | Related URLs |
|---|---|---|---|---|---|---|---|
| OpenOUSD | https://openousd.org | web_app | education, transparency, politics | local | Oakland, CA, USA | School-by-school spending and staffing transparency for Oakland USD | GitHub (site code): https://github.com/openoakland/openousd-site |
| Giga – Global School Map | https://giga.global | platform | education, world-affairs, infrastructure, ai | global |  | Maps schools worldwide and tracks connectivity to close the digital divide | GitHub (UNICEF publications org): https://github.com/orgs/UNICEF/publications |
| OpenSpending | https://openspending.org | platform | politics, world-affairs, transparency, economics | global |  | Open platform to collect and visualize public financial (budget/expenditure) data | GitHub: https://github.com/openspending/openspending |
| Open Budgets India | https://openbudgetsindia.org | portal | politics, world-affairs, transparency, economics | national | India | Curated machine-readable Indian government budget datasets and learning resources |  |
| Vulekamali | https://vulekamali.gov.za | portal | politics, world-affairs, transparency, economics | national | South Africa | Official open budget portal for South Africa with datasets and visualizations |  |
| Open Budget Oakland | https://openbudgetoakland.org | web_app | politics, transparency, economics | local | Oakland, CA, USA | Interactive exploration of Oakland city budget with comparisons and drill-downs | GitHub (API): https://github.com/openoakland/budget |
| Open Contracting Data Standard (OCDS) | https://www.open-contracting.org/data-standard/ | standard | politics, world-affairs, transparency, infrastructure | global |  | Open data standard for publishing public procurement across the contracting lifecycle | GitHub: https://github.com/open-contracting |
| SISOCS (CoST Infrastructure Transparency) | https://sisocs.org | platform | world-affairs, transparency, infrastructure, politics | international |  | Platforms for disclosing public infrastructure project data across the full lifecycle | App: https://app.sisocs.org |
| Asheville Capital Projects Dashboard (SimpliCity) | https://dashboards.ashevillenc.gov/capital_projects | dashboard | infrastructure, politics, transparency | local | Asheville, NC, USA | Municipal dashboard for capital project budgets, timelines, and status | GitHub: https://github.com/cityofasheville/simplicity2 |
| OpenAQ | https://openaq.org | platform | health, world-affairs, environment, ai | global |  | Open air quality data platform aggregating monitoring data globally | GitHub: https://github.com/openaq |
| Sensor.Community (Luftdaten) | https://sensor.community/en/ | network | health, environment, world-affairs | global |  | Citizen-driven open sensor network for air quality and environmental data | Maps: https://maps.sensor.community; GitHub: https://github.com/opendata-stuttgart |
| Data.Healthcare.gov | https://data.healthcare.gov/ | portal | health, politics | national | United States | US government portal for healthcare-related open datasets |  |
| CDC Data & Statistics | https://www.cdc.gov/datastatistics | portal | health | national | United States | CDC data and statistics for public health |  |
| FDA FAERS | https://www.fda.gov/drugs/questions-and-answers-fda-adverse-event-reporting-system-faers | dataset | health | national | United States | Adverse event reporting data for drugs and therapeutics (FAERS) |  |
| ClinicalTrials.gov | https://clinicaltrials.gov/ | registry | health, world-affairs | global |  | Public registry of clinical studies and trial metadata |  |
| UCI Machine Learning Repository | https://archive.ics.uci.edu/ml/index.php | repository | ai | global |  | Classic ML datasets for benchmarking and teaching |  |
| Kaggle Datasets | https://www.kaggle.com/datasets | platform | ai, education | global |  | Large catalog of datasets commonly used for ML projects |  |
| TensorFlow Datasets | https://www.tensorflow.org/datasets | repository | ai | global |  | Curated, ML-ready datasets maintained for TensorFlow workflows |  |
| Academic Torrents | https://academictorrents.com/ | repository | ai, world-affairs, education | global |  | Distribution platform for large research datasets |  |
| Data Commons | https://datacommons.org/ | knowledge_graph | ai, world-affairs, education, health | global |  | Open knowledge graph that integrates public datasets with an API |  |
| NCES (National Center for Education Statistics) | https://nces.ed.gov/ | portal | education, politics | national | United States | Official US education statistics and datasets |  |
| UNESCO Institute for Statistics (UIS) | https://uis.unesco.org/ | portal | education, world-affairs | global |  | International education (and other) indicators and statistics |  |
| Data.gov – Education topic | https://data.gov/education | portal | education, politics | national | United States | US federal open data filtered to education-related datasets |  |
| Data.gov (US Open Data) | https://data.gov/ | portal | world-affairs, politics, health, education | national | United States | US federal open data catalog across agencies and topics |  |
| Data.gov.uk (UK Open Data) | https://www.data.gov.uk/ | portal | world-affairs, politics, health, education | national | United Kingdom | UK government open data catalog |  |
| Open.data.gov.sa | https://open.data.gov.sa | portal | world-affairs, politics | national | Saudi Arabia | Saudi government open data portal |  |
| World Bank Open Data | https://data.worldbank.org/ | portal | world-affairs, politics, education, health | global |  | Global development indicators and economic datasets |  |
| UN Data | https://data.un.org/ | portal | world-affairs, politics, education, health | global |  | United Nations global statistics and indicators |  |
| Data.gov – Government topic | https://data.gov/government | portal | politics, world-affairs | national | United States | US federal open data filtered to government/civic datasets |  |
| Data.gov.uk – Government topic search | https://www.data.gov.uk/search?topic=Government | portal | politics, world-affairs | national | United Kingdom | UK open data filtered to government topic |  |
| CoinGecko API | https://www.coingecko.com/en/api | api | crypto | global |  | Crypto market and token pricing data API |  |
| Binance Public Data | https://data.binance.vision/ | dataset | crypto | global |  | Exchange-provided historical market/trade data downloads |  |
| Google Dataset Search | https://datasetsearch.research.google.com/ | search_tool | health, ai, education, world-affairs, politics, crypto | global |  | Search engine to discover datasets across the web |  |
| Data.World | https://data.world/ | platform | health, ai, education, world-affairs, politics, crypto | global |  | Community and organization dataset hosting and discovery |  |
| Internet Archive – Datasets | https://archive.org/details/datasets | archive | health, ai, education, world-affairs, politics, crypto | global |  | Long-term preservation and distribution of datasets |  |

## Schema location

The schema lives in `schemas/dataset.schema.json` and can be used by other tools
that understand JSON Schema.
