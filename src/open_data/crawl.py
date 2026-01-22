"""
Interactive crawl job for public data projects defined in data-sources.json.
"""

from __future__ import annotations

import datetime as dt
import json
import sys
from pathlib import Path
from urllib.parse import urljoin, urldefrag, urlparse

import requests
from bs4 import BeautifulSoup

from open_data.tasks import load_json, write_json, write_csv


DATA_SOURCES_PATH = Path("src/open_data/data-sources.json")


def choose_project(projects: list[dict]) -> dict:
    """Prompt the user to select a project to crawl."""
    print("\nAvailable projects:\n")

    for idx, project in enumerate(projects, start=1):
        domains = ", ".join(project.get("domains", []))
        print(f"{idx}. {project['name']} ({domains})")

    choice = input("\nSelect a project number to crawl: ").strip()

    try:
        index = int(choice) - 1
        return projects[index]
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
    keywords = ("data", "dataset", "api", "download", "stat", "program")
    return [
        link
        for link in links
        if any(k in f"{link['text']} {link['url']}".lower() for k in keywords)
    ]


def slugify(name: str) -> str:
    return name.lower().replace(" ", "_").replace("-", "_")


def run() -> int:
    sources = load_json(DATA_SOURCES_PATH)
    projects = sources.get("projects", [])

    if not projects:
        print("No projects found in data-sources.json")
        return 1

    project = choose_project(projects)

    html, error = fetch_html(project["url"])
    links = []
    filtered = []

    if html:
        links = normalize_links(extract_links(html), project["url"])
        filtered = filter_links(links)

    payload = {
        "project": project,
        "fetched_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "link_count": len(links),
        "filtered_link_count": len(filtered),
        "links": filtered,
        "error": error,
    }

    output_dir = Path("outputs") / slugify(project["name"])
    write_json(output_dir / "crawl.json", payload)
    write_csv(output_dir / "links.csv", filtered, ["text", "url"])

    print(json.dumps(payload, indent=2))
    return 1 if error else 0


if __name__ == "__main__":
    raise SystemExit(run())
