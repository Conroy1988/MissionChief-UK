#!/usr/bin/env python3

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def patch(path: Path, old: str, new: str, sentinel: str) -> bool:
    text = path.read_text(encoding="utf-8")
    if sentinel in text:
        return False
    if old not in text:
        raise ValueError(f"{path.relative_to(ROOT)}: Coastguard generator integration point is missing")
    path.write_text(text.replace(old, new, 1), encoding="utf-8")
    return True


def main() -> int:
    try:
        changed: list[str] = []
        candidate = ROOT / "scripts" / "report_canonical_candidates.py"
        if patch(
            candidate,
            '    "tow_trucks_missions",\n}\n',
            '    "tow_trucks_missions",\n    "coastal_rescue_missions",\n}\n',
            '    "coastal_rescue_missions",\n',
        ):
            changed.append(candidate.relative_to(ROOT).as_posix())

        generator = ROOT / "scripts" / "generate_ready_canonical_batch.py"
        if patch(
            generator,
            '    "tow_trucks_missions": ("recovery", ["Recovery Vehicle Missions"]),\n}\n',
            '    "tow_trucks_missions": ("recovery", ["Recovery Vehicle Missions"]),\n    "coastal_rescue_missions": ("coastguard", ["Coastguard Missions"]),\n}\n',
            '    "coastal_rescue_missions": ("coastguard", ["Coastguard Missions"]),\n',
        ):
            changed.append(generator.relative_to(ROOT).as_posix())

        backlog = ROOT / "scripts" / "report_key_mapping_backlog.py"
        if patch(
            backlog,
            '    "tow_trucks_missions",\n}\n',
            '    "tow_trucks_missions",\n    "coastal_rescue_missions",\n}\n',
            '    "coastal_rescue_missions",\n',
        ):
            changed.append(backlog.relative_to(ROOT).as_posix())
    except (OSError, ValueError) as exc:
        print(f"Coastguard generator integration failed: {exc}", file=sys.stderr)
        return 1

    print(
        "Coastguard generator integration synchronized: "
        + (", ".join(changed) if changed else "already current")
        + "."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
