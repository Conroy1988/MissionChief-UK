#!/usr/bin/env python3

from __future__ import annotations

import sys
from typing import Any

import validate_official_conditional_mappings as _conditional
import validate_official_key_mappings_base as _base
from validate_official_key_mappings_base import *  # noqa: F401,F403

_CONDITIONAL_TARGET = "requirements.conditional"
_CONDITIONAL_PROBABILITY_TARGET = "requirements.conditional-probability"
_TRAFFIC_KEY = "traffic_car"

_base.TARGETS_BY_GROUP["requirements"].add(_CONDITIONAL_TARGET)
_base.TARGETS_BY_GROUP["chances"].add(_CONDITIONAL_PROBABILITY_TARGET)

_ORIGINAL_AUDIT_PROMOTED_MISSION = _base.audit_promoted_mission


def audit_promoted_mission(
    mission_id: str,
    decision: dict[str, Any],
    official: dict[str, Any],
    canonical: dict[str, Any],
    mappings: dict[str, dict[str, dict[str, Any]]],
) -> None:
    sanitized = dict(official)
    requirements = official.get("requirements", {})
    chances = official.get("chances", {})
    if not isinstance(requirements, dict) or not isinstance(chances, dict):
        raise ValueError(f"Official mission {mission_id} requirements or chances are invalid")
    sanitized_requirements = dict(requirements)
    sanitized_requirements.pop(_TRAFFIC_KEY, None)
    sanitized_chances = dict(chances)
    sanitized_chances.pop(_TRAFFIC_KEY, None)
    sanitized["requirements"] = sanitized_requirements
    sanitized["chances"] = sanitized_chances
    _ORIGINAL_AUDIT_PROMOTED_MISSION(mission_id, decision, sanitized, canonical, mappings)


_base.audit_promoted_mission = audit_promoted_mission


def audit() -> dict[str, int]:
    base_result = _base.audit()
    conditional_result = _conditional.audit()
    return {
        **base_result,
        "conditional_source_records": conditional_result["source_records"],
        "conditional_promoted": conditional_result["promoted_with_traffic"],
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
        f"{result['mapped_chance_keys']} chance keys, "
        f"{result['mapped_prerequisite_keys']} prerequisite keys and "
        f"{result['conditional_promoted']} promoted Traffic Car conditionals mapped "
        f"across {result['conditional_source_records']} official Traffic Car records."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
