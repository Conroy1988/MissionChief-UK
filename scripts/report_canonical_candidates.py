#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any

from conditional_resource_contract import (
    build_expected_conditionals,
    load_mapping_registry as load_conditional_mappings,
    owned_paths as conditional_owned_paths,
)
from patient_contract import build_expected_patient, load_mapping_registry as load_patient_mappings, patient_owned_paths
from personnel_contract import build_expected_personnel, load_mapping_registry as load_personnel_mappings
from personnel_education_contract import (
    build_expected_personnel_educations,
    load_mapping_registry as load_personnel_education_mappings,
    owned_paths as personnel_education_owned_paths,
)
from prisoner_contract import build_expected_prisoners, load_mapping_registry as load_prisoner_mappings, owned_additional_keys
from recovery_contract import (
    build_expected_recovery,
    load_mapping_registry as load_recovery_mappings,
    owned_additional_keys as recovery_owned_additional_keys,
)

ROOT = Path(__file__).resolve().parents[1]
OFFICIAL_PATH = ROOT / "data" / "sources" / "missionchief-uk" / "einsaetze.raw.json"
CANONICAL_ROOT = ROOT / "data" / "uk" / "missions"
KEY_MAPPING_PATH = ROOT / "data" / "uk" / "official-key-mappings.json"

KEY_GROUPS = ("requirements", "chances", "prerequisites")
RELATIONSHIP_KEYS = ("expansion_missions_ids", "followup_missions_ids")
PATIENT_MAPPINGS = load_patient_mappings()
PERSONNEL_MAPPINGS = load_personnel_mappings()
PRISONER_MAPPINGS = load_prisoner_mappings()
CONDITIONAL_MAPPINGS = load_conditional_mappings()
PERSONNEL_EDUCATION_MAPPINGS = load_personnel_education_mappings()
RECOVERY_MAPPINGS = load_recovery_mappings()
RECOVERY_ADDITIONAL_KEYS = recovery_owned_additional_keys(RECOVERY_MAPPINGS)
PATIENT_ADDITIONAL_KEYS, PATIENT_CHANCE_KEYS = patient_owned_paths(PATIENT_MAPPINGS)
PRISONER_ADDITIONAL_KEYS = owned_additional_keys(PRISONER_MAPPINGS)
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
    *PRISONER_ADDITIONAL_KEYS,
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


def stable_id(value: Any) -> tuple[int, int | str]:
    try:
        return (0, int(value))
    except (TypeError, ValueError):
        return (1, str(value))


def mission_name(record: dict[str, Any] | None) -> str:
    if record is None:
        return ""
    value = record.get("name") or record.get("caption") or record.get("title")
    return str(value).strip() if value is not None else ""


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
                if group == "requirements" and str(official_key) in CONDITIONAL_REQUIREMENT_KEYS:
                    continue
                if group == "chances" and str(official_key) in CONDITIONAL_CHANCE_KEYS:
                    continue
                if group == "requirements" and str(official_key) in PERSONNEL_EDUCATION_REQUIREMENT_KEYS:
                    continue
                if group == "prerequisites" and str(official_key) in PERSONNEL_EDUCATION_PREREQUISITE_KEYS:
                    continue
                blockers.append(f"unmapped {group}.{official_key}")
                continue
            if mapping.get("status") == "not-applicable" and value not in mapping.get("allowed_values", []):
                blockers.append(
                    f"{group}.{official_key}={value!r} outside allow-list {mapping.get('allowed_values', [])!r}"
                )
    return blockers


def relationship_blockers(
    additional: dict[str, Any],
    official_by_id: dict[str, dict[str, Any]],
) -> list[str]:
    blockers: list[str] = []
    for field in RELATIONSHIP_KEYS:
        values = additional.get(field, [])
        if not isinstance(values, list):
            blockers.append(f"additional.{field} is not an array")
            continue
        missing = [str(value) for value in values if str(value) not in official_by_id]
        if missing:
            blockers.append(f"unresolved additional.{field}: {', '.join(missing)}")
        counts = Counter(str(value) for value in values)
        duplicates = [f"{value} x{count}" for value, count in sorted(counts.items()) if count > 1]
        if duplicates:
            blockers.append(
                f"duplicate additional.{field} requires relationship multiplicity modelling: {', '.join(duplicates)}"
            )
    return blockers


def operational_blockers(
    record: dict[str, Any],
    official_by_id: dict[str, dict[str, Any]],
) -> list[str]:
    blockers: list[str] = []
    additional = record.get("additional", {})
    if not isinstance(additional, dict):
        blockers.append("additional is not an object")
    else:
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
        if unsupported:
            blockers.append("additional fields require mapping: " + ", ".join(unsupported))
        filter_id = additional.get("filter_id")
        if filter_id not in SAFE_GENERATOR_FAMILIES:
            blockers.append(f"generator family requires review: {filter_id!r}")
        blockers.extend(relationship_blockers(additional, official_by_id))

    mission_id = record.get("id")
    base_mission_id = record.get("base_mission_id")
    if base_mission_id is not None and str(base_mission_id) != str(mission_id):
        blockers.append(f"variant of base mission {base_mission_id} requires explicit modelling")
    if record.get("additive_overlays") not in (None, ""):
        blockers.append("additive overlay requires explicit modelling")
    if record.get("overlay_index") is not None:
        blockers.append("overlay variant requires explicit modelling")
    if record.get("generated_by") not in (None, ""):
        blockers.append("generated_by requires service-family review")
    return blockers


