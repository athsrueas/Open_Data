# Educational Inequality Map Ontology

## Purpose
This ontology is designed for a knowledge graph that supports:
- Cross-country comparison of education access, funding, cost, and outcomes
- Future subnational and school-level drilldowns
- Equity analysis across demographic groups
- Provenance-first, reproducible integration of public datasets

## Status note
This document is a **provisional ontology proposal**, not the final ontology.

Current direction captured so far:
- Minimum viable graph centered on `Jurisdiction`, `GeographyGeometry`, `Metric`, `Observation`, `Dataset`, `DatasetRelease`, `IndicatorDefinition`, `PopulationGroup`, and `DemographicDimension`
- Geo and education should stay separated:
  - Geo owns place identity and hierarchy
  - Education owns interpretation, labels, and education-specific entities
- Working rule:
  - identity from Geo
  - meaning from Education

Important dependency:
- A meeting with Armando is scheduled for **March 31, 2026** to discuss the real ontology.
- Do not treat this file as final until Armando's ontology guidance is incorporated.
- Avoid deep implementation commitments before then, especially:
  - irreversible schema choices
  - hard-coded graph loaders
  - ETL mappings that assume this ontology is final

The graph should work for both:
- A property graph implementation such as Neo4j
- An RDF-compatible model with stable URIs and versioned classes

## Ontology design principles
- Use stable canonical IDs for every real-world entity.
- Separate real-world entities from observations, metrics, and datasets.
- Treat high-stakes metrics as time-scoped observations, not static properties.
- Keep provenance explicit for every imported value.
- Allow country-only coverage now, while preserving a path to subnational and school-level expansion.
- Preserve disaggregation rather than flattening it away.

## Versioning
- Ontology name: `edu_inequality_kg`
- Initial version: `v0.1.0`
- Namespace suggestion: `eikg:`

## Core classes

### 1. Jurisdiction
Represents a geographic or administrative education system.

Examples:
- Country
- State
- Province
- District
- Municipality
- Charter network

Properties:
- `jurisdiction_id`: canonical internal ID
- `name`: official display name
- `short_name`: optional abbreviated name
- `jurisdiction_type`: enum
- `iso2_code`: optional
- `iso3_code`: optional
- `ansi_fips_code`: optional
- `geoboundaries_id`: optional
- `world_bank_income_group`: optional
- `un_region`: optional
- `un_subregion`: optional
- `oecd_member`: boolean
- `parent_jurisdiction_id`: optional
- `start_date`: optional
- `end_date`: optional
- `status`: active, historical, provisional
- `notes`: optional text

Recommended controlled values for `jurisdiction_type`:
- `country`
- `state`
- `province`
- `district`
- `municipality`
- `school_network`
- `school_catchment`
- `other`

### 2. School
Represents an individual school or school campus.

Properties:
- `school_id`: canonical internal ID
- `source_school_id`: source-native identifier
- `name`: official or source name
- `alternate_names`: optional array
- `school_level`: primary, lower_secondary, upper_secondary, mixed, tertiary, unknown
- `management_type`: public, private, charter, faith_based, community, unknown
- `is_active`: boolean
- `latitude`: optional
- `longitude`: optional
- `address_text`: optional
- `country_iso3`: optional
- `admin1_code`: optional
- `admin2_code`: optional
- `connectivity_status`: optional
- `electricity_status`: optional
- `water_status`: optional
- `sanitation_status`: optional
- `disability_access_status`: optional
- `opening_year`: optional
- `closing_year`: optional

### 3. PopulationGroup
Represents a population segment to which access, outcomes, or disparity measures apply.

Examples:
- school-age children
- girls age 10-14
- rural students
- lowest wealth quintile learners

Properties:
- `population_group_id`
- `name`
- `description`
- `age_band`: optional
- `sex`: all, female, male, other, unknown
- `wealth_band`: optional
- `residence_type`: urban, rural, peri_urban, mixed, unknown
- `disability_status`: optional
- `migration_status`: optional
- `language_group`: optional
- `income_group_label`: optional
- `school_level_focus`: optional

### 4. DemographicDimension
Represents a reusable dimension used to disaggregate observations.

Examples:
- sex
- wealth quintile
- residence
- age band
- disability status

Properties:
- `dimension_id`
- `dimension_type`
- `label`
- `code`
- `description`
- `sort_order`

### 5. Metric
Represents a measurable concept.

Examples:
- literacy_rate_15_plus
- government_expenditure_on_education_pct_gdp
- pisa_reading_score
- schools_per_1000_school_age_children

