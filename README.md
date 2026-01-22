# Open Data

Tools for collecting and organizing open data.

## Catalog metadata foundation

This repository now ships a lightweight metadata schema and validator to provide
an extensible foundation for dataset discovery, ingestion, and cataloging.

## Example data sources
| Domain          | Name                                   | URL                                                                 | Type      | Notes |
|-----------------|----------------------------------------|----------------------------------------------------------------------|-----------|-------|
| Health          | Data.Healthcare.gov                    | https://data.healthcare.gov/                                        | Portal    | US healthcare utilization, claims, providers |
| Health          | CDC Public Use Datasets                | https://www.cdc.gov/datastatistics                                  | Portal    | Disease surveillance, public health |
| Health          | FAERS (FDA Adverse Events)             | https://www.fda.gov/drugs/questions-and-answers-fda-adverse-event-reporting-system-faers | Dataset   | Drug adverse event reporting |
| Health          | ClinicalTrials.gov                    | https://clinicaltrials.gov/                                         | Portal    | Global clinical trial registry |
| AI              | UCI Machine Learning Repository        | https://archive.ics.uci.edu/ml/index.php                            | Portal    | Classic ML benchmark datasets |
| AI              | Kaggle Datasets                        | https://www.kaggle.com/datasets                                     | Portal    | Community & competition datasets |
| AI              | TensorFlow Datasets                   | https://www.tensorflow.org/datasets                                 | Portal    | ML-ready datasets |
| AI              | Academic Torrents                     | https://academictorrents.com/                                       | Portal    | Large-scale research datasets |
| AI              | Data Commons                           | https://datacommons.org/                                            | Knowledge Graph | Structured public data graph |
| Education       | NCES (US Education Statistics)         | https://nces.ed.gov/                                                | Portal    | Official US education data |
| Education       | UNESCO Institute for Statistics        | https://uis.unesco.org/                                             | Portal    | Global education indicators |
| Education       | Education Data (Data.gov)              | https://data.gov/education                                          | Portal    | US open education datasets |
| World Affairs   | Data.gov (US Open Data)                | https://data.gov/                                                   | Portal    | Federal datasets across domains |
| World Affairs   | Data.gov.uk                            | https://www.data.gov.uk/                                            | Portal    | UK government open data |
| World Affairs   | World Bank Open Data                   | https://data.worldbank.org/                                         | Portal    | Global economic & development data |
| World Affairs   | UN Data                                | https://data.un.org/                                                | Portal    | UN global statistics |
| Politics        | Government Data (Data.gov)             | https://data.gov/government                                         | Portal    | Civic, policy, governance data |
| Politics        | Open Government Data (UK)              | https://www.data.gov.uk/search?topic=Government                     | Portal    | UK political & civic datasets |
| Crypto          | CoinGecko API                          | https://www.coingecko.com/en/api                                    | API       | Crypto market data |
| Crypto          | Binance Public Data                    | https://data.binance.vision/                                        | Dataset   | Exchange market & trade data |
| Crypto          | Google Dataset Search (Crypto queries) | https://datasetsearch.research.google.com/                          | Search Tool | Discovery of blockchain datasets |
| Cross-Domain    | Data.World                             | https://data.world/                                                 | Platform  | Community-curated datasets |
| Cross-Domain    | Internet Archive Datasets              | https://archive.org/details/datasets                                | Archive   | Long-term dataset preservation |

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
