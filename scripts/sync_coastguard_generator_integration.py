#!/usr/bin/env python3

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXPECTED_FAMILIES = {
    "firehouse_missions",
    "police_station_missions",
    "ambulance_station_missions",
    "tow_trucks_missions",
    "coastal_rescue_missions",
    "mountain_missions",
    "bomb_disposal_missions",
}


def main() -> int:
    try:
        sys.path.insert(0, str(ROOT / "scripts"))
        from operational_metadata_contract import GENERATOR_METADATA

        if set(GENERATOR_METADATA) != EXPECTED_FAMILIES:
            raise ValueError(
                "operational generator contract differs: "
                f"expected={sorted(EXPECTED_FAMILIES)}, actual={sorted(GENERATOR_METADATA)}"
            )
        required_imports = {
            ROOT / "scripts" / "report_canonical_candidates.py": "GENERATOR_METADATA",
            ROOT / "scripts" / "generate_ready_canonical_batch.py": "GENERATOR_METADATA",
            ROOT / "scripts" / "report_key_mapping_backlog.py": "GENERATOR_METADATA",
        }
        for path, sentinel in required_imports.items():
            text = path.read_text(encoding="utf-8")
            if sentinel not in text:
                raise ValueError(
                    f"{path.relative_to(ROOT)}: shared operational generator integration is missing"
                )
    except (OSError, ValueError) as exc:
        print(f"Coastguard generator integration failed: {exc}", file=sys.stderr)
        return 1

    print(
        "Coastguard generator integration synchronized: shared seven-family operational contract is current."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
