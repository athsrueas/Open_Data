# U.S. Education Initiatives Research and Ingestion Plan

This plan turns the U.S. initiatives subspace into a research-grade dataset.
It focuses on:

- identifying strong source stacks for each initiative
- deciding where each source should be retrieved from
- defining the pull-down and extraction tasks
- mapping extracted evidence into the repo data structures

## Canonical initiative set for the next pass

Use this as the working set for source mapping and evidence ingestion.

### Keep

- `mississippi-miracle`
- `literacy-based-promotion-laws`
- `common-core-state-standards`
- `gates-millennium-scholars`

### Reframe

- `science-of-reading-sor`
  - keep only as a `research_movement`, not as a single evaluable intervention

### Replace weak seed rows with better-documented interventions

- replace `science-of-mathematics-emerging` with `nclb-annual-testing-accountability`
- replace `southern-surge` with `chicago-test-based-promotion-accountability`
- replace `get-schooled-initiative` with `career-academies`
- replace `gates-foundation-education-initiatives` with `p-tech-9-14`
- add `careerwise-colorado`
- add `school-garden-interventions`
- add `school-cellphone-bans`

## Data structures to populate

### Summary layer

- `Education Initiatives/initiative_evidence_reviews.csv`

This stores initiative-level rollups:

- research status
- evidence score
- consensus direction
- confidence
- continuum metadata

### Source layer

- `Education Initiatives/initiative_sources.csv`

This stores one row per source with:

- initiative
- source role
- repository
- retrieval mode
- raw target path
- extraction priority

### Claim layer

- `Education Initiatives/initiative_claims.csv`

This stores atomic claims:

- claim text
- outcome domain
- population
- timeframe
- direction
- supporting source IDs
- conflicting source IDs

### Generated outputs

- `outputs/us_education_initiatives/subspace/initiatives.bundle.json`
- `outputs/us_education_initiatives/subspace/initiatives.flat.csv`
- `outputs/us_education_initiatives/subspace/catalog.json`

## Source repositories by type

### Official / primary

- Congress.gov
- state education agency pages
- district archive pages
- official initiative program sites
- official standards sites

Use these for:

- statute text
- implementation guidance
- eligibility rules
- program design
- official scope and geography

### Scholarly / technical

- NBER
- ERIC
- SAGE / AERA Open
- ScienceDirect
- MDRC
- Urban Institute
- Apprenticeship.gov for linked research PDFs

Use these for:

- causal estimates
- implementation studies
- subgroup analysis
- outcome definitions
- limitations

## Where to get papers and source files

### Best retrieval order

1. direct PDF from the publisher or repository
2. landing page + downloadable PDF
3. abstract page + bibliographic metadata when full text is not open
4. official HTML page capture when the source is web-native

### Repository notes

- `NBER`
  - usually gives both abstract page and stable PDF URL
  - preferred for working papers on testing/accountability and school phone bans
- `MDRC`
  - preferred for Career Academies and P-TECH reports
  - often has stable PDF documents
- `ERIC`
  - useful as an index when the journal page is harder to locate
  - capture ERIC metadata even if final full text comes from another host
- `ScienceDirect`
  - strong for economics and applied education papers
  - capture landing page metadata and PDF when access permits
- `SAGE / AERA Open`
  - useful for Common Core and Gates Millennium Scholars evaluation papers
- `state agency pages`
  - preferred source for laws, program guidance, and current implementation

## Pull-down workflow

### Phase 1. Source acquisition

For each row in `initiative_sources.csv`:

1. open the listed `url`
2. capture bibliographic metadata
3. download or save the PDF / page content into the `target_relpath`
4. record any missing or blocked access in `status` and `notes`

Target raw location pattern:

- `outputs/us_education_initiatives/sources/<target_relpath>`

Recommended file naming:

- `author_year_shorttitle.pdf`
- `agency_program_or_law.html`
- `pending.txt` for unresolved official archives

