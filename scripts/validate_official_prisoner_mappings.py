#!/usr/bin/env python3

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

from prisoner_contract import ROOT, build_expected_prisoners, load_mapping_registry, read_json

OFFICIAL_PATH = ROOT / "data" / "sources" / "missionchief-uk" / "einsaetze.raw.json"
CANONICAL_ROOT = ROOT / "data" / "uk" / "missions"
VERIFICATION_REGISTRY_PATH = ROOT / "data" / "uk" / "mission-verification-registry.json"
PROMOTED_STAGES = {"requirements-mapped", "operationally-verified", "fully-canonical"}


def records_by_id(records: Any, label: str) -> dict[str, dict[str, Any]]:
    if not isinstance(records, list):
        raise ValueError(f"{label} records must be an array")
    result: dict[str, dict[str, Any]] = {}
    for index, record in enumerate(records):
        if not isinstance(record, dict) or record.get("id") is None:
            raise ValueError(f"{label} record {index} is invalid")
        mission_id = str(record["id"])
        if mission_id in result:
            raise ValueError(f"{label} repeats mission id {mission_id}")
        result[mission_id] = record
    return result


def canonical_records() -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    for path in sorted(CANONICAL_ROOT.glob("*.json")):
        record = read_json(path)
        if not isinstance(record, dict) or record.get("id") is None:
            raise ValueError(f"{path.relative_to(ROOT)} is not a valid canonical mission")
        mission_id = str(record["id"])
        if mission_id in result:
            raise ValueError(f"Canonical mission collection repeats id {mission_id}")
        result[mission_id] = record
    return result


def audit() -> dict[str, int]:
    envelope = read_json(OFFICIAL_PATH)
    if not isinstance(envelope, dict):
        raise ValueError("Official UK mission source envelope must be an object")
    official_by_id = records_by_id(envelope.get("records"), "Official UK mission source")
    canonical_by_id = canonical_records()
    mappings = load_mapping_registry()

    verification_registry = read_json(VERIFICATION_REGISTRY_PATH)
    if not isinstance(verification_registry, dict):
        raise ValueError("Mission verification registry must be an object")
    decisions = verification_registry.get("records")
    if not isinstance(decisions, dict):
        raise ValueError("Mission verification registry records must be an object")

    promoted = 0
    prisoner_bearing = 0
    for mission_id, decision in decisions.items():
        if not isinstance(decision, dict) or decision.get("stage") not in PROMOTED_STAGES:
            continue
        key = str(mission_id)
        official = official_by_id.get(key)
        canonical = canonical_by_id.get(key)
        if official is None or canonical is None:
            raise ValueError(f"Promoted mission {key} must exist in official and canonical collections")
        expected = build_expected_prisoners(official, mappings)
        actual = canonical.get("prisoners")
        if expected:
            prisoner_bearing += 1
            if actual != expected:
                raise ValueError(
                    f"Mission {key} prisoner mapping differs: expected={json.dumps(expected)}, "
                    f"canonical={json.dumps(actual)}"
                )
        elif actual is not None:
            raise ValueError(f"Mission {key} has canonical prisoners but the official record publishes no prisoner fields")
        promoted += 1

    return {
        "promoted": promoted,
        "prisoner_bearing": prisoner_bearing,
        "mapped_fields": len(mappings),
    }


def main() -> int:
    try:
        result = audit()
    except ValueError as exc:
        print(f"Official prisoner mapping audit failed: {exc}", file=sys.stderr)
        return 1

    print(
        "Official prisoner mapping audit passed: "
        f"{result['promoted']}/{result['promoted']} promoted missions exact, "
        f"{result['prisoner_bearing']} prisoner-bearing promoted missions and "
        f"{result['mapped_fields']} prisoner fields mapped."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
