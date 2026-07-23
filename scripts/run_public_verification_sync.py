#!/usr/bin/env python3

from __future__ import annotations

import re
import sys
from pathlib import Path

import sync_public_verification_metrics as sync

ROOT = Path(__file__).resolve().parents[1]
README_PATH = ROOT / "README.md"
RELEASE_PATH = ROOT / "docs" / "releases" / "v1.1.0.md"


class RunnerFailure(RuntimeError):
    pass


def replace_once(text: str, pattern: str, replacement: str, label: str, *, flags: int = 0) -> str:
    updated, count = re.subn(pattern, replacement, text, count=1, flags=flags)
    if count != 1:
        raise RunnerFailure(f"Expected exactly one {label} pattern; found {count}")
    return updated


def normalise_templates(readme: str, release: str) -> tuple[str, str]:
    readme = replace_once(
        readme,
        r"Batches 4–\d+ extend the verified vehicle-key contract.*?strict-equivalence validation\.",
        "Batch 4 adds strict chance-aware interpretation; strict-equivalence validation.",
        "README generated batch summary",
        flags=re.DOTALL,
    )
    release = replace_once(
        release,
        r"All [\d,]+ promoted missions pass exact official identity.*?(?=\n\n## Accuracy controls)",
        "The first 49 records use explicitly mapped official fields.",
        "release generated verification narrative",
        flags=re.DOTALL,
    )
    return readme, release


def main() -> int:
    originals = {
        README_PATH: README_PATH.read_text(encoding="utf-8"),
        RELEASE_PATH: RELEASE_PATH.read_text(encoding="utf-8"),
    }
    try:
        readme, release = normalise_templates(originals[README_PATH], originals[RELEASE_PATH])
        README_PATH.write_text(readme, encoding="utf-8")
        RELEASE_PATH.write_text(release, encoding="utf-8")
        result = sync.main()
        if result != 0:
            raise RunnerFailure("Core synchronization returned a failure status")
    except (OSError, RunnerFailure) as exc:
        for path, content in originals.items():
            path.write_text(content, encoding="utf-8")
        print(f"Repeatable public verification synchronization failed: {exc}", file=sys.stderr)
        return 1

    print("Repeatable public verification synchronization passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
