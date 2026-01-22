"""CLI entry point for validating minimal dataset metadata."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from open_data.metadata import ValidationError, load_dataset, summarize_dataset, validate_many


def _load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate dataset metadata against the minimal Open Data schema."
    )
    parser.add_argument("path", type=Path, help="Path to a dataset JSON file")
    parser.add_argument(
        "--summary",
        action="store_true",
        help="Print a human-readable summary when validation passes.",
    )
    args = parser.parse_args()

    payload = _load_json(args.path)
    if isinstance(payload, list):
        errors = validate_many(payload)
    else:
        try:
            dataset = load_dataset(payload)
        except ValidationError as exc:
            errors = str(exc).split("\n")
        else:
            errors = []
            if args.summary:
                print(summarize_dataset(dataset))

    if errors:
        for message in errors:
            print(message)
        return 1

    print("Metadata validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
