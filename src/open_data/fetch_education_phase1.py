"""Fetch a small Phase 1 education inequality extract into ontology-shaped CSVs.

This script intentionally stays conservative:
- official source only (World Bank API)
- country-year data only
- ontology-shaped exports that remain easy to remap later
"""

from __future__ import annotations

import csv
import datetime as dt
import json
from pathlib import Path
from typing import Any
from urllib.parse import urlencode, urljoin
from urllib.request import urlopen


BASE_API = "https://api.worldbank.org/v2/"
OUTPUT_ROOT = Path("outputs") / "educational_inequality_map" / "phase1_world_bank"


INDICATORS = [
    {
        "metric_id": "government_expenditure_education_pct_gdp",
        "source_indicator_code": "SE.XPD.TOTL.GD.ZS",
        "display_name": "Government expenditure on education, total (% of GDP)",
        "domain": "funding",
        "metric_family": "funding",
        "unit_type": "percentage",
        "unit_label": "% of GDP",
        "directionality": "context_dependent",
        "description": "General government expenditure on education expressed as a percentage of GDP.",
    },
    {
        "metric_id": "government_expenditure_education_pct_total_govt_expenditure",
        "source_indicator_code": "SE.XPD.TOTL.GB.ZS",
        "display_name": "Government expenditure on education, total (% of government expenditure)",
        "domain": "funding",
        "metric_family": "funding",
        "unit_type": "percentage",
        "unit_label": "% of government expenditure",
        "directionality": "context_dependent",
        "description": "General government expenditure on education expressed as a percentage of total government expenditure.",
    },
    {
        "metric_id": "adult_literacy_rate_15_plus",
        "source_indicator_code": "SE.ADT.LITR.ZS",
        "display_name": "Literacy rate, adult total (% of people ages 15 and above)",
        "domain": "outcomes",
        "metric_family": "literacy",
        "unit_type": "percentage",
        "unit_label": "% of population age 15+",
        "directionality": "higher_is_better",
        "description": "Share of adults age 15 and above who can read and write with understanding.",
    },
    {
        "metric_id": "completion_rate_primary",
        "source_indicator_code": "SE.PRM.CMPT.ZS",
        "display_name": "Completion rate, primary, total (% of relevant age group)",
        "domain": "access",
        "metric_family": "completion",
        "unit_type": "percentage",
        "unit_label": "% of relevant age group",
        "directionality": "higher_is_better",
        "description": "Primary completion rate for the relevant age group.",
    },
    {
        "metric_id": "total_population",
        "source_indicator_code": "SP.POP.TOTL",
        "display_name": "Population, total",
        "domain": "context",
        "metric_family": "population_context",
        "unit_type": "count",
        "unit_label": "people",
        "directionality": "neutral",
        "description": "Total midyear population.",
    },
    {
        "metric_id": "gdp_per_capita_constant_usd",
        "source_indicator_code": "NY.GDP.PCAP.KD",
        "display_name": "GDP per capita (constant 2015 US$)",
        "domain": "context",
        "metric_family": "population_context",
        "unit_type": "currency",
        "unit_label": "constant 2015 US$",
        "directionality": "context_dependent",
        "description": "GDP per capita based on constant 2015 U.S. dollars.",
    },
]


def fetch_json(path: str, params: dict[str, Any]) -> Any:
    query = urlencode(params)
    url = urljoin(BASE_API, path)
    with urlopen(f"{url}?{query}", timeout=60) as response:
        return json.loads(response.read().decode("utf-8"))


