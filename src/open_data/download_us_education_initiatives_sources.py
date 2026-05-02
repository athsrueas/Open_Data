from __future__ import annotations

import argparse
import csv
import json
import re
import sys
import time
from html import unescape
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

SOURCE_CSV_PATH = ROOT / "Education Initiatives" / "initiative_sources.csv"
OUTPUT_ROOT = ROOT / "outputs" / "us_education_initiatives" / "sources"
RUNS_DIR = OUTPUT_ROOT / "runs"

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
)


def load_rows() -> list[dict[str, str]]:
    with SOURCE_CSV_PATH.open(encoding="utf-8", newline="") as handle:
        return [{key: (value or "").strip() for key, value in row.items()} for row in csv.DictReader(handle)]


def fetch(url: str) -> tuple[bytes, str]:
    request = Request(url, headers={"User-Agent": USER_AGENT})
    with urlopen(request, timeout=45) as response:
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
    return (
        url.lower().endswith(".pdf")
        or "application/pdf" in content_type.lower()
        or body.startswith(b"%PDF")
    )


def extract_pdf_candidate(html: str, base_url: str) -> str | None:
    patterns = [
        r'<meta[^>]+name="citation_pdf_url"[^>]+content="([^"]+)"',
        r'<meta[^>]+content="([^"]+)"[^>]+name="citation_pdf_url"',
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


def result_row(row: dict[str, str], **updates: Any) -> dict[str, Any]:
    payload: dict[str, Any] = dict(row)
    payload.update(updates)
    return payload


def process_row(row: dict[str, str]) -> dict[str, Any]:
    source_id = row["source_id"]
    url = row["url"]
    mode = row["retrieval_mode"]
    target = Path(row["target_relpath"])
    output_path = OUTPUT_ROOT / target

    if row["status"] != "queued":
        return result_row(row, run_status="skipped", detail="row not queued")

    if not url:
        return result_row(row, run_status="skipped", detail="missing url")

    try:
        if mode == "direct_pdf":
            body, content_type = fetch(url)
            if not looks_like_pdf(url, content_type, body):
                html = body.decode("utf-8", errors="ignore")
                alt_path = output_path.with_suffix(".html")
                write_text(alt_path, html)
                candidate = extract_pdf_candidate(html, url)
                saved = [str(alt_path.relative_to(ROOT))]
                if candidate:
                    try:
                        pdf_body, pdf_type = fetch(candidate)
                        if looks_like_pdf(candidate, pdf_type, pdf_body):
                            write_bytes(output_path, pdf_body)
                            saved.insert(0, str(output_path.relative_to(ROOT)))
                            return result_row(
                                row,
                                run_status="downloaded",
                                saved_paths=saved,
                                detail=f"landing page parsed; pdf downloaded from {candidate}",
                            )
                    except (HTTPError, URLError, TimeoutError) as pdf_error:
                        return result_row(
                            row,
                            run_status="landing_only",
                            saved_paths=saved,
                            detail=f"pdf candidate failed: {candidate} ({pdf_error})",
                        )
                return result_row(
                    row,
                    run_status="landing_only",
                    saved_paths=saved,
                    detail=f"expected pdf but received {content_type or 'unknown content type'}",
                )
            write_bytes(output_path, body)
            return result_row(
                row,
                run_status="downloaded",
                saved_paths=[str(output_path.relative_to(ROOT))],
                detail="pdf downloaded",
            )

        if mode == "manual_html_capture":
            body, _content_type = fetch(url)
            text = body.decode("utf-8", errors="ignore")
            write_text(output_path, text)
            return result_row(
                row,
                run_status="downloaded",
                saved_paths=[str(output_path.relative_to(ROOT))],
                detail="html captured",
            )

        if mode in {"landing_page_plus_pdf", "eric_record_plus_pdf_search"}:
            body, content_type = fetch(url)
            if looks_like_pdf(url, content_type, body):
                write_bytes(output_path, body)
                return result_row(
                    row,
                    run_status="downloaded",
                    saved_paths=[str(output_path.relative_to(ROOT))],
                    detail="pdf downloaded directly",
                )

            html = body.decode("utf-8", errors="ignore")
            landing_path = output_path.with_suffix(".landing.html")
            write_text(landing_path, html)
            candidate = extract_pdf_candidate(html, url)
            saved = [str(landing_path.relative_to(ROOT))]
            if candidate:
                try:
                    pdf_body, pdf_type = fetch(candidate)
                    if looks_like_pdf(candidate, pdf_type, pdf_body):
                        write_bytes(output_path, pdf_body)
                        saved.insert(0, str(output_path.relative_to(ROOT)))
                        return result_row(
                            row,
                            run_status="downloaded",
                            saved_paths=saved,
                            detail=f"landing page parsed; pdf downloaded from {candidate}",
                        )
                except (HTTPError, URLError, TimeoutError) as pdf_error:
                    return result_row(
                        row,
                        run_status="landing_only",
                        saved_paths=saved,
                        detail=f"pdf candidate failed: {candidate} ({pdf_error})",
                    )

            return result_row(
                row,
                run_status="landing_only",
                saved_paths=saved,
                detail="landing page saved; no pdf candidate resolved",
            )

        return result_row(row, run_status="skipped", detail=f"unsupported retrieval mode: {mode}")

    except (HTTPError, URLError, TimeoutError) as error:
        return result_row(row, run_status="failed", detail=str(error))
    except Exception as error:  # noqa: BLE001
        return result_row(row, run_status="failed", detail=f"{type(error).__name__}: {error}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--priority", default="high", help="Priority level to pull: high, medium, or all")
    parser.add_argument("--limit", type=int, default=0, help="Optional maximum number of rows to process")
    args = parser.parse_args()

    rows = load_rows()
    selected = []
    for row in rows:
        if row["status"] != "queued":
            continue
        if args.priority != "all" and row["extraction_priority"] != args.priority:
            continue
        selected.append(row)

    if args.limit > 0:
        selected = selected[: args.limit]

    results = []
    for row in selected:
        results.append(process_row(row))
        time.sleep(0.35)

    RUNS_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    run_path = RUNS_DIR / f"download_run_{timestamp}.json"
    latest_path = RUNS_DIR / "latest.json"
    payload = {
        "priority": args.priority,
        "count": len(results),
        "results": results,
    }
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
