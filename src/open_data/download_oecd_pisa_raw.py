"""Download OECD PISA 2022 raw files from the direct webfs index.

Supports smaller profile-based fetches for Phase 1 staging and uses streamed,
resumable downloads so large files do not need to be held fully in memory.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any
from urllib.request import Request, urlopen


RAW_DIR = Path("outputs") / "educational_inequality_map" / "raw" / dt.date.today().isoformat() / "oecd_pisa"
USER_AGENT = "Mozilla/5.0"
DEFAULT_TIMEOUT_SECONDS = 120
DEFAULT_CHUNK_SIZE = 8 * 1024 * 1024
DEFAULT_WORKERS = 3
MAX_RETRIES = 3


RESOURCES = [
    {
        "name": "index_html",
        "url": "https://webfs.oecd.org/pisa2022/index.html",
        "relative_path": "index.html",
        "group": "docs",
    },
    {
        "name": "school_questionnaire_sas",
        "url": "https://webfs.oecd.org/pisa2022/SCH_QQQ_SAS.zip",
        "relative_path": "downloads/SCH_QQQ_SAS.zip",
        "group": "sas",
    },
    {
        "name": "student_questionnaire_sas",
        "url": "https://webfs.oecd.org/pisa2022/STU_QQQ_SAS.zip",
        "relative_path": "downloads/STU_QQQ_SAS.zip",
        "group": "sas",
    },
    {
        "name": "teacher_questionnaire_sas",
        "url": "https://webfs.oecd.org/pisa2022/TCH_QQQ_SAS.zip",
        "relative_path": "downloads/TCH_QQQ_SAS.zip",
        "group": "sas",
    },
    {
        "name": "student_cognitive_sas",
        "url": "https://webfs.oecd.org/pisa2022/STU_COG_SAS.zip",
        "relative_path": "downloads/STU_COG_SAS.zip",
        "group": "sas",
    },
    {
        "name": "student_timing_sas",
        "url": "https://webfs.oecd.org/pisa2022/STU_TIM_SAS.zip",
        "relative_path": "downloads/STU_TIM_SAS.zip",
        "group": "sas",
    },
    {
        "name": "creative_thinking_sas",
        "url": "https://webfs.oecd.org/pisa2022/CRT_SAS.zip",
        "relative_path": "downloads/CRT_SAS.zip",
        "group": "sas",
    },
    {
        "name": "financial_literacy_sas",
        "url": "https://webfs.oecd.org/pisa2022/FLT_SAS.zip",
        "relative_path": "downloads/FLT_SAS.zip",
        "group": "sas",
    },
    {
        "name": "school_questionnaire_spss",
        "url": "https://webfs.oecd.org/pisa2022/SCH_QQQ_SPSS.zip",
        "relative_path": "downloads/SCH_QQQ_SPSS.zip",
        "group": "spss",
    },
    {
        "name": "student_questionnaire_spss",
        "url": "https://webfs.oecd.org/pisa2022/STU_QQQ_SPSS.zip",
        "relative_path": "downloads/STU_QQQ_SPSS.zip",
        "group": "spss",
    },
    {
        "name": "teacher_questionnaire_spss",
        "url": "https://webfs.oecd.org/pisa2022/TCH_QQQ_SPSS.zip",
        "relative_path": "downloads/TCH_QQQ_SPSS.zip",
        "group": "spss",
    },
    {
        "name": "student_cognitive_spss",
        "url": "https://webfs.oecd.org/pisa2022/STU_COG_SPSS.zip",
        "relative_path": "downloads/STU_COG_SPSS.zip",
        "group": "spss",
    },
    {
        "name": "student_timing_spss",
        "url": "https://webfs.oecd.org/pisa2022/STU_TIM_SPSS.zip",
        "relative_path": "downloads/STU_TIM_SPSS.zip",
        "group": "spss",
    },
    {
        "name": "creative_thinking_spss",
        "url": "https://webfs.oecd.org/pisa2022/CRT_SPSS.zip",
        "relative_path": "downloads/CRT_SPSS.zip",
        "group": "spss",
    },
    {
        "name": "financial_literacy_spss",
        "url": "https://webfs.oecd.org/pisa2022/FLT_SPSS.zip",
        "relative_path": "downloads/FLT_SPSS.zip",
        "group": "spss",
    },
    {
        "name": "codebook_xlsx",
        "url": "https://webfs.oecd.org/pisa2022/CY08MSP_CODEBOOK_27thJune24.xlsx",
        "relative_path": "downloads/CY08MSP_CODEBOOK_27thJune24.xlsx",
        "group": "docs",
    },
    {
        "name": "questionnaire_compendia",
        "url": "https://webfs.oecd.org/pisa2022/PISA2022_FinalRelease_Compendia_18thJune24.zip",
        "relative_path": "downloads/PISA2022_FinalRelease_Compendia_18thJune24.zip",
        "group": "docs",
    },
    {
        "name": "cognitive_compendia",
        "url": "https://webfs.oecd.org/pisa2022/PISA2022_FinalRelease_Compendia_18thJune24_cog.zip",
        "relative_path": "downloads/PISA2022_FinalRelease_Compendia_18thJune24_cog.zip",
        "group": "docs",
    },
    {
        "name": "creative_thinking_compendia",
        "url": "https://webfs.oecd.org/pisa2022/PISA2022_FinalRelease_CrT_Compendia_18thJune24.zip",
        "relative_path": "downloads/PISA2022_FinalRelease_CrT_Compendia_18thJune24.zip",
        "group": "docs",
    },
    {
        "name": "financial_literacy_compendia",
        "url": "https://webfs.oecd.org/pisa2022/PISA2022_FinalRelease_FLT_Compendia_27thJune24.zip",
        "relative_path": "downloads/PISA2022_FinalRelease_FLT_Compendia_27thJune24.zip",
        "group": "docs",
    },
    {
        "name": "public_codes_zip",
        "url": "https://webfs.oecd.org/pisa2022/PISA2022_Stata_PublicCodes.zip",
        "relative_path": "downloads/PISA2022_Stata_PublicCodes.zip",
        "group": "docs",
    },
    {
        "name": "escs_trend_zip",
        "url": "https://webfs.oecd.org/pisa2022/escs_trend.zip",
        "relative_path": "downloads/escs_trend.zip",
        "group": "docs",
    },
]


PROFILE_GROUPS = {
    "phase1": {"docs", "sas"},
    "phase1-spss": {"docs", "spss"},
    "docs-only": {"docs"},
    "full": {"docs", "sas", "spss"},
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--profile",
        choices=sorted(PROFILE_GROUPS),
        default="phase1",
        help="Which set of OECD PISA assets to download.",
    )
    parser.add_argument(
        "--workers",
        type=int,
        default=DEFAULT_WORKERS,
        help="Concurrent download workers for missing files.",
    )
    parser.add_argument(
        "--chunk-size-mb",
        type=int,
        default=DEFAULT_CHUNK_SIZE // (1024 * 1024),
        help="Chunk size in MiB for streamed downloads.",
    )
    parser.add_argument(
        "--timeout-seconds",
        type=int,
        default=DEFAULT_TIMEOUT_SECONDS,
        help="Socket timeout in seconds per request/read.",
    )
    return parser.parse_args()


def build_manifest(resources: list[dict[str, Any]], profile: str) -> dict[str, Any]:
    return {
        "generated_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "source": "OECD PISA 2022 direct webfs index",
        "status": "provisional_pending_armando_review",
        "profile": profile,
        "resources": resources,
    }


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def persist_manifest(resources: list[dict[str, Any]], profile: str) -> None:
    write_json(RAW_DIR / "manifest.json", build_manifest(resources, profile))


def resolve_content_length(response: Any) -> int | None:
    raw_value = response.headers.get("Content-Length")
    if raw_value is None:
        return None
    if isinstance(raw_value, list):
        raw_value = raw_value[0]
    try:
        return int(raw_value)
    except (TypeError, ValueError):
        return None


def fetch_to_path(
    resource: dict[str, str],
    chunk_size: int,
    timeout_seconds: int,
    selected_names: set[str],
    position: int,
) -> dict[str, Any]:
    target = RAW_DIR / resource["relative_path"]
    temp_target = target.with_suffix(f"{target.suffix}.part")

    if target.exists():
        return {
            "name": resource["name"],
            "url": resource["url"],
            "saved_to": str(target).replace("\\", "/"),
            "status": "skipped_existing",
            "bytes": target.stat().st_size,
            "profile_selected": resource["name"] in selected_names,
        }

    attempt = 0
    while attempt < MAX_RETRIES:
        attempt += 1
        existing_bytes = temp_target.stat().st_size if temp_target.exists() else 0
        headers = {"User-Agent": USER_AGENT, "Accept-Language": "en-US,en;q=0.9"}
        if existing_bytes:
            headers["Range"] = f"bytes={existing_bytes}-"

        request = Request(resource["url"], headers=headers)
        try:
            with urlopen(request, timeout=timeout_seconds) as response:
                content_length = resolve_content_length(response)
                supports_resume = response.status == 206
                if existing_bytes and not supports_resume:
                    existing_bytes = 0
                    if temp_target.exists():
                        temp_target.unlink()

                temp_target.parent.mkdir(parents=True, exist_ok=True)
                mode = "ab" if existing_bytes else "wb"
                downloaded_bytes = existing_bytes
                report_interval = max(chunk_size * 8, 64 * 1024 * 1024)
                next_report_at = downloaded_bytes + report_interval
                started_at = time.monotonic()

                with temp_target.open(mode) as handle:
                    while True:
                        chunk = response.read(chunk_size)
                        if not chunk:
                            break
                        handle.write(chunk)
                        downloaded_bytes += len(chunk)

                        if downloaded_bytes >= next_report_at:
                            elapsed = max(time.monotonic() - started_at, 0.1)
                            rate_mib_s = downloaded_bytes / elapsed / (1024 * 1024)
                            total_bytes = (
                                downloaded_bytes + content_length
                                if supports_resume and content_length is not None
                                else content_length
                            )
                            if total_bytes:
                                pct = downloaded_bytes / total_bytes * 100
                                print(
                                    f"  [{position}] {resource['name']}: "
                                    f"{downloaded_bytes / (1024 * 1024):,.1f} MiB "
                                    f"of {total_bytes / (1024 * 1024):,.1f} MiB "
                                    f"({pct:,.1f}%) at {rate_mib_s:,.1f} MiB/s"
                                )
                            else:
                                print(
                                    f"  [{position}] {resource['name']}: "
                                    f"{downloaded_bytes / (1024 * 1024):,.1f} MiB "
                                    f"downloaded at {rate_mib_s:,.1f} MiB/s"
                                )
                            next_report_at += report_interval

                temp_target.replace(target)
                return {
                    "name": resource["name"],
                    "url": resource["url"],
                    "saved_to": str(target).replace("\\", "/"),
                    "status": "downloaded",
                    "bytes": target.stat().st_size,
                    "attempts": attempt,
                    "profile_selected": resource["name"] in selected_names,
                }
        except Exception as exc:
            if attempt >= MAX_RETRIES:
                return {
                    "name": resource["name"],
                    "url": resource["url"],
                    "saved_to": str(target).replace("\\", "/"),
                    "status": "error",
                    "error": str(exc),
                    "attempts": attempt,
                    "partial_bytes": temp_target.stat().st_size if temp_target.exists() else 0,
                    "profile_selected": resource["name"] in selected_names,
                }

            sleep_seconds = attempt * 2
            print(f"  [{position}] {resource['name']}: retrying in {sleep_seconds}s after {exc}")
            time.sleep(sleep_seconds)

    raise RuntimeError(f"Unreachable retry state for {resource['name']}")


def run() -> None:
    args = parse_args()
    selected_resources = [resource for resource in RESOURCES if resource["group"] in PROFILE_GROUPS[args.profile]]
    selected_names = {resource["name"] for resource in selected_resources}

    results: list[dict[str, Any]] = []
    manifest_path = RAW_DIR / "manifest.json"

    if manifest_path.exists():
        try:
            existing_manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            if isinstance(existing_manifest.get("resources"), list):
                results = existing_manifest["resources"]
        except json.JSONDecodeError:
            pass

    existing_by_name = {result.get("name"): result for result in results if isinstance(result, dict)}
    manifest_lock = threading.Lock()

    print(
        f"Downloading OECD PISA profile '{args.profile}' "
        f"with {len(selected_resources)} resources and {args.workers} workers"
    )

    future_map: dict[Any, tuple[int, dict[str, str]]] = {}
    workers = max(1, min(args.workers, len(selected_resources)))
    chunk_size = max(1, args.chunk_size_mb) * 1024 * 1024

    with ThreadPoolExecutor(max_workers=workers) as executor:
        for index, resource in enumerate(selected_resources, start=1):
            target = RAW_DIR / resource["relative_path"]
            print(f"[{index}/{len(selected_resources)}] queue {resource['name']} -> {target}")
            if target.exists():
                result = {
                    "name": resource["name"],
                    "url": resource["url"],
                    "saved_to": str(target).replace("\\", "/"),
                    "status": "skipped_existing",
                    "bytes": target.stat().st_size,
                    "profile_selected": True,
                }
                existing_by_name[resource["name"]] = result
                persist_manifest(
                    [existing_by_name[item["name"]] for item in selected_resources if item["name"] in existing_by_name],
                    args.profile,
                )
                print(f"  skipped existing ({result['bytes']:,} bytes)")
                continue

            future = executor.submit(
                fetch_to_path,
                resource,
                chunk_size,
                args.timeout_seconds,
                selected_names,
                f"{index}/{len(selected_resources)}",
            )
            future_map[future] = (index, resource)

        for future in as_completed(future_map):
            index, resource = future_map[future]
            result = future.result()
            with manifest_lock:
                existing_by_name[resource["name"]] = result
                persist_manifest(
                    [existing_by_name[item["name"]] for item in selected_resources if item["name"] in existing_by_name],
                    args.profile,
                )

            if result["status"] == "downloaded":
                print(f"[{index}/{len(selected_resources)}] completed {resource['name']} ({result['bytes']:,} bytes)")
            elif result["status"] == "error":
                partial = result.get("partial_bytes", 0)
                print(f"[{index}/{len(selected_resources)}] error {resource['name']} after {partial:,} partial bytes: {result['error']}")

    print(f"Wrote OECD PISA raw files to {RAW_DIR}")


if __name__ == "__main__":
    run()