def fetch_paginated(path: str, params: dict[str, Any]) -> list[dict[str, Any]]:
    page = 1
    rows: list[dict[str, Any]] = []

    while True:
        payload = fetch_json(path, {**params, "page": page})
        meta, page_rows = payload
        rows.extend(page_rows)
        if page >= int(meta["pages"]):
            return rows
        page += 1


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def build_jurisdictions(snapshot_date: str) -> list[dict[str, Any]]:
    rows = fetch_paginated("country", {"format": "json", "per_page": 400})
    jurisdictions: list[dict[str, Any]] = []

    for row in rows:
        if row.get("region", {}).get("value") == "Aggregates":
            continue
        jurisdictions.append(
            {
                "jurisdiction_id": f"jurisdiction/{row['id']}",
                "name": row.get("name", ""),
                "jurisdiction_type": "country",
                "iso2_code": row.get("iso2Code", ""),
                "iso3_code": row.get("id", ""),
                "world_bank_region": row.get("region", {}).get("value", ""),
                "world_bank_income_group": row.get("incomeLevel", {}).get("value", ""),
                "capital_city": row.get("capitalCity", ""),
                "longitude": row.get("longitude", ""),
                "latitude": row.get("latitude", ""),
                "status": "active",
                "source_system": "WorldBank_EdStats",
                "source_snapshot_date": snapshot_date,
            }
        )

    return sorted(jurisdictions, key=lambda item: item["iso3_code"])


def build_metrics() -> list[dict[str, Any]]:
    metrics: list[dict[str, Any]] = []
    for indicator in INDICATORS:
        metrics.append(
            {
                "metric_id": indicator["metric_id"],
                "display_name": indicator["display_name"],
                "description": indicator["description"],
                "metric_family": indicator["metric_family"],
                "domain": indicator["domain"],
                "unit_type": indicator["unit_type"],
                "unit_label": indicator["unit_label"],
                "directionality": indicator["directionality"],
                "aggregation_level": "country_year",
                "is_core_phase1": "true",
                "source_metric_code": indicator["source_indicator_code"],
            }
        )
    return metrics


def build_datasets() -> list[dict[str, Any]]:
    return [
        {
            "dataset_id": "dataset/worldbank/edstats_phase1_api",
            "name": "World Bank Education / Development Indicators API (Phase 1 extract)",
            "publisher": "World Bank",
            "source_system": "WorldBank_EdStats",
            "description": "Country-year indicators pulled from the World Bank API for the Educational Inequality Map Phase 1 extract.",
            "homepage_url": "https://data.worldbank.org/topic/education",
            "api_url": "https://api.worldbank.org/v2/",
            "license_name": "World Bank Open Data Terms",
            "coverage_scope": "global",
            "update_cadence": "periodic",
            "data_format": "json",
            "access_constraints": "open",
        }
    ]


def build_dataset_releases(snapshot_date: str) -> list[dict[str, Any]]:
    return [
        {
            "dataset_release_id": f"release/worldbank/edstats_phase1/{snapshot_date}",
            "dataset_id": "dataset/worldbank/edstats_phase1_api",
            "version_label": f"worldbank_api_snapshot_{snapshot_date}",
            "snapshot_date": snapshot_date,
            "download_url": "https://api.worldbank.org/v2/",
            "notes": "Generated by src/open_data/fetch_education_phase1.py",
        }
    ]


def build_indicator_definitions() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for indicator in INDICATORS:
        rows.append(
            {
                "indicator_definition_id": f"indicator_definition/worldbank/{indicator['source_indicator_code']}",
                "metric_id": indicator["metric_id"],
                "dataset_id": "dataset/worldbank/edstats_phase1_api",
                "source_indicator_code": indicator["source_indicator_code"],
                "source_indicator_name": indicator["display_name"],
                "definition_text": indicator["description"],
                "official_unit": indicator["unit_label"],
                "valid_from_year": "",
                "valid_to_year": "",
            }
        )
    return rows


def build_observations(snapshot_date: str, valid_country_codes: set[str]) -> list[dict[str, Any]]:
    release_id = f"release/worldbank/edstats_phase1/{snapshot_date}"
    observations: list[dict[str, Any]] = []

    for indicator in INDICATORS:
        rows = fetch_paginated(
            f"country/all/indicator/{indicator['source_indicator_code']}",
            {"format": "json", "per_page": 20000},
        )
        for row in rows:
            country = row.get("country", {})
            country_iso3 = row.get("countryiso3code", "")
            if not country_iso3 or country_iso3 not in valid_country_codes:
                continue
            if row.get("value") is None:
                continue
            observations.append(
                {
                    "observation_id": f"observation/{country_iso3}/{indicator['metric_id']}/{row['date']}/all",
                    "subject_type": "Jurisdiction",
                    "subject_id": f"jurisdiction/{country_iso3}",
                    "metric_id": indicator["metric_id"],
                    "value_numeric": row["value"],
                    "value_text": "",
                    "unit_label": indicator["unit_label"],
                    "year": row["date"],
                    "time_granularity": "annual",
                    "quality_flag": "unknown",
                    "comparability_flag": "partially_comparable",
                    "population_group_id": "",
                    "dataset_release_id": release_id,
                    "source_indicator_code": indicator["source_indicator_code"],
                    "source_country_code": country_iso3,
                    "source_country_name": country.get("value", ""),
                }
            )

    observations.sort(key=lambda item: (item["metric_id"], item["subject_id"], item["year"]))
    return observations


