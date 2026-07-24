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
    "canonical_target": "requirements.alternatives",
    "canonical_ids": ["hazmat_unit", "cbrn_vehicle"],
    "chance_key": "hazmat_vehicles",
    "checked_at": "2026-07-23",
    "sources": [
        "https://www.missionchief.co.uk/einsaetze/72",
        "https://www.missionchief.co.uk/einsaetze/180",
        "https://www.missionchief.co.uk/einsaetze/300",
        "https://www.missionchief.co.uk/einsaetze/590",
        "https://www.missionchief.co.uk/einsaetze.json",
    ],
    "notes": "The official field is displayed as HazMat Units or CBRN Vehicles. A same-key chance applies to the qualifying alternative group as a whole.",
}

CHANCE_MAPPING = {
    "status": "verified",
    "canonical_target": "requirements.probabilistic-alternatives",
    "canonical_ids": ["hazmat_unit", "cbrn_vehicle"],
    "requirement_key": "hazmat_vehicles",
    "checked_at": "2026-07-23",
    "sources": [
        "https://www.missionchief.co.uk/einsaetze/72",
        "https://www.missionchief.co.uk/einsaetze/479",
        "https://www.missionchief.co.uk/einsaetze/805",
        "https://www.missionchief.co.uk/einsaetze/823",
        "https://www.missionchief.co.uk/einsaetze.json",
    ],
    "notes": "The integer percentage is the probability that the published HazMat Unit or CBRN Vehicle alternative quantity is required.",
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
    output_requirements["hazmat_vehicles"] = REQUIREMENT_MAPPING
    output_chances["hazmat_vehicles"] = CHANCE_MAPPING
    output["requirements"] = output_requirements
    output["chances"] = output_chances
    return output


def main() -> int:
    parser = argparse.ArgumentParser(description="Synchronize probabilistic HazMat Unit or CBRN Vehicle mapping")
    parser.add_argument("--check", action="store_true", help="Fail instead of writing when the registry differs")
    args = parser.parse_args()

    try:
        output = synchronized_document()
        content = json.dumps(output, ensure_ascii=False, indent=2) + "\n"
        current = MAPPING_PATH.read_text(encoding="utf-8")
    except (OSError, ValueError) as exc:
        print(f"Probabilistic HazMat alternative mapping synchronization failed: {exc}", file=sys.stderr)
        return 1

    changed = current != content
    if args.check and changed:
        print("Probabilistic HazMat alternative mapping synchronization check failed: registry is stale", file=sys.stderr)
        return 1
    if changed and not args.check:
        MAPPING_PATH.write_text(content, encoding="utf-8")
    print(
        "Probabilistic HazMat alternative mapping "
        + ("checked" if args.check else "synchronized")
        + f": {'change required' if changed else 'already current'}."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
