#!/usr/bin/env python3

from __future__ import annotations

import json
import sys
from datetime import date
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
OFFICIAL_PATH = ROOT / "data" / "sources" / "missionchief-uk" / "einsaetze.raw.json"
CANONICAL_ROOT = ROOT / "data" / "uk" / "missions"
VERIFICATION_REGISTRY_PATH = ROOT / "data" / "uk" / "mission-verification-registry.json"
KEY_MAPPING_PATH = ROOT / "data" / "uk" / "official-key-mappings.json"

PROMOTED_STAGES = {"requirements-mapped", "operationally-verified", "fully-canonical"}
KEY_GROUPS = ("requirements", "chances", "prerequisites")
MAPPING_STATUSES = {"verified", "not-applicable"}


def read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"{path.relative_to(ROOT)}: unable to read JSON: {exc}") from exc


def mission_name(record: dict[str, Any]) -> str:
    value = record.get("name") or record.get("caption") or record.get("title")
    return str(value).strip() if value is not None else ""


def parse_iso_date(value: Any, label: str) -> None:
    if not isinstance(value, str):
        raise ValueError(f"{label} must be an ISO date")
    try:
        date.fromisoformat(value)
    except ValueError as exc:
        raise ValueError(f"{label} must be an ISO date") from exc


def records_by_id(records: Any, label: str) -> dict[str, dict[str, Any]]:
    if not isinstance(records, list):
        raise ValueError(f"{label} records must be an array")
    result: dict[str, dict[str, Any]] = {}
    for index, record in enumerate(records):
        if not isinstance(record, dict):
            raise ValueError(f"{label} record {index} must be an object")
        mission_id = record.get("id")
        if mission_id is None or str(mission_id).strip() == "":
            raise ValueError(f"{label} record {index} has no mission id")
        key = str(mission_id)
        if key in result:
            raise ValueError(f"{label} contains duplicate mission id {key}")
        result[key] = record
    return result


def canonical_records() -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    for path in sorted(CANONICAL_ROOT.glob("*.json")):
        record = read_json(path)
        if not isinstance(record, dict):
            raise ValueError(f"{path.relative_to(ROOT)}: canonical mission must be an object")
        mission_id = record.get("id")
        if mission_id is None or str(mission_id).strip() == "":
            raise ValueError(f"{path.relative_to(ROOT)}: canonical mission has no id")
        key = str(mission_id)
        if key in result:
            raise ValueError(f"Duplicate canonical mission id {key}")
        result[key] = record
    return result


def validate_mapping_registry(registry: Any) -> dict[str, dict[str, dict[str, Any]]]:
    if not isinstance(registry, dict) or registry.get("schema_version") != "1":
        raise ValueError("Official key mapping registry schema_version must be '1'")
    parse_iso_date(registry.get("updated_at"), "Official key mapping registry updated_at")

    validated: dict[str, dict[str, dict[str, Any]]] = {}
    for group in KEY_GROUPS:
        mappings = registry.get(group)
        if not isinstance(mappings, dict):
            raise ValueError(f"Official key mapping group {group} must be an object")
        validated[group] = {}
        for official_key, mapping in mappings.items():
            if not isinstance(official_key, str) or not official_key:
                raise ValueError(f"Official key mapping group {group} contains an invalid key")
            if not isinstance(mapping, dict):
                raise ValueError(f"Official mapping {group}.{official_key} must be an object")
            status = mapping.get("status")
            if status not in MAPPING_STATUSES:
                raise ValueError(f"Official mapping {group}.{official_key} has invalid status {status!r}")
            parse_iso_date(mapping.get("checked_at"), f"Official mapping {group}.{official_key} checked_at")
            sources = mapping.get("sources")
            if not isinstance(sources, list) or not sources or not all(isinstance(item, str) and item for item in sources):
                raise ValueError(f"Official mapping {group}.{official_key} requires evidence sources")
            if status == "verified":
                target = mapping.get("canonical_target")
                canonical_id = mapping.get("canonical_id")
                if target not in {"requirements.guaranteed", "preconditions"}:
                    raise ValueError(
                        f"Official mapping {group}.{official_key} uses unsupported canonical target {target!r}"
                    )
                if not isinstance(canonical_id, str) or not canonical_id:
                    raise ValueError(f"Official mapping {group}.{official_key} requires canonical_id")
            else:
                allowed_values = mapping.get("allowed_values")
                if not isinstance(allowed_values, list) or not allowed_values:
                    raise ValueError(
                        f"Not-applicable mapping {group}.{official_key} must narrowly define allowed_values"
                    )
            validated[group][official_key] = mapping
    return validated


