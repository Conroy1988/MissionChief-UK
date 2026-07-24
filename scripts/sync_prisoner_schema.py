#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "data" / "schema" / "mission.schema.json"

EXPECTED = {
    "type": "object",
    "properties": {
        "minimum": {"type": "integer", "minimum": 0},
        "maximum": {"type": "integer", "minimum": 0},
    },
    "additionalProperties": False,
}


def read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"{path.relative_to(ROOT)}: unable to read JSON: {exc}") from exc


def synchronized_document() -> dict[str, Any]:
    document = read_json(SCHEMA_PATH)
    if not isinstance(document, dict):
        raise ValueError("Mission schema must be an object")
    definitions = document.get("$defs")
    if not isinstance(definitions, dict):
        raise ValueError("Mission schema $defs must be an object")
    output = dict(document)
    output_definitions = dict(definitions)
    output_definitions["prisonerInfo"] = EXPECTED
    output["$defs"] = output_definitions
    return output


def main() -> int:
    parser = argparse.ArgumentParser(description="Synchronize the canonical prisoner range schema")
    parser.add_argument("--check", action="store_true", help="Fail instead of writing when the schema differs")
    args = parser.parse_args()

    try:
        output = synchronized_document()
        content = json.dumps(output, ensure_ascii=False, indent=2) + "\n"
        current = SCHEMA_PATH.read_text(encoding="utf-8")
    except (OSError, ValueError) as exc:
        print(f"Prisoner schema synchronization failed: {exc}", file=sys.stderr)
        return 1

    changed = current != content
    if args.check and changed:
        print("Prisoner schema synchronization check failed: schema is stale", file=sys.stderr)
        return 1
    if changed and not args.check:
        SCHEMA_PATH.write_text(content, encoding="utf-8")
    print(
        "Prisoner schema "
        + ("checked" if args.check else "synchronized")
        + f": {'change required' if changed else 'already current'}."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
