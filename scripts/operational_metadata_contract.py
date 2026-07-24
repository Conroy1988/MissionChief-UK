#!/usr/bin/env python3

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]

GENERATOR_METADATA: dict[str, tuple[str, list[str]]] = {
    "firehouse_missions": ("fire", ["Fire Fighting Missions"]),
    "police_station_missions": ("police", ["Police Missions"]),
    "ambulance_station_missions": ("ambulance", ["Ambulance Missions"]),
    "tow_trucks_missions": ("recovery", ["Recovery Vehicle Missions"]),
    "coastal_rescue_missions": ("coastguard", ["Coastguard Missions"]),
    "mountain_missions": ("mountain_rescue", ["Mountain Rescue Missions"]),
    "bomb_disposal_missions": ("bomb_disposal", ["Bomb Disposal Missions"]),
}

OPERATIONAL_ADDITIONAL_KEYS = {
    "allow_ktw_instead_of_rtw",
    "allow_without_poi",
    "average_min_fire_personnel",
    "average_min_police_personnel",
    "date_end",
    "date_start",
    "duration",
    "duration_text",
    "fire_alarm_system_possible",
    "guard_mission",
    "handoff_possible_via_building_types",
    "only_alliance_mission",
    "pump_water_amount",
    "subsequent_mission_only",
    "subsequent_missions_ids",
    "swat_personnel",
    "unavailable_in_normal_missions",
    "uses_custom_spawn_area",
    "vehicle_groups",
}

GENERATION_BOOLEAN_KEYS = {
    "allow_ktw_instead_of_rtw",
    "allow_without_poi",
    "fire_alarm_system_possible",
    "guard_mission",
    "only_alliance_mission",
    "subsequent_mission_only",
    "unavailable_in_normal_missions",
}


