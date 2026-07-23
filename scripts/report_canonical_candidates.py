#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
OFFICIAL_PATH = ROOT / "data" / "sources" / "missionchief-uk" / "einsaetze.raw.json"
CANONICAL_ROOT = ROOT / "data" / "uk" / "missions"
KEY_MAPPING_PATH = ROOT / "data" / "uk" / "official-key-mappings.json"

KEY_GROUPS = ("requirements", "chances", "prerequisites")
SAFE_ADDITIONAL_KEYS = {
    "filter_id",
    "expansion_missions_ids",
    "followup_missions_ids",
}


def read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"{path.relative_to(ROOT)}: unable to read JSON: {exc}") from exc


def stable_id(value: Any) -> tuple[int, int | str]:
    try:
        return (0, int(value))
    except (TypeError, ValueError):
        return (1, str(value))


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.casefold()).strip("-")
    return slug or "mission"


def canonical_ids() -> set[str]:
    result: set[str] = set()
    for path in CANONICAL_ROOT.glob("*.json"):
        record = read_json(path)
        if isinstance(record, dict) and record.get("id") is not None:
            result.add(str(record["id"]))
    return result


def mapped_keys() -> dict[str, dict[str, dict[str, Any]]]:
    registry = read_json(KEY_MAPPING_PATH)
    if not isinstance(registry, dict):
        raise ValueError("Official key mapping registry must be an object")
    result: dict[str, dict[str, dict[str, Any]]] = {}
    for group in KEY_GROUPS:
        mappings = registry.get(group)
        if not isinstance(mappings, dict):
            raise ValueError(f"Official key mapping group {group} must be an object")
        result[group] = mappings
    return result


def key_blockers(record: dict[str, Any], mappings: dict[str, dict[str, dict[str, Any]]]) -> list[str]:
    blockers: list[str] = []
    for group in KEY_GROUPS:
        values = record.get(group, {})
        if not isinstance(values, dict):
            blockers.append(f"{group} is not an object")
            continue
        for official_key, value in values.items():
            mapping = mappings[group].get(str(official_key))
            if mapping is None:
                blockers.append(f"unmapped {group}.{official_key}")
                continue
            if mapping.get("status") == "not-applicable" and value not in mapping.get("allowed_values", []):
                blockers.append(
                    f"{group}.{official_key}={value!r} outside allow-list {mapping.get('allowed_values', [])!r}"
                )
    return blockers


def operational_blockers(record: dict[str, Any]) -> list[str]:
    blockers: list[str] = []
    additional = record.get("additional", {})
    if not isinstance(additional, dict):
        blockers.append("additional is not an object")
    else:
        unsupported = sorted(set(additional) - SAFE_ADDITIONAL_KEYS)
        if unsupported:
            blockers.append("additional fields require mapping: " + ", ".join(unsupported))
        filter_id = additional.get("filter_id")
        if filter_id != "firehouse_missions":
            blockers.append(f"generator family requires review: {filter_id!r}")

    if record.get("additive_overlays") not in (None, ""):
        blockers.append("additive overlay requires explicit modelling")
    if record.get("overlay_index") is not None:
        blockers.append("overlay variant requires explicit modelling")
    if record.get("generated_by") not in (None, ""):
        blockers.append("generated_by requires service-family review")
    return blockers


def candidate_record(record: dict[str, Any]) -> dict[str, Any]:
    additional = record.get("additional", {}) if isinstance(record.get("additional"), dict) else {}
    return {
        "id": record.get("id"),
        "name": record.get("name"),
        "suggested_path": f"data/uk/missions/{slugify(str(record.get('name', 'mission')))}.json",
        "average_credits": record.get("average_credits"),
        "mission_categories": record.get("mission_categories", []),
        "place": record.get("place"),
        "place_array": record.get("place_array", []),
        "requirements": record.get("requirements", {}),
        "chances": record.get("chances", {}),
        "prerequisites": record.get("prerequisites", {}),
        "expansion_missions_ids": additional.get("expansion_missions_ids", []),
        "followup_missions_ids": additional.get("followup_missions_ids", []),
    }


def report() -> dict[str, Any]:
    envelope = read_json(OFFICIAL_PATH)
    if not isinstance(envelope, dict) or not isinstance(envelope.get("records"), list):
        raise ValueError("Official UK mission source envelope is invalid")

    existing = canonical_ids()
    mappings = mapped_keys()
    ready: list[dict[str, Any]] = []
    blocked: list[dict[str, Any]] = []

    for record in envelope["records"]:
        if not isinstance(record, dict) or record.get("id") is None:
            continue
        mission_id = str(record["id"])
        if mission_id in existing:
            continue

        blockers = key_blockers(record, mappings) + operational_blockers(record)
        if blockers:
            blocked.append({
                "id": record.get("id"),
                "name": record.get("name"),
                "blockers": blockers,
            })
        else:
            ready.append(candidate_record(record))

    ready.sort(key=lambda item: stable_id(item["id"]))
    blocked.sort(key=lambda item: stable_id(item["id"]))
    return {
        "schema_version": "1",
        "official_count": len(envelope["records"]),
        "canonical_count": len(existing),
        "ready_count": len(ready),
        "blocked_count": len(blocked),
        "ready": ready,
        "blocked": blocked,
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Report evidence-safe canonical mission candidates from the retained official UK snapshot"
    )
    parser.add_argument("--limit", type=int, default=40, help="Maximum ready candidates to print")
    parser.add_argument("--blocked-limit", type=int, default=0, help="Maximum blocked candidates to print")
    args = parser.parse_args()

    try:
        result = report()
    except ValueError as exc:
        print(f"Canonical candidate reporting failed: {exc}", file=sys.stderr)
        return 1

    output = {
        "schema_version": result["schema_version"],
        "official_count": result["official_count"],
        "canonical_count": result["canonical_count"],
        "ready_count": result["ready_count"],
        "blocked_count": result["blocked_count"],
        "ready": result["ready"][: max(0, args.limit)],
        "blocked": result["blocked"][: max(0, args.blocked_limit)],
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
