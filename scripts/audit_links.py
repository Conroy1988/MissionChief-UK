#!/usr/bin/env python3

from __future__ import annotations

import html
import re
import sys
import unicodedata
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
DOCS_ROOT = ROOT / "docs"
SITE_HOST = "conroy1988.github.io"
SITE_PREFIX = "/MissionChief-UK/"

MARKDOWN_LINK_RE = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
REFERENCE_LINK_RE = re.compile(r"^\s*\[[^\]]+\]:\s*(\S+)", re.MULTILINE)
HTML_LINK_RE = re.compile(r"\b(?:href|src)\s*=\s*[\"']([^\"']+)[\"']", re.IGNORECASE)
HEADING_RE = re.compile(r"^\s{0,3}#{1,6}\s+(.+?)\s*#*\s*$")
EXPLICIT_ID_RE = re.compile(r"\{#([A-Za-z][\w:.-]*)\}\s*$")
FENCE_RE = re.compile(r"^\s*(```+|~~~+)")
INLINE_LINK_TEXT_RE = re.compile(r"\[([^\]]+)\]\([^)]*\)")
HTML_TAG_RE = re.compile(r"<[^>]+>")
MARKDOWN_MARKUP_RE = re.compile(r"[`*_~]")


@dataclass(frozen=True)
class LinkReference:
    source: Path
    line: int
    target: str


