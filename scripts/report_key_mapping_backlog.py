#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from conditional_resource_contract import (
    build_expected_conditionals,
    load_mapping_registry as load_conditional_mappings,
    owned_paths as conditional_owned_paths,
)
from patient_contract import load_mapping_registry, patient_owned_paths
from recovery_contract import (
    build_expected_recovery,
    load_mapping_registry as load_recovery_mappings,
    owned_additional_keys as recovery_owned_additional_keys,
)
from personnel_education_contract import (
    build_expected_personnel_educations,
    load_mapping_registry as load_personnel_education_mappings,
    owned_paths as personnel_education_owned_paths,
)

ROOT = Path(__file__).resolve().parents[1]
OFFICIAL_PATH = ROOT / "data" / "sources" / "missionchief-uk" / "einsaetze.raw.json"
MAPPINGS_PATH = ROOT / "data" / "uk" / "official-key-mappings.json"
CANONICAL_ROOT = ROOT / "data" / "uk" / "missions"
KEY_GROUPS = ("requirements", "chances", "prerequisites")
RELATIONSHIP_KEYS = ("expansion_missions_ids", "followup_missions_ids")
PATIENT_MAPPINGS = load_mapping_registry()
CONDITIONAL_MAPPINGS = load_conditional_mappings()
PERSONNEL_EDUCATION_MAPPINGS = load_personnel_education_mappings()
RECOVERY_MAPPINGS = load_recovery_mappings()
RECOVERY_ADDITIONAL_KEYS = recovery_owned_additional_keys(RECOVERY_MAPPINGS)
PATIENT_ADDITIONAL_KEYS, PATIENT_CHANCE_KEYS = patient_owned_paths(PATIENT_MAPPINGS)
(
    CONDITIONAL_REQUIREMENT_KEYS,
    CONDITIONAL_CHANCE_KEYS,
    CONDITIONAL_ADDITIONAL_KEYS,
    CONDITIONAL_RESOURCES,
) = conditional_owned_paths(CONDITIONAL_MAPPINGS)
(
    PERSONNEL_EDUCATION_REQUIREMENT_KEYS,
    PERSONNEL_EDUCATION_PREREQUISITE_KEYS,
    PERSONNEL_EDUCATION_ADDITIONAL_KEYS,
    PERSONNEL_EDUCATION_ROLES,
) = personnel_education_owned_paths(PERSONNEL_EDUCATION_MAPPINGS)
SAFE_ADDITIONAL_KEYS = {
    "filter_id",
    *RELATIONSHIP_KEYS,
    *PATIENT_ADDITIONAL_KEYS,
    *CONDITIONAL_ADDITIONAL_KEYS,
    *PERSONNEL_EDUCATION_ADDITIONAL_KEYS,
    *RECOVERY_ADDITIONAL_KEYS,
}
SAFE_GENERATOR_FAMILIES = {
    "firehouse_missions",
    "police_station_missions",
    "ambulance_station_missions",
    "tow_trucks_missions",
}


def read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"{path.relative_to(ROOT)}: unable to read JSON: {exc}") from exc


def mission_name(record: dict[str, Any]) -> str:
    value = record.get("name") or record.get("caption") or record.get("title")
    return str(value).strip() if value is not None else ""


def canonical_ids() -> set[str]:
    result: set[str] = set()
    for path in CANONICAL_ROOT.glob("*.json"):
        record = read_json(path)
        if isinstance(record, dict) and record.get("id") is not None:
            result.add(str(record["id"]))
    return result


def load_mapped_keys() -> dict[str, set[str]]:
    registry = read_json(MAPPINGS_PATH)
    if not isinstance(registry, dict):
        raise ValueError("Official key mapping registry must be an object")
    result: dict[str, set[str]] = {}
    for group in KEY_GROUPS:
        values = registry.get(group)
        if not isinstance(values, dict):
            raise ValueError(f"Official key mapping group {group} must be an object")
        result[group] = {str(key) for key in values}
    result["requirements"].update(CONDITIONAL_REQUIREMENT_KEYS)
    result["chances"].update(CONDITIONAL_CHANCE_KEYS)
    result["requirements"].update(PERSONNEL_EDUCATION_REQUIREMENT_KEYS)
    result["prerequisites"].update(PERSONNEL_EDUCATION_PREREQUISITE_KEYS)
    return result


def record_unmapped_keys(record: dict[str, Any], mapped: dict[str, set[str]]) -> list[tuple[str, str]]:
    result: list[tuple[str, str]] = []
    for group in KEY_GROUPS:
        values = record.get(group, {})
        if not isinstance(values, dict):
            continue
        for key in values:
            key_text = str(key)
            if key_text not in mapped[group]:
                result.append((group, key_text))
    return result