def guaranteed_requirements(record: dict[str, Any], mission_id: str) -> dict[str, int]:
    requirements = record.get("requirements")
    if not isinstance(requirements, dict):
        raise ValueError(f"Canonical mission {mission_id} has no requirements object")
    guaranteed = requirements.get("guaranteed")
    if not isinstance(guaranteed, list):
        raise ValueError(f"Canonical mission {mission_id} has no guaranteed requirement array")
    result: dict[str, int] = {}
    for item in guaranteed:
        if not isinstance(item, dict):
            raise ValueError(f"Canonical mission {mission_id} has an invalid guaranteed requirement")
        resource = item.get("resource")
        quantity = item.get("quantity")
        if not isinstance(resource, str) or not resource or not isinstance(quantity, int):
            raise ValueError(f"Canonical mission {mission_id} has an invalid guaranteed requirement")
        if resource in result:
            raise ValueError(f"Canonical mission {mission_id} repeats guaranteed resource {resource}")
        result[resource] = quantity
    return result


def probabilistic_requirements(record: dict[str, Any], mission_id: str) -> list[dict[str, Any]]:
    requirements = record.get("requirements")
    if not isinstance(requirements, dict):
        raise ValueError(f"Canonical mission {mission_id} has no requirements object")
    probabilistic = requirements.get("probabilistic", [])
    if not isinstance(probabilistic, list):
        raise ValueError(f"Canonical mission {mission_id} has an invalid probabilistic requirement array")
    return probabilistic


