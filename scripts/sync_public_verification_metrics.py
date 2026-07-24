#!/usr/bin/env python3

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Callable

ROOT = Path(__file__).resolve().parents[1]
STATUS_PATH = ROOT / "data" / "sources" / "missionchief-uk" / "mission-verification-status.json"
BATCH_ROOT = ROOT / "data" / "uk" / "mission-verification-batches"
README_PATH = ROOT / "README.md"
HOME_PATH = ROOT / "docs" / "index.md"
API_PATH = ROOT / "docs" / "api" / "index.md"
RELEASE_PATH = ROOT / "docs" / "releases" / "v1.1.0.md"
CHANGELOG_PATH = ROOT / "CHANGELOG.md"
MISSION_LOOKUP_PATH = ROOT / "docs" / "tools" / "mission-lookup.md"
OFFICIAL_CATALOGUE_PATH = ROOT / "docs" / "reference" / "official-mission-catalogue.md"

COLLECTION_ROOTS = {
    "missions": ROOT / "data" / "uk" / "missions",
    "vehicles": ROOT / "data" / "uk" / "vehicles",
    "infrastructure": ROOT / "data" / "uk" / "infrastructure",
    "training": ROOT / "data" / "uk" / "training",
}

STATIC_BATCHES: dict[int, list[int]] = {
    1: [0, 1, 2, 3, 4, 6, 7, 8, 9, 10, 11],
    2: [13, 14, 15, 16, 17, 18, 19, 23, 24, 27],
}


class SyncFailure(RuntimeError):
    pass


def read_json(path: Path) -> object:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise SyncFailure(f"Unable to read {path.relative_to(ROOT)}: {exc}") from exc


def replace_once(
    text: str,
    pattern: str,
    replacement: str | Callable[[re.Match[str]], str],
    label: str,
    *,
    flags: int = 0,
) -> str:
    updated, count = re.subn(pattern, replacement, text, count=1, flags=flags)
    if count != 1:
        raise SyncFailure(f"Expected exactly one {label} pattern; found {count}")
    return updated


def write_if_changed(path: Path, content: str) -> bool:
    existing = path.read_text(encoding="utf-8")
    if existing == content:
        return False
    path.write_text(content, encoding="utf-8")
    return True


def load_metrics() -> dict[str, int | float]:
    document = read_json(STATUS_PATH)
    if not isinstance(document, dict):
        raise SyncFailure("Mission verification status must be an object")
    summary = document.get("summary")
    if not isinstance(summary, dict):
        raise SyncFailure("Mission verification status summary is missing")
    cumulative = summary.get("cumulative_stage_counts")
    if not isinstance(cumulative, dict):
        raise SyncFailure("Mission verification cumulative stage counts are missing")

    official = summary.get("official_count")
    canonical = summary.get("canonical_count")
    direct = summary.get("direct_canonical_id_matches")
    fully = cumulative.get("fully-canonical")
    remaining = summary.get("remaining_to_fully_canonical")
    values = (official, canonical, direct, fully, remaining)
    if not all(isinstance(value, int) for value in values):
        raise SyncFailure("Verification metrics must be integers")
    assert isinstance(official, int)
    assert isinstance(canonical, int)
    assert isinstance(direct, int)
    assert isinstance(fully, int)
    assert isinstance(remaining, int)
    if fully + remaining != official:
        raise SyncFailure("Fully canonical and remaining metrics do not equal official count")
    if direct > canonical or fully > direct:
        raise SyncFailure("Canonical verification metric ordering is invalid")

    collection_counts = {
        name: len(list(path.glob("*.json")))
        for name, path in COLLECTION_ROOTS.items()
    }
    if collection_counts["missions"] != canonical:
        raise SyncFailure(
            "Canonical mission directory contains "
            f"{collection_counts['missions']} records; status reports {canonical}"
        )

    return {
        "official": official,
        "canonical": canonical,
        "direct": direct,
        "fully": fully,
        "remaining": remaining,
        "awaiting": official - direct,
        "overlays": canonical - direct,
        "identity_percent": round((direct / official) * 100, 2),
        "fully_percent": round((fully / official) * 100, 2),
        "vehicles": collection_counts["vehicles"],
        "infrastructure": collection_counts["infrastructure"],
        "training": collection_counts["training"],
        "search_entities": sum(collection_counts.values()),
    }


