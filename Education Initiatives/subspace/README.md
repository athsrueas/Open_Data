# U.S. Education Initiatives Subspace

This subspace is the working package for U.S.-specific education intervention
datasets and the visualization tooling that sits on top of them.

## What belongs here

- source manifests for the initiative datasets
- provisional schema contracts
- dimension planning for evidence and continuum scoring
- build conventions for normalized exports and viewer payloads

## Current source inputs

- `../education_initiatives.csv`
- `../initiative_evidence_reviews.csv`
- `../initiative_sources.csv`
- `../initiative_claims.csv`
- `../research_process.md`

## Build outputs

The subspace build writes:

- `outputs/us_education_initiatives/subspace/initiatives.bundle.json`
- `outputs/us_education_initiatives/subspace/initiatives.flat.csv`
- `outputs/us_education_initiatives/subspace/catalog.json`
- `viewer/us_education_initiatives/data.js`

The source-manifest helper writes:

- `outputs/us_education_initiatives/sources/source_manifest.json`
- `outputs/us_education_initiatives/sources/download_queue.csv`

## Build commands

```bash
python src/open_data/build_us_education_initiatives_subspace.py
python src/open_data/build_us_education_initiatives_source_manifest.py
```

The legacy viewer-only build still exists, but the subspace build is now the
canonical path because it writes both reusable data exports and the viewer
payload.

## Design direction

This subspace should support:

- replacing weak initiative rows with better-documented interventions
- evidence-oriented comparison instead of flat descriptive summaries
- continuum scoring for topics such as testing intensity, technology use,
  work-based learning, and outdoor learning
- future geospatial and timeline views without locking into a single front-end
  contract too early
- structured source acquisition and claim extraction for each initiative
