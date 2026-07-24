#!/usr/bin/env python3

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
COMPACT_FILES = (
    ROOT / "data" / "sources" / "missionchief-uk" / "einsaetze.raw.json",
    ROOT / "docs" / "assets" / "data" / "official" / "uk-missions.json",
)
REDUNDANT_FILES = (
    ROOT / "data" / "sources" / "missionchief-uk" / "official-missions.json",
)


def compact_json(path: Path) -> None:
    value: Any = json.loads(path.read_text(encoding="utf-8"))
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        json.dump(value, handle, ensure_ascii=False, separators=(",", ":"), sort_keys=True)
        handle.write("\n")


def main() -> int:
    for path in COMPACT_FILES:
        if not path.exists():
            raise FileNotFoundError(f"Required generated catalogue file is missing: {path}")
        compact_json(path)
        if path.stat().st_size >= 1_000_000:
            raise ValueError(f"Compacted catalogue file exceeds the repository content limit: {path}")

    for path in REDUNDANT_FILES:
        path.unlink(missing_ok=True)

    print("Compacted official UK mission snapshots and removed redundant normalized duplication")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
