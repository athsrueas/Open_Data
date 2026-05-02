from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.open_data.us_education_initiatives import VIEWER_DATA_JS_PATH, build_dataset


def main() -> None:
    payload = build_dataset()
    serialized = json.dumps(payload, indent=2)
    VIEWER_DATA_JS_PATH.parent.mkdir(parents=True, exist_ok=True)
    VIEWER_DATA_JS_PATH.write_text(
        "window.US_EDUCATION_INITIATIVES_DATA = " + serialized + ";\n",
        encoding="utf-8",
    )
    print(f"Wrote {VIEWER_DATA_JS_PATH}")


if __name__ == "__main__":
    main()
