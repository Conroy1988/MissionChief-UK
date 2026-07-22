#!/usr/bin/env python3

from __future__ import annotations

import hashlib
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SOURCE_ROOT = ROOT / "data" / "sources" / "missionchief-uk"
PUBLIC_ROOT = ROOT / "docs" / "assets" / "data" / "official"
CANONICAL_ROOT = ROOT / "data" / "uk" / "missions"
OFFICIAL_URL = "https://www.missionchief.co.uk/einsaetze.json"
MINIMUM_EXPECTED_MISSIONS = 1000
MAX_TRACKED_FILE_BYTES = 1_000_000

RAW_PATH = SOURCE_ROOT / "einsaetze.raw.json"
COVERAGE_PATH = SOURCE_ROOT / "mission-coverage.json"
INVENTORY_PATH = SOURCE_ROOT / "official-key-inventory.json"
PUBLIC_PATH = PUBLIC_ROOT / "uk-missions.json"
PUBLIC_COVERAGE_PATH = PUBLIC_ROOT / "uk-mission-coverage.json"


def read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"{path.relative_to(ROOT)}: unable to read JSON: {exc}") from exc


def mission_name(record: dict[str, Any]) -> str:
    value = record.get("name") or record.get("caption") or record.get("title")
    return str(value).strip() if value is not None else ""


def stable_id(value: Any) -> tuple[int, int | str]:
    try:
        return (0, int(value))
    except (TypeError, ValueError):
        return (1, str(value))


def canonical_records() -> list[dict[str, Any]]:
    records = []
    for path in sorted(CANONICAL_ROOT.glob("*.json")):
        value = read_json(path)
        if not isinstance(value, dict):
            raise ValueError(f"{path.relative_to(ROOT)}: canonical mission must be an object")
        records.append(value)
    return records


def validate_records(records: Any, label: str) -> tuple[list[dict[str, Any]], dict[str, dict[str, Any]]]:
    if not isinstance(records, list):
        raise ValueError(f"{label}: records must be an array")
    if len(records) < MINIMUM_EXPECTED_MISSIONS:
        raise ValueError(
            f"{label}: only {len(records)} missions; expected at least {MINIMUM_EXPECTED_MISSIONS}"
        )

    by_id: dict[str, dict[str, Any]] = {}
    for index, record in enumerate(records):
        if not isinstance(record, dict):
            raise ValueError(f"{label}: record {index} is not an object")
        mission_id = record.get("id")
        name = mission_name(record)
        if mission_id is None or str(mission_id).strip() == "":
            raise ValueError(f"{label}: record {index} has no id")
        if not name:
            raise ValueError(f"{label}: mission {mission_id} has no name")
        key = str(mission_id)
        if key in by_id:
            raise ValueError(f"{label}: duplicate mission id {key}")
        by_id[key] = record

    ordered = sorted(records, key=lambda record: stable_id(record.get("id")))
    if records != ordered:
        raise ValueError(f"{label}: records are not sorted deterministically by mission id")
    return records, by_id


def expected_key_inventory(records: list[dict[str, Any]], field: str) -> list[dict[str, Any]]:
    counter: Counter[str] = Counter()
    for record in records:
        value = record.get(field)
        if isinstance(value, dict):
            counter.update(str(key) for key in value)
    return [{"key": key, "mission_count": count} for key, count in sorted(counter.items())]


def normalized_source_payload(records: list[dict[str, Any]]) -> bytes:
    return json.dumps(records, ensure_ascii=False, separators=(",", ":")).encode("utf-8")


