# Education Dashboard Change Requests (May 2026)

## Purpose
Translate stakeholder change requests and recommendations into an execution-ready plan for:
- data quality
- dashboard narrative design
- repository/subspace structure
- bounty publication readiness

## Product direction
- Primary audience: journalists, concerned citizens, and parents.
- Primary mode: story-led investigative dashboard, not raw-data-first tooling.
- Publication standard: do not publish publicly until state coverage and outcome panel depth are sufficient to avoid misleading conclusions.

## Prioritized execution plan

### Priority 0: Data reliability gate (must complete before public launch)
1. Build out state-year outcomes panel depth across:
   - NAEP (g4/g8 reading/math)
   - SAT + participation
   - ACT + participation
   - graduation (ACGR)
   - absenteeism
   - socioeconomic controls (poverty/FRPL proxy)
   - connectivity/device access where defensible
2. Enforce provenance and comparability metadata on every numeric row:
   - `source_release_id`
   - `source_row_id`
   - `comparability_flag`
3. Add publication-readiness checks:
   - per-indicator state coverage threshold
   - per-indicator year-span threshold
   - explicit warnings for partial comparability windows

### Priority 1: Story-led dashboard redesign
1. Replace generic dashboard framing with headline-led narrative blocks.
2. Add short explanatory text beside each map and comparison panel.
3. Add “surprising finding” callouts with evidence links.
4. Add side-by-side comparative maps:
   - state vs state
   - period vs period
   - initiative-adoption windows (pre/post)

### Priority 2: Insight framing and analysis
1. Add trend-change analysis tied to initiative timing.
2. Add negative/neutral finding surfacing (not just positive impact framing).
3. Add cost-effectiveness lens where spending and outcomes can be joined.
4. Add structured claim cards with direct source and confidence context.

### Priority 3: Repository and GEO space operations
1. Prepare a dedicated education-data repository split plan from general open-data scope.
2. Create and grant editorship in “Education Data Sets” subspace.
3. Resolve credit/bounty blockers and publish bounty pipeline.
4. Track asynchronous coordination and blockers in a single running ops note.

## Ownership map
- Thomas Freestone:
  - dashboard audience + storytelling redesign
  - data depth expansion and provenance-first extraction
  - ontology and GEO graph integration path
- Bertrand Armando:
  - subspace creation, sharing, and permissioning support
  - bounty publication unblock support
- Adam Ficher / Nick:
  - credits/points unblock and bounty funding pathway
  - examples/inspiration material sharing

## Immediate next sprint (recommended)
1. Finish loading SAT/ACT state-year series with participation controls.
2. Load ACGR and absenteeism state-year series.
3. Implement coverage/quality publish gate report.
4. Ship first narrative dashboard pass with:
   - headline panel
   - 2 to 3 evidence callouts
   - side-by-side map module
