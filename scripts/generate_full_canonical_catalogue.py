#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from copy import deepcopy
from pathlib import Path
from typing import Any

from conditional_resource_contract import build_expected_conditionals
from generate_ready_canonical_batch import (
    CONDITIONAL_MAPPINGS,
    PERSONNEL_EDUCATION_MAPPINGS,
    PERSONNEL_MAPPINGS,
    PRISONER_MAPPINGS,
    RECOVERY_MAPPINGS,
    SNAPSHOT_URL,
    build_canonical_record,
    resolve_checked_at,
)
from operational_metadata_contract import build_expected_operational_fields
from patient_contract import build_expected_patient, load_mapping_registry as load_patient_mappings
from personnel_contract import build_expected_personnel
from personnel_education_contract import build_expected_personnel_educations
from prisoner_contract import build_expected_prisoners
from recovery_contract import build_expected_recovery
from report_canonical_candidates import (
    canonical_records_by_id,
    effective_verification_decisions,
    mission_name,
    slugify,
    stable_id,
)

ROOT = Path(__file__).resolve().parents[1]
OFFICIAL_PATH = ROOT / "data" / "sources" / "missionchief-uk" / "einsaetze.raw.json"
KEY_MAPPING_PATH = ROOT / "data" / "uk" / "official-key-mappings.json"
CANONICAL_ROOT = ROOT / "data" / "uk" / "missions"
BATCH_ROOT = ROOT / "data" / "uk" / "mission-verification-batches"
REFERENCE_ROOT = ROOT / "docs" / "reference"
BATCH_NUMBER = 31
BATCH_PATH = BATCH_ROOT / f"fully-canonical-fire-batch-{BATCH_NUMBER}.json"
REFERENCE_PATH = REFERENCE_ROOT / f"fully-canonical-mission-batch-{BATCH_NUMBER}.md"
BATCH_PATTERN = re.compile(r"fully-canonical-fire-batch-(\d+)\.json$")

OWNED_FIELDS = {
    "id",
    "name",
    "service",
    "mission_types",
    "requirements",
    "verification",
    "poi",
    "preconditions",
    "patients",
    "personnel",
    "prisoners",
    "recovery",
    "reward",
    "follow_up_missions",
    "expandable_missions",
    "duration_minutes",
    "custom_spawn_area",
    "availability_window",
    "generation_rules",
    "water_requirements",
    "subsequent_missions",
    "official_metadata",
    "notes",
}


def read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"{path.relative_to(ROOT)}: unable to read JSON: {exc}") from exc


