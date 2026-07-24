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
from report_canonical_candidates import (
    canonical_records_by_id,
    effective_verification_decisions,
    known_keys_by_group,
    mapped_keys as load_mapping_records,
    source_blockers,
    stable_id,
    unmapped_key_paths,
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
    "coastal_rescue_missions",
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
    return set(canonical_records_by_id())


def load_mapped_keys() -> dict[str, set[str]]:
    return known_keys_by_group(load_mapping_records())


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


def operational_complexity(
    record: dict[str, Any],
    official_by_id: dict[str, dict[str, Any]] | None = None,
    mappings: dict[str, dict[str, dict[str, Any]]] | None = None,
) -> list[str]:
    if official_by_id is None:
        envelope = read_json(OFFICIAL_PATH)
        records = envelope.get("records") if isinstance(envelope, dict) else None
        if not isinstance(records, list):
            raise ValueError("Official UK mission source envelope is invalid")
        official_by_id = {
            str(item["id"]): item
            for item in records
            if isinstance(item, dict) and item.get("id") is not None
        }
    if mappings is None:
        mappings = load_mapping_records()
    return [
        blocker
        for blocker in source_blockers(record, mappings, official_by_id)
        if not blocker.startswith("unmapped ")
    ]


def blockers_after_resolving_key(
    blockers: list[str],
    group: str,
    key: str,
) -> list[str]:
    target = f"unmapped {group}.{key}"
    removed = False
    result: list[str] = []
    for blocker in blockers:
        if blocker == target and not removed:
            removed = True
            continue
        result.append(blocker)
    return result


def single_key_unlock_bucket(
    state: str,
    blockers: list[str],
    group: str,
    key: str,
) -> str | None:
    if blockers_after_resolving_key(blockers, group, key):
        return None
    if state == "official-only":
        return "creation"
    if state == "canonical-unpromoted":
        return "existing-audit"
    return None


def build_report(example_limit: int) -> dict[str, Any]:
    envelope = read_json(OFFICIAL_PATH)
    if not isinstance(envelope, dict) or not isinstance(envelope.get("records"), list):
        raise ValueError("Official UK mission source envelope is invalid")
    records = [record for record in envelope["records"] if isinstance(record, dict) and record.get("id") is not None]
    official_by_id = {str(record["id"]): record for record in records}
    if len(official_by_id) != len(records):
        raise ValueError("Official UK mission source repeats one or more mission ids")
    mappings = load_mapping_records()
    mapped = known_keys_by_group(mappings)
    canonical = canonical_records_by_id()
    canonical_id_set = set(canonical)
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
    missing_canonical = fully_canonical_ids - canonical_id_set
    if missing_canonical:
        raise ValueError(
            "Fully canonical verification decisions lack direct canonical records: "
            + ", ".join(sorted(missing_canonical, key=stable_id))
        )

    states = ("official-only", "canonical-unpromoted", "fully-canonical")
    state_counts: Counter[str] = Counter()
    counts: Counter[tuple[str, str]] = Counter()
    counts_by_state: Counter[tuple[tuple[str, str], str]] = Counter()
    creation_unlocks: Counter[tuple[str, str]] = Counter()
    existing_audit_unlocks: Counter[tuple[str, str]] = Counter()
    examples_by_state: dict[
        tuple[str, str],
        dict[str, list[dict[str, Any]]],
    ] = defaultdict(lambda: {state: [] for state in states})
    keys_by_state: dict[str, set[tuple[str, str]]] = {state: set() for state in states}
    occurrences_by_state: Counter[str] = Counter()

    for record in records:
        mission_id = str(record["id"])
        if mission_id in fully_canonical_ids:
            state = "fully-canonical"
        elif mission_id in canonical:
            state = "canonical-unpromoted"
        else:
            state = "official-only"
        state_counts[state] += 1

        unmapped = unmapped_key_paths(record, mappings)
        blockers = source_blockers(record, mappings, official_by_id)
        for group, key in unmapped:
            identity = (group, key)
            counts[identity] += 1
            counts_by_state[(identity, state)] += 1
            keys_by_state[state].add(identity)
            occurrences_by_state[state] += 1
            unlock_bucket = single_key_unlock_bucket(state, blockers, group, key)
            if unlock_bucket == "creation":
                creation_unlocks[identity] += 1
            elif unlock_bucket == "existing-audit":
                existing_audit_unlocks[identity] += 1

            state_examples = examples_by_state[identity][state]
            if len(state_examples) < example_limit:
                value_group = record.get(group, {})
                other_unmapped = [
                    f"{other_group}.{other_key}"
                    for other_group, other_key in unmapped
                    if (other_group, other_key) != identity
                ]
                remaining_blockers = blockers_after_resolving_key(blockers, group, key)
                other_blockers = [
                    blocker
                    for blocker in remaining_blockers
                    if not blocker.startswith("unmapped ")
                ]
                canonical_entry = canonical.get(mission_id)
                decision = decisions.get(mission_id, {})
                registry_stage = decision.get("stage")
                if state != "official-only" and (
                    not isinstance(registry_stage, str) or not registry_stage
                ):
                    registry_stage = (
                        "identity-verified"
                        if canonical_entry is not None
                        and mission_name(canonical_entry["record"]) == mission_name(record)
                        else "captured"
                    )
                state_examples.append(
                    {
                        "id": record.get("id"),
                        "name": mission_name(record),
                        "state": state,
                        "value": value_group.get(key) if isinstance(value_group, dict) else None,
                        "average_credits": record.get("average_credits"),
                        "filter_id": record.get("additional", {}).get("filter_id")
                        if isinstance(record.get("additional"), dict)
                        else None,
                        "canonical_path": canonical_entry["path"]
                        if canonical_entry is not None
                        else None,
                        "registry_stage": registry_stage
                        if state != "official-only"
                        else None,
                        "other_unmapped_keys": other_unmapped,
                        "other_blockers": other_blockers,
                        "operational_complexity": other_blockers,
                        "official_url": record.get("official_url")
                        or f"https://www.missionchief.co.uk/einsaetze/{record.get('id')}",
                    }
                )

    entries = [
        {
            "group": group,
            "key": key,
            "path": f"{group}.{key}",
            "catalogue_mission_count": counts[(group, key)],
            "official_only_mission_count": counts_by_state[((group, key), "official-only")],
            "canonical_unpromoted_mission_count": counts_by_state[
                ((group, key), "canonical-unpromoted")
            ],
            "fully_canonical_mission_count": counts_by_state[
                ((group, key), "fully-canonical")
            ],
            "single_key_creation_unlock_count": creation_unlocks[(group, key)],
            "single_key_existing_audit_unlock_count": existing_audit_unlocks[
                (group, key)
            ],
            "examples_by_state": examples_by_state[(group, key)],
            # Schema v2 compatibility aliases retain their creation-pool meaning.
            "remaining_mission_count": counts_by_state[((group, key), "official-only")],
            "single_key_unlock_count": creation_unlocks[(group, key)],
            "examples": examples_by_state[(group, key)]["official-only"],
        }
        for group, key in counts
    ]
    entries.sort(
        key=lambda item: (
            -item["single_key_creation_unlock_count"],
            -item["single_key_existing_audit_unlock_count"],
            -item["catalogue_mission_count"],
            item["group"],
            item["key"],
        )
    )

    direct_canonical_ids = set(official_by_id) & canonical_id_set
    canonical_only_ids = canonical_id_set - set(official_by_id)
    catalogue_occurrences = sum(counts.values())
    return {
        "schema_version": "3",
        "official_count": len(records),
        "canonical_count": len(canonical),
        "direct_canonical_count": len(direct_canonical_ids),
        "canonical_only_count": len(canonical_only_ids),
        "fully_canonical_count": state_counts["fully-canonical"],
        "official_only_count": state_counts["official-only"],
        "canonical_unpromoted_count": state_counts["canonical-unpromoted"],
        "patient_contract_fields": len(PATIENT_MAPPINGS),
        "conditional_resource_contracts": len(CONDITIONAL_MAPPINGS),
        "personnel_education_roles": len(PERSONNEL_EDUCATION_MAPPINGS["roles"]),
        "recovery_asset_contracts": len(RECOVERY_MAPPINGS),
        "mapped_key_counts": {group: len(mapped[group]) for group in KEY_GROUPS},
        "catalogue_unmapped_key_count": len(entries),
        "catalogue_unmapped_occurrence_count": catalogue_occurrences,
        "official_only_unmapped_key_count": len(keys_by_state["official-only"]),
        "official_only_unmapped_occurrence_count": occurrences_by_state[
            "official-only"
        ],
        "canonical_unpromoted_unmapped_key_count": len(
            keys_by_state["canonical-unpromoted"]
        ),
        "canonical_unpromoted_unmapped_occurrence_count": occurrences_by_state[
            "canonical-unpromoted"
        ],
        "fully_canonical_unmapped_key_count": len(keys_by_state["fully-canonical"]),
        "fully_canonical_unmapped_occurrence_count": occurrences_by_state[
            "fully-canonical"
        ],
        # Schema v2 compatibility alias retains its creation-pool meaning.
        "unmapped_key_count": len(keys_by_state["official-only"]),
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
