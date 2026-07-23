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
    active_requirement_keys as active_conditional_requirement_keys,
    build_expected_conditionals,
    load_mapping_registry as load_conditional_mappings,
    owned_paths as conditional_owned_paths,
)
from patient_contract import ROOT, build_expected_patient, load_mapping_registry
from personnel_education_contract import (
    build_expected_personnel_educations,
    load_mapping_registry as load_personnel_education_mappings,
    owned_paths as personnel_education_owned_paths,
)
from recovery_contract import build_expected_recovery, load_mapping_registry as load_recovery_mappings
from report_canonical_candidates import report as candidate_report

OFFICIAL_PATH = ROOT / "data" / "sources" / "missionchief-uk" / "einsaetze.raw.json"
KEY_MAPPING_PATH = ROOT / "data" / "uk" / "official-key-mappings.json"
CANONICAL_ROOT = ROOT / "data" / "uk" / "missions"
BATCH_ROOT = ROOT / "data" / "uk" / "mission-verification-batches"
REFERENCE_ROOT = ROOT / "docs" / "reference"
VERIFICATION_REGISTRY_PATH = ROOT / "data" / "uk" / "mission-verification-registry.json"
SNAPSHOT_URL = "https://www.missionchief.co.uk/einsaetze.json"
CHECKED_AT = "2026-07-23"
BATCH_PATTERN = re.compile(r"fully-canonical-fire-batch-(\d+)\.json$")
CONDITIONAL_MAPPINGS = load_conditional_mappings()
(
    CONDITIONAL_REQUIREMENT_KEYS,
    CONDITIONAL_CHANCE_KEYS,
    CONDITIONAL_ADDITIONAL_KEYS,
    CONDITIONAL_RESOURCES,
) = conditional_owned_paths(CONDITIONAL_MAPPINGS)
PERSONNEL_EDUCATION_MAPPINGS = load_personnel_education_mappings()
(
    PERSONNEL_EDUCATION_REQUIREMENT_KEYS,
    PERSONNEL_EDUCATION_PREREQUISITE_KEYS,
    PERSONNEL_EDUCATION_ADDITIONAL_KEYS,
    PERSONNEL_EDUCATION_ROLES,
) = personnel_education_owned_paths(PERSONNEL_EDUCATION_MAPPINGS)
RECOVERY_MAPPINGS = load_recovery_mappings()

GENERATOR_METADATA = {
    "firehouse_missions": ("fire", ["Fire Fighting Missions"]),
    "police_station_missions": ("police", ["Police Missions"]),
    "ambulance_station_missions": ("ambulance", ["Ambulance Missions"]),
    "tow_trucks_missions": ("recovery", ["Recovery Vehicle Missions"]),
}


def read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"{path.relative_to(ROOT)}: unable to read JSON: {exc}") from exc


