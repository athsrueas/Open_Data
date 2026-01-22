"""Barebones metadata helpers for public data tasks."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


class ValidationError(ValueError):
    """Raised when metadata fails validation checks."""


@dataclass(frozen=True)
class Resource:
    name: str
    access_url: str
    media_type: str


@dataclass(frozen=True)
class Dataset:
    id: str
    title: str
    description: str
    resources: list[Resource]


REQUIRED_FIELDS = {"id", "title", "description", "resources"}
REQUIRED_RESOURCE_FIELDS = {"name", "access_url", "media_type"}


def validate_dataset_payload(payload: dict) -> list[str]:
    """Validate the minimal required fields for a dataset payload."""
    errors: list[str] = []
    if not isinstance(payload, dict):
        return ["Payload must be an object."]

    missing = REQUIRED_FIELDS - payload.keys()
    if missing:
        errors.append(f"Missing required fields: {', '.join(sorted(missing))}.")

    resources = payload.get("resources")
    if resources is None:
        return errors

    if not isinstance(resources, list):
        errors.append("resources must be a list.")
        return errors

    if not resources:
        errors.append("resources must contain at least one entry.")
        return errors

    for idx, resource in enumerate(resources):
        if not isinstance(resource, dict):
            errors.append(f"resources[{idx}] must be an object.")
            continue
        missing_resource = REQUIRED_RESOURCE_FIELDS - resource.keys()
        if missing_resource:
            errors.append(
                f"resources[{idx}] missing fields: {', '.join(sorted(missing_resource))}."
            )

    return errors


def load_dataset(payload: dict) -> Dataset:
    """Create a Dataset from a payload, raising ValidationError on failure."""
    errors = validate_dataset_payload(payload)
    if errors:
        raise ValidationError("\n".join(errors))

    resources = [
        Resource(
            name=item["name"],
            access_url=item["access_url"],
            media_type=item["media_type"],
        )
        for item in payload["resources"]
    ]

    return Dataset(
        id=payload["id"],
        title=payload["title"],
        description=payload["description"],
        resources=resources,
    )


def summarize_dataset(dataset: Dataset) -> str:
    """Return a short summary string for quick inspection."""
    return f"{dataset.title} ({dataset.id}) | resources: {len(dataset.resources)}"


def validate_many(payloads: Iterable[dict]) -> list[str]:
    """Validate multiple payloads and return a flat list of errors."""
    errors: list[str] = []
    for index, payload in enumerate(payloads):
        payload_errors = validate_dataset_payload(payload)
        if payload_errors:
            errors.append(f"Dataset {index}:")
            errors.extend(f"  - {message}" for message in payload_errors)
    return errors
