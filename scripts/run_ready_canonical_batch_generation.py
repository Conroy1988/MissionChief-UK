#!/usr/bin/env python3

from __future__ import annotations

from typing import Any

import generate_ready_canonical_batch as generator
from personnel_contract import build_expected_personnel, load_mapping_registry, owned_paths
from verification_registry import load_verification_registry

ORIGINAL_BUILD_CANONICAL_RECORD = generator.build_canonical_record
PERSONNEL_MAPPINGS = load_mapping_registry()
PERSONNEL_REQUIREMENT_KEYS, PERSONNEL_CHANCE_KEYS, _ = owned_paths(PERSONNEL_MAPPINGS)


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


def build_canonical_record_with_personnel(
    official: dict[str, Any],
    mappings: dict[str, Any],
    patient_mappings: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    output = ORIGINAL_BUILD_CANONICAL_RECORD(
        without_personnel_owned_keys(official),
        mappings,
        patient_mappings,
    )
    personnel = build_expected_personnel(official, PERSONNEL_MAPPINGS)
    if personnel:
        output["personnel"] = personnel
    return output


def main() -> int:
    generator.count_fully_canonical = merged_fully_canonical_count
    generator.build_canonical_record = build_canonical_record_with_personnel
    return generator.main()


if __name__ == "__main__":
    raise SystemExit(main())
