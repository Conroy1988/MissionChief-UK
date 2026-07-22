#!/usr/bin/env python3

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_ROOT = ROOT / "data" / "uk"


def main() -> int:
    failures: list[str] = []
    for path in sorted(DATA_ROOT.glob("*.json")):
        try:
            with path.open("r", encoding="utf-8") as handle:
                json.load(handle)
        except (OSError, json.JSONDecodeError) as exc:
            failures.append(f"{path.relative_to(ROOT)}: {exc}")

    if failures:
        print("Structured data validation failed:")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("Structured data files contain valid JSON.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
