# U.S. Education Initiatives Research Process

This dataset needs a stricter evidence workflow than the global education map.
The goal is not just to list initiatives. The goal is to separate:

- what the initiative claimed it would do
- what policymakers and journalists said it did
- what stronger research designs suggest it actually changed

## Core rule

Do not treat a Wikipedia page, think-piece, advocacy site, or foundation summary
as sufficient evidence for initiative quality. Those sources are useful for
orientation, naming, timelines, and actor discovery, but not for final claims
about effectiveness.

## Evidence ladder

Use sources in this order whenever possible:

1. Official primary material
   - legislation
   - state agency guidance
   - initiative websites
   - grant announcements
   - implementation memos
2. Scholarly and technical evaluation
   - peer-reviewed articles
   - NBER / IZA / EdWorkingPaper / RAND / Brookings style working papers
   - university center evaluations
   - state or district accountability evaluations with methods sections
3. High-quality secondary synthesis
   - systematic reviews
   - meta-analyses
   - literature reviews from credible research organizations
4. Journalistic and commentary sources
   - explanatory reporting
   - investigative pieces
   - interviews and opinion essays

Journalism can surface controversy, implementation failure, or political
context, but it should not be the only basis for outcome claims.

## Minimum research packet per initiative

Each initiative should eventually have:

- 1 orientation source
- 1 primary implementation source
- 2 scholarly or technical evaluation sources if available
- 1 critical or dissenting source if credible criticism exists
- a short evidence note describing what is actually known versus inferred

If an initiative is too new for scholarly evaluation, mark it as `emerging` or
`implementation_only` rather than forcing a false quality claim.

## Research workflow

### 1. Frame the initiative correctly

Before searching, write down:

- exact initiative name
- alternate names and abbreviations
- sponsoring organization
- geography
- years active
- policy mechanism type

This prevents mixing a policy movement with one state implementation of that
movement.

### 2. Search by claim type

Run separate searches for:

- implementation details
- intended outcomes
- measured outcomes
- unintended effects
- critiques and replication challenges

Search pattern examples:

- `"<initiative name>" evaluation`
- `"<initiative name>" quasi-experimental`
- `"<initiative name>" outcomes`
- `"<initiative name>" criticism`
- `site:eric.ed.gov "<initiative name>"`
- `site:nber.org "<initiative name>"`
- `site:edworkingpapers.com "<initiative name>"`

### 3. Extract claims as atomic statements

Do not store broad summaries first. Store discrete claims such as:

- third-grade reading scores increased after adoption
- gains were concentrated among lower-performing students
- retention policy may explain part of the effect
- implementation fidelity varied across districts

Each claim should later map to one or more sources.

### 4. Grade study quality

For each scholarly or technical source, note:

- design: descriptive, correlational, quasi-experimental, experimental, review
- unit: school, district, state, student
- sample and years
- treatment definition
- comparison group
- main limitation
- whether the source measures outcomes directly or proxies them

### 5. Resolve conflicts explicitly

When sources disagree, do not average them into a vague statement.
Write:

- where they agree
- where they conflict
- which source has the stronger design
- whether the disagreement is about implementation, timeframe, population, or
  outcome measure

### 6. Write the evidence note

The evidence note should answer:

- what happened
- what evidence supports it
- how strong that evidence is
- what remains uncertain

## Status labels

Use these in `initiative_evidence_reviews.csv`:

- `seed`: only seed row exists, not reviewed
- `orientation_complete`: names, dates, actors, and primary sources captured
- `implementation_only`: implementation sources exist, impact evidence weak or absent
- `scholarly_reviewed`: at least two serious evaluation sources reviewed
- `contested`: evidence base is mixed or politically disputed
- `emerging`: too new for quality claims

## Evidence score

Use a conservative 1-5 scale:

1. Anecdotal or advocacy-heavy only
2. Some credible descriptive support, weak causal inference
3. Moderate evidence with at least one serious evaluation
4. Strong evidence with multiple credible evaluations pointing in the same direction
5. Strong multi-source consensus with clear outcome evidence and limited major disputes

This score should reflect evidence quality, not whether the result is positive.

## Consensus direction

Allowed values:

- `positive`
- `mixed`
- `negative`
- `unclear`
- `not_yet_evaluable`

## What to capture in the template

`initiative_evidence_reviews.csv` is the summary layer. It should not hold full
notes or quotes. It should hold the distilled status for the viewer and future
ETL.

Recommended supporting files later:

- `initiative_claims.csv`
- `initiative_sources.csv`
- `initiative_quotes.md`

## Immediate next pass

For the current nine-row seed dataset:

1. Replace Wikipedia-only outcome summaries with better primary and scholarly anchors.
2. Separate statewide reforms from broader movements such as Science of Reading.
3. Mark new or emerging items as `not_yet_evaluable` until stronger outcome work exists.
4. Add at least one critical or mixed-evidence source for initiatives with strong public narratives.
