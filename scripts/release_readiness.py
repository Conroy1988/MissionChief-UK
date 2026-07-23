#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any, Iterable

import yaml

ROOT = Path(__file__).resolve().parents[1]
DATA_ROOT = ROOT / "data" / "uk"
OUTPUT_ROOT = ROOT / "docs" / "assets" / "data" / "v1"
OFFICIAL_OUTPUT_ROOT = ROOT / "docs" / "assets" / "data" / "official"
VERSION_PATH = ROOT / "data" / "version.json"
MKDOCS_PATH = ROOT / "mkdocs.yml"
README_PATH = ROOT / "README.md"

COLLECTIONS = {
    "missions": DATA_ROOT / "missions",
    "vehicles": DATA_ROOT / "vehicles",
    "infrastructure": DATA_ROOT / "infrastructure",
    "training": DATA_ROOT / "training",
}

EXPECTED_STATIC_PAGES = (
    "tools/mission-lookup.md",
    "tools/resource-comparison.md",
    "tools/fleet-planner.md",
    "tools/query-catalogue.md",
    "reference/official-mission-catalogue.md",
    "reference/mission-verification-status.md",
    "reference/generated-faq.md",
    "api/index.md",
    "quality-assurance.md",
)

REQUIRED_QA_FILES = (
    "package.json",
    "playwright.config.mjs",
    "tests/e2e/live-site.spec.mjs",
    "tests/e2e/official-mission-catalogue.spec.mjs",
    "scripts/audit_links.py",
    "scripts/validate_official_mission_catalogue.py",
    "scripts/reconcile_official_mission_coverage.py",
    "scripts/verification_registry.py",
    "scripts/merge_verification_registry_batches.py",
    "scripts/validate_official_key_mappings.py",
    "scripts/report_canonical_candidates.py",
    "scripts/report_key_mapping_backlog.py",
    "scripts/generate_mission_verification_status.py",
    "scripts/validate_verification_programme_assets.py",
    "docs/quality-assurance.md",
)

REQUIRED_OFFICIAL_FILES = (
    "scripts/import_official_uk_missions.py",
    "scripts/publish_official_mission_catalogue.py",
    "scripts/compact_official_mission_catalogue.py",
    ".github/workflows/import-official-uk-missions.yml",
    "data/uk/mission-verification-registry.json",
    "data/uk/official-key-mappings.json",
    "data/sources/missionchief-uk/README.md",
    "data/sources/missionchief-uk/einsaetze.raw.json",
    "data/sources/missionchief-uk/mission-coverage.json",
    "data/sources/missionchief-uk/mission-verification-status.json",
    "data/sources/missionchief-uk/official-key-inventory.json",
    "docs/assets/data/official/uk-missions.json",
    "docs/assets/data/official/uk-mission-coverage.json",
    "docs/assets/data/official/uk-mission-verification.json",
    "docs/javascripts/official-catalogue-loader.js",
    "docs/javascripts/official-mission-details.js",
    "docs/reference/mission-verification-status.md",
)

REQUIRED_JAVASCRIPT_ORDER = (
    "javascripts/official-catalogue-loader.js",
    "javascripts/intelligence-tools.js",
    "javascripts/official-mission-details.js",
)

PLAYWRIGHT_PROJECTS = (
    "chromium-desktop",
    "firefox-desktop",
    "webkit-iphone",
    "webkit-ipad",
)


class AuditFailure(RuntimeError):
    pass


def read_json(path: Path) -> Any:
    try:
        with path.open("r", encoding="utf-8") as handle:
            return json.load(handle)
    except FileNotFoundError as exc:
        raise AuditFailure(f"Required file is missing: {path.relative_to(ROOT)}") from exc
    except json.JSONDecodeError as exc:
        raise AuditFailure(f"Invalid JSON in {path.relative_to(ROOT)}: {exc}") from exc


def stable_id(record: dict[str, Any]) -> tuple[str, str]:
    return (str(record.get("id", "")), str(record.get("name", "")))


