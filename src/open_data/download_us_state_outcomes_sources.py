from __future__ import annotations

import argparse
import csv
import json
import re
import time
from html import unescape
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parents[2]
REGISTRY_PATH = ROOT / "outputs" / "us_education_initiatives" / "state_outcomes" / "source_registry.csv"
OUTPUT_ROOT = ROOT / "outputs" / "us_education_initiatives" / "state_outcomes"
RUNS_DIR = OUTPUT_ROOT / "runs"

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
)


def load_rows() -> list[dict[str, str]]:
    with REGISTRY_PATH.open(encoding="utf-8", newline="") as handle:
        return [{k: (v or "").strip() for k, v in row.items()} for row in csv.DictReader(handle)]


def save_rows(rows: list[dict[str, str]]) -> None:
    if not rows:
        return
    with REGISTRY_PATH.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def fetch(url: str) -> tuple[bytes, str]:
    request = Request(url, headers={"User-Agent": USER_AGENT})
    with urlopen(request, timeout=60) as response:
        body = response.read()
        content_type = response.headers.get("Content-Type", "")
    return body, content_type


def write_bytes(path: Path, payload: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(payload)


def write_text(path: Path, payload: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(payload, encoding="utf-8")


def looks_like_pdf(url: str, content_type: str, body: bytes) -> bool:
    return url.lower().endswith(".pdf") or "application/pdf" in content_type.lower() or body.startswith(b"%PDF")


def extract_pdf_candidate(html: str, base_url: str) -> str | None:
    patterns = [
        r'<meta[^>]+name="citation_pdf_url"[^>]+content="([^"]+)"',
        r'"pdfUrl":"([^"]+)"',
        r'"downloadPdfUrl":"([^"]+)"',
        r'href="([^"]+\.pdf(?:\?[^"]*)?)"',
        r"href='([^']+\.pdf(?:\?[^']*)?)'",
    ]
    for pattern in patterns:
        match = re.search(pattern, html, flags=re.IGNORECASE)
        if match:
            return urljoin(base_url, unescape(match.group(1).replace("\\u002F", "/").replace("\\/", "/")))
    return None


def process_row(row: dict[str, str]) -> dict[str, Any]:
    url = row.get("source_url", "")
    mode = row.get("retrieval_mode", "")
    target_relpath = row.get("target_relpath", "")
    output_path = OUTPUT_ROOT / target_relpath

    if not url:
        return {"source_id": row.get("source_id", ""), "run_status": "failed", "detail": "missing source_url"}

    try:
        body, content_type = fetch(url)
        if mode == "direct_pdf":
            if looks_like_pdf(url, content_type, body):
                write_bytes(output_path, body)
                return {"source_id": row.get("source_id", ""), "run_status": "downloaded", "saved_paths": [str(output_path.relative_to(ROOT))], "detail": "pdf downloaded"}
            html = body.decode("utf-8", errors="ignore")
            landing_path = output_path.with_suffix(".html")
            write_text(landing_path, html)
            candidate = extract_pdf_candidate(html, url)
            if candidate:
                try:
                    pdf_body, pdf_type = fetch(candidate)
                    if looks_like_pdf(candidate, pdf_type, pdf_body):
                        write_bytes(output_path, pdf_body)
                        return {"source_id": row.get("source_id", ""), "run_status": "downloaded", "saved_paths": [str(output_path.relative_to(ROOT)), str(landing_path.relative_to(ROOT))], "detail": f"landing parsed; pdf downloaded from {candidate}"}
                except Exception as error:  # noqa: BLE001
                    return {"source_id": row.get("source_id", ""), "run_status": "landing_only", "saved_paths": [str(landing_path.relative_to(ROOT))], "detail": f"pdf candidate failed: {error}"}
            return {"source_id": row.get("source_id", ""), "run_status": "landing_only", "saved_paths": [str(landing_path.relative_to(ROOT))], "detail": "expected pdf but got non-pdf response"}

        html_text = body.decode("utf-8", errors="ignore")
        write_text(output_path, html_text)
        return {"source_id": row.get("source_id", ""), "run_status": "downloaded", "saved_paths": [str(output_path.relative_to(ROOT))], "detail": "html captured"}
    except (HTTPError, URLError, TimeoutError) as error:
        return {"source_id": row.get("source_id", ""), "run_status": "failed", "detail": str(error)}
    except Exception as error:  # noqa: BLE001
        return {"source_id": row.get("source_id", ""), "run_status": "failed", "detail": f"{type(error).__name__}: {error}"}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--priority", default="all", help="high, medium, or all")
    parser.add_argument("--only-queued", action="store_true", help="Process only rows with status=queued")
    args = parser.parse_args()

    rows = load_rows()
    selected: list[dict[str, str]] = []
    for row in rows:
        if args.only_queued and row.get("status") != "queued":
            continue
        if args.priority != "all" and row.get("priority") != args.priority:
            continue
        selected.append(row)

    results: list[dict[str, Any]] = []
    by_source_id: dict[str, dict[str, Any]] = {}
    for row in selected:
        result = process_row(row)
        results.append(result)
        by_source_id[result["source_id"]] = result
        time.sleep(0.25)

    for row in rows:
        source_id = row.get("source_id", "")
        result = by_source_id.get(source_id)
        if not result:
            continue
        if result["run_status"] == "downloaded":
            row["status"] = "downloaded"
        elif result["run_status"] == "landing_only":
            row["status"] = "landing_only"
        elif result["run_status"] == "failed":
            row["status"] = "failed"

    save_rows(rows)

    RUNS_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    run_path = RUNS_DIR / f"state_outcomes_download_run_{timestamp}.json"
    latest_path = RUNS_DIR / "state_outcomes_latest.json"
    payload = {"priority": args.priority, "count": len(results), "results": results}
    run_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    latest_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

    counts: dict[str, int] = {}
    for item in results:
        key = str(item["run_status"])
        counts[key] = counts.get(key, 0) + 1
    print(f"Processed {len(results)} rows")
    print(json.dumps(counts, indent=2))
    print(f"Wrote {run_path}")


if __name__ == "__main__":
    main()
