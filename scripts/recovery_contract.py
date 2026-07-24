#!/usr/bin/env python3

from __future__ import annotations

import json
from datetime import date
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MAPPING_PATH = ROOT / "data" / "uk" / "official-recovery-field-mappings.json"
MISSING = object()
ALLOWED_ASSET_TYPES = {"car", "truck", "vehicle"}


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
        raise ValueError("Official recovery field mapping registry schema_version must be '1'")
    parse_iso_date(document.get("updated_at"), "Official recovery field mapping registry updated_at")
    assets = document.get("assets")
    if not isinstance(assets, dict) or not assets:
        raise ValueError("Official recovery field mapping registry assets must be a non-empty object")

    paths: set[str] = set()
    asset_types: set[str] = set()
    validated: dict[str, dict[str, Any]] = {}
    for mapping_id, mapping in assets.items():
        label = f"Official recovery mapping {mapping_id}"
        if not isinstance(mapping_id, str) or not mapping_id:
            raise ValueError("Recovery mapping identifiers must be non-empty strings")
        if not isinstance(mapping, dict):
            raise ValueError(f"{label} must be an object")
        minimum_path = mapping.get("minimum_path")
        maximum_path = mapping.get("maximum_path")
        for field_name, path in (("minimum_path", minimum_path), ("maximum_path", maximum_path)):
            if not isinstance(path, str) or not path.startswith("additional.") or len(path) <= len("additional."):
                raise ValueError(f"{label} {field_name} must begin with additional.")
            if path in paths:
                raise ValueError(f"{label} repeats official path {path}")
            paths.add(path)
        if minimum_path == maximum_path:
            raise ValueError(f"{label} minimum and maximum paths must differ")
        asset_type = mapping.get("canonical_asset_type")
        if asset_type not in ALLOWED_ASSET_TYPES:
            raise ValueError(f"{label} has unsupported canonical_asset_type {asset_type!r}")
        if asset_type in asset_types:
            raise ValueError(f"Canonical recovery asset type {asset_type!r} is mapped more than once")
        asset_types.add(str(asset_type))
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


def checked_integer(value: Any, label: str) -> int:
    if not isinstance(value, int) or isinstance(value, bool) or value < 0:
        raise ValueError(f"{label} must be a non-negative integer")
    return value


def owned_additional_keys(
    mappings: dict[str, dict[str, Any]] | None = None,
) -> set[str]:
    if mappings is None:
        mappings = load_mapping_registry()
    result: set[str] = set()
    for mapping in mappings.values():
        result.add(str(mapping["minimum_path"]).split(".", 1)[1])
        result.add(str(mapping["maximum_path"]).split(".", 1)[1])
    return result


def mapped_asset_types(
    mappings: dict[str, dict[str, Any]] | None = None,
) -> set[str]:
    if mappings is None:
        mappings = load_mapping_registry()
    return {str(mapping["canonical_asset_type"]) for mapping in mappings.values()}


def build_expected_recovery(
    official_record: dict[str, Any],
    mappings: dict[str, dict[str, Any]] | None = None,
) -> dict[str, Any]:
    if mappings is None:
        mappings = load_mapping_registry()
    mission_id = official_record.get("id")
    assets: list[dict[str, Any]] = []

    for mapping in mappings.values():
        minimum_path = str(mapping["minimum_path"])
        maximum_path = str(mapping["maximum_path"])
        raw_minimum = nested_value(official_record, minimum_path)
        raw_maximum = nested_value(official_record, maximum_path)
        if raw_minimum is MISSING and raw_maximum is MISSING:
            continue
        if raw_minimum is MISSING or raw_maximum is MISSING:
            missing = minimum_path if raw_minimum is MISSING else maximum_path
            raise ValueError(
                f"Mission {mission_id} recovery range is incomplete; missing {missing}"
            )
        minimum = checked_integer(raw_minimum, f"Mission {mission_id} {minimum_path}")
        maximum = checked_integer(raw_maximum, f"Mission {mission_id} {maximum_path}")
        if minimum > maximum:
            raise ValueError(
                f"Mission {mission_id} recovery minimum {minimum} exceeds maximum {maximum} "
                f"for {mapping['canonical_asset_type']}"
            )
        assets.append(
            {
                "asset_type": str(mapping["canonical_asset_type"]),
                "minimum": minimum,
                "maximum": maximum,
                "notes": [
                    "Published towing range; this is an operational outcome, not a dispatched emergency-resource requirement."
                ],
            }
        )

    if not assets:
        return {}
    return {"assets": sorted(assets, key=lambda item: item["asset_type"])}


