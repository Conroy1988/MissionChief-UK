#!/usr/bin/env python3

from __future__ import annotations

import json
from datetime import date
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MAPPING_PATH = ROOT / "data" / "uk" / "official-prisoner-field-mappings.json"
MISSING = object()


def read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"{path.relative_to(ROOT)}: unable to read JSON: {exc}") from exc


def parse_iso_date(value: Any, label: str) -> None:
    if not isinstance(value, str):
        raise ValueError(f"{label} must be an ISO date")
    try:
        date.fromisoformat(value)
    except ValueError as exc:
        raise ValueError(f"{label} must be an ISO date") from exc


def validate_mapping_registry(document: Any) -> dict[str, dict[str, Any]]:
    if not isinstance(document, dict) or document.get("schema_version") != "1":
        raise ValueError("Official prisoner field mapping registry schema_version must be '1'")
    parse_iso_date(document.get("updated_at"), "Official prisoner field mapping registry updated_at")
    fields = document.get("fields")
    if not isinstance(fields, dict) or not fields:
        raise ValueError("Official prisoner field mapping registry fields must be a non-empty object")

    targets: set[str] = set()
    validated: dict[str, dict[str, Any]] = {}
    for official_path, mapping in fields.items():
        label = f"Official prisoner mapping {official_path}"
        if not isinstance(official_path, str) or not official_path.startswith("additional."):
            raise ValueError(f"{label} must target additional.*")
        if not isinstance(mapping, dict) or mapping.get("status") != "verified":
            raise ValueError(f"{label} must be a verified mapping object")
        target = mapping.get("canonical_target")
        if target not in {"prisoners.minimum", "prisoners.maximum"}:
            raise ValueError(f"{label} has unsupported canonical target {target!r}")
        if target in targets:
            raise ValueError(f"Canonical prisoner target {target} is mapped more than once")
        targets.add(str(target))
        if mapping.get("value_transform") != "identity-integer":
            raise ValueError(f"{label} value_transform must be identity-integer")
        parse_iso_date(mapping.get("checked_at"), f"{label} checked_at")
        sources = mapping.get("sources")
        if not isinstance(sources, list) or not sources or not all(isinstance(item, str) and item for item in sources):
            raise ValueError(f"{label} requires evidence sources")
        validated[official_path] = mapping

    audit = document.get("catalogue_audit")
    if not isinstance(audit, dict):
        raise ValueError("Official prisoner field mapping registry requires catalogue_audit")
    for key in ("official_records", "minimum_records", "maximum_records"):
        value = audit.get(key)
        if not isinstance(value, int) or isinstance(value, bool) or value < 0:
            raise ValueError(f"Official prisoner catalogue_audit.{key} must be a non-negative integer")
    return validated


def load_mapping_registry(path: Path = DEFAULT_MAPPING_PATH) -> dict[str, dict[str, Any]]:
    return validate_mapping_registry(read_json(path))


def nested_value(record: dict[str, Any], path: str) -> Any:
    root, field = path.split(".", 1)
    container = record.get(root)
    if not isinstance(container, dict) or field not in container:
        return MISSING
    return container[field]


def checked_integer(value: Any, label: str) -> int:
    if not isinstance(value, int) or isinstance(value, bool) or value < 0:
        raise ValueError(f"{label} must be a non-negative integer")
    return value


def build_expected_prisoners(
    official_record: dict[str, Any],
    mappings: dict[str, dict[str, Any]] | None = None,
) -> dict[str, int]:
    if mappings is None:
        mappings = load_mapping_registry()
    output: dict[str, int] = {}
    for official_path, mapping in mappings.items():
        value = nested_value(official_record, official_path)
        if value is MISSING:
            continue
        target = str(mapping["canonical_target"]).split(".", 1)[1]
        output[target] = checked_integer(value, f"Mission {official_record.get('id')} {official_path}")

    minimum = output.get("minimum")
    maximum = output.get("maximum")
    if minimum is not None and maximum is None:
        raise ValueError(f"Mission {official_record.get('id')} publishes a prisoner minimum without a maximum")
    if minimum is not None and maximum is not None and minimum > maximum:
        raise ValueError(
            f"Mission {official_record.get('id')} prisoner minimum {minimum} exceeds maximum {maximum}"
        )
    return output


def owned_additional_keys(
    mappings: dict[str, dict[str, Any]] | None = None,
) -> set[str]:
    if mappings is None:
        mappings = load_mapping_registry()
    return {path.split(".", 1)[1] for path in mappings}
