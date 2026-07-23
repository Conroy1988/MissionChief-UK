#!/usr/bin/env python3

from __future__ import annotations

from typing import Any

import generate_ready_canonical_batch as generator
from verification_registry import load_verification_registry


def merged_fully_canonical_count() -> int:
    merged: dict[str, Any] = load_verification_registry(
        generator.ROOT,
        generator.VERIFICATION_REGISTRY_PATH,
        generator.BATCH_ROOT,
    )
    records = merged.get("records")
    if not isinstance(records, dict):
        raise ValueError("Merged mission verification registry records must be an object")
    return sum(
        1
        for decision in records.values()
        if isinstance(decision, dict) and decision.get("stage") == "fully-canonical"
    )


def main() -> int:
    generator.count_fully_canonical = merged_fully_canonical_count
    return generator.main()


if __name__ == "__main__":
    raise SystemExit(main())
