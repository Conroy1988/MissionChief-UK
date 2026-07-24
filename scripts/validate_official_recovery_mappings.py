#!/usr/bin/env python3

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

from recovery_contract import (
    ROOT,
    build_expected_recovery,
    load_mapping_registry,
    validate_promoted_recovery,
)

OFFICIAL_PATH = ROOT / "data" / "sources" / "missionchief-uk" / "einsaetze.raw.json"
CANONICAL_ROOT = ROOT / "data" / "uk" / "missions"
VERIFICATION_REGISTRY_PATH = ROOT / "data" / "uk" / "mission-verification-registry.json"
PROMOTED_STAGES = {"requirements-mapped", "operationally-verified", "fully-canonical"}


def read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"{path.relative_to(ROOT)}: unable to read JSON: {exc}") from exc


def records_by_id(records: Any, label: str) -> dict[str, dict[str, Any]]:
    if not isinstance(records, list):
        raise ValueError(f"{label} records must be an array")
    output: dict[str, dict[str, Any]] = {}
    for index, record in enumerate(records):
        if not isinstance(record, dict) or record.get("id") is None:
            raise ValueError(f"{label} record {index} is invalid")
        key = str(record["id"])
        if key in output:
            raise ValueError(f"{label} repeats mission id {key}")
        output[key] = record
    return output


def canonical_records() -> dict[str, dict[str, Any]]:
    output: dict[str, dict[str, Any]] = {}
    for path in sorted(CANONICAL_ROOT.glob("*.json")):
        record = read_json(path)
        if not isinstance(record, dict) or record.get("id") is None:
            raise ValueError(f"{path.relative_to(ROOT)}: canonical mission is invalid")
        key = str(record["id"])
        if key in output:
            raise ValueError(f"Duplicate canonical mission id {key}")
        output[key] = record
    return output


def audit() -> dict[str, int]:
    official_envelope = read_json(OFFICIAL_PATH)
    if not isinstance(official_envelope, dict):
        raise ValueError("Official UK mission source envelope must be an object")
    official_by_id = records_by_id(official_envelope.get("records"), "Official UK mission source")
    canonical_by_id = canonical_records()
    mappings = load_mapping_registry()

    verification_registry = read_json(VERIFICATION_REGISTRY_PATH)
    decisions = verification_registry.get("records") if isinstance(verification_registry, dict) else None
    if not isinstance(decisions, dict):
        raise ValueError("Mission verification registry records must be an object")

    promoted = 0
    exact = 0
    recovery_missions = 0
    strict_missions = 0
    for mission_id, decision in decisions.items():
        if not isinstance(decision, dict) or decision.get("stage") not in PROMOTED_STAGES:
            continue
        promoted += 1
        key = str(mission_id)
        official = official_by_id.get(key)
        canonical = canonical_by_id.get(key)
        if official is None or canonical is None:
            raise ValueError(f"Promoted mission {key} must exist in official and canonical collections")
        expected = build_expected_recovery(official, mappings)
        if expected:
            recovery_missions += 1
        if decision.get("strict_recovery_equivalence") is True:
            strict_missions += 1
        if validate_promoted_recovery(key, decision, official, canonical, mappings):
            exact += 1

    return {
        "promoted": promoted,
        "exact": exact,
        "recovery_missions": recovery_missions,
        "strict_missions": strict_missions,
        "asset_types": len(mappings),
    }


def main() -> int:
    try:
        result = audit()
    except ValueError as exc:
        print(f"Official recovery mapping audit failed: {exc}", file=sys.stderr)
        return 1

    print(
        "Official recovery mapping audit passed: "
        f"{result['promoted']} promoted missions inspected, "
        f"{result['exact']} exact recovery missions, "
        f"{result['strict_missions']} strict decisions and "
        f"{result['asset_types']} mapped asset types."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
