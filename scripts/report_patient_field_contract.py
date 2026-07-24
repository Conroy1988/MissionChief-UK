#!/usr/bin/env python3

from __future__ import annotations

import json
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
OFFICIAL_PATH = ROOT / "data" / "sources" / "missionchief-uk" / "einsaetze.raw.json"
PATIENT_ADDITIONAL_KEYS = (
    "possible_patient",
    "possible_patient_min",
    "patient_specialization_captions",
    "patient_specialization_ids",
    "patient_specializations",
    "patient_uk_code_possible",
    "patient_allow_first_responder_chance",
    "patient_at_end_of_mission",
)
PATIENT_CHANCE_KEYS = ("patient_transport", "patient_critical_care")


def read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"{path.relative_to(ROOT)}: unable to read JSON: {exc}") from exc


def value_type(value: Any) -> str:
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


def mission_name(record: dict[str, Any]) -> str:
    value = record.get("name") or record.get("caption") or record.get("title")
    return str(value).strip() if value is not None else ""


def compact_value(value: Any) -> Any:
    if isinstance(value, list) and len(value) > 8:
        return [*value[:8], f"… +{len(value) - 8}"]
    if isinstance(value, str) and len(value) > 120:
        return value[:117] + "…"
    return value


def main() -> int:
    try:
        envelope = read_json(OFFICIAL_PATH)
        if not isinstance(envelope, dict) or not isinstance(envelope.get("records"), list):
            raise ValueError("Official UK mission source envelope is invalid")
        records = [record for record in envelope["records"] if isinstance(record, dict)]
    except ValueError as exc:
        print(f"Patient field contract reporting failed: {exc}", file=sys.stderr)
        return 1

    field_counts: Counter[str] = Counter()
    field_types: dict[str, Counter[str]] = defaultdict(Counter)
    chance_counts: Counter[str] = Counter()
    chance_types: dict[str, Counter[str]] = defaultdict(Counter)
    shape_counts: Counter[tuple[str, ...]] = Counter()
    examples: dict[tuple[str, ...], list[dict[str, Any]]] = defaultdict(list)
    max_without_min = 0
    min_without_max = 0
    patient_records = 0

    for record in records:
        additional = record.get("additional", {})
        chances = record.get("chances", {})
        if not isinstance(additional, dict):
            additional = {}
        if not isinstance(chances, dict):
            chances = {}

        present_additional = [key for key in PATIENT_ADDITIONAL_KEYS if key in additional]
        present_chances = [key for key in PATIENT_CHANCE_KEYS if key in chances]
        present = tuple([*(f"additional.{key}" for key in present_additional), *(f"chances.{key}" for key in present_chances)])
        if not present:
            continue

        patient_records += 1
        shape_counts[present] += 1
        if len(examples[present]) < 4:
            examples[present].append(
                {
                    "id": record.get("id"),
                    "name": mission_name(record),
                    "filter_id": additional.get("filter_id"),
                    "additional": {key: compact_value(additional[key]) for key in present_additional},
                    "chances": {key: chances[key] for key in present_chances},
                }
            )

        for key in present_additional:
            field_counts[key] += 1
            field_types[key][value_type(additional[key])] += 1
        for key in present_chances:
            chance_counts[key] += 1
            chance_types[key][value_type(chances[key])] += 1

        if "possible_patient" in additional and "possible_patient_min" not in additional:
            max_without_min += 1
        if "possible_patient_min" in additional and "possible_patient" not in additional:
            min_without_max += 1

    report = {
        "schema_version": "1",
        "official_count": len(records),
        "patient_record_count": patient_records,
        "additional_fields": [
            {
                "key": key,
                "count": field_counts[key],
                "types": dict(sorted(field_types[key].items())),
            }
            for key in PATIENT_ADDITIONAL_KEYS
        ],
        "chance_fields": [
            {
                "key": key,
                "count": chance_counts[key],
                "types": dict(sorted(chance_types[key].items())),
            }
            for key in PATIENT_CHANCE_KEYS
        ],
        "range_diagnostics": {
            "maximum_without_minimum": max_without_min,
            "minimum_without_maximum": min_without_max,
        },
        "shape_count": len(shape_counts),
        "shapes": [
            {
                "fields": list(shape),
                "count": count,
                "examples": examples[shape],
            }
            for shape, count in sorted(shape_counts.items(), key=lambda item: (-item[1], item[0]))
        ],
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
