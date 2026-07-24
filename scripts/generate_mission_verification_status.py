#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from datetime import date
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
OFFICIAL_PATH = ROOT / "data" / "sources" / "missionchief-uk" / "einsaetze.raw.json"
CANONICAL_ROOT = ROOT / "data" / "uk" / "missions"
REGISTRY_PATH = ROOT / "data" / "uk" / "mission-verification-registry.json"
SOURCE_OUTPUT = ROOT / "data" / "sources" / "missionchief-uk" / "mission-verification-status.json"
PUBLIC_OUTPUT = ROOT / "docs" / "assets" / "data" / "official" / "uk-mission-verification.json"
MARKDOWN_OUTPUT = ROOT / "docs" / "reference" / "mission-verification-status.md"

STAGES = (
    "captured",
    "identity-verified",
    "requirements-mapped",
    "operationally-verified",
    "fully-canonical",
)
STAGE_LABELS = {
    "captured": "Captured",
    "identity-verified": "Identity verified",
    "requirements-mapped": "Requirements mapped",
    "operationally-verified": "Operationally verified",
    "fully-canonical": "Fully canonical",
}
NEXT_ACTIONS = {
    "captured": "Create a canonical record and verify the official ID and exact UK mission name.",
    "identity-verified": "Map every published requirement, chance and prerequisite key without guessing.",
    "requirements-mapped": "Verify conditional behaviour, probabilities, patients, personnel, relationships and variants.",
    "operationally-verified": "Complete the final evidence-completeness audit and promote the registry entry.",
    "fully-canonical": "Maintain through source-change monitoring and periodic revalidation.",
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


def mission_name(record: dict[str, Any]) -> str:
    value = record.get("name") or record.get("caption") or record.get("title")
    return str(value).strip() if value is not None else ""


def canonical_records() -> tuple[list[dict[str, Any]], dict[str, tuple[dict[str, Any], str]]]:
    records: list[dict[str, Any]] = []
    by_id: dict[str, tuple[dict[str, Any], str]] = {}
    for path in sorted(CANONICAL_ROOT.glob("*.json")):
        record = read_json(path)
        if not isinstance(record, dict):
            raise ValueError(f"{path.relative_to(ROOT)}: canonical mission must be an object")
        mission_id = record.get("id")
        if mission_id is None or str(mission_id).strip() == "":
            raise ValueError(f"{path.relative_to(ROOT)}: canonical mission has no id")
        key = str(mission_id)
        if key in by_id:
            raise ValueError(f"Duplicate canonical mission id {key}")
        relative_path = path.relative_to(ROOT).as_posix()
        records.append(record)
        by_id[key] = (record, relative_path)
    return records, by_id


def validate_registry(
    registry: Any,
    official_by_id: dict[str, dict[str, Any]],
    canonical_by_id: dict[str, tuple[dict[str, Any], str]],
) -> dict[str, dict[str, Any]]:
    if not isinstance(registry, dict):
        raise ValueError("Mission verification registry must be an object")
    if registry.get("schema_version") != "1":
        raise ValueError("Mission verification registry schema_version must be '1'")
    if registry.get("target_stage") != "fully-canonical":
        raise ValueError("Mission verification registry target_stage must be fully-canonical")

    updated_at = registry.get("updated_at")
    if not isinstance(updated_at, str):
        raise ValueError("Mission verification registry updated_at is missing")
    try:
        date.fromisoformat(updated_at)
    except ValueError as exc:
        raise ValueError("Mission verification registry updated_at must be an ISO date") from exc

    documented_stages = registry.get("stages")
    if not isinstance(documented_stages, dict) or tuple(documented_stages) != STAGES:
        raise ValueError("Mission verification registry must document every stage in canonical order")

    records = registry.get("records")
    if not isinstance(records, dict):
        raise ValueError("Mission verification registry records must be an object keyed by official mission id")

    validated: dict[str, dict[str, Any]] = {}
    for mission_id, decision in records.items():
        key = str(mission_id)
        if key not in official_by_id:
            raise ValueError(f"Registry mission {key} does not exist in the official UK catalogue")
        if key not in canonical_by_id:
            raise ValueError(f"Registry mission {key} cannot be promoted without a direct canonical id match")
        if not isinstance(decision, dict):
            raise ValueError(f"Registry mission {key} decision must be an object")

        stage = decision.get("stage")
        if stage not in STAGES[2:]:
            raise ValueError(
                f"Registry mission {key} stage must explicitly promote to requirements-mapped, "
                "operationally-verified or fully-canonical"
            )

        checked_at = decision.get("checked_at")
        if not isinstance(checked_at, str):
            raise ValueError(f"Registry mission {key} checked_at is missing")
        try:
            date.fromisoformat(checked_at)
        except ValueError as exc:
            raise ValueError(f"Registry mission {key} checked_at must be an ISO date") from exc

        sources = decision.get("sources")
        if not isinstance(sources, list) or not sources or not all(isinstance(item, str) and item for item in sources):
            raise ValueError(f"Registry mission {key} must contain at least one evidence source")

        canonical, _ = canonical_by_id[key]
        official_name = mission_name(official_by_id[key])
        canonical_name = mission_name(canonical)
        if official_name.casefold() != canonical_name.casefold():
            raise ValueError(
                f"Registry mission {key} cannot be promoted while names differ: "
                f"official={official_name!r}, canonical={canonical_name!r}"
            )
        verification = canonical.get("verification")
        if not isinstance(verification, dict) or verification.get("status") != "verified":
            raise ValueError(f"Registry mission {key} requires a canonically verified mission record")

        validated[key] = decision
    return validated


def build_status() -> dict[str, Any]:
    official = read_json(OFFICIAL_PATH)
    registry = read_json(REGISTRY_PATH)
    if not isinstance(official, dict):
        raise ValueError("Official mission source envelope must be an object")
    official_records = official.get("records")
    if not isinstance(official_records, list) or not official_records:
        raise ValueError("Official mission source records must be a non-empty array")

    official_by_id: dict[str, dict[str, Any]] = {}
    for index, record in enumerate(official_records):
        if not isinstance(record, dict):
            raise ValueError(f"Official mission record {index} is not an object")
        mission_id = record.get("id")
        name = mission_name(record)
        if mission_id is None or str(mission_id).strip() == "" or not name:
            raise ValueError(f"Official mission record {index} has no stable id or name")
        key = str(mission_id)
        if key in official_by_id:
            raise ValueError(f"Duplicate official mission id {key}")
        official_by_id[key] = record

    canonical, canonical_by_id = canonical_records()
    registry_records = validate_registry(registry, official_by_id, canonical_by_id)
    stage_index = {stage: index for index, stage in enumerate(STAGES)}

    status_records: list[dict[str, Any]] = []
    name_mismatches = 0
    direct_matches = 0
    for mission_id in sorted(official_by_id, key=stable_id):
        official_record = official_by_id[mission_id]
        official_name = mission_name(official_record)
        canonical_pair = canonical_by_id.get(mission_id)
        canonical_record: dict[str, Any] | None = None
        canonical_path: str | None = None
        identity_matches = False
        stage = "captured"

        if canonical_pair is not None:
            direct_matches += 1
            canonical_record, canonical_path = canonical_pair
            canonical_name = mission_name(canonical_record)
            identity_matches = official_name.casefold() == canonical_name.casefold()
            if identity_matches:
                stage = "identity-verified"
            else:
                name_mismatches += 1

        decision = registry_records.get(mission_id)
        if decision is not None:
            promoted_stage = str(decision["stage"])
            if stage_index[promoted_stage] <= stage_index[stage]:
                raise ValueError(f"Registry mission {mission_id} does not advance beyond automatic stage {stage}")
            stage = promoted_stage

        verification = canonical_record.get("verification") if canonical_record else None
        blockers: list[str] = []
        if canonical_record is None:
            blockers.append("No direct canonical mission record exists for this official mission id.")
        elif not identity_matches:
            blockers.append("The canonical and official mission names do not match exactly.")
        elif stage != "fully-canonical":
            blockers.append(NEXT_ACTIONS[stage])

        status_records.append(
            {
                "id": official_record.get("id"),
                "name": official_name,
                "stage": stage,
                "stage_rank": stage_index[stage],
                "next_action": NEXT_ACTIONS[stage],
                "official_url": f"https://www.missionchief.co.uk/einsaetze/{mission_id}",
                "canonical_path": canonical_path,
                "canonical_verification_status": (
                    verification.get("status") if isinstance(verification, dict) else None
                ),
                "registry_decision": decision,
                "blocking_reasons": blockers,
            }
        )

    exact_counts = Counter(record["stage"] for record in status_records)
    cumulative_counts = {
        stage: sum(1 for record in status_records if record["stage_rank"] >= stage_index[stage])
        for stage in STAGES
    }
    official_count = len(status_records)
    fully_canonical = cumulative_counts["fully-canonical"]
    canonical_only = sorted(set(canonical_by_id) - set(official_by_id), key=stable_id)

    return {
        "schema_version": "1",
        "collection": "official-uk-mission-verification",
        "target_stage": "fully-canonical",
        "source": {
            "url": official.get("source_url"),
            "fetched_at": official.get("fetched_at"),
            "sha256": official.get("source_sha256"),
        },
        "registry_updated_at": registry.get("updated_at"),
        "summary": {
            "official_count": official_count,
            "canonical_count": len(canonical),
            "direct_canonical_id_matches": direct_matches,
            "canonical_only_count": len(canonical_only),
            "name_mismatch_count": name_mismatches,
            "registry_promotions": len(registry_records),
            "exact_stage_counts": {stage: exact_counts.get(stage, 0) for stage in STAGES},
            "cumulative_stage_counts": cumulative_counts,
            "fully_canonical_percent": round(fully_canonical / official_count * 100, 2),
            "remaining_to_fully_canonical": official_count - fully_canonical,
        },
        "canonical_only_ids": canonical_only,
        "records": status_records,
    }


def markdown(status: dict[str, Any]) -> str:
    summary = status["summary"]
    cumulative = summary["cumulative_stage_counts"]
    exact = summary["exact_stage_counts"]
    official_count = summary["official_count"]

    lines = [
        "# Mission Verification Status",
        "",
        "This page is generated from the complete official UK mission catalogue, the canonical mission records and the explicit mission-verification registry.",
        "",
        "!!! warning \"100% means fully canonical\"",
        "    A mission is not counted as complete merely because it exists in the official feed. It must complete identity, requirement, operational and evidence-completeness verification.",
        "",
        "## Current programme position",
        "",
        "| Verification gate | Missions at or beyond gate | Coverage | Exact current stage |",
        "|---|---:|---:|---:|",
    ]
    for stage in STAGES:
        count = cumulative[stage]
        percent = count / official_count * 100 if official_count else 0
        lines.append(
            f"| {STAGE_LABELS[stage]} | {count:,} / {official_count:,} | {percent:.2f}% | {exact[stage]:,} |"
        )

    lines.extend(
        [
            "",
            f"**Remaining to fully canonical:** {summary['remaining_to_fully_canonical']:,}",
            "",
            f"**Direct canonical ID matches:** {summary['direct_canonical_id_matches']:,}",
            "",
            f"**Canonical overlay or derived records:** {summary['canonical_only_count']:,}",
            "",
            "## Verification gates",
            "",
            "1. **Captured** — retained losslessly from the official UK mission feed.",
            "2. **Identity verified** — official ID and exact UK name match a canonical record.",
            "3. **Requirements mapped** — published requirement, chance and prerequisite keys are normalized without guessing.",
            "4. **Operationally verified** — conditional mechanics, probabilities, patients, personnel, relationships and variants have reproducible evidence.",
            "5. **Fully canonical** — a final evidence-completeness audit has been completed.",
            "",
            "## Highest-priority backlog",
            "",
            "The table below shows the first 100 incomplete missions in deterministic mission-ID order within the lowest verification stage. The complete backlog is available from `assets/data/official/uk-mission-verification.json`.",
            "",
            "| ID | Mission | Current stage | Next action |",
            "|---:|---|---|---|",
        ]
    )

    backlog = [record for record in status["records"] if record["stage"] != "fully-canonical"]
    backlog.sort(key=lambda record: (record["stage_rank"], stable_id(record["id"])))
    for record in backlog[:100]:
        name = str(record["name"]).replace("|", "\\|")
        action = str(record["next_action"]).replace("|", "\\|")
        lines.append(f"| `{record['id']}` | {name} | {STAGE_LABELS[record['stage']]} | {action} |")

    lines.extend(
        [
            "",
            "## Machine-readable status",
            "",
            "```text",
            "assets/data/official/uk-mission-verification.json",
            "```",
            "",
            "The machine-readable document contains every official mission, its current verification gate, canonical path when present, registry decision, blockers and next action.",
            "",
        ]
    )
    return "\n".join(lines)


def render_outputs(status: dict[str, Any]) -> dict[Path, str]:
    compact = json.dumps(status, ensure_ascii=False, separators=(",", ":"), sort_keys=False) + "\n"
    return {
        SOURCE_OUTPUT: compact,
        PUBLIC_OUTPUT: compact,
        MARKDOWN_OUTPUT: markdown(status),
    }


def apply_outputs(outputs: dict[Path, str], check: bool) -> None:
    mismatches: list[str] = []
    for path, expected in outputs.items():
        if check:
            try:
                current = path.read_text(encoding="utf-8")
            except OSError:
                mismatches.append(f"missing {path.relative_to(ROOT)}")
                continue
            if current != expected:
                mismatches.append(f"stale {path.relative_to(ROOT)}")
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(expected, encoding="utf-8")
    if mismatches:
        raise ValueError("Mission verification outputs are not current: " + ", ".join(mismatches))


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate the 100% UK mission verification programme status")
    parser.add_argument("--check", action="store_true", help="Fail when committed generated outputs are missing or stale")
    parser.add_argument(
        "--require-complete",
        action="store_true",
        help="Fail unless every official UK mission is explicitly fully canonical",
    )
    args = parser.parse_args()

    try:
        status = build_status()
        apply_outputs(render_outputs(status), check=args.check)
        summary = status["summary"]
        if args.require_complete and summary["remaining_to_fully_canonical"] != 0:
            raise ValueError(
                f"100% verification gate is not met: {summary['remaining_to_fully_canonical']} missions remain"
            )
    except ValueError as exc:
        print(f"Mission verification status generation failed: {exc}", file=sys.stderr)
        return 1

    summary = status["summary"]
    print(
        "Mission verification status generated: "
        f"{summary['fully_canonical_percent']:.2f}% fully canonical, "
        f"{summary['remaining_to_fully_canonical']} of {summary['official_count']} missions remaining."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
