#!/usr/bin/env python3

from __future__ import annotations

import sys

from validate_official_key_mappings import (
    KEY_MAPPING_PATH,
    OFFICIAL_PATH,
    PROMOTED_STAGES,
    VERIFICATION_REGISTRY_PATH,
    audit_promoted_mission,
    canonical_records,
    read_json,
    records_by_id,
    validate_mapping_registry,
)


def main() -> int:
    try:
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
    except ValueError as exc:
        print(f"Official key mapping failure report could not start: {exc}", file=sys.stderr)
        return 1

    promoted = 0
    failures: list[str] = []
    for mission_id, decision in decisions.items():
        if not isinstance(decision, dict) or decision.get("stage") not in PROMOTED_STAGES:
            continue
        promoted += 1
        key = str(mission_id)
        official = official_by_id.get(key)
        canonical = canonical_by_id.get(key)
        if official is None or canonical is None:
            failures.append(f"Mission {key}: promoted record must exist in official and canonical collections")
            continue
        try:
            audit_promoted_mission(key, decision, official, canonical, mappings)
        except ValueError as exc:
            failures.append(str(exc))

    if failures:
        print(
            f"Official key mapping failure report found {len(failures)} failing missions "
            f"across {promoted} promoted records:",
            file=sys.stderr,
        )
        for failure in failures:
            print(f"- {failure}", file=sys.stderr)
        return 1

    print(f"Official key mapping failure report passed: all {promoted} promoted missions are equivalent.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
