#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from personnel_education_contract import (
    ROOT,
    build_expected_personnel_educations,
    load_mapping_registry,
    merge_personnel_educations,
    owned_paths,
)

OFFICIAL_PATH = ROOT / "data" / "sources" / "missionchief-uk" / "einsaetze.raw.json"
CANONICAL_ROOT = ROOT / "data" / "uk" / "missions"


def read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"{path.relative_to(ROOT)}: unable to read JSON: {exc}") from exc


def write_json(path: Path, document: Any) -> None:
    path.write_text(json.dumps(document, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def official_records() -> dict[str, dict[str, Any]]:
    envelope = read_json(OFFICIAL_PATH)
    records = envelope.get("records") if isinstance(envelope, dict) else None
    if not isinstance(records, list):
        raise ValueError("Official UK mission records must be an array")
    output: dict[str, dict[str, Any]] = {}
    for record in records:
        if not isinstance(record, dict) or record.get("id") is None:
            raise ValueError("Official UK mission source contains an invalid record")
        mission_id = str(record["id"])
        if mission_id in output:
            raise ValueError(f"Official UK mission source repeats id {mission_id}")
        output[mission_id] = record
    return output


def synchronize(check_only: bool) -> tuple[int, int]:
    official_by_id = official_records()
    registry = load_mapping_registry()
    _, _, _, roles = owned_paths(registry)
    direct = 0
    changed = 0

    for path in sorted(CANONICAL_ROOT.glob("*.json")):
        canonical = read_json(path)
        if not isinstance(canonical, dict) or canonical.get("id") is None:
            raise ValueError(f"{path.relative_to(ROOT)}: canonical mission is invalid")
        official = official_by_id.get(str(canonical["id"]))
        if official is None:
            continue
        direct += 1
        expected = build_expected_personnel_educations(official, registry)
        synchronized = merge_personnel_educations(canonical, expected, roles)
        if synchronized == canonical:
            continue
        changed += 1
        if not check_only:
            write_json(path, synchronized)

    return direct, changed


def main() -> int:
    parser = argparse.ArgumentParser(description="Synchronize canonical personnel education fields")
    parser.add_argument("--check", action="store_true", help="Fail instead of writing when canonical records are stale")
    args = parser.parse_args()

    try:
        direct, changed = synchronize(args.check)
    except ValueError as exc:
        print(f"Canonical personnel education synchronization failed: {exc}", file=sys.stderr)
        return 1

    if args.check and changed:
        print(
            f"Canonical personnel education synchronization check failed: {changed} of {direct} direct records are stale",
            file=sys.stderr,
        )
        return 1
    print(
        "Canonical personnel education fields "
        + ("checked" if args.check else "synchronized")
        + f": {direct} direct canonical records, {changed} file(s) changed."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
