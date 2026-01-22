# Public data discovery and collection survey

## Existing projects for locating and collecting important public data

- **Data.gov (US)**: A centralized catalog of datasets published by U.S. federal agencies with metadata, download links, and APIs.
- **data.gov.uk (UK)**: The United Kingdom's open data catalog, including national statistics, transport, and other public datasets.
- **EU Open Data Portal**: Access to datasets from European Union institutions and bodies, with standardized metadata and bulk download options.
- **Open Data Network**: Aggregates and normalizes datasets from many local and regional government portals for easier discovery.
- **World Bank Open Data**: Global development indicators and economic data, often used in policy and research.
- **UN Data**: United Nations statistics and indicators across demographics, health, and development.
- **OpenStreetMap**: Community-driven geospatial dataset with broad coverage, frequently used for public-good mapping initiatives.
- **Humanitarian Data Exchange (HDX)**: Curated data for humanitarian response, including crisis and displacement datasets.
- **International Aid Transparency Initiative (IATI)**: Standardized reporting on aid flows and projects with machine-readable data.
- **OECD Data**: Economic, social, and environmental indicators with consistent metadata.
- **Census data portals** (e.g., U.S. Census, Statistics Canada): Population, housing, and economic datasets.

## Free and open APIs with public-good data

### Education
- **U.S. College Scorecard API**: Outcomes, costs, and student demographics for U.S. higher education institutions.
- **UNESCO Institute for Statistics API**: Global education indicators (enrollment, literacy, etc.).

### Demographics
- **U.S. Census API**: Population, housing, and socioeconomic data at multiple geographic levels.
- **World Bank API**: Demographics and development indicators by country and year.
- **UN Data API**: Population and development statistics across member states.

### Charity finances / nonprofit transparency
- **IRS Exempt Organizations Business Master File**: Data on U.S. nonprofits' registration status (bulk data and subsets).
- **Open990**: Data extracted from IRS Form 990 filings for nonprofit financial transparency.
- **Charity Navigator (public data exports)**: Ratings and financial metrics for U.S. nonprofits (where available).

### Existing public-good initiatives
- **IATI Registry API**: Aid project data for global development and humanitarian work.
- **HDX API**: Humanitarian datasets and metadata for crisis response.
- **OpenStreetMap APIs**: Access to geospatial data and change sets for public mapping.

## Protocols and standards for data sharing (including Solid)

- **Solid (Social Linked Data)**: A decentralized data platform founded by Tim Berners-Lee, emphasizing user-controlled data pods and interoperability using Linked Data standards.
- **Linked Data and RDF**: Standards for expressing data as interconnected resources (RDF, RDFa, Turtle), enabling cross-dataset linking and semantic queries.
- **JSON-LD**: JSON-based serialization for Linked Data, commonly used to embed semantics into APIs and datasets.
- **SPARQL**: Query language and protocol for RDF data, enabling federated queries across linked datasets.
- **WebID and OIDC**: Identity and authentication mechanisms often paired with Solid for resource access control.
- **ActivityPub**: A W3C protocol for decentralized social networking, relevant for distributing updates about datasets or data collection activity.
- **OpenAPI / JSON Schema**: Widely used specifications for documenting and validating API-based data access.
- **DCAT (Data Catalog Vocabulary)**: A W3C standard for describing datasets in catalogs, improving discoverability and interoperability.

## Suggested next steps

1. Identify priority domains (education, public health, housing, climate, etc.) and create a shortlist of datasets/APIs.
2. Normalize metadata into a common schema (e.g., DCAT) for cross-source search and categorization.
3. Build ingestion connectors for top-priority sources and schedule regular refreshes.
4. Define a governance and data-quality checklist (licensing, update cadence, provenance).
5. Track provenance and updates using standardized metadata (e.g., DCAT + JSON-LD) and publish a unified catalog.
