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
    "kdow_orgl": {
        "status": "verified",
        "canonical_target": "personnel.chance-aware",
        "canonical_role": "Operational Team Leader",
        "chance_key": "kdow_orgl",
        "checked_at": "2026-07-23",
        "sources": [
            "https://www.missionchief.co.uk/einsaetze/143",
            "https://www.missionchief.co.uk/einsaetze/149",
            "https://www.missionchief.co.uk/einsaetze/587",
            "https://www.missionchief.co.uk/einsaetze.json",
        ],
        "notes": "The official kdow_orgl quantity is displayed as required Operational Team Leaders. A same-key chance field converts the quantity to probabilistic personnel.",
    },
    "midwife": {
        "status": "verified",
        "canonical_target": "personnel.chance-aware",
        "canonical_role": "Community Midwife",
        "chance_key": "midwife",
        "checked_at": "2026-07-23",
        "sources": [
            "https://www.missionchief.co.uk/einsaetze/690",
            "https://www.missionchief.co.uk/einsaetze/691",
            "https://www.missionchief.co.uk/einsaetze/692",
            "https://www.missionchief.co.uk/einsaetze.json",
        ],
        "notes": "The official midwife quantity is displayed as required Community Midwives. The verified records publish no chance field, so the quantity is guaranteed.",
    },
}

CHANCE_MAPPINGS = {
    "kdow_orgl": {
        "status": "verified",
        "canonical_target": "personnel.probabilistic",
        "canonical_role": "Operational Team Leader",
        "requirement_key": "kdow_orgl",
        "checked_at": "2026-07-23",
        "sources": [
            "https://www.missionchief.co.uk/einsaetze/143",
            "https://www.missionchief.co.uk/einsaetze/189",
            "https://www.missionchief.co.uk/einsaetze.json",
        ],
        "notes": "The integer percentage is the probability that the published Operational Team Leader quantity is required.",
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
    chances = document.get("chances")
    if not isinstance(requirements, dict) or not isinstance(chances, dict):
        raise ValueError("Official key mapping registry requirements and chances must be objects")
    output = dict(document)
    output_requirements = dict(requirements)
    output_chances = dict(chances)
    output_requirements.update(REQUIREMENT_MAPPINGS)
    output_chances.update(CHANCE_MAPPINGS)
    output["requirements"] = output_requirements
    output["chances"] = output_chances
    return output


def main() -> int:
    parser = argparse.ArgumentParser(description="Synchronize verified personnel-owned entries into the official key registry")
    parser.add_argument("--check", action="store_true", help="Fail instead of writing when the registry differs")
    args = parser.parse_args()

    try:
        output = synchronized_document()
        content = json.dumps(output, ensure_ascii=False, indent=2) + "\n"
        current = MAPPING_PATH.read_text(encoding="utf-8")
    except (OSError, ValueError) as exc:
        print(f"Official personnel key mapping synchronization failed: {exc}", file=sys.stderr)
        return 1

    changed = current != content
    if args.check and changed:
        print("Official personnel key mapping synchronization check failed: registry is stale", file=sys.stderr)
        return 1
    if changed and not args.check:
        MAPPING_PATH.write_text(content, encoding="utf-8")
    print(
        "Official personnel key mappings "
        + ("checked" if args.check else "synchronized")
        + f": {'change required' if changed else 'already current'}."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
