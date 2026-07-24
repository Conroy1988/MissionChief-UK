#!/usr/bin/env python3

from __future__ import annotations

import json
import sys
from pathlib import Path

from verification_registry import load_verification_registry

ROOT = Path(__file__).resolve().parents[1]
BASE_PATH = ROOT / "data" / "uk" / "mission-verification-registry.json"
BATCH_ROOT = ROOT / "data" / "uk" / "mission-verification-batches"


def main() -> int:
    try:
        merged = load_verification_registry(ROOT, BASE_PATH, BATCH_ROOT)
        source_files = merged.pop("source_files", [])
        BASE_PATH.write_text(
            json.dumps(merged, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
    except (OSError, ValueError) as exc:
        print(f"Mission verification registry merge failed: {exc}", file=sys.stderr)
        return 1

    print(
        "Mission verification registry merged: "
        f"{len(merged['records'])} decisions from {len(source_files)} source files."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
