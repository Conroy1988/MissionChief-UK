#!/usr/bin/env python3

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any, Iterable

import yaml

ROOT = Path(__file__).resolve().parents[1]
SOURCE_STATUS = ROOT / "data" / "sources" / "missionchief-uk" / "mission-verification-status.json"
PUBLIC_STATUS = ROOT / "docs" / "assets" / "data" / "official" / "uk-mission-verification.json"
BATCH_ROOT = ROOT / "data" / "uk" / "mission-verification-batches"
REFERENCE_ROOT = ROOT / "docs" / "reference"
BATCH_REGISTRY_PATTERN = re.compile(r"fully-canonical-fire-batch-(\d+)\.json$")
BATCH_PAGE_PATTERN = re.compile(r"fully-canonical-mission-batch-(\d+)\.md$")

REQUIRED_FILES = (
    "data/uk/mission-verification-registry.json",
    "data/uk/official-key-mappings.json",
    "scripts/merge_verification_registry_batches.py",
    "scripts/validate_official_key_mappings.py",
    "scripts/validate_official_patient_mappings.py",
    "scripts/validate_official_personnel_mappings.py",
    "scripts/validate_official_personnel_education_mappings.py",
    "scripts/validate_official_prisoner_mappings.py",
    "scripts/validate_official_recovery_mappings.py",
    "scripts/validate_official_operational_mappings.py",
    "scripts/generate_full_canonical_catalogue.py",
    "scripts/generate_mission_verification_status.py",
    "scripts/run_public_verification_sync.py",
    "scripts/validate_verification_programme_assets.py",
    "scripts/run_full_data_audit.sh",
    "scripts/classify_ci_changes.py",
    "tests/python/test_ci_change_classifier.py",
    "data/sources/missionchief-uk/mission-verification-status.json",
    "docs/assets/data/official/uk-mission-verification.json",
    "docs/reference/mission-verification-status.md",
    ".github/workflows/branch-validation-report.yml",
    ".github/workflows/production-pages-verification.yml",
    "DELIVERY_ACCELERATION.md",
)

COMMON_EVIDENCE_MARKERS = (
    "reconcile_official_mission_coverage.py",
    "merge_verification_registry_batches.py",
    "validate_official_key_mappings.py",
    "validate_official_patient_mappings.py",
    "validate_official_personnel_mappings.py",
    "validate_official_personnel_education_mappings.py",
    "validate_official_prisoner_mappings.py",
    "validate_official_recovery_mappings.py",
    "validate_official_operational_mappings.py",
    "generate_full_canonical_catalogue.py",
    "python -m unittest discover -s tests/python",
    "generate_mission_verification_status.py",
    "validate_verification_programme_assets.py",
)


def read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"{path.relative_to(ROOT)}: unable to read JSON: {exc}") from exc


def flatten_nav(value: Any) -> Iterable[str]:
    if isinstance(value, str):
        yield value
    elif isinstance(value, list):
        for item in value:
            yield from flatten_nav(item)
    elif isinstance(value, dict):
        for item in value.values():
            yield from flatten_nav(item)


def numbered_paths(root: Path, glob_pattern: str, pattern: re.Pattern[str]) -> dict[int, Path]:
    result: dict[int, Path] = {}
    for path in sorted(root.glob(glob_pattern)):
        match = pattern.search(path.name)
        if match is None:
            continue
        number = int(match.group(1))
        if number in result:
            raise ValueError(f"Duplicate fully canonical batch number {number}")
        result[number] = path
    return result


def validate_batch_assets() -> int:
    registries = numbered_paths(BATCH_ROOT, "fully-canonical-fire-batch-*.json", BATCH_REGISTRY_PATTERN)
    pages = numbered_paths(REFERENCE_ROOT, "fully-canonical-mission-batch-*.md", BATCH_PAGE_PATTERN)
    if not registries or not pages:
        raise ValueError("Mission verification batch assets are missing")
    if sorted(pages) != list(range(1, max(pages) + 1)):
        raise ValueError(f"Fully canonical batch pages are not contiguous: {sorted(pages)}")
    if sorted(registries) != list(range(3, max(registries) + 1)):
        raise ValueError(f"Fully canonical batch registries are not contiguous: {sorted(registries)}")
    if max(registries) != max(pages):
        raise ValueError("Latest verification registry and evidence page differ")

    seen: set[str] = set()
    for number, path in sorted(registries.items()):
        document = read_json(path)
        records = document.get("records") if isinstance(document, dict) else None
        if document.get("schema_version") != "1" or not isinstance(records, dict) or not records:
            raise ValueError(f"Invalid verification batch registry: {path.relative_to(ROOT)}")
        if number < 3:
            raise ValueError("Dynamic verification batches must begin at Batch 3")
        for mission_id in records:
            key = str(mission_id)
            if key in seen:
                raise ValueError(f"Duplicate batch verification decision for mission {key}")
            seen.add(key)

    config = yaml.safe_load((ROOT / "mkdocs.yml").read_text(encoding="utf-8"))
    if not isinstance(config, dict):
        raise ValueError("mkdocs.yml must contain a mapping")
    nav_targets = set(flatten_nav(config.get("nav")))
    required_nav = {"reference/mission-verification-status.md"}
    required_nav.update(path.relative_to(REFERENCE_ROOT.parent).as_posix() for path in pages.values())
    missing = sorted(required_nav - nav_targets)
    if missing:
        raise ValueError(f"Verification pages are missing from navigation: {missing}")
    return len(pages)


