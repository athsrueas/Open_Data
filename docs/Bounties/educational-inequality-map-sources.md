# Educational Inequality Map: Source Inventory

## Goal
Identify the datasets needed to build a complete, cross-country education inequality dataset for mapping and comparison across:
- Access
- Funding
- Cost
- Outcomes
- Equity and context

## Sources already identified in this project

### 1. Giga / Global school mapping
- **Giga - Global School Map**
  - URL: https://giga.global/map/
  - Why it matters: strongest current lead for school-location coverage and connectivity-oriented school mapping.
  - Repo context:
    - [README.md](C:/Users/tfreestone/Code/athsrueas/Open_Data/README.md)
    - [src/open_data/data-sources.json](C:/Users/tfreestone/Code/athsrueas/Open_Data/src/open_data/data-sources.json)
    - [outputs/giga__global_school_map/crawl.json](C:/Users/tfreestone/Code/athsrueas/Open_Data/outputs/giga__global_school_map/crawl.json)

### 2. UNESCO UIS
- **UNESCO Institute for Statistics (UIS)**
  - URL: https://databrowser.uis.unesco.org/
  - Already noted in:
    - [README.md](C:/Users/tfreestone/Code/athsrueas/Open_Data/README.md)
    - [src/open_data/data-sources.json](C:/Users/tfreestone/Code/athsrueas/Open_Data/src/open_data/data-sources.json)
    - [docs/Bounties/education-knowledge-graph-outline.md](C:/Users/tfreestone/Code/athsrueas/Open_Data/docs/Bounties/education-knowledge-graph-outline.md)
  - Best current use:
    - Literacy rates
    - Enrollment and completion
    - Gender parity
    - Out-of-school rates
    - Public education finance indicators

### 3. World Bank education indicators
- **World Bank Open Data / EdStats**
  - URL: https://data.worldbank.org/topic/education
  - Already noted in:
    - [README.md](C:/Users/tfreestone/Code/athsrueas/Open_Data/README.md)
    - [src/open_data/data-sources.json](C:/Users/tfreestone/Code/athsrueas/Open_Data/src/open_data/data-sources.json)
    - [docs/Bounties/education-knowledge-graph-outline.md](C:/Users/tfreestone/Code/athsrueas/Open_Data/docs/Bounties/education-knowledge-graph-outline.md)
  - Best current use:
    - Spending
    - Pupil-teacher ratio
    - Enrollment
    - Population and poverty context

### 4. OECD PISA
- **OECD PISA**
  - URL: https://www.oecd.org/en/about/programmes/pisa/pisa-data.html
  - Already noted in:
    - [docs/Bounties/education-knowledge-graph-outline.md](C:/Users/tfreestone/Code/athsrueas/Open_Data/docs/Bounties/education-knowledge-graph-outline.md)
  - Best current use:
    - Cross-country learning outcomes
    - Reading, mathematics, and science performance

## Additional official sources needed for a more complete dataset

### A. UIS bulk download and metadata
- **UIS Bulk Data Download**
  - URL: https://databrowser.uis.unesco.org/documentation/bulk
  - Why add it:
    - This is the programmatic bulk entry point for education indicators.
    - Better for reproducible ETL than ad hoc browser downloads.
  - Use for:
    - Annual country-year extracts for literacy, out-of-school, completion, trained teachers, and finance indicators.

### B. UIS benchmark and methodology resources
- **UIS Resources / SDG 4 metadata**
  - URL: https://databrowser.uis.unesco.org/resources
  - Why add it:
    - Gives official definitions and metadata needed to keep indicators comparable.
  - Use for:
    - Indicator semantics
    - Disaggregation rules
    - Licensing and attribution

### C. World Bank API and EdStats DataBank
- **World Bank API documentation**
  - URL: https://datahelpdesk.worldbank.org/knowledgebase/articles/898581-api-basic-call-structures
- **World Bank Education topic**
  - URL: https://data.worldbank.org/topic/education
- **World Bank EdStats DataBank**
  - URL: https://databank.worldbank.org/databases/education
  - Why add them:
    - Needed for scripted extraction and for indicators not as easy to pull from UIS alone.
  - Use for:
    - Spending, progression, pupil-teacher ratios, demographics, poverty-linked controls, and some learning indicators.

### D. Learning outcome gap fillers
- **World Bank Harmonized Learning Outcomes (HLO)**
  - URL: https://datacatalog.worldbank.org/search/dataset/0038001/harmonized-learning-outcomes-hlo-database
  - Why add it:
    - Extends learning-outcome comparability beyond countries participating in OECD PISA.
  - Use for:
    - National learning outcomes across more countries and years.

- **World Bank Learning Poverty database**
  - URL: https://datacatalog.worldbank.org/dataset/learning-poverty
  - Why add it:
    - Gives a cross-country early-learning and reading outcome lens directly tied to education inequality.
  - Use for:
    - Share of children below minimum proficiency and out-of-school linked measures.

### E. Equity and within-country inequality
- **UNICEF MICS-EAGLE**
  - URL: https://data.unicef.org/resources/mics-education-analysis-for-global-learning-and-equity/
  - Why add it:
    - Adds household-level and subgroup-level inequality signals that country averages miss.
  - Use for:
    - Gender, wealth, residence, and other equity disaggregations.

- **UNICEF MICS-Link in Education**
  - URL: https://data.unicef.org/data-for-action/linking-data-for-better-education-insights-introducing-mics-link-in-education/
  - Why add it:
    - Helps connect household and school data for richer within-country analysis.
  - Use for:
    - Linking administrative and survey-based education access measures.

