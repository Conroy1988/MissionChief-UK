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
HEADING_RE = re.compile(r"^\s{0,3}(#{1,6})\s+(.+?)\s*#*\s*$")
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


class LinkAuditError(RuntimeError):
    pass


def display(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def source_files() -> list[Path]:
    files = [ROOT / "README.md", ROOT / "CHANGELOG.md"]
    files.extend(sorted(DOCS_ROOT.rglob("*.md")))
    return [path for path in files if path.is_file()]


def content_without_fences(text: str) -> str:
    output: list[str] = []
    active_fence: str | None = None
    for line in text.splitlines(keepends=True):
        match = FENCE_RE.match(line)
        if match:
            marker = match.group(1)[0]
            active_fence = None if active_fence == marker else marker
            output.append("\n")
            continue
        output.append("\n" if active_fence else line)
    return "".join(output)


def extract_target(raw: str) -> str:
    value = html.unescape(raw.strip())
    if value.startswith("<") and ">" in value:
        return value[1 : value.index(">")].strip()
    # Markdown permits an optional quoted title after the destination.
    return value.split(maxsplit=1)[0].strip()


def references(path: Path) -> list[LinkReference]:
    text = content_without_fences(path.read_text(encoding="utf-8"))
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


def github_slug(text: str) -> str:
    value = html.unescape(text).lower()
    value = INLINE_LINK_TEXT_RE.sub(r"\1", value)
    value = HTML_TAG_RE.sub("", value)
    value = MARKDOWN_MARKUP_RE.sub("", value)
    value = unicodedata.normalize("NFKD", value)
    value = "".join(character for character in value if not unicodedata.combining(character))
    value = "".join(character for character in value if character.isalnum() or character in " -_")
    return re.sub(r"\s", "-", value)


def mkdocs_slug(text: str) -> str:
    value = html.unescape(text).lower()
    value = INLINE_LINK_TEXT_RE.sub(r"\1", value)
    value = HTML_TAG_RE.sub("", value)
    value = MARKDOWN_MARKUP_RE.sub("", value)
    value = unicodedata.normalize("NFKD", value)
    value = "".join(character for character in value if not unicodedata.combining(character))
    value = re.sub(r"[^\w\s-]", "", value)
    return re.sub(r"[-\s]+", "-", value).strip("-")


def anchors(path: Path) -> set[str]:
    if path.suffix.lower() != ".md":
        return set()
    values: set[str] = set()
    counts: dict[str, int] = {}
    in_fence = False
    fence_marker: str | None = None
    for line in path.read_text(encoding="utf-8").splitlines():
        fence = FENCE_RE.match(line)
        if fence:
            marker = fence.group(1)[0]
            if not in_fence:
                in_fence = True
                fence_marker = marker
            elif marker == fence_marker:
                in_fence = False
                fence_marker = None
            continue
        if in_fence:
            continue
        heading = HEADING_RE.match(line)
        if not heading:
            continue
        heading_text = heading.group(2).strip()
        explicit = EXPLICIT_ID_RE.search(heading_text)
        if explicit:
            values.add(explicit.group(1))
            heading_text = EXPLICIT_ID_RE.sub("", heading_text).strip()
        for base in {github_slug(heading_text), mkdocs_slug(heading_text)}:
            if not base:
                continue
            count = counts.get(base, 0)
            values.add(base if count == 0 else f"{base}_{count}")
            counts[base] = count + 1
    return values


def candidate_files(path: Path) -> list[Path]:
    candidates = [path]
    if path.suffix.lower() == ".html":
        candidates.extend([path.with_suffix(".md"), path.parent / "index.md"])
    elif not path.suffix:
        candidates.extend([path.with_suffix(".md"), path / "index.md"])
    elif path.is_dir():
        candidates.append(path / "index.md")
    return candidates


def site_path_to_source(path: str) -> Path:
    relative = path
    if relative.startswith(SITE_PREFIX):
        relative = relative[len(SITE_PREFIX) :]
    else:
        relative = relative.lstrip("/")
    relative = unquote(relative)
    if not relative:
        return DOCS_ROOT / "index.md"
    destination = DOCS_ROOT / relative
    if relative.endswith("/"):
        destination = destination / "index.md"
    return destination


def resolve(reference: LinkReference) -> tuple[Path | None, str | None, str | None]:
    target = reference.target.strip()
    if target.startswith(("mailto:", "tel:", "javascript:", "data:")):
        return None, None, None

    parsed = urlsplit(target)
    fragment = unquote(parsed.fragment) if parsed.fragment else None
    if parsed.scheme in {"http", "https"}:
        if parsed.hostname != SITE_HOST:
            return None, None, None
        destination = site_path_to_source(parsed.path)
    elif parsed.scheme or target.startswith("//"):
        return None, None, None
    elif parsed.path:
        clean_path = unquote(parsed.path)
        if clean_path.startswith("/MissionChief-UK/"):
            destination = site_path_to_source(clean_path)
        elif clean_path.startswith("/"):
            # Other root-relative paths are outside this Pages project.
            return None, None, None
        else:
            destination = (reference.source.parent / clean_path).resolve()
    else:
        destination = reference.source.resolve()

    resolved = next((item for item in candidate_files(destination) if item.is_file()), None)
    if resolved is None:
        return destination, fragment, "missing"
    return resolved, fragment, None


def audit() -> list[str]:
    failures: list[str] = []
    anchor_cache: dict[Path, set[str]] = {}
    for source in source_files():
        for reference in references(source):
            destination, fragment, state = resolve(reference)
            if destination is None:
                continue
            location = f"{display(source)}:{reference.line}"
            if state == "missing":
                failures.append(f"{location}: missing local target {reference.target!r} (resolved near {display(destination)})")
                continue
            if fragment and destination.suffix.lower() == ".md":
                available = anchor_cache.setdefault(destination, anchors(destination))
                if fragment not in available:
                    failures.append(
                        f"{location}: missing anchor #{fragment} in {display(destination)} from {reference.target!r}"
                    )
    return failures


def main() -> int:
    failures = audit()
    if failures:
        print("Documentation link audit failed:")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print(f"Documentation link audit passed across {len(source_files())} Markdown files")
    return 0


if __name__ == "__main__":
    sys.exit(main())
