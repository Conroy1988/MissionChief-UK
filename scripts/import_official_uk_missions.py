#!/usr/bin/env python3

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import time
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_URL = "https://www.missionchief.co.uk/einsaetze.json"
DEFAULT_OUTPUT = ROOT / "data" / "sources" / "missionchief-uk"
DEFAULT_CANONICAL = ROOT / "data" / "uk" / "missions"
MINIMUM_PLAUSIBLE_RECORDS = 100


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Download, validate and reconcile the official MissionChief UK mission catalogue."
    )
    parser.add_argument("--url", default=DEFAULT_URL, help="Official mission JSON endpoint.")
    parser.add_argument("--input", type=Path, help="Read an existing JSON payload instead of downloading it.")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--canonical-dir", type=Path, default=DEFAULT_CANONICAL)
    parser.add_argument("--timeout", type=int, default=45)
    parser.add_argument("--retries", type=int, default=3)
    return parser.parse_args()


def read_payload(args: argparse.Namespace) -> tuple[bytes, str]:
    if args.input:
        return args.input.read_bytes(), str(args.input)

    request = Request(
        args.url,
        headers={
            "Accept": "application/json",
            "User-Agent": "MissionChief-UK-Guide/official-catalogue-importer (+https://github.com/Conroy1988/MissionChief-UK)",
        },
    )
    last_error: Exception | None = None
    for attempt in range(1, max(1, args.retries) + 1):
        try:
            with urlopen(request, timeout=args.timeout) as response:
                status = getattr(response, "status", 200)
                if status != 200:
                    raise RuntimeError(f"Official mission endpoint returned HTTP {status}")
                content_type = response.headers.get("Content-Type", "")
                if "json" not in content_type.lower():
                    raise RuntimeError(f"Official mission endpoint returned unexpected content type: {content_type}")
                return response.read(), args.url
        except (HTTPError, URLError, TimeoutError, RuntimeError) as exc:
            last_error = exc
            if attempt < max(1, args.retries):
                time.sleep(min(2 ** (attempt - 1), 8))
    raise RuntimeError(f"Unable to retrieve official UK mission catalogue: {last_error}")


