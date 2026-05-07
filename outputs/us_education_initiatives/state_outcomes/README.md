# State Outcomes CSV Set

This folder defines the core state-outcomes tables for trend analysis and initiative linkage.

## Files

- `state_year_indicator_catalog.csv`
  - Master catalog of each indicator, source system, year coverage, and comparability risk.
- `state_year_scores_raw.csv`
  - Raw long-format observations: one row per `state_code` + `year` + `indicator_id`.
- `state_initiatives_by_state_year.csv`
  - State-initiative linkage table with adoption timing and evidence/source anchors.
- `initiatives_key.csv`
  - Initiative-centric key table (one row per initiative) used for joins and filtering.

## Join keys

- `state_year_scores_raw.indicator_id` -> `state_year_indicator_catalog.indicator_id`
- `state_initiatives_by_state_year.initiative_id` -> `initiatives_key.initiative_id`
- `state_year_scores_raw.state_code` and `state_initiatives_by_state_year.state_code`
- `state_year_scores_raw.year` and `state_initiatives_by_state_year.policy_start_year` for event windows
