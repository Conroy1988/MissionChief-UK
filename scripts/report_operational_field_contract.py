#!/usr/bin/env python3

from __future__ import annotations

import json
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
OFFICIAL_PATH = ROOT / "data" / "sources" / "missionchief-uk" / "einsaetze.raw.json"

PERSONNEL_PATHS = (
    ("requirements", "personnel_educations"),
    ("prerequisites", "personnel_educations"),
    ("additional", "personnel_educations"),
)
PRISONER_FIELDS = ("min_possible_prisoners", "max_possible_prisoners")
TIMED_FIELDS = ("guard_mission", "duration", "duration_text", "date_start", "date_end")
OTHER_OPERATIONAL_FIELDS = (
    "swat_personnel",
    "average_min_fire_personnel",
    "average_min_police_personnel",
    "patient_at_end_of_mission",
    "subsequent_mission_only",
    "uses_custom_spawn_area",
)


def read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"{path.relative_to(ROOT)}: unable to read JSON: {exc}") from exc


def type_name(value: Any) -> str:
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "boolean"
    if isinstance(value, int):
        return "integer"
    if isinstance(value, float):
        return "number"
    if isinstance(value, str):
        return "string"
    if isinstance(value, list):
        return "array"
    if isinstance(value, dict):
        return "object"
    return type(value).__name__


def mission_summary(record: dict[str, Any], value: Any) -> dict[str, Any]:
    additional = record.get("additional")
    return {
        "id": record.get("id"),
        "name": record.get("name"),
        "filter_id": additional.get("filter_id") if isinstance(additional, dict) else None,
        "value": value,
        "official_url": record.get("official_url") or f"https://www.missionchief.co.uk/einsaetze/{record.get('id')}",
    }


def audit() -> dict[str, Any]:
    envelope = read_json(OFFICIAL_PATH)
    records = envelope.get("records") if isinstance(envelope, dict) else None
    if not isinstance(records, list):
        raise ValueError("Official UK mission records must be an array")

    personnel_counts: dict[str, Counter[str]] = {
        f"{root}.{field}": Counter() for root, field in PERSONNEL_PATHS
    }
    personnel_types: dict[str, Counter[str]] = {
        f"{root}.{field}": Counter() for root, field in PERSONNEL_PATHS
    }
    personnel_examples: dict[str, dict[str, list[dict[str, Any]]]] = {
        f"{root}.{field}": defaultdict(list) for root, field in PERSONNEL_PATHS
    }
    prisoner_counts: Counter[str] = Counter()
    prisoner_types: dict[str, Counter[str]] = {field: Counter() for field in PRISONER_FIELDS}
    prisoner_examples: dict[str, list[dict[str, Any]]] = {field: [] for field in PRISONER_FIELDS}
    timed_counts: Counter[str] = Counter()
    timed_types: dict[str, Counter[str]] = {field: Counter() for field in TIMED_FIELDS}
    timed_examples: dict[str, list[dict[str, Any]]] = {field: [] for field in TIMED_FIELDS}
    other_counts: Counter[str] = Counter()
    other_types: dict[str, Counter[str]] = {field: Counter() for field in OTHER_OPERATIONAL_FIELDS}
    generator_counts: Counter[str] = Counter()

    valid_records = 0
    for record in records:
        if not isinstance(record, dict) or record.get("id") is None:
            continue
        valid_records += 1
        additional = record.get("additional")
        if isinstance(additional, dict):
            generator_counts[str(additional.get("filter_id"))] += 1

        for root, field in PERSONNEL_PATHS:
            container = record.get(root)
            if not isinstance(container, dict) or field not in container:
                continue
            value = container[field]
            path = f"{root}.{field}"
            personnel_types[path][type_name(value)] += 1
            if not isinstance(value, dict):
                continue
            for role, quantity in value.items():
                role_text = str(role)
                personnel_counts[path][role_text] += 1
                if len(personnel_examples[path][role_text]) < 4:
                    personnel_examples[path][role_text].append(mission_summary(record, quantity))

        if isinstance(additional, dict):
            for field in PRISONER_FIELDS:
                if field not in additional:
                    continue
                value = additional[field]
                prisoner_counts[field] += 1
                prisoner_types[field][type_name(value)] += 1
                if len(prisoner_examples[field]) < 10:
                    prisoner_examples[field].append(mission_summary(record, value))
            for field in TIMED_FIELDS:
                if field not in additional:
                    continue
                value = additional[field]
                timed_counts[field] += 1
                timed_types[field][type_name(value)] += 1
                if len(timed_examples[field]) < 8:
                    timed_examples[field].append(mission_summary(record, value))
            for field in OTHER_OPERATIONAL_FIELDS:
                if field not in additional:
                    continue
                value = additional[field]
                other_counts[field] += 1
                other_types[field][type_name(value)] += 1

    personnel: dict[str, Any] = {}
    for path in sorted(personnel_counts):
        personnel[path] = {
            "record_count": sum(personnel_types[path].values()),
            "types": dict(sorted(personnel_types[path].items())),
            "role_count": len(personnel_counts[path]),
            "roles": [
                {
                    "key": role,
                    "record_count": count,
                    "examples": personnel_examples[path][role],
                }
                for role, count in sorted(
                    personnel_counts[path].items(),
                    key=lambda item: (-item[1], item[0]),
                )
            ],
        }

    return {
        "schema_version": "1",
        "official_count": valid_records,
        "personnel_educations": personnel,
        "prisoners": {
            field: {
                "count": prisoner_counts[field],
                "types": dict(sorted(prisoner_types[field].items())),
                "examples": prisoner_examples[field],
            }
            for field in PRISONER_FIELDS
        },
        "timed_missions": {
            field: {
                "count": timed_counts[field],
                "types": dict(sorted(timed_types[field].items())),
                "examples": timed_examples[field],
            }
            for field in TIMED_FIELDS
        },
        "other_operational_fields": {
            field: {
                "count": other_counts[field],
                "types": dict(sorted(other_types[field].items())),
            }
            for field in OTHER_OPERATIONAL_FIELDS
        },
        "generator_families": dict(sorted(generator_counts.items(), key=lambda item: (-item[1], item[0]))),
    }


def main() -> int:
    try:
        result = audit()
    except ValueError as exc:
        print(f"Operational field contract reporting failed: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
