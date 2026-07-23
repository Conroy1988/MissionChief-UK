#!/usr/bin/env python3

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT_ROOT = ROOT / "scripts"


def mapping_scripts() -> list[Path]:
    scripts = [
        path
        for path in SCRIPT_ROOT.glob("sync_official_*mapping*.py")
        if path.name != Path(__file__).name
    ]
    if not scripts:
        raise ValueError("No official key mapping synchronizers were discovered")
    return sorted(scripts, key=lambda path: path.name)


def main() -> int:
    parser = argparse.ArgumentParser(description="Run every deterministic official key mapping synchronizer")
    parser.add_argument("--check", action="store_true", help="Require every mapping registry fragment to be current")
    args = parser.parse_args()

    try:
        scripts = mapping_scripts()
    except ValueError as exc:
        print(f"Official key mapping synchronization failed: {exc}", file=sys.stderr)
        return 1

    failures: list[str] = []
    for path in scripts:
        command = [sys.executable, str(path)]
        if args.check:
            command.append("--check")
        completed = subprocess.run(command, cwd=ROOT, check=False)
        if completed.returncode != 0:
            failures.append(path.name)

    if failures:
        print(
            "Official key mapping synchronization failed for: " + ", ".join(failures),
            file=sys.stderr,
        )
        return 1
    print(f"Official key mapping synchronization passed: {len(scripts)} synchronizer(s) executed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