def operational_complexity(record: dict[str, Any]) -> list[str]:
    blockers: list[str] = []
    additional = record.get("additional")
    if isinstance(additional, dict):
        try:
            build_expected_conditionals(record, CONDITIONAL_MAPPINGS)
        except ValueError as exc:
            blockers.append(str(exc))
        try:
            build_expected_personnel_educations(record, PERSONNEL_EDUCATION_MAPPINGS)
        except ValueError as exc:
            blockers.append(str(exc))
        try:
            build_expected_recovery(record, RECOVERY_MAPPINGS)
        except ValueError as exc:
            blockers.append(str(exc))
        unsupported = sorted(set(additional) - SAFE_ADDITIONAL_KEYS)
        blockers.extend(f"additional.{key}" for key in unsupported)
        if additional.get("filter_id") not in SAFE_GENERATOR_FAMILIES:
            blockers.append(f"generator:{additional.get('filter_id')!r}")
        for field in RELATIONSHIP_KEYS:
            values = additional.get(field, [])
            if not isinstance(values, list):
                blockers.append(f"additional.{field}.invalid")
                continue
            counts = Counter(str(value) for value in values)
            if any(count > 1 for count in counts.values()):
                blockers.append(f"additional.{field}.duplicate-multiplicity")
    elif additional not in (None, {}):
        blockers.append("additional")

    mission_id = record.get("id")
    base_mission_id = record.get("base_mission_id")
    if base_mission_id is not None and str(base_mission_id) != str(mission_id):
        blockers.append(f"variant:{base_mission_id}")
    for key in ("overlay_index", "additive_overlays", "generated_by"):
        if record.get(key) not in (None, "", []):
            blockers.append(key)
    return blockers


def build_report(example_limit: int) -> dict[str, Any]:
    envelope = read_json(OFFICIAL_PATH)
    if not isinstance(envelope, dict) or not isinstance(envelope.get("records"), list):
        raise ValueError("Official UK mission source envelope is invalid")
    records = [record for record in envelope["records"] if isinstance(record, dict) and record.get("id") is not None]
    mapped = load_mapped_keys()
    existing = canonical_ids()

    counts: Counter[tuple[str, str]] = Counter()
    single_key_unlocks: Counter[tuple[str, str]] = Counter()
    examples: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)

    for record in records:
        if str(record["id"]) in existing:
            continue
        unmapped = record_unmapped_keys(record, mapped)
        complexity = operational_complexity(record)
        for group, key in unmapped:
            identity = (group, key)
            counts[identity] += 1
            if len(examples[identity]) < example_limit:
                value_group = record.get(group, {})
                examples[identity].append(
                    {
                        "id": record.get("id"),
                        "name": mission_name(record),
                        "value": value_group.get(key) if isinstance(value_group, dict) else None,
                        "average_credits": record.get("average_credits"),
                        "filter_id": record.get("additional", {}).get("filter_id")
                        if isinstance(record.get("additional"), dict)
                        else None,
                        "other_unmapped_keys": [
                            f"{other_group}.{other_key}"
                            for other_group, other_key in unmapped
                            if (other_group, other_key) != identity
                        ],
                        "operational_complexity": complexity,
                        "official_url": f"https://www.missionchief.co.uk/einsaetze/{record.get('id')}",
                    }
                )
        if len(unmapped) == 1 and not complexity:
            single_key_unlocks[unmapped[0]] += 1

    entries = [
        {
            "group": group,
            "key": key,
            "remaining_mission_count": counts[(group, key)],
            "single_key_unlock_count": single_key_unlocks[(group, key)],
            "examples": examples[(group, key)],
        }
        for group, key in counts
    ]
    entries.sort(
        key=lambda item: (
            -item["single_key_unlock_count"],
            -item["remaining_mission_count"],
            item["group"],
            item["key"],
        )
    )

    return {
        "schema_version": "2",
        "official_count": len(records),
        "canonical_count": len(existing),
        "patient_contract_fields": len(PATIENT_MAPPINGS),
        "conditional_resource_contracts": len(CONDITIONAL_MAPPINGS),
        "personnel_education_roles": len(PERSONNEL_EDUCATION_MAPPINGS["roles"]),
        "recovery_asset_contracts": len(RECOVERY_MAPPINGS),
        "mapped_key_counts": {group: len(mapped[group]) for group in KEY_GROUPS},
        "unmapped_key_count": len(entries),
        "entries": entries,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Rank unmapped official UK mission keys by canonicalisation leverage")
    parser.add_argument("--limit", type=int, default=100, help="Maximum key entries to print")
    parser.add_argument("--examples", type=int, default=5, help="Maximum mission examples retained per key")
    parser.add_argument("--key", help="Print only an exact official key across all groups")
    args = parser.parse_args()

    try:
        report = build_report(max(1, args.examples))
    except ValueError as exc:
        print(f"Official key mapping backlog reporting failed: {exc}", file=sys.stderr)
        return 1

    entries = report["entries"]
    if args.key:
        entries = [entry for entry in entries if entry["key"] == args.key]
    else:
        entries = entries[: max(0, args.limit)]
    output = dict(report)
    output["entries"] = entries
    print(json.dumps(output, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
