#!/usr/bin/env python3

from __future__ import annotations

import sys
from pathlib import Path

import sync_public_verification_metrics as sync
import sync_verification_batch_navigation as nav_sync

ROOT = Path(__file__).resolve().parents[1]
PUBLICATION_PATHS = (
    sync.README_PATH,
    sync.HOME_PATH,
    sync.API_PATH,
    sync.RELEASE_PATH,
    sync.CHANGELOG_PATH,
    sync.MISSION_LOOKUP_PATH,
    sync.OFFICIAL_CATALOGUE_PATH,
    ROOT / "mkdocs.yml",
)


class RunnerFailure(RuntimeError):
    pass


def main() -> int:
    try:
        originals = {
            path: path.read_text(encoding="utf-8")
            for path in PUBLICATION_PATHS
        }
    except OSError as exc:
        print(f"Repeatable public verification synchronization failed: {exc}", file=sys.stderr)
        return 1

    try:
        if sync.main() != 0:
            raise RunnerFailure("Core synchronization returned a failure status")
        if nav_sync.main() != 0:
            raise RunnerFailure("Batch navigation synchronization returned a failure status")
    except (OSError, RunnerFailure) as exc:
        for path, content in originals.items():
            path.write_text(content, encoding="utf-8")
        print(f"Repeatable public verification synchronization failed: {exc}", file=sys.stderr)
        return 1

    print("Repeatable public verification and navigation synchronization passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