def audit_promoted_mission(
    mission_id: str,
    decision: dict[str, Any],
    official: dict[str, Any],
    canonical: dict[str, Any],
    mappings: dict[str, dict[str, dict[str, Any]]],
) -> None:
    official_name = mission_name(official)
    canonical_name = mission_name(canonical)
    if official_name.casefold() != canonical_name.casefold():
        raise ValueError(
            f"Mission {mission_id} cannot be requirement-mapped while names differ: "
            f"official={official_name!r}, canonical={canonical_name!r}"
        )

    expected_guaranteed: dict[str, int] = {}
    expected_preconditions: dict[str, int] = {}

    for group in KEY_GROUPS:
        values = official.get(group, {})
        if not isinstance(values, dict):
            raise ValueError(f"Official mission {mission_id} field {group} must be an object")
        for official_key, value in values.items():
            mapping = mappings[group].get(str(official_key))
            if mapping is None:
                raise ValueError(
                    f"Mission {mission_id} is promoted but official key {group}.{official_key} is unmapped"
                )
            if mapping["status"] == "not-applicable":
                if value not in mapping["allowed_values"]:
                    raise ValueError(
                        f"Mission {mission_id} uses {group}.{official_key}={value!r}, outside the "
                        f"not-applicable allow-list {mapping['allowed_values']!r}"
                    )
                continue

            target = mapping["canonical_target"]
            canonical_id = mapping["canonical_id"]
            if not isinstance(value, int) or value < 0:
                raise ValueError(
                    f"Mission {mission_id} uses non-integer mapped value {group}.{official_key}={value!r}"
                )
            if target == "requirements.guaranteed":
                if group != "requirements":
                    raise ValueError(f"Mapping {group}.{official_key} targets guaranteed requirements incorrectly")
                expected_guaranteed[canonical_id] = value
            elif target == "preconditions":
                if group != "prerequisites":
                    raise ValueError(f"Mapping {group}.{official_key} targets preconditions incorrectly")
                expected_preconditions[canonical_id] = value

    canonical_guaranteed = guaranteed_requirements(canonical, mission_id)
    canonical_preconditions = canonical.get("preconditions", {})
    if not isinstance(canonical_preconditions, dict):
        raise ValueError(f"Canonical mission {mission_id} preconditions must be an object")

    for resource, quantity in expected_guaranteed.items():
        if canonical_guaranteed.get(resource) != quantity:
            raise ValueError(
                f"Mission {mission_id} maps official requirement to {resource}={quantity}, "
                f"canonical value is {canonical_guaranteed.get(resource)!r}"
            )
    for precondition, quantity in expected_preconditions.items():
        if canonical_preconditions.get(precondition) != quantity:
            raise ValueError(
                f"Mission {mission_id} maps official prerequisite to {precondition}={quantity}, "
                f"canonical value is {canonical_preconditions.get(precondition)!r}"
            )

    if decision.get("strict_key_equivalence") is True:
        if canonical_guaranteed != expected_guaranteed:
            raise ValueError(
                f"Mission {mission_id} strict guaranteed requirements differ: "
                f"expected={expected_guaranteed}, canonical={canonical_guaranteed}"
            )
        if canonical_preconditions != expected_preconditions:
            raise ValueError(
                f"Mission {mission_id} strict preconditions differ: "
                f"expected={expected_preconditions}, canonical={canonical_preconditions}"
            )
        official_chances = official.get("chances", {})
        if official_chances != {}:
            raise ValueError(f"Mission {mission_id} cannot use strict empty-chance equivalence with published chances")
        if probabilistic_requirements(canonical, mission_id):
            raise ValueError(f"Mission {mission_id} has canonical probabilistic requirements but no official chances")


def audit() -> dict[str, int]:
    official_envelope = read_json(OFFICIAL_PATH)
    if not isinstance(official_envelope, dict):
        raise ValueError("Official UK mission source envelope must be an object")
    official_by_id = records_by_id(official_envelope.get("records"), "Official UK mission source")
    canonical_by_id = canonical_records()
    mappings = validate_mapping_registry(read_json(KEY_MAPPING_PATH))

    verification_registry = read_json(VERIFICATION_REGISTRY_PATH)
    if not isinstance(verification_registry, dict):
        raise ValueError("Mission verification registry must be an object")
    decisions = verification_registry.get("records")
    if not isinstance(decisions, dict):
        raise ValueError("Mission verification registry records must be an object")

    promoted = 0
    fully_canonical = 0
    for mission_id, decision in decisions.items():
        if not isinstance(decision, dict) or decision.get("stage") not in PROMOTED_STAGES:
            continue
        key = str(mission_id)
        official = official_by_id.get(key)
        canonical = canonical_by_id.get(key)
        if official is None or canonical is None:
            raise ValueError(f"Promoted mission {key} must exist in official and canonical collections")
        audit_promoted_mission(key, decision, official, canonical, mappings)
        promoted += 1
        if decision.get("stage") == "fully-canonical":
            fully_canonical += 1

    return {
        "promoted": promoted,
        "fully_canonical": fully_canonical,
        "mapped_requirement_keys": len(mappings["requirements"]),
        "mapped_chance_keys": len(mappings["chances"]),
        "mapped_prerequisite_keys": len(mappings["prerequisites"]),
    }


def main() -> int:
    try:
        result = audit()
    except ValueError as exc:
        print(f"Official key mapping audit failed: {exc}", file=sys.stderr)
        return 1

    print(
        "Official key mapping audit passed: "
        f"{result['promoted']} promoted missions, "
        f"{result['fully_canonical']} fully canonical, "
        f"{result['mapped_requirement_keys']} requirement keys, "
        f"{result['mapped_chance_keys']} chance keys and "
        f"{result['mapped_prerequisite_keys']} prerequisite keys mapped."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