### Phase 2. Metadata extraction

Extract into `initiative_sources.csv` or a future structured table:

- authors
- publication year
- source organization
- source type
- geography
- study design
- full citation

### Phase 3. Claim extraction

For each evaluation or review source:

1. extract the discrete claims
2. assign outcome domain
3. assign direction
4. note population and timeframe
5. link supporting and conflicting source IDs

Write results into `initiative_claims.csv`.

### Phase 4. Evidence rollup

Update `initiative_evidence_reviews.csv`:

- `research_status`
- `evidence_score`
- `consensus_direction`
- `confidence_label`
- `quality_notes`
- continuum fields

## Initiative-by-initiative source stacks

### Mississippi Miracle

- primary:
  - Mississippi Department of Education LBPA page
- evaluation:
  - Spencer 2024 Economics of Education Review
- action:
  - extract effect sizes, cohorts, policy bundle components, limitations

### Literacy-Based Promotion Laws

- primary:
  - Mississippi LBPA page now
  - later add Florida and other state statutes
- evaluation:
  - Texas third-grade retention paper
- action:
  - treat as a policy family with state-level subcases

### Common Core State Standards

- primary:
  - Common Core introductory standards PDF
- evaluation:
  - Bleiberg 2021 AERA Open
- action:
  - capture heterogeneity and debate instead of overclaiming a single direction

### No Child Left Behind annual testing/accountability

- primary:
  - Congress.gov statute text
- evaluation:
  - Dee and Jacob 2009 NBER
- action:
  - extract tested grades, math vs reading, subgroup effects

### Chicago test-based promotion and accountability

- primary:
  - district archive policy language still needed
- evaluation:
  - Jacob 2002 NBER
  - Jacob and Lefgren 2002 NBER
- action:
  - separate accountability effects from remediation/retention effects

### Florida A+ accountability plan

- primary:
  - current Florida DOE school grades page
  - later find historical A+ archival page
- evaluation:
  - Figlio and Rouse 2006
- action:
  - capture both improvement effects and incentive/gaming concerns

### Career Academies

- primary:
  - National Career Academy Coalition standards or overview
- evaluation:
  - MDRC long-term report
- action:
  - extract randomized design, earnings impacts, subgroup findings

### P-TECH 9-14

- primary:
  - Texas Education Agency P-TECH page
- evaluation:
  - MDRC final report
- action:
  - separate implementation findings from measurable outcomes

### CareerWise Colorado

- primary:
  - CareerWise research archive
- evaluation:
  - MDRC study page
  - Harvard / Apprenticeship.gov report
- action:
  - distinguish descriptive pathway evidence from causal evidence

### School garden interventions

- primary:
  - TX Sprouts evaluation page
- evaluation:
  - academic performance cluster RCT
  - science knowledge study
- action:
  - treat as outdoor/hands-on learning evidence, not just health programming

### School cellphone bans

- evaluation:
  - NBER Florida paper
  - 2024 scoping review
- action:
  - assign reduced-tech continuum values and preserve mixed-evidence framing

## Tooling tasks

### Immediate

- keep `initiative_sources.csv` current
- keep `initiative_claims.csv` atomic and citation-linked
- run `python src/open_data/build_us_education_initiatives_subspace.py` after evidence rollups change

### Next scriptable additions

- downloader for `initiative_sources.csv` rows with direct PDFs
- metadata extractor for PDFs and HTML captures
- source-to-claim validator that flags claims with no supporting source IDs

## Exit criteria for Phase 1

A solid first research pass is complete when:

- every kept or replacement initiative has at least 1 primary source
- every evaluable initiative has at least 1 serious evaluation source
- at least 5 initiatives have extracted claims in `initiative_claims.csv`
- at least 5 initiatives are upgraded from `seed`
- the generated flat export no longer depends on Wikipedia-only rows for core evidence
