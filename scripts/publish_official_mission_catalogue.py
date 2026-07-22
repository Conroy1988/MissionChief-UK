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


def main() -> int:
    catalogue = read_json(SOURCE_ROOT / "official-missions.json")
    coverage = read_json(SOURCE_ROOT / "mission-coverage.json")
    records = catalogue.get("records", [])
    if not isinstance(records, list) or len(records) < 100:
        raise ValueError("Official UK mission catalogue is missing or implausibly small")

    public_records = []
    for record in records:
        if not isinstance(record, dict):
            raise ValueError("Official mission catalogue contains a non-object record")
        public_record = {key: value for key, value in record.items() if key != "raw"}
        public_records.append(public_record)

    write_json(
        OUTPUT_ROOT / "uk-missions.json",
        {
            "schema_version": "1",
            "collection": "official-uk-missions",
            "source": catalogue.get("source", {}),
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
    print(f"Published {len(public_records)} official UK mission catalogue records at {OUTPUT_ROOT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
