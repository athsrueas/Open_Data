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
