#!/usr/bin/env python3

from __future__ import annotations

import json
from datetime import date
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MAPPING_PATH = ROOT / "data" / "uk" / "official-personnel-field-mappings.json"
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
        raise ValueError("Official personnel field mapping registry schema_version must be '1'")
    parse_iso_date(document.get("updated_at"), "Official personnel field mapping registry updated_at")
    roles = document.get("roles")
    if not isinstance(roles, dict) or not roles:
        raise ValueError("Official personnel field mapping registry roles must be a non-empty object")

    validated: dict[str, dict[str, Any]] = {}
    official_paths: set[str] = set()
    canonical_roles: set[str] = set()
    for mapping_id, mapping in roles.items():
        label = f"Official personnel mapping {mapping_id}"
        if not isinstance(mapping_id, str) or not mapping_id:
            raise ValueError("Official personnel mapping identifiers must be non-empty strings")
        if not isinstance(mapping, dict) or mapping.get("status") != "verified":
            raise ValueError(f"{label} must be a verified mapping object")
        role = mapping.get("canonical_role")
        if not isinstance(role, str) or not role:
            raise ValueError(f"{label} requires canonical_role")
        if role in canonical_roles:
            raise ValueError(f"Canonical personnel role {role!r} is mapped more than once")
        canonical_roles.add(role)
        requirement_path = mapping.get("requirement_path")
        chance_path = mapping.get("chance_path")
        if not isinstance(requirement_path, str) or not requirement_path.startswith("requirements."):
            raise ValueError(f"{label} requirement_path must begin with requirements.")
        if not isinstance(chance_path, str) or not chance_path.startswith("chances."):
            raise ValueError(f"{label} chance_path must begin with chances.")
        if requirement_path in official_paths or chance_path in official_paths:
            raise ValueError(f"{label} repeats an official personnel path")
        official_paths.update({requirement_path, chance_path})
        if mapping.get("canonical_target") != "personnel.chance-aware":
            raise ValueError(f"{label} canonical_target must be personnel.chance-aware")
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


def build_expected_personnel(
    official_record: dict[str, Any],
    mappings: dict[str, dict[str, Any]] | None = None,
) -> dict[str, Any]:
    if mappings is None:
        mappings = load_mapping_registry()
    required: list[dict[str, Any]] = []
    probabilistic: list[dict[str, Any]] = []
    mission_id = official_record.get("id")

    for mapping in mappings.values():
        requirement_path = str(mapping["requirement_path"])
        raw_quantity = nested_value(official_record, requirement_path)
        if raw_quantity is MISSING:
            raw_chance = nested_value(official_record, str(mapping["chance_path"]))
            if raw_chance is not MISSING:
                raise ValueError(
                    f"Mission {mission_id} publishes {mapping['chance_path']} without {requirement_path}"
                )
            continue
        quantity = checked_quantity(raw_quantity, f"Mission {mission_id} {requirement_path}")
        raw_chance = nested_value(official_record, str(mapping["chance_path"]))
        percent = 100 if raw_chance is MISSING else checked_percent(
            raw_chance,
            f"Mission {mission_id} {mapping['chance_path']}",
        )
        if quantity == 0 or percent == 0:
            continue
        role = str(mapping["canonical_role"])
        if percent == 100:
            required.append({"role": role, "quantity": quantity})
        else:
            probabilistic.append({"role": role, "quantity": quantity, "probability": percent / 100})

    output: dict[str, Any] = {}
    if required:
        output["required"] = sorted(required, key=lambda item: item["role"])
    if probabilistic:
        output["probabilistic"] = sorted(probabilistic, key=lambda item: item["role"])
    return output


def owned_paths(
    mappings: dict[str, dict[str, Any]] | None = None,
) -> tuple[set[str], set[str], set[str]]:
    if mappings is None:
        mappings = load_mapping_registry()
    requirements: set[str] = set()
    chances: set[str] = set()
    roles: set[str] = set()
    for mapping in mappings.values():
        requirements.add(str(mapping["requirement_path"]).split(".", 1)[1])
        chances.add(str(mapping["chance_path"]).split(".", 1)[1])
        roles.add(str(mapping["canonical_role"]))
    return requirements, chances, roles


def merge_mapped_personnel(
    canonical_record: dict[str, Any],
    expected: dict[str, Any],
    roles: set[str],
) -> dict[str, Any]:
    output = dict(canonical_record)
    current = output.get("personnel")
    personnel = dict(current) if isinstance(current, dict) else {}

    for field in ("required", "probabilistic"):
        values = personnel.get(field, [])
        if values is None:
            values = []
        if not isinstance(values, list):
            raise ValueError(f"Canonical mission {canonical_record.get('id')} personnel.{field} must be an array")
        retained: list[Any] = []
        for item in values:
            if not isinstance(item, dict):
                raise ValueError(f"Canonical mission {canonical_record.get('id')} personnel.{field} contains an invalid item")
            if item.get("role") not in roles:
                retained.append(item)
        retained.extend(expected.get(field, []))
        if retained:
            personnel[field] = retained
        else:
            personnel.pop(field, None)

    if personnel:
        output["personnel"] = personnel
    else:
        output.pop("personnel", None)
    return output


def extract_mapped_personnel(
    canonical_record: dict[str, Any],
    roles: set[str],
) -> dict[str, Any]:
    personnel = canonical_record.get("personnel")
    if personnel is None:
        return {}
    if not isinstance(personnel, dict):
        raise ValueError(f"Canonical mission {canonical_record.get('id')} personnel must be an object")
    output: dict[str, Any] = {}
    for field in ("required", "probabilistic"):
        values = personnel.get(field, [])
        if not isinstance(values, list):
            raise ValueError(f"Canonical mission {canonical_record.get('id')} personnel.{field} must be an array")
        selected: list[dict[str, Any]] = []
        seen: set[str] = set()
        for item in values:
            if not isinstance(item, dict):
                raise ValueError(f"Canonical mission {canonical_record.get('id')} personnel.{field} contains an invalid item")
            role = item.get("role")
            if role not in roles:
                continue
            if role in seen:
                raise ValueError(f"Canonical mission {canonical_record.get('id')} repeats mapped personnel role {role}")
            seen.add(str(role))
            selected.append(item)
        if selected:
            output[field] = sorted(selected, key=lambda item: str(item.get("role")))
    return output