Properties:
- `metric_id`
- `name`
- `display_name`
- `description`
- `metric_family`
- `metric_subfamily`
- `domain`: access, funding, cost, outcomes, context, equity, infrastructure
- `unit_type`: percentage, count, index, ratio, currency, standardized_score, binary
- `unit_label`
- `directionality`: higher_is_better, lower_is_better, neutral, context_dependent
- `aggregation_level`: school, jurisdiction, population_group, region, country_year
- `education_level`: pre_primary, primary, lower_secondary, upper_secondary, tertiary, mixed, unspecified
- `subject_area`: reading, math, science, literacy, infrastructure, finance, general
- `methodology_reference`: optional URL or citation
- `source_metric_code`: optional
- `is_derived`: boolean
- `derivation_formula`: optional
- `is_core_phase1`: boolean

Recommended controlled values for `metric_family`:
- `access`
- `participation`
- `completion`
- `learning_outcome`
- `literacy`
- `funding`
- `cost`
- `teacher_capacity`
- `school_infrastructure`
- `population_context`
- `equity_gap`
- `composite_index`

### 6. Observation
Represents a time-scoped measured value for a metric on a subject.

This should be the main fact node in the graph.

Properties:
- `observation_id`
- `value_numeric`: optional
- `value_text`: optional
- `value_boolean`: optional
- `unit_label`
- `normalized_value`: optional
- `normalization_basis`: optional
- `year`
- `period_start`: optional
- `period_end`: optional
- `time_granularity`: annual, quarterly, monthly, snapshot
- `is_estimate`: boolean
- `is_imputed`: boolean
- `is_modeled`: boolean
- `confidence_score`: optional
- `quality_flag`: high, medium, low, unknown
- `comparability_flag`: fully_comparable, partially_comparable, source_specific
- `missing_reason`: optional
- `suppression_reason`: optional
- `notes`: optional

### 7. Dataset
Represents a public dataset, API endpoint, file release, or database.

Examples:
- UNESCO UIS bulk extract
- World Bank EdStats
- OECD PISA 2022 release
- Giga school map export

Properties:
- `dataset_id`
- `name`
- `publisher`
- `source_system`: UIS, WorldBank, OECD, UNICEF, DHS, Giga, geoBoundaries, WorldPop
- `description`
- `homepage_url`
- `download_url`: optional
- `api_url`: optional
- `license_name`: optional
- `license_url`: optional
- `coverage_scope`: global, international, national, subnational, local
- `update_cadence`: annual, periodic, ad_hoc, continuous, unknown
- `data_format`: csv, xlsx, json, geojson, parquet, api, mixed
- `schema_version`: optional
- `citation_text`: optional
- `access_constraints`: open, registration_required, restricted
- `active_from_year`: optional
- `active_to_year`: optional

### 8. DatasetRelease
Represents a specific snapshot or version of a dataset used in ETL.

Properties:
- `dataset_release_id`
- `dataset_id`
- `version_label`
- `snapshot_date`
- `release_date`: optional
- `download_url`: optional
- `content_hash`: optional
- `file_count`: optional
- `record_count`: optional
- `etl_input_path`: optional
- `notes`: optional

### 9. SourceDocument
Represents a report, metadata page, law, method note, or source file.

Properties:
- `document_id`
- `title`
- `document_type`: methodology, report, metadata, statute, survey_manual, article, dataset_file
- `publisher`
- `publication_date`: optional
- `url`
- `language`: optional
- `citation_text`: optional
- `checksum`: optional

### 10. IndicatorDefinition
Represents the formal definition of a metric as published by a source.

Properties:
- `indicator_definition_id`
- `metric_id`
- `dataset_id`
- `source_indicator_code`
- `source_indicator_name`
- `definition_text`
- `calculation_method`: optional
- `denominator_definition`: optional
- `numerator_definition`: optional
- `official_unit`
- `official_disaggregation_dimensions`: optional array
- `valid_from_year`: optional
- `valid_to_year`: optional

### 11. EducationLevel
Represents a controlled vocabulary node for level of education.

Properties:
- `education_level_id`
- `code`
- `label`
- `isced_level`: optional
- `description`

### 12. SubjectArea
Represents learning or curriculum subject areas.

Properties:
- `subject_area_id`
- `code`
- `label`
- `description`

### 13. ServiceType
Represents school service or infrastructure categories.

Examples:
- internet_for_pedagogical_use
- electricity
- drinking_water
- sanitation
- disability_access

Properties:
- `service_type_id`
- `code`
- `label`
- `description`
- `service_domain`: digital, utilities, access, inclusion

