from __future__ import annotations

import csv
import json
import re
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parents[2]
SOURCE_DIR = ROOT / "Education Initiatives"
SOURCE_CSV_PATH = SOURCE_DIR / "education_initiatives.csv"
EVIDENCE_CSV_PATH = SOURCE_DIR / "initiative_evidence_reviews.csv"
STATE_LAYOUT_CSV_PATH = SOURCE_DIR / "state_tile_layout.csv"
STATE_ANCHOR_CSV_PATH = SOURCE_DIR / "initiative_state_anchors.csv"
SUBSPACE_DIR = SOURCE_DIR / "subspace"
SUBSPACE_MANIFEST_PATH = SUBSPACE_DIR / "manifest.json"
SUBSPACE_SCHEMA_PATH = SUBSPACE_DIR / "initiative_record.schema.json"
OUTPUT_DIR = ROOT / "outputs" / "us_education_initiatives" / "subspace"
VIEWER_DIR = ROOT / "viewer" / "us_education_initiatives"
VIEWER_DATA_JS_PATH = VIEWER_DIR / "data.js"


STATE_NAMES = {
    "alabama",
    "alaska",
    "arizona",
    "arkansas",
    "california",
    "colorado",
    "connecticut",
    "delaware",
    "florida",
    "georgia",
    "hawaii",
    "idaho",
    "illinois",
    "indiana",
    "iowa",
    "kansas",
    "kentucky",
    "louisiana",
    "maine",
    "maryland",
    "massachusetts",
    "michigan",
    "minnesota",
    "mississippi",
    "missouri",
    "montana",
    "nebraska",
    "nevada",
    "new hampshire",
    "new jersey",
    "new mexico",
    "new york",
    "north carolina",
    "north dakota",
    "ohio",
    "oklahoma",
    "oregon",
    "pennsylvania",
    "rhode island",
    "south carolina",
    "south dakota",
    "tennessee",
    "texas",
    "utah",
    "vermont",
    "virginia",
    "washington",
    "west virginia",
    "wisconsin",
    "wyoming",
}


REGION_KEYWORDS = {
    "southern": "South",
    "southern u.s.": "South",
    "midwest": "Midwest",
    "northeast": "Northeast",
    "west coast": "West Coast",
    "southwest": "Southwest",
}


STATE_CODE_TO_NAME = {
    "AL": "Alabama",
    "AK": "Alaska",
    "AZ": "Arizona",
    "AR": "Arkansas",
    "CA": "California",
    "CO": "Colorado",
    "CT": "Connecticut",
    "DE": "Delaware",
    "FL": "Florida",
    "GA": "Georgia",
    "HI": "Hawaii",
    "ID": "Idaho",
    "IL": "Illinois",
    "IN": "Indiana",
    "IA": "Iowa",
    "KS": "Kansas",
    "KY": "Kentucky",
    "LA": "Louisiana",
    "ME": "Maine",
    "MD": "Maryland",
    "MA": "Massachusetts",
    "MI": "Michigan",
    "MN": "Minnesota",
    "MS": "Mississippi",
    "MO": "Missouri",
    "MT": "Montana",
    "NE": "Nebraska",
    "NV": "Nevada",
    "NH": "New Hampshire",
    "NJ": "New Jersey",
    "NM": "New Mexico",
    "NY": "New York",
    "NC": "North Carolina",
    "ND": "North Dakota",
    "OH": "Ohio",
    "OK": "Oklahoma",
    "OR": "Oregon",
    "PA": "Pennsylvania",
    "RI": "Rhode Island",
    "SC": "South Carolina",
    "SD": "South Dakota",
    "TN": "Tennessee",
    "TX": "Texas",
    "UT": "Utah",
    "VT": "Vermont",
    "VA": "Virginia",
    "WA": "Washington",
    "WV": "West Virginia",
    "WI": "Wisconsin",
    "WY": "Wyoming",
}