def validate_status() -> dict[str, Any]:
    source = read_json(SOURCE_STATUS)
    public = read_json(PUBLIC_STATUS)
    if source != public:
        raise ValueError("Public mission verification endpoint differs from generated source status")
    if not isinstance(source, dict) or source.get("schema_version") != "1":
        raise ValueError("Mission verification status metadata is invalid")
    if source.get("collection") != "official-uk-mission-verification":
        raise ValueError("Mission verification collection is invalid")
    if source.get("target_stage") != "fully-canonical":
        raise ValueError("Mission verification target stage is invalid")

    summary = source.get("summary")
    records = source.get("records")
    if not isinstance(summary, dict) or not isinstance(records, list):
        raise ValueError("Mission verification summary or records are invalid")

    official = summary.get("official_count")
    canonical = summary.get("canonical_count")
    direct = summary.get("direct_canonical_id_matches")
    fully = summary.get("cumulative_stage_counts", {}).get("fully-canonical")
    remaining = summary.get("remaining_to_fully_canonical")
    if not all(isinstance(value, int) for value in (official, canonical, direct, fully, remaining)):
        raise ValueError("Mission verification completion metrics must be integers")
    if official != len(records) or fully + remaining != official or fully > direct or direct > canonical:
        raise ValueError("Mission verification completion arithmetic is inconsistent")

    ids = [str(record.get("id")) for record in records if isinstance(record, dict)]
    if len(ids) != official or len(ids) != len(set(ids)):
        raise ValueError("Mission verification records must contain unique IDs")
    return summary


def require_markers(path: str, markers: tuple[str, ...]) -> str:
    text = (ROOT / path).read_text(encoding="utf-8")
    for marker in markers:
        if marker not in text:
            raise ValueError(f"{path} does not enforce {marker}")
    return text


def validate_delivery_architecture() -> None:
    require_markers(
        ".github/workflows/branch-validation-report.yml",
        (
            "run_full_data_audit.sh",
            "DIAGNOSTICS_DIR",
            "stage36b-built-site",
            "Chromium and WebKit acceptance",
            "schedule:",
            "github.event.pull_request.draft == false",
            "stage36b/full-audit",
            "actionlint_1.7.12_linux_amd64.tar.gz",
        ),
    )

    deploy = require_markers(
        ".github/workflows/deploy-pages.yml",
        (
            "validate_data.py",
            "release_readiness.py",
            "audit_links.py",
            "mkdocs build --strict",
            "actions/upload-pages-artifact",
            "actions/deploy-pages",
            "smoke_pages.py",
        ),
    )
    for forbidden in (
        "playwright install",
        "npm run test:e2e",
        "validate_official_key_mappings.py",
        "merge_verification_registry_batches.py",
    ):
        if forbidden in deploy:
            raise ValueError(f"Pages deployment retains slow-path control: {forbidden}")

    require_markers(
        ".github/workflows/production-pages-verification.yml",
        (
            "workflow_run:",
            "github.event.workflow_run.head_sha",
            "github.event.workflow_run.head_branch == 'main'",
            "smoke_pages.py",
            "npm run test:e2e",
            "retention-days: 30",
        ),
    )

    vehicle = require_markers(
        ".github/workflows/vehicle-inventory-validation.yml",
        (
            "validate_vehicle_inventory.py",
            "generate_vehicle_field_resolution.py --check",
            "generate_vehicle_coverage.py --check",
            "test_vehicle_inventory.py",
            "workflow_dispatch:",
        ),
    )
    if "pull_request:" in vehicle:
        raise ValueError("Dedicated vehicle workflow must not duplicate pull-request validation")

    require_markers(".github/workflows/release-v1.yml", COMMON_EVIDENCE_MARKERS)
    require_markers(
        ".github/workflows/import-official-uk-missions.yml",
        (*COMMON_EVIDENCE_MARKERS, "report_canonical_candidates.py", "report_key_mapping_backlog.py"),
    )
    require_markers(
        "scripts/run_full_data_audit.sh",
        (
            *COMMON_EVIDENCE_MARKERS,
            "report_promoted_mapping_failures.py",
            "report_canonical_candidates.py",
            "report_key_mapping_backlog.py",
            "run_public_verification_sync.py",
            "sync_verification_batch_navigation.py",
            "DIAGNOSTICS_DIR",
            "check_validation_worktree.py synchronizer",
            "check_validation_worktree.py final-working-tree",
        ),
    )

    validate_workflow = (ROOT / ".github/workflows/validate.yml").read_text(encoding="utf-8")
    if "documentation-fast" in validate_workflow:
        require_markers(
            ".github/workflows/validate.yml",
            (
                "classify_ci_changes.py",
                "documentation-fast",
                "data-fast",
                "vehicle-fast",
                "interface-fast",
                "workflow-fast",
                "Validation result",
                "playwright install --with-deps chromium",
                "converted_to_draft",
            ),
        )
    else:
        require_markers(
            ".github/workflows/validate.yml",
            (
                "Validate canonical JSON documents",
                "Build documentation strictly",
                "Run browser acceptance tests against built site",
            ),
        )


def main() -> int:
    try:
        for relative in REQUIRED_FILES:
            if not (ROOT / relative).is_file():
                raise ValueError(f"Required verification programme file is missing: {relative}")
        batch_count = validate_batch_assets()
        summary = validate_status()
        validate_delivery_architecture()
    except (OSError, ValueError, yaml.YAMLError) as exc:
        print(f"Mission verification programme asset audit failed: {exc}", file=sys.stderr)
        return 1

    fully = summary["cumulative_stage_counts"]["fully-canonical"]
    print(
        "Mission verification programme asset audit passed: "
        f"{fully}/{summary['official_count']} fully canonical, "
        f"{summary['canonical_count']} canonical records, "
        f"{batch_count} evidence batch pages and "
        f"{summary['remaining_to_fully_canonical']} missions remaining."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