def decode_records(payload: bytes) -> list[dict[str, Any]]:
    try:
        decoded = json.loads(payload.decode("utf-8-sig"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValueError(f"Official mission feed is not valid UTF-8 JSON: {exc}") from exc

    if isinstance(decoded, dict):
        decoded = list(decoded.values())
    if not isinstance(decoded, list):
        raise ValueError("Official mission feed must be a JSON array or object of mission records")

    records = [record for record in decoded if isinstance(record, dict)]
    if len(records) != len(decoded):
        raise ValueError("Official mission feed contains non-object entries")
    if len(records) < MINIMUM_PLAUSIBLE_RECORDS:
        raise ValueError(
            f"Official mission feed contains only {len(records)} records; expected at least {MINIMUM_PLAUSIBLE_RECORDS}"
        )
    return records


def mission_name(record: dict[str, Any]) -> str:
    value = record.get("name") or record.get("caption") or record.get("title")
    return str(value).strip() if value is not None else ""


def stable_id(value: Any) -> tuple[int, int | str]:
    try:
        return (0, int(value))
    except (TypeError, ValueError):
        return (1, str(value))


def validate_records(records: list[dict[str, Any]]) -> None:
    ids: dict[str, int] = {}
    failures: list[str] = []
    for index, record in enumerate(records):
        mission_id = record.get("id")
        name = mission_name(record)
        if mission_id is None or str(mission_id).strip() == "":
            failures.append(f"record {index}: missing id")
            continue
        if not name:
            failures.append(f"mission {mission_id}: missing name")
        key = str(mission_id)
        if key in ids:
            failures.append(f"mission id {key}: duplicate records at positions {ids[key]} and {index}")
        else:
            ids[key] = index
    if failures:
        raise ValueError("Official mission feed validation failed:\n- " + "\n- ".join(failures[:100]))


def load_canonical(directory: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    if not directory.exists():
        return records
    for path in sorted(directory.glob("*.json")):
        try:
            value = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise ValueError(f"Unable to read canonical mission {path}: {exc}") from exc
        if isinstance(value, dict):
            records.append(value)
    return records


def key_inventory(records: list[dict[str, Any]], field: str) -> list[dict[str, Any]]:
    counter: Counter[str] = Counter()
    for record in records:
        value = record.get(field)
        if isinstance(value, dict):
            counter.update(str(key) for key in value)
    return [{"key": key, "mission_count": count} for key, count in sorted(counter.items())]


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        json.dump(value, handle, ensure_ascii=False, indent=2, sort_keys=True)
        handle.write("\n")


def existing_source_timestamp(output: Path, source_sha256: str) -> str | None:
    path = output / "einsaetze.raw.json"
    if not path.exists():
        return None
    try:
        previous = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    if previous.get("source_sha256") != source_sha256:
        return None
    fetched_at = previous.get("fetched_at")
    return fetched_at if isinstance(fetched_at, str) and fetched_at else None


def coverage_report(official: list[dict[str, Any]], canonical: list[dict[str, Any]]) -> dict[str, Any]:
    official_by_id = {str(record["id"]): record for record in official}
    canonical_by_id = {str(record.get("id")): record for record in canonical if record.get("id") is not None}
    official_only_ids = sorted(set(official_by_id) - set(canonical_by_id), key=stable_id)
    canonical_only_ids = sorted(set(canonical_by_id) - set(official_by_id), key=stable_id)
    matched_ids = sorted(set(official_by_id) & set(canonical_by_id), key=stable_id)

    mismatched_names = []
    for mission_id in matched_ids:
        official_name = mission_name(official_by_id[mission_id])
        canonical_name = mission_name(canonical_by_id[mission_id])
        if official_name.casefold() != canonical_name.casefold():
            mismatched_names.append(
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
        "coverage_percent": round((len(matched_ids) / len(official) * 100), 2) if official else 0,
        "official_only": [
            {"id": official_by_id[mission_id].get("id"), "name": mission_name(official_by_id[mission_id])}
            for mission_id in official_only_ids
        ],
        "canonical_only": [
            {"id": canonical_by_id[mission_id].get("id"), "name": mission_name(canonical_by_id[mission_id])}
            for mission_id in canonical_only_ids
        ],
        "name_mismatches": mismatched_names,
    }


def main() -> int:
    args = parse_args()
    payload, source = read_payload(args)
    records = decode_records(payload)
    validate_records(records)
    records.sort(key=lambda record: stable_id(record.get("id")))

    canonical = load_canonical(args.canonical_dir)
    output = args.output_dir
    source_sha256 = hashlib.sha256(payload).hexdigest()
    fetched_at = existing_source_timestamp(output, source_sha256)
    if fetched_at is None:
        fetched_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")

    raw_document = {
        "source_url": args.url,
        "retrieved_from": source,
        "fetched_at": fetched_at,
        "source_sha256": source_sha256,
        "count": len(records),
        "records": records,
    }
    report = coverage_report(records, canonical)
    report.update(
        {
            "schema_version": "1",
            "generated_at": fetched_at,
            "source_url": args.url,
            "source_sha256": source_sha256,
        }
    )
    inventory = {
        "schema_version": "1",
        "generated_at": fetched_at,
        "source_sha256": source_sha256,
        "requirements": key_inventory(records, "requirements"),
        "chances": key_inventory(records, "chances"),
        "prerequisites": key_inventory(records, "prerequisites"),
    }

    write_json(output / "einsaetze.raw.json", raw_document)
    write_json(output / "mission-coverage.json", report)
    write_json(output / "official-key-inventory.json", inventory)

    print(
        f"Imported {len(records)} official UK missions; "
        f"{report['matched_count']} currently have canonical records and "
        f"{report['official_only_count']} require canonical review. "
        f"Source SHA-256: {source_sha256}."
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, RuntimeError) as exc:
        print(f"Official UK mission import failed: {exc}", file=sys.stderr)
        raise SystemExit(1)