### 14. FundingFlow
Represents a financial transfer, commitment, allocation, or spend event.

Use this only where finance data is available at more than aggregate indicator level.

Properties:
- `funding_flow_id`
- `flow_type`: allocation, expenditure, grant, aid, budget_commitment, transfer
- `amount`
- `currency`
- `constant_currency_year`: optional
- `usd_amount_constant`: optional
- `fiscal_year`: optional
- `calendar_year`: optional
- `earmarked_purpose`: optional
- `financing_source_type`: domestic_public, household_private, donor, mixed, unknown
- `notes`: optional

### 15. EducationProgram
Represents a policy, reform, or targeted education program when the graph expands into causal narratives.

Properties:
- `program_id`
- `name`
- `program_type`: literacy, attendance, infrastructure, teacher_training, digital_connectivity, financing_reform, other
- `description`
- `start_year`: optional
- `end_year`: optional
- `status`
- `lead_agency`: optional

### 16. GeographyGeometry
Represents a geometry asset for mapping.

Properties:
- `geometry_id`
- `geometry_type`: point, polygon, multipolygon, raster_grid
- `geometry_source`
- `geometry_version`
- `crs`
- `bbox`: optional
- `feature_count`: optional
- `storage_uri`
- `simplification_level`: optional

### 17. ETLRun
Represents a reproducible ingestion run.

Properties:
- `etl_run_id`
- `pipeline_name`
- `pipeline_version`
- `run_timestamp`
- `run_status`
- `git_commit`: optional
- `input_manifest_hash`: optional
- `output_manifest_hash`: optional
- `operator_name`: optional
- `notes`: optional

### 18. Claim
Represents a human-readable or machine-generated assertion derived from observations.

Examples:
- "Country X has high spending but low learning outcomes."
- "Region Y improved literacy after funding increased."

Properties:
- `claim_id`
- `claim_type`: descriptive, comparative, trend, outlier, disparity, causal_hypothesis
- `claim_text`
- `confidence_score`: optional
- `status`: draft, reviewed, published, disputed
- `created_at`
- `notes`: optional

### 19. CompositeIndex
Represents a derived index used in ranking or visualization.

Examples:
- education_access_index
- funding_effort_index
- education_inequality_index

Properties:
- `composite_index_id`
- `name`
- `description`
- `formula_text`
- `normalization_method`
- `value_range_min`
- `value_range_max`
- `polarity`
- `version`

### 20. DataGap
Represents a known absence, limitation, or comparability issue.

Properties:
- `data_gap_id`
- `gap_type`: missing_data, low_coverage, inconsistent_definition, sparse_geography, sparse_time, restricted_access
- `description`
- `severity`: low, medium, high
- `first_identified_at`
- `last_reviewed_at`: optional
- `resolution_status`: open, mitigated, resolved, accepted

## Core relationships

### Geographic structure
- `(:Jurisdiction)-[:PART_OF]->(:Jurisdiction)`
- `(:School)-[:LOCATED_IN]->(:Jurisdiction)`
- `(:Jurisdiction)-[:HAS_GEOMETRY]->(:GeographyGeometry)`
- `(:School)-[:HAS_GEOMETRY]->(:GeographyGeometry)`

### Observation model
- `(:Jurisdiction)-[:HAS_OBSERVATION]->(:Observation)`
- `(:School)-[:HAS_OBSERVATION]->(:Observation)`
- `(:PopulationGroup)-[:HAS_OBSERVATION]->(:Observation)`
- `(:Observation)-[:MEASURES]->(:Metric)`
- `(:Observation)-[:FOR_EDUCATION_LEVEL]->(:EducationLevel)`
- `(:Observation)-[:FOR_SUBJECT_AREA]->(:SubjectArea)`
- `(:Observation)-[:FOR_POPULATION_GROUP]->(:PopulationGroup)`
- `(:Observation)-[:DISAGGREGATED_BY]->(:DemographicDimension)`
- `(:Observation)-[:FROM_RELEASE]->(:DatasetRelease)`
- `(:Observation)-[:DEFINED_BY]->(:IndicatorDefinition)`
- `(:Observation)-[:GENERATED_BY]->(:ETLRun)`

### Dataset and provenance
- `(:DatasetRelease)-[:RELEASE_OF]->(:Dataset)`
- `(:Dataset)-[:DOCUMENTED_BY]->(:SourceDocument)`
- `(:IndicatorDefinition)-[:PUBLISHED_IN]->(:SourceDocument)`
- `(:Metric)-[:HAS_DEFINITION]->(:IndicatorDefinition)`

