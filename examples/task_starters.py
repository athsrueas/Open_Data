"""Quick starters for discrete public data tasks."""

from pathlib import Path

from open_data.tasks import (
    audit_missing_fields,
    build_index_rows,
    load_json,
    normalize_metadata,
    write_csv,
    write_json,
)


def main() -> None:
    dataset = load_json(Path("examples/sample_dataset.json"))

    normalized = normalize_metadata(dataset)
    write_json(Path("examples/output/normalized_metadata.json"), normalized)

    index_rows = build_index_rows([dataset])
    write_csv(
        Path("examples/output/dataset_index.csv"),
        index_rows,
        fieldnames=["id", "title", "license", "resource_count"],
    )

    audit_rows = audit_missing_fields([dataset], ["license", "publisher", "landing_page"])
    write_csv(
        Path("examples/output/missing_fields.csv"),
        audit_rows,
        fieldnames=["id", "missing_fields"],
    )


if __name__ == "__main__":
    main()
