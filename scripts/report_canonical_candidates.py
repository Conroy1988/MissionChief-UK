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
VERIFICATION_REGISTRY_PATH = ROOT / "data" / "uk" / "mission-verification-registry.json"
VERIFICATION_BATCH_ROOT = ROOT / "data" / "uk" / "mission-verification-batches"

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
    "coastal_rescue_missions",
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


def canonical_records_by_id() -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    for path in sorted(CANONICAL_ROOT.glob("*.json")):
        record = read_json(path)
        if isinstance(record, dict) and record.get("id") is not None:
            mission_id = str(record["id"])
            if mission_id in result:
                raise ValueError(f"Canonical mission id {mission_id} is repeated in {path.relative_to(ROOT)}")
            result[mission_id] = {
                "record": record,
                "path": path.relative_to(ROOT).as_posix(),
            }
    return result


def canonical_ids() -> set[str]:
    return set(canonical_records_by_id())


def merge_verification_decision_documents(
    documents: list[tuple[str, Any]],
) -> dict[str, dict[str, Any]]:
    decisions: dict[str, dict[str, Any]] = {}
    sources: dict[str, str] = {}
    for label, document in documents:
        if not isinstance(document, dict) or document.get("schema_version") != "1":
            raise ValueError(f"{label}: schema_version must be '1'")
        records = document.get("records")
        if not isinstance(records, dict):
            raise ValueError(f"{label}: records must be an object")
        for mission_id, decision in records.items():
            key = str(mission_id)
            if not isinstance(decision, dict):
                raise ValueError(f"{label}: decision {key} must be an object")
            if key in decisions:
                if decisions[key] != decision:
                    raise ValueError(
                        f"Conflicting mission verification decision {key} in {sources[key]} and {label}"
                    )
                continue
            decisions[key] = decision
            sources[key] = label
    return decisions


def effective_verification_decisions() -> dict[str, dict[str, Any]]:
    documents = [
        (
            VERIFICATION_REGISTRY_PATH.relative_to(ROOT).as_posix(),
            read_json(VERIFICATION_REGISTRY_PATH),
        )
    ]
    documents.extend(
        (path.relative_to(ROOT).as_posix(), read_json(path))
        for path in sorted(VERIFICATION_BATCH_ROOT.glob("*.json"))
    )
    return merge_verification_decision_documents(documents)


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


def is_known_key(
    group: str,
    official_key: str,
    mappings: dict[str, dict[str, dict[str, Any]]],
) -> bool:
    if official_key in mappings[group]:
        return True
    if group == "requirements" and official_key in CONDITIONAL_REQUIREMENT_KEYS:
        return True
    if group == "chances" and official_key in CONDITIONAL_CHANCE_KEYS:
        return True
    if group == "requirements" and official_key in PERSONNEL_EDUCATION_REQUIREMENT_KEYS:
        return True
    if group == "prerequisites" and official_key in PERSONNEL_EDUCATION_PREREQUISITE_KEYS:
        return True
    return False


def known_keys_by_group(
    mappings: dict[str, dict[str, dict[str, Any]]],
) -> dict[str, set[str]]:
    result = {group: set(mappings[group]) for group in KEY_GROUPS}
    result["requirements"].update(CONDITIONAL_REQUIREMENT_KEYS)
    result["chances"].update(CONDITIONAL_CHANCE_KEYS)
    result["requirements"].update(PERSONNEL_EDUCATION_REQUIREMENT_KEYS)
    result["prerequisites"].update(PERSONNEL_EDUCATION_PREREQUISITE_KEYS)
    return result


def unmapped_key_paths(
    record: dict[str, Any],
    mappings: dict[str, dict[str, dict[str, Any]]],
) -> list[tuple[str, str]]:
    result: list[tuple[str, str]] = []
    for group in KEY_GROUPS:
        values = record.get(group, {})
        if not isinstance(values, dict):
            continue
        for official_key in values:
            key = str(official_key)
            if not is_known_key(group, key, mappings):
                result.append((group, key))
    return result


