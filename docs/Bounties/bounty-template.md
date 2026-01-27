```md
# Work Outline (Generic Template): Curated Knowledge Graph with Stable Ontology + Reproducible ETL

## Goal
Build a knowledge graph that connects **[domains]** across **[geographies / networks]** to enable **[insights / decisions / questions]**, with a hard quality bar for:
- **Stable, versioned ontology**
- **Reproducible ETL (deterministic, pinned inputs, tested)**
- **Evidence-first claims (auditable provenance)**
- **Composable updates (small, reviewable deltas)**

---

## 1) Scope & core query intents
### Use cases
- **Detect:** [pattern types: anomalies, clusters, fraud, gaps, outliers]
- **Attribute:** [entities → owners/actors/categories]
- **Track:** [incidents/programs/interventions over time]
- **Explain:** [drivers, segments, causal hypotheses]
- **Benchmark:** [peer comparisons, cohorts, targets]

### Query intents (examples)
- “Which **[entities]** changed **[input]** by > **[X]** and improved **[outcome]** by > **[Y]** over **[T]**?”
- “Which **[entities]** show **[high input]** but **[low outcome]**?”
- “What are the top **[clusters/communities]** by **[metric]** in **[time window]**?”
- “Which assertions conflict across sources and require review?”

---

## 2) Datasets to build on
Describe the minimum viable set of sources for Phase 1.

### Domain A: [Inputs / activity / investment]
- [Source 1]: [what it provides] — [URL]
- [Source 2]: [what it provides] — [URL]

### Domain B: [Outcomes / results]
- [Source 3]: [what it provides] — [URL]
- [Source 4]: [what it provides] — [URL]

### Domain C: [Context / demographics / attribution]
- [Source 5]: [what it provides] — [URL]

### Domain D: [Authoritative labels / ground truth] (optional)
- [Source 6]: [what it provides] — [URL]

### Reference table: primary data sources
| Source | Coverage | Example fields/indicators | Access |
|---|---|---|---|
| [Name] | [Global/Regional/Network] | [Indicator list] | [URL] |
| [Name] | [Global/Regional/Network] | [Indicator list] | [URL] |

---

## 3) Stable ontology (minimum viable)
### Ontology principles
- **Semantic versioning**: `vMAJOR.MINOR.PATCH`  
  - MAJOR: breaking changes (requires migration)
  - MINOR: additive only
  - PATCH: clarifications/metadata
- **Controlled vocabularies** for key categories (no free-text in canonical graph)
- **Deprecate, don’t repurpose**: explicit replacements + effective date
- **Naming rules**: [prefixes, casing, namespaces, ID fields]

### Identifier strategy
- Canonical IDs for core entities: **[standard IDs]**
- Cross-source join keys: **[primary keys + normalization rules]**

### Claim-first model (evidence & provenance)
Represent high-stakes statements as **Claims** (not raw edges), requiring:
- **Evidence**: [dataset row / report / transaction / measurement / document]
- **Asserter**: [ETL run / dataset / curator/reviewer]
- **Scope**: [time range, geography/network, version]
- **Confidence** (optional): [0–1 or tiered]

Provenance reference (optional):
- [PROV-O or other provenance standard] — [URL]

---

## 4) Entity model (starter set)
### Nodes
- **Entity**: [Country/Region/Account/Organization/etc.]
- **Metric/Indicator**: [name, definition, unit]
- **Observation/Event**: [value, time, unit, flags]
- **Actor/Owner** (optional): [real-world entity]
- **Cluster/Group** (optional): [method, parameters]
- **Incident/Program** (optional): [type, time_range]
- **Label**: [category (enum), description]
- **Claim**: [statement_type, scope, confidence]
- **Evidence**: [kind, URI, hash?]
- **Dataset**: [publisher, version, snapshot_date]
- **ETLRun**: [pipeline_name, version, input_hash, run_time]

### Relationships
- Entity —HAS_OBSERVATION→ Observation/Event
- Observation/Event —MEASURES→ Metric/Indicator
- Observation/Event —FROM_DATASET→ Dataset
- Entity —IN_GROUP→ Cluster/Group (optional)
- Actor —ASSOCIATED_WITH→ Entity (optional)
- Entity —INVOLVED_IN→ Incident/Program (optional)
- Claim —SUPPORTED_BY→ Evidence
- Claim —ASSERTED_BY→ Dataset/ETLRun/Reviewer
- Entity —SAME_AS→ Entity (explicit equivalence only)

---

## 5) Reproducible ETL standard (required)
### Minimum ETL requirements
- **Pinned inputs**: [commit hash / snapshot date / exported query artifact]
- **Deterministic transform**: same inputs → same outputs
- **Validation tests**:
  - schema validation
  - golden-file samples
  - invariants ([ID validity], [no missing provenance], etc.)
- **Content-addressed outputs**: outputs are hashable/diffable bundles
- **Clear contracts**: input/output schemas + field semantics

### Suggested module layout
- `extract/` (download + snapshot metadata)
- `transform/` (normalize → canonical tables/JSON)
- `load/` (emit graph bundles / operations)
- `tests/` (schema + golden samples + invariants)
- `docker/` (Dockerfile + lockfiles)
- `README.md` (one-command runbook + expected outputs)

---

## 6) Publishing & governance
- Publish changes as **small deltas**: [operations/bundles/patches]
- Review gates (suggested):
  - new label categories / vocab terms
  - entity equivalence links (SAME_AS)
  - actor/owner attributions
  - ontology MINOR/MAJOR changes
- Conflict handling:
  - record competing claims + evidence
  - define precedence rules by source tier

---

## 7) Deliverables (Phase 1)
- Ontology **v0.1.0**: types, vocabularies, ID policy, deprecation rules
- **[N] ETL modules**: reproducible + tested
- Minimal sample graph: **[N entities]**, **[M metrics/labels]**, **[time span]**
- Query cookbook: **[5–10]** queries with expected outputs
- README: sources, assumptions, limitations, licensing notes

---

## 8) Bounty-sized tasks (high leverage)
- ETL: ingest **[Source X]** → Claims/Labels/Observations (pinned snapshot + tests)
- Ontology: publish **[vocabulary]** + naming rules + deprecation/migration notes
- Entity resolution: **[ActorPack/registry]** format + reconciliation rules
- Exporter: **[analysis output]** → Cluster/Claims/Evidence (reproducible parameters)
- Governance: reviewer checklist + conflict resolution workflow

---
```
