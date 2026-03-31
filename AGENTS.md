# AGENTS

## Active bounty
- **Educational Inequality Map** is the current active bounty.
- Canonical brief: [docs/Bounties/educational-inequality-map.md](docs/Bounties/educational-inequality-map.md)
- Supporting research notes: [docs/Bounties/education-knowledge-graph-outline.md](docs/Bounties/education-knowledge-graph-outline.md)

## Current objective
Build a complete, reusable education-access dataset that can power:
- A global disparity map
- Country-to-country comparisons for cost, access, funding, and outcomes
- Future subnational and school-level drilldowns

## Immediate priorities
1. Consolidate the data sources already identified in the repo.
2. Fill missing source categories for school coverage, funding, outcomes, equity, and map boundaries.
3. Produce a minimum Phase 1 schema for country-year comparisons without locking in the final ontology prematurely.
4. Stage the ETL plan for later ingestion and harmonization work.

## Visualization direction
- The intended user-facing experience is a polished global disparity map plus a country-comparison interface.
- Preferred Phase 1 web visualization stack:
  - `MapLibre GL JS` for the base interactive map
  - `deck.gl` for richer geospatial overlays and high-performance interaction
  - the staged `geoBoundaries` ADM0 geometries for country polygons
- Preferred visual style:
  - choropleth-first world map
  - restrained editorial UI rather than a dashboard card grid
  - strong typography, sparse controls, and a focused country detail panel
- Safe work before ontology lock-in:
  - map UX exploration
  - library evaluation
  - view-model planning
  - component sketches that keep data contracts easy to revise
- Avoid locking into a rigid front-end data contract until the Phase 1 indicator layer is clearer.

## Ontology status
- The current ontology work is **provisional**.
- A meeting with Armando is scheduled for **March 31, 2026** to discuss the real ontology.
- Do not push too far into irreversible schema, ETL, or graph-model implementation until Armando's ontology guidance is incorporated.
- Safe work before that meeting:
  - source discovery
  - indicator inventory
  - join-key planning
  - provisional schema sketches
  - ingestion experiments that keep mappings easy to revise

## Source-of-truth files
- [docs/Bounties/educational-inequality-map.md](docs/Bounties/educational-inequality-map.md)
- [docs/Bounties/education-knowledge-graph-outline.md](docs/Bounties/education-knowledge-graph-outline.md)
- [docs/Bounties/educational-inequality-map-sources.md](docs/Bounties/educational-inequality-map-sources.md)
- [docs/Bounties/educational-inequality-map-ontology.md](docs/Bounties/educational-inequality-map-ontology.md)
- [TASKLIST.md](TASKLIST.md)
