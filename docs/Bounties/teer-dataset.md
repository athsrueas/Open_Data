# TEER Dataset (Theory of Effective Education Reform Dataset)

**Source:** Thomas Freestone

## Overview
The TEER Dataset (Theory of Effective Education Reform Dataset) is a standardized, open longitudinal panel dataset covering 50+ jurisdictions, including all U.S. states plus selected international systems, from 2000–2025+. Its goal is to quantify four proposed interlocking pillars of successful education reform:
- Foundational instruction
- Tight accountability
- Capacity-building with autonomy
- Sustained local ownership

The dataset should link these pillars directly to student achievement outcomes, including NAEP, PISA, and equivalent state metrics. The primary analysis surface is an interactive dashboard with regression-ready CSV exports, heatmaps, and synthetic-control charts that let users test the TEER hypothesis in real time.

## Problem
Education reform research is fragmented. Achievement data such as NAEP and PISA live in one set of silos, while policy laws, curricula, and implementation details are scattered across statutes, foundation reports, agency archives, and case studies without a common coding schema.

This fragmentation produces irreproducible claims such as "Mississippi's miracle" versus "Gates Foundation failures" and makes it difficult to rigorously test why some systems improve dramatically while others with similar funding do not.

## Bounty direction
Build a machine-readable, longitudinal education reform dataset that connects reform design, implementation, and student outcomes across jurisdictions, with a dashboard and export layer that supports causal analysis, replication, and falsification.

## Expected outcome
Researchers, policymakers, journalists, and educators should be able to:
- Download a single machine-readable file
- Query an online dashboard
- Replicate the five miracle cases
- Identify counter-examples
- Use the data directly in R, Stata, Python, or Tableau

The final dataset should be publishable through Geo- and app-based views or DOI-backed releases for durable citation and reuse.

## Why it matters
Education spending in the U.S. and globally exceeds $1 trillion annually, yet many large-scale reforms produce weak or null results. At the same time, demand for evidence about what actually works is growing quickly, from Science of Reading legislation to debates about charters, retention, and high-performing international systems.

This dataset addresses that gap at a moment when legislatures, philanthropies, and major public institutions are deciding which reforms to scale over the next decade.

## Key use cases
- Interactive Pillar Scorecard Heatmap: color-coded U.S. state map showing four-pillar adoption levels overlaid with 2013–2024 NAEP reading gains
- Miracle vs. Counterfactual Longitudinal Dashboard: synthetic-control comparisons for Mississippi, Poland, Sobral, and other cases against matched non-reform systems
- Reform Failure Analyzer: scatterplot and comparison tools showing funding levels, pillar completeness, and achievement change side by side

## Impact
The primary audience includes state education commissioners, congressional staff, OECD analysts, major media outlets, and university education-policy programs. A well-structured TEER dataset could influence NAEP briefings, congressional testimony, annual policy reports, and public-facing media explainers, helping steer future reform dollars toward evidence-based designs.

## Entities and relationships
Primary entities:
- Jurisdiction
- ReformYear
- PillarScore
- AchievementMetric
- ReformEvent

Suggested relationships:
- Jurisdiction -> has PillarScore -> in ReformYear
- ReformYear -> produces AchievementMetric -> adjusted for Demographics
- Jurisdiction -> experiences ReformEvent -> triggers PillarScore change

## Data attributes
Per entity or jurisdiction-year panel row, include:
- Jurisdiction name
- ISO or ANSI code
- Category (U.S. State, International, Charter District)
- Parent entity
- Year (2000–2025)
- Pillar composite score (0–4)
- Per-pupil spending (constant USD)
- Teacher-student ratio
- Percent disadvantaged enrollment
- Standardized achievement deltas in reading and math
- Control variables such as poverty, demographics, and migration
- Data version
- Normalized rate vs. national average
- Source citation
- Blind-coding reliability score
- Falsification flag

## Suggested ontology
- `pillar_1_foundational_instruction`: 0–1
- `pillar_2_accountability`: 0–1
- `pillar_3_capacity_autonomy`: 0–1
- `pillar_4_sustained_ownership`: 0–1
- `teer_composite`: 0–4
- `achievement_delta_sd`: standardized pre/post gain
- `synthetic_control_weight`: counterfactual matching weight
- `falsification_counterexample`: boolean

## Potential sources
- National Center for Education Statistics (NCES) and NAEP Data Explorer
- OECD PISA Database
- Education Commission of the States (ECS) policy tracking
- National Conference of State Legislatures (NCSL) Pre-K-12 legislation database
- Stanford World Education Reform Database (WERD)
- State department of education legislative archives and curriculum records
- World Bank and UNESCO country reports
- Shanker Institute Reading Reform Across America legislative survey

## Initial scope
The first release should cover all 50 U.S. states plus the District of Columbia from 2000–2025, along with five high-signal international or municipal cases:
- Poland
- Vietnam
- Sobral, Brazil
- New Orleans Recovery School District
- Massachusetts as an early comparator

The first public version should emphasize pre- and post-2013 Mississippi-style reforms, complete pillar coding, and NAEP/PISA outcomes through 2024. Subsequent versions can expand to additional OECD countries and charter networks once completeness and inter-rater reliability are strong.

## Notes
- Treat this as a claim-testing dataset, not just a descriptive archive, so variable definitions need to support falsification.
- Separate policy adoption from implementation fidelity wherever possible.
- Maintain transparent coding rules and blind-coding reliability so users can audit subjective pillar assignments.
- Preserve annual panel structure and event-level records so both regression and case-study workflows remain possible.

## Starting point suggestions
- Build a jurisdiction-year schema first, with clear IDs and one row per jurisdiction-year.
- Ingest NAEP and PISA outcomes before adding policy and implementation variables.
- Pilot the four-pillar coding on Mississippi, Massachusetts, and one international case to refine the rubric.
- Publish an initial codebook and regression-ready CSV export before expanding to the full dashboard.
