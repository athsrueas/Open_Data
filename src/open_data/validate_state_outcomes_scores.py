from __future__ import annotations

import csv
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCORES_PATH = ROOT / "outputs" / "us_education_initiatives" / "state_outcomes" / "state_year_scores_raw.csv"


REQUIRED_FOR_NUMERIC = [
    "record_id",
    "state_code",
    "state_name",
    "year",
    "indicator_id",
    "value_numeric",
    "unit_label",
    "source_system",
    "source_dataset",
    "source_release_id",
    "source_url",
    "source_row_id",
    "quality_flag",
    "comparability_flag",
]


def main() -> None:
    rows = list(csv.DictReader(SCORES_PATH.open(encoding="utf-8", newline="")))
    failures: list[str] = []
    for idx, row in enumerate(rows, start=2):
        has_numeric = (row.get("value_numeric", "") or "").strip() != ""
        if not has_numeric:
            continue
        for field in REQUIRED_FOR_NUMERIC:
            if not (row.get(field, "") or "").strip():
                failures.append(f"line {idx}: missing required field `{field}`")

    sat_act_ids = {"sat_total_mean_score", "sat_participation_rate", "act_composite_mean_score", "act_participation_rate"}
    for idx, row in enumerate(rows, start=2):
        if row.get("indicator_id") not in sat_act_ids:
            continue
        if (row.get("value_numeric", "") or "").strip() and row.get("comparability_flag") not in {"fully_comparable", "partially_comparable", "source_specific"}:
            failures.append(f"line {idx}: SAT/ACT comparability_flag must be controlled value")

    if failures:
        print("Validation failed:")
        for failure in failures[:50]:
            print(f"- {failure}")
        print(f"Total failures: {len(failures)}")
        raise SystemExit(1)

    print(f"Validation passed for {len(rows)} rows in {SCORES_PATH}")


if __name__ == "__main__":
    main()