def audit() -> dict[str, Any]:
    required_paths = (RAW_PATH, COVERAGE_PATH, INVENTORY_PATH, PUBLIC_PATH, PUBLIC_COVERAGE_PATH)
    for path in required_paths:
        if not path.exists():
            raise ValueError(f"Missing official catalogue asset: {path.relative_to(ROOT)}")

    for path in (RAW_PATH, PUBLIC_PATH):
        size = path.stat().st_size
        if size >= MAX_TRACKED_FILE_BYTES:
            raise ValueError(
                f"{path.relative_to(ROOT)} is {size} bytes; must remain below {MAX_TRACKED_FILE_BYTES}"
            )

    raw = read_json(RAW_PATH)
    public = read_json(PUBLIC_PATH)
    coverage = read_json(COVERAGE_PATH)
    public_coverage = read_json(PUBLIC_COVERAGE_PATH)
    inventory = read_json(INVENTORY_PATH)

    if not isinstance(raw, dict) or not isinstance(public, dict):
        raise ValueError("Official source and public catalogue envelopes must be objects")

    raw_records, raw_by_id = validate_records(raw.get("records"), "raw official catalogue")
    public_records, public_by_id = validate_records(public.get("records"), "public official catalogue")

    raw_count = raw.get("count")
    public_count = public.get("count")
    if raw_count != len(raw_records) or public_count != len(public_records):
        raise ValueError("Official catalogue envelope count does not match its record array")
    if raw_count != public_count:
        raise ValueError(f"Raw/public mission counts differ: {raw_count} vs {public_count}")
    if set(raw_by_id) != set(public_by_id):
        missing_public = sorted(set(raw_by_id) - set(public_by_id), key=stable_id)
        missing_raw = sorted(set(public_by_id) - set(raw_by_id), key=stable_id)
        raise ValueError(
            f"Raw/public mission IDs differ; missing public={missing_public[:10]}, missing raw={missing_raw[:10]}"
        )

    source_sha = raw.get("source_sha256")
    if not isinstance(source_sha, str) or len(source_sha) != 64 or any(char not in "0123456789abcdef" for char in source_sha):
        raise ValueError("Raw source SHA-256 is missing or invalid")
    if raw.get("source_url") != OFFICIAL_URL:
        raise ValueError(f"Unexpected official source URL: {raw.get('source_url')}")

    public_source = public.get("source")
    if not isinstance(public_source, dict):
        raise ValueError("Public catalogue source metadata is missing")
    metadata_shas = {
        source_sha,
        public_source.get("sha256"),
        coverage.get("source_sha256"),
        public_coverage.get("source_sha256"),
        inventory.get("source_sha256"),
    }
    if metadata_shas != {source_sha}:
        raise ValueError(f"Catalogue source SHA metadata is inconsistent: {metadata_shas}")
    if public_source.get("url") != OFFICIAL_URL:
        raise ValueError("Public catalogue does not identify the official UK endpoint")
    if public_source.get("fetched_at") != raw.get("fetched_at"):
        raise ValueError("Raw and public catalogue source timestamps differ")

    for mission_id, raw_record in raw_by_id.items():
        public_record = public_by_id[mission_id]
        for key, value in raw_record.items():
            if key not in public_record or public_record[key] != value:
                raise ValueError(f"Public mission {mission_id} does not preserve official field '{key}'")
        expected_url = f"https://www.missionchief.co.uk/einsaetze/{mission_id}"
        if public_record.get("official_url") != expected_url:
            raise ValueError(f"Public mission {mission_id} has an invalid official URL")
        additional = raw_record.get("additional") if isinstance(raw_record.get("additional"), dict) else {}
        expected_limited = bool(additional.get("date_start") or additional.get("date_end"))
        if public_record.get("limited_availability") is not expected_limited:
            raise ValueError(f"Public mission {mission_id} has incorrect limited-availability metadata")
        expected_availability = {
            "starts_at": additional.get("date_start"),
            "ends_at": additional.get("date_end"),
        }
        if public_record.get("availability") != expected_availability:
            raise ValueError(f"Public mission {mission_id} has incorrect availability metadata")

    canonical = canonical_records()
    canonical_by_id = {str(record["id"]): record for record in canonical}
    raw_ids = set(raw_by_id)
    canonical_ids = set(canonical_by_id)
    matched_ids = raw_ids & canonical_ids
    official_only_ids = raw_ids - canonical_ids
    canonical_only_ids = canonical_ids - raw_ids

    expected_coverage = {
        "official_count": len(raw_records),
        "canonical_count": len(canonical),
        "matched_count": len(matched_ids),
        "official_only_count": len(official_only_ids),
        "canonical_only_count": len(canonical_only_ids),
        "coverage_percent": round(len(matched_ids) / len(raw_records) * 100, 2),
    }
    for key, value in expected_coverage.items():
        if coverage.get(key) != value or public_coverage.get(key) != value:
            raise ValueError(
                f"Coverage field '{key}' is inconsistent; expected {value}, "
                f"source={coverage.get(key)}, public={public_coverage.get(key)}"
            )

    expected_official_only = [
        {"id": raw_by_id[mission_id].get("id"), "name": mission_name(raw_by_id[mission_id])}
        for mission_id in sorted(official_only_ids, key=stable_id)
    ]
    expected_canonical_only = [
        {"id": canonical_by_id[mission_id].get("id"), "name": mission_name(canonical_by_id[mission_id])}
        for mission_id in sorted(canonical_only_ids, key=stable_id)
    ]
    if coverage.get("official_only") != expected_official_only:
        raise ValueError("Official-only reconciliation list is stale or incorrectly ordered")
    if coverage.get("canonical_only") != expected_canonical_only:
        raise ValueError("Canonical-only reconciliation list is stale or incorrectly ordered")

    expected_mismatches = []
    for mission_id in sorted(matched_ids, key=stable_id):
        official_name = mission_name(raw_by_id[mission_id])
        canonical_name = mission_name(canonical_by_id[mission_id])
        if official_name.casefold() != canonical_name.casefold():
            expected_mismatches.append(
                {
                    "id": raw_by_id[mission_id].get("id"),
                    "official_name": official_name,
                    "canonical_name": canonical_name,
                }
            )
    if coverage.get("name_mismatches") != expected_mismatches:
        raise ValueError("Canonical/official name mismatch report is stale")

    for field in ("requirements", "chances", "prerequisites"):
        expected = expected_key_inventory(raw_records, field)
        if inventory.get(field) != expected:
            raise ValueError(f"Official {field} key inventory is stale")

    return {
        "official_count": len(raw_records),
        "canonical_count": len(canonical),
        "matched_count": len(matched_ids),
        "official_only_count": len(official_only_ids),
        "source_sha256": source_sha,
        "raw_compact_sha256": hashlib.sha256(normalized_source_payload(raw_records)).hexdigest(),
    }


def main() -> int:
    try:
        result = audit()
    except ValueError as exc:
        print(f"Official UK mission catalogue audit failed: {exc}", file=sys.stderr)
        return 1

    print(
        "Official UK mission catalogue audit passed: "
        f"{result['official_count']} official missions, "
        f"{result['matched_count']}/{result['canonical_count']} canonical ID matches, "
        f"{result['official_only_count']} official missions awaiting canonical mapping, "
        f"source SHA-256 {result['source_sha256']}."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
