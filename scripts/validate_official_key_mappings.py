#!/usr/bin/env python3

from __future__ import annotations

import json
import math
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
DELEGATED_REQUIREMENT_TARGETS = {"personnel.chance-aware"}
DELEGATED_CHANCE_TARGETS = {
    "patients.transport_probability",
    "patients.critical_care_probability",
    "personnel.probabilistic",
}
TARGETS_BY_GROUP = {
    "requirements": {
        "requirements.guaranteed",
        "requirements.chance-aware",
        "requirements.alternatives",
        *DELEGATED_REQUIREMENT_TARGETS,
    },
    "chances": {"requirements.probabilistic", *DELEGATED_CHANCE_TARGETS},
    "prerequisites": {"preconditions"},
}


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


def validated_resource_list(value: Any, label: str) -> list[str]:
    if (
        not isinstance(value, list)
        or len(value) < 2
        or not all(isinstance(item, str) and item for item in value)
        or len(value) != len(set(value))
    ):
        raise ValueError(f"{label} requires at least two unique canonical_ids")
    return value


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
            label = f"Official mapping {group}.{official_key}"
            if not isinstance(official_key, str) or not official_key:
                raise ValueError(f"Official key mapping group {group} contains an invalid key")
            if not isinstance(mapping, dict):
                raise ValueError(f"{label} must be an object")
            status = mapping.get("status")
            if status not in MAPPING_STATUSES:
                raise ValueError(f"{label} has invalid status {status!r}")
            parse_iso_date(mapping.get("checked_at"), f"{label} checked_at")
            sources = mapping.get("sources")
            if not isinstance(sources, list) or not sources or not all(isinstance(item, str) and item for item in sources):
                raise ValueError(f"{label} requires evidence sources")

            if status == "verified":
                target = mapping.get("canonical_target")
                if target not in TARGETS_BY_GROUP[group]:
                    raise ValueError(f"{label} uses unsupported canonical target {target!r}")
                if group == "requirements" and target == "requirements.alternatives":
                    validated_resource_list(mapping.get("canonical_ids"), label)
                elif target in DELEGATED_REQUIREMENT_TARGETS or target == "personnel.probabilistic":
                    role = mapping.get("canonical_role")
                    if not isinstance(role, str) or not role:
                        raise ValueError(f"{label} requires canonical_role")
                elif target in DELEGATED_CHANCE_TARGETS:
                    pass
                else:
                    canonical_id = mapping.get("canonical_id")
                    if not isinstance(canonical_id, str) or not canonical_id:
                        raise ValueError(f"{label} requires canonical_id")
                if group == "chances" and target in {"requirements.probabilistic", "personnel.probabilistic"}:
                    requirement_key = mapping.get("requirement_key", official_key)
                    if not isinstance(requirement_key, str) or not requirement_key:
                        raise ValueError(f"{label} requires requirement_key")
            else:
                allowed_values = mapping.get("allowed_values")
                if not isinstance(allowed_values, list) or not allowed_values:
                    raise ValueError(f"{label} must narrowly define allowed_values")
            validated[group][official_key] = mapping
    return validated


def requirements_object(record: dict[str, Any], mission_id: str) -> dict[str, Any]:
    requirements = record.get("requirements")
    if not isinstance(requirements, dict):
        raise ValueError(f"Canonical mission {mission_id} has no requirements object")
    return requirements


def guaranteed_requirements(record: dict[str, Any], mission_id: str) -> dict[str, int]:
    guaranteed = requirements_object(record, mission_id).get("guaranteed")
    if not isinstance(guaranteed, list):
        raise ValueError(f"Canonical mission {mission_id} has no guaranteed requirement array")
    result: dict[str, int] = {}
    for item in guaranteed:
        if not isinstance(item, dict):
            raise ValueError(f"Canonical mission {mission_id} has an invalid guaranteed requirement")
        resource = item.get("resource")
        quantity = item.get("quantity")
        if not isinstance(resource, str) or not resource or not isinstance(quantity, int) or isinstance(quantity, bool) or quantity < 1:
            raise ValueError(f"Canonical mission {mission_id} has an invalid guaranteed requirement")
        if resource in result:
            raise ValueError(f"Canonical mission {mission_id} repeats guaranteed resource {resource}")
        result[resource] = quantity
    return result


