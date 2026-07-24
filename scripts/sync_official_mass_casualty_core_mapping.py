#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
MAPPING_PATH = ROOT / "data" / "uk" / "official-key-mappings.json"

REQUIREMENT_MAPPINGS = {
    "ems_mobile_command": {
        "status": "verified",
        "canonical_target": "requirements.alternatives",
        "canonical_ids": [
            "iccu",
            "ambulance_control_unit",
            "airfield_firefighting_command_vehicle",
        ],
        "checked_at": "2026-07-23",
        "sources": [
            "https://www.missionchief.co.uk/einsaetze/587",
            "https://www.missionchief.co.uk/einsaetze/588",
            "https://www.missionchief.co.uk/einsaetze/590",
            "https://www.missionchief.co.uk/einsaetze.json",
        ],
        "notes": "The official field is displayed as ICCU, Ambulance Control Unit or Airfield Firefighting Command Vehicle. The quantity is a qualifying total across the three canonical command resources.",
    },
    "emergency_welfare": {
        "status": "verified",
        "canonical_target": "requirements.guaranteed",
        "canonical_id": "welfare_vehicle",
        "checked_at": "2026-07-23",
        "sources": [
            "https://www.missionchief.co.uk/einsaetze/587",
            "https://www.missionchief.co.uk/einsaetze/588",
            "https://www.missionchief.co.uk/einsaetze/760",
            "https://www.missionchief.co.uk/einsaetze.json",
        ],
        "notes": "The official emergency_welfare count represents guaranteed Welfare Vehicles.",
    },
    "mass_casualty_equipment": {
        "status": "verified",
        "canonical_target": "requirements.guaranteed",
        "canonical_id": "mass_casualty_equipment",
        "checked_at": "2026-07-23",
        "sources": [
            "https://www.missionchief.co.uk/einsaetze/587",
            "https://www.missionchief.co.uk/einsaetze/588",
            "https://www.missionchief.co.uk/einsaetze.json",
        ],
        "notes": "The official mass_casualty_equipment count represents guaranteed Mass Casualty Equipment units.",
    },
}

PREREQUISITE_MAPPINGS = {
    "mass_casualty_count": {
        "status": "verified",
        "canonical_target": "preconditions",
        "canonical_id": "mass_casualty_extensions",
        "checked_at": "2026-07-23",
        "sources": [
            "https://www.missionchief.co.uk/einsaetze/587",
            "https://www.missionchief.co.uk/einsaetze/588",
            "https://www.missionchief.co.uk/einsaetze.json",
        ],
        "notes": "The official mass_casualty_count value is the minimum Mass Casualty Extension count required to generate the mission.",
    }
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
    output_requirements.update(REQUIREMENT_MAPPINGS)
    output_prerequisites.update(PREREQUISITE_MAPPINGS)
    output["requirements"] = output_requirements
    output["prerequisites"] = output_prerequisites
    return output


def main() -> int:
    parser = argparse.ArgumentParser(description="Synchronize verified Mass Casualty and HART command mappings")
    parser.add_argument("--check", action="store_true", help="Fail instead of writing when the registry differs")
    args = parser.parse_args()

    try:
        output = synchronized_document()
        content = json.dumps(output, ensure_ascii=False, indent=2) + "\n"
        current = MAPPING_PATH.read_text(encoding="utf-8")
    except (OSError, ValueError) as exc:
        print(f"Mass Casualty core mapping synchronization failed: {exc}", file=sys.stderr)
        return 1

    changed = current != content
    if args.check and changed:
        print("Mass Casualty core mapping synchronization check failed: registry is stale", file=sys.stderr)
        return 1
    if changed and not args.check:
        MAPPING_PATH.write_text(content, encoding="utf-8")
    print(
        "Mass Casualty core mappings "
        + ("checked" if args.check else "synchronized")
        + f": {'change required' if changed else 'already current'}."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