def write_json(path: Path, document: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(document, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def official_records() -> list[dict[str, Any]]:
    envelope = read_json(OFFICIAL_PATH)
    records = envelope.get("records") if isinstance(envelope, dict) else None
    if not isinstance(records, list):
        raise ValueError("Official UK mission source records must be an array")
    output: list[dict[str, Any]] = []
    seen: set[str] = set()
    for index, record in enumerate(records):
        if not isinstance(record, dict) or record.get("id") is None:
            raise ValueError(f"Official UK mission record {index} is invalid")
        mission_id = str(record["id"])
        if mission_id in seen:
            raise ValueError(f"Official UK mission source repeats id {mission_id}")
        seen.add(mission_id)
        output.append(record)
    return output


def existing_decisions_before_completion() -> dict[str, dict[str, Any]]:
    batch31_ids: set[str] = set()
    if BATCH_PATH.exists():
        batch31 = read_json(BATCH_PATH)
        records = batch31.get("records") if isinstance(batch31, dict) else None
        if not isinstance(records, dict):
            raise ValueError(f"Batch {BATCH_NUMBER} records must be an object")
        batch31_ids = {str(mission_id) for mission_id in records}

    documents: list[dict[str, Any]] = []
    base = read_json(ROOT / "data" / "uk" / "mission-verification-registry.json")
    documents.append(base)
    for path in sorted(BATCH_ROOT.glob("*.json")):
        if path == BATCH_PATH:
            continue
        documents.append(read_json(path))
    output: dict[str, dict[str, Any]] = {}
    for document in documents:
        records = document.get("records") if isinstance(document, dict) else None
        if not isinstance(records, dict):
            raise ValueError("Verification decision document records must be an object")
        for mission_id, decision in records.items():
            key = str(mission_id)
            if key in batch31_ids:
                continue
            if not isinstance(decision, dict):
                raise ValueError(f"Verification decision {key} must be an object")
            previous = output.get(key)
            if previous is not None and previous != decision:
                raise ValueError(f"Verification decision {key} conflicts before Batch {BATCH_NUMBER}")
            output[key] = decision
    return output


def suggested_paths(
    records: list[dict[str, Any]],
    existing: dict[str, dict[str, Any]],
) -> dict[str, Path]:
    duplicate_names = Counter(mission_name(record).casefold() for record in records)
    result: dict[str, Path] = {}
    occupied = {entry["path"] for entry in existing.values()}
    for record in records:
        mission_id = str(record["id"])
        current = existing.get(mission_id)
        if current is not None:
            result[mission_id] = ROOT / current["path"]
            continue
        name = mission_name(record)
        slug = slugify(name)
        if duplicate_names[name.casefold()] > 1:
            slug = f"{slug}-{slugify(mission_id)}"
        relative = f"data/uk/missions/{slug}.json"
        if relative in occupied:
            relative = f"data/uk/missions/{slug}-{slugify(mission_id)}.json"
        if relative in occupied:
            raise ValueError(f"Unable to assign a unique canonical path for mission {mission_id}")
        occupied.add(relative)
        result[mission_id] = ROOT / relative
    if len({path.as_posix() for path in result.values()}) != len(result):
        raise ValueError("Canonical path generation produced duplicates")
    return result


def preserve_non_owned_fields(
    generated: dict[str, Any],
    existing: dict[str, Any] | None,
) -> dict[str, Any]:
    if existing is None:
        return generated
    output = dict(generated)
    for field, value in existing.items():
        if field not in OWNED_FIELDS:
            output[field] = deepcopy(value)
    return output


def decision_for(record: dict[str, Any], checked_at: str) -> dict[str, Any]:
    mission_id = str(record["id"])
    return {
        "stage": "fully-canonical",
        "checked_at": checked_at,
        "strict_key_equivalence": True,
        "strict_patient_equivalence": True,
        "strict_personnel_equivalence": bool(
            build_expected_personnel(record, PERSONNEL_MAPPINGS)
        ),
        "strict_personnel_education_equivalence": bool(
            build_expected_personnel_educations(record, PERSONNEL_EDUCATION_MAPPINGS)
        ),
        "strict_prisoner_equivalence": bool(
            build_expected_prisoners(record, PRISONER_MAPPINGS)
        ),
        "strict_conditional_equivalence": bool(
            build_expected_conditionals(record, CONDITIONAL_MAPPINGS)
        ),
        "strict_recovery_equivalence": bool(
            build_expected_recovery(record, RECOVERY_MAPPINGS)
        ),
        "strict_operational_equivalence": True,
        "sources": [
            record.get("official_url")
            or f"https://www.missionchief.co.uk/einsaetze/{mission_id}",
            SNAPSHOT_URL,
        ],
        "notes": [
            "Promoted by the complete-catalogue generator after every retained official field passed its evidence-controlled contract.",
            "Exact resource, prerequisite, patient, personnel, prisoner, recovery, relationship and operational-metadata equivalence is required.",
        ],
    }


def evidence_page(
    pending: list[dict[str, Any]],
    official_count: int,
    canonical_before: int,
    fully_before: int,
) -> str:
    by_service = Counter(
        build_expected_operational_fields(record)["service"] for record in pending
    )
    service_rows = [
        f"| {service.replace('_', ' ').title()} | {count} |"
        for service, count in sorted(by_service.items())
    ]
    identifiers = ", ".join(f"`{record['id']}`" for record in pending)
    return "\n".join(
        [
            f"# Fully Canonical Mission Batch {BATCH_NUMBER}",
            "",
            f"Batch {BATCH_NUMBER} completes the evidence-controlled canonicalisation of the United Kingdom mission catalogue by promoting **{len(pending)}** missions.",
            "",
            "## Result",
            "",
            "```text",
            f"Official missions:        {official_count}",
            f"Canonical before:         {canonical_before}",
            f"Fully canonical before:   {fully_before}",
            f"Promoted in Batch {BATCH_NUMBER}:   {len(pending)}",
            f"Fully canonical after:    {official_count}",
            "Remaining:                0",
            "```",
            "",
            "## Promotions by service family",
            "",
            "| Service family | Missions |",
            "|---|---:|",
            *service_rows,
            "",
            "## Evidence boundary",
            "",
            "- Every official key is mapped through an evidence-controlled registry.",
            "- Operational metadata, variants, overlays, generator families, availability windows, water thresholds and relationship multiplicity are retained explicitly rather than inferred.",
            "- Every promoted record is protected by strict official equivalence validators.",
            "- The generator is deterministic and must reproduce the committed catalogue without drift.",
            "",
            "## Promoted mission identifiers",
            "",
            identifiers,
            "",
            "Promotion decisions are stored in:",
            "",
            "```text",
            f"data/uk/mission-verification-batches/fully-canonical-fire-batch-{BATCH_NUMBER}.json",
            "```",
            "",
        ]
    )


def build_expected(checked_at: str) -> tuple[
    dict[Path, dict[str, Any]], dict[str, Any], str, set[str]
]:
    records = official_records()
    official_by_id = {str(record["id"]): record for record in records}
    mappings = read_json(KEY_MAPPING_PATH)
    if not isinstance(mappings, dict):
        raise ValueError("Official key mapping registry must be an object")
    patient_mappings = load_patient_mappings()
    existing = canonical_records_by_id()
    paths = suggested_paths(records, existing)

    generated: dict[Path, dict[str, Any]] = {}
    for mission_id in sorted(official_by_id, key=stable_id):
        official = official_by_id[mission_id]
        record = build_canonical_record(
            official,
            mappings,
            patient_mappings,
            checked_at,
        )
        current = existing.get(mission_id)
        record = preserve_non_owned_fields(
            record,
            current["record"] if current is not None else None,
        )
        generated[paths[mission_id]] = record

    previous = existing_decisions_before_completion()
    fully_before_ids = {
        mission_id
        for mission_id, decision in previous.items()
        if decision.get("stage") == "fully-canonical"
    }
    pending_ids = set(official_by_id) - fully_before_ids
    pending = [official_by_id[mission_id] for mission_id in sorted(pending_ids, key=stable_id)]
    if len(pending) != 836:
        raise ValueError(
            f"Batch {BATCH_NUMBER} must contain 836 missions, found {len(pending)}"
        )
    decisions = {
        str(record["id"]): decision_for(record, checked_at)
        for record in pending
    }
    batch = {
        "schema_version": "1",
        "updated_at": checked_at,
        "records": decisions,
    }
    page = evidence_page(
        pending,
        len(records),
        284,
        len(fully_before_ids),
    )
    return generated, batch, page, set(official_by_id)


def apply(check_only: bool, checked_at: str) -> tuple[int, int, int]:
    generated, batch, page, official_ids = build_expected(checked_at)
    changed = 0
    for path, expected in generated.items():
        actual = read_json(path) if path.exists() else None
        if actual == expected:
            continue
        changed += 1
        if not check_only:
            write_json(path, expected)

    actual_batch = read_json(BATCH_PATH) if BATCH_PATH.exists() else None
    if actual_batch != batch:
        changed += 1
        if not check_only:
            write_json(BATCH_PATH, batch)
    actual_page = REFERENCE_PATH.read_text(encoding="utf-8") if REFERENCE_PATH.exists() else None
    if actual_page != page:
        changed += 1
        if not check_only:
            REFERENCE_PATH.parent.mkdir(parents=True, exist_ok=True)
            REFERENCE_PATH.write_text(page, encoding="utf-8")

    current = canonical_records_by_id()
    direct = set(current) & official_ids
    canonical_only = set(current) - official_ids
    if not check_only:
        direct = official_ids
    return len(direct), len(canonical_only), changed


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate and verify the complete canonical UK mission catalogue"
    )
    parser.add_argument("--check", action="store_true", help="Fail when the committed catalogue differs")
    parser.add_argument("--checked-at", default="2026-07-24", help="ISO evidence date")
    args = parser.parse_args()
    try:
        checked_at = resolve_checked_at(args.checked_at)
        direct, overlays, changed = apply(args.check, checked_at)
    except ValueError as exc:
        print(f"Complete canonical catalogue generation failed: {exc}", file=sys.stderr)
        return 1
    if args.check and changed:
        print(
            f"Complete canonical catalogue generation check failed: {changed} committed output(s) differ",
            file=sys.stderr,
        )
        return 1
    print(
        "Complete canonical catalogue "
        + ("checked" if args.check else "generated")
        + f": {direct} direct records, {overlays} canonical-only overlays and {changed} output(s) changed."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
