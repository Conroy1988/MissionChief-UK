#!/usr/bin/env python3

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SOURCE_ROOT = ROOT / "data" / "sources" / "missionchief-uk"
OUTPUT_ROOT = ROOT / "docs" / "assets" / "data" / "official"


def read_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        json.dump(value, handle, ensure_ascii=False, indent=2, sort_keys=True)
        handle.write("\n")


def stable_id(value: Any) -> tuple[int, int | str]:
    try:
        return (0, int(value))
    except (TypeError, ValueError):
        return (1, str(value))


def main() -> int:
    raw_document = read_json(SOURCE_ROOT / "einsaetze.raw.json")
    coverage = read_json(SOURCE_ROOT / "mission-coverage.json")
    records = raw_document.get("records", [])
    if not isinstance(records, list) or len(records) < 100:
        raise ValueError("Official UK mission catalogue is missing or implausibly small")

    public_records = []
    for record in records:
        if not isinstance(record, dict):
            raise ValueError("Official mission catalogue contains a non-object record")
        mission_id = record.get("id")
        if mission_id is None:
            raise ValueError("Official mission catalogue contains a record without an id")
        additional = record.get("additional") if isinstance(record.get("additional"), dict) else {}
        public_record = dict(record)
        public_record["official_url"] = f"https://www.missionchief.co.uk/einsaetze/{mission_id}"
        public_record["limited_availability"] = bool(additional.get("date_start") or additional.get("date_end"))
        public_record["availability"] = {
            "starts_at": additional.get("date_start"),
            "ends_at": additional.get("date_end"),
        }
        public_records.append(public_record)

    public_records.sort(key=lambda record: stable_id(record.get("id")))
    source = {
        "authority": "MissionChief UK",
        "url": raw_document.get("source_url"),
        "fetched_at": raw_document.get("fetched_at"),
        "sha256": raw_document.get("source_sha256"),
    }

    write_json(
        OUTPUT_ROOT / "uk-missions.json",
        {
            "schema_version": "1",
            "collection": "official-uk-missions",
            "source": source,
            "count": len(public_records),
            "records": public_records,
        },
    )
    write_json(
        OUTPUT_ROOT / "uk-mission-coverage.json",
        {
            "schema_version": "1",
            "collection": "official-uk-mission-coverage",
            **coverage,
        },
    )
    print(f"Published {len(public_records)} lossless official UK mission records at {OUTPUT_ROOT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
