"""Download raw education source payloads into a landing-zone directory.

This script stages source data exactly as received so downstream transforms
can be revised later without re-querying the source.
"""

from __future__ import annotations

import datetime as dt
import json
from pathlib import Path
from typing import Any
from urllib.parse import urlencode, urljoin
from urllib.request import urlopen


BASE_API = "https://api.worldbank.org/v2/"
RAW_ROOT = Path("outputs") / "educational_inequality_map" / "raw" / "worldbank"

INDICATOR_CODES = [
    "SE.XPD.TOTL.GD.ZS",
    "SE.XPD.TOTL.GB.ZS",
    "SE.ADT.LITR.ZS",
    "SE.PRM.CMPT.ZS",
    "SP.POP.TOTL",
    "NY.GDP.PCAP.KD",
]


def fetch_json(path: str, params: dict[str, Any]) -> Any:
    query = urlencode(params)
    url = urljoin(BASE_API, path)
    with urlopen(f"{url}?{query}", timeout=60) as response:
        return json.loads(response.read().decode("utf-8"))


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def download_paginated(path: str, params: dict[str, Any], output_dir: Path) -> dict[str, Any]:
    first_payload = fetch_json(path, {**params, "page": 1})
    meta = first_payload[0]
    pages = int(meta["pages"])
    total = int(meta["total"])

    write_json(output_dir / "page-001.json", first_payload)

    for page in range(2, pages + 1):
        payload = fetch_json(path, {**params, "page": page})
        write_json(output_dir / f"page-{page:03d}.json", payload)

    return {
        "path": path,
        "pages": pages,
        "total_rows_reported": total,
        "output_dir": str(output_dir).replace("\\", "/"),
    }


def run() -> None:
    snapshot = dt.date.today().isoformat()
    run_dir = RAW_ROOT / snapshot

    manifest: dict[str, Any] = {
        "generated_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "snapshot_date": snapshot,
        "source_system": "WorldBank_EdStats",
        "mode": "raw_landing_zone",
        "status": "provisional_pending_armando_review",
        "downloads": [],
    }

    countries_info = download_paginated(
        "country",
        {"format": "json", "per_page": 400},
        run_dir / "country",
    )
    manifest["downloads"].append(
        {
            "name": "country_metadata",
            **countries_info,
        }
    )

    for code in INDICATOR_CODES:
        info = download_paginated(
            f"country/all/indicator/{code}",
            {"format": "json", "per_page": 20000},
            run_dir / "indicator" / code,
        )
        manifest["downloads"].append(
            {
                "name": f"indicator_{code}",
                "indicator_code": code,
                **info,
            }
        )

    write_json(run_dir / "manifest.json", manifest)
    print(f"Wrote raw World Bank payloads to {run_dir}")


if __name__ == "__main__":
    run()
