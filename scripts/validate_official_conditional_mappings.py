#!/usr/bin/env python3

from __future__ import annotations

import json
import math
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
OFFICIAL_PATH = ROOT / "data" / "sources" / "missionchief-uk" / "einsaetze.raw.json"
CANONICAL_ROOT = ROOT / "data" / "uk" / "missions"
REGISTRY_PATH = ROOT / "data" / "uk" / "mission-verification-registry.json"
MAPPING_PATH = ROOT / "data" / "uk" / "official-key-mappings.json"
TRAFFIC_KEY = "traffic_car"
CONDITION_FIELD = "need_traffic_car_only_if_present"
CONDITION_TEXT = "only_when_available"
CONTEXTUAL_TARGET = "requirements.contextual"
CONTEXTUAL_PROBABILITY_TARGET = "requirements.contextual-probability"
PROMOTED_STAGES = {"requirements-mapped", "operationally-verified", "fully-canonical"}

TrafficValue = tuple[str, int, float | None]


def read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"{path.relative_to(ROOT)}: unable to read JSON: {exc}") from exc


def records_by_id(records: Any, label: str) -> dict[str, dict[str, Any]]:
    if not isinstance(records, list):
        raise ValueError(f"{label} records must be an array")
    result: dict[str, dict[str, Any]] = {}
    for index, record in enumerate(records):
        if not isinstance(record, dict) or record.get("id") is None:
            raise ValueError(f"{label} record {index} is invalid")
        key = str(record["id"])
        if key in result:
            raise ValueError(f"{label} repeats mission id {key}")
        result[key] = record
    return result


def canonical_records() -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    for path in sorted(CANONICAL_ROOT.glob("*.json")):
        record = read_json(path)
        if not isinstance(record, dict) or record.get("id") is None:
            raise ValueError(f"{path.relative_to(ROOT)}: canonical mission is invalid")
        key = str(record["id"])
        if key in result:
            raise ValueError(f"Canonical mission id {key} is duplicated")
        result[key] = record
    return result


def validate_mapping_contract() -> None:
    registry = read_json(MAPPING_PATH)
    if not isinstance(registry, dict):
        raise ValueError("Official key mapping registry must be an object")
    requirements = registry.get("requirements")
    chances = registry.get("chances")
    if not isinstance(requirements, dict) or not isinstance(chances, dict):
        raise ValueError("Official key mapping requirement and chance groups must be objects")

    requirement = requirements.get(TRAFFIC_KEY)
    chance = chances.get(TRAFFIC_KEY)
    if not isinstance(requirement, dict) or requirement.get("status") != "verified":
        raise ValueError("requirements.traffic_car must have a verified mapping")
    if requirement.get("canonical_target") != CONTEXTUAL_TARGET:
        raise ValueError(f"requirements.traffic_car must target {CONTEXTUAL_TARGET}")
    if requirement.get("canonical_id") != TRAFFIC_KEY:
        raise ValueError("requirements.traffic_car must target canonical traffic_car")
    if requirement.get("condition_path") != f"additional.{CONDITION_FIELD}":
        raise ValueError("requirements.traffic_car has the wrong condition_path")
    if requirement.get("condition_value") is not True:
        raise ValueError("requirements.traffic_car has the wrong condition_value")
    if requirement.get("condition") != CONDITION_TEXT:
        raise ValueError("requirements.traffic_car has the wrong canonical condition")

    if not isinstance(chance, dict) or chance.get("status") != "verified":
        raise ValueError("chances.traffic_car must have a verified mapping")
    if chance.get("canonical_target") != CONTEXTUAL_PROBABILITY_TARGET:
        raise ValueError(f"chances.traffic_car must target {CONTEXTUAL_PROBABILITY_TARGET}")
    if chance.get("canonical_id") != TRAFFIC_KEY or chance.get("requirement_key") != TRAFFIC_KEY:
        raise ValueError("chances.traffic_car must link to canonical and official traffic_car")


def checked_quantity(value: Any, label: str) -> int:
    if not isinstance(value, int) or isinstance(value, bool) or value < 0:
        raise ValueError(f"{label} must be a non-negative integer")
    return value