def stable_int(value: object) -> int:
    try:
        return int(str(value))
    except (TypeError, ValueError) as exc:
        raise SyncFailure(f"Batch mission ID is not numeric: {value!r}") from exc


def load_batches() -> dict[int, list[int]]:
    batches = {number: list(ids) for number, ids in STATIC_BATCHES.items()}
    pattern = re.compile(r"fully-canonical-fire-batch-(\d+)\.json$")
    for path in sorted(BATCH_ROOT.glob("fully-canonical-fire-batch-*.json")):
        match = pattern.search(path.name)
        if match is None:
            continue
        number = int(match.group(1))
        document = read_json(path)
        if not isinstance(document, dict) or not isinstance(document.get("records"), dict):
            raise SyncFailure(f"Invalid batch registry: {path.relative_to(ROOT)}")
        ids = sorted(stable_int(value) for value in document["records"])
        if not ids:
            raise SyncFailure(f"Batch registry is empty: {path.relative_to(ROOT)}")
        batches[number] = ids

    expected = list(range(1, max(batches) + 1))
    if sorted(batches) != expected:
        raise SyncFailure(f"Batch sequence is not contiguous: {sorted(batches)}")
    return batches


def render_batch_block(batches: dict[int, list[int]], width: int = 10) -> str:
    lines: list[str] = []
    for number, ids in sorted(batches.items()):
        chunks = [ids[index : index + width] for index in range(0, len(ids), width)]
        for index, chunk in enumerate(chunks):
            prefix = f"Batch {number}: " if index == 0 else "         "
            suffix = "," if index < len(chunks) - 1 else ""
            lines.append(prefix + ", ".join(str(value) for value in chunk) + suffix)
    return "\n".join(lines)


def render_changelog_batches(batches: dict[int, list[int]]) -> str:
    return "\n".join(
        f"- Batch {number}: IDs " + ", ".join(f"`{value}`" for value in ids) + "."
        for number, ids in sorted(batches.items())
    )


def format_number(value: int | float) -> str:
    if isinstance(value, int):
        return f"{value:,}"
    return f"{value:.2f}"