- **DHS Program datasets and survey methodology**
  - URL: https://www.dhsprogram.com/data/Dataset-Availability-Status-Overview.cfm
  - URL: https://dhsprogram.com/What-We-Do/Survey-Types/DHS-Methodology.cfm
  - Why add it:
    - Valuable where MICS coverage is absent or lagged.
  - Use for:
    - Literacy, attendance context, household conditions, and subnational disaggregation in many low- and middle-income countries.

### F. Population denominators and map geometry
- **WorldPop Data Catalog**
  - URL: https://www.worldpop.org/datacatalog/
  - Why add it:
    - Needed to estimate school-age population denominators and spatial catchments.
  - Use for:
    - Population-normalized school access metrics
    - School-to-population ratios
    - Gridded overlays

- **geoBoundaries**
  - URL: https://www.geoboundaries.org/
  - Why add it:
    - Needed for reliable country and subnational map polygons.
  - Use for:
    - Choropleths
    - Regional joins
    - Consistent ADM-level mapping

## Recommended Phase 1 dataset stack

### Must-have
- Giga school map
- UIS bulk indicators
- World Bank EdStats / API
- OECD PISA
- geoBoundaries

### Strongly recommended
- World Bank HLO
- World Bank Learning Poverty
- WorldPop

### Add for deeper equity analysis
- UNICEF MICS-EAGLE
- UNICEF MICS-Link
- DHS Program microdata and metadata

## Proposed Phase 1 indicator groups

### Access
- Schools mapped
- Enrollment
- Completion
- Out-of-school rate
- School-to-school-age-population ratio

### Funding and cost
- Government expenditure on education as % of GDP
- Government expenditure on education as % of government expenditure
- Per-student public expenditure where available

### Outcomes
- Adult and youth literacy
- PISA reading/math/science
- Harmonized learning outcomes
- Learning poverty

### Context and disparity
- Population
- Poverty
- Urbanization
- Gender parity
- Wealth and residence disaggregation where survey data exists

## Gaps still likely after Phase 1
- Consistent globally comparable school-level finance data
- Uniform school quality or infrastructure-condition data
- Fully comparable subnational outcome data across all countries
- Direct school catchment boundaries

## Recommendation
Treat the first complete version as a **country-year comparative dataset with optional subnational overlays**, not a universal school-level master file. The school-level layer can grow country by country, but the country-year backbone is already achievable with the sources above.

## Raw source ontology notes

### World Bank raw payload shape
The raw World Bank downloads in [outputs/educational_inequality_map/raw/worldbank/2026-03-30](C:/Users/tfreestone/Code/athsrueas/Open_Data/outputs/educational_inequality_map/raw/worldbank/2026-03-30) already reveal a strong implicit ontology from the source publisher.

The source treats the basic fact shape as:
- `indicator`
- `country`
- `countryiso3code`
- `date`
- `value`

In practice, that means the World Bank's core worldview is:
- a metric catalog of indicators
- a geography catalog of reporting units
- a time series of observations at the intersection of geography and indicator

### What the professionals clearly think is important

#### 1. Observation-first structure
The main fact is not "country has literacy" as a static property. It is:
- a specific indicator
- for a specific reporting unit
- in a specific year
- with a numeric value

That strongly supports our choice to center the working graph on `Observation`.

#### 2. Geography is more than countries
The raw API includes both:
- sovereign countries
- aggregate reporting regions such as `Africa Eastern and Southern`

That shows the source thinks reporting geographies and analytical aggregates are both first-class. This is useful, but it also means we should keep a clear distinction between:
- canonical jurisdictions we want in our graph
- aggregate pseudo-jurisdictions we may want to model separately later

#### 3. Classification systems matter
The country metadata payload includes:
- `region`
- `adminregion`
- `incomeLevel`
- `lendingType`

This tells us the source considers these classifications meaningful enough to ship with every geography record. For our graph, that is a strong signal that classifications should not be treated as incidental labels. They are useful dimensions for grouping, comparison, and filtering.

#### 4. Source identifiers matter more than pretty labels
Each important object comes with compact IDs:
- country IDs
- ISO-like codes
- indicator codes
- classification IDs

This is a professional data-publisher pattern: stable machine IDs first, human-readable labels second. That aligns well with our need for canonical identifiers and stable joins.

#### 5. Metadata is thin at the fact row level
Each row has only limited row-level metadata:
- `unit`
- `obs_status`
- `decimal`

This means the source optimizes for broad comparability and distribution rather than rich provenance per observation. It is one reason we should add our own provenance layer through:
- dataset releases
- indicator definitions
- ETL manifests
- data quality flags

#### 6. Nulls are part of the ontology
The raw downloads include many rows where the year exists but the value is null. That implies the source is modeling:
- expected reporting coverage across time
- not just existing measurements

This is important. Missingness is informative and should not be discarded too early in downstream transforms.

### Practical takeaway for our project
The World Bank raw structure reinforces several good working assumptions:
- keep `Observation` at the center
- treat geography, metric, and time as the core fact axes
- preserve raw source IDs
- keep classifications like region and income group available as dimensions
- do not assume all reporting units are canonical places
- preserve missingness and source-specific metadata in the raw layer

### Caution
This is the ontology of one professional source, not the final ontology of the project.
It is useful evidence for how mature publishers structure education data, but we should still wait for Armando's ontology guidance before freezing the long-term graph model.
