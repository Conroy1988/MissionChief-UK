#!/usr/bin/env python3

from __future__ import annotations

import json
from datetime import date
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MAPPING_PATH = ROOT / "data" / "uk" / "official-patient-field-mappings.json"

MISSING = object()
ALLOWED_TRANSFORMS = {
    "identity-integer",
    "identity-string-array",
    "identity-string-array-preserve-duplicates",
    "identity-integer-array",
    "identity-string",
    "percent-to-probability",
    "identity-boolean",
}


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
        raise ValueError("Official patient field mapping registry schema_version must be '1'")
    parse_iso_date(document.get("updated_at"), "Official patient field mapping registry updated_at")

    fields = document.get("fields")
    if not isinstance(fields, dict) or not fields:
        raise ValueError("Official patient field mapping registry fields must be a non-empty object")

    targets: set[str] = set()
    validated: dict[str, dict[str, Any]] = {}
    for official_path, mapping in fields.items():
        label = f"Official patient mapping {official_path}"
        if not isinstance(official_path, str) or "." not in official_path:
            raise ValueError(f"{label} has an invalid source path")
        root, field = official_path.split(".", 1)
        if root not in {"additional", "chances"} or not field:
            raise ValueError(f"{label} must target additional.* or chances.*")
        if not isinstance(mapping, dict) or mapping.get("status") != "verified":
            raise ValueError(f"{label} must be a verified mapping object")
        target = mapping.get("canonical_target")
        if not isinstance(target, str) or not target.startswith("patients."):
            raise ValueError(f"{label} canonical_target must begin with patients.")
        if target in targets:
            raise ValueError(f"Patient canonical target {target} is mapped more than once")
        targets.add(target)
        transform = mapping.get("value_transform")
        if transform not in ALLOWED_TRANSFORMS:
            raise ValueError(f"{label} uses unsupported transform {transform!r}")
        parse_iso_date(mapping.get("checked_at"), f"{label} checked_at")
        sources = mapping.get("sources")
        if not isinstance(sources, list) or not sources or not all(isinstance(item, str) and item for item in sources):
            raise ValueError(f"{label} requires evidence sources")
        validated[official_path] = mapping

    audit = document.get("catalogue_audit")
    if not isinstance(audit, dict):
        raise ValueError("Official patient field mapping registry requires catalogue_audit")
    for key in (
        "official_records",
        "patient_records",
        "distinct_field_shapes",
        "maximum_without_minimum",
        "minimum_without_maximum",
    ):
        value = audit.get(key)
        if not isinstance(value, int) or isinstance(value, bool) or value < 0:
            raise ValueError(f"Official patient catalogue_audit.{key} must be a non-negative integer")
    if audit["minimum_without_maximum"] != 0:
        raise ValueError("Official patient catalogue audit must not contain a minimum without a maximum")
    return validated


def load_mapping_registry(path: Path = DEFAULT_MAPPING_PATH) -> dict[str, dict[str, Any]]:
    return validate_mapping_registry(read_json(path))


def nested_value(record: dict[str, Any], path: str) -> Any:
    root, field = path.split(".", 1)
    container = record.get(root)
    if not isinstance(container, dict) or field not in container:
        return MISSING
    return container[field]


def validated_string_array(value: Any, label: str) -> list[str]:
    if not isinstance(value, list) or not all(isinstance(item, str) and item for item in value):
        raise ValueError(f"{label} must be an array of non-empty strings")
    return list(value)


def transform_value(value: Any, transform: str, label: str) -> Any:
    if transform == "identity-integer":
        if not isinstance(value, int) or isinstance(value, bool) or value < 0:
            raise ValueError(f"{label} must be a non-negative integer")
        return value
    if transform == "identity-string-array":
        output = validated_string_array(value, label)
        if len(output) != len(set(output)):
            raise ValueError(f"{label} must not contain duplicate values")
        return output
    if transform == "identity-string-array-preserve-duplicates":
        return validated_string_array(value, label)
    if transform == "identity-integer-array":
        if (
            not isinstance(value, list)
            or not all(isinstance(item, int) and not isinstance(item, bool) and item >= 0 for item in value)
        ):
            raise ValueError(f"{label} must be an array of non-negative integers")
        if len(value) != len(set(value)):
            raise ValueError(f"{label} must not contain duplicate values")
        return list(value)
    if transform == "identity-string":
        if not isinstance(value, str) or not value:
            raise ValueError(f"{label} must be a non-empty string")
        return value
    if transform == "percent-to-probability":
        if not isinstance(value, int) or isinstance(value, bool) or not 0 <= value <= 100:
            raise ValueError(f"{label} must be an integer percentage from 0 to 100")
        return value / 100
    if transform == "identity-boolean":
        if not isinstance(value, bool):
            raise ValueError(f"{label} must be a boolean")
        return value
    raise ValueError(f"{label} uses unsupported transform {transform!r}")


def build_expected_patient(
    official_record: dict[str, Any],
    mappings: dict[str, dict[str, Any]] | None = None,
) -> dict[str, Any]:
    if mappings is None:
        mappings = load_mapping_registry()

    expected: dict[str, Any] = {}
    for official_path, mapping in mappings.items():
        value = nested_value(official_record, official_path)
        if value is MISSING:
            continue
        transformed = transform_value(
            value,
            str(mapping["value_transform"]),
            f"Mission {official_record.get('id')} {official_path}",
        )
        target = str(mapping["canonical_target"]).split(".", 1)[1]
        expected[target] = transformed

    minimum = expected.get("minimum")
    maximum = expected.get("maximum")
    if minimum is not None and maximum is None:
        raise ValueError(f"Mission {official_record.get('id')} publishes a patient minimum without a maximum")
    if minimum is not None and maximum is not None and minimum > maximum:
        raise ValueError(
            f"Mission {official_record.get('id')} publishes patient minimum {minimum} above maximum {maximum}"
        )

    captions = expected.get("specializations")
    identifiers = expected.get("specialization_ids")
    if captions is not None and identifiers is not None and len(captions) != len(identifiers):
        raise ValueError(
            f"Mission {official_record.get('id')} patient specialization captions and IDs differ in length"
        )
    return expected


def patient_owned_paths(
    mappings: dict[str, dict[str, Any]] | None = None,
) -> tuple[set[str], set[str]]:
    if mappings is None:
        mappings = load_mapping_registry()
    additional: set[str] = set()
    chances: set[str] = set()
    for path in mappings:
        root, field = path.split(".", 1)
        if root == "additional":
            additional.add(field)
        else:
            chances.add(field)
    return additional, chances
