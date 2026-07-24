#!/usr/bin/env python3

from __future__ import annotations

import json
from datetime import date
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MAPPING_PATH = ROOT / "data" / "uk" / "official-personnel-education-mappings.json"
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


def validate_mapping_registry(document: Any) -> dict[str, Any]:
    if not isinstance(document, dict) or document.get("schema_version") != "1":
        raise ValueError("Official personnel education registry schema_version must be '1'")
    parse_iso_date(document.get("updated_at"), "Official personnel education registry updated_at")

    paths = document.get("paths")
    if not isinstance(paths, dict):
        raise ValueError("Official personnel education registry paths must be an object")
    expected_roots = {
        "required": "requirements.",
        "available": "prerequisites.",
        "captions": "additional.",
    }
    validated_paths: dict[str, str] = {}
    for field, root in expected_roots.items():
        value = paths.get(field)
        if not isinstance(value, str) or not value.startswith(root) or len(value) <= len(root):
            raise ValueError(f"Official personnel education path {field} must begin with {root}")
        validated_paths[field] = value
    if len(set(validated_paths.values())) != len(validated_paths):
        raise ValueError("Official personnel education paths must be unique")

    roles = document.get("roles")
    if not isinstance(roles, dict) or not roles:
        raise ValueError("Official personnel education registry roles must be a non-empty object")

    canonical_roles: set[str] = set()
    captions: set[str] = set()
    validated_roles: dict[str, dict[str, Any]] = {}
    for internal_key, mapping in roles.items():
        label = f"Official personnel education mapping {internal_key}"
        if not isinstance(internal_key, str) or not internal_key:
            raise ValueError("Official personnel education internal keys must be non-empty strings")
        if not isinstance(mapping, dict):
            raise ValueError(f"{label} must be an object")
        canonical_role = mapping.get("canonical_role")
        caption = mapping.get("official_caption")
        if not isinstance(canonical_role, str) or not canonical_role:
            raise ValueError(f"{label} requires canonical_role")
        if not isinstance(caption, str) or not caption:
            raise ValueError(f"{label} requires official_caption")
        if canonical_role in canonical_roles:
            raise ValueError(f"Canonical personnel role {canonical_role!r} is mapped more than once")
        if caption in captions:
            raise ValueError(f"Official personnel caption {caption!r} is mapped more than once")
        canonical_roles.add(canonical_role)
        captions.add(caption)
        sources = mapping.get("sources")
        if not isinstance(sources, list) or not sources or not all(isinstance(item, str) and item for item in sources):
            raise ValueError(f"{label} requires evidence sources")
        validated_roles[internal_key] = mapping

    return {
        "paths": validated_paths,
        "roles": validated_roles,
    }


def load_mapping_registry(path: Path = DEFAULT_MAPPING_PATH) -> dict[str, Any]:
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


