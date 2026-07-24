#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
MAPPING_PATH = ROOT / "data" / "uk" / "official-key-mappings.json"

PREREQUISITES = {
    "tow_trucks": {
        "status": "verified",
        "canonical_target": "preconditions",
        "canonical_id": "recovery_centres",
        "checked_at": "2026-07-23",
        "sources": [
            "https://www.missionchief.co.uk/einsaetze/776",
            "https://www.missionchief.co.uk/einsaetze/779",
            "https://www.missionchief.co.uk/einsaetze/784",
            "https://www.missionchief.co.uk/einsaetze.json"
        ],
        "notes": "The official tow_trucks prerequisite is the countable Recovery Centre mission-generation requirement."
    },
    "tow_trucks_large": {
        "status": "verified",
        "canonical_target": "preconditions",
        "canonical_id": "hgv_recovery_extensions",
        "checked_at": "2026-07-23",
        "sources": [
            "https://www.missionchief.co.uk/einsaetze/810",
            "https://police.missionchief.co.uk/einsaetze/13?additive_overlays=a",
            "https://www.missionchief.co.uk/einsaetze.json"
        ],
        "notes": "The official tow_trucks_large prerequisite is the countable HGV Recovery Extension mission-generation requirement."
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
    prerequisites = document.get("prerequisites")
    if not isinstance(prerequisites, dict):
        raise ValueError("Official key mapping registry prerequisites must be an object")
    output = dict(document)
    output_prerequisites = dict(prerequisites)
    output_prerequisites.update(PREREQUISITES)
    output["prerequisites"] = output_prerequisites
    return output


def main() -> int:
    parser = argparse.ArgumentParser(description="Synchronize verified recovery generation prerequisites")
    parser.add_argument("--check", action="store_true", help="Fail instead of writing when the registry differs")
    args = parser.parse_args()

    try:
        output = synchronized_document()
        content = json.dumps(output, ensure_ascii=False, indent=2) + "\n"
        current = MAPPING_PATH.read_text(encoding="utf-8")
    except (OSError, ValueError) as exc:
        print(f"Recovery prerequisite synchronization failed: {exc}", file=sys.stderr)
        return 1

    changed = current != content
    if args.check and changed:
        print("Recovery prerequisite synchronization check failed: registry is stale", file=sys.stderr)
        return 1
    if changed and not args.check:
        MAPPING_PATH.write_text(content, encoding="utf-8")
    print(
        "Recovery prerequisites "
        + ("checked" if args.check else "synchronized")
        + f": {'change required' if changed else 'already current'}."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
