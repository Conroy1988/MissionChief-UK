#!/usr/bin/env python3

from __future__ import annotations

import json
import math
from datetime import date
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MAPPING_PATH = ROOT / "data" / "uk" / "official-conditional-resource-mappings.json"
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
        raise ValueError("Official conditional resource registry schema_version must be '1'")
    parse_iso_date(document.get("updated_at"), "Official conditional resource registry updated_at")
    resources = document.get("resources")
    if not isinstance(resources, dict) or not resources:
        raise ValueError("Official conditional resource registry resources must be a non-empty object")

    validated: dict[str, dict[str, Any]] = {}
    official_paths: set[str] = set()
    canonical_resources: set[str] = set()
    for mapping_id, mapping in resources.items():
        label = f"Official conditional resource mapping {mapping_id}"
        if not isinstance(mapping_id, str) or not mapping_id:
            raise ValueError("Conditional resource mapping identifiers must be non-empty strings")
        if not isinstance(mapping, dict) or mapping.get("status") != "verified":
            raise ValueError(f"{label} must be a verified mapping object")
        canonical_resource = mapping.get("canonical_resource")
        if not isinstance(canonical_resource, str) or not canonical_resource:
            raise ValueError(f"{label} requires canonical_resource")
        if canonical_resource in canonical_resources:
            raise ValueError(f"Canonical conditional resource {canonical_resource!r} is mapped more than once")
        canonical_resources.add(canonical_resource)

        for field_name, root in (
            ("requirement_path", "requirements."),
            ("chance_path", "chances."),
            ("condition_flag_path", "additional."),
        ):
            path = mapping.get(field_name)
            if not isinstance(path, str) or not path.startswith(root) or len(path) <= len(root):
                raise ValueError(f"{label} {field_name} must begin with {root}")
            if path in official_paths:
                raise ValueError(f"{label} repeats official path {path}")
            official_paths.add(path)

        condition = mapping.get("condition")
        if not isinstance(condition, str) or not condition:
            raise ValueError(f"{label} requires condition")
        parse_iso_date(mapping.get("checked_at"), f"{label} checked_at")
        sources = mapping.get("sources")
        if not isinstance(sources, list) or not sources or not all(isinstance(item, str) and item for item in sources):
            raise ValueError(f"{label} requires evidence sources")
        validated[mapping_id] = mapping
    return validated


def load_mapping_registry(path: Path = DEFAULT_MAPPING_PATH) -> dict[str, dict[str, Any]]:
    return validate_mapping_registry(read_json(path))


def nested_value(record: dict[str, Any], path: str) -> Any:
    root, field = path.split(".", 1)
    container = record.get(root)
    if not isinstance(container, dict) or field not in container:
        return MISSING
    return container[field]


def checked_quantity(value: Any, label: str) -> int:
    if not isinstance(value, int) or isinstance(value, bool) or value < 0:
        raise ValueError(f"{label} must be a non-negative integer")
    return value


def checked_percent(value: Any, label: str) -> int:
    if not isinstance(value, int) or isinstance(value, bool) or not 0 <= value <= 100:
        raise ValueError(f"{label} must be an integer percentage from 0 to 100")
    return value


def owned_paths(
    mappings: dict[str, dict[str, Any]] | None = None,
) -> tuple[set[str], set[str], set[str], set[str]]:
    if mappings is None:
        mappings = load_mapping_registry()
    requirements: set[str] = set()
    chances: set[str] = set()
    additional: set[str] = set()
    resources: set[str] = set()
    for mapping in mappings.values():
        requirements.add(str(mapping["requirement_path"]).split(".", 1)[1])
        chances.add(str(mapping["chance_path"]).split(".", 1)[1])
        additional.add(str(mapping["condition_flag_path"]).split(".", 1)[1])
        resources.add(str(mapping["canonical_resource"]))
    return requirements, chances, additional, resources


def active_requirement_keys(
    official_record: dict[str, Any],
    mappings: dict[str, dict[str, Any]] | None = None,
) -> set[str]:
    if mappings is None:
        mappings = load_mapping_registry()
    result: set[str] = set()
    for mapping in mappings.values():
        raw_quantity = nested_value(official_record, str(mapping["requirement_path"]))
        raw_flag = nested_value(official_record, str(mapping["condition_flag_path"]))
        if raw_quantity is not MISSING and raw_flag is True:
            result.add(str(mapping["requirement_path"]).split(".", 1)[1])
    return result


def active_chance_keys(
    official_record: dict[str, Any],
    mappings: dict[str, dict[str, Any]] | None = None,
) -> set[str]:
    if mappings is None:
        mappings = load_mapping_registry()
    result: set[str] = set()
    for mapping in mappings.values():
        raw_quantity = nested_value(official_record, str(mapping["requirement_path"]))
        raw_flag = nested_value(official_record, str(mapping["condition_flag_path"]))
        raw_chance = nested_value(official_record, str(mapping["chance_path"]))
        if raw_quantity is not MISSING and raw_flag is True and raw_chance is not MISSING:
            result.add(str(mapping["chance_path"]).split(".", 1)[1])
    return result


