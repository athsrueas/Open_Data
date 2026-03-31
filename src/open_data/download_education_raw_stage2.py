"""Stage additional raw education sources into source-specific landing zones.

Downloads only directly accessible raw assets and records gated/manual steps
in manifests when a source requires human interaction.
"""

from __future__ import annotations

import datetime as dt
import json
from pathlib import Path
from typing import Any
from urllib.request import Request, urlopen


RAW_ROOT = Path("outputs") / "educational_inequality_map" / "raw"
USER_AGENT = "Mozilla/5.0"


UIS_RESOURCES = [
    {
        "name": "uis_bulk_page",
        "url": "https://databrowser.uis.unesco.org/resources/bulk",
        "relative_path": Path("unesco_uis") / "bulk_page.html",
        "kind": "html",
    },
    {
        "name": "uis_bulk_uis_zip",
        "url": "https://download.uis.unesco.org/bdds/202602/UIS",
        "relative_path": Path("unesco_uis") / "downloads" / "UIS_202602.zip",
        "kind": "binary",
    },
    {
        "name": "uis_bulk_sdg_zip",
        "url": "https://download.uis.unesco.org/bdds/202602/SDG.zip",
        "relative_path": Path("unesco_uis") / "downloads" / "SDG_202602.zip",
        "kind": "binary",
    },
    {
        "name": "uis_bulk_opri_zip",
        "url": "https://download.uis.unesco.org/bdds/202602/OPRI.zip",
        "relative_path": Path("unesco_uis") / "downloads" / "OPRI_202602.zip",
        "kind": "binary",
    },
]


GIGA_RESOURCES = [
    {
        "name": "giga_open_data_page",
        "url": "https://giga.global/what-we-do/our-solutions/open-data/",
        "relative_path": Path("giga") / "open_data_page.html",
        "kind": "html",
    },
    {
        "name": "giga_explore_api_docs",
        "url": "https://maps.giga.global/docs/explore-api",
        "relative_path": Path("giga") / "explore_api_docs.html",
        "kind": "html",
    },
    {
        "name": "giga_locations_countries",
        "url": "https://uni-ooi-giga-backend-hjekcuagasashucv.a03.azurefd.net/api/locations/countries/",
        "relative_path": Path("giga") / "api" / "locations_countries.json",
        "kind": "json",
    },
    {
        "name": "giga_published_layers",
        "url": "https://uni-ooi-giga-backend-hjekcuagasashucv.a03.azurefd.net/api/accounts/layers/PUBLISHED/?expand=created_by,last_modified_by,published_by&ordering=-last_modified_at",
        "relative_path": Path("giga") / "api" / "published_layers.json",
        "kind": "json",
    },
    {
        "name": "giga_global_stats",
        "url": "https://uni-ooi-giga-backend-hjekcuagasashucv.a03.azurefd.net/api/statistics/global-stat/",
        "relative_path": Path("giga") / "api" / "global_stat.json",
        "kind": "json",
    },
]


WORLD_BANK_EXTRA_RESOURCES = [
    {
        "name": "worldbank_hlo_catalog_page",
        "url": "https://datacatalog.worldbank.org/search/dataset/0038001/harmonized-learning-outcomes-hlo-database",
        "relative_path": Path("worldbank_research") / "hlo_catalog_page.html",
        "kind": "html",
    },
    {
        "name": "worldbank_hlo_xlsx",
        "url": "https://datacatalogfiles.worldbank.org/ddh-published/0038001/1/DR0046131/hlo_database.xlsx",
        "relative_path": Path("worldbank_research") / "downloads" / "hlo_database.xlsx",
        "kind": "binary",
    },
    {
        "name": "worldbank_learning_poverty_catalog_page",
        "url": "https://datacatalog.worldbank.org/search/dataset/0038947/learning-poverty-global-database-historical-data-and-sub-components",
        "relative_path": Path("worldbank_research") / "learning_poverty_catalog_page.html",
        "kind": "html",
    },
    {
        "name": "worldbank_learning_poverty_2024_xls",
        "url": "https://datacatalogfiles.worldbank.org/ddh-published/0038947/8/DR0094223/lpv_edstats_1303.xls",
        "relative_path": Path("worldbank_research") / "downloads" / "lpv_edstats_1303_2024.xls",
        "kind": "binary",
    },
    {
        "name": "worldbank_learning_poverty_2022_xls",
        "url": "https://datacatalogfiles.worldbank.org/ddh-published/0038947/8/DR0090187/lpv_edstats_1205.xls",
        "relative_path": Path("worldbank_research") / "downloads" / "lpv_edstats_1205_2022.xls",
        "kind": "binary",
    },
    {
        "name": "worldbank_learning_poverty_2021_xls",
        "url": "https://datacatalogfiles.worldbank.org/ddh-published/0038947/8/DR0054368/lpv_edstats_update2021.xls",
        "relative_path": Path("worldbank_research") / "downloads" / "lpv_edstats_update2021.xls",
        "kind": "binary",
    },
    {
        "name": "worldbank_learning_poverty_2019_xls",
        "url": "https://datacatalogfiles.worldbank.org/ddh-published/0038947/8/DR0048277/lpv_edstats.xls",
        "relative_path": Path("worldbank_research") / "downloads" / "lpv_edstats_2019.xls",
        "kind": "binary",
    },
]


