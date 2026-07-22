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
VERSION_PATH = ROOT / "data" / "version.json"
MKDOCS_PATH = ROOT / "mkdocs.yml"
README_PATH = ROOT / "README.md"

COLLECTIONS = {
    "missions": DATA_ROOT / "missions",
    "vehicles": DATA_ROOT / "vehicles",
    "infrastructure": DATA_ROOT / "infrastructure",
    "training": DATA_ROOT / "training",
}

EXPECTED_TOOL_PAGES = (
    "tools/mission-lookup.md",
    "tools/resource-comparison.md",
    "tools/fleet-planner.md",
    "tools/query-catalogue.md",
    "reference/generated-faq.md",
    "api/index.md",
    "quality-assurance.md",
    "releases/v1.0.0.md",
)

REQUIRED_QA_FILES = (
    "package.json",
    "playwright.config.js",
    "tests/e2e/site.spec.js",
    "scripts/audit_links.py",
    "docs/quality-assurance.md",
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


def flatten_nav(value: Any) -> Iterable[str]:
    if isinstance(value, str):
        yield value
    elif isinstance(value, list):
        for item in value:
            yield from flatten_nav(item)
    elif isinstance(value, dict):
        for item in value.values():
            yield from flatten_nav(item)


def audit_navigation() -> None:
    config = yaml.safe_load(MKDOCS_PATH.read_text(encoding="utf-8"))
    require(isinstance(config, dict), "mkdocs.yml must contain a mapping")
    nav = config.get("nav")
    require(isinstance(nav, list), "mkdocs.yml must define a navigation list")

    nav_targets = set(flatten_nav(nav))
    for target in nav_targets:
        require((ROOT / "docs" / target).is_file(), f"MkDocs navigation target does not exist: docs/{target}")
    for target in EXPECTED_TOOL_PAGES:
        require(target in nav_targets, f"Release-critical page is not present in MkDocs navigation: {target}")

    javascript = config.get("extra_javascript", [])
    require(
        isinstance(javascript, list) and "javascripts/intelligence-tools.js" in javascript,
        "MkDocs must load javascripts/intelligence-tools.js",
    )


def audit_quality_assets() -> None:
    for relative in REQUIRED_QA_FILES:
        require((ROOT / relative).is_file(), f"Release-critical QA file is missing: {relative}")

    package = read_json(ROOT / "package.json")
    require(isinstance(package, dict), "package.json must contain an object")
    scripts = package.get("scripts")
    require(isinstance(scripts, dict) and scripts.get("test:e2e") == "playwright test",
            "package.json must expose the Playwright test:e2e command")
    dependencies = package.get("devDependencies")
    require(isinstance(dependencies, dict), "package.json must define devDependencies")
    for dependency in ("@playwright/test", "@axe-core/playwright"):
        require(dependency in dependencies, f"package.json is missing QA dependency: {dependency}")

    config_text = (ROOT / "playwright.config.js").read_text(encoding="utf-8")
    for project in PLAYWRIGHT_PROJECTS:
        require(project in config_text, f"Playwright configuration is missing project: {project}")

    suite_text = (ROOT / "tests" / "e2e" / "site.spec.js").read_text(encoding="utf-8")
    for marker in ("mission-lookup", "comparison", "fleet-planner", "query-catalogue", "AxeBuilder"):
        require(marker in suite_text, f"Browser acceptance suite is missing coverage marker: {marker}")


def audit_exports() -> dict[str, int]:
    version = read_json(VERSION_PATH)
    require(isinstance(version, dict), "data/version.json must contain an object")
    release_version = version.get("version")
    require(
        isinstance(release_version, str) and re.fullmatch(r"\d+\.\d+\.\d+", release_version) is not None,
        "data/version.json must contain a semantic version",
    )
    require(version.get("stage") == 34, "The v1 release must identify Stage 34")
    require(version.get("status") == "production", "The v1 release status must be production")

    manifest = read_json(OUTPUT_ROOT / "manifest.json")
    require(manifest.get("api_version") == "v1", "Manifest api_version must be v1")
    require(manifest.get("data_version") == release_version, "Manifest data_version does not match data/version.json")
    require(manifest.get("released_at") == version.get("released_at"), "Manifest release date does not match data/version.json")
    require(manifest.get("stage") == version.get("stage"), "Manifest stage does not match data/version.json")
    require(manifest.get("status") == version.get("status"), "Manifest status does not match data/version.json")

    manifest_collections = manifest.get("collections")
    require(isinstance(manifest_collections, dict), "Manifest collections must be an object")

    counts: dict[str, int] = {}
    search_keys: set[tuple[str, str]] = set()
    for name, directory in COLLECTIONS.items():
        source_records = load_source_collection(directory)
        payload = read_json(OUTPUT_ROOT / f"{name}.json")
        require(payload.get("schema_version") == "1", f"{name}.json schema_version must be 1")
        require(payload.get("data_version") == release_version, f"{name}.json data_version mismatch")
        require(payload.get("released_at") == version.get("released_at"), f"{name}.json release date mismatch")
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

    readme = README_PATH.read_text(encoding="utf-8")
    readme_lower = readme.lower()
    readme_words = re.sub(r"[^a-z0-9]+", " ", readme_lower)
    for name, count in counts.items():
        require(str(count) in readme, f"README does not expose the current {name} count ({count})")
    require("stage_34_complete" in readme_lower or "stage 34 complete" in readme_words,
            "README stage badge is not synchronized to Stage 34")
    require(release_version in readme_lower and "static api" in readme_words,
            f"README does not identify Static API v{release_version}")

    return counts


def audit_built_site(site_dir: Path) -> None:
    require(site_dir.is_dir(), f"Built site directory does not exist: {site_dir}")
    expected_files = (
        "index.html",
        "tools/mission-lookup/index.html",
        "tools/resource-comparison/index.html",
        "tools/fleet-planner/index.html",
        "tools/query-catalogue/index.html",
        "reference/generated-faq/index.html",
        "api/index.html",
        "quality-assurance/index.html",
        "releases/v1.0.0/index.html",
        "javascripts/intelligence-tools.js",
        "assets/data/v1/manifest.json",
        "assets/data/v1/missions.json",
        "assets/data/v1/vehicles.json",
        "assets/data/v1/infrastructure.json",
        "assets/data/v1/training.json",
        "assets/data/v1/search-index.json",
        "assets/data/v1/faq.json",
        "assets/data/v1/openapi.json",
    )
    for relative in expected_files:
        require((site_dir / relative).is_file(), f"Built site is missing release-critical output: {relative}")

    built_manifest = read_json(site_dir / "assets" / "data" / "v1" / "manifest.json")
    source_manifest = read_json(OUTPUT_ROOT / "manifest.json")
    require(built_manifest == source_manifest, "Built-site manifest differs from the generated source manifest")


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit MissionChief UK v1 release readiness")
    parser.add_argument("--site-dir", type=Path, help="Also validate a completed MkDocs output directory")
    args = parser.parse_args()

    try:
        audit_quality_assets()
        counts = audit_exports()
        audit_navigation()
        if args.site_dir is not None:
            audit_built_site(args.site_dir.resolve())
    except (AuditFailure, OSError, yaml.YAMLError) as exc:
        print(f"Release-readiness audit failed: {exc}")
        return 1

    summary = ", ".join(f"{name}={count}" for name, count in counts.items())
    site_note = f"; built site={args.site_dir}" if args.site_dir is not None else ""
    print(f"Release-readiness audit passed: {summary}{site_note}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
