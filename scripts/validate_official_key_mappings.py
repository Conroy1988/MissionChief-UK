#!/usr/bin/env python3

from __future__ import annotations

import sys
from typing import Any

import validate_official_conditional_mappings as _contextual
import validate_official_key_mappings_base as _base
from validate_official_key_mappings_base import *  # noqa: F401,F403

_CONTEXTUAL_TARGET = "requirements.contextual"
_CONTEXTUAL_PROBABILITY_TARGET = "requirements.contextual-probability"
_TRAFFIC_KEY = "traffic_car"

_base.TARGETS_BY_GROUP["requirements"].add(_CONTEXTUAL_TARGET)
_base.TARGETS_BY_GROUP["chances"].add(_CONTEXTUAL_PROBABILITY_TARGET)

_ORIGINAL_AUDIT_PROMOTED_MISSION = _base.audit_promoted_mission


def _without_traffic_car(record: dict[str, Any]) -> dict[str, Any]:
    output = dict(record)
    requirements = record.get("requirements")
    if not isinstance(requirements, dict):
        return output
    cleaned = dict(requirements)
    for field in ("guaranteed", "probabilistic", "conditional"):
        values = requirements.get(field)
        if not isinstance(values, list):
            continue
        cleaned[field] = [
            item
            for item in values
            if not (isinstance(item, dict) and item.get("resource") == _TRAFFIC_KEY)
        ]
    alternatives = requirements.get("alternatives")
    if isinstance(alternatives, list):
        cleaned["alternatives"] = [
            item
            for item in alternatives
            if not (
                isinstance(item, dict)
                and isinstance(item.get("resources"), list)
                and _TRAFFIC_KEY in item["resources"]
            )
        ]
    output["requirements"] = cleaned
    return output


def audit_promoted_mission(
    mission_id: str,
    decision: dict[str, Any],
    official: dict[str, Any],
    canonical: dict[str, Any],
    mappings: dict[str, dict[str, dict[str, Any]]],
) -> None:
    sanitized_official = dict(official)
    requirements = official.get("requirements", {})
    chances = official.get("chances", {})
    if not isinstance(requirements, dict) or not isinstance(chances, dict):
        raise ValueError(f"Official mission {mission_id} requirements or chances are invalid")
    sanitized_requirements = dict(requirements)
    sanitized_requirements.pop(_TRAFFIC_KEY, None)
    sanitized_chances = dict(chances)
    sanitized_chances.pop(_TRAFFIC_KEY, None)
    sanitized_official["requirements"] = sanitized_requirements
    sanitized_official["chances"] = sanitized_chances
    _ORIGINAL_AUDIT_PROMOTED_MISSION(
        mission_id,
        decision,
        sanitized_official,
        _without_traffic_car(canonical),
        mappings,
    )


_base.audit_promoted_mission = audit_promoted_mission


def audit() -> dict[str, int]:
    base_result = _base.audit()
    contextual_result = _contextual.audit()
    return {
        **base_result,
        "contextual_source_records": contextual_result["source_records"],
        "contextual_promoted": contextual_result["promoted_with_traffic"],
        "contextual_promoted_conditional": contextual_result["promoted_conditional"],
        "contextual_promoted_ordinary": contextual_result["promoted_ordinary"],
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
        f"{result['contextual_promoted']} promoted Traffic Car missions mapped "
        f"({result['contextual_promoted_conditional']} conditional, "
        f"{result['contextual_promoted_ordinary']} ordinary) across "
        f"{result['contextual_source_records']} official Traffic Car records."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
