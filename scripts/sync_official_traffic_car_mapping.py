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
    "canonical_target": "requirements.contextual",
    "canonical_id": "traffic_car",
    "condition_path": "additional.need_traffic_car_only_if_present",
    "condition_value": True,
    "condition": "only_when_available",
    "chance_key": "traffic_car",
    "checked_at": "2026-07-23",
    "sources": [
        "https://www.missionchief.co.uk/einsaetze/29",
        "https://www.missionchief.co.uk/einsaetze/587",
        "https://www.missionchief.co.uk/einsaetze/588",
        "https://www.missionchief.co.uk/einsaetze/590",
        "https://www.missionchief.co.uk/einsaetze/776",
        "https://www.missionchief.co.uk/einsaetze.json",
    ],
    "notes": "Traffic Car quantities are contextual. When need_traffic_car_only_if_present is true, the resource is conditional on availability. Otherwise the quantity is guaranteed, or probabilistic when a same-key chance is published.",
}

CHANCE_MAPPING = {
    "status": "verified",
    "canonical_target": "requirements.contextual-probability",
    "canonical_id": "traffic_car",
    "requirement_key": "traffic_car",
    "checked_at": "2026-07-23",
    "sources": [
        "https://www.missionchief.co.uk/einsaetze/29",
        "https://www.missionchief.co.uk/einsaetze/588",
        "https://www.missionchief.co.uk/einsaetze.json",
    ],
    "notes": "The integer percentage controls whether the Traffic Car quantity is required. The separate availability flag determines whether the resulting requirement remains conditional.",
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
        raise ValueError("Official key mapping requirement and chance groups must be objects")

    output = dict(document)
    output_requirements = dict(requirements)
    output_chances = dict(chances)
    output_requirements["traffic_car"] = REQUIREMENT_MAPPING
    output_chances["traffic_car"] = CHANCE_MAPPING
    output["requirements"] = output_requirements
    output["chances"] = output_chances
    return output


def main() -> int:
    parser = argparse.ArgumentParser(description="Synchronize the contextual Traffic Car mapping contract")
    parser.add_argument("--check", action="store_true", help="Fail instead of writing when the registry differs")
    args = parser.parse_args()

    try:
        output = synchronized_document()
        content = json.dumps(output, ensure_ascii=False, indent=2) + "\n"
        current = MAPPING_PATH.read_text(encoding="utf-8")
    except (OSError, ValueError) as exc:
        print(f"Contextual Traffic Car mapping synchronization failed: {exc}", file=sys.stderr)
        return 1

    changed = current != content
    if args.check and changed:
        print("Contextual Traffic Car mapping synchronization check failed: registry is stale", file=sys.stderr)
        return 1
    if changed and not args.check:
        MAPPING_PATH.write_text(content, encoding="utf-8")
    print(
        "Contextual Traffic Car mapping "
        + ("checked" if args.check else "synchronized")
        + f": {'change required' if changed else 'already current'}."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