def checked_percent(value: Any, label: str) -> int:
    if not isinstance(value, int) or isinstance(value, bool) or not 0 <= value <= 100:
        raise ValueError(f"{label} must be an integer percentage from 0 to 100")
    return value


def expected_traffic_car(record: dict[str, Any]) -> TrafficValue | None:
    mission_id = str(record.get("id"))
    requirements = record.get("requirements", {})
    chances = record.get("chances", {})
    additional = record.get("additional", {})
    if not isinstance(requirements, dict) or not isinstance(chances, dict) or not isinstance(additional, dict):
        raise ValueError(f"Official mission {mission_id} requirements, chances or additional fields are invalid")

    has_requirement = TRAFFIC_KEY in requirements
    has_chance = TRAFFIC_KEY in chances
    if has_chance and not has_requirement:
        raise ValueError(f"Official mission {mission_id} publishes a Traffic Car chance without a quantity")
    if not has_requirement:
        return None

    raw_flag = additional.get(CONDITION_FIELD)
    if CONDITION_FIELD in additional and not isinstance(raw_flag, bool):
        raise ValueError(f"Official mission {mission_id} additional.{CONDITION_FIELD} must be a boolean")
    conditional = raw_flag is True

    quantity = checked_quantity(requirements[TRAFFIC_KEY], f"Mission {mission_id} requirements.traffic_car")
    percent = 100
    if has_chance:
        percent = checked_percent(chances[TRAFFIC_KEY], f"Mission {mission_id} chances.traffic_car")
    if quantity == 0 or percent == 0:
        return None

    probability = None if percent == 100 else percent / 100
    if conditional:
        return "conditional", quantity, probability
    if probability is None:
        return "guaranteed", quantity, None
    return "probabilistic", quantity, probability


def checked_probability(value: Any, label: str) -> float:
    if (
        not isinstance(value, (int, float))
        or isinstance(value, bool)
        or not 0 < float(value) < 1
    ):
        raise ValueError(f"{label} must be greater than 0 and less than 1")
    return float(value)


def actual_traffic_car(record: dict[str, Any]) -> TrafficValue | None:
    mission_id = str(record.get("id"))
    requirements = record.get("requirements")
    if not isinstance(requirements, dict):
        raise ValueError(f"Canonical mission {mission_id} has no requirements object")

    found: list[TrafficValue] = []
    guaranteed = requirements.get("guaranteed", [])
    if not isinstance(guaranteed, list):
        raise ValueError(f"Canonical mission {mission_id} requirements.guaranteed must be an array")
    for item in guaranteed:
        if not isinstance(item, dict) or item.get("resource") != TRAFFIC_KEY:
            continue
        quantity = item.get("quantity")
        if not isinstance(quantity, int) or isinstance(quantity, bool) or quantity < 1:
            raise ValueError(f"Canonical mission {mission_id} has an invalid guaranteed Traffic Car quantity")
        found.append(("guaranteed", quantity, None))

    probabilistic = requirements.get("probabilistic", [])
    if not isinstance(probabilistic, list):
        raise ValueError(f"Canonical mission {mission_id} requirements.probabilistic must be an array")
    for item in probabilistic:
        if not isinstance(item, dict) or item.get("resource") != TRAFFIC_KEY:
            continue
        quantity = item.get("quantity")
        if not isinstance(quantity, int) or isinstance(quantity, bool) or quantity < 1:
            raise ValueError(f"Canonical mission {mission_id} has an invalid probabilistic Traffic Car quantity")
        found.append(
            (
                "probabilistic",
                quantity,
                checked_probability(item.get("probability"), f"Canonical mission {mission_id} Traffic Car probability"),
            )
        )

    conditional = requirements.get("conditional", [])
    if not isinstance(conditional, list):
        raise ValueError(f"Canonical mission {mission_id} requirements.conditional must be an array")
    for item in conditional:
        if not isinstance(item, dict) or item.get("resource") != TRAFFIC_KEY:
            continue
        quantity = item.get("quantity")
        if not isinstance(quantity, int) or isinstance(quantity, bool) or quantity < 1:
            raise ValueError(f"Canonical mission {mission_id} has an invalid conditional Traffic Car quantity")
        if item.get("condition") != CONDITION_TEXT:
            raise ValueError(f"Canonical mission {mission_id} has an invalid Traffic Car condition")
        raw_probability = item.get("probability")
        probability = None if raw_probability is None else checked_probability(
            raw_probability,
            f"Canonical mission {mission_id} conditional Traffic Car probability",
        )
        found.append(("conditional", quantity, probability))

    alternatives = requirements.get("alternatives", [])
    if not isinstance(alternatives, list):
        raise ValueError(f"Canonical mission {mission_id} requirements.alternatives must be an array")
    if any(
        isinstance(item, dict)
        and isinstance(item.get("resources"), list)
        and TRAFFIC_KEY in item["resources"]
        for item in alternatives
    ):
        raise ValueError(f"Canonical mission {mission_id} stores Traffic Car in an alternative group")

    if len(found) > 1:
        raise ValueError(f"Canonical mission {mission_id} stores Traffic Car in multiple requirement modes")
    return found[0] if found else None