def resolve_relationships(values: Any, official_by_id: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    if not isinstance(values, list):
        return []
    return [
        {"id": value, "name": mission_name(official_by_id.get(str(value)))}
        for value in values
    ]


def candidate_record(
    record: dict[str, Any],
    official_by_id: dict[str, dict[str, Any]],
    duplicate_names: Counter[str],
) -> dict[str, Any]:
    additional = record.get("additional", {}) if isinstance(record.get("additional"), dict) else {}
    mission_id = str(record.get("id"))
    name = mission_name(record)
    slug = slugify(name)
    if duplicate_names[name.casefold()] > 1:
        slug = f"{slug}-{mission_id}"
    output = {
        "id": record.get("id"),
        "name": name,
        "suggested_path": f"data/uk/missions/{slug}.json",
        "average_credits": record.get("average_credits"),
        "mission_categories": record.get("mission_categories", []),
        "place": record.get("place"),
        "place_array": record.get("place_array", []),
        "requirements": record.get("requirements", {}),
        "chances": record.get("chances", {}),
        "prerequisites": record.get("prerequisites", {}),
        "generator_family": additional.get("filter_id"),
        "expansion_missions": resolve_relationships(additional.get("expansion_missions_ids", []), official_by_id),
        "followup_missions": resolve_relationships(additional.get("followup_missions_ids", []), official_by_id),
    }
    patients = build_expected_patient(record, PATIENT_MAPPINGS)
    if patients:
        output["patients"] = patients
    personnel = build_expected_personnel(record, PERSONNEL_MAPPINGS)
    if personnel:
        output["personnel"] = personnel
    prisoners = build_expected_prisoners(record, PRISONER_MAPPINGS)
    if prisoners:
        output["prisoners"] = prisoners
    conditionals = build_expected_conditionals(record, CONDITIONAL_MAPPINGS)
    if conditionals:
        output["conditional_requirements"] = conditionals
    personnel_educations = build_expected_personnel_educations(
        record, PERSONNEL_EDUCATION_MAPPINGS
    )
    if personnel_educations:
        output["personnel_educations"] = personnel_educations
    recovery = build_expected_recovery(record, RECOVERY_MAPPINGS)
    if recovery:
        output["recovery"] = recovery
    return output


def report() -> dict[str, Any]:
    envelope = read_json(OFFICIAL_PATH)
    if not isinstance(envelope, dict) or not isinstance(envelope.get("records"), list):
        raise ValueError("Official UK mission source envelope is invalid")

    records = [record for record in envelope["records"] if isinstance(record, dict) and record.get("id") is not None]
    official_by_id = {str(record["id"]): record for record in records}
    duplicate_names = Counter(mission_name(record).casefold() for record in records)
    existing = canonical_ids()
    mappings = mapped_keys()
    ready: list[dict[str, Any]] = []
    blocked: list[dict[str, Any]] = []

    for record in records:
        mission_id = str(record["id"])
        if mission_id in existing:
            continue

        blockers = key_blockers(record, mappings) + operational_blockers(record, official_by_id)
        if blockers:
            blocked.append({"id": record.get("id"), "name": mission_name(record), "blockers": blockers})
        else:
            ready.append(candidate_record(record, official_by_id, duplicate_names))

    ready.sort(key=lambda item: stable_id(item["id"]))
    blocked.sort(key=lambda item: stable_id(item["id"]))
    return {
        "schema_version": "7",
        "official_count": len(records),
        "canonical_count": len(existing),
        "patient_contract_fields": len(PATIENT_MAPPINGS),
        "conditional_resource_contracts": len(CONDITIONAL_MAPPINGS),
        "personnel_education_roles": len(PERSONNEL_EDUCATION_MAPPINGS["roles"]),
        "recovery_asset_contracts": len(RECOVERY_MAPPINGS),
        "personnel_contract_roles": len(PERSONNEL_MAPPINGS),
        "prisoner_contract_fields": len(PRISONER_MAPPINGS),
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
        "patient_contract_fields": result["patient_contract_fields"],
        "conditional_resource_contracts": result["conditional_resource_contracts"],
        "personnel_education_roles": result["personnel_education_roles"],
        "recovery_asset_contracts": result["recovery_asset_contracts"],
        "personnel_contract_roles": result["personnel_contract_roles"],
        "prisoner_contract_fields": result["prisoner_contract_fields"],
        "ready_count": result["ready_count"],
        "blocked_count": result["blocked_count"],
        "ready": result["ready"][: max(0, args.limit)],
        "blocked": result["blocked"][: max(0, args.blocked_limit)],
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
