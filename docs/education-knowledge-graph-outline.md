# Global Education Outcomes Knowledge Graph – Work Outline

## Goal
Build a knowledge graph that connects education investment, access, and outcome indicators across countries (and later subnational regions or schools) to surface relationships that are hard to see in isolated datasets.

## 1. Scope & use cases
- Compare investment vs. outcomes (e.g., education spend vs. literacy/PISA performance).
- Identify lag effects (e.g., spend increases preceding outcome improvements).
- Segment by demographics (e.g., gender parity, income groups, urban/rural).
- Support queries like:
  - "Which countries increased education spend by >X% and improved literacy by >Y%?"
  - "Which regions show high spending but low outcomes?"

## 2. Core datasets to integrate
### Investment & access
- UNESCO UIS: education spend, enrollment, completion.
- World Bank EdStats: spending, pupil-teacher ratio, enrollment.

### Outcomes
- OECD PISA: test scores (math/reading/science).
- UNESCO UIS: literacy rates, completion/graduation.

### Demographics & context
- World Bank: GDP per capita, poverty, population, urbanization.
- UNESCO UIS: gender parity indices, age-group enrollment.

### Reference table: primary data sources
| Source | Coverage | Example indicators | Access URL |
| --- | --- | --- | --- |
| UNESCO UIS (Education & Literacy) | Global | Literacy rates, completion, enrollment, gender parity | https://www.uis.unesco.org/en/themes/education-literacy |
| UNESCO UIS Data Browser | Global | UIS indicators by country/year | https://databrowser.uis.unesco.org/ |
| World Bank DataBank (Literacy & Education) | Global | Spending, enrollment, literacy, completion | https://databank.worldbank.org/id/50213e0c?Report_Name=Literacy-and-education |
| OECD PISA | Participating countries | Test scores (math/reading/science) | https://www.oecd.org/en/about/programmes/pisa/pisa-data.html |

### Reference table: standards & interoperability
| Resource | Why it matters | URL |
| --- | --- | --- |
| SDMX for Education | Shared statistical data model for education indicators | https://sdmx.org/sdmx-for-education/ |
| Linked SDMX Data (csarven) | Example of RDF/linked-data representation for SDMX | https://csarven.ca/linked-sdmx-data |

### Reference table: research & KG patterns
| Reference | Focus | URL |
| --- | --- | --- |
| Knowledge-graph work in education data integration (2024) | KG methods for education datasets | https://www.sciencedirect.com/science/article/pii/S0169023X24001290 |
| Sustainability/education data integration study (2024) | Cross-dataset indicator analysis | https://www.mdpi.com/2071-1050/16/11/4328 |

## 3. Entity model (manual nodes + relationships)
### Nodes
- Country (ISO-3, name, region, income group)
- Indicator (spend, literacy, enrollment, test score)
- Observation (value + year + unit)
- Dataset/Source (UNESCO, World Bank, OECD)
- Demographic dimension (gender, age group, urban/rural)

### Relationships
- Country **HAS_OBSERVATION** Observation
- Observation **MEASURES** Indicator
- Observation **FROM_SOURCE** Dataset/Source
- Observation **FOR_DEMOGRAPHIC** Demographic dimension
- Country **IN_REGION** Region (optional)
- Country **IN_INCOME_GROUP** Income group (optional)

## 4. Data normalization plan
- Normalize country identifiers to ISO-3.
- Align time ranges (e.g., 2000–present, yearly).
- Harmonize indicator definitions and units (spend as % GDP, per-student spend).
- Tag missing or estimated values.

## 5. Knowledge graph structure
- Use a property graph model:
  - Nodes: Country, Indicator, Observation, Dataset, Demographic.
  - Edges: HAS_OBSERVATION, MEASURES, FROM_SOURCE, FOR_DEMOGRAPHIC.
- Store in a graph DB (Neo4j) or RDF (if interoperability is required).
  - Target: canonical public endpoint (SPARQL or property graph API) with a stable ontology and reproducible ETL.

## 6. Example triples (manual definition)
- Country: "Kenya" (ISO3=KEN)
- Indicator: "Literacy Rate (15+)"
- Observation: value=82.3, year=2020
- Relationships:
  - Kenya HAS_OBSERVATION obs123
  - obs123 MEASURES LiteracyRate15Plus
  - obs123 FROM_SOURCE UNESCO_UIS

## 7. Derived insights & queries
- Correlations: spending vs. outcomes (with lag).
- Outliers: high spend/low outcomes, low spend/high outcomes.
- Cohort comparisons: income group vs. performance.

## 8. Deliverables (initial phase)
- Schema definition for nodes/edges.
- Minimal dataset extract (3–5 countries, 3–4 indicators) as a sample graph.
- Query cookbook (5 example queries).
- Short README on data sources + limitations.

## 9. Risks & assumptions
- Indicator definitions differ across sources.
- PISA coverage limited to participating countries.
- Time alignment gaps across datasets.

## 10. Next steps
- Identify exact indicators + metadata keys to ingest.
- Draft ETL mapping sheet (source → indicator → unit → node/edge).
- Choose storage layer and import format.
