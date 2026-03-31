"""Serve the education viewer from the repository root."""

from __future__ import annotations

import argparse
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path


ROOT = Path(__file__).resolve().parent
DEFAULT_DIRECTORY = ROOT / "viewer" / "educational_inequality_map"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Serve the Educational Inequality Map viewer."
    )
    parser.add_argument(
        "port",
        nargs="?",
        type=int,
        default=8787,
        help="Port to bind to. Defaults to 8787.",
    )
    parser.add_argument(
        "--host",
        default="127.0.0.1",
        help="Host interface to bind to. Defaults to 127.0.0.1.",
    )
    parser.add_argument(
        "--directory",
        type=Path,
        default=DEFAULT_DIRECTORY,
        help="Directory to serve. Defaults to the viewer folder.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    directory = args.directory.resolve()
    if not directory.exists():
        raise SystemExit(f"Viewer directory does not exist: {directory}")

    handler = partial(SimpleHTTPRequestHandler, directory=str(directory))
    with ThreadingHTTPServer((args.host, args.port), handler) as httpd:
        print(
            f"Serving {directory} at http://{args.host}:{args.port}",
            flush=True,
        )
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down server.", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
