# Adult Skills Backfill Plan

This note tracks the current plan for backfilling `adult literacy` gaps in the Educational Inequality Map viewer using official adult-skills sources.

## Why this exists

The current viewer uses World Bank `SE.ADT.LITR.ZS` where available. That leaves large gaps for several major high-income countries. For the United States, we already use an explicit equivalent derived from official NCES `PIAAC 2023` results:

- `adult_literacy_equivalent = 100 - share_at_level_1_or_below_in_literacy`

This document extends that approach to other major countries using OECD `Survey of Adult Skills (PIAAC)` materials where possible.

## Recommended derivation

Use this only when a direct `adult literacy rate` is missing.

- Source family: `OECD Survey of Adult Skills (PIAAC)` or official national adult-skills releases
- Provisional metric name: `adult_literacy_equivalent`
- Derivation: `100 - share_at_level_1_or_below_in_literacy`
- Reference population: typically adults `16-65`
- Comparability flag: `not_directly_comparable`
- Quality flag: `published_derived`

## Priority countries

These are the current high-priority countries with large populations and no direct literacy value in the viewer.

| Country | ISO3 | Recommended source | Notes |
|---|---|---|---|
| Japan | `JPN` | OECD PIAAC 2023 country note | Good fit for the same derivation used for the U.S. |
| Germany | `DEU` | OECD PIAAC 2023 country note | Good fit for the same derivation used for the U.S. |
| United Kingdom | `GBR` | OECD PIAAC 2023 England country note | Coverage is England, not full UK; requires explicit caveat. |
| France | `FRA` | OECD PIAAC 2023 country note | Good fit for the same derivation used for the U.S. |
| Canada | `CAN` | OECD PIAAC 2023 country note | Good fit for the same derivation used for the U.S. |
| Australia | `AUS` | OECD PIAAC Cycle 1 country note | Older than the 2023 notes; use only until a better official adult-skills source is staged. |
| Netherlands | `NLD` | OECD PIAAC 2023 country note | Good fit for the same derivation used for the U.S. |
| Belgium | `BEL` | OECD PIAAC 2023 Belgium (Flemish Region) country note | Regional, not national; requires explicit caveat. |
| Czechia | `CZE` | OECD PIAAC 2023 country note | Good fit for the same derivation used for the U.S. |
| Sweden | `SWE` | OECD PIAAC 2023 country note | Good fit for the same derivation used for the U.S. |

## Staging plan

The stage-2 downloader now has an `oecd_piaac_adult_skills` group that should stage:

- the OECD country-material index
- OECD 2023 country notes for the high-priority countries above
- the older Australia cycle-1 note PDF as an interim source

Expected raw landing zone:

- `outputs/educational_inequality_map/raw/2026-03-30/oecd_adult_skills/`

## Parser plan

The next parser should:

1. read staged local HTML or PDF-derived text, not live web pages
2. extract the country-specific `share at Level 1 or below in literacy`
3. compute `adult_literacy_equivalent`
4. attach the exact source note and caveat
5. write a small normalized intermediate file, for example:

`outputs/educational_inequality_map/processed/adult_skills_equivalents.csv`

Suggested fields:

- `iso3`
- `country_name`
- `source_system`
- `source_release_year`
- `reference_population`
- `low_literacy_share_pct`
- `adult_literacy_equivalent_pct`
- `coverage_note`
- `comparability_flag`
- `quality_flag`
- `source_url`

## Caveats to preserve in the viewer

- `GBR`: the OECD cycle-2 note available here is for `England`, not all of the UK.
- `BEL`: the OECD cycle-2 note available here is for the `Flemish Region`, not all of Belgium.
- `AUS`: current easy-to-stage OECD source appears to be an older cycle-1 note rather than a 2023 note.
- Any adult-skills-based value must stay visually distinct from direct literacy-rate observations.

## Current blocker and fallback route

As of March 30, 2026, the direct OECD HTML country-note pages appear to be protected by a Cloudflare challenge when fetched from our scripted downloader, even with browser-like headers. That means the official country-note URLs are good provenance targets, but not yet a reliable automated staging path.

The best fallback route is:

1. stage the official OECD `Education at a Glance 2025` PDF
2. use its PIAAC chapter and referenced `Table 2` / StatLink data as the aggregate source for literacy proficiency distributions
3. keep the country-note URLs in the manifest and notes as provenance targets for later manual or browser-assisted retrieval

This keeps the pipeline official and reproducible without depending entirely on the blocked HTML pages.

## Source links

- [OECD Country Specific Material](https://www.oecd.org/en/about/programmes/piaac/country-specific-material.html)
- [OECD Education at a Glance 2025 PDF](https://www.oecd.org/content/dam/oecd/en/publications/reports/2025/09/education-at-a-glance-2025_c58fc9ae/1c0d9c79-en.pdf)
- [OECD Survey of Adults Skills 2023: Germany](https://www.oecd.org/en/publications/2024/12/survey-of-adults-skills-2023-country-notes_df7b4a60/germany_264dd624.html)
- [OECD Survey of Adults Skills 2023: France](https://www.oecd.org/en/publications/2024/12/survey-of-adults-skills-2023-country-notes_df7b4a60/france_ba42b6a4.html)
- [OECD Survey of Adults Skills 2023: Canada](https://www.oecd.org/en/publications/survey-of-adults-skills-2023-country-notes_ab4f6b8c-en/canada_5ecab9d9-en.html)
- [OECD Survey of Adults Skills 2023: Japan](https://www.oecd.org/en/publications/2024/12/survey-of-adults-skills-2023-country-notes_df7b4a60/japan_c63b2ef1.html)
- [OECD Survey of Adults Skills 2023: England (United Kingdom)](https://www.oecd.org/en/publications/survey-of-adults-skills-2023-country-notes_ab4f6b8c-en/united-kingdom_02bc78e4-en.html)
- [OECD Survey of Adults Skills 2023: Netherlands](https://www.oecd.org/en/publications/survey-of-adults-skills-2023-country-notes_ab4f6b8c-en/netherlands_bdaa68d1-en.html)
- [OECD Survey of Adults Skills 2023: Czechia](https://www.oecd.org/en/publications/2024/12/survey-of-adults-skills-2023-country-notes_df7b4a60/czechia_48f7166c.html)
- [OECD Survey of Adults Skills 2023: Sweden](https://www.oecd.org/en/publications/survey-of-adults-skills-2023-country-notes_ab4f6b8c-en/sweden_743ccd1f-en.html)
- [OECD Survey of Adults Skills 2023: Belgium (Flemish Region)](https://www.oecd.org/en/publications/survey-of-adults-skills-2023-country-notes_ab4f6b8c-en/belgium_7187249a-en.html)
- [OECD Australia Cycle 1 Country Note PDF](https://www.oecd.org/content/dam/oecd/en/about/programmes/edu/piaac/country-specific-material/cycle-1/Australia-Country-Note.pdf)