def build_expected_conditionals(
    official_record: dict[str, Any],
    mappings: dict[str, dict[str, Any]] | None = None,
) -> list[dict[str, Any]]:
    if mappings is None:
        mappings = load_mapping_registry()
    mission_id = official_record.get("id")
    result: list[dict[str, Any]] = []

    for mapping in mappings.values():
        requirement_path = str(mapping["requirement_path"])
        chance_path = str(mapping["chance_path"])
        flag_path = str(mapping["condition_flag_path"])
        raw_quantity = nested_value(official_record, requirement_path)
        raw_chance = nested_value(official_record, chance_path)
        raw_flag = nested_value(official_record, flag_path)

        if raw_quantity is MISSING:
            if raw_chance is not MISSING or raw_flag is not MISSING:
                raise ValueError(
                    f"Mission {mission_id} publishes {chance_path} or {flag_path} without {requirement_path}"
                )
            continue

        quantity = checked_quantity(raw_quantity, f"Mission {mission_id} {requirement_path}")
        if raw_flag is MISSING or raw_flag is False:
            continue
        if raw_flag is not True:
            raise ValueError(f"Mission {mission_id} {flag_path} must be a boolean")
        percent = 100 if raw_chance is MISSING else checked_percent(raw_chance, f"Mission {mission_id} {chance_path}")
        if quantity == 0 or percent == 0:
            continue

        item: dict[str, Any] = {
            "resource": str(mapping["canonical_resource"]),
            "quantity": quantity,
            "condition": str(mapping["condition"]),
            "notes": [
                "The official UK mission states that this resource is required only when available."
            ],
        }
        if percent < 100:
            item["probability"] = percent / 100
        result.append(item)

    return sorted(result, key=lambda item: str(item["resource"]))


def extract_conditionals(
    canonical_record: dict[str, Any],
    resources: set[str],
) -> list[dict[str, Any]]:
    requirements = canonical_record.get("requirements")
    if not isinstance(requirements, dict):
        raise ValueError(f"Canonical mission {canonical_record.get('id')} requirements must be an object")
    values = requirements.get("conditional", [])
    if not isinstance(values, list):
        raise ValueError(f"Canonical mission {canonical_record.get('id')} requirements.conditional must be an array")

    selected: list[dict[str, Any]] = []
    seen: set[str] = set()
    for item in values:
        if not isinstance(item, dict):
            raise ValueError(f"Canonical mission {canonical_record.get('id')} contains an invalid conditional item")
        resource = item.get("resource")
        if resource not in resources:
            continue
        if resource in seen:
            raise ValueError(f"Canonical mission {canonical_record.get('id')} repeats conditional resource {resource}")
        seen.add(str(resource))
        quantity = item.get("quantity")
        condition = item.get("condition")
        probability = item.get("probability", MISSING)
        if not isinstance(quantity, int) or isinstance(quantity, bool) or quantity < 1:
            raise ValueError(f"Canonical mission {canonical_record.get('id')} has invalid conditional quantity")
        if not isinstance(condition, str) or not condition:
            raise ValueError(f"Canonical mission {canonical_record.get('id')} has invalid conditional condition")
        normalized: dict[str, Any] = {
            "resource": str(resource),
            "quantity": quantity,
            "condition": condition,
        }
        if probability is not MISSING:
            if (
                not isinstance(probability, (int, float))
                or isinstance(probability, bool)
                or not 0 < float(probability) < 1
            ):
                raise ValueError(f"Canonical mission {canonical_record.get('id')} has invalid conditional probability")
            normalized["probability"] = float(probability)
        selected.append(normalized)
    return sorted(selected, key=lambda item: item["resource"])


def conditionals_equal(actual: list[dict[str, Any]], expected: list[dict[str, Any]]) -> bool:
    def normalize(values: list[dict[str, Any]]) -> list[tuple[str, int, str, float | None]]:
        output: list[tuple[str, int, str, float | None]] = []
        for item in values:
            probability = item.get("probability")
            output.append(
                (
                    str(item["resource"]),
                    int(item["quantity"]),
                    str(item["condition"]),
                    None if probability is None else float(probability),
                )
            )
        return sorted(output)

    left = normalize(actual)
    right = normalize(expected)
    if len(left) != len(right):
        return False
    for actual_item, expected_item in zip(left, right):
        if actual_item[:3] != expected_item[:3]:
            return False
        actual_probability = actual_item[3]
        expected_probability = expected_item[3]
        if actual_probability is None or expected_probability is None:
            if actual_probability is not None or expected_probability is not None:
                return False
        elif not math.isclose(actual_probability, expected_probability, abs_tol=1e-9):
            return False
    return True


def validate_promoted_conditionals(
    mission_id: str,
    decision: dict[str, Any],
    official_record: dict[str, Any],
    canonical_record: dict[str, Any],
    mappings: dict[str, dict[str, Any]] | None = None,
) -> bool:
    if mappings is None:
        mappings = load_mapping_registry()
    _, _, _, resources = owned_paths(mappings)
    expected = build_expected_conditionals(official_record, mappings)
    actual = extract_conditionals(canonical_record, resources)
    strict = decision.get("strict_conditional_equivalence") is True
    if strict or expected or actual:
        if not conditionals_equal(actual, expected):
            raise ValueError(
                f"Mission {mission_id} conditional resources differ: expected={expected!r}, canonical={actual!r}"
            )
        return True
    return False
