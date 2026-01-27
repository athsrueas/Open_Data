# crypto-behavior-kg.md

## Goal

Build an open, continuously-augmented **Crypto Behavior Knowledge Graph** that connects **on-chain activity + labels + entity attribution** across **multiple chains** to enable **behavioral insights and detection** (fraud, sybil patterns, laundering, and altruistic flows like donations/public goods funding).

Primary success criteria:
- **Stable ontology** (versioned, backwards-compatible)
- **Reproducible ETL** (deterministic, pinned inputs, tested)
- **Evidence-first claims** (auditable provenance per assertion)
- **Composable graph updates** (small, reviewable deltas; GRC-20 friendly)

---

## 1. Scope & use cases (bounty-ready)

### Core use cases
- **Detect:** Sybil clusters, drainer campaigns, phishing/scam networks, laundering paths
- **Attribute:** Address/contract clusters to **actors/entities** (exchanges, protocols, scammers, sanctioned entities)
- **Track:** Incident-centric graphs (hack → exploited contract → drained wallets → cash-out paths)
- **Represent altruism:** Donation flows (grants, public goods, charities), donor networks, repeat funders

### Support queries like
- “Which clusters share common **funders** and **sweepers** within a **[time window]**?”
- “Which addresses are **flagged as phishing/drainer** and have **>N downstream hops** to known cash-out endpoints?”
- “Which actors show **high inbound** from flagged sources but **low direct interaction** with DeFi protocols?”
- “Which donation recipients saw **>X% donor overlap** between rounds and **net growth** in repeat donors?”

---

## 2. Core datasets to integrate (and build upon)

### Domain A: On-chain activity (transactions, traces, holders)
- Ethereum ETL tooling: https://github.com/blockchain-etl/ethereum-etl
- Ethereum ETL BigQuery docs: https://ethereum-etl.readthedocs.io/en/latest/google-bigquery/
- BlockSci (analysis platform + reference paper): https://github.com/citp/BlockSci and https://www.usenix.org/system/files/sec20-kalodner.pdf

### Domain B: Fraud / scam / phishing labels (seed claims)
- CryptoScamDB: https://cryptoscamdb.org/ and https://github.com/CryptoScamDB
- ScamSniffer scam database: https://github.com/scamsniffer/scam-database
- MetaMask phishing detect list: https://github.com/MetaMask/eth-phishing-detect
- Forta labelled datasets: https://github.com/forta-network/labelled-datasets
- Chainabuse (public reporting context): https://www.circle.com/pressroom/crypto-industry-leaders-champion-free-multi-chain-scam-reporting-tool-chainabuse-to-empower-users-against-crypto-fraud

### Domain C: Sybil research & relationship patterns (reproducible clustering)
- Arbitrum Foundation sybil-detection: https://github.com/ArbitrumFoundation/sybil-detection

### Domain D: Attribution / entity tags (actors ↔ addresses)
- GraphSense TagPacks: https://github.com/graphsense/graphsense-tagpacks
- GraphSense TagPack tooling: https://github.com/graphsense/graphsense-tagpack-tool
- GraphSense “Actors” concept: https://github.com/graphsense/graphsense-tagpacks/wiki/GraphSense-Actors

### Domain E: Authoritative “known bad” (sanctions)
- OFAC Sanctions List Service: https://ofac.treasury.gov/sanctions-list-service
- OFAC FAQ (virtual currency identifiers): https://ofac.treasury.gov/faqs/562
- Open extractor: https://github.com/0xB10C/ofac-sanctioned-digital-currency-addresses

### Domain F: Altruism / public goods flows (optional, for “good behavior” graph)
- Gitcoin ecosystem (rounds/flows context): https://www.gitcoin.co/

---

## 3. Reference tables

### 3.1 Primary data sources (minimum set)

