#!/usr/bin/env python3

from __future__ import annotations

from typing import Any

import generate_ready_canonical_batch_base as _base
from generate_ready_canonical_batch_base import *  # noqa: F401,F403

_ORIGINAL_TRANSLATE_REQUIREMENTS = _base.translate_requirements
_TRAFFIC_KEY = "traffic_car"
_CONDITION_FIELD = "need_traffic_car_only_if_present"


def _checked_quantity(value: Any, label: str) -> int:
    if not isinstance(value, int) or isinstance(value, bool) or value < 0:
        raise ValueError(f"{label} must be a non-negative integer")
    return value


def _checked_percent(value: Any, label: str) -> int:
    if not isinstance(value, int) or isinstance(value, bool) or not 0 <= value <= 100:
        raise ValueError(f"{label} must be an integer percentage from 0 to 100")
    return value


def translate_requirements(official: dict[str, Any], mappings: dict[str, Any]) -> dict[str, Any]:
    mission_id = str(official.get("id"))
    requirements = official.get("requirements", {})
    chances = official.get("chances", {})
    additional = official.get("additional", {})
    if not isinstance(requirements, dict) or not isinstance(chances, dict) or not isinstance(additional, dict):
        raise ValueError(f"Mission {mission_id} requirements, chances or additional fields are invalid")

    has_requirement = _TRAFFIC_KEY in requirements
    has_chance = _TRAFFIC_KEY in chances
    if has_chance and not has_requirement:
        raise ValueError(f"Mission {mission_id} publishes chances.traffic_car without requirements.traffic_car")
    if not has_requirement:
        return _ORIGINAL_TRANSLATE_REQUIREMENTS(official, mappings)

    mapping = mappings.get("requirements", {}).get(_TRAFFIC_KEY)
    chance_mapping = mappings.get("chances", {}).get(_TRAFFIC_KEY) if has_chance else None
    if not isinstance(mapping, dict) or mapping.get("canonical_target") != "requirements.conditional":
        raise ValueError(f"Mission {mission_id} traffic_car requirement does not have a conditional mapping")
    if has_chance and (
        not isinstance(chance_mapping, dict)
        or chance_mapping.get("canonical_target") != "requirements.conditional-probability"
    ):
        raise ValueError(f"Mission {mission_id} traffic_car chance does not have a conditional-probability mapping")

    quantity = _checked_quantity(requirements[_TRAFFIC_KEY], f"Mission {mission_id} requirements.traffic_car")
    required_flag = mapping.get("condition_value", True)
    if quantity > 0 and additional.get(_CONDITION_FIELD) is not required_flag:
        raise ValueError(
            f"Mission {mission_id} requires Traffic Cars but additional.{_CONDITION_FIELD} is not {required_flag!r}"
        )

    sanitized = dict(official)
    sanitized_requirements = dict(requirements)
    sanitized_requirements.pop(_TRAFFIC_KEY, None)
    sanitized_chances = dict(chances)
    sanitized_chances.pop(_TRAFFIC_KEY, None)
    sanitized["requirements"] = sanitized_requirements
    sanitized["chances"] = sanitized_chances
    output = _ORIGINAL_TRANSLATE_REQUIREMENTS(sanitized, mappings)

    probability: float | None = None
    if has_chance:
        percent = _checked_percent(chances[_TRAFFIC_KEY], f"Mission {mission_id} chances.traffic_car")
        if percent == 0:
            return output
        if percent < 100:
            probability = percent / 100
    if quantity == 0:
        return output

    item: dict[str, Any] = {
        "resource": str(mapping.get("canonical_id", "traffic_car")),
        "quantity": quantity,
        "condition": str(mapping.get("condition", "only_when_available")),
        "notes": [
            "The official UK mission data marks this Traffic Car requirement as applicable only when the resource is available."
        ],
    }
    if probability is not None:
        item["probability"] = probability
    output.setdefault("conditional", []).append(item)
    output["conditional"] = sorted(output["conditional"], key=lambda entry: str(entry.get("resource")))
    return output


_base.translate_requirements = translate_requirements

generate = _base.generate
main = _base.main

if __name__ == "__main__":
    raise SystemExit(main())
