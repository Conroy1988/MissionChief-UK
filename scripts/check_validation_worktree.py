#!/usr/bin/env python3

from __future__ import annotations

import argparse
import subprocess
import sys
from collections.abc import Iterable
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# The registry merge is an intentional in-run materialization of the immutable
# base registry plus evidence batches. Downstream validators consume the merged
# document, but the release branch retains the source and batch files separately.
TRANSIENT_TRACKED_OUTPUTS = {
    "data/uk/mission-verification-registry.json",
}

# These generated documents are consumed by validation or built-site checks and
# are intentionally absent from the source branch.
TRANSIENT_UNTRACKED_OUTPUTS = {
    "data/sources/missionchief-uk/mission-verification-status.json",
    "docs/assets/data/official/uk-mission-verification.json",
    "docs/assets/data/v1/faq.json",
    "docs/assets/data/v1/infrastructure.json",
    "docs/assets/data/v1/manifest.json",
    "docs/assets/data/v1/missions.json",
    "docs/assets/data/v1/openapi.json",
    "docs/assets/data/v1/search-index.json",
    "docs/assets/data/v1/training.json",
    "docs/assets/data/v1/vehicles.json",
}


class WorktreeCheckFailure(RuntimeError):
    pass


def git_lines(*args: str) -> set[str]:
    result = subprocess.run(
        ("git", *args),
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        message = result.stderr.strip() or result.stdout.strip() or f"git {' '.join(args)} failed"
        raise WorktreeCheckFailure(message)
    return {line.strip() for line in result.stdout.splitlines() if line.strip()}


def unexpected_changes(
    tracked: Iterable[str],
    untracked: Iterable[str],
    *,
    allow_validation_generated_outputs: bool,
) -> tuple[list[str], list[str]]:
    tracked_paths = set(tracked)
    untracked_paths = set(untracked)
    if allow_validation_generated_outputs:
        tracked_paths -= TRANSIENT_TRACKED_OUTPUTS
        untracked_paths -= TRANSIENT_UNTRACKED_OUTPUTS
    return sorted(tracked_paths), sorted(untracked_paths)


def missing_expected_changes(
    tracked: Iterable[str],
    untracked: Iterable[str],
    *,
    allow_validation_generated_outputs: bool,
) -> tuple[list[str], list[str]]:
    if not allow_validation_generated_outputs:
        return [], []

    return (
        sorted(TRANSIENT_TRACKED_OUTPUTS - set(tracked)),
        sorted(TRANSIENT_UNTRACKED_OUTPUTS - set(untracked)),
    )


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Fail when release-candidate validation leaves unexpected repository changes"
    )
    parser.add_argument(
        "--allow-validation-generated-outputs",
        action="store_true",
        help="Require exactly the explicitly enumerated transient validation outputs",
    )
    args = parser.parse_args()

    try:
        tracked = git_lines("diff", "HEAD", "--name-only", "--diff-filter=ACDMRTUXB", "--", ".")
        untracked = git_lines("ls-files", "--others", "--exclude-standard")
        unexpected_tracked, unexpected_untracked = unexpected_changes(
            tracked,
            untracked,
            allow_validation_generated_outputs=args.allow_validation_generated_outputs,
        )
        missing_tracked, missing_untracked = missing_expected_changes(
            tracked,
            untracked,
            allow_validation_generated_outputs=args.allow_validation_generated_outputs,
        )
    except WorktreeCheckFailure as exc:
        print(f"Validation worktree check failed: {exc}", file=sys.stderr)
        return 1

    if unexpected_tracked or unexpected_untracked or missing_tracked or missing_untracked:
        if unexpected_tracked:
            print("Unexpected tracked changes:", file=sys.stderr)
            for path in unexpected_tracked:
                print(f"  {path}", file=sys.stderr)
        if unexpected_untracked:
            print("Unexpected untracked files:", file=sys.stderr)
            for path in unexpected_untracked:
                print(f"  {path}", file=sys.stderr)
        if missing_tracked:
            print("Missing expected transient tracked outputs:", file=sys.stderr)
            for path in missing_tracked:
                print(f"  {path}", file=sys.stderr)
        if missing_untracked:
            print("Missing expected transient untracked outputs:", file=sys.stderr)
            for path in missing_untracked:
                print(f"  {path}", file=sys.stderr)
        return 1

    allowed_tracked = sorted(tracked & TRANSIENT_TRACKED_OUTPUTS)
    allowed_untracked = sorted(untracked & TRANSIENT_UNTRACKED_OUTPUTS)
    print(
        "Validation worktree check passed: "
        f"{len(allowed_tracked)} transient tracked and "
        f"{len(allowed_untracked)} transient untracked outputs allowed."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