def merge_recovery(
    canonical_record: dict[str, Any],
    expected: dict[str, Any],
    asset_types: set[str],
) -> dict[str, Any]:
    output = dict(canonical_record)
    current = output.get("recovery")
    current_assets: list[Any] = []
    if current is not None:
        if not isinstance(current, dict):
            raise ValueError(f"Canonical mission {canonical_record.get('id')} recovery must be an object")
        raw_assets = current.get("assets", [])
        if not isinstance(raw_assets, list):
            raise ValueError(f"Canonical mission {canonical_record.get('id')} recovery.assets must be an array")
        current_assets = raw_assets

    retained: list[dict[str, Any]] = []
    for item in current_assets:
        if not isinstance(item, dict):
            raise ValueError(f"Canonical mission {canonical_record.get('id')} recovery.assets contains an invalid item")
        if item.get("asset_type") not in asset_types:
            retained.append(item)
    retained.extend(expected.get("assets", []))
    retained.sort(key=lambda item: str(item.get("asset_type")))

    if retained:
        output["recovery"] = {"assets": retained}
    else:
        output.pop("recovery", None)
    return output


def extract_recovery(
    canonical_record: dict[str, Any],
    asset_types: set[str],
) -> dict[str, Any]:
    recovery = canonical_record.get("recovery")
    if recovery is None:
        return {}
    if not isinstance(recovery, dict):
        raise ValueError(f"Canonical mission {canonical_record.get('id')} recovery must be an object")
    assets = recovery.get("assets")
    if not isinstance(assets, list):
        raise ValueError(f"Canonical mission {canonical_record.get('id')} recovery.assets must be an array")

    selected: list[dict[str, Any]] = []
    seen: set[str] = set()
    for item in assets:
        if not isinstance(item, dict):
            raise ValueError(f"Canonical mission {canonical_record.get('id')} recovery.assets contains an invalid item")
        asset_type = item.get("asset_type")
        if asset_type not in asset_types:
            continue
        if asset_type in seen:
            raise ValueError(f"Canonical mission {canonical_record.get('id')} repeats recovery asset {asset_type}")
        seen.add(str(asset_type))
        minimum = checked_integer(item.get("minimum"), f"Canonical mission {canonical_record.get('id')} recovery {asset_type} minimum")
        maximum = checked_integer(item.get("maximum"), f"Canonical mission {canonical_record.get('id')} recovery {asset_type} maximum")
        if minimum > maximum:
            raise ValueError(
                f"Canonical mission {canonical_record.get('id')} recovery {asset_type} minimum exceeds maximum"
            )
        selected.append(
            {
                "asset_type": str(asset_type),
                "minimum": minimum,
                "maximum": maximum,
            }
        )
    if not selected:
        return {}
    return {"assets": sorted(selected, key=lambda item: item["asset_type"])}


def normalize_recovery(document: dict[str, Any]) -> dict[str, Any]:
    assets = document.get("assets")
    if not isinstance(assets, list):
        return {}
    return {
        "assets": sorted(
            [
                {
                    "asset_type": str(item["asset_type"]),
                    "minimum": int(item["minimum"]),
                    "maximum": int(item["maximum"]),
                }
                for item in assets
            ],
            key=lambda item: item["asset_type"],
        )
    }


def validate_promoted_recovery(
    mission_id: str,
    decision: dict[str, Any],
    official_record: dict[str, Any],
    canonical_record: dict[str, Any],
    mappings: dict[str, dict[str, Any]] | None = None,
) -> bool:
    if mappings is None:
        mappings = load_mapping_registry()
    asset_types = mapped_asset_types(mappings)
    expected = normalize_recovery(build_expected_recovery(official_record, mappings))
    actual = extract_recovery(canonical_record, asset_types)
    strict = decision.get("strict_recovery_equivalence") is True
    if strict or expected or actual:
        if actual != expected:
            raise ValueError(
                f"Mission {mission_id} recovery outcome differs: expected={expected!r}, canonical={actual!r}"
            )
        return True
    return False
