from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.open_data.us_education_initiatives import (
    OUTPUT_DIR,
    VIEWER_DATA_JS_PATH,
    build_dataset,
    build_flat_rows,
    build_state_flat_rows,
    build_subspace_catalog,
    write_csv,
    write_json,
)


def main() -> None:
    dataset = build_dataset()
    catalog = build_subspace_catalog(dataset)
    flat_rows = build_flat_rows(dataset)
    state_flat_rows = build_state_flat_rows(dataset)

    write_json(OUTPUT_DIR / "initiatives.bundle.json", dataset)
    write_json(OUTPUT_DIR / "catalog.json", catalog)
    write_csv(OUTPUT_DIR / "initiatives.flat.csv", flat_rows)
    write_csv(OUTPUT_DIR / "states.flat.csv", state_flat_rows)

    VIEWER_DATA_JS_PATH.parent.mkdir(parents=True, exist_ok=True)
    VIEWER_DATA_JS_PATH.write_text(
        "window.US_EDUCATION_INITIATIVES_DATA = " + json.dumps(dataset, indent=2) + ";\n",
        encoding="utf-8",
    )

    print(f"Wrote {OUTPUT_DIR / 'initiatives.bundle.json'}")
    print(f"Wrote {OUTPUT_DIR / 'initiatives.flat.csv'}")
    print(f"Wrote {OUTPUT_DIR / 'states.flat.csv'}")
    print(f"Wrote {OUTPUT_DIR / 'catalog.json'}")
    print(f"Wrote {VIEWER_DATA_JS_PATH}")


if __name__ == "__main__":
    main()
