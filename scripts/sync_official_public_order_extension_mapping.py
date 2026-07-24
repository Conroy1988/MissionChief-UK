#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
MAPPING_PATH = ROOT / "data" / "uk" / "official-key-mappings.json"

MAPPING = {
    "status": "verified",
    "canonical_target": "preconditions",
    "canonical_id": "police_public_order_extensions",
    "checked_at": "2026-07-23",
    "sources": [
        "https://www.missionchief.co.uk/einsaetze/198",
        "https://www.missionchief.co.uk/einsaetze/510",
        "https://www.missionchief.co.uk/einsaetze/511",
        "https://www.missionchief.co.uk/einsaetze/512",
        "https://www.missionchief.co.uk/einsaetze.json",
    ],
    "notes": "The official riot_police value is displayed as the minimum Police & Public Order Extension count required to generate the mission.",
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
    prerequisites = document.get("prerequisites")
    if not isinstance(prerequisites, dict):
        raise ValueError("Official key mapping registry prerequisites must be an object")
    output = dict(document)
    output_prerequisites = dict(prerequisites)
    output_prerequisites["riot_police"] = MAPPING
    output["prerequisites"] = output_prerequisites
    return output


def main() -> int:
    parser = argparse.ArgumentParser(description="Synchronize the Police & Public Order Extension prerequisite mapping")
    parser.add_argument("--check", action="store_true", help="Fail instead of writing when the registry differs")
    args = parser.parse_args()

    try:
        output = synchronized_document()
        content = json.dumps(output, ensure_ascii=False, indent=2) + "\n"
        current = MAPPING_PATH.read_text(encoding="utf-8")
    except (OSError, ValueError) as exc:
        print(f"Public Order Extension mapping synchronization failed: {exc}", file=sys.stderr)
        return 1

    changed = current != content
    if args.check and changed:
        print("Public Order Extension mapping synchronization check failed: registry is stale", file=sys.stderr)
        return 1
    if changed and not args.check:
        MAPPING_PATH.write_text(content, encoding="utf-8")
    print(
        "Public Order Extension mapping "
        + ("checked" if args.check else "synchronized")
        + f": {'change required' if changed else 'already current'}."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