### Funding model
- `(:Jurisdiction)-[:RECEIVES_FUNDING]->(:FundingFlow)`
- `(:FundingFlow)-[:FROM_JURISDICTION]->(:Jurisdiction)`
- `(:FundingFlow)-[:TO_JURISDICTION]->(:Jurisdiction)`
- `(:FundingFlow)-[:FOR_PROGRAM]->(:EducationProgram)`
- `(:FundingFlow)-[:FROM_RELEASE]->(:DatasetRelease)`

### School services
- `(:School)-[:OFFERS_SERVICE]->(:ServiceType)`
- `(:Observation)-[:ABOUT_SERVICE]->(:ServiceType)`

### Policy and program context
- `(:Jurisdiction)-[:RUNS_PROGRAM]->(:EducationProgram)`
- `(:EducationProgram)-[:TARGETS_POPULATION]->(:PopulationGroup)`
- `(:EducationProgram)-[:ASSESSED_BY]->(:Observation)`

### Derived analytics
- `(:CompositeIndex)-[:USES_METRIC]->(:Metric)`
- `(:Observation)-[:INSTANCE_OF_INDEX]->(:CompositeIndex)`
- `(:Claim)-[:SUPPORTED_BY]->(:Observation)`
- `(:Claim)-[:ABOUT]->(:Jurisdiction)`
- `(:Claim)-[:ABOUT]->(:PopulationGroup)`
- `(:Claim)-[:GENERATED_BY]->(:ETLRun)`

### Data quality tracking
- `(:DataGap)-[:AFFECTS]->(:Dataset)`
- `(:DataGap)-[:AFFECTS]->(:Metric)`
- `(:DataGap)-[:AFFECTS]->(:Jurisdiction)`
- `(:DataGap)-[:AFFECTS]->(:Observation)`

## Recommended canonical property sets by subject

### Minimum properties for `Jurisdiction`
- `jurisdiction_id`
- `name`
- `jurisdiction_type`
- `iso3_code`
- `parent_jurisdiction_id`
- `status`

### Minimum properties for `School`
- `school_id`
- `name`
- `source_school_id`
- `latitude`
- `longitude`
- `country_iso3`

### Minimum properties for `Metric`
- `metric_id`
- `display_name`
- `metric_family`
- `domain`
- `unit_type`
- `directionality`
- `is_core_phase1`

### Minimum properties for `Observation`
- `observation_id`
- `value_numeric` or `value_text`
- `year`
- `time_granularity`
- `quality_flag`

### Minimum properties for `Dataset`
- `dataset_id`
- `name`
- `publisher`
- `source_system`
- `homepage_url`

### Minimum properties for `DatasetRelease`
- `dataset_release_id`
- `dataset_id`
- `version_label`
- `snapshot_date`

## Phase 1 metric catalog

### Access metrics
- `schools_mapped_count`
- `schools_with_internet_pct`
- `schools_with_electricity_pct`
- `schools_with_drinking_water_pct`
- `schools_with_sanitation_pct`
- `schools_per_1000_school_age_children`
- `net_enrollment_rate_primary`
- `net_enrollment_rate_lower_secondary`
- `completion_rate_primary`
- `completion_rate_lower_secondary`
- `out_of_school_rate_primary_age`
- `out_of_school_rate_lower_secondary_age`

### Funding and cost metrics
- `government_expenditure_education_pct_gdp`
- `government_expenditure_education_pct_total_govt_expenditure`
- `per_student_expenditure_primary_constant_usd`
- `per_student_expenditure_secondary_constant_usd`
- `household_education_expenditure_share`
- `aid_to_education_constant_usd`

### Outcome metrics
- `adult_literacy_rate_15_plus`
- `youth_literacy_rate_15_24`
- `pisa_reading_score`
- `pisa_math_score`
- `pisa_science_score`
- `harmonized_learning_outcome_score`
- `learning_poverty_rate`

### Context metrics
- `school_age_population`
- `total_population`
- `poverty_rate`
- `gdp_per_capita_constant_usd`
- `urban_population_pct`
- `pupil_teacher_ratio_primary`
- `trained_teacher_pct_primary`

### Equity metrics
- `gender_parity_index_enrollment_primary`
- `gender_parity_index_completion_lower_secondary`
- `urban_rural_gap_completion`
- `wealth_quintile_gap_attendance`
- `disability_gap_school_attendance`

### Derived metrics
- `funding_efficiency_score`
- `access_outcome_gap_score`
- `education_inequality_index`
- `service_deprivation_index`

## Controlled vocabularies