def write_manifest(snapshot_date: str, row_counts: dict[str, int]) -> None:
    payload = {
        "generated_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "snapshot_date": snapshot_date,
        "source": "World Bank API",
        "ontology_status": "provisional_pending_armando_review",
        "outputs": row_counts,
    }
    path = OUTPUT_ROOT / "manifest.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def run() -> None:
    snapshot_date = dt.date.today().isoformat()

    jurisdictions = build_jurisdictions(snapshot_date)
    valid_country_codes = {row["iso3_code"] for row in jurisdictions}
    metrics = build_metrics()
    datasets = build_datasets()
    dataset_releases = build_dataset_releases(snapshot_date)
    indicator_definitions = build_indicator_definitions()
    observations = build_observations(snapshot_date, valid_country_codes)

    write_csv(
        OUTPUT_ROOT / "jurisdictions.csv",
        jurisdictions,
        [
            "jurisdiction_id",
            "name",
            "jurisdiction_type",
            "iso2_code",
            "iso3_code",
            "world_bank_region",
            "world_bank_income_group",
            "capital_city",
            "longitude",
            "latitude",
            "status",
            "source_system",
            "source_snapshot_date",
        ],
    )
    write_csv(
        OUTPUT_ROOT / "metrics.csv",
        metrics,
        [
            "metric_id",
            "display_name",
            "description",
            "metric_family",
            "domain",
            "unit_type",
            "unit_label",
            "directionality",
            "aggregation_level",
            "is_core_phase1",
            "source_metric_code",
        ],
    )
    write_csv(
        OUTPUT_ROOT / "datasets.csv",
        datasets,
        [
            "dataset_id",
            "name",
            "publisher",
            "source_system",
            "description",
            "homepage_url",
            "api_url",
            "license_name",
            "coverage_scope",
            "update_cadence",
            "data_format",
            "access_constraints",
        ],
    )
    write_csv(
        OUTPUT_ROOT / "dataset_releases.csv",
        dataset_releases,
        [
            "dataset_release_id",
            "dataset_id",
            "version_label",
            "snapshot_date",
            "download_url",
            "notes",
        ],
    )
    write_csv(
        OUTPUT_ROOT / "indicator_definitions.csv",
        indicator_definitions,
        [
            "indicator_definition_id",
            "metric_id",
            "dataset_id",
            "source_indicator_code",
            "source_indicator_name",
            "definition_text",
            "official_unit",
            "valid_from_year",
            "valid_to_year",
        ],
    )
    write_csv(
        OUTPUT_ROOT / "observations.csv",
        observations,
        [
            "observation_id",
            "subject_type",
            "subject_id",
            "metric_id",
            "value_numeric",
            "value_text",
            "unit_label",
            "year",
            "time_granularity",
            "quality_flag",
            "comparability_flag",
            "population_group_id",
            "dataset_release_id",
            "source_indicator_code",
            "source_country_code",
            "source_country_name",
        ],
    )

    write_manifest(
        snapshot_date,
        {
            "jurisdictions": len(jurisdictions),
            "metrics": len(metrics),
            "datasets": len(datasets),
            "dataset_releases": len(dataset_releases),
            "indicator_definitions": len(indicator_definitions),
            "observations": len(observations),
        },
    )

    print(f"Wrote Phase 1 education extract to {OUTPUT_ROOT}")


if __name__ == "__main__":
    run()