def sync_readme(text: str, metrics: dict[str, int | float], batches: dict[int, list[int]]) -> str:
    official = format_number(metrics["official"])
    canonical = format_number(metrics["canonical"])
    direct = format_number(metrics["direct"])
    fully = format_number(metrics["fully"])
    awaiting = format_number(metrics["awaiting"])
    overlays = format_number(metrics["overlays"])
    remaining = format_number(metrics["remaining"])
    identity_percent = format_number(metrics["identity_percent"])
    fully_percent = format_number(metrics["fully_percent"])
    vehicles = format_number(metrics["vehicles"])
    infrastructure = format_number(metrics["infrastructure"])
    training = format_number(metrics["training"])
    search_entities = format_number(metrics["search_entities"])
    max_batch = max(batches)
    batch_block = render_batch_block(batches)

    text = replace_once(
        text,
        r"\*\*[\d,]+ official UK missions · [\d,]+ canonical mission records · [\d,]+ fully canonical missions · Instant command search · Fleet planning · Evidence governance · Versioned public data\*\*",
        f"**{official} official UK missions · {canonical} canonical mission records · {fully} fully canonical missions · Instant command search · Fleet planning · Evidence governance · Versioned public data**",
        "README hero metrics",
    )
    row_values = {
        "Canonical missions": canonical,
        "Official/canonical ID matches": direct,
        "Fully canonical missions": fully,
        "Official records awaiting canonical records": awaiting,
        "Canonical-only overlays": overlays,
        "Deployable resources": vehicles,
        "Infrastructure": infrastructure,
        "Qualifications": training,
        "Canonical searchable entities": search_entities,
    }
    for label, value in row_values.items():
        text = replace_once(
            text,
            rf"(\| \*\*{re.escape(label)}\*\* \| \*\*)[\d,]+(\*\* \|)",
            rf"\g<1>{value}\g<2>",
            f"README {label} row",
        )

    text = replace_once(
        text,
        r"\| Identity verified \| \*\*[\d,]+ / [\d,]+ — [\d.]+%\*\* \|",
        f"| Identity verified | **{direct} / {official} — {identity_percent}%** |",
        "README identity metric",
    )
    text = replace_once(
        text,
        r"\| Fully canonical \| \*\*[\d,]+ / [\d,]+ — [\d.]+%\*\* \|",
        f"| Fully canonical | **{fully} / {official} — {fully_percent}%** |",
        "README fully canonical metric",
    )
    text = replace_once(
        text,
        r"\| Remaining to fully canonical \| \*\*[\d,]+\*\* \|",
        f"| Remaining to fully canonical | **{remaining}** |",
        "README remaining metric",
    )
    text = replace_once(
        text,
        r"(The current evidence-controlled batches are:\n\n```text\n).*?(\n```)",
        rf"\g<1>{batch_block}\g<2>",
        "README batch block",
        flags=re.DOTALL,
    )
    text = replace_once(
        text,
        r"(?:Batch 4 adds strict chance-aware interpretation|Batches 4–\d+ extend the verified vehicle-key contract).*?strict-equivalence validation\.",
        (
            f"Batches 4–{max_batch} extend the verified vehicle-key contract through evidence-safe, "
            f"exact-ID promotions. All {fully} records pass aggregate identity and strict-equivalence validation."
        ),
        "README batch summary",
        flags=re.DOTALL,
    )
    text = replace_once(
        text,
        r"(\| \*\*Canonical mapped\*\* \| )[\d,]+( normalized project records \|)",
        rf"\g<1>{canonical}\g<2>",
        "README canonical lookup count",
    )
    text = replace_once(
        text,
        r"(├── missions/\s+)[\d,]+( canonical mission records)",
        rf"\g<1>{canonical}\g<2>",
        "README data estate mission count",
    )
    text = replace_once(
        text,
        r"(├── vehicles/\s+)[\d,]+( deployable resources)",
        rf"\g<1>{vehicles}\g<2>",
        "README data estate resource count",
    )
    text = replace_once(
        text,
        r"(├── infrastructure/\s+)[\d,]+( buildings and extensions)",
        rf"\g<1>{infrastructure}\g<2>",
        "README data estate infrastructure count",
    )
    text = replace_once(
        text,
        r"(└── training/\s+)[\d,]+( qualification records)",
        rf"\g<1>{training}\g<2>",
        "README data estate qualification count",
    )
    return text


def sync_home(text: str, metrics: dict[str, int | float]) -> str:
    replacements = (
        (r'(data-mcuk-metric="missions">)[\d,]+(<)', format_number(metrics["canonical"]), "home hero canonical"),
        (r'(data-mcuk-metric="fully-canonical">)[\d,]+(<)', format_number(metrics["fully"]), "home hero fully"),
        (r'(alongside )[\d,]+( higher-trust canonical mappings)', format_number(metrics["canonical"]), "home lookup canonical"),
        (r'(data-mcuk-collection="missions">)[\d,]+(<)', format_number(metrics["canonical"]), "home board canonical"),
        (r'(data-mcuk-verification="fully-canonical">)[\d,]+(<)', format_number(metrics["fully"]), "home board fully"),
        (r'(data-mcuk-collection="vehicles">)[\d,]+(<)', format_number(metrics["vehicles"]), "home board resource count"),
        (r'(data-mcuk-collection="infrastructure">)[\d,]+(<)', format_number(metrics["infrastructure"]), "home board infrastructure count"),
        (r'(data-mcuk-collection="training">)[\d,]+(<)', format_number(metrics["training"]), "home board qualification count"),
        (r'(<span><b>)[\d,]+(</b> direct ID matches)', format_number(metrics["direct"]), "home direct matches"),
        (r'(data-mcuk-search-count>)[\d,]+(<)', format_number(metrics["search_entities"]), "home search count"),
    )
    for pattern, value, label in replacements:
        text = replace_once(text, pattern, rf"\g<1>{value}\g<2>", label)
    return text


def sync_mission_lookup(text: str, metrics: dict[str, int | float]) -> str:
    block = "\n".join(
        (
            f"{format_number(metrics['official'])} official UK missions",
            f"{format_number(metrics['canonical'])} canonical mission records",
            f"{format_number(metrics['direct'])} direct official/canonical ID matches",
            f"{format_number(metrics['fully'])} fully canonical missions",
            f"{format_number(metrics['awaiting'])} official missions awaiting direct canonical records",
        )
    )
    return replace_once(
        text,
        r"(## Current coverage\n\n```text\n).*?(\n```)",
        lambda match: match.group(1) + block + match.group(2),
        "Mission Lookup coverage block",
        flags=re.DOTALL,
    )