def slugify(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")


def split_field(value: str) -> list[str]:
    normalized = re.sub(r"\s*[;/]\s*", "|", value.strip())
    normalized = re.sub(r"\s*,\s*", "|", normalized)
    parts = [part.strip() for part in normalized.split("|")]
    return [part for part in parts if part]


def parse_timeline(value: str) -> dict[str, object]:
    years = [int(match) for match in re.findall(r"\b(?:19|20)\d{2}\b", value)]
    start_year = years[0] if years else None
    end_year = years[-1] if years else None
    lower = value.lower()
    is_ongoing = "present" in lower
    if is_ongoing and end_year is not None:
        end_year = datetime.now(UTC).year

    era = "Unknown"
    if start_year is not None:
        era = f"{start_year // 10 * 10}s"

    return {
        "label": value,
        "startYear": start_year,
        "endYear": end_year,
        "isOngoing": is_ongoing,
        "era": era,
    }


def classify_location(value: str) -> tuple[str, list[str]]:
    lower = value.lower()
    tags: list[str] = []

    if "nationwide" in lower or "united states" in lower:
        return "national", ["United States"]

    if "multi-state" in lower or "multiple u.s. states" in lower:
        return "multi_state", ["Multiple states"]

    for keyword, label in REGION_KEYWORDS.items():
        if keyword in lower:
            tags.append(label)

    for state in sorted(STATE_NAMES):
        if state in lower:
            tags.append(state.title())

    if tags:
        if len([tag for tag in tags if tag in REGION_KEYWORDS.values()]) > 0 and len(tags) == 1:
            return "region", tags
        if len(tags) == 1:
            return "state", tags
        return "mixed", tags

    return "other", [value]


def score_initiative(row: dict[str, str]) -> int:
    score = 0
    if row["Timeline"] and "present" in row["Timeline"].lower():
        score += 3
    if "nationwide" in row["Location"].lower() or "united states" in row["Location"].lower():
        score += 2
    score += len(split_field(row["Policies/Mechanisms"]))
    return score


def load_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return [{key: (value or "").strip() for key, value in row.items()} for row in csv.DictReader(handle)]


def load_evidence_by_id() -> dict[str, dict[str, str]]:
    if not EVIDENCE_CSV_PATH.exists():
        return {}
    rows = load_rows(EVIDENCE_CSV_PATH)
    return {
        row["initiative_id"]: row
        for row in rows
        if row.get("initiative_id")
    }


def load_state_layout_rows() -> list[dict[str, str]]:
    if not STATE_LAYOUT_CSV_PATH.exists():
        return []
    return load_rows(STATE_LAYOUT_CSV_PATH)


def load_state_anchor_rows() -> list[dict[str, str]]:
    if not STATE_ANCHOR_CSV_PATH.exists():
        return []
    return load_rows(STATE_ANCHOR_CSV_PATH)


def build_state_map(initiatives: list[dict[str, object]]) -> dict[str, object]:
    layout_rows = load_state_layout_rows()
    anchor_rows = load_state_anchor_rows()
    by_id = {str(item["id"]): item for item in initiatives}

    national_ids = sorted(
        [str(item["id"]) for item in initiatives if str(item["locationScope"]) == "national"]
    )
    anchor_rows_by_state: dict[str, list[dict[str, str]]] = {}
    for row in anchor_rows:
        state_code = row.get("state_code", "").upper()
        if not state_code:
            continue
        anchor_rows_by_state.setdefault(state_code, []).append(row)

    states: list[dict[str, object]] = []
    direct_anchor_state_count = 0

    for layout in layout_rows:
        code = layout["state_code"].upper()
        anchors = anchor_rows_by_state.get(code, [])
        direct_ids = sorted({row["initiative_id"] for row in anchors if row.get("initiative_id") in by_id})
        all_ids = sorted(set(direct_ids) | set(national_ids))
        direct_items = [by_id[item_id] for item_id in direct_ids if item_id in by_id]
        all_items = [by_id[item_id] for item_id in all_ids if item_id in by_id]
        direct_anchor_count = len(direct_ids)
        if direct_anchor_count:
            direct_anchor_state_count += 1

        strongest_evidence = max(
            (
                int(str(item["evidence"].get("evidenceScore") or "0"))
                for item in all_items
            ),
            default=0,
        )
        testing_count = sum(
            1
            for item in direct_items
            if str(item["continuums"].get("testingIntensity")) in {"high", "very_high"}
        )
        work_based_count = sum(
            1
            for item in direct_items
            if str(item["continuums"].get("workBasedLearningIntensity")) in {"high", "very_high"}
        )
        outdoor_count = sum(
            1
            for item in direct_items
            if str(item["continuums"].get("outdoorLearningIntensity")) in {"high", "very_high"}
        )
        reduced_tech_count = sum(
            1
            for item in direct_items
            if str(item.get("theme")) == "reduced_technology_and_attention"
            or str(item["continuums"].get("technologyComparison")) == "high_tech_vs_low_tech"
        )
        high_tech_count = sum(
            1
            for item in direct_items
            if str(item["continuums"].get("technologyPosition")) == "high_tech"
            or str(item.get("theme")) == "ai_enabled_instruction_and_operations"
        )

        # Composite continuum score to give the map a stronger, interpretable gradient.
        # Higher = comparatively more low-tech/work-based/outdoor emphasis; lower = comparatively more high-tech/testing-heavy emphasis.
        continuum_score_raw = (
            50
            + (reduced_tech_count * 14)
            + (work_based_count * 10)
            + (outdoor_count * 8)
            - (high_tech_count * 14)
            - (max(0, testing_count - 1) * 6)
            + (direct_anchor_count * 4)
        )
        continuum_score = max(0, min(100, int(continuum_score_raw)))

        states.append(
            {
                "code": code,
                "name": layout["state_name"] or STATE_CODE_TO_NAME.get(code, code),
                "tileCol": int(layout["tile_col"]),
                "tileRow": int(layout["tile_row"]),
                "insetGroup": layout["inset_group"] or "main",
                "directAnchorCount": direct_anchor_count,
                "nationalContextCount": len(national_ids),
                "combinedCount": len(all_ids),
                "strongestEvidenceScore": strongest_evidence,
                "testingAnchorCount": testing_count,
                "workBasedAnchorCount": work_based_count,
                "outdoorAnchorCount": outdoor_count,
                "reducedTechnologyAnchorCount": reduced_tech_count,
                "highTechnologyAnchorCount": high_tech_count,
                "continuumBalanceScore": continuum_score,
                "anchorInitiativeIds": direct_ids,
                "nationalInitiativeIds": national_ids,
                "anchorDetails": [
                    {
                        "initiativeId": row["initiative_id"],
                        "initiative": str(by_id[row["initiative_id"]]["initiative"]) if row.get("initiative_id") in by_id else row.get("initiative_id", ""),
                        "anchorType": row.get("anchor_type", ""),
                        "anchorStrength": row.get("anchor_strength", ""),
                        "sourceIds": split_field(row.get("source_ids", "")),
                        "evidenceBasis": row.get("evidence_basis", ""),
                        "notes": row.get("notes", ""),
                    }
                    for row in anchors
                    if row.get("initiative_id") in by_id
                ],
            }
        )

    states.sort(key=lambda item: (str(item["insetGroup"]) != "main", int(item["tileRow"]), int(item["tileCol"]), str(item["code"])))

    return {
        "layoutKind": "state_tilegrid_with_insets",
        "metrics": [
            {"key": "continuumBalanceScore", "label": "Low-tech to high-tech continuum score"},
            {"key": "directAnchorCount", "label": "Direct evidence anchors"},
            {"key": "testingAnchorCount", "label": "Testing-heavy anchors"},
            {"key": "workBasedAnchorCount", "label": "Work-based learning anchors"},
            {"key": "outdoorAnchorCount", "label": "Outdoor learning anchors"},
            {"key": "reducedTechnologyAnchorCount", "label": "Reduced-tech anchors"},
            {"key": "combinedCount", "label": "Direct plus national context"},
        ],
        "summary": {
            "stateCount": len(states),
            "statesWithDirectAnchors": direct_anchor_state_count,
            "nationalInitiativeCount": len(national_ids),
            "directAnchorRowCount": len(anchor_rows),
        },
        "states": states,
    }


def build_dataset() -> dict[str, object]:
    rows = load_rows(SOURCE_CSV_PATH)
    evidence_by_id = load_evidence_by_id()

    initiatives: list[dict[str, object]] = []
    location_counts: Counter[str] = Counter()
    category_counts: Counter[str] = Counter()
    era_counts: Counter[str] = Counter()
    tag_counts: Counter[str] = Counter()
    evidence_status_counts: Counter[str] = Counter()

    for row in rows:
        initiative_id = slugify(row["Initiative"])
        evidence = evidence_by_id.get(initiative_id, {})
        location_scope, location_tags = classify_location(row["Location"])
        timeline = parse_timeline(row["Timeline"])
        category = row["Category"]
        entity_type = evidence.get("entity_type") or "unspecified"
        theme = evidence.get("theme") or "unspecified"
        score = score_initiative(row)

        focus_tags = split_field(row["Core Focus"])
        policy_tags = split_field(row["Policies/Mechanisms"])
        outcome_tags = split_field(row["Outcomes"])
        people = split_field(row["Key Figures"])
        source_host = urlparse(row["Source"]).netloc.replace("www.", "")

        category_counts[category] += 1
        location_counts[location_scope] += 1
        era_counts[str(timeline["era"])] += 1
        evidence_status_counts[evidence.get("research_status", "seed")] += 1

        for tag in focus_tags + policy_tags:
            tag_counts[tag] += 1

        initiatives.append(
            {
                "id": initiative_id,
                "initiative": row["Initiative"],
                "category": category,
                "entityType": entity_type,
                "theme": theme,
                "coreFocus": row["Core Focus"],
                "focusTags": focus_tags,
                "keyFigures": people,
                "timeline": timeline,
                "locationLabel": row["Location"],
                "locationScope": location_scope,
                "locationTags": location_tags,
                "policies": policy_tags,
                "outcomes": outcome_tags,
                "outcomeSummary": row["Outcomes"],
                "source": row["Source"],
                "sourceHost": source_host,
                "score": score,
                "evidence": {
                    "researchStatus": evidence.get("research_status", "seed"),
                    "evidenceScore": evidence.get("evidence_score", ""),
                    "consensusDirection": evidence.get("consensus_direction", ""),
                    "confidenceLabel": evidence.get("confidence_label", ""),
                    "qualityNotes": evidence.get("quality_notes", ""),
                    "scholarlySourcesReviewed": evidence.get("scholarly_sources_reviewed", ""),
                    "journalisticSourcesReviewed": evidence.get("journalistic_sources_reviewed", ""),
                    "lastReviewed": evidence.get("last_reviewed", ""),
                },
                "continuums": {
                    "technologyPosition": evidence.get("technology_position", ""),
                    "technologyComparison": evidence.get("technology_comparison", ""),
                    "testingIntensity": evidence.get("testing_intensity", ""),
                    "workBasedLearningIntensity": evidence.get("work_based_learning_intensity", ""),
                    "outdoorLearningIntensity": evidence.get("outdoor_learning_intensity", ""),
                },
            }
        )

    initiatives.sort(key=lambda item: (-int(item["score"]), str(item["initiative"])))
    state_map = build_state_map(initiatives)

    featured = [item["id"] for item in initiatives[:3]]
    latest_start = max(
        (
            item["timeline"]["startYear"]
            for item in initiatives
            if item["timeline"]["startYear"] is not None
        ),
        default=None,
    )

    summary = {
        "initiativeCount": len(initiatives),
        "categoryCount": len(category_counts),
        "latestStartYear": latest_start,
        "activeNowCount": sum(1 for item in initiatives if item["timeline"]["isOngoing"]),
        "evidenceStatuses": dict(sorted(evidence_status_counts.items())),
    }

    return {
        "title": "U.S. Education Initiatives Atlas",
        "subtitle": "A reusable initiative dataset and browser for education reforms, programs, and policy movements across the United States.",
        "generatedAt": datetime.now(UTC).isoformat(),
        "summary": summary,
        "featuredInitiativeIds": featured,
        "categoryCounts": [
            {"label": label, "count": count}
            for label, count in sorted(category_counts.items(), key=lambda item: (-item[1], item[0]))
        ],
        "locationCounts": [
            {"scope": scope, "count": count}
            for scope, count in sorted(location_counts.items(), key=lambda item: (-item[1], item[0]))
        ],
        "eraCounts": [
            {"era": era, "count": count}
            for era, count in sorted(era_counts.items(), key=lambda item: item[0])
        ],
        "topTags": [{"label": label, "count": count} for label, count in tag_counts.most_common(12)],
        "stateMap": state_map,
        "initiatives": initiatives,
    }


def build_subspace_catalog(dataset: dict[str, object]) -> dict[str, object]:
    return {
        "subspace": "us_education_initiatives",
        "title": dataset["title"],
        "generatedAt": dataset["generatedAt"],
        "sourcePaths": {
            "initiativesCsv": str(SOURCE_CSV_PATH.relative_to(ROOT)),
            "evidenceCsv": str(EVIDENCE_CSV_PATH.relative_to(ROOT)),
            "stateTileLayoutCsv": str(STATE_LAYOUT_CSV_PATH.relative_to(ROOT)),
            "stateAnchorsCsv": str(STATE_ANCHOR_CSV_PATH.relative_to(ROOT)),
            "manifest": str(SUBSPACE_MANIFEST_PATH.relative_to(ROOT)),
            "schema": str(SUBSPACE_SCHEMA_PATH.relative_to(ROOT)),
        },
        "outputs": {
            "bundleJson": str((OUTPUT_DIR / "initiatives.bundle.json").relative_to(ROOT)),
            "flatCsv": str((OUTPUT_DIR / "initiatives.flat.csv").relative_to(ROOT)),
            "statesFlatCsv": str((OUTPUT_DIR / "states.flat.csv").relative_to(ROOT)),
            "catalogJson": str((OUTPUT_DIR / "catalog.json").relative_to(ROOT)),
            "viewerDataJs": str(VIEWER_DATA_JS_PATH.relative_to(ROOT)),
        },
        "summary": dataset["summary"],
    }


def build_flat_rows(dataset: dict[str, object]) -> list[dict[str, str]]:
    flat_rows: list[dict[str, str]] = []
    for item in dataset["initiatives"]:
        evidence = item["evidence"]
        continuums = item["continuums"]
        timeline = item["timeline"]
        flat_rows.append(
            {
                "initiative_id": str(item["id"]),
                "initiative": str(item["initiative"]),
                "category": str(item["category"]),
                "entity_type": str(item["entityType"]),
                "theme": str(item["theme"]),
                "location_scope": str(item["locationScope"]),
                "location_label": str(item["locationLabel"]),
                "location_tags": "|".join(str(tag) for tag in item["locationTags"]),
                "timeline_label": str(timeline["label"]),
                "timeline_start_year": "" if timeline["startYear"] is None else str(timeline["startYear"]),
                "timeline_end_year": "" if timeline["endYear"] is None else str(timeline["endYear"]),
                "timeline_ongoing": str(bool(timeline["isOngoing"])).lower(),
                "core_focus": str(item["coreFocus"]),
                "focus_tags": "|".join(str(tag) for tag in item["focusTags"]),
                "key_figures": "|".join(str(tag) for tag in item["keyFigures"]),
                "policies": "|".join(str(tag) for tag in item["policies"]),
                "outcomes": "|".join(str(tag) for tag in item["outcomes"]),
                "research_status": str(evidence["researchStatus"]),
                "evidence_score": str(evidence["evidenceScore"]),
                "consensus_direction": str(evidence["consensusDirection"]),
                "confidence_label": str(evidence["confidenceLabel"]),
                "technology_position": str(continuums["technologyPosition"]),
                "technology_comparison": str(continuums["technologyComparison"]),
                "testing_intensity": str(continuums["testingIntensity"]),
                "work_based_learning_intensity": str(continuums["workBasedLearningIntensity"]),
                "outdoor_learning_intensity": str(continuums["outdoorLearningIntensity"]),
                "source_url": str(item["source"]),
                "source_host": str(item["sourceHost"]),
            }
        )
    return flat_rows


def build_state_flat_rows(dataset: dict[str, object]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    state_map = dataset.get("stateMap", {})
    for item in state_map.get("states", []):
        rows.append(
            {
                "state_code": str(item["code"]),
                "state_name": str(item["name"]),
                "inset_group": str(item["insetGroup"]),
                "tile_col": str(item["tileCol"]),
                "tile_row": str(item["tileRow"]),
                "direct_anchor_count": str(item["directAnchorCount"]),
                "national_context_count": str(item["nationalContextCount"]),
                "combined_count": str(item["combinedCount"]),
                "testing_anchor_count": str(item["testingAnchorCount"]),
                "work_based_anchor_count": str(item["workBasedAnchorCount"]),
                "outdoor_anchor_count": str(item["outdoorAnchorCount"]),
                "reduced_technology_anchor_count": str(item["reducedTechnologyAnchorCount"]),
                "high_technology_anchor_count": str(item["highTechnologyAnchorCount"]),
                "continuum_balance_score": str(item["continuumBalanceScore"]),
                "strongest_evidence_score": str(item["strongestEvidenceScore"]),
                "anchor_initiative_ids": "|".join(str(value) for value in item["anchorInitiativeIds"]),
                "national_initiative_ids": "|".join(str(value) for value in item["nationalInitiativeIds"]),
            }
        )
    return rows


def write_json(path: Path, payload: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fieldnames = list(rows[0].keys())
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