def display(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def source_files() -> list[Path]:
    files = [ROOT / "README.md", ROOT / "CHANGELOG.md"]
    files.extend(sorted(DOCS_ROOT.rglob("*.md")))
    return [path for path in files if path.is_file()]


def without_fenced_code(text: str) -> str:
    output: list[str] = []
    fence_marker: str | None = None
    for line in text.splitlines(keepends=True):
        match = FENCE_RE.match(line)
        if match:
            marker = match.group(1)[0]
            fence_marker = None if fence_marker == marker else marker
            output.append("\n")
            continue
        output.append("\n" if fence_marker else line)
    return "".join(output)


def extract_target(raw: str) -> str:
    value = html.unescape(raw.strip())
    if value.startswith("<") and ">" in value:
        return value[1 : value.index(">")].strip()
    return value.split(maxsplit=1)[0].strip()


def references(path: Path) -> list[LinkReference]:
    text = without_fenced_code(path.read_text(encoding="utf-8"))
    found: list[LinkReference] = []
    seen: set[tuple[int, str]] = set()
    for pattern in (MARKDOWN_LINK_RE, REFERENCE_LINK_RE, HTML_LINK_RE):
        for match in pattern.finditer(text):
            target = extract_target(match.group(1))
            if not target:
                continue
            line = text.count("\n", 0, match.start()) + 1
            key = (line, target)
            if key not in seen:
                found.append(LinkReference(path, line, target))
                seen.add(key)
    return found


def normalize_heading(text: str) -> str:
    value = html.unescape(text).lower()
    value = INLINE_LINK_TEXT_RE.sub(r"\1", value)
    value = HTML_TAG_RE.sub("", value)
    value = MARKDOWN_MARKUP_RE.sub("", value)
    value = unicodedata.normalize("NFKD", value)
    return "".join(character for character in value if not unicodedata.combining(character))


def github_slug(text: str) -> str:
    value = normalize_heading(text)
    value = "".join(character for character in value if character.isalnum() or character in " -_")
    return re.sub(r"\s", "-", value)


def mkdocs_slug(text: str) -> str:
    value = normalize_heading(text)
    value = re.sub(r"[^\w\s-]", "", value)
    return re.sub(r"[-\s]+", "-", value).strip("-")


def slug_for_renderer(path: Path, heading: str) -> str:
    try:
        path.resolve().relative_to(DOCS_ROOT.resolve())
    except ValueError:
        return github_slug(heading)
    return mkdocs_slug(heading)


def duplicate_anchor(path: Path, base: str, count: int) -> str:
    if count == 0:
        return base
    try:
        path.resolve().relative_to(DOCS_ROOT.resolve())
    except ValueError:
        return f"{base}-{count}"
    return f"{base}_{count}"


def anchors(path: Path) -> set[str]:
    if path.suffix.lower() != ".md":
        return set()
    values: set[str] = set()
    occurrence: dict[str, int] = {}
    fence_marker: str | None = None
    for line in path.read_text(encoding="utf-8").splitlines():
        fence = FENCE_RE.match(line)
        if fence:
            marker = fence.group(1)[0]
            fence_marker = None if fence_marker == marker else marker
            continue
        if fence_marker:
            continue
        match = HEADING_RE.match(line)
        if not match:
            continue
        heading = match.group(1).strip()
        explicit = EXPLICIT_ID_RE.search(heading)
        if explicit:
            values.add(explicit.group(1))
            heading = EXPLICIT_ID_RE.sub("", heading).strip()
        base = slug_for_renderer(path, heading)
        if not base:
            continue
        count = occurrence.get(base, 0)
        values.add(duplicate_anchor(path, base, count))
        occurrence[base] = count + 1
    return values


def candidate_files(path: Path) -> list[Path]:
    candidates = [path]
    if path.suffix.lower() == ".html":
        candidates.extend([path.with_suffix(".md"), path.parent / "index.md"])
    elif not path.suffix:
        candidates.extend([path.with_suffix(".md"), path / "index.md"])
    return candidates


def page_url_to_source(path: str) -> Path:
    relative = unquote(path)
    if relative.startswith(SITE_PREFIX):
        relative = relative[len(SITE_PREFIX) :]
    else:
        relative = relative.lstrip("/")
    if not relative:
        return DOCS_ROOT / "index.md"
    # A MkDocs route such as /tools/mission-lookup/ may be sourced from
    # either tools/mission-lookup.md or tools/mission-lookup/index.md.
    return DOCS_ROOT / relative.rstrip("/")


def resolve(reference: LinkReference) -> tuple[Path | None, str | None, bool]:
    target = reference.target.strip()
    if target.startswith(("mailto:", "tel:", "javascript:", "data:")):
        return None, None, False

    parsed = urlsplit(target)
    fragment = unquote(parsed.fragment) if parsed.fragment else None
    if parsed.scheme in {"http", "https"}:
        if parsed.hostname != SITE_HOST:
            return None, None, False
        requested = page_url_to_source(parsed.path)
    elif parsed.scheme or target.startswith("//"):
        return None, None, False
    elif parsed.path:
        local_path = unquote(parsed.path)
        if local_path.startswith("/MissionChief-UK/"):
            requested = page_url_to_source(local_path)
        elif local_path.startswith("/"):
            return None, None, False
        else:
            requested = (reference.source.parent / local_path).resolve()
    else:
        requested = reference.source.resolve()

    resolved = next((candidate for candidate in candidate_files(requested) if candidate.is_file()), None)
    return resolved or requested, fragment, resolved is None


def audit() -> list[str]:
    failures: list[str] = []
    anchor_cache: dict[Path, set[str]] = {}
    for source in source_files():
        for reference in references(source):
            destination, fragment, missing = resolve(reference)
            if destination is None:
                continue
            location = f"{display(source)}:{reference.line}"
            if missing:
                failures.append(
                    f"{location}: missing local target {reference.target!r} (resolved near {display(destination)})"
                )
                continue
            if fragment and destination.suffix.lower() == ".md":
                available = anchor_cache.setdefault(destination, anchors(destination))
                if fragment not in available:
                    failures.append(
                        f"{location}: missing anchor #{fragment} in {display(destination)} from {reference.target!r}"
                    )
    return failures


def main() -> int:
    files = source_files()
    failures = audit()
    if failures:
        print("Documentation link audit failed:")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print(f"Documentation link audit passed across {len(files)} Markdown files")
    return 0


if __name__ == "__main__":
    sys.exit(main())