def probabilistic_requirements(record: dict[str, Any], mission_id: str) -> dict[str, tuple[int, float]]:
    probabilistic = requirements_object(record, mission_id).get("probabilistic", [])
    if not isinstance(probabilistic, list):
        raise ValueError(f"Canonical mission {mission_id} has an invalid probabilistic requirement array")
    result: dict[str, tuple[int, float]] = {}
    for item in probabilistic:
        if not isinstance(item, dict):
            raise ValueError(f"Canonical mission {mission_id} has an invalid probabilistic requirement")
        resource = item.get("resource")
        quantity = item.get("quantity")
        probability = item.get("probability")
        if (
            not isinstance(resource, str)
            or not resource
            or not isinstance(quantity, int)
            or isinstance(quantity, bool)
            or quantity < 1
            or not isinstance(probability, (int, float))
            or isinstance(probability, bool)
            or not 0 <= float(probability) <= 1
        ):
            raise ValueError(f"Canonical mission {mission_id} has an invalid probabilistic requirement")
        if resource in result:
            raise ValueError(f"Canonical mission {mission_id} repeats probabilistic resource {resource}")
        result[resource] = (quantity, float(probability))
    return result


def alternative_requirements(record: dict[str, Any], mission_id: str) -> dict[tuple[str, ...], int]:
    alternatives = requirements_object(record, mission_id).get("alternatives", [])
    if not isinstance(alternatives, list):
        raise ValueError(f"Canonical mission {mission_id} has an invalid alternatives requirement array")
    result: dict[tuple[str, ...], int] = {}
    for item in alternatives:
        if not isinstance(item, dict):
            raise ValueError(f"Canonical mission {mission_id} has an invalid alternative requirement")
        resources = item.get("resources")
        quantity = item.get("quantity")
        if (
            not isinstance(resources, list)
            or len(resources) < 2
            or not all(isinstance(resource, str) and resource for resource in resources)
            or len(resources) != len(set(resources))
            or not isinstance(quantity, int)
            or isinstance(quantity, bool)
            or quantity < 1
        ):
            raise ValueError(f"Canonical mission {mission_id} has an invalid alternative requirement")
        key = tuple(sorted(resources))
        if key in result:
            raise ValueError(f"Canonical mission {mission_id} repeats alternative resource group {key}")
        result[key] = quantity
    return result


def add_expected(target: dict[str, int], resource: str, quantity: int, mission_id: str, label: str) -> None:
    previous = target.get(resource)
    if previous is not None and previous != quantity:
        raise ValueError(f"Mission {mission_id} maps conflicting {label} quantities for {resource}: {previous} and {quantity}")
    target[resource] = quantity


def add_expected_probability(
    target: dict[str, tuple[int, float]],
    resource: str,
    quantity: int,
    probability: float,
    mission_id: str,
) -> None:
    previous = target.get(resource)
    value = (quantity, probability)
    if previous is not None and previous != value:
        raise ValueError(f"Mission {mission_id} maps conflicting probabilistic values for {resource}: {previous} and {value}")
    target[resource] = value


def add_expected_alternative(
    target: dict[tuple[str, ...], int],
    resources: list[str],
    quantity: int,
    mission_id: str,
) -> None:
    key = tuple(sorted(resources))
    previous = target.get(key)
    if previous is not None and previous != quantity:
        raise ValueError(f"Mission {mission_id} maps conflicting alternative quantities for {key}: {previous} and {quantity}")
    target[key] = quantity


