#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
MAPPING_PATH = ROOT / "data" / "uk" / "official-key-mappings.json"

REQUIREMENT_MAPPING = {
    "status": "verified",
    "canonical_target": "requirements.guaranteed",
    "canonical_id": "coastguard_rescue_vehicle",
    "checked_at": "2026-07-23",
    "sources": [
        "https://www.missionchief.co.uk/einsaetze/543",
        "https://www.missionchief.co.uk/einsaetze/545",
        "https://www.missionchief.co.uk/einsaetze/569",
        "https://www.missionchief.co.uk/einsaetze.json"
    ],
    "notes": "The official coastal_rescue count is displayed as the required Coastguard Rescue Vehicle quantity."
}

PREREQUISITE_MAPPING = {
    "status": "verified",
    "canonical_target": "preconditions",
    "canonical_id": "coastguard_rescue_stations",
    "checked_at": "2026-07-23",
    "sources": [
        "https://www.missionchief.co.uk/einsaetze/543",
        "https://www.missionchief.co.uk/einsaetze/545",
        "https://www.missionchief.co.uk/einsaetze/569",
        "https://www.missionchief.co.uk/einsaetze.json"
    ],
    "notes": "The official water_rescue_2 prerequisite is the countable Coastguard Rescue Station mission-generation requirement."
}


def read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"{path.relative_to(ROOT)}: unable to read JSON: {exc}") from exc


def synchronized_document() -> dict[str, Any]:
    document = read_json(MAPPING_PATH)
    if not isinstance(document, dict):
        raise ValueError("Official key mapping registry must be an object")
    requirements = document.get("requirements")
    prerequisites = document.get("prerequisites")
    if not isinstance(requirements, dict) or not isinstance(prerequisites, dict):
        raise ValueError("Official key mapping registry requirements and prerequisites must be objects")
    output = dict(document)
    output_requirements = dict(requirements)
    output_prerequisites = dict(prerequisites)
    output_requirements["coastal_rescue"] = REQUIREMENT_MAPPING
    output_prerequisites["water_rescue_2"] = PREREQUISITE_MAPPING
    output["requirements"] = output_requirements
    output["prerequisites"] = output_prerequisites
    return output


def main() -> int:
    parser = argparse.ArgumentParser(description="Synchronize verified core Coastguard response mappings")
    parser.add_argument("--check", action="store_true", help="Fail instead of writing when the registry differs")
    args = parser.parse_args()

    try:
        output = synchronized_document()
        content = json.dumps(output, ensure_ascii=False, indent=2) + "\n"
        current = MAPPING_PATH.read_text(encoding="utf-8")
    except (OSError, ValueError) as exc:
        print(f"Core Coastguard mapping synchronization failed: {exc}", file=sys.stderr)
        return 1

    changed = current != content
    if args.check and changed:
        print("Core Coastguard mapping synchronization check failed: registry is stale", file=sys.stderr)
        return 1
    if changed and not args.check:
        MAPPING_PATH.write_text(content, encoding="utf-8")
    print(
        "Core Coastguard mappings "
        + ("checked" if args.check else "synchronized")
        + f": {'change required' if changed else 'already current'}."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
