# Open Data

Tools for collecting and organizing open data.

## Catalog metadata foundation

This repository now ships a lightweight metadata schema and validator to provide
an extensible foundation for dataset discovery, ingestion, and cataloging.

## Example data sources
| Domain(s)                    | Project Name                  | URL                                                                 | Type        | Scope / Geography        | Short Description |
|-----------------------------|-------------------------------|----------------------------------------------------------------------|-------------|--------------------------|-------------------|
| Education, Transparency     | OpenOUSD                      | https://openousd.org                                                 | Web App     | Local (Oakland, CA)      | School-by-school spending and staffing transparency |
| Education, Infrastructure   | Giga (Global School Map)      | https://giga.global                                                  | Platform    | Global                  | Maps global school connectivity and internet access |
| Budget, Transparency        | OpenSpending                  | https://openspending.org                                             | Platform    | Global                  | Government budget and expenditure visualization |
| Budget, Transparency        | Open Budgets India            | https://openbudgetsindia.org                                         | Portal      | National (India)         | Unified, machine-readable Indian budget data |
| Budget, Transparency        | Vulekamali                    | https://vulekamali.gov.za                                            | Portal      | National (South Africa)  | Official open budget portal with visualizations |
| Budget, Civic Tech          | Open Budget Oakland           | https://openbudgetoakland.org                                        | Web App     | Local (Oakland, CA)      | Interactive city budget exploration |
| Infrastructure, Procurement | Open Contracting Data Standard| https://www.open-contracting.org/data-standard/                      | Standard    | Global                  | Open standard for public procurement data |
| Infrastructure              | SISOCS (CoST)                 | https://sisocs.org                                                   | Platform    | International            | Infrastructure project lifecycle transparency |
| Infrastructure              | Asheville Capital Dashboard   | https://dashboards.ashevillenc.gov/capital_projects                  | Dashboard   | Local (Asheville, NC)    | Municipal capital project tracking |
| Environment, Health         | OpenAQ                        | https://openaq.org                                                   | Platform    | Global                  | Aggregated global air quality data |
| Environment, Health         | Sensor.Community              | https://sensor.community/en/                                         | Network     | Global                  | Citizen-driven open environmental sensor network |
| Health                      | Data.Healthcare.gov           | https://data.healthcare.gov/                                         | Portal      | United States            | Federal healthcare datasets |
| Health                      | ClinicalTrials.gov            | https://clinicaltrials.gov/                                          | Registry    | Global                  | Public clinical trials database |
| Health                      | CDC Public Use Data           | https://www.cdc.gov/datastatistics                                   | Portal      | United States            | Disease and public health statistics |
| AI, ML                      | UCI ML Repository             | https://archive.ics.uci.edu/ml/index.php                             | Repository  | Global                  | Benchmark machine learning datasets |
| AI, ML                      | Kaggle Datasets               | https://www.kaggle.com/datasets                                      | Platform    | Global                  | Community-driven ML datasets |
| AI, ML                      | TensorFlow Datasets           | https://www.tensorflow.org/datasets                                  | Repository  | Global                  | Production-ready ML datasets |
| AI, Research                | Academic Torrents             | https://academictorrents.com/                                        | Repository  | Global                  | Large-scale academic datasets |
| World Affairs, Economics    | World Bank Open Data          | https://data.worldbank.org/                                          | Portal      | Global                  | Development and economic indicators |
| World Affairs               | UN Data                       | https://data.un.org/                                                 | Portal      | Global                  | UN global statistics |
| Government, Politics        | Data.gov (US)                 | https://data.gov/                                                    | Portal      | United States            | Federal open data catalog |
| Government, Politics        | Data.gov.uk                   | https://www.data.gov.uk/                                             | Portal      | United Kingdom           | UK government open data |
| Crypto, Finance              | CoinGecko API                | https://www.coingecko.com/en/api                                     | API         | Global                  | Cryptocurrency market data |
| Crypto, Finance              | Binance Public Data          | https://data.binance.vision/                                         | Dataset     | Global                  | Exchange-level crypto market data |
| Cross-Domain                | Data.World                    | https://data.world/                                                  | Platform    | Global                  | Community-curated open datasets |
| Cross-Domain                | Internet Archive Datasets     | https://archive.org/details/datasets                                 | Archive     | Global                  | Long-term dataset preservation |


### What is included

- A JSON schema describing core dataset metadata fields.
- Python dataclasses that mirror the schema and provide validation helpers.
- A CLI to validate dataset metadata files and print a short summary.

### Try it locally

```bash
PYTHONPATH=src python -m open_data.validate examples/sample_dataset.json --summary
```

### Schema location

The schema lives in `schemas/dataset.schema.json` and can be used by other tools
that understand JSON Schema.
