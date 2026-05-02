# U.S. Education Initiatives Research Task List

## Phase 0. Canonicalize the initiative list

- [ ] Mark weak seed rows for replacement in `education_initiatives.csv`.
- [ ] Add replacement rows for `nclb-annual-testing-accountability`, `chicago-test-based-promotion-accountability`, `florida-a-plus-accountability`, `career-academies`, `p-tech-9-14`, `careerwise-colorado`, `school-garden-interventions`, and `school-cellphone-bans`.
- [ ] Keep `science-of-reading-sor` only if it remains explicitly labeled as a `research_movement`.

## Phase 1. Build the source inventory

- [ ] Populate `initiative_sources.csv` for every kept and replacement initiative.
- [ ] For each initiative, ensure at least one `primary` source row exists.
- [ ] For each evaluable initiative, ensure at least one `evaluation` source row exists.
- [ ] Add one `review` or `critical` source where evidence is mixed or contested.
- [ ] Resolve all `pending_search` rows by finding stable official pages or archive substitutes.

## Phase 2. Pull down the source files

- [ ] Create `outputs/us_education_initiatives/sources/raw/official/`.
- [ ] Create `outputs/us_education_initiatives/sources/raw/scholarly/`.
- [ ] Create `outputs/us_education_initiatives/sources/raw/technical/`.
- [ ] Download direct PDFs from NBER, MDRC, and Apprenticeship.gov where available.
- [ ] Save HTML snapshots or metadata captures for state agency and program pages.
- [ ] Record blocked or paywalled sources in `initiative_sources.csv` rather than silently skipping them.

## Phase 3. Extract evidence

- [ ] For each evaluation source, record study design.
- [ ] For each evaluation source, record geography and population.
- [ ] For each evaluation source, record main outcome measures.
- [ ] For each evaluation source, record limitations and caveats.
- [ ] Write atomic findings into `initiative_claims.csv`.

## Phase 4. Update evidence reviews

- [ ] Upgrade `research_status` from `seed` where orientation work is complete.
- [ ] Assign `evidence_score` for reviewed initiatives.
- [ ] Assign `consensus_direction`.
- [ ] Write `quality_notes` with disagreements and uncertainty.
- [ ] Fill continuum fields for technology, testing, work-based learning, and outdoor learning.

## Phase 5. Rebuild and inspect outputs

- [ ] Run `python src/open_data/build_us_education_initiatives_subspace.py`.
- [ ] Inspect `initiatives.flat.csv` for empty evidence fields.
- [ ] Inspect `initiatives.bundle.json` to confirm new initiatives and updated statuses appear.
- [ ] Verify the viewer payload still loads after the evidence data expands.

## Priority order for first execution

- [ ] Mississippi Miracle
- [ ] No Child Left Behind annual testing/accountability
- [ ] Chicago test-based promotion/accountability
- [ ] Florida A+ accountability
- [ ] Career Academies
- [ ] P-TECH 9-14
- [ ] CareerWise Colorado
- [ ] School cellphone bans
- [ ] School garden interventions
- [ ] Common Core State Standards