def mapping_policy_blockers(
    record: dict[str, Any],
    mappings: dict[str, dict[str, dict[str, Any]]],
) -> list[str]:
    blockers: list[str] = []
    for group in KEY_GROUPS:
        values = record.get(group, {})
        if not isinstance(values, dict):
            blockers.append(f"{group} is not an object")
            continue
        for official_key, value in values.items():
            key = str(official_key)
            mapping = mappings[group].get(key)
            if mapping is None:
                continue
            if mapping.get("status") == "not-applicable" and value not in mapping.get("allowed_values", []):
                blockers.append(
                    f"{group}.{key}={value!r} outside allow-list {mapping.get('allowed_values', [])!r}"
                )
    return blockers


def key_blockers(record: dict[str, Any], mappings: dict[str, dict[str, dict[str, Any]]]) -> list[str]:
    return [
        f"unmapped {group}.{key}"
        for group, key in unmapped_key_paths(record, mappings)
    ] + mapping_policy_blockers(record, mappings)


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


def source_blockers(
    record: dict[str, Any],
    mappings: dict[str, dict[str, dict[str, Any]]],
    official_by_id: dict[str, dict[str, Any]],
) -> list[str]:
    return key_blockers(record, mappings) + operational_blockers(record, official_by_id)


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
        "state": "official-only",
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
    if len(official_by_id) != len(records):
        raise ValueError("Official UK mission source repeats one or more mission ids")
    duplicate_names = Counter(mission_name(record).casefold() for record in records)
    canonical = canonical_records_by_id()
    canonical_id_set = set(canonical)
    direct_canonical_ids = set(official_by_id) & canonical_id_set
    canonical_only_ids = canonical_id_set - set(official_by_id)
    decisions = effective_verification_decisions()
    fully_canonical_decision_ids = {
        mission_id
        for mission_id, decision in decisions.items()
        if decision.get("stage") == "fully-canonical"
    }
    missing_official = fully_canonical_decision_ids - set(official_by_id)
    if missing_official:
        raise ValueError(
            "Fully canonical verification decisions lack official records: "
            + ", ".join(sorted(missing_official, key=stable_id))
        )
    fully_canonical_ids = fully_canonical_decision_ids
    missing_canonical = fully_canonical_ids - direct_canonical_ids
    if missing_canonical:
        raise ValueError(
            "Fully canonical verification decisions lack direct canonical records: "
            + ", ".join(sorted(missing_canonical, key=stable_id))
        )
    mappings = mapped_keys()
    ready: list[dict[str, Any]] = []
    blocked: list[dict[str, Any]] = []
    equivalence_audit_required: list[dict[str, Any]] = []
    existing_blocked: list[dict[str, Any]] = []

    for record in records:
        mission_id = str(record["id"])
        if mission_id in fully_canonical_ids:
            continue

        blockers = source_blockers(record, mappings, official_by_id)
        if mission_id not in canonical:
            if blockers:
                blocked.append(
                    {
                        "id": record.get("id"),
                        "name": mission_name(record),
                        "state": "official-only",
                        "blockers": blockers,
                    }
                )
            else:
                ready.append(candidate_record(record, official_by_id, duplicate_names))
            continue

        canonical_entry = canonical[mission_id]
        canonical_record = canonical_entry["record"]
        official_name = mission_name(record)
        canonical_name = mission_name(canonical_record)
        identity_matches = official_name == canonical_name
        verification = canonical_record.get("verification")
        verification_status = verification.get("status") if isinstance(verification, dict) else None
        decision = decisions.get(mission_id, {})
        registry_stage = decision.get("stage")
        if not isinstance(registry_stage, str) or not registry_stage:
            registry_stage = "identity-verified" if identity_matches else "captured"
        identity_blockers: list[str] = []
        if not identity_matches:
            identity_blockers.append(
                f"canonical name {canonical_name!r} does not match official name {official_name!r}"
            )
        if verification_status != "verified":
            identity_blockers.append(
                f"canonical verification.status must be 'verified', found {verification_status!r}"
            )
        existing_entry = {
            "id": record.get("id"),
            "name": official_name,
            "state": "canonical-unpromoted",
            "canonical_path": canonical_entry["path"],
            "canonical_name": canonical_name,
            "canonical_verification_status": verification_status,
            "identity_matches": identity_matches,
            "registry_stage": registry_stage,
            "requires_equivalence_audit": True,
        }
        blockers = identity_blockers + blockers
        if blockers:
            existing_blocked.append({**existing_entry, "blockers": blockers})
        else:
            equivalence_audit_required.append(existing_entry)

    ready.sort(key=lambda item: stable_id(item["id"]))
    blocked.sort(key=lambda item: stable_id(item["id"]))
    equivalence_audit_required.sort(key=lambda item: stable_id(item["id"]))
    existing_blocked.sort(key=lambda item: stable_id(item["id"]))

    new_record_count = len(ready) + len(blocked)
    existing_record_count = len(equivalence_audit_required) + len(existing_blocked)
    if len(records) != len(fully_canonical_ids) + new_record_count + existing_record_count:
        raise ValueError("Official catalogue reporting partition is incomplete")
    if len(canonical) != len(direct_canonical_ids) + len(canonical_only_ids):
        raise ValueError("Canonical catalogue reporting partition is incomplete")

    new_records = {
        "count": new_record_count,
        "ready_count": len(ready),
        "blocked_count": len(blocked),
        "ready": ready,
        "blocked": blocked,
    }
    existing_records = {
        "count": existing_record_count,
        "equivalence_audit_required_count": len(equivalence_audit_required),
        "blocked_count": len(existing_blocked),
        "equivalence_audit_required": equivalence_audit_required,
        "blocked": existing_blocked,
    }
    result = {
        "schema_version": "8",
        "official_count": len(records),
        "canonical_count": len(canonical),
        "direct_canonical_count": len(direct_canonical_ids),
        "canonical_only_count": len(canonical_only_ids),
        "fully_canonical_count": len(fully_canonical_ids),
        "remaining_to_fully_canonical_count": len(records) - len(fully_canonical_ids),
        "patient_contract_fields": len(PATIENT_MAPPINGS),
        "conditional_resource_contracts": len(CONDITIONAL_MAPPINGS),
        "personnel_education_roles": len(PERSONNEL_EDUCATION_MAPPINGS["roles"]),
        "recovery_asset_contracts": len(RECOVERY_MAPPINGS),
        "personnel_contract_roles": len(PERSONNEL_MAPPINGS),
        "prisoner_contract_fields": len(PRISONER_MAPPINGS),
        "new_records": new_records,
        "existing_records": existing_records,
    }
    result.update(
        {
            "ready_count": new_records["ready_count"],
            "blocked_count": new_records["blocked_count"],
            "ready": new_records["ready"],
            "blocked": new_records["blocked"],
        }
    )
    return result


