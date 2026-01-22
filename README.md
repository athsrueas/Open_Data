# Open Data

Tools for collecting and organizing open data.

## Catalog metadata foundation

This repository now ships a lightweight metadata schema and validator to provide
an extensible foundation for dataset discovery, ingestion, and cataloging.

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



### What is included

- A JSON schema describing core dataset metadata fields.
- Python dataclasses that mirror the schema and provide validation helpers.
- A CLI to validate dataset metadata files and print a short summary.

### Try it locally

```bash
insert code here [I haven't actually written much working scraping scripting or anything yet]
```

### Schema location

The schema lives in `schemas/dataset.schema.json` and can be used by other tools
that understand JSON Schema.
