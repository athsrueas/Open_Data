"""Core metadata models and validation helpers for Open Data catalogs."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable, List, Optional
from urllib.parse import urlparse


class ValidationError(ValueError):
    """Raised when metadata fails validation checks."""


@dataclass(frozen=True)
class Publisher:
    name: str
    url: Optional[str] = None
    email: Optional[str] = None


@dataclass(frozen=True)
class Resource:
    name: str
    access_url: str
    media_type: str
    description: Optional[str] = None
    download_url: Optional[str] = None
    size_bytes: Optional[int] = None


@dataclass(frozen=True)
class Dataset:
    id: str
    title: str
    description: str
    publisher: Publisher
    license: str
    resources: List[Resource]
    keywords: List[str] = field(default_factory=list)
    themes: List[str] = field(default_factory=list)
    issued: Optional[str] = None
    modified: Optional[str] = None
    landing_page: Optional[str] = None
    spatial: Optional[str] = None
    temporal: Optional[str] = None
    provenance_source: Optional[str] = None
    provenance_retrieved_at: Optional[str] = None


REQUIRED_FIELDS = {"id", "title", "description", "publisher", "license", "resources"}
REQUIRED_RESOURCE_FIELDS = {"name", "access_url", "media_type"}


def _is_valid_url(value: str) -> bool:
    parsed = urlparse(value)
    return bool(parsed.scheme and parsed.netloc)


def _ensure(condition: bool, message: str, errors: list[str]) -> None:
    if not condition:
        errors.append(message)


def validate_dataset_payload(payload: dict) -> list[str]:
    errors: list[str] = []
    _ensure(isinstance(payload, dict), "Payload must be an object.", errors)
    if errors:
        return errors

    missing = REQUIRED_FIELDS - payload.keys()
    if missing:
        errors.append(f"Missing required fields: {', '.join(sorted(missing))}.")

    if "resources" in payload:
        resources = payload["resources"]
        _ensure(isinstance(resources, list), "resources must be a list.", errors)
        if isinstance(resources, list):
            _ensure(len(resources) > 0, "resources must contain at least one entry.", errors)
            for idx, resource in enumerate(resources):
                if not isinstance(resource, dict):
                    errors.append(f"resources[{idx}] must be an object.")
                    continue
                missing_resource = REQUIRED_RESOURCE_FIELDS - resource.keys()
                if missing_resource:
                    errors.append(
                        f"resources[{idx}] missing fields: {', '.join(sorted(missing_resource))}."
                    )
                access_url = resource.get("access_url")
                if isinstance(access_url, str):
                    _ensure(
                        _is_valid_url(access_url),
                        f"resources[{idx}].access_url must be a valid URL.",
                        errors,
                    )

                download_url = resource.get("download_url")
                if isinstance(download_url, str):
                    _ensure(
                        _is_valid_url(download_url),
                        f"resources[{idx}].download_url must be a valid URL.",
                        errors,
                    )

                size_bytes = resource.get("size_bytes")
                if size_bytes is not None:
                    _ensure(
                        isinstance(size_bytes, int) and size_bytes >= 0,
                        f"resources[{idx}].size_bytes must be a non-negative integer.",
                        errors,
                    )

    publisher = payload.get("publisher")
    if isinstance(publisher, dict):
        name = publisher.get("name")
        _ensure(isinstance(name, str) and name.strip(), "publisher.name is required.", errors)
        url = publisher.get("url")
        if isinstance(url, str):
            _ensure(_is_valid_url(url), "publisher.url must be a valid URL.", errors)
    elif "publisher" in payload:
        errors.append("publisher must be an object.")

    landing_page = payload.get("landing_page")
    if isinstance(landing_page, str):
        _ensure(_is_valid_url(landing_page), "landing_page must be a valid URL.", errors)

    return errors


def load_dataset(payload: dict) -> Dataset:
    errors = validate_dataset_payload(payload)
    if errors:
        raise ValidationError("\n".join(errors))

    publisher_payload = payload["publisher"]
    publisher = Publisher(
        name=publisher_payload["name"],
        url=publisher_payload.get("url"),
        email=publisher_payload.get("email"),
    )

    resources = [
        Resource(
            name=item["name"],
            description=item.get("description"),
            access_url=item["access_url"],
            download_url=item.get("download_url"),
            media_type=item["media_type"],
            size_bytes=item.get("size_bytes"),
        )
        for item in payload["resources"]
    ]

    provenance = payload.get("provenance") or {}

    return Dataset(
        id=payload["id"],
        title=payload["title"],
        description=payload["description"],
        publisher=publisher,
        license=payload["license"],
        resources=resources,
        keywords=list(payload.get("keywords", [])),
        themes=list(payload.get("themes", [])),
        issued=payload.get("issued"),
        modified=payload.get("modified"),
        landing_page=payload.get("landing_page"),
        spatial=payload.get("spatial"),
        temporal=payload.get("temporal"),
        provenance_source=provenance.get("source"),
        provenance_retrieved_at=provenance.get("retrieved_at"),
    )


def summarize_dataset(dataset: Dataset) -> str:
    resource_count = len(dataset.resources)
    keywords = ", ".join(dataset.keywords) if dataset.keywords else "none"
    themes = ", ".join(dataset.themes) if dataset.themes else "none"
    return (
        f"{dataset.title} ({dataset.id})\n"
        f"Publisher: {dataset.publisher.name}\n"
        f"Resources: {resource_count}\n"
        f"Keywords: {keywords}\n"
        f"Themes: {themes}"
    )


def validate_many(payloads: Iterable[dict]) -> list[str]:
    errors: list[str] = []
    for index, payload in enumerate(payloads):
        payload_errors = validate_dataset_payload(payload)
        if payload_errors:
            errors.append(f"Dataset {index}:")
            errors.extend(f"  - {message}" for message in payload_errors)
    return errors
