#!/usr/bin/env python3

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SOURCE_ROOT = ROOT / "data" / "sources" / "missionchief-uk"
PUBLIC_ROOT = ROOT / "docs" / "assets" / "data" / "official"
CANONICAL_ROOT = ROOT / "data" / "uk" / "missions"
RAW_PATH = SOURCE_ROOT / "einsaetze.raw.json"
SOURCE_COVERAGE_PATH = SOURCE_ROOT / "mission-coverage.json"
PUBLIC_COVERAGE_PATH = PUBLIC_ROOT / "uk-mission-coverage.json"


def read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"{path.relative_to(ROOT)}: unable to read JSON: {exc}") from exc


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        json.dump(value, handle, ensure_ascii=False, indent=2, sort_keys=True)
        handle.write("\n")


def mission_name(record: dict[str, Any]) -> str:
    value = record.get("name") or record.get("caption") or record.get("title")
    return str(value).strip() if value is not None else ""


def stable_id(value: Any) -> tuple[int, int | str]:
    try:
        return (0, int(value))
    except (TypeError, ValueError):
        return (1, str(value))


def canonical_records() -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for path in sorted(CANONICAL_ROOT.glob("*.json")):
        value = read_json(path)
        if not isinstance(value, dict):
            raise ValueError(f"{path.relative_to(ROOT)}: canonical mission must be an object")
        if value.get("id") is None:
            raise ValueError(f"{path.relative_to(ROOT)}: canonical mission has no id")
        records.append(value)
    return records


def coverage_report(official: list[dict[str, Any]], canonical: list[dict[str, Any]]) -> dict[str, Any]:
    official_by_id = {str(record["id"]): record for record in official}
    canonical_by_id = {str(record["id"]): record for record in canonical}
    official_only_ids = sorted(set(official_by_id) - set(canonical_by_id), key=stable_id)
    canonical_only_ids = sorted(set(canonical_by_id) - set(official_by_id), key=stable_id)
    matched_ids = sorted(set(official_by_id) & set(canonical_by_id), key=stable_id)

    name_mismatches: list[dict[str, Any]] = []
    for mission_id in matched_ids:
        official_name = mission_name(official_by_id[mission_id])
        canonical_name = mission_name(canonical_by_id[mission_id])
        if official_name.casefold() != canonical_name.casefold():
            name_mismatches.append(
                {
                    "id": official_by_id[mission_id].get("id"),
                    "official_name": official_name,
                    "canonical_name": canonical_name,
                }
            )

    return {
        "official_count": len(official),
        "canonical_count": len(canonical),
        "matched_count": len(matched_ids),
        "official_only_count": len(official_only_ids),
        "canonical_only_count": len(canonical_only_ids),
        "coverage_percent": round(len(matched_ids) / len(official) * 100, 2) if official else 0,
        "official_only": [
            {"id": official_by_id[mission_id].get("id"), "name": mission_name(official_by_id[mission_id])}
            for mission_id in official_only_ids
        ],
        "canonical_only": [
            {"id": canonical_by_id[mission_id].get("id"), "name": mission_name(canonical_by_id[mission_id])}
            for mission_id in canonical_only_ids
        ],
        "name_mismatches": name_mismatches,
    }


def reconcile() -> dict[str, Any]:
    raw = read_json(RAW_PATH)
    if not isinstance(raw, dict):
        raise ValueError("Official UK mission source envelope must be an object")
    official = raw.get("records")
    if not isinstance(official, list) or not official:
        raise ValueError("Official UK mission source records must be a non-empty array")
    if not all(isinstance(record, dict) and record.get("id") is not None for record in official):
        raise ValueError("Official UK mission source contains an invalid record")

    report = coverage_report(official, canonical_records())
    report.update(
        {
            "schema_version": "1",
            "generated_at": raw.get("fetched_at"),
            "source_url": raw.get("source_url"),
            "source_sha256": raw.get("source_sha256"),
        }
    )
    write_json(SOURCE_COVERAGE_PATH, report)
    write_json(PUBLIC_COVERAGE_PATH, {"collection": "official-uk-mission-coverage", **report})
    return report


def main() -> int:
    try:
        report = reconcile()
    except ValueError as exc:
        print(f"Official mission coverage reconciliation failed: {exc}", file=sys.stderr)
        return 1

    print(
        "Official mission coverage reconciled: "
        f"{report['matched_count']}/{report['official_count']} direct official/canonical matches, "
        f"{report['official_only_count']} official missions awaiting canonical records and "
        f"{report['canonical_only_count']} canonical-only overlays or derived records."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