def _checked_object(value: Any, label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValueError(f"{label} must be an object")
    return value


def _checked_non_negative_int(value: Any, label: str) -> int:
    if not isinstance(value, int) or isinstance(value, bool) or value < 0:
        raise ValueError(f"{label} must be a non-negative integer")
    return value


def _checked_bool(value: Any, label: str) -> bool:
    if not isinstance(value, bool):
        raise ValueError(f"{label} must be a boolean")
    return value


def _checked_string(value: Any, label: str) -> str:
    if not isinstance(value, str):
        raise ValueError(f"{label} must be a string")
    return value


def generator_metadata(official_record: dict[str, Any]) -> tuple[str, list[str]]:
    mission_id = official_record.get("id")
    additional = _checked_object(official_record.get("additional"), f"Mission {mission_id} additional")
    family = additional.get("filter_id")
    if not isinstance(family, str) or family not in GENERATOR_METADATA:
        raise ValueError(f"Mission {mission_id} uses unsupported generator family {family!r}")
    service, mission_types = GENERATOR_METADATA[family]
    return service, list(mission_types)


def relationship_ids(official_record: dict[str, Any], field: str) -> list[str]:
    mission_id = official_record.get("id")
    additional = _checked_object(official_record.get("additional"), f"Mission {mission_id} additional")
    values = additional.get(field, [])
    if not isinstance(values, list):
        raise ValueError(f"Mission {mission_id} additional.{field} must be an array")
    return [str(value) for value in values]


def build_expected_operational_fields(official_record: dict[str, Any]) -> dict[str, Any]:
    mission_id = official_record.get("id")
    additional = _checked_object(official_record.get("additional"), f"Mission {mission_id} additional")
    requirements = _checked_object(official_record.get("requirements"), f"Mission {mission_id} requirements")
    prerequisites = _checked_object(official_record.get("prerequisites"), f"Mission {mission_id} prerequisites")
    service, mission_types = generator_metadata(official_record)

    output: dict[str, Any] = {
        "service": service,
        "mission_types": mission_types,
    }

    if "duration" in additional:
        seconds = _checked_non_negative_int(additional["duration"], f"Mission {mission_id} additional.duration")
        if seconds % 60 != 0:
            raise ValueError(f"Mission {mission_id} additional.duration must be an exact number of minutes")
        output["duration_minutes"] = seconds // 60

    if "uses_custom_spawn_area" in additional:
        output["custom_spawn_area"] = _checked_bool(
            additional["uses_custom_spawn_area"],
            f"Mission {mission_id} additional.uses_custom_spawn_area",
        )

    availability: dict[str, str] = {}
    if "date_start" in additional:
        availability["starts_at"] = _checked_string(
            additional["date_start"], f"Mission {mission_id} additional.date_start"
        )
    if "date_end" in additional:
        availability["ends_at"] = _checked_string(
            additional["date_end"], f"Mission {mission_id} additional.date_end"
        )
    if availability:
        output["availability_window"] = availability

    generation_rules: dict[str, Any] = {}
    if "main_building" in prerequisites:
        generation_rules["main_building_type"] = _checked_non_negative_int(
            prerequisites["main_building"], f"Mission {mission_id} prerequisites.main_building"
        )
    if "max_police_stations" in prerequisites:
        generation_rules["max_police_stations"] = _checked_non_negative_int(
            prerequisites["max_police_stations"],
            f"Mission {mission_id} prerequisites.max_police_stations",
        )
    for key in sorted(GENERATION_BOOLEAN_KEYS):
        if key in additional:
            generation_rules[key] = _checked_bool(
                additional[key], f"Mission {mission_id} additional.{key}"
            )
    if generation_rules:
        output["generation_rules"] = generation_rules

    water_requirements: dict[str, int] = {}
    if "min_pump_speed" in requirements:
        water_requirements["minimum_pump_speed"] = _checked_non_negative_int(
            requirements["min_pump_speed"], f"Mission {mission_id} requirements.min_pump_speed"
        )
    if "pump_water_amount" in additional:
        water_requirements["pump_water_amount"] = _checked_non_negative_int(
            additional["pump_water_amount"], f"Mission {mission_id} additional.pump_water_amount"
        )
    if water_requirements:
        output["water_requirements"] = water_requirements

    subsequent = relationship_ids(official_record, "subsequent_missions_ids")
    if subsequent:
        output["subsequent_missions"] = subsequent

    official_additional = {
        key: deepcopy(additional[key])
        for key in sorted(OPERATIONAL_ADDITIONAL_KEYS)
        if key in additional
    }
    family = additional.get("filter_id")
    output["official_metadata"] = {
        "generator_family": _checked_string(family, f"Mission {mission_id} additional.filter_id"),
        "mission_categories": deepcopy(official_record.get("mission_categories", [])),
        "icons": deepcopy(official_record.get("icons", [])),
        "base_mission_id": deepcopy(official_record.get("base_mission_id", official_record.get("id"))),
        "additive_overlays": deepcopy(official_record.get("additive_overlays") or ""),
        "overlay_index": deepcopy(official_record.get("overlay_index")),
        "generated_by": deepcopy(official_record.get("generated_by") or ""),
        "additional": official_additional,
    }
    return output


def merge_operational_fields(
    canonical_record: dict[str, Any],
    expected: dict[str, Any],
) -> dict[str, Any]:
    output = dict(canonical_record)
    owned = {
        "service",
        "mission_types",
        "duration_minutes",
        "custom_spawn_area",
        "availability_window",
        "generation_rules",
        "water_requirements",
        "subsequent_missions",
        "official_metadata",
    }
    for field in owned:
        if field in expected:
            output[field] = deepcopy(expected[field])
        else:
            output.pop(field, None)
    return output


def extract_operational_fields(canonical_record: dict[str, Any]) -> dict[str, Any]:
    fields = (
        "service",
        "mission_types",
        "duration_minutes",
        "custom_spawn_area",
        "availability_window",
        "generation_rules",
        "water_requirements",
        "subsequent_missions",
        "official_metadata",
    )
    return {field: deepcopy(canonical_record[field]) for field in fields if field in canonical_record}