OECD_RESOURCES = [
    {
        "name": "oecd_pisa_index_page",
        "url": "https://webfs.oecd.org/pisa2022/index.html",
        "relative_path": Path("oecd_pisa") / "index.html",
        "kind": "html",
    },
    {
        "name": "oecd_pisa_school_questionnaire_sas",
        "url": "https://webfs.oecd.org/pisa2022/SCH_QQQ_SAS.zip",
        "relative_path": Path("oecd_pisa") / "downloads" / "SCH_QQQ_SAS.zip",
        "kind": "binary",
    },
    {
        "name": "oecd_pisa_student_questionnaire_sas",
        "url": "https://webfs.oecd.org/pisa2022/STU_QQQ_SAS.zip",
        "relative_path": Path("oecd_pisa") / "downloads" / "STU_QQQ_SAS.zip",
        "kind": "binary",
    },
    {
        "name": "oecd_pisa_teacher_questionnaire_sas",
        "url": "https://webfs.oecd.org/pisa2022/TCH_QQQ_SAS.zip",
        "relative_path": Path("oecd_pisa") / "downloads" / "TCH_QQQ_SAS.zip",
        "kind": "binary",
    },
    {
        "name": "oecd_pisa_student_cognitive_sas",
        "url": "https://webfs.oecd.org/pisa2022/STU_COG_SAS.zip",
        "relative_path": Path("oecd_pisa") / "downloads" / "STU_COG_SAS.zip",
        "kind": "binary",
    },
    {
        "name": "oecd_pisa_student_timing_sas",
        "url": "https://webfs.oecd.org/pisa2022/STU_TIM_SAS.zip",
        "relative_path": Path("oecd_pisa") / "downloads" / "STU_TIM_SAS.zip",
        "kind": "binary",
    },
    {
        "name": "oecd_pisa_creative_thinking_sas",
        "url": "https://webfs.oecd.org/pisa2022/CRT_SAS.zip",
        "relative_path": Path("oecd_pisa") / "downloads" / "CRT_SAS.zip",
        "kind": "binary",
    },
    {
        "name": "oecd_pisa_financial_literacy_sas",
        "url": "https://webfs.oecd.org/pisa2022/FLT_SAS.zip",
        "relative_path": Path("oecd_pisa") / "downloads" / "FLT_SAS.zip",
        "kind": "binary",
    },
    {
        "name": "oecd_pisa_school_questionnaire_spss",
        "url": "https://webfs.oecd.org/pisa2022/SCH_QQQ_SPSS.zip",
        "relative_path": Path("oecd_pisa") / "downloads" / "SCH_QQQ_SPSS.zip",
        "kind": "binary",
    },
    {
        "name": "oecd_pisa_student_questionnaire_spss",
        "url": "https://webfs.oecd.org/pisa2022/STU_QQQ_SPSS.zip",
        "relative_path": Path("oecd_pisa") / "downloads" / "STU_QQQ_SPSS.zip",
        "kind": "binary",
    },
    {
        "name": "oecd_pisa_teacher_questionnaire_spss",
        "url": "https://webfs.oecd.org/pisa2022/TCH_QQQ_SPSS.zip",
        "relative_path": Path("oecd_pisa") / "downloads" / "TCH_QQQ_SPSS.zip",
        "kind": "binary",
    },
    {
        "name": "oecd_pisa_student_cognitive_spss",
        "url": "https://webfs.oecd.org/pisa2022/STU_COG_SPSS.zip",
        "relative_path": Path("oecd_pisa") / "downloads" / "STU_COG_SPSS.zip",
        "kind": "binary",
    },
    {
        "name": "oecd_pisa_student_timing_spss",
        "url": "https://webfs.oecd.org/pisa2022/STU_TIM_SPSS.zip",
        "relative_path": Path("oecd_pisa") / "downloads" / "STU_TIM_SPSS.zip",
        "kind": "binary",
    },
    {
        "name": "oecd_pisa_creative_thinking_spss",
        "url": "https://webfs.oecd.org/pisa2022/CRT_SPSS.zip",
        "relative_path": Path("oecd_pisa") / "downloads" / "CRT_SPSS.zip",
        "kind": "binary",
    },
    {
        "name": "oecd_pisa_financial_literacy_spss",
        "url": "https://webfs.oecd.org/pisa2022/FLT_SPSS.zip",
        "relative_path": Path("oecd_pisa") / "downloads" / "FLT_SPSS.zip",
        "kind": "binary",
    },
    {
        "name": "oecd_pisa_codebook",
        "url": "https://webfs.oecd.org/pisa2022/CY08MSP_CODEBOOK_27thJune24.xlsx",
        "relative_path": Path("oecd_pisa") / "downloads" / "CY08MSP_CODEBOOK_27thJune24.xlsx",
        "kind": "binary",
    },
    {
        "name": "oecd_pisa_questionnaire_compendia",
        "url": "https://webfs.oecd.org/pisa2022/PISA2022_FinalRelease_Compendia_18thJune24.zip",
        "relative_path": Path("oecd_pisa") / "downloads" / "PISA2022_FinalRelease_Compendia_18thJune24.zip",
        "kind": "binary",
    },
    {
        "name": "oecd_pisa_cognitive_compendia",
        "url": "https://webfs.oecd.org/pisa2022/PISA2022_FinalRelease_Compendia_18thJune24_cog.zip",
        "relative_path": Path("oecd_pisa") / "downloads" / "PISA2022_FinalRelease_Compendia_18thJune24_cog.zip",
        "kind": "binary",
    },
    {
        "name": "oecd_pisa_creative_thinking_compendia",
        "url": "https://webfs.oecd.org/pisa2022/PISA2022_FinalRelease_CrT_Compendia_18thJune24.zip",
        "relative_path": Path("oecd_pisa") / "downloads" / "PISA2022_FinalRelease_CrT_Compendia_18thJune24.zip",
        "kind": "binary",
    },
    {
        "name": "oecd_pisa_financial_literacy_compendia",
        "url": "https://webfs.oecd.org/pisa2022/PISA2022_FinalRelease_FLT_Compendia_27thJune24.zip",
        "relative_path": Path("oecd_pisa") / "downloads" / "PISA2022_FinalRelease_FLT_Compendia_27thJune24.zip",
        "kind": "binary",
    },
    {
        "name": "oecd_pisa_public_codes_zip",
        "url": "https://webfs.oecd.org/pisa2022/PISA2022_Stata_PublicCodes.zip",
        "relative_path": Path("oecd_pisa") / "downloads" / "PISA2022_Stata_PublicCodes.zip",
        "kind": "binary",
    },
    {
        "name": "oecd_pisa_rescaled_indices_zip",
        "url": "https://webfs.oecd.org/pisa2022/escs_trend.zip",
        "relative_path": Path("oecd_pisa") / "downloads" / "escs_trend.zip",
        "kind": "binary",
    },
]