def sync_official_catalogue(text: str, metrics: dict[str, int | float]) -> str:
    block = "\n".join(
        (
            f"{format_number(metrics['official'])} official UK missions captured",
            f"{format_number(metrics['canonical'])} canonical mission records",
            f"{format_number(metrics['direct'])} direct official/canonical ID matches",
            f"{format_number(metrics['fully'])} fully canonical missions",
            f"{format_number(metrics['awaiting'])} official missions awaiting direct canonical records",
            f"{format_number(metrics['overlays'])} canonical-only overlays or derived records",
        )
    )
    return replace_once(
        text,
        r"(## Current programme position\n\n```text\n).*?(\n```)",
        lambda match: match.group(1) + block + match.group(2),
        "official catalogue programme block",
        flags=re.DOTALL,
    )


def sync_api(text: str, metrics: dict[str, int | float]) -> str:
    values = {
        "Canonical missions": metrics["canonical"],
        "Official UK missions": metrics["official"],
        "Direct official/canonical ID matches": metrics["direct"],
        "Fully canonical missions": metrics["fully"],
    }
    for label, value in values.items():
        text = replace_once(
            text,
            rf"({re.escape(label)}: )[\d,]+",
            rf"\g<1>{format_number(value)}",
            f"API {label}",
        )
    text = replace_once(text, r'("count": )[\d,]+,', rf'\g<1>{metrics["canonical"]},', "API canonical envelope count")
    summary_values = {
        "official_count": metrics["official"],
        "canonical_count": metrics["canonical"],
        "direct_canonical_id_matches": metrics["direct"],
        "fully_canonical_percent": metrics["fully_percent"],
        "remaining_to_fully_canonical": metrics["remaining"],
    }
    for key, value in summary_values.items():
        formatted = format_number(value) if isinstance(value, float) else str(value)
        text = replace_once(
            text,
            rf'("{key}": )[\d.]+',
            rf"\g<1>{formatted}",
            f"API verification {key}",
        )
    return text


def sync_release(text: str, metrics: dict[str, int | float], batches: dict[int, list[int]]) -> str:
    baseline_values = (
        (r"[\d,]+ official UK mission records", f"{format_number(metrics['official'])} official UK mission records", "release official baseline"),
        (r"[\d,]+ canonical mission records", f"{format_number(metrics['canonical'])} canonical mission records", "release canonical baseline"),
        (r"[\d,]+ official IDs matched to canonical records", f"{format_number(metrics['direct'])} official IDs matched to canonical records", "release direct baseline"),
        (r"[\d,]+ fully canonical mission records", f"{format_number(metrics['fully'])} fully canonical mission records", "release fully baseline"),
        (r"[\d,]+ official records awaiting direct canonical records", f"{format_number(metrics['awaiting'])} official records awaiting direct canonical records", "release awaiting baseline"),
        (r"[\d,]+ canonical overlay or derived records without standalone official IDs", f"{format_number(metrics['overlays'])} canonical overlay or derived records without standalone official IDs", "release overlay baseline"),
        (r"[\d,]+ canonical deployable-resource records", f"{format_number(metrics['vehicles'])} canonical deployable-resource records", "release resource baseline"),
        (r"[\d,]+ canonical infrastructure records", f"{format_number(metrics['infrastructure'])} canonical infrastructure records", "release infrastructure baseline"),
        (r"[\d,]+ qualification records", f"{format_number(metrics['training'])} qualification records", "release qualification baseline"),
    )
    for pattern, replacement, label in baseline_values:
        text = replace_once(text, pattern, replacement, label)
    text = replace_once(
        text,
        r"The first \w+ fully canonical batches contain:",
        f"The first {len(batches)} fully canonical batches contain:",
        "release batch count heading",
    )
    text = replace_once(
        text,
        r"(The first \d+ fully canonical batches contain:\n\n```text\n).*?(\n```)",
        rf"\g<1>{render_batch_block(batches)}\g<2>",
        "release batch block",
        flags=re.DOTALL,
    )
    text = replace_once(
        text,
        r"(?:The first 49 records use explicitly mapped|All [\d,]+ promoted missions pass exact official identity).*?(?=\n\n## Accuracy controls)",
        (
            f"All {format_number(metrics['fully'])} promoted missions pass exact official identity, aggregate diagnostics "
            f"and strict key equivalence. The current analyser has exhausted every mission covered by the verified "
            f"mapping contract and reports zero immediately safe records; the next phase requires another verified "
            f"official-key mapping."
        ),
        "release verification narrative",
        flags=re.DOTALL,
    )
    return text


