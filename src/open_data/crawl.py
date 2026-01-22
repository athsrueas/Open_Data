"""
Interactive crawl job for public data catalog items defined in data-sources.json.

Intended to be run directly:
    python src/open_data/crawl.py
"""

from __future__ import annotations

import datetime as dt
import json
import sys
from pathlib import Path
from urllib.parse import urljoin, urldefrag, urlparse

import requests
from bs4 import BeautifulSoup

# Local sibling import; this script is intended to be run directly
from tasks import load_json, write_json, write_csv


DATA_SOURCES_PATH = Path(__file__).parent / "data-sources.json"


def choose_item(items: list[dict]) -> dict:
    """Prompt the user to select an item from the catalog."""
    print("\nAvailable catalog items:\n")

    for idx, item in enumerate(items, start=1):
        domains = ", ".join(item.get("domains", []))
        print(f"{idx}. {item.get('name')} ({domains})")

    choice = input("\nSelect a project number to crawl: ").strip()

    try:
        index = int(choice) - 1
        return items[index]
    except (ValueError, IndexError):
        print("Invalid selection.")
        sys.exit(1)


def fetch_html(url: str) -> tuple[str | None, str | None]:
    headers = {
        "User-Agent": "open-data-crawler/1.0 (+purpose: public data discovery)",
        "Accept": "text/html",
    }
    try:
        resp = requests.get(url, headers=headers, timeout=30)
        resp.raise_for_status()
        return resp.text, None
    except requests.RequestException as exc:
        return None, str(exc)


def extract_links(html: str) -> list[dict[str, str]]:
    soup = BeautifulSoup(html, "lxml")
    return [
        {"text": a.get_text(" ", strip=True), "href": a.get("href", "")}
        for a in soup.find_all("a", href=True)
    ]


def normalize_links(links: list[dict], base_url: str) -> list[dict[str, str]]:
    seen = set()
    normalized = []

    for link in links:
        text = link["text"].strip()
        href = link["href"].strip()
        if not text or not href:
            continue

        url = urljoin(base_url, href)
        url, _ = urldefrag(url)

        if urlparse(url).scheme not in ("http", "https"):
            continue

        key = (text, url)
        if key in seen:
            continue

        seen.add(key)
        normalized.append({"text": text, "url": url})

    return normalized


def filter_links(links: list[dict[str, str]]) -> list[dict[str, str]]:
    """Light heuristic filter for data/program-related links."""
    keywords = ("data", "dataset", "api", "download", "stat", "statistics", "program")
    return [
        link
        for link in links
        if any(k in f"{link['text']} {link['url']}".lower() for k in keywords)
    ]


def slugify(name: str) -> str:
    return (
        name.lower()
        .replace(" ", "_")
        .replace("-", "_")
        .encode("ascii", "ignore")
        .decode("ascii")
    )


def run() -> None:
    catalog = load_json(DATA_SOURCES_PATH)

    items = catalog.get("items", [])

    if not items:
        print("No items found in data-sources.json")
        return

    item = choose_item(items)

    html, error = fetch_html(item["url"])
    links = []
    filtered = []

    if html:
        links = normalize_links(extract_links(html), item["url"])
        filtered = filter_links(links)

    payload = {
        "item": item,
        "fetched_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "link_count": len(links),
        "filtered_link_count": len(filtered),
        "links": filtered,
        "error": error,
    }

    output_dir = Path("outputs") / slugify(item["name"])
    write_json(output_dir / "crawl.json", payload)
    write_csv(output_dir / "links.csv", filtered, ["text", "url"])

    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    run()
