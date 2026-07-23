#!/usr/bin/env python3

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REFERENCE_ROOT = ROOT / "docs" / "reference"
MKDOCS_PATH = ROOT / "mkdocs.yml"
PAGE_PATTERN = re.compile(r"fully-canonical-mission-batch-(\d+)\.md$")
BLOCK_PATTERN = re.compile(
    r"(?P<indent>\s*)- Fully Canonical Batch 1: reference/fully-canonical-mission-batch-1\.md\n"
    r".*?"
    r"(?=\s*- Verified Mission Records: reference/verified-mission-records\.md)",
    re.DOTALL,
)


class NavigationFailure(RuntimeError):
    pass


def discover_pages() -> list[tuple[int, Path]]:
    pages: list[tuple[int, Path]] = []
    for path in REFERENCE_ROOT.glob("fully-canonical-mission-batch-*.md"):
        match = PAGE_PATTERN.fullmatch(path.name)
        if match is not None:
            pages.append((int(match.group(1)), path))
    pages.sort()
    if not pages:
        raise NavigationFailure("No fully canonical batch pages were found")
    numbers = [number for number, _ in pages]
    expected = list(range(1, max(numbers) + 1))
    if numbers != expected:
        raise NavigationFailure(f"Batch evidence pages are not contiguous: {numbers}")
    return pages


def main() -> int:
    try:
        pages = discover_pages()
        original = MKDOCS_PATH.read_text(encoding="utf-8")
        match = BLOCK_PATTERN.search(original)
        if match is None:
            raise NavigationFailure("Fully canonical navigation block was not found")
        indent = match.group("indent")
        rendered = "".join(
            f"{indent}- Fully Canonical Batch {number}: reference/{path.name}\n"
            for number, path in pages
        )
        updated, count = BLOCK_PATTERN.subn(rendered, original, count=1)
        if count != 1:
            raise NavigationFailure(f"Expected one navigation block, replaced {count}")
        if updated != original:
            MKDOCS_PATH.write_text(updated, encoding="utf-8")
    except (OSError, NavigationFailure) as exc:
        print(f"Verification batch navigation synchronization failed: {exc}", file=sys.stderr)
        return 1

    print(f"Verification batch navigation synchronized for {len(pages)} evidence pages.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