| Source | Coverage | Example indicators / objects | Access |
|---|---|---|---|
| ethereum-etl | Chain data extraction | tx, logs, traces, blocks | https://github.com/blockchain-etl/ethereum-etl |
| CryptoScamDB | Scam labels | domains, addresses, categories | https://cryptoscamdb.org/ |
| ScamSniffer | Phishing labels | domains, addresses | https://github.com/scamsniffer/scam-database |
| OFAC SLS | Sanctions | sanctioned identifiers | https://ofac.treasury.gov/sanctions-list-service |
| GraphSense TagPacks | Attribution | actors, tags, categories | https://github.com/graphsense/graphsense-tagpacks |
| Arbitrum sybil-detection | Sybil patterns | funder/sweep graphs, clusters | https://github.com/ArbitrumFoundation/sybil-detection |

### 3.2 Standards & interoperability (recommended)

| Resource | Why it matters | URL |
|---|---|---|
| PROV-O | provenance/evidence modeling | https://www.w3.org/TR/prov-o/ |
| CAIP-10 | chain-agnostic account identifiers | https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-10.md |
| CAIP-19 | chain-agnostic asset identifiers | https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-19.md |

---

## 4. Stable ontology plan (curator governance)

### 4.1 Ontology principles
- **Versioned schema**: `vMAJOR.MINOR.PATCH`
  - MAJOR: breaking changes (rare; requires migration tooling)
  - MINOR: additive changes only
  - PATCH: clarifications/typos/metadata
- **Backwards compatibility contract**
  - Never repurpose a field/edge type silently
  - Deprecate with explicit replacement and effective date
- **Controlled vocabularies**
  - Label categories must be enumerated (no free-text categories in canonical graph)

### 4.2 Canonical identifiers
- Accounts: **CAIP-10**
- Assets: **CAIP-19**
- Chain reference: CAIP chain namespace (e.g., `eip155:1`)

### 4.3 Claim model (evidence-first)
Every “behavior” statement is represented as a **Claim** node that is:
- asserted by a curator or ETL run
- supported by Evidence artifacts
- scoped (chain + time range)
- confidence-rated (optional but recommended)

---

## 5. Entity model (minimum viable, crypto-native)

### 5.1 Nodes
- **Chain**: `{chain_id}`
- **Account** (EOA): `{account_id (CAIP-10)}`
- **Contract**: `{account_id (CAIP-10), code_hash?, creation_tx?}`
- **Asset**: `{asset_id (CAIP-19)}`
- **Transaction**: `{tx_hash, chain_id, time}`
- **Actor** (entity): `{name, type (exchange/protocol/person/etc.), registry_refs?}`
- **Cluster**: `{cluster_id, method, parameters_hash}`
- **Incident**: `{incident_id, type (hack/drainer/phishing/etc.), time_range}`
- **Label**: `{label_id, category (enum), description}`
- **Claim**: `{claim_id, statement_type, scope, confidence}`
- **Evidence**: `{evidence_id, kind (dataset_row/report/tx/proof), uri, hash?}`
- **Dataset**: `{publisher, dataset_name, version, snapshot_date, source_uri}`
- **ETLRun**: `{pipeline_name, version, input_hash, run_time}`

### 5.2 Relationships
- Account/Contract —**INTERACTED_WITH**→ Contract
- Account/Contract —**TRANSFERRED_TO**→ Account/Contract (optionally via Transaction)
- Actor —**CONTROLS**→ Account/Contract
- Account/Contract —**MEMBER_OF**→ Cluster
- Account/Contract/Actor —**INVOLVED_IN**→ Incident
- Account/Contract —**FLAGGED_AS**→ Label (SHOULD be mediated via Claim in curated layer)
- Claim —**SUPPORTED_BY**→ Evidence
- Claim —**ASSERTED_BY**→ Dataset / ETLRun / CuratorIdentity
- Entity —**SAME_AS**→ Entity (explicit equivalence; never implicit)

---

## 6. Data normalization & reproducible ETL (deterministic pipeline spec)

