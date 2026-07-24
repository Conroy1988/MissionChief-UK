#!/usr/bin/env python3

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

from operational_metadata_contract import (
    ROOT,
    build_expected_operational_fields,
    extract_operational_fields,
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
        mission_id = str(record["id"])
        if mission_id in output:
            raise ValueError(f"{label} repeats mission id {mission_id}")
        output[mission_id] = record
    return output


def canonical_records() -> dict[str, dict[str, Any]]:
    output: dict[str, dict[str, Any]] = {}
    for path in sorted(CANONICAL_ROOT.glob("*.json")):
        record = read_json(path)
        if not isinstance(record, dict) or record.get("id") is None:
            raise ValueError(f"{path.relative_to(ROOT)}: canonical mission is invalid")
        mission_id = str(record["id"])
        if mission_id in output:
            raise ValueError(f"Duplicate canonical mission id {mission_id}")
        output[mission_id] = record
    return output


def audit() -> dict[str, int]:
    envelope = read_json(OFFICIAL_PATH)
    official_by_id = records_by_id(
        envelope.get("records") if isinstance(envelope, dict) else None,
        "Official UK mission source",
    )
    canonical_by_id = canonical_records()
    registry = read_json(VERIFICATION_REGISTRY_PATH)
    decisions = registry.get("records") if isinstance(registry, dict) else None
    if not isinstance(decisions, dict):
        raise ValueError("Mission verification registry records must be an object")

    promoted = 0
    exact = 0
    strict = 0
    for mission_id, decision in decisions.items():
        if not isinstance(decision, dict) or decision.get("stage") not in PROMOTED_STAGES:
            continue
        promoted += 1
        key = str(mission_id)
        official = official_by_id.get(key)
        canonical = canonical_by_id.get(key)
        if official is None or canonical is None:
            raise ValueError(f"Promoted mission {key} must exist in official and canonical collections")
        expected = build_expected_operational_fields(official)
        actual = extract_operational_fields(canonical)
        if decision.get("strict_operational_equivalence") is True:
            strict += 1
        if actual != expected:
            raise ValueError(
                f"Mission {key} operational metadata differs: expected={expected!r}, canonical={actual!r}"
            )
        exact += 1

    return {
        "promoted": promoted,
        "exact": exact,
        "strict": strict,
        "official": len(official_by_id),
    }


def main() -> int:
    try:
        result = audit()
    except ValueError as exc:
        print(f"Official operational metadata audit failed: {exc}", file=sys.stderr)
        return 1
    print(
        "Official operational metadata audit passed: "
        f"{result['promoted']} promoted missions inspected, "
        f"{result['exact']} exact and {result['strict']} strict decisions "
        f"across {result['official']} official records."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