def sync_changelog(text: str, metrics: dict[str, int | float], batches: dict[int, list[int]]) -> str:
    replacements = (
        (r"against [\d,]+ canonical mission records", f"against {format_number(metrics['canonical'])} canonical mission records", "changelog canonical count"),
        (
            r"Identified [\d,]+ direct official/canonical ID matches, [\d,]+ official records awaiting direct canonical records and [\d,]+ canonical overlay or derived records",
            (
                f"Identified {format_number(metrics['direct'])} direct official/canonical ID matches, "
                f"{format_number(metrics['awaiting'])} official records awaiting direct canonical records and "
                f"{format_number(metrics['overlays'])} canonical overlay or derived records"
            ),
            "changelog reconciliation metrics",
        ),
        (
            r"Fully canonicalized [\d,]+ missions across \w+ Fire and Rescue batches\.",
            f"Fully canonicalized {format_number(metrics['fully'])} missions across {len(batches)} Fire and Rescue batches.",
            "changelog fully canonical total",
        ),
        (
            r"Confirmed all [\d,]+ promoted missions pass exact official identity and strict key equivalence\.",
            f"Confirmed all {format_number(metrics['fully'])} promoted missions pass exact official identity and strict key equivalence.",
            "changelog promoted total",
        ),
        (
            r"Expanded the canonical mission collection from 62 to [\d,]+ records\.",
            f"Expanded the canonical mission collection from 62 to {format_number(metrics['canonical'])} records.",
            "changelog canonical expansion total",
        ),
    )
    for pattern, replacement, label in replacements:
        text = replace_once(text, pattern, replacement, label)
    text = replace_once(
        text,
        r"- Batch 1: IDs .*?(?=\n- Added verified Aerial Appliance Truck)",
        render_changelog_batches(batches) + "\n",
        "changelog batch list",
        flags=re.DOTALL,
    )
    return text


def main() -> int:
    try:
        metrics = load_metrics()
        batches = load_batches()
        updates = {
            README_PATH: sync_readme(README_PATH.read_text(encoding="utf-8"), metrics, batches),
            HOME_PATH: sync_home(HOME_PATH.read_text(encoding="utf-8"), metrics),
            API_PATH: sync_api(API_PATH.read_text(encoding="utf-8"), metrics),
            RELEASE_PATH: sync_release(RELEASE_PATH.read_text(encoding="utf-8"), metrics, batches),
            CHANGELOG_PATH: sync_changelog(CHANGELOG_PATH.read_text(encoding="utf-8"), metrics, batches),
            MISSION_LOOKUP_PATH: sync_mission_lookup(
                MISSION_LOOKUP_PATH.read_text(encoding="utf-8"), metrics
            ),
            OFFICIAL_CATALOGUE_PATH: sync_official_catalogue(
                OFFICIAL_CATALOGUE_PATH.read_text(encoding="utf-8"), metrics
            ),
        }
        changed = [path for path, content in updates.items() if write_if_changed(path, content)]
    except (OSError, SyncFailure) as exc:
        print(f"Public verification metric synchronization failed: {exc}", file=sys.stderr)
        return 1

    changed_text = ", ".join(path.relative_to(ROOT).as_posix() for path in changed) or "none"
    print(
        "Public verification metrics synchronized: "
        f"canonical={metrics['canonical']}, direct={metrics['direct']}, "
        f"fully={metrics['fully']}, remaining={metrics['remaining']}, "
        f"vehicles={metrics['vehicles']}, infrastructure={metrics['infrastructure']}, "
        f"training={metrics['training']}, "
        f"batches={len(batches)}, changed={changed_text}."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