def write_json(path: Path, document: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(document, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def records_by_id(records: Any) -> dict[str, dict[str, Any]]:
    if not isinstance(records, list):
        raise ValueError("Official UK mission records must be an array")
    result: dict[str, dict[str, Any]] = {}
    for index, record in enumerate(records):
        if not isinstance(record, dict) or record.get("id") is None:
            raise ValueError(f"Official UK mission record {index} is invalid")
        mission_id = str(record["id"])
        if mission_id in result:
            raise ValueError(f"Official UK mission source repeats id {mission_id}")
        result[mission_id] = record
    return result


def canonical_id(value: Any) -> int | str:
    text = str(value)
    if text.isdigit():
        return int(text)
    return text


def checked_integer(value: Any, label: str) -> int:
    if not isinstance(value, int) or isinstance(value, bool) or value < 0:
        raise ValueError(f"{label} must be a non-negative integer")
    return value


def checked_percent(value: Any, label: str) -> int:
    if not isinstance(value, int) or isinstance(value, bool) or not 0 <= value <= 100:
        raise ValueError(f"{label} must be an integer percentage from 0 to 100")
    return value


def add_quantity(target: dict[str, int], resource: str, quantity: int, label: str) -> None:
    previous = target.get(resource)
    if previous is not None and previous != quantity:
        raise ValueError(f"{label} maps conflicting quantities for {resource}: {previous} and {quantity}")
    target[resource] = quantity


def add_probability(
    target: dict[str, tuple[int, float]],
    resource: str,
    quantity: int,
    probability: float,
    label: str,
) -> None:
    value = (quantity, probability)
    previous = target.get(resource)
    if previous is not None and previous != value:
        raise ValueError(f"{label} maps conflicting probabilities for {resource}: {previous} and {value}")
    target[resource] = value


def translate_requirements(
    official: dict[str, Any],
    mappings: dict[str, Any],
) -> dict[str, Any]:
    mission_id = str(official.get("id"))
    official_requirements = official.get("requirements", {})
    official_chances = official.get("chances", {})
    if not isinstance(official_requirements, dict) or not isinstance(official_chances, dict):
        raise ValueError(f"Mission {mission_id} requirements or chances are invalid")

    guaranteed: dict[str, int] = {}
    probabilistic: dict[str, tuple[int, float]] = {}
    alternatives: dict[tuple[str, ...], tuple[list[str], int]] = {}
    conditionals = build_expected_conditionals(official, CONDITIONAL_MAPPINGS)
    conditional_requirement_keys = active_conditional_requirement_keys(
        official, CONDITIONAL_MAPPINGS
    )

    for official_key, raw_quantity in official_requirements.items():
        if str(official_key) in conditional_requirement_keys:
            continue
        mapping = mappings["requirements"].get(str(official_key))
        if not isinstance(mapping, dict):
            if str(official_key) in CONDITIONAL_REQUIREMENT_KEYS:
                continue
            if str(official_key) in PERSONNEL_EDUCATION_REQUIREMENT_KEYS:
                continue
            raise ValueError(f"Mission {mission_id} requirement {official_key} is unmapped")
        if mapping.get("status") == "not-applicable":
            if raw_quantity not in mapping.get("allowed_values", []):
                raise ValueError(f"Mission {mission_id} requirement {official_key} is outside its allow-list")
            continue
        quantity = checked_integer(raw_quantity, f"Mission {mission_id} requirements.{official_key}")
        if quantity == 0:
            continue
        target = mapping.get("canonical_target")
        if target == "requirements.alternatives":
            if official_key in official_chances:
                raise ValueError(f"Mission {mission_id} requires probabilistic alternative-group support")
            resources = mapping.get("canonical_ids")
            if not isinstance(resources, list) or len(resources) < 2:
                raise ValueError(f"Mission {mission_id} alternative mapping {official_key} is invalid")
            key = tuple(sorted(str(resource) for resource in resources))
            alternatives[key] = ([str(resource) for resource in resources], quantity)
            continue
        resource = mapping.get("canonical_id")
        if not isinstance(resource, str) or not resource:
            raise ValueError(f"Mission {mission_id} requirement mapping {official_key} has no canonical resource")
        if target == "requirements.guaranteed":
            add_quantity(guaranteed, resource, quantity, f"Mission {mission_id}")
            continue
        if target != "requirements.chance-aware":
            raise ValueError(f"Mission {mission_id} requirement mapping {official_key} has unsupported target {target!r}")
        chance_key = str(mapping.get("chance_key", official_key))
        raw_chance = official_chances.get(chance_key)
        if raw_chance is None:
            add_quantity(guaranteed, resource, quantity, f"Mission {mission_id}")
            continue
        percent = checked_percent(raw_chance, f"Mission {mission_id} chances.{chance_key}")
        if percent == 0:
            continue
        if percent == 100:
            add_quantity(guaranteed, resource, quantity, f"Mission {mission_id}")
        else:
            add_probability(probabilistic, resource, quantity, percent / 100, f"Mission {mission_id}")

    output: dict[str, Any] = {
        "guaranteed": [
            {"resource": resource, "quantity": quantity}
            for resource, quantity in sorted(guaranteed.items())
        ]
    }
    if probabilistic:
        output["probabilistic"] = [
            {"resource": resource, "quantity": quantity, "probability": probability}
            for resource, (quantity, probability) in sorted(probabilistic.items())
        ]
    if alternatives:
        output["alternatives"] = [
            {
                "resources": resources,
                "quantity": quantity,
                "notes": ["Any listed qualifying resource may satisfy this official alternative group."],
            }
            for _, (resources, quantity) in sorted(alternatives.items())
        ]
    if conditionals:
        output["conditional"] = conditionals
    return output


def translate_preconditions(official: dict[str, Any], mappings: dict[str, Any]) -> dict[str, int]:
    mission_id = str(official.get("id"))
    prerequisites = official.get("prerequisites", {})
    if not isinstance(prerequisites, dict):
        raise ValueError(f"Mission {mission_id} prerequisites are invalid")
    output: dict[str, int] = {}
    for official_key, raw_quantity in prerequisites.items():
        mapping = mappings["prerequisites"].get(str(official_key))
        if not isinstance(mapping, dict):
            if str(official_key) in PERSONNEL_EDUCATION_PREREQUISITE_KEYS:
                continue
            raise ValueError(f"Mission {mission_id} prerequisite {official_key} is unmapped")
        if mapping.get("status") == "not-applicable":
            if raw_quantity not in mapping.get("allowed_values", []):
                raise ValueError(f"Mission {mission_id} prerequisite {official_key} is outside its allow-list")
            continue
        quantity = checked_integer(raw_quantity, f"Mission {mission_id} prerequisites.{official_key}")
        canonical_target = mapping.get("canonical_id")
        if not isinstance(canonical_target, str) or not canonical_target:
            raise ValueError(f"Mission {mission_id} prerequisite mapping {official_key} has no canonical target")
        previous = output.get(canonical_target)
        if previous is not None and previous != quantity:
            raise ValueError(f"Mission {mission_id} maps conflicting preconditions for {canonical_target}")
        output[canonical_target] = quantity
    return output


def poi_values(official: dict[str, Any]) -> list[str]:
    values: list[str] = []
    raw_array = official.get("place_array", [])
    if isinstance(raw_array, list):
        values.extend(str(item).strip() for item in raw_array if str(item).strip())
    place = official.get("place")
    if isinstance(place, str) and place.strip():
        values.append(place.strip())
    return list(dict.fromkeys(values))


def relationship_ids(official: dict[str, Any], key: str) -> list[str]:
    additional = official.get("additional", {})
    if not isinstance(additional, dict):
        return []
    values = additional.get(key, [])
    if not isinstance(values, list):
        raise ValueError(f"Mission {official.get('id')} additional.{key} is not an array")
    strings = [str(value) for value in values]
    if len(strings) != len(set(strings)):
        raise ValueError(f"Mission {official.get('id')} additional.{key} contains duplicate multiplicity")
    return strings


def build_canonical_record(
    official: dict[str, Any],
    mappings: dict[str, Any],
    patient_mappings: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    mission_id = str(official.get("id"))
    additional = official.get("additional", {})
    if not isinstance(additional, dict):
        raise ValueError(f"Mission {mission_id} additional must be an object")
    generator = additional.get("filter_id")
    metadata = GENERATOR_METADATA.get(generator)
    if metadata is None:
        raise ValueError(f"Mission {mission_id} generator {generator!r} is not approved")
    service, mission_types = metadata
    name = official.get("name")
    if not isinstance(name, str) or not name:
        raise ValueError(f"Mission {mission_id} has no official name")

    record: dict[str, Any] = {
        "id": canonical_id(official["id"]),
        "name": name,
        "service": service,
        "mission_types": mission_types,
        "requirements": translate_requirements(official, mappings),
        "verification": {
            "status": "verified",
            "checked_at": CHECKED_AT,
            "sources": [official.get("official_url") or f"https://www.missionchief.co.uk/einsaetze/{mission_id}", SNAPSHOT_URL],
        },
    }
    poi = poi_values(official)
    if poi:
        record["poi"] = poi
    preconditions = translate_preconditions(official, mappings)
    if preconditions:
        record["preconditions"] = preconditions
    patients = build_expected_patient(official, patient_mappings)
    if patients:
        record["patients"] = patients
    personnel_educations = build_expected_personnel_educations(
        official, PERSONNEL_EDUCATION_MAPPINGS
    )
    if personnel_educations:
        record["personnel"] = personnel_educations
    recovery = build_expected_recovery(official, RECOVERY_MAPPINGS)
    if recovery:
        record["recovery"] = recovery
    reward = official.get("average_credits")
    if isinstance(reward, (int, float)) and not isinstance(reward, bool):
        record["reward"] = {"average_credits": reward}
    followups = relationship_ids(official, "followup_missions_ids")
    expansions = relationship_ids(official, "expansion_missions_ids")
    if followups:
        record["follow_up_missions"] = followups
    if expansions:
        record["expandable_missions"] = expansions
    record["notes"] = [
        "Generated deterministically from the retained official UK mission snapshot.",
        "Resource, prerequisite and patient fields are protected by strict official equivalence validators.",
    ]
    return record


def next_batch_number() -> int:
    numbers: list[int] = []
    for path in BATCH_ROOT.glob("fully-canonical-fire-batch-*.json"):
        match = BATCH_PATTERN.search(path.name)
        if match:
            numbers.append(int(match.group(1)))
    return max(numbers, default=2) + 1


def count_fully_canonical() -> int:
    registry = read_json(VERIFICATION_REGISTRY_PATH)
    records = registry.get("records") if isinstance(registry, dict) else None
    if not isinstance(records, dict):
        raise ValueError("Mission verification registry records must be an object")
    return sum(
        1
        for decision in records.values()
        if isinstance(decision, dict) and decision.get("stage") == "fully-canonical"
    )


def evidence_page(
    batch_number: int,
    candidates: list[dict[str, Any]],
    official_by_id: dict[str, dict[str, Any]],
    canonical_before: int,
    direct_before: int,
    fully_before: int,
    official_count: int,
) -> str:
    rows: list[str] = []
    for candidate in candidates:
        mission_id = str(candidate["id"])
        official = official_by_id[mission_id]
        generator = candidate.get("generator_family") or "—"
        patient = candidate.get("patients", {})
        maximum = patient.get("maximum") if isinstance(patient, dict) else None
        patient_text = str(maximum) if maximum is not None else "—"
        credits = official.get("average_credits")
        credits_text = f"{credits:,}" if isinstance(credits, int) else str(credits or "—")
        rows.append(
            f"| `{mission_id}` | {candidate['name']} | `{generator}` | {patient_text} | {credits_text} |"
        )

    count = len(candidates)
    canonical_after = canonical_before + count
    direct_after = direct_before + count
    fully_after = fully_before + count
    remaining_after = official_count - fully_after
    return "\n".join(
        [
            f"# Fully Canonical Mission Batch {batch_number}",
            "",
            f"Batch {batch_number} promotes {count} analyser-approved missions unlocked by the lossless official patient contract.",
            "",
            "## Batch result",
            "",
            "| ID | Mission | Generator | Maximum patients | Average credits |",
            "|---:|---|---|---:|---:|",
            *rows,
            "",
            "## Evidence safeguards",
            "",
            "- Every record was selected by the evidence-safe candidate analyser after all resource, prerequisite, relationship and patient blockers were cleared.",
            "- Patient maxima and optional minima, specialisation captions and IDs, UK codes, transport and critical-care probabilities, first-responder probability and end-of-mission generation flags are preserved exactly when published.",
            "- Resource probabilities remain distinct from patient probabilities.",
            "- Duplicate relationship multiplicity, variants, overlays, unsupported generators and unmapped keys remain blocked.",
            "- Strict resource-key and patient equivalence are mandatory for every promotion.",
            "",
            "## Coverage movement",
            "",
            "```text",
            f"Before Batch {batch_number}",
            f"Canonical records:       {canonical_before}",
            f"Direct ID matches:       {direct_before}",
            f"Fully canonical:         {fully_before}",
            f"Remaining to canonical:  {official_count - fully_before}",
            "",
            f"After Batch {batch_number}",
            f"Canonical records:       {canonical_after}",
            f"Direct ID matches:       {direct_after}",
            f"Fully canonical:         {fully_after}",
            f"Remaining to canonical:  {remaining_after}",
            "```",
            "",
            f"Batch {batch_number} raises identity coverage to **{direct_after / official_count * 100:.2f}%** and fully canonical coverage to **{fully_after / official_count * 100:.2f}%**.",
            "",
            "Promotion decisions are stored in:",
            "",
            "```text",
            f"data/uk/mission-verification-batches/fully-canonical-fire-batch-{batch_number}.json",
            "```",
            "",
        ]
    )


def generate(limit: int, check_only: bool) -> tuple[int, int, list[str]]:
    envelope = read_json(OFFICIAL_PATH)
    if not isinstance(envelope, dict):
        raise ValueError("Official UK mission source envelope must be an object")
    official_by_id = records_by_id(envelope.get("records"))
    mappings = read_json(KEY_MAPPING_PATH)
    if not isinstance(mappings, dict):
        raise ValueError("Official key mapping registry must be an object")
    patient_mappings = load_mapping_registry()

    candidate_document = candidate_report()
    ready = candidate_document.get("ready")
    if not isinstance(ready, list):
        raise ValueError("Canonical candidate report did not return a ready array")
    selected = ready[:limit]
    if not selected:
        return 0, next_batch_number(), []
    if check_only:
        return len(selected), next_batch_number(), [str(item.get("id")) for item in selected]

    batch_number = next_batch_number()
    registry_path = BATCH_ROOT / f"fully-canonical-fire-batch-{batch_number}.json"
    page_path = REFERENCE_ROOT / f"fully-canonical-mission-batch-{batch_number}.md"
    if registry_path.exists() or page_path.exists():
        raise ValueError(f"Batch {batch_number} assets already exist")

    canonical_before = sum(1 for _ in CANONICAL_ROOT.glob("*.json"))
    direct_before = sum(1 for mission_id in official_by_id if any(
        str(read_json(path).get("id")) == mission_id for path in CANONICAL_ROOT.glob("*.json")
    ))
    fully_before = count_fully_canonical()

    decisions: dict[str, Any] = {}
    generated_paths: list[str] = []
    for candidate in selected:
        mission_id = str(candidate.get("id"))
        official = official_by_id.get(mission_id)
        if official is None:
            raise ValueError(f"Candidate mission {mission_id} is absent from the official source")
        relative_path = candidate.get("suggested_path")
        if not isinstance(relative_path, str) or not relative_path.startswith("data/uk/missions/"):
            raise ValueError(f"Candidate mission {mission_id} has an invalid suggested path")
        path = ROOT / relative_path
        if path.exists():
            raise ValueError(f"Candidate mission path already exists: {relative_path}")
        write_json(path, build_canonical_record(official, mappings, patient_mappings))
        generated_paths.append(relative_path)
        decisions[mission_id] = {
            "stage": "fully-canonical",
            "checked_at": CHECKED_AT,
            "strict_key_equivalence": True,
            "strict_patient_equivalence": True,
            "strict_conditional_equivalence": bool(
                build_expected_conditionals(official, CONDITIONAL_MAPPINGS)
            ),
            "strict_personnel_education_equivalence": bool(
                build_expected_personnel_educations(
                    official, PERSONNEL_EDUCATION_MAPPINGS
                )
            ),
            "strict_recovery_equivalence": bool(
                build_expected_recovery(official, RECOVERY_MAPPINGS)
            ),
            "sources": [official.get("official_url") or f"https://www.missionchief.co.uk/einsaetze/{mission_id}", SNAPSHOT_URL],
            "notes": [
                "Generated from the retained official UK snapshot after all candidate blockers cleared.",
                "Exact resource, prerequisite, patient, personnel-education, conditional-resource, recovery-outcome and relationship equivalence is required.",
            ],
        }

    write_json(
        registry_path,
        {"schema_version": "1", "updated_at": CHECKED_AT, "records": decisions},
    )
    page_path.write_text(
        evidence_page(
            batch_number,
            selected,
            official_by_id,
            canonical_before,
            direct_before,
            fully_before,
            len(official_by_id),
        ),
        encoding="utf-8",
    )
    generated_paths.extend(
        [registry_path.relative_to(ROOT).as_posix(), page_path.relative_to(ROOT).as_posix()]
    )
    return len(selected), batch_number, generated_paths


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate one fully canonical batch from all analyser-approved missions")
    parser.add_argument("--limit", type=int, default=200, help="Maximum missions to promote in one batch")
    parser.add_argument("--check", action="store_true", help="Fail when analyser-approved missions remain ungenerated")
    args = parser.parse_args()

    try:
        count, batch_number, paths = generate(max(1, args.limit), args.check)
    except ValueError as exc:
        print(f"Ready canonical batch generation failed: {exc}", file=sys.stderr)
        return 1

    if args.check and count:
        print(
            f"Ready canonical batch generation check failed: {count} mission(s) remain for Batch {batch_number}: "
            + ", ".join(paths),
            file=sys.stderr,
        )
        return 1
    if count == 0:
        print("Ready canonical batch generation is stable: no analyser-approved missions remain.")
        return 0
    print(
        f"Generated fully canonical Batch {batch_number}: {count} mission(s), "
        f"{len(paths)} file(s) written."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