def limited_report(
    result: dict[str, Any],
    ready_limit: int,
    blocked_limit: int,
    existing_limit: int,
) -> dict[str, Any]:
    output = dict(result)
    new_records = dict(result["new_records"])
    new_records["ready"] = result["new_records"]["ready"][: max(0, ready_limit)]
    new_records["blocked"] = result["new_records"]["blocked"][: max(0, blocked_limit)]
    existing_records = dict(result["existing_records"])
    existing_records["equivalence_audit_required"] = result["existing_records"][
        "equivalence_audit_required"
    ][: max(0, existing_limit)]
    existing_records["blocked"] = result["existing_records"]["blocked"][: max(0, existing_limit)]
    output["new_records"] = new_records
    output["existing_records"] = existing_records
    output["ready"] = new_records["ready"]
    output["blocked"] = new_records["blocked"]
    return output


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Report evidence-safe canonical mission candidates from the retained official UK snapshot"
    )
    parser.add_argument("--limit", type=int, default=40, help="Maximum ready candidates to print")
    parser.add_argument("--blocked-limit", type=int, default=0, help="Maximum blocked candidates to print")
    parser.add_argument(
        "--existing-limit",
        type=int,
        default=40,
        help="Maximum existing unpromoted candidates to print per state",
    )
    args = parser.parse_args()

    try:
        result = report()
    except ValueError as exc:
        print(f"Canonical candidate reporting failed: {exc}", file=sys.stderr)
        return 1

    output = limited_report(result, args.limit, args.blocked_limit, args.existing_limit)
    print(json.dumps(output, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