def load_source_collection(directory: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for path in sorted(directory.glob("*.json")):
        record = read_json(path)
        if not isinstance(record, dict):
            raise AuditFailure(f"Collection record must be an object: {path.relative_to(ROOT)}")
        records.append(record)
    return sorted(records, key=stable_id)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AuditFailure(message)


def exposes_number(text: str, value: int) -> bool:
    return str(value) in text or f"{value:,}" in text


def flatten_nav(value: Any) -> Iterable[str]:
    if isinstance(value, str):
        yield value
    elif isinstance(value, list):
        for item in value:
            yield from flatten_nav(item)
    elif isinstance(value, dict):
        for item in value.values():
            yield from flatten_nav(item)


def audit_navigation(release_version: str) -> None:
    config = yaml.safe_load(MKDOCS_PATH.read_text(encoding="utf-8"))
    require(isinstance(config, dict), "mkdocs.yml must contain a mapping")
    nav = config.get("nav")
    require(isinstance(nav, list), "mkdocs.yml must define a navigation list")

    nav_targets = set(flatten_nav(nav))
    for target in nav_targets:
        require((ROOT / "docs" / target).is_file(), f"MkDocs navigation target does not exist: docs/{target}")

    dynamic_batches = [
        path.relative_to(ROOT / "docs").as_posix()
        for path in sorted((ROOT / "docs" / "reference").glob("fully-canonical-mission-batch-*.md"))
    ]
    for target in (*EXPECTED_STATIC_PAGES, *dynamic_batches, f"releases/v{release_version}.md"):
        require(target in nav_targets, f"Release-critical page is not present in MkDocs navigation: {target}")

    javascript = config.get("extra_javascript", [])
    require(isinstance(javascript, list), "MkDocs extra_javascript must be a list")
    for asset in REQUIRED_JAVASCRIPT_ORDER:
        require(asset in javascript, f"MkDocs must load {asset}")
    positions = [javascript.index(asset) for asset in REQUIRED_JAVASCRIPT_ORDER]
    require(positions == sorted(positions), "Official catalogue loader, lookup and detail scripts are in the wrong order")


def audit_quality_assets(release_version: str) -> None:
    for relative in (*REQUIRED_QA_FILES, *REQUIRED_OFFICIAL_FILES):
        require((ROOT / relative).is_file(), f"Release-critical file is missing: {relative}")

    batch_files = sorted((DATA_ROOT / "mission-verification-batches").glob("*.json"))
    require(bool(batch_files), "No mission verification batch registry files exist")

    package = read_json(ROOT / "package.json")
    require(isinstance(package, dict), "package.json must contain an object")
    require(package.get("version") == release_version, "package.json version does not match data/version.json")
    scripts = package.get("scripts")
    require(
        isinstance(scripts, dict) and scripts.get("test:e2e") == "playwright test",
        "package.json must expose the Playwright test:e2e command",
    )
    dependencies = package.get("devDependencies")
    require(isinstance(dependencies, dict), "package.json must define devDependencies")
    for dependency in ("@playwright/test", "@axe-core/playwright"):
        require(dependency in dependencies, f"package.json is missing QA dependency: {dependency}")

    config_text = (ROOT / "playwright.config.mjs").read_text(encoding="utf-8")
    for project in PLAYWRIGHT_PROJECTS:
        require(project in config_text, f"Playwright configuration is missing project: {project}")

    suite_text = (ROOT / "tests" / "e2e" / "live-site.spec.mjs").read_text(encoding="utf-8")
    for marker in ("mission-lookup", "comparison", "fleet-planner", "query-catalogue", "AxeBuilder"):
        require(marker in suite_text, f"Browser acceptance suite is missing coverage marker: {marker}")

    official_suite = (ROOT / "tests" / "e2e" / "official-mission-catalogue.spec.mjs").read_text(encoding="utf-8")
    for marker in (
        "official-uk-missions",
        "official_only_count",
        "officialOnlyIds",
        "pendingRecord",
        "Coverage must retain an official-only record",
        "pendingUrl",
        "Complete official catalogue record",
        "mcuk-official-field-details",
    ):
        require(marker in official_suite, f"Official mission acceptance suite is missing marker: {marker}")

    workflow_text = (ROOT / ".github" / "workflows" / "import-official-uk-missions.yml").read_text(encoding="utf-8")
    for marker in (
        "workflow_dispatch",
        "schedule:",
        "reconcile_official_mission_coverage.py",
        "validate_official_mission_catalogue.py",
        "merge_verification_registry_batches.py",
        "validate_official_key_mappings.py",
        "report_canonical_candidates.py",
        "generate_mission_verification_status.py",
        "validate_verification_programme_assets.py",
        "git diff --cached --quiet",
        "gh workflow run deploy-pages.yml --ref main",
    ):
        require(marker in workflow_text, f"Official catalogue refresh workflow is missing control: {marker}")


def release_metadata() -> dict[str, Any]:
    release = read_json(VERSION_PATH)
    require(isinstance(release, dict), "data/version.json must contain an object")
    version = release.get("version")
    require(
        isinstance(version, str) and re.fullmatch(r"1\.\d+\.\d+", version) is not None,
        "data/version.json must contain a v1 semantic version",
    )
    require(release.get("stage") == 34, "The v1 release must identify Stage 34")
    require(release.get("status") == "production", "The v1 release status must be production")
    require(
        (ROOT / "docs" / "releases" / f"v{version}.md").is_file(),
        f"Release notes are missing for v{version}",
    )
    return release


def audit_exports(release: dict[str, Any]) -> dict[str, int]:
    release_version = release["version"]
    manifest = read_json(OUTPUT_ROOT / "manifest.json")
    require(manifest.get("api_version") == "v1", "Manifest api_version must be v1")
    require(manifest.get("data_version") == release_version, "Manifest data_version does not match data/version.json")
    require(manifest.get("released_at") == release.get("released_at"), "Manifest release date does not match data/version.json")
    require(manifest.get("stage") == release.get("stage"), "Manifest stage does not match data/version.json")
    require(manifest.get("status") == release.get("status"), "Manifest status does not match data/version.json")

    manifest_collections = manifest.get("collections")
    require(isinstance(manifest_collections, dict), "Manifest collections must be an object")

    counts: dict[str, int] = {}
    search_keys: set[tuple[str, str]] = set()
    for name, directory in COLLECTIONS.items():
        source_records = load_source_collection(directory)
        payload = read_json(OUTPUT_ROOT / f"{name}.json")
        require(payload.get("schema_version") == "1", f"{name}.json schema_version must be 1")
        require(payload.get("data_version") == release_version, f"{name}.json data_version mismatch")
        require(payload.get("released_at") == release.get("released_at"), f"{name}.json release date mismatch")
        require(payload.get("collection") == name, f"{name}.json collection name mismatch")
        exported_records = payload.get("records")
        require(isinstance(exported_records, list), f"{name}.json records must be an array")
        require(exported_records == source_records, f"{name}.json is not a deterministic copy of the canonical records")
        require(payload.get("count") == len(source_records), f"{name}.json count does not match canonical files")

        collection_manifest = manifest_collections.get(name)
        require(isinstance(collection_manifest, dict), f"Manifest is missing collection: {name}")
        require(collection_manifest.get("count") == len(source_records), f"Manifest count mismatch for {name}")
        require(collection_manifest.get("path") == f"{name}.json", f"Manifest path mismatch for {name}")

        ids = [str(record.get("id")) for record in source_records]
        require(len(ids) == len(set(ids)), f"Duplicate canonical IDs detected in {name}")
        counts[name] = len(source_records)
        search_keys.update((name, record_id) for record_id in ids)

    search_index = read_json(OUTPUT_ROOT / "search-index.json")
    search_records = search_index.get("records")
    require(isinstance(search_records, list), "search-index.json records must be an array")
    require(search_index.get("data_version") == release_version, "Search-index version mismatch")
    require(search_index.get("count") == len(search_records), "Search-index count does not match its records")
    actual_search_keys = {
        (str(item.get("collection")), str(item.get("id")))
        for item in search_records
        if isinstance(item, dict)
    }
    require(actual_search_keys == search_keys, "Search index does not contain exactly one entry for every canonical record")

    faq = read_json(OUTPUT_ROOT / "faq.json")
    entries = faq.get("entries")
    require(isinstance(entries, list) and entries, "faq.json must contain at least one FAQ entry")
    require(faq.get("count") == len(entries), "FAQ count does not match FAQ entries")
    require(faq.get("data_version") == release_version, "FAQ version mismatch")

    openapi = read_json(OUTPUT_ROOT / "openapi.json")
    require(openapi.get("openapi") == "3.1.0", "OpenAPI contract must use OpenAPI 3.1.0")
    require(openapi.get("info", {}).get("version") == release_version, "OpenAPI version mismatch")
    paths = openapi.get("paths")
    require(isinstance(paths, dict), "OpenAPI paths must be an object")
    expected_paths = {"/manifest.json", "/search-index.json", "/faq.json"}
    expected_paths.update(f"/{name}.json" for name in COLLECTIONS)
    require(expected_paths.issubset(paths), "OpenAPI contract is missing one or more public collection paths")

    require(manifest.get("search_index", {}).get("path") == "search-index.json", "Manifest search-index path mismatch")
    require(manifest.get("faq", {}).get("path") == "faq.json", "Manifest FAQ path mismatch")
    require(manifest.get("openapi", {}).get("path") == "openapi.json", "Manifest OpenAPI path mismatch")

    verification = read_json(OFFICIAL_OUTPUT_ROOT / "uk-mission-verification.json")
    summary = verification.get("summary")
    require(isinstance(summary, dict), "Verification endpoint summary is missing")
    fully_canonical = summary.get("cumulative_stage_counts", {}).get("fully-canonical")
    direct_matches = summary.get("direct_canonical_id_matches")
    remaining = summary.get("remaining_to_fully_canonical")
    require(summary.get("canonical_count") == counts["missions"], "Verification canonical count mismatch")
    require(isinstance(fully_canonical, int), "Verification fully canonical count is invalid")
    require(isinstance(direct_matches, int), "Verification direct match count is invalid")
    require(isinstance(remaining, int), "Verification remaining count is invalid")

    readme = README_PATH.read_text(encoding="utf-8")
    readme_lower = readme.lower()
    readme_words = re.sub(r"[^a-z0-9]+", " ", readme_lower)
    for name, count in counts.items():
        require(exposes_number(readme, count), f"README does not expose the current {name} count ({count})")
    require(
        "stage_34_complete" in readme_lower or "stage 34 complete" in readme_words,
        "README stage badge is not synchronized to Stage 34",
    )
    require(
        release_version in readme_lower and "static api" in readme_words,
        f"README does not identify Static API v{release_version}",
    )
    require(exposes_number(readme, 1062), "README does not expose the official UK mission catalogue baseline")
    require(f"{fully_canonical} fully canonical" in readme_lower, "README fully canonical count is stale")
    require(exposes_number(readme, direct_matches), "README direct canonical match count is stale")
    require(exposes_number(readme, remaining), "README remaining verification count is stale")
    require("11 fully canonical" in readme_lower, "README does not preserve the Batch 1 historical milestone")
    return counts


def audit_built_site(site_dir: Path, release_version: str) -> None:
    require(site_dir.is_dir(), f"Built site directory does not exist: {site_dir}")
    expected_files = [
        "index.html",
        "tools/mission-lookup/index.html",
        "tools/resource-comparison/index.html",
        "tools/fleet-planner/index.html",
        "tools/query-catalogue/index.html",
        "reference/official-mission-catalogue/index.html",
        "reference/mission-verification-status/index.html",
        "reference/generated-faq/index.html",
        "api/index.html",
        "quality-assurance/index.html",
        f"releases/v{release_version}/index.html",
        "javascripts/official-catalogue-loader.js",
        "javascripts/intelligence-tools.js",
        "javascripts/official-mission-details.js",
        "assets/data/official/uk-missions.json",
        "assets/data/official/uk-mission-coverage.json",
        "assets/data/official/uk-mission-verification.json",
        "assets/data/v1/manifest.json",
        "assets/data/v1/missions.json",
        "assets/data/v1/vehicles.json",
        "assets/data/v1/infrastructure.json",
        "assets/data/v1/training.json",
        "assets/data/v1/search-index.json",
        "assets/data/v1/faq.json",
        "assets/data/v1/openapi.json",
    ]
    expected_files.extend(
        f"reference/{path.stem}/index.html"
        for path in sorted((ROOT / "docs" / "reference").glob("fully-canonical-mission-batch-*.md"))
    )
    for relative in expected_files:
        require((site_dir / relative).is_file(), f"Built site is missing release-critical output: {relative}")

    built_manifest = read_json(site_dir / "assets" / "data" / "v1" / "manifest.json")
    source_manifest = read_json(OUTPUT_ROOT / "manifest.json")
    require(built_manifest == source_manifest, "Built-site manifest differs from the generated source manifest")

    for filename in ("uk-missions.json", "uk-mission-coverage.json", "uk-mission-verification.json"):
        built = read_json(site_dir / "assets" / "data" / "official" / filename)
        source = read_json(OFFICIAL_OUTPUT_ROOT / filename)
        require(built == source, f"Built official catalogue asset differs from source: {filename}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit MissionChief UK v1 release readiness")
    parser.add_argument("--site-dir", type=Path, help="Also validate a completed MkDocs output directory")
    args = parser.parse_args()

    try:
        release = release_metadata()
        audit_quality_assets(release["version"])
        counts = audit_exports(release)
        audit_navigation(release["version"])
        if args.site_dir is not None:
            audit_built_site(args.site_dir.resolve(), release["version"])
    except (AuditFailure, OSError, yaml.YAMLError) as exc:
        print(f"Release-readiness audit failed: {exc}")
        return 1

    summary = ", ".join(f"{name}={count}" for name, count in counts.items())
    site_note = f"; built site={args.site_dir}" if args.site_dir is not None else ""
    print(f"Release-readiness audit passed: version={release['version']}, {summary}{site_note}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
