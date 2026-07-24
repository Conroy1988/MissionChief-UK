#!/usr/bin/env python3

from __future__ import annotations

from typing import Any

import generate_ready_canonical_batch as generator
from personnel_contract import build_expected_personnel, load_mapping_registry, owned_paths
from prisoner_contract import build_expected_prisoners, load_mapping_registry as load_prisoner_mappings
from verification_registry import load_verification_registry

ORIGINAL_BUILD_CANONICAL_RECORD = generator.build_canonical_record
ORIGINAL_TRANSLATE_REQUIREMENTS = generator.translate_requirements
PERSONNEL_MAPPINGS = load_mapping_registry()
PRISONER_MAPPINGS = load_prisoner_mappings()
PERSONNEL_REQUIREMENT_KEYS, PERSONNEL_CHANCE_KEYS, _ = owned_paths(PERSONNEL_MAPPINGS)
PROBABILISTIC_ALTERNATIVE_TARGET = "requirements.probabilistic-alternatives"


def merged_fully_canonical_count() -> int:
    merged: dict[str, Any] = load_verification_registry(
        generator.ROOT,
        generator.VERIFICATION_REGISTRY_PATH,
        generator.BATCH_ROOT,
    )
    records = merged.get("records")
    if not isinstance(records, dict):
        raise ValueError("Merged mission verification registry records must be an object")
    return sum(
        1
        for decision in records.values()
        if isinstance(decision, dict) and decision.get("stage") == "fully-canonical"
    )


def without_personnel_owned_keys(official: dict[str, Any]) -> dict[str, Any]:
    output = dict(official)
    requirements = official.get("requirements", {})
    chances = official.get("chances", {})
    if not isinstance(requirements, dict) or not isinstance(chances, dict):
        raise ValueError(f"Mission {official.get('id')} requirements or chances are invalid")
    output["requirements"] = {
        key: value for key, value in requirements.items() if str(key) not in PERSONNEL_REQUIREMENT_KEYS
    }
    output["chances"] = {
        key: value for key, value in chances.items() if str(key) not in PERSONNEL_CHANCE_KEYS
    }
    return output


def translate_requirements_with_probabilistic_alternatives(
    official: dict[str, Any],
    mappings: dict[str, Any],
) -> dict[str, Any]:
    requirements = official.get("requirements", {})
    chances = official.get("chances", {})
    if not isinstance(requirements, dict) or not isinstance(chances, dict):
        raise ValueError(f"Mission {official.get('id')} requirements or chances are invalid")
    requirement_mappings = mappings.get("requirements", {})
    chance_mappings = mappings.get("chances", {})
    if not isinstance(requirement_mappings, dict) or not isinstance(chance_mappings, dict):
        raise ValueError("Official key mapping registry requirements and chances must be objects")

    handled: list[tuple[str, str, dict[str, Any], int, int]] = []
    for official_key, raw_quantity in requirements.items():
        mapping = requirement_mappings.get(str(official_key))
        if not isinstance(mapping, dict) or mapping.get("canonical_target") != "requirements.alternatives":
            continue
        chance_key = str(mapping.get("chance_key", official_key))
        if chance_key not in chances:
            continue
        chance_mapping = chance_mappings.get(chance_key)
        if not isinstance(chance_mapping, dict) or chance_mapping.get("canonical_target") != PROBABILISTIC_ALTERNATIVE_TARGET:
            continue
        quantity = generator.checked_integer(
            raw_quantity,
            f"Mission {official.get('id')} requirements.{official_key}",
        )
        percent = generator.checked_percent(
            chances[chance_key],
            f"Mission {official.get('id')} chances.{chance_key}",
        )
        handled.append((str(official_key), chance_key, mapping, quantity, percent))

    filtered = dict(official)
    filtered["requirements"] = {
        key: value for key, value in requirements.items() if str(key) not in {item[0] for item in handled}
    }
    filtered["chances"] = {
        key: value for key, value in chances.items() if str(key) not in {item[1] for item in handled}
    }
    output = ORIGINAL_TRANSLATE_REQUIREMENTS(filtered, mappings)

    alternatives = list(output.get("alternatives", []))
    for official_key, chance_key, mapping, quantity, percent in handled:
        resources = mapping.get("canonical_ids")
        if not isinstance(resources, list) or len(resources) < 2 or not all(
            isinstance(resource, str) and resource for resource in resources
        ):
            raise ValueError(f"Mission {official.get('id')} alternative mapping {official_key} is invalid")
        chance_mapping = chance_mappings[chance_key]
        if tuple(sorted(resources)) != tuple(sorted(chance_mapping.get("canonical_ids", []))):
            raise ValueError(
                f"Mission {official.get('id')} alternative requirement and chance mappings target different resources"
            )
        if str(chance_mapping.get("requirement_key", chance_key)) != official_key:
            raise ValueError(
                f"Mission {official.get('id')} chance mapping {chance_key} does not link to requirement {official_key}"
            )
        if quantity == 0 or percent == 0:
            continue
        item: dict[str, Any] = {
            "resources": list(resources),
            "quantity": quantity,
            "notes": ["Any listed qualifying resource may satisfy this official alternative group."],
        }
        if percent < 100:
            item["probability"] = percent / 100
        alternatives.append(item)
    if alternatives:
        output["alternatives"] = alternatives
    return output


def build_canonical_record_with_operational_contracts(
    official: dict[str, Any],
    mappings: dict[str, Any],
    patient_mappings: dict[str, dict[str, Any]],
    checked_at: str,
) -> dict[str, Any]:
    output = ORIGINAL_BUILD_CANONICAL_RECORD(
        without_personnel_owned_keys(official),
        mappings,
        patient_mappings,
        checked_at,
    )
    personnel = build_expected_personnel(official, PERSONNEL_MAPPINGS)
    if personnel:
        output["personnel"] = personnel
    prisoners = build_expected_prisoners(official, PRISONER_MAPPINGS)
    if prisoners:
        output["prisoners"] = prisoners
    return output


def main() -> int:
    generator.count_fully_canonical = merged_fully_canonical_count
    generator.translate_requirements = translate_requirements_with_probabilistic_alternatives
    generator.build_canonical_record = build_canonical_record_with_operational_contracts
    return generator.main()


if __name__ == "__main__":
    raise SystemExit(main())