### 6.1 Reproducible ETL requirements (must-have)
- Inputs are **pinned** (commit hash, snapshot date, or exact query export)
- Pipeline is **deterministic** given pinned inputs
- Output is **content-addressed** (hash-based) and diffable
- Includes **tests**
  - schema validation
  - golden-file sample outputs
  - basic invariants (no invalid CAIP IDs, no missing provenance)

### 6.2 Recommended repository layout for each ETL module
- `extract/` (download + snapshot metadata)
- `transform/` (normalize → canonical tables/JSON)
- `load/` (emit graph deltas / GRC-20 ops)
- `tests/` (schema + golden samples)
- `docker/` (Dockerfile + lockfiles)
- `README.md` (how to run; what it produces; expected hashes)

---

## 7. Knowledge graph structure & publishing

- Model type: **Property graph** (recommended for behavior traversals) or **RDF** (if prioritizing interoperability)
- Storage: **Neo4j** / **RDF store** / other
- Access: **Cypher** / **SPARQL** / **REST**
- Ontology/Schema: versioned (see section 4)
- Publishing format: **GRC-20** (Geo ecosystem)
  - GRC-20 format: https://github.com/geobrowser/grc-20
  - Recipes: https://github.com/geobrowser/grc-20-recipes
  - TS tooling: https://github.com/graphprotocol/grc-20-ts
- Geo tooling context:
  - Curator program: https://www.geobrowser.io/curator-program
  - GeoGenesis: https://github.com/geobrowser/geogenesis

---

## 8. Example instance (concrete pattern)

**Claim:** “Account `eip155:1:0x...` is flagged as `drainer` for Incident `INC-2026-01-XYZ`”

- Account HAS_CLAIM Claim#123
- Claim#123 FLAG_CATEGORY Label:drainer
- Claim#123 INVOLVED_IN Incident:INC-2026-01-XYZ
- Claim#123 SUPPORTED_BY Evidence:TxHash / ReportURL / DatasetRow
- Claim#123 ASSERTED_BY ETLRun:scamsniffer_ingest@v1.2.0 (input_hash=...)

---

## 9. Derived insights & query cookbook (initial set)

1. **Sybil discovery**
   - Find clusters with shared funders + high internal transfer density over [T]
2. **Cash-out pathing**
   - For flagged addresses, compute shortest paths to known exchange deposit clusters
3. **Incident expansion**
   - For an incident seed address, expand to 2-hop neighborhood and rank by value moved
4. **Label conflicts**
   - Show accounts with contradictory labels across datasets; require curator review
5. **Altruism networks**
   - Identify repeat donors and high-overlap donor communities across grant rounds

---

## 10. Deliverables (initial phase)

- **Ontology v0.1.0**: node/edge types, controlled vocabularies, identifier policy
- **Two reproducible ETL modules** (minimum):
  1) ScamSniffer → Claims/Labels
  2) OFAC → Claims/Labels
- **Sample graph bundle**:
  - N accounts, M claims, K incidents, with full provenance
- **Query cookbook**: 5–10 queries with expected outputs
- **Documentation**: sources, assumptions, licensing notes, limitations

---

## 11. Risks & assumptions

- Attribution is probabilistic; must represent uncertainty (confidence + evidence)
- Label feeds vary in quality; must enforce source tiering and conflict review
- Cross-chain identity linking is hard; start chain-scoped, add equivalence later
- Licensing/terms differ; store only what is permitted and cite sources

---

## 12. Next steps

1. Choose the first **label vocabulary** (enum list) and publish Ontology v0.1.0
2. Draft an ETL mapping sheet: source → fields → transforms → claims emitted
3. Implement ETL Module #1 (ScamSniffer) with tests + pinned snapshot
4. Implement ETL Module #2 (OFAC) with tests + pinned snapshot
5. Add a curator review checklist and start publishing GRC-20 deltas
