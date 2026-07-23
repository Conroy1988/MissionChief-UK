#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
MAPPING_PATH = ROOT / "data" / "uk" / "official-key-mappings.json"

AMBULANCE_MAPPING = {
    "status": "verified",
    "canonical_target": "requirements.guaranteed",
    "canonical_id": "ambulance",
    "checked_at": "2026-07-23",
    "sources": [
        "https://www.missionchief.co.uk/einsaetze/234",
        "https://www.missionchief.co.uk/einsaetze/527",
        "https://www.missionchief.co.uk/einsaetze/691",
        "https://www.missionchief.co.uk/einsaetze.json",
    ],
    "notes": "The official ambulances count is the guaranteed number of frontline Ambulance vehicles.",
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
    if not isinstance(requirements, dict):
        raise ValueError("Official key mapping registry requirements must be an object")
    output = dict(document)
    output_requirements = dict(requirements)
    output_requirements["ambulances"] = AMBULANCE_MAPPING
    output["requirements"] = output_requirements
    return output


def main() -> int:
    parser = argparse.ArgumentParser(description="Synchronize the verified frontline Ambulance key mapping")
    parser.add_argument("--check", action="store_true", help="Fail instead of writing when the registry differs")
    args = parser.parse_args()

    try:
        output = synchronized_document()
        content = json.dumps(output, ensure_ascii=False, indent=2) + "\n"
        current = MAPPING_PATH.read_text(encoding="utf-8")
    except (OSError, ValueError) as exc:
        print(f"Official Ambulance key mapping synchronization failed: {exc}", file=sys.stderr)
        return 1

    changed = current != content
    if args.check and changed:
        print("Official Ambulance key mapping synchronization check failed: registry is stale", file=sys.stderr)
        return 1
    if changed and not args.check:
        MAPPING_PATH.write_text(content, encoding="utf-8")
    print(
        "Official Ambulance key mapping "
        + ("checked" if args.check else "synchronized")
        + f": {'change required' if changed else 'already current'}."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