def validated_percent(value: Any, label: str) -> int:
    if not isinstance(value, int) or isinstance(value, bool) or not 0 <= value <= 100:
        raise ValueError(f"{label} must be an integer percentage from 0 to 100")
    return value


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

    official_requirements = official.get("requirements", {})
    official_chances = official.get("chances", {})
    official_prerequisites = official.get("prerequisites", {})
    for group, values in (
        ("requirements", official_requirements),
        ("chances", official_chances),
        ("prerequisites", official_prerequisites),
    ):
        if not isinstance(values, dict):
            raise ValueError(f"Official mission {mission_id} field {group} must be an object")

    expected_guaranteed: dict[str, int] = {}
    expected_probabilistic: dict[str, tuple[int, float]] = {}
    expected_alternatives: dict[tuple[str, ...], int] = {}
    expected_preconditions: dict[str, int] = {}

    for official_key, value in official_requirements.items():
        mapping = mappings["requirements"].get(str(official_key))
        if mapping is None:
            raise ValueError(f"Mission {mission_id} is promoted but official key requirements.{official_key} is unmapped")
        if mapping["status"] == "not-applicable":
            if value not in mapping["allowed_values"]:
                raise ValueError(
                    f"Mission {mission_id} uses requirements.{official_key}={value!r}, outside the "
                    f"not-applicable allow-list {mapping['allowed_values']!r}"
                )
            continue
        if not isinstance(value, int) or isinstance(value, bool) or value < 0:
            raise ValueError(f"Mission {mission_id} uses non-integer mapped value requirements.{official_key}={value!r}")

        target = mapping["canonical_target"]
        if target in DELEGATED_REQUIREMENT_TARGETS:
            continue
        if target == "requirements.alternatives":
            if official_key in official_chances:
                raise ValueError(
                    f"Mission {mission_id} publishes a chance for alternative requirements.{official_key}; "
                    "probabilistic alternative groups are not yet supported"
                )
            if value > 0:
                add_expected_alternative(expected_alternatives, mapping["canonical_ids"], value, mission_id)
            continue

        resource = mapping["canonical_id"]
        if target == "requirements.guaranteed":
            if value > 0:
                add_expected(expected_guaranteed, resource, value, mission_id, "guaranteed")
            continue

        chance_key = str(mapping.get("chance_key", official_key))
        chance = official_chances.get(chance_key)
        if chance is None:
            if value > 0:
                add_expected(expected_guaranteed, resource, value, mission_id, "guaranteed")
            continue
        chance_mapping = mappings["chances"].get(chance_key)
        if chance_mapping is None:
            raise ValueError(
                f"Mission {mission_id} maps chance-aware requirements.{official_key} but chances.{chance_key} is unmapped"
            )
        if chance_mapping["status"] != "verified" or chance_mapping["canonical_target"] != "requirements.probabilistic":
            raise ValueError(f"Mission {mission_id} chance mapping chances.{chance_key} is not a resource probability")
        if chance_mapping["canonical_id"] != resource:
            raise ValueError(
                f"Mission {mission_id} chance mapping chances.{chance_key} targets {chance_mapping['canonical_id']} "
                f"instead of {resource}"
            )
        if str(chance_mapping.get("requirement_key", chance_key)) != str(official_key):
            raise ValueError(
                f"Mission {mission_id} chance mapping chances.{chance_key} does not link to requirements.{official_key}"
            )
        percent = validated_percent(chance, f"Mission {mission_id} chances.{chance_key}")
        if percent <= 0 or value <= 0:
            continue
        if percent >= 100:
            add_expected(expected_guaranteed, resource, value, mission_id, "guaranteed")
        else:
            add_expected_probability(expected_probabilistic, resource, value, percent / 100, mission_id)

    for official_key, value in official_chances.items():
        mapping = mappings["chances"].get(str(official_key))
        if mapping is None:
            raise ValueError(f"Mission {mission_id} is promoted but official key chances.{official_key} is unmapped")
        if mapping["status"] == "not-applicable":
            if value not in mapping["allowed_values"]:
                raise ValueError(
                    f"Mission {mission_id} uses chances.{official_key}={value!r}, outside the "
                    f"not-applicable allow-list {mapping['allowed_values']!r}"
                )
            continue
        validated_percent(value, f"Mission {mission_id} chances.{official_key}")
        target = mapping["canonical_target"]
        if target in DELEGATED_CHANCE_TARGETS:
            continue
        requirement_key = str(mapping.get("requirement_key", official_key))
        if requirement_key not in official_requirements:
            raise ValueError(
                f"Mission {mission_id} publishes chances.{official_key} without linked requirements.{requirement_key}"
            )
        requirement_mapping = mappings["requirements"].get(requirement_key)
        if requirement_mapping is None or requirement_mapping.get("canonical_target") != "requirements.chance-aware":
            raise ValueError(
                f"Mission {mission_id} chance chances.{official_key} requires a chance-aware requirements.{requirement_key} mapping"
            )
        if requirement_mapping.get("canonical_id") != mapping.get("canonical_id"):
            raise ValueError(f"Mission {mission_id} chance and requirement mappings target different canonical resources")

    for official_key, value in official_prerequisites.items():
        mapping = mappings["prerequisites"].get(str(official_key))
        if mapping is None:
            raise ValueError(f"Mission {mission_id} is promoted but official key prerequisites.{official_key} is unmapped")
        if mapping["status"] == "not-applicable":
            if value not in mapping["allowed_values"]:
                raise ValueError(
                    f"Mission {mission_id} uses prerequisites.{official_key}={value!r}, outside the "
                    f"not-applicable allow-list {mapping['allowed_values']!r}"
                )
            continue
        if not isinstance(value, int) or isinstance(value, bool) or value < 0:
            raise ValueError(f"Mission {mission_id} uses non-integer prerequisite {official_key}={value!r}")
        expected_preconditions[mapping["canonical_id"]] = value

    canonical_guaranteed = guaranteed_requirements(canonical, mission_id)
    canonical_probabilistic = probabilistic_requirements(canonical, mission_id)
    canonical_alternatives = alternative_requirements(canonical, mission_id)
    canonical_preconditions = canonical.get("preconditions", {})
    if not isinstance(canonical_preconditions, dict):
        raise ValueError(f"Canonical mission {mission_id} preconditions must be an object")

    for resource, quantity in expected_guaranteed.items():
        if canonical_guaranteed.get(resource) != quantity:
            raise ValueError(
                f"Mission {mission_id} maps official requirement to guaranteed {resource}={quantity}, "
                f"canonical value is {canonical_guaranteed.get(resource)!r}"
            )
    for resource, (quantity, probability) in expected_probabilistic.items():
        actual = canonical_probabilistic.get(resource)
        if actual is None or actual[0] != quantity or not math.isclose(actual[1], probability, abs_tol=1e-9):
            raise ValueError(
                f"Mission {mission_id} maps official requirement to probabilistic {resource}="
                f"({quantity}, {probability}), canonical value is {actual!r}"
            )
    for resources, quantity in expected_alternatives.items():
        if canonical_alternatives.get(resources) != quantity:
            raise ValueError(
                f"Mission {mission_id} maps official requirement to alternative {resources}={quantity}, "
                f"canonical value is {canonical_alternatives.get(resources)!r}"
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
        if canonical_probabilistic.keys() != expected_probabilistic.keys():
            raise ValueError(
                f"Mission {mission_id} strict probabilistic resources differ: "
                f"expected={expected_probabilistic}, canonical={canonical_probabilistic}"
            )
        for resource, expected in expected_probabilistic.items():
            actual = canonical_probabilistic[resource]
            if actual[0] != expected[0] or not math.isclose(actual[1], expected[1], abs_tol=1e-9):
                raise ValueError(
                    f"Mission {mission_id} strict probabilistic value differs for {resource}: "
                    f"expected={expected}, canonical={actual}"
                )
        if canonical_alternatives != expected_alternatives:
            raise ValueError(
                f"Mission {mission_id} strict alternative requirements differ: "
                f"expected={expected_alternatives}, canonical={canonical_alternatives}"
            )
        if canonical_preconditions != expected_preconditions:
            raise ValueError(
                f"Mission {mission_id} strict preconditions differ: "
                f"expected={expected_preconditions}, canonical={canonical_preconditions}"
            )


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
