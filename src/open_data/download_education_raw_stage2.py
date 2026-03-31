"""Stage additional raw education sources into source-specific landing zones.

Downloads only directly accessible raw assets and records gated/manual steps
in manifests when a source requires human interaction.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
from pathlib import Path
from typing import Any
from urllib.parse import quote, urlsplit, urlunsplit
from urllib.request import Request, urlopen


RAW_ROOT = Path("outputs") / "educational_inequality_map" / "raw"
USER_AGENT = "Mozilla/5.0"
GEOBOUNDARIES_METADATA_URL = "https://www.geoboundaries.org/api/current/gbOpen/ALL/ADM0/"


UIS_RESOURCES = [
    {
        "name": "uis_bulk_page",
        "url": "https://databrowser.uis.unesco.org/resources/bulk",
        "relative_path": Path("unesco_uis") / "bulk_page.html",
        "kind": "html",
    },
    {
        "name": "uis_background_doc_pdf",
        "url": "https://download.uis.unesco.org/bdds/202602/UIS - Data Release Background Doc -EN-Feb 2026.pdf",
        "relative_path": Path("unesco_uis") / "downloads" / "UIS_background_doc_EN_Feb_2026.pdf",
        "kind": "pdf",
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


GEOBOUNDARIES_RESOURCES = [
    {
        "name": "geoboundaries_adm0_metadata",
        "url": GEOBOUNDARIES_METADATA_URL,
        "relative_path": Path("geoboundaries") / "api" / "gbOpen_ALL_ADM0.json",
        "kind": "json",
    }
]


OECD_PIAAC_ADULT_SKILLS_RESOURCES = [
    {
        "name": "oecd_piaac_country_material_index",
        "url": "https://www.oecd.org/en/about/programmes/piaac/country-specific-material.html",
        "relative_path": Path("oecd_adult_skills") / "country_specific_material.html",
        "kind": "html",
    },
    {
        "name": "oecd_education_at_a_glance_2025_pdf",
        "url": "https://www.oecd.org/content/dam/oecd/en/publications/reports/2025/09/education-at-a-glance-2025_c58fc9ae/1c0d9c79-en.pdf",
        "relative_path": Path("oecd_adult_skills") / "education_at_a_glance_2025.pdf",
        "kind": "pdf",
    },
    {
        "name": "oecd_piaac_canada_2023_country_note",
        "url": "https://www.oecd.org/en/publications/survey-of-adults-skills-2023-country-notes_ab4f6b8c-en/canada_5ecab9d9-en.html",
        "relative_path": Path("oecd_adult_skills") / "canada_2023_country_note.html",
        "kind": "html",
    },
    {
        "name": "oecd_piaac_japan_2023_country_note",
        "url": "https://www.oecd.org/en/publications/2024/12/survey-of-adults-skills-2023-country-notes_df7b4a60/japan_c63b2ef1.html",
        "relative_path": Path("oecd_adult_skills") / "japan_2023_country_note.html",
        "kind": "html",
    },
    {
        "name": "oecd_piaac_france_2023_country_note",
        "url": "https://www.oecd.org/en/publications/2024/12/survey-of-adults-skills-2023-country-notes_df7b4a60/france_ba42b6a4.html",
        "relative_path": Path("oecd_adult_skills") / "france_2023_country_note.html",
        "kind": "html",
    },
    {
        "name": "oecd_piaac_germany_2023_country_note",
        "url": "https://www.oecd.org/en/publications/2024/12/survey-of-adults-skills-2023-country-notes_df7b4a60/germany_264dd624.html",
        "relative_path": Path("oecd_adult_skills") / "germany_2023_country_note.html",
        "kind": "html",
    },
    {
        "name": "oecd_piaac_england_2023_country_note",
        "url": "https://www.oecd.org/en/publications/survey-of-adults-skills-2023-country-notes_ab4f6b8c-en/united-kingdom_02bc78e4-en.html",
        "relative_path": Path("oecd_adult_skills") / "england_2023_country_note.html",
        "kind": "html",
    },
    {
        "name": "oecd_piaac_netherlands_2023_country_note",
        "url": "https://www.oecd.org/en/publications/survey-of-adults-skills-2023-country-notes_ab4f6b8c-en/netherlands_bdaa68d1-en.html",
        "relative_path": Path("oecd_adult_skills") / "netherlands_2023_country_note.html",
        "kind": "html",
    },
    {
        "name": "oecd_piaac_czechia_2023_country_note",
        "url": "https://www.oecd.org/en/publications/survey-of-adults-skills-2023-country-notes_ab4f6b8c-en/czechia_7ed38300-en.html",
        "relative_path": Path("oecd_adult_skills") / "czechia_2023_country_note.html",
        "kind": "html",
    },
    {
        "name": "oecd_piaac_sweden_2023_country_note",
        "url": "https://www.oecd.org/en/publications/survey-of-adults-skills-2023-country-notes_ab4f6b8c-en/sweden_743ccd1f-en.html",
        "relative_path": Path("oecd_adult_skills") / "sweden_2023_country_note.html",
        "kind": "html",
    },
    {
        "name": "oecd_piaac_belgium_flemish_2023_country_note",
        "url": "https://www.oecd.org/en/publications/survey-of-adults-skills-2023-country-notes_ab4f6b8c-en/belgium_7187249a-en.html",
        "relative_path": Path("oecd_adult_skills") / "belgium_flemish_2023_country_note.html",
        "kind": "html",
    },
    {
        "name": "oecd_piaac_australia_cycle1_country_note_pdf",
        "url": "https://www.oecd.org/content/dam/oecd/en/about/programmes/edu/piaac/country-specific-material/cycle-1/Australia-Country-Note.pdf",
        "relative_path": Path("oecd_adult_skills") / "australia_cycle1_country_note.pdf",
        "kind": "pdf",
    },
]


NCES_PIAAC_US_RESOURCES = [
    {
        "name": "nces_piaac_2023_national_results",
        "url": "https://nces.ed.gov/surveys/piaac/2023/national_results.asp",
        "relative_path": Path("nces_piaac_us") / "national_results_2023.html",
        "kind": "html",
    },
    {
        "name": "nces_piaac_faq",
        "url": "https://nces.ed.gov/surveys/piaac/faq.asp",
        "relative_path": Path("nces_piaac_us") / "faq.html",
        "kind": "html",
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
        "group": "docs",
    },
    {
        "name": "oecd_pisa_school_questionnaire_sas",
        "url": "https://webfs.oecd.org/pisa2022/SCH_QQQ_SAS.zip",
        "relative_path": Path("oecd_pisa") / "downloads" / "SCH_QQQ_SAS.zip",
        "kind": "binary",
        "group": "sas",
    },
    {
        "name": "oecd_pisa_student_questionnaire_sas",
        "url": "https://webfs.oecd.org/pisa2022/STU_QQQ_SAS.zip",
        "relative_path": Path("oecd_pisa") / "downloads" / "STU_QQQ_SAS.zip",
        "kind": "binary",
        "group": "sas",
    },
    {
        "name": "oecd_pisa_teacher_questionnaire_sas",
        "url": "https://webfs.oecd.org/pisa2022/TCH_QQQ_SAS.zip",
        "relative_path": Path("oecd_pisa") / "downloads" / "TCH_QQQ_SAS.zip",
        "kind": "binary",
        "group": "sas",
    },
    {
        "name": "oecd_pisa_student_cognitive_sas",
        "url": "https://webfs.oecd.org/pisa2022/STU_COG_SAS.zip",
        "relative_path": Path("oecd_pisa") / "downloads" / "STU_COG_SAS.zip",
        "kind": "binary",
        "group": "sas",
    },
    {
        "name": "oecd_pisa_student_timing_sas",
        "url": "https://webfs.oecd.org/pisa2022/STU_TIM_SAS.zip",
        "relative_path": Path("oecd_pisa") / "downloads" / "STU_TIM_SAS.zip",
        "kind": "binary",
        "group": "sas",
    },
    {
        "name": "oecd_pisa_creative_thinking_sas",
        "url": "https://webfs.oecd.org/pisa2022/CRT_SAS.zip",
        "relative_path": Path("oecd_pisa") / "downloads" / "CRT_SAS.zip",
        "kind": "binary",
        "group": "sas",
    },
    {
        "name": "oecd_pisa_financial_literacy_sas",
        "url": "https://webfs.oecd.org/pisa2022/FLT_SAS.zip",
        "relative_path": Path("oecd_pisa") / "downloads" / "FLT_SAS.zip",
        "kind": "binary",
        "group": "sas",
    },
    {
        "name": "oecd_pisa_school_questionnaire_spss",
        "url": "https://webfs.oecd.org/pisa2022/SCH_QQQ_SPSS.zip",
        "relative_path": Path("oecd_pisa") / "downloads" / "SCH_QQQ_SPSS.zip",
        "kind": "binary",
        "group": "spss",
    },
    {
        "name": "oecd_pisa_student_questionnaire_spss",
        "url": "https://webfs.oecd.org/pisa2022/STU_QQQ_SPSS.zip",
        "relative_path": Path("oecd_pisa") / "downloads" / "STU_QQQ_SPSS.zip",
        "kind": "binary",
        "group": "spss",
    },
    {
        "name": "oecd_pisa_teacher_questionnaire_spss",
        "url": "https://webfs.oecd.org/pisa2022/TCH_QQQ_SPSS.zip",
        "relative_path": Path("oecd_pisa") / "downloads" / "TCH_QQQ_SPSS.zip",
        "kind": "binary",
        "group": "spss",
    },
    {
        "name": "oecd_pisa_student_cognitive_spss",
        "url": "https://webfs.oecd.org/pisa2022/STU_COG_SPSS.zip",
        "relative_path": Path("oecd_pisa") / "downloads" / "STU_COG_SPSS.zip",
        "kind": "binary",
        "group": "spss",
    },
    {
        "name": "oecd_pisa_student_timing_spss",
        "url": "https://webfs.oecd.org/pisa2022/STU_TIM_SPSS.zip",
        "relative_path": Path("oecd_pisa") / "downloads" / "STU_TIM_SPSS.zip",
        "kind": "binary",
        "group": "spss",
    },
    {
        "name": "oecd_pisa_creative_thinking_spss",
        "url": "https://webfs.oecd.org/pisa2022/CRT_SPSS.zip",
        "relative_path": Path("oecd_pisa") / "downloads" / "CRT_SPSS.zip",
        "kind": "binary",
        "group": "spss",
    },
    {
        "name": "oecd_pisa_financial_literacy_spss",
        "url": "https://webfs.oecd.org/pisa2022/FLT_SPSS.zip",
        "relative_path": Path("oecd_pisa") / "downloads" / "FLT_SPSS.zip",
        "kind": "binary",
        "group": "spss",
    },
    {
        "name": "oecd_pisa_codebook",
        "url": "https://webfs.oecd.org/pisa2022/CY08MSP_CODEBOOK_27thJune24.xlsx",
        "relative_path": Path("oecd_pisa") / "downloads" / "CY08MSP_CODEBOOK_27thJune24.xlsx",
        "kind": "binary",
        "group": "docs",
    },
    {
        "name": "oecd_pisa_questionnaire_compendia",
        "url": "https://webfs.oecd.org/pisa2022/PISA2022_FinalRelease_Compendia_18thJune24.zip",
        "relative_path": Path("oecd_pisa") / "downloads" / "PISA2022_FinalRelease_Compendia_18thJune24.zip",
        "kind": "binary",
        "group": "docs",
    },
    {
        "name": "oecd_pisa_cognitive_compendia",
        "url": "https://webfs.oecd.org/pisa2022/PISA2022_FinalRelease_Compendia_18thJune24_cog.zip",
        "relative_path": Path("oecd_pisa") / "downloads" / "PISA2022_FinalRelease_Compendia_18thJune24_cog.zip",
        "kind": "binary",
        "group": "docs",
    },
    {
        "name": "oecd_pisa_creative_thinking_compendia",
        "url": "https://webfs.oecd.org/pisa2022/PISA2022_FinalRelease_CrT_Compendia_18thJune24.zip",
        "relative_path": Path("oecd_pisa") / "downloads" / "PISA2022_FinalRelease_CrT_Compendia_18thJune24.zip",
        "kind": "binary",
        "group": "docs",
    },
    {
        "name": "oecd_pisa_financial_literacy_compendia",
        "url": "https://webfs.oecd.org/pisa2022/PISA2022_FinalRelease_FLT_Compendia_27thJune24.zip",
        "relative_path": Path("oecd_pisa") / "downloads" / "PISA2022_FinalRelease_FLT_Compendia_27thJune24.zip",
        "kind": "binary",
        "group": "docs",
    },
    {
        "name": "oecd_pisa_public_codes_zip",
        "url": "https://webfs.oecd.org/pisa2022/PISA2022_Stata_PublicCodes.zip",
        "relative_path": Path("oecd_pisa") / "downloads" / "PISA2022_Stata_PublicCodes.zip",
        "kind": "binary",
        "group": "docs",
    },
    {
        "name": "oecd_pisa_rescaled_indices_zip",
        "url": "https://webfs.oecd.org/pisa2022/escs_trend.zip",
        "relative_path": Path("oecd_pisa") / "downloads" / "escs_trend.zip",
        "kind": "binary",
        "group": "docs",
    },
]


OECD_PROFILE_GROUPS = {
    "phase1": {"docs", "sas"},
    "phase1-spss": {"docs", "spss"},
    "docs-only": {"docs"},
    "full": {"docs", "sas", "spss"},
}


GROUP_RESOURCES = {
    "unesco_uis": UIS_RESOURCES,
    "giga": GIGA_RESOURCES,
    "geoboundaries": GEOBOUNDARIES_RESOURCES,
    "oecd_piaac_adult_skills": OECD_PIAAC_ADULT_SKILLS_RESOURCES,
    "nces_piaac_us": NCES_PIAAC_US_RESOURCES,
    "worldbank_research": WORLD_BANK_EXTRA_RESOURCES,
    "oecd_pisa": OECD_RESOURCES,
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--groups",
        nargs="+",
        choices=sorted(GROUP_RESOURCES),
        default=["unesco_uis", "giga", "geoboundaries", "oecd_piaac_adult_skills", "nces_piaac_us", "worldbank_research", "oecd_pisa"],
        help="Source groups to stage. OECD PISA defaults to the lighter Phase 1 profile unless you override it.",
    )
    parser.add_argument(
        "--oecd-profile",
        choices=sorted(OECD_PROFILE_GROUPS),
        default="phase1",
        help="Subset of OECD PISA resources to stage when oecd_pisa is included.",
    )
    return parser.parse_args()


def get_resources_for_group(group_name: str, args: argparse.Namespace) -> list[dict[str, str]]:
    if group_name != "oecd_pisa":
        return GROUP_RESOURCES[group_name]

    allowed_groups = OECD_PROFILE_GROUPS[args.oecd_profile]
    return [resource for resource in OECD_RESOURCES if resource["group"] in allowed_groups]


def fetch_bytes(url: str) -> bytes:
    parts = urlsplit(url)
    safe_url = urlunsplit(
        (
            parts.scheme,
            parts.netloc,
            quote(parts.path),
            parts.query,
            parts.fragment,
        )
    )
    request = Request(safe_url, headers={"User-Agent": USER_AGENT, "Accept-Language": "en-US,en;q=0.9"})
    with urlopen(request, timeout=120) as response:
        return response.read()


def fetch_json(url: str) -> Any:
    return json.loads(fetch_bytes(url).decode("utf-8"))


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


def download_geoboundaries_group(base_dir: Path) -> list[dict[str, Any]]:
    group_name = "geoboundaries"
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

    metadata_target = base_dir / group_name / "api" / "gbOpen_ALL_ADM0.json"
    print(f"[{group_name} 1/2] geoboundaries_adm0_metadata -> {metadata_target}")
    if metadata_target.exists():
        metadata_payload = json.loads(metadata_target.read_text(encoding="utf-8"))
        metadata_result = {
            "name": "geoboundaries_adm0_metadata",
            "url": GEOBOUNDARIES_METADATA_URL,
            "saved_to": str(metadata_target).replace("\\", "/"),
            "bytes": metadata_target.stat().st_size,
            "status": "skipped_existing",
            "kind": "json",
            "feature_count": len(metadata_payload) if isinstance(metadata_payload, list) else 0,
        }
        print(f"  skipped existing ({metadata_result['bytes']:,} bytes)")
    else:
        metadata_payload = fetch_json(GEOBOUNDARIES_METADATA_URL)
        write_json(metadata_target, metadata_payload)
        metadata_result = {
            "name": "geoboundaries_adm0_metadata",
            "url": GEOBOUNDARIES_METADATA_URL,
            "saved_to": str(metadata_target).replace("\\", "/"),
            "bytes": metadata_target.stat().st_size,
            "status": "downloaded",
            "kind": "json",
            "feature_count": len(metadata_payload) if isinstance(metadata_payload, list) else 0,
        }
        print(f"  downloaded {metadata_result['bytes']:,} bytes")

    existing_by_name["geoboundaries_adm0_metadata"] = metadata_result
    write_json(
        manifest_path,
        build_group_manifest(
            group_name,
            [existing_by_name["geoboundaries_adm0_metadata"]],
        ),
    )

    if not isinstance(metadata_payload, list):
        return [existing_by_name["geoboundaries_adm0_metadata"]]

    downloads_dir = base_dir / group_name / "downloads" / "ADM0_simplified"
    downloaded_count = 0
    skipped_count = 0
    error_count = 0

    print(f"[{group_name} 2/2] geoboundaries_adm0_simplified_geojsons -> {downloads_dir}")
    for index, record in enumerate(metadata_payload, start=1):
        boundary_iso = record.get("boundaryISO", f"unknown_{index}")
        source_url = record.get("simplifiedGeometryGeoJSON") or record.get("gjDownloadURL")
        if not source_url:
            error_count += 1
            continue

        target = downloads_dir / f"{boundary_iso}.geojson"
        if target.exists():
            skipped_count += 1
            continue

        try:
            payload = fetch_bytes(source_url)
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(payload)
            downloaded_count += 1
        except Exception:
            error_count += 1

    geometries_result = {
        "name": "geoboundaries_adm0_simplified_geojsons",
        "url": GEOBOUNDARIES_METADATA_URL,
        "saved_to": str(downloads_dir).replace("\\", "/"),
        "status": "downloaded" if error_count == 0 else "partial",
        "kind": "geojson_collection",
        "files_total": len(metadata_payload),
        "files_downloaded_now": downloaded_count,
        "files_skipped_existing": skipped_count,
        "files_error": error_count,
    }
    print(
        "  "
        f"downloaded_now={downloaded_count:,}, "
        f"skipped_existing={skipped_count:,}, "
        f"errors={error_count:,}"
    )

    existing_by_name["geoboundaries_adm0_simplified_geojsons"] = geometries_result
    write_json(
        manifest_path,
        build_group_manifest(
            group_name,
            [
                existing_by_name["geoboundaries_adm0_metadata"],
                existing_by_name["geoboundaries_adm0_simplified_geojsons"],
            ],
        ),
    )

    return [
        existing_by_name["geoboundaries_adm0_metadata"],
        existing_by_name["geoboundaries_adm0_simplified_geojsons"],
    ]


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
    args = parse_args()
    snapshot = dt.date.today().isoformat()
    base_dir = RAW_ROOT / snapshot

    summary = {
        "generated_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "snapshot_date": snapshot,
        "mode": "raw_landing_zone_stage2",
        "status": "provisional_pending_armando_review",
        "groups_requested": args.groups,
        "oecd_profile": args.oecd_profile if "oecd_pisa" in args.groups else "",
        "groups": {},
    }

    for group_name in args.groups:
        if group_name == "geoboundaries":
            summary["groups"][group_name] = download_geoboundaries_group(base_dir)
            continue

        resources = get_resources_for_group(group_name, args)
        summary["groups"][group_name] = download_group(base_dir, group_name, resources)

    if "oecd_pisa" in args.groups:
        write_oecd_notes(base_dir)

    write_json(base_dir / "stage2_manifest.json", summary)
    print(f"Wrote additional raw education sources to {base_dir}")


if __name__ == "__main__":
    run()