def values_equal(actual: TrafficValue | None, expected: TrafficValue | None) -> bool:
    if actual is None or expected is None:
        return actual is None and expected is None
    if actual[0] != expected[0] or actual[1] != expected[1]:
        return False
    if actual[2] is None or expected[2] is None:
        return actual[2] is None and expected[2] is None
    return math.isclose(actual[2], expected[2], abs_tol=1e-9)


def audit() -> dict[str, int]:
    validate_mapping_contract()
    official_envelope = read_json(OFFICIAL_PATH)
    if not isinstance(official_envelope, dict):
        raise ValueError("Official mission source envelope must be an object")
    official = records_by_id(official_envelope.get("records"), "Official UK mission source")
    canonical = canonical_records()

    source_records = 0
    source_conditional = 0
    source_ordinary = 0
    source_probabilistic = 0
    for record in official.values():
        requirements = record.get("requirements", {})
        if isinstance(requirements, dict) and TRAFFIC_KEY in requirements:
            source_records += 1
            expected = expected_traffic_car(record)
            if expected is not None:
                if expected[0] == "conditional":
                    source_conditional += 1
                else:
                    source_ordinary += 1
                if expected[2] is not None:
                    source_probabilistic += 1

    registry = read_json(REGISTRY_PATH)
    decisions = registry.get("records") if isinstance(registry, dict) else None
    if not isinstance(decisions, dict):
        raise ValueError("Mission verification registry records must be an object")

    promoted = 0
    promoted_with_traffic = 0
    promoted_conditional = 0
    promoted_ordinary = 0
    for mission_id, decision in decisions.items():
        if not isinstance(decision, dict) or decision.get("stage") not in PROMOTED_STAGES:
            continue
        key = str(mission_id)
        official_record = official.get(key)
        canonical_record = canonical.get(key)
        if official_record is None or canonical_record is None:
            raise ValueError(f"Promoted mission {key} must exist in official and canonical collections")
        expected = expected_traffic_car(official_record)
        actual = actual_traffic_car(canonical_record)
        if not values_equal(actual, expected):
            raise ValueError(
                f"Mission {key} Traffic Car requirement differs: expected={expected!r}, canonical={actual!r}"
            )
        promoted += 1
        if expected is not None:
            promoted_with_traffic += 1
            if expected[0] == "conditional":
                promoted_conditional += 1
            else:
                promoted_ordinary += 1

    return {
        "source_records": source_records,
        "source_conditional": source_conditional,
        "source_ordinary": source_ordinary,
        "source_probabilistic": source_probabilistic,
        "promoted": promoted,
        "promoted_with_traffic": promoted_with_traffic,
        "promoted_conditional": promoted_conditional,
        "promoted_ordinary": promoted_ordinary,
    }


def main() -> int:
    try:
        result = audit()
    except ValueError as exc:
        print(f"Official contextual requirement audit failed: {exc}", file=sys.stderr)
        return 1
    print(
        "Official contextual requirement audit passed: "
        f"{result['source_records']} Traffic Car source records "
        f"({result['source_conditional']} conditional, {result['source_ordinary']} ordinary, "
        f"{result['source_probabilistic']} probabilistic), "
        f"{result['promoted_with_traffic']} promoted Traffic Car missions "
        f"({result['promoted_conditional']} conditional, {result['promoted_ordinary']} ordinary) and "
        f"{result['promoted']} promoted missions checked."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
