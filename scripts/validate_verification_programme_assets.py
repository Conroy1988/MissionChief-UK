#!/usr/bin/env python3

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
SOURCE_STATUS = ROOT / "data" / "sources" / "missionchief-uk" / "mission-verification-status.json"
PUBLIC_STATUS = ROOT / "docs" / "assets" / "data" / "official" / "uk-mission-verification.json"

REQUIRED_FILES = (
    "data/uk/mission-verification-registry.json",
    "data/uk/official-key-mappings.json",
    "scripts/reconcile_official_mission_coverage.py",
    "scripts/validate_official_key_mappings.py",
    "scripts/generate_mission_verification_status.py",
    "scripts/validate_verification_programme_assets.py",
    "data/sources/missionchief-uk/mission-verification-status.json",
    "docs/assets/data/official/uk-mission-verification.json",
    "docs/reference/mission-verification-status.md",
    "docs/reference/fully-canonical-mission-batch-1.md",
)

REQUIRED_NAV_TARGETS = (
    "reference/mission-verification-status.md",
    "reference/fully-canonical-mission-batch-1.md",
)

WORKFLOW_MARKERS = {
    ".github/workflows/validate.yml": (
        "reconcile_official_mission_coverage.py",
        "validate_official_key_mappings.py",
        "generate_mission_verification_status.py",
        "validate_verification_programme_assets.py",
    ),
    ".github/workflows/deploy-pages.yml": (
        "reconcile_official_mission_coverage.py",
        "validate_official_key_mappings.py",
        "generate_mission_verification_status.py",
        "validate_verification_programme_assets.py",
    ),
    ".github/workflows/release-v1.yml": (
        "reconcile_official_mission_coverage.py",
        "validate_official_key_mappings.py",
        "generate_mission_verification_status.py",
        "validate_verification_programme_assets.py",
    ),
    ".github/workflows/import-official-uk-missions.yml": (
        "reconcile_official_mission_coverage.py",
        "validate_official_key_mappings.py",
        "generate_mission_verification_status.py",
        "validate_verification_programme_assets.py",
    ),
}


def read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"{path.relative_to(ROOT)}: unable to read JSON: {exc}") from exc


def flatten_nav(value: Any) -> list[str]:
    result: list[str] = []
    if isinstance(value, str):
        result.append(value)
    elif isinstance(value, list):
        for item in value:
            result.extend(flatten_nav(item))
    elif isinstance(value, dict):
        for item in value.values():
            result.extend(flatten_nav(item))
    return result


def validate_status(status: Any) -> dict[str, Any]:
    if not isinstance(status, dict):
        raise ValueError("Mission verification status must be an object")
    if status.get("schema_version") != "1":
        raise ValueError("Mission verification status schema_version must be '1'")
    if status.get("collection") != "official-uk-mission-verification":
        raise ValueError("Mission verification status collection is invalid")
    if status.get("target_stage") != "fully-canonical":
        raise ValueError("Mission verification status target_stage must be fully-canonical")

    summary = status.get("summary")
    records = status.get("records")
    if not isinstance(summary, dict) or not isinstance(records, list):
        raise ValueError("Mission verification status summary or records are invalid")

    official_count = summary.get("official_count")
    canonical_count = summary.get("canonical_count")
    fully_canonical = summary.get("cumulative_stage_counts", {}).get("fully-canonical")
    remaining = summary.get("remaining_to_fully_canonical")
    if not isinstance(official_count, int) or official_count != len(records):
        raise ValueError("Mission verification official_count does not match its records")
    if not isinstance(canonical_count, int) or canonical_count < 1:
        raise ValueError("Mission verification canonical_count is invalid")
    if not isinstance(fully_canonical, int) or not isinstance(remaining, int):
        raise ValueError("Mission verification completion metrics are invalid")
    if fully_canonical + remaining != official_count:
        raise ValueError("Mission verification completion arithmetic is inconsistent")

    record_ids = [str(record.get("id")) for record in records if isinstance(record, dict)]
    if len(record_ids) != official_count or len(record_ids) != len(set(record_ids)):
        raise ValueError("Mission verification records must contain unique IDs")

    return summary


def audit() -> dict[str, Any]:
    for relative in REQUIRED_FILES:
        if not (ROOT / relative).is_file():
            raise ValueError(f"Required verification programme file is missing: {relative}")

    source_status = read_json(SOURCE_STATUS)
    public_status = read_json(PUBLIC_STATUS)
    if source_status != public_status:
        raise ValueError("Public mission verification endpoint differs from generated source status")
    summary = validate_status(source_status)

    config = yaml.safe_load((ROOT / "mkdocs.yml").read_text(encoding="utf-8"))
    if not isinstance(config, dict):
        raise ValueError("mkdocs.yml must contain an object")
    nav_targets = set(flatten_nav(config.get("nav")))
    for target in REQUIRED_NAV_TARGETS:
        if target not in nav_targets:
            raise ValueError(f"Verification programme page is missing from MkDocs navigation: {target}")

    for workflow, markers in WORKFLOW_MARKERS.items():
        text = (ROOT / workflow).read_text(encoding="utf-8")
        for marker in markers:
            if marker not in text:
                raise ValueError(f"Workflow {workflow} does not enforce {marker}")

    return summary


def main() -> int:
    try:
        summary = audit()
    except (OSError, ValueError, yaml.YAMLError) as exc:
        print(f"Mission verification programme asset audit failed: {exc}", file=sys.stderr)
        return 1

    fully_canonical = summary["cumulative_stage_counts"]["fully-canonical"]
    print(
        "Mission verification programme asset audit passed: "
        f"{fully_canonical}/{summary['official_count']} fully canonical, "
        f"{summary['canonical_count']} canonical records and "
        f"{summary['remaining_to_fully_canonical']} missions remaining."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
