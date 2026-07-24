#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from prisoner_contract import ROOT, build_expected_prisoners, load_mapping_registry, read_json

OFFICIAL_PATH = ROOT / "data" / "sources" / "missionchief-uk" / "einsaetze.raw.json"
CANONICAL_ROOT = ROOT / "data" / "uk" / "missions"


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


def synchronize(check_only: bool) -> tuple[int, list[str]]:
    envelope = read_json(OFFICIAL_PATH)
    if not isinstance(envelope, dict):
        raise ValueError("Official UK mission source envelope must be an object")
    official_by_id = records_by_id(envelope.get("records"))
    mappings = load_mapping_registry()

    direct_records = 0
    changed: list[str] = []
    for path in sorted(CANONICAL_ROOT.glob("*.json")):
        record = read_json(path)
        if not isinstance(record, dict) or record.get("id") is None:
            raise ValueError(f"{path.relative_to(ROOT)} is not a valid canonical mission record")
        official = official_by_id.get(str(record["id"]))
        if official is None:
            continue
        direct_records += 1
        expected = build_expected_prisoners(official, mappings)
        output = dict(record)
        if expected:
            output["prisoners"] = expected
        else:
            output.pop("prisoners", None)
        content = json.dumps(output, ensure_ascii=False, indent=2) + "\n"
        if path.read_text(encoding="utf-8") == content:
            continue
        changed.append(path.relative_to(ROOT).as_posix())
        if not check_only:
            path.write_text(content, encoding="utf-8")
    return direct_records, changed


def main() -> int:
    parser = argparse.ArgumentParser(description="Synchronize canonical prisoner ranges from the retained official UK source")
    parser.add_argument("--check", action="store_true", help="Fail instead of writing when prisoner fields differ")
    args = parser.parse_args()

    try:
        direct_records, changed = synchronize(args.check)
    except ValueError as exc:
        print(f"Canonical prisoner synchronization failed: {exc}", file=sys.stderr)
        return 1

    if args.check and changed:
        print("Canonical prisoner synchronization check failed; stale files:", file=sys.stderr)
        for path in changed:
            print(f"- {path}", file=sys.stderr)
        return 1

    action = "checked" if args.check else "synchronized"
    print(
        f"Canonical prisoner fields {action}: {direct_records} direct canonical records, "
        f"{len(changed)} file(s) {'would change' if args.check else 'changed'}."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