### `domain`
- `access`
- `funding`
- `cost`
- `outcomes`
- `context`
- `equity`
- `infrastructure`
- `derived`

### `quality_flag`
- `high`
- `medium`
- `low`
- `unknown`

### `comparability_flag`
- `fully_comparable`
- `partially_comparable`
- `source_specific`

### `source_system`
- `Giga`
- `UNESCO_UIS`
- `WorldBank_EdStats`
- `WorldBank_HLO`
- `WorldBank_LearningPoverty`
- `OECD_PISA`
- `UNICEF_MICS`
- `UNICEF_MICS_EAGLE`
- `DHS`
- `WorldPop`
- `geoBoundaries`
- `Other`

## Identity and key design

### URI / key pattern suggestions
- Jurisdiction: `jurisdiction/{iso3}` or `jurisdiction/{country_iso3}/{adm_level}/{local_code}`
- School: `school/{source_system}/{source_school_id}`
- Metric: `metric/{metric_id}`
- Observation: `observation/{subject_id}/{metric_id}/{year}/{disagg_key}`
- Dataset: `dataset/{source_system}/{dataset_slug}`
- DatasetRelease: `release/{dataset_slug}/{snapshot_date}`

### Preferred join keys
- Country level: ISO-3
- Subnational level: source admin code plus normalized parent ISO-3
- School level: source-native ID plus source system
- Time: year as integer, with optional period dates

## Example graph patterns

### Example 1: country-year literacy observation
- `Jurisdiction(KEN)`
- `Observation(obs_ken_literacy_2020_all)`
- `Metric(adult_literacy_rate_15_plus)`
- `DatasetRelease(uis_2025_09_snapshot)`

Relationships:
- `KEN HAS_OBSERVATION obs_ken_literacy_2020_all`
- `obs_ken_literacy_2020_all MEASURES adult_literacy_rate_15_plus`
- `obs_ken_literacy_2020_all FROM_RELEASE uis_2025_09_snapshot`

### Example 2: school access measure
- `School(giga_12345)`
- `ServiceType(internet_for_pedagogical_use)`
- `Observation(obs_school_12345_internet_2025)`

Relationships:
- `giga_12345 OFFERS_SERVICE internet_for_pedagogical_use`
- `giga_12345 HAS_OBSERVATION obs_school_12345_internet_2025`
- `obs_school_12345_internet_2025 ABOUT_SERVICE internet_for_pedagogical_use`

### Example 3: inequity slice
- `Jurisdiction(BRA)`
- `PopulationGroup(rural_girls_primary_age)`
- `Observation(obs_bra_completion_rural_girls_2022)`

Relationships:
- `BRA HAS_OBSERVATION obs_bra_completion_rural_girls_2022`
- `obs_bra_completion_rural_girls_2022 FOR_POPULATION_GROUP rural_girls_primary_age`

## Recommended implementation notes
- Make `Observation` the center of the graph rather than storing metrics directly on jurisdictions.
- Keep `Metric` separate from `IndicatorDefinition` so different sources can define similar metrics without collapsing them incorrectly.
- Model both `Dataset` and `DatasetRelease` so ETL remains reproducible.
- Use `PopulationGroup` plus `DemographicDimension` together:
  - `PopulationGroup` for reusable slices
  - `DemographicDimension` for atomic disaggregation tags
- Introduce `FundingFlow` only where you have actual flow data; do not force all aggregate finance indicators into flow form.

## Minimum viable graph for v0.1.0
The smallest ontology slice that should be implemented first:
- `Jurisdiction`
- `Metric`
- `Observation`
- `Dataset`
- `DatasetRelease`
- `IndicatorDefinition`
- `PopulationGroup`
- `DemographicDimension`
- `GeographyGeometry`

Minimum relationships:
- `HAS_OBSERVATION`
- `MEASURES`
- `FROM_RELEASE`
- `HAS_DEFINITION`
- `PART_OF`
- `HAS_GEOMETRY`
- `FOR_POPULATION_GROUP`
- `DISAGGREGATED_BY`

## Later extensions
These can be deferred until the core dataset is working:
- `School`
- `FundingFlow`
- `EducationProgram`
- `Claim`
- `CompositeIndex`
- `DataGap`
- fine-grained service and infrastructure modeling

## Recommendation
Start with a country-year observation graph, then layer in:
1. subnational jurisdictions
2. population-group inequity slices
3. school-level infrastructure and access nodes
4. funding-flow and causal-claim structures

This keeps the ontology broad enough for the full vision without making Phase 1 ETL unmanageably complex.
