# Public Data Accessibility Project

**Source:** Adam Ficher

## Problem
Coworkers frustrated by lack of data organization across jurisdictions. Public data exists but requires extensive scraping and conversion from PDFs to usable formats.

## Bounty direction
Create public APIs and standardized formats for commonly needed municipal data sets.

## Targeted start
Focus on data types Thomas's team uses most: demographics, utilities, infrastructure planning.

## Example scopes
- Property tax assessment standardization across counties
- Building permit process data and timelines
- Zoning regulation databases by municipality
- Public school enrollment and capacity data

## Notes
- Standardize column definitions and metadata for each municipal dataset type.
- Prioritize jurisdictions with machine-readable data to establish a reference schema.
- Track provenance and document any OCR or manual cleanup steps.
- Define a minimal API contract (pagination, filters, update cadence).

## Starting point suggestions
- Select two nearby counties and focus on one dataset type (property tax or permits).
- Build a lightweight ingestion pipeline that converts PDFs to CSV with an audit log.
- Publish a sample API endpoint or downloadable CSV with consistent field names.
- Document the schema and a checklist for adding new jurisdictions.
