from __future__ import annotations

import csv
import json
import sys
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

SOURCE_CSV_PATH = ROOT / "Education Initiatives" / "initiative_sources.csv"
OUTPUT_DIR = ROOT / "outputs" / "us_education_initiatives" / "sources"
MANIFEST_PATH = OUTPUT_DIR / "source_manifest.json"
QUEUE_CSV_PATH = OUTPUT_DIR / "download_queue.csv"


def load_rows() -> list[dict[str, str]]:
    with SOURCE_CSV_PATH.open(encoding="utf-8", newline="") as handle:
        return [{key: (value or "").strip() for key, value in row.items()} for row in csv.DictReader(handle)]


def build_manifest(rows: list[dict[str, str]]) -> dict[str, object]:
    by_repo = Counter(row["repository"] for row in rows if row.get("repository"))
    by_status = Counter(row["status"] for row in rows if row.get("status"))
    return {
        "sourceCsv": str(SOURCE_CSV_PATH.relative_to(ROOT)),
        "generatedFiles": {
            "manifest": str(MANIFEST_PATH.relative_to(ROOT)),
            "queueCsv": str(QUEUE_CSV_PATH.relative_to(ROOT)),
        },
        "counts": {
            "rows": len(rows),
            "repositories": dict(sorted(by_repo.items())),
            "statuses": dict(sorted(by_status.items())),
        },
        "sources": [
            {
                "sourceId": row["source_id"],
                "initiativeId": row["initiative_id"],
                "role": row["source_role"],
                "repository": row["repository"],
                "url": row["url"],
                "retrievalMode": row["retrieval_mode"],
                "targetRelpath": row["target_relpath"],
                "status": row["status"],
            }
            for row in rows
        ],
    }


def write_outputs(rows: list[dict[str, str]], manifest: dict[str, object]) -> None:
    MANIFEST_PATH.parent.mkdir(parents=True, exist_ok=True)
    MANIFEST_PATH.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

    queue_rows = []
    for row in rows:
        queue_rows.append(
            {
                "source_id": row["source_id"],
                "initiative_id": row["initiative_id"],
                "repository": row["repository"],
                "url": row["url"],
                "retrieval_mode": row["retrieval_mode"],
                "target_path": str((OUTPUT_DIR / row["target_relpath"]).resolve()),
                "status": row["status"],
                "priority": row["extraction_priority"],
            }
        )

    fieldnames = list(queue_rows[0].keys()) if queue_rows else []
    with QUEUE_CSV_PATH.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(queue_rows)


def main() -> None:
    rows = load_rows()
    manifest = build_manifest(rows)
    write_outputs(rows, manifest)
    print(f"Wrote {MANIFEST_PATH}")
    print(f"Wrote {QUEUE_CSV_PATH}")


if __name__ == "__main__":
    main()