def fetch_bytes(url: str) -> bytes:
    request = Request(url, headers={"User-Agent": USER_AGENT, "Accept-Language": "en-US,en;q=0.9"})
    with urlopen(request, timeout=120) as response:
        return response.read()


def write_bytes(path: Path, payload: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(payload)


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def build_group_manifest(group_name: str, resources: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "generated_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "group": group_name,
        "status": "provisional_pending_armando_review",
        "resources": resources,
    }


def download_group(base_dir: Path, group_name: str, resources: list[dict[str, str]]) -> list[dict[str, Any]]:
    manifest_path = base_dir / group_name / "manifest.json"
    results: list[dict[str, Any]] = []

    if manifest_path.exists():
        try:
            existing_manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            if isinstance(existing_manifest.get("resources"), list):
                results = existing_manifest["resources"]
        except json.JSONDecodeError:
            pass

    existing_by_name = {result.get("name"): result for result in results if isinstance(result, dict)}

    for index, resource in enumerate(resources, start=1):
        target = base_dir / resource["relative_path"]
        temp_target = target.with_suffix(f"{target.suffix}.part")

        if temp_target.exists():
            temp_target.unlink()

        print(f"[{group_name} {index}/{len(resources)}] {resource['name']} -> {target}")

        if target.exists():
            result = {
                "name": resource["name"],
                "url": resource["url"],
                "saved_to": str(target).replace("\\", "/"),
                "bytes": target.stat().st_size,
                "status": "skipped_existing",
                "kind": resource["kind"],
            }
            existing_by_name[resource["name"]] = result
            print(f"  skipped existing ({result['bytes']:,} bytes)")
            write_json(
                manifest_path,
                build_group_manifest(
                    group_name,
                    [existing_by_name[item["name"]] for item in resources if item["name"] in existing_by_name],
                ),
            )
            continue

        try:
            payload = fetch_bytes(resource["url"])
            temp_target.parent.mkdir(parents=True, exist_ok=True)
            temp_target.write_bytes(payload)
            temp_target.replace(target)
            result = {
                "name": resource["name"],
                "url": resource["url"],
                "saved_to": str(target).replace("\\", "/"),
                "bytes": len(payload),
                "status": "downloaded",
                "kind": resource["kind"],
            }
            existing_by_name[resource["name"]] = result
            print(f"  downloaded {len(payload):,} bytes")
        except Exception as exc:
            if temp_target.exists():
                temp_target.unlink()
            result = {
                "name": resource["name"],
                "url": resource["url"],
                "saved_to": str(target).replace("\\", "/"),
                "status": "error",
                "error": str(exc),
                "kind": resource["kind"],
            }
            existing_by_name[resource["name"]] = result
            print(f"  error: {exc}")

        write_json(
            manifest_path,
            build_group_manifest(
                group_name,
                [existing_by_name[item["name"]] for item in resources if item["name"] in existing_by_name],
            ),
        )

    return [existing_by_name[item["name"]] for item in resources if item["name"] in existing_by_name]


def write_oecd_notes(base_dir: Path) -> None:
    notes = {
        "generated_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "source": "OECD PISA 2022",
        "status": "direct_index_available",
        "notes": [
            "The direct OECD file index at https://webfs.oecd.org/pisa2022/index.html was used for raw staging.",
            "PISA 2022 SAS and SPSS raw file archives are directly downloadable from that index.",
            "The original survey landing page still exists at https://survey.oecd.org/index.php?r=survey/index&sid=197663&lang=en and may document terms or user tracking expectations.",
        ],
    }
    write_json(base_dir / "oecd_pisa" / "manual_notes.json", notes)


def run() -> None:
    snapshot = dt.date.today().isoformat()
    base_dir = RAW_ROOT / snapshot

    summary = {
        "generated_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "snapshot_date": snapshot,
        "mode": "raw_landing_zone_stage2",
        "status": "provisional_pending_armando_review",
        "groups": {},
    }

    summary["groups"]["unesco_uis"] = download_group(base_dir, "unesco_uis", UIS_RESOURCES)
    summary["groups"]["giga"] = download_group(base_dir, "giga", GIGA_RESOURCES)
    summary["groups"]["worldbank_research"] = download_group(base_dir, "worldbank_research", WORLD_BANK_EXTRA_RESOURCES)
    summary["groups"]["oecd_pisa"] = download_group(base_dir, "oecd_pisa", OECD_RESOURCES)
    write_oecd_notes(base_dir)

    write_json(base_dir / "stage2_manifest.json", summary)
    print(f"Wrote additional raw education sources to {base_dir}")


if __name__ == "__main__":
    run()
