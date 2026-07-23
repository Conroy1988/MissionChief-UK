#!/usr/bin/env python3

from __future__ import annotations

from typing import Any

import generate_ready_canonical_batch_base as _base
from generate_ready_canonical_batch_base import *  # noqa: F401,F403

_ORIGINAL_TRANSLATE_REQUIREMENTS = _base.translate_requirements
_TRAFFIC_KEY = "traffic_car"
_CONDITION_FIELD = "need_traffic_car_only_if_present"
_CONTEXTUAL_TARGET = "requirements.contextual"
_CONTEXTUAL_PROBABILITY_TARGET = "requirements.contextual-probability"


def _checked_quantity(value: Any, label: str) -> int:
    if not isinstance(value, int) or isinstance(value, bool) or value < 0:
        raise ValueError(f"{label} must be a non-negative integer")
    return value


def _checked_percent(value: Any, label: str) -> int:
    if not isinstance(value, int) or isinstance(value, bool) or not 0 <= value <= 100:
        raise ValueError(f"{label} must be an integer percentage from 0 to 100")
    return value


def _append_resource(
    output: dict[str, Any],
    field: str,
    item: dict[str, Any],
) -> None:
    values = output.setdefault(field, [])
    if not isinstance(values, list):
        raise ValueError(f"Generated requirements.{field} must be an array")
    values.append(item)
    values.sort(key=lambda entry: str(entry.get("resource")))


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
    if not isinstance(mapping, dict) or mapping.get("canonical_target") != _CONTEXTUAL_TARGET:
        raise ValueError(f"Mission {mission_id} traffic_car requirement does not have a contextual mapping")
    if has_chance and (
        not isinstance(chance_mapping, dict)
        or chance_mapping.get("canonical_target") != _CONTEXTUAL_PROBABILITY_TARGET
    ):
        raise ValueError(f"Mission {mission_id} traffic_car chance does not have a contextual-probability mapping")

    raw_flag = additional.get(_CONDITION_FIELD)
    if _CONDITION_FIELD in additional and not isinstance(raw_flag, bool):
        raise ValueError(f"Mission {mission_id} additional.{_CONDITION_FIELD} must be a boolean")
    conditional = raw_flag is mapping.get("condition_value", True)

    quantity = _checked_quantity(requirements[_TRAFFIC_KEY], f"Mission {mission_id} requirements.traffic_car")
    percent = 100
    if has_chance:
        percent = _checked_percent(chances[_TRAFFIC_KEY], f"Mission {mission_id} chances.traffic_car")

    sanitized = dict(official)
    sanitized_requirements = dict(requirements)
    sanitized_requirements.pop(_TRAFFIC_KEY, None)
    sanitized_chances = dict(chances)
    sanitized_chances.pop(_TRAFFIC_KEY, None)
    sanitized["requirements"] = sanitized_requirements
    sanitized["chances"] = sanitized_chances
    output = _ORIGINAL_TRANSLATE_REQUIREMENTS(sanitized, mappings)

    if quantity == 0 or percent == 0:
        return output

    resource = str(mapping.get("canonical_id", _TRAFFIC_KEY))
    probability = None if percent == 100 else percent / 100
    if conditional:
        item: dict[str, Any] = {
            "resource": resource,
            "quantity": quantity,
            "condition": str(mapping.get("condition", "only_when_available")),
            "notes": [
                "The official UK mission data marks this Traffic Car requirement as applicable only when the resource is available."
            ],
        }
        if probability is not None:
            item["probability"] = probability
        _append_resource(output, "conditional", item)
    elif probability is None:
        _append_resource(output, "guaranteed", {"resource": resource, "quantity": quantity})
    else:
        _append_resource(
            output,
            "probabilistic",
            {"resource": resource, "quantity": quantity, "probability": probability},
        )
    return output


_base.translate_requirements = translate_requirements

generate = _base.generate
main = _base.main

if __name__ == "__main__":
    raise SystemExit(main())
