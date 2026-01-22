"""Tiny helper functions to scaffold discrete public data tasks."""

from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Iterable, Mapping


def load_json(path: Path) -> dict:
    """Load a JSON file into a dictionary."""
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def write_json(path: Path, payload: Mapping) -> None:
    """Write a dictionary to a JSON file with readable formatting."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, sort_keys=True)
        handle.write("\n")


def write_csv(path: Path, rows: Iterable[Mapping[str, str]], fieldnames: list[str]) -> None:
    """Write rows to a CSV file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def normalize_metadata(payload: Mapping) -> dict:
    """Create a minimal, normalized metadata record from a raw payload."""
    return {
        "id": payload.get("id", ""),
        "title": payload.get("title", ""),
        "description": payload.get("description", ""),
        "license": payload.get("license", ""),
        "resources": payload.get("resources", []),
    }


def build_index_rows(payloads: Iterable[Mapping]) -> list[dict[str, str]]:
    """Build quick index rows for a CSV export."""
    rows: list[dict[str, str]] = []
    for payload in payloads:
        rows.append(
            {
                "id": str(payload.get("id", "")),
                "title": str(payload.get("title", "")),
                "license": str(payload.get("license", "")),
                "resource_count": str(len(payload.get("resources", []))),
            }
        )
    return rows


def audit_missing_fields(payloads: Iterable[Mapping], fields: list[str]) -> list[dict[str, str]]:
    """Return a report of missing fields for each payload."""
    report: list[dict[str, str]] = []
    for payload in payloads:
        missing = [field for field in fields if not payload.get(field)]
        report.append(
            {
                "id": str(payload.get("id", "")),
                "missing_fields": ", ".join(missing) if missing else "none",
            }
        )
    return report
