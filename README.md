# Open Data

Tools for collecting and organizing open data.

## Catalog metadata foundation

This repository now ships a lightweight metadata schema and validator to provide
an extensible foundation for dataset discovery, ingestion, and cataloging.

### What is included

- A JSON schema describing core dataset metadata fields.
- Python dataclasses that mirror the schema and provide validation helpers.
- A CLI to validate dataset metadata files and print a short summary.

### Try it locally

```bash
PYTHONPATH=src python -m open_data.validate examples/sample_dataset.json --summary
```

### Schema location

The schema lives in `schemas/dataset.schema.json` and can be used by other tools
that understand JSON Schema.
