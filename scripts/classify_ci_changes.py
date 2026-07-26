#!/usr/bin/env python3
"""Classify repository changes into the smallest safe GitHub Actions lanes."""

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path
from typing import Iterable


DOC_FILES = {"README.md", "CHANGELOG.md", "mkdocs.yml", "LICENSE"}
DOC_PREFIXES = ("docs/", "assets/readme/")
INTERFACE_FILES = {"package.json", "package-lock.json", "playwright.config.mjs"}
INTERFACE_PREFIXES = (
    "docs/javascripts/",
    "docs/stylesheets/",
    "tests/e2e/",
)
WORKFLOW_PREFIXES = (".github/workflows/", ".github/actions/")
RELEASE_FILES = {
    "data/version.json",
    "CHANGELOG.md",
    "requirements.txt",
    "package.json",
    "package-lock.json",
    "scripts/release_readiness.py",
}
RELEASE_PREFIXES = ("docs/releases/",)
DATA_PREFIXES = (
    "data/",
    "scripts/",
    "tests/python/",
    "docs/assets/data/",
)
DATA_FILES = {
    "requirements.txt",
    "CATALOGUE_DRIFT.md",
}
VEHICLE_PREFIXES = (
    "data/uk/vehicles/",
    "data/schema/vehicle",
    "data/sources/missionchief-uk/vehicle-",
    "docs/assets/data/official/uk-vehicle-",
    "docs/reference/vehicle-",
)
VEHICLE_FILES = {
    "data/uk/vehicle-field-resolution.json",
    "scripts/vehicle_inventory.py",
    "scripts/generate_vehicle_coverage.py",
    "scripts/generate_vehicle_field_resolution.py",
    "scripts/validate_vehicle_inventory.py",
    "tests/python/test_vehicle_inventory.py",
    "tests/python/test_vehicle_field_resolution.py",
    ".github/workflows/vehicle-inventory-validation.yml",
}
KNOWN_ROOT_FILES = DOC_FILES | INTERFACE_FILES | RELEASE_FILES | DATA_FILES | {
    "playwright.config.mjs",
    "mkdocs.yml",
}


def _matches(path: str, files: set[str], prefixes: tuple[str, ...]) -> bool:
    return path in files or path.startswith(prefixes)


def is_docs(path: str) -> bool:
    return _matches(path, DOC_FILES, DOC_PREFIXES)


def is_interface(path: str) -> bool:
    return _matches(path, INTERFACE_FILES, INTERFACE_PREFIXES)


def is_workflow(path: str) -> bool:
    return path.startswith(WORKFLOW_PREFIXES)


def is_release(path: str) -> bool:
    if _matches(path, RELEASE_FILES, RELEASE_PREFIXES):
        return True
    return path in {
        ".github/workflows/release-v1.yml",
        ".github/workflows/deploy-pages.yml",
        ".github/workflows/production-pages-verification.yml",
    }


def is_data(path: str) -> bool:
    return _matches(path, DATA_FILES, DATA_PREFIXES)


def is_vehicle(path: str) -> bool:
    return _matches(path, VEHICLE_FILES, VEHICLE_PREFIXES)


def is_known(path: str) -> bool:
    if path in KNOWN_ROOT_FILES:
        return True
    return any(
        predicate(path)
        for predicate in (is_docs, is_interface, is_workflow, is_release, is_data, is_vehicle)
    ) or path.startswith((".github/", "tests/", "assets/"))


def classify(paths: Iterable[str]) -> dict[str, bool | int | list[str]]:
    changed = sorted({path.strip().replace("\\", "/") for path in paths if path.strip()})
    docs = any(is_docs(path) for path in changed)
    interface = any(is_interface(path) for path in changed)
    workflow = any(is_workflow(path) for path in changed)
    release = any(is_release(path) for path in changed)
    data = any(is_data(path) for path in changed)
    vehicle = any(is_vehicle(path) for path in changed)
    unknown = any(not is_known(path) for path in changed)
    vehicle_only = bool(changed) and vehicle and all(is_vehicle(path) for path in changed)
    guide_only = bool(changed) and docs and not any(
        (interface, workflow, release, data, vehicle, unknown)
    )
    full_required = workflow or release or unknown
    return {
        "changed_count": len(changed),
        "docs": docs,
        "interface": interface,
        "workflow": workflow,
        "release": release,
        "data": data,
        "vehicle": vehicle,
        "unknown": unknown,
        "vehicle_only": vehicle_only,
        "guide_only": guide_only,
        "full_required": full_required,
        "paths": changed,
    }


def git_changed_paths(base: str, head: str) -> list[str]:
    command = ["git", "diff", "--name-only", "--diff-filter=ACMRTUXB", base, head, "--"]
    result = subprocess.run(command, check=True, text=True, capture_output=True)
    return result.stdout.splitlines()


def write_github_output(path: Path, result: dict[str, bool | int | list[str]]) -> None:
    with path.open("a", encoding="utf-8", newline="\n") as handle:
        for key, value in result.items():
            if key == "paths":
                continue
            if isinstance(value, bool):
                rendered = str(value).lower()
            else:
                rendered = str(value)
            handle.write(f"{key}={rendered}\n")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base", help="Git base ref or SHA")
    parser.add_argument("--head", help="Git head ref or SHA")
    parser.add_argument("--paths-file", type=Path, help="Read changed paths from a text file")
    parser.add_argument("--github-output", type=Path, help="Append scalar outputs for GitHub Actions")
    args = parser.parse_args()

    if args.paths_file is not None:
        paths = args.paths_file.read_text(encoding="utf-8").splitlines()
    elif args.base and args.head:
        paths = git_changed_paths(args.base, args.head)
    else:
        parser.error("provide --paths-file or both --base and --head")

    result = classify(paths)
    print(json.dumps(result, indent=2, sort_keys=True))
    if args.github_output is not None:
        write_github_output(args.github_output, result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
