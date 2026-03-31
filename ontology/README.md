# Ontology Starter Files

This folder contains provisional ontology-oriented CSV examples for the
Educational Inequality Map bounty.

These files are meant to support:

- join-key planning
- indicator inventory
- graph/table boundary design
- reversible Phase 1 processing
- discussion prep before the ontology is finalized

## Status

This folder is intentionally provisional.

The ontology for this project is not final yet. Per the repo guidance, the real
ontology discussion with Armando is scheduled for March 31, 2026, so nothing in
this folder should be treated as irreversible schema truth.

## What is in this folder

- `classes.csv`
  - Provisional class inventory for the graph/domain model
- `relationships.csv`
  - Provisional edge/relationship inventory
- `phase1_metrics.csv`
  - Candidate Phase 1 metric catalog with source and status notes
- `properties_phase1.csv`
  - Minimal property sketch for the highest-priority classes
- `example_nodes.csv`
  - Small example node rows showing how IDs and labels may look
- `example_edges.csv`
  - Small example edge rows showing how core provenance and observation links may look

## Recent update

These starter files were updated after inspecting the raw source payloads now
staged under `outputs/educational_inequality_map/`.

The important shift is that the ontology is now more explicitly
GeoBrowser-oriented and map-first:

- `Observation` is treated as the canonical fact object
  - This matches the structure we now see in the existing World Bank Phase 1
    outputs and in the raw UNESCO UIS tables, which are already close to
    `jurisdiction + indicator + year + value`.
- `GeographyGeometry` is promoted into the high-priority core
  - We now have geoBoundaries ADM0 assets staged, so geometry is no longer just
    theoretical support data.
- `IndicatorDefinition` is kept separate from `Metric`
  - This is important because UIS, World Bank, HLO, Learning Poverty, and later
    OECD PISA may describe related concepts with different native indicator
    codes, units, and methodological notes.
- `DatasetRelease` is emphasized as the provenance anchor
  - The downloader and manifest outputs are now strong enough that reproducible
    release lineage should be part of the working model, not an afterthought.
- `Giga` and `OECD PISA` are intentionally not forced into the center of the
  model yet
  - Giga currently looks more like country metadata plus layer definitions than
    a ready country-year fact table.
  - OECD PISA is rich and useful, but its raw microdata and codebooks are still
    better treated as source, release, and definition assets until we choose an
    explicit country-year aggregation strategy.

## What changed and why

- `classes.csv`
  - `GeographyGeometry` moved to high priority because boundary assets are now
    staged and needed for the map itself.
  - Core class notes were rewritten to reflect a map-first,
    observation-centric design.
- `relationships.csv`
  - Added explicit geometry provenance and observation-to-definition links so
    GeoBrowser can keep map assets and source semantics traceable.
  - Shifted documentation linkage toward `DatasetRelease`, which better matches
    how codebooks, PDFs, and compendia are actually versioned in the repo.
- `phase1_metrics.csv`
  - Notes now distinguish between metrics that are ready to harmonize soon
    versus metrics that remain deferred because the source data is not yet in a
    stable country-year observation shape.
- `properties_phase1.csv`
  - Added concrete geometry properties and stronger provenance properties for
    observations and indicator definitions.
  - This should make it easier to move from ontology discussion to a practical
    GeoBrowser CSV contract later.
- `example_nodes.csv` and `example_edges.csv`
  - Examples now include a geometry node and geometry-related edges so the
    starter graph better reflects the actual map product we are building.

## Related ontology information elsewhere in the repo

The main ontology-related references currently live outside this folder too:

- `AGENTS.md`
  - High-level project guardrails, including the note that ontology work is provisional until Armando's guidance is incorporated
- `TASKLIST.md`
  - Current education/Phase 1 priorities that should shape ontology scope
- `docs/Bounties/educational-inequality-map.md`
  - Canonical bounty brief and comparison goals
- `docs/Bounties/education-knowledge-graph-outline.md`
  - Earlier knowledge-graph framing, use cases, entity ideas, and next-step notes
- `docs/Bounties/educational-inequality-map-ontology.md`
  - The most detailed in-repo provisional ontology writeup so far
- `docs/Bounties/educational-inequality-map-sources.md`
  - Source catalog context that should inform which entities, metrics, and joins actually matter

## How to use this folder

Use these CSVs as lightweight working artifacts, not as a locked schema. They
are best for:

- checking whether candidate source fields map cleanly to a small shared set of classes
- deciding which properties are truly required for Phase 1 country-year comparisons
- keeping source-specific definitions separate from harmonized metric concepts
- testing import ideas for graph or tabular processing without committing to final modeling

## Recommended workflow

1. Use `docs/Bounties/educational-inequality-map-sources.md` to identify the next source or indicator family.
2. Use `phase1_metrics.csv` and `properties_phase1.csv` to decide the smallest useful harmonized representation.
3. Update `classes.csv` and `relationships.csv` only when the change improves current Phase 1 processing or clarifies a real source-mapping decision.
4. Revisit all of this after the March 31, 2026 ontology discussion.

## Important caution

If a choice would force hard-to-reverse ETL mappings, graph loaders, or
canonical IDs beyond the country-year Phase 1 layer, defer it until the
ontology discussion is settled.
