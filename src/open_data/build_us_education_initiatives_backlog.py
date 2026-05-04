from __future__ import annotations

import csv
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.open_data.us_education_initiatives import OUTPUT_DIR as SUBSPACE_OUTPUT_DIR
from src.open_data.us_education_initiatives import build_dataset, write_json

SUBSPACE_BUNDLE_PATH = ROOT / "outputs" / "us_education_initiatives" / "subspace" / "initiatives.bundle.json"
SOURCES_CSV_PATH = ROOT / "Education Initiatives" / "initiative_sources.csv"
ANCHORS_CSV_PATH = ROOT / "Education Initiatives" / "initiative_state_anchors.csv"
OUTPUT_DIR = ROOT / "outputs" / "us_education_initiatives" / "research"
STATE_GAPS_PATH = OUTPUT_DIR / "state_coverage_gaps.csv"
SOURCE_BACKLOG_PATH = OUTPUT_DIR / "source_research_backlog.csv"
ANCHOR_EXPANSION_PATH = OUTPUT_DIR / "anchor_expansion_seed.csv"


def load_bundle() -> dict[str, object]:
    return json.loads(SUBSPACE_BUNDLE_PATH.read_text(encoding="utf-8"))


def rebuild_subspace_bundle() -> None:
    dataset = build_dataset()
    write_json(SUBSPACE_OUTPUT_DIR / "initiatives.bundle.json", dataset)


def load_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return [{k: (v or "").strip() for k, v in row.items()} for row in csv.DictReader(handle)]


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def build_state_gaps(bundle: dict[str, object]) -> list[dict[str, str]]:
    states = bundle["stateMap"]["states"]
    rows: list[dict[str, str]] = []
    for state in sorted(states, key=lambda item: item["name"]):
        direct = int(state["directAnchorCount"])
        combined = int(state["combinedCount"])
        rows.append(
            {
                "state_code": str(state["code"]),
                "state_name": str(state["name"]),
                "inset_group": str(state["insetGroup"]),
                "direct_anchor_count": str(direct),
                "national_context_count": str(state["nationalContextCount"]),
                "combined_count": str(combined),
                "priority": (
                    "high"
                    if direct == 0
                    else "medium"
                    if direct == 1
                    else "low"
                ),
                "needs_direct_anchor": "yes" if direct == 0 else "no",
            }
        )
    return rows


def build_source_backlog(bundle: dict[str, object], source_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    initiatives = {item["id"]: item for item in bundle["initiatives"]}
    by_initiative: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in source_rows:
        by_initiative[row["initiative_id"]].append(row)

    backlog: list[dict[str, str]] = []
    for initiative_id, item in sorted(initiatives.items(), key=lambda pair: pair[1]["initiative"]):
        rows = by_initiative.get(initiative_id, [])
        role_counts = Counter(r["source_role"] for r in rows)
        tier_counts = Counter(r["source_tier"] for r in rows)
        status_counts = Counter(r["status"] for r in rows)
        missing_primary = "yes" if role_counts.get("primary", 0) == 0 else "no"
        missing_eval = "yes" if role_counts.get("evaluation", 0) == 0 else "no"
        pending_search_count = status_counts.get("pending_search", 0)
        if missing_primary == "yes" or missing_eval == "yes" or pending_search_count > 0:
            priority = "high" if missing_eval == "yes" or pending_search_count > 0 else "medium"
            backlog.append(
                {
                    "initiative_id": initiative_id,
                    "initiative": str(item["initiative"]),
                    "research_status": str(item["evidence"]["researchStatus"]),
                    "sources_total": str(len(rows)),
                    "primary_sources": str(role_counts.get("primary", 0)),
                    "evaluation_sources": str(role_counts.get("evaluation", 0)),
                    "review_sources": str(role_counts.get("review", 0)),
                    "official_sources": str(tier_counts.get("official", 0)),
                    "scholarly_sources": str(tier_counts.get("scholarly", 0)),
                    "technical_sources": str(tier_counts.get("technical", 0)),
                    "pending_search_sources": str(pending_search_count),
                    "missing_primary_source": missing_primary,
                    "missing_evaluation_source": missing_eval,
                    "priority": priority,
                }
            )
    return backlog


def build_anchor_expansion_seed(bundle: dict[str, object], anchor_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    states = bundle["stateMap"]["states"]
    existing_pairs = {(row["state_code"], row["initiative_id"]) for row in anchor_rows}

    # Prefer practical expansion families with clear state comparability.
    expansion_initiatives = [
        "literacy-based-promotion-laws",
        "school-cellphone-bans-phone-free-school-policies",
        "florida-a-school-grading-accountability-plan",
        "no-child-left-behind-annual-testing-accountability",
        "careerwise-colorado-youth-apprenticeship",
        "p-tech-9-14",
    ]

    rows: list[dict[str, str]] = []
    for state in sorted(states, key=lambda item: item["name"]):
        state_code = str(state["code"])
        for initiative_id in expansion_initiatives:
            if (state_code, initiative_id) in existing_pairs:
                continue
            rows.append(
                {
                    "state_code": state_code,
                    "state_name": str(state["name"]),
                    "initiative_id": initiative_id,
                    "anchor_type": "pending_research",
                    "anchor_strength": "unknown",
                    "source_ids": "",
                    "evidence_basis": "",
                    "status": "todo",
                    "notes": "Add when official state implementation or strong evaluation evidence is identified.",
                }
            )
    return rows


def main() -> None:
    rebuild_subspace_bundle()
    bundle = load_bundle()
    source_rows = load_csv(SOURCES_CSV_PATH)
    anchor_rows = load_csv(ANCHORS_CSV_PATH)

    state_gaps = build_state_gaps(bundle)
    source_backlog = build_source_backlog(bundle, source_rows)
    anchor_expansion_seed = build_anchor_expansion_seed(bundle, anchor_rows)

    write_csv(STATE_GAPS_PATH, state_gaps)
    write_csv(SOURCE_BACKLOG_PATH, source_backlog)
    write_csv(ANCHOR_EXPANSION_PATH, anchor_expansion_seed)

    print(f"Wrote {STATE_GAPS_PATH}")
    print(f"Wrote {SOURCE_BACKLOG_PATH}")
    print(f"Wrote {ANCHOR_EXPANSION_PATH}")
    print(f"Refreshed {SUBSPACE_BUNDLE_PATH}")
    print(f"State gaps rows: {len(state_gaps)}")
    print(f"Source backlog rows: {len(source_backlog)}")
    print(f"Anchor expansion seed rows: {len(anchor_expansion_seed)}")


if __name__ == "__main__":
    main()