def checked_object(value: Any, label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValueError(f"{label} must be an object")
    return value


def owned_paths(
    registry: dict[str, Any] | None = None,
) -> tuple[set[str], set[str], set[str], set[str]]:
    if registry is None:
        registry = load_mapping_registry()
    paths = registry["paths"]
    roles = registry["roles"]
    return (
        {str(paths["required"]).split(".", 1)[1]},
        {str(paths["available"]).split(".", 1)[1]},
        {str(paths["captions"]).split(".", 1)[1]},
        {str(mapping["canonical_role"]) for mapping in roles.values()},
    )


def translate_internal_roles(
    raw: Any,
    path: str,
    roles: dict[str, dict[str, Any]],
    mission_id: Any,
) -> dict[str, int]:
    if raw is MISSING:
        return {}
    values = checked_object(raw, f"Mission {mission_id} {path}")
    output: dict[str, int] = {}
    for internal_key, raw_quantity in values.items():
        mapping = roles.get(str(internal_key))
        if mapping is None:
            raise ValueError(f"Mission {mission_id} {path} contains unmapped role {internal_key!r}")
        quantity = checked_quantity(raw_quantity, f"Mission {mission_id} {path}.{internal_key}")
        if quantity == 0:
            continue
        canonical_role = str(mapping["canonical_role"])
        previous = output.get(canonical_role)
        if previous is not None and previous != quantity:
            raise ValueError(
                f"Mission {mission_id} {path} maps conflicting quantities for {canonical_role}: "
                f"{previous} and {quantity}"
            )
        output[canonical_role] = quantity
    return output


def translate_caption_roles(
    raw: Any,
    path: str,
    roles: dict[str, dict[str, Any]],
    mission_id: Any,
) -> dict[str, int]:
    if raw is MISSING:
        return {}
    values = checked_object(raw, f"Mission {mission_id} {path}")
    by_caption = {
        str(mapping["official_caption"]): str(mapping["canonical_role"])
        for mapping in roles.values()
    }
    output: dict[str, int] = {}
    for caption, raw_quantity in values.items():
        canonical_role = by_caption.get(str(caption))
        if canonical_role is None:
            raise ValueError(f"Mission {mission_id} {path} contains unmapped caption {caption!r}")
        quantity = checked_quantity(raw_quantity, f"Mission {mission_id} {path}.{caption}")
        if quantity == 0:
            continue
        previous = output.get(canonical_role)
        if previous is not None and previous != quantity:
            raise ValueError(
                f"Mission {mission_id} {path} repeats conflicting quantities for {canonical_role}: "
                f"{previous} and {quantity}"
            )
        output[canonical_role] = quantity
    return output


def requirement_items(values: dict[str, int]) -> list[dict[str, Any]]:
    return [
        {"role": role, "quantity": quantity}
        for role, quantity in sorted(values.items())
    ]


def build_expected_personnel_educations(
    official_record: dict[str, Any],
    registry: dict[str, Any] | None = None,
) -> dict[str, Any]:
    if registry is None:
        registry = load_mapping_registry()
    paths = registry["paths"]
    roles = registry["roles"]
    mission_id = official_record.get("id")

    raw_required = nested_value(official_record, str(paths["required"]))
    raw_available = nested_value(official_record, str(paths["available"]))
    raw_captions = nested_value(official_record, str(paths["captions"]))
    if raw_required is MISSING and raw_available is MISSING and raw_captions is MISSING:
        return {}

    required = translate_internal_roles(raw_required, str(paths["required"]), roles, mission_id)
    available = translate_internal_roles(raw_available, str(paths["available"]), roles, mission_id)
    captions = translate_caption_roles(raw_captions, str(paths["captions"]), roles, mission_id)

    if raw_captions is not MISSING and raw_required is MISSING:
        raise ValueError(
            f"Mission {mission_id} publishes {paths['captions']} without {paths['required']}"
        )
    if raw_captions is not MISSING and captions != required:
        raise ValueError(
            f"Mission {mission_id} personnel caption table differs from required personnel: "
            f"captions={captions!r}, required={required!r}"
        )

    output: dict[str, Any] = {}
    if required:
        output["required"] = requirement_items(required)
    if available:
        output["available"] = requirement_items(available)
    return output


def merge_personnel_educations(
    canonical_record: dict[str, Any],
    expected: dict[str, Any],
    roles: set[str],
) -> dict[str, Any]:
    output = dict(canonical_record)
    current = output.get("personnel")
    personnel = dict(current) if isinstance(current, dict) else {}

    for field in ("required", "available"):
        values = personnel.get(field, [])
        if values is None:
            values = []
        if not isinstance(values, list):
            raise ValueError(f"Canonical mission {canonical_record.get('id')} personnel.{field} must be an array")
        retained: list[dict[str, Any]] = []
        for item in values:
            if not isinstance(item, dict):
                raise ValueError(
                    f"Canonical mission {canonical_record.get('id')} personnel.{field} contains an invalid item"
                )
            if item.get("role") not in roles:
                retained.append(item)
        retained.extend(expected.get(field, []))
        if retained:
            personnel[field] = sorted(retained, key=lambda item: str(item.get("role")))
        else:
            personnel.pop(field, None)

    if personnel:
        output["personnel"] = personnel
    else:
        output.pop("personnel", None)
    return output


def extract_personnel_educations(
    canonical_record: dict[str, Any],
    roles: set[str],
) -> dict[str, Any]:
    personnel = canonical_record.get("personnel")
    if personnel is None:
        return {}
    if not isinstance(personnel, dict):
        raise ValueError(f"Canonical mission {canonical_record.get('id')} personnel must be an object")

    output: dict[str, Any] = {}
    for field in ("required", "available"):
        values = personnel.get(field, [])
        if not isinstance(values, list):
            raise ValueError(f"Canonical mission {canonical_record.get('id')} personnel.{field} must be an array")
        selected: list[dict[str, Any]] = []
        seen: set[str] = set()
        for item in values:
            if not isinstance(item, dict):
                raise ValueError(
                    f"Canonical mission {canonical_record.get('id')} personnel.{field} contains an invalid item"
                )
            role = item.get("role")
            if role not in roles:
                continue
            if role in seen:
                raise ValueError(
                    f"Canonical mission {canonical_record.get('id')} repeats personnel.{field} role {role}"
                )
            seen.add(str(role))
            quantity = item.get("quantity")
            if not isinstance(quantity, int) or isinstance(quantity, bool) or quantity < 1:
                raise ValueError(
                    f"Canonical mission {canonical_record.get('id')} has invalid personnel.{field} quantity"
                )
            selected.append({"role": str(role), "quantity": quantity})
        if selected:
            output[field] = sorted(selected, key=lambda item: item["role"])
    return output


def validate_promoted_personnel_educations(
    mission_id: str,
    decision: dict[str, Any],
    official_record: dict[str, Any],
    canonical_record: dict[str, Any],
    registry: dict[str, Any] | None = None,
) -> bool:
    if registry is None:
        registry = load_mapping_registry()
    _, _, _, roles = owned_paths(registry)
    expected = build_expected_personnel_educations(official_record, registry)
    actual = extract_personnel_educations(canonical_record, roles)
    strict = decision.get("strict_personnel_education_equivalence") is True
    if strict or expected or actual:
        if actual != expected:
            raise ValueError(
                f"Mission {mission_id} personnel education fields differ: "
                f"expected={expected!r}, canonical={actual!r}"
            )
        return True
    return False
