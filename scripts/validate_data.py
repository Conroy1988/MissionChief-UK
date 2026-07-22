#!/usr/bin/env python3

from __future__ import annotations

import json
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
DATA_ROOT = ROOT / "data" / "uk"
SCHEMA_ROOT = ROOT / "data" / "schema"

SCHEMA_BY_DIRECTORY = {
    "vehicle": "vehicle.schema.json",
    "vehicles": "vehicle.schema.json",
    "mission": "mission.schema.json",
    "missions": "mission.schema.json",
}


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def schema_for(path: Path) -> Path | None:
    schema_name = SCHEMA_BY_DIRECTORY.get(path.parent.name.lower())
    if schema_name is None:
        return None
    return SCHEMA_ROOT / schema_name


def format_error(path: Path, error: Any) -> str:
    location = ".".join(str(part) for part in error.absolute_path) or "<root>"
    return f"{path.relative_to(ROOT)} [{location}]: {error.message}"


def mission_resource_references(path: Path, record: dict[str, Any]) -> list[tuple[Path, str, str]]:
    references: list[tuple[Path, str, str]] = []
    requirements = record.get("requirements", {})
    if not isinstance(requirements, dict):
        return references

    for requirement_type in ("guaranteed", "probabilistic"):
        entries = requirements.get(requirement_type, [])
        if not isinstance(entries, list):
            continue
        for entry in entries:
            if isinstance(entry, dict) and isinstance(entry.get("resource"), str):
                references.append((path, requirement_type, entry["resource"]))
    return references


def main() -> int:
    failures: list[str] = []
    warnings: list[str] = []
    seen_ids: dict[str, dict[str, Path]] = defaultdict(dict)
    schema_cache: dict[Path, Draft202012Validator] = {}
    vehicle_ids: set[str] = set()
    mission_resources: list[tuple[Path, str, str]] = []
    files = sorted(DATA_ROOT.rglob("*.json"))

    for path in files:
        try:
            record = load_json(path)
        except (OSError, json.JSONDecodeError) as exc:
            failures.append(f"{path.relative_to(ROOT)}: {exc}")
            continue

        schema_path = schema_for(path)
        if schema_path is None:
            warnings.append(
                f"{path.relative_to(ROOT)}: no schema mapping for directory '{path.parent.name}'"
            )
            continue

        try:
            validator = schema_cache.get(schema_path)
            if validator is None:
                schema = load_json(schema_path)
                Draft202012Validator.check_schema(schema)
                validator = Draft202012Validator(schema, format_checker=FormatChecker())
                schema_cache[schema_path] = validator
        except Exception as exc:
            failures.append(f"{schema_path.relative_to(ROOT)}: schema load failed: {exc}")
            continue

        for error in sorted(validator.iter_errors(record), key=lambda item: list(item.absolute_path)):
            failures.append(format_error(path, error))

        kind = path.parent.name.lower()
        if isinstance(record, dict) and "id" in record:
            record_id = str(record["id"])
            previous = seen_ids[kind].get(record_id)
            if previous is not None:
                failures.append(
                    f"{path.relative_to(ROOT)}: duplicate id '{record_id}' also used by "
                    f"{previous.relative_to(ROOT)}"
                )
            else:
                seen_ids[kind][record_id] = path

            if kind in {"vehicle", "vehicles"}:
                vehicle_ids.add(record_id)

        if kind in {"mission", "missions"} and isinstance(record, dict):
            mission_resources.extend(mission_resource_references(path, record))

    for path, requirement_type, resource_id in mission_resources:
        if resource_id not in vehicle_ids:
            failures.append(
                f"{path.relative_to(ROOT)} [{requirement_type}]: resource '{resource_id}' "
                "does not have a matching record under data/uk/vehicles"
            )

    if warnings:
        print("Structured data validation warnings:")
        for warning in warnings:
            print(f"- {warning}")

    if failures:
        print("Structured data validation failed:")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print(
        f"Validated {len(files)} structured data file(s) successfully, including "
        f"{len(mission_resources)} mission resource reference(s)."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
