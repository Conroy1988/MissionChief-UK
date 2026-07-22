#!/usr/bin/env python3

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DATA_ROOT = ROOT / "data" / "uk"
OUTPUT_ROOT = ROOT / "docs" / "assets" / "data" / "v1"
VERSION_FILE = ROOT / "data" / "version.json"

COLLECTIONS = {
    "missions": DATA_ROOT / "missions",
    "vehicles": DATA_ROOT / "vehicles",
    "infrastructure": DATA_ROOT / "infrastructure",
    "training": DATA_ROOT / "training",
}


def read_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        json.dump(value, handle, ensure_ascii=False, indent=2, sort_keys=True)
        handle.write("\n")


def stable_id(record: dict[str, Any]) -> tuple[str, str]:
    return (str(record.get("id", "")), str(record.get("name", "")))


def load_collection(directory: Path) -> list[dict[str, Any]]:
    if not directory.exists():
        return []
    records = [read_json(path) for path in sorted(directory.glob("*.json"))]
    return sorted((record for record in records if isinstance(record, dict)), key=stable_id)


def searchable_text(record: dict[str, Any]) -> str:
    terms: list[str] = []
    for key in ("id", "name", "service", "category"):
        value = record.get(key)
        if value is not None:
            terms.append(str(value))
    for key in ("aliases", "mission_types", "poi", "capabilities", "training", "roles"):
        value = record.get(key, [])
        if isinstance(value, list):
            terms.extend(str(item) for item in value)
    return " ".join(terms).lower()


def main() -> int:
    release = read_json(VERSION_FILE)
    version = release["version"]
    released_at = release["released_at"]

    manifest_collections: dict[str, dict[str, Any]] = {}
    search_records: list[dict[str, Any]] = []

    for name, directory in COLLECTIONS.items():
        records = load_collection(directory)
        payload = {
            "schema_version": "1",
            "data_version": version,
            "released_at": released_at,
            "collection": name,
            "count": len(records),
            "records": records,
        }
        write_json(OUTPUT_ROOT / f"{name}.json", payload)
        manifest_collections[name] = {
            "count": len(records),
            "path": f"{name}.json",
        }
        for record in records:
            search_records.append(
                {
                    "collection": name,
                    "id": record.get("id"),
                    "name": record.get("name"),
                    "service": record.get("service"),
                    "search_text": searchable_text(record),
                }
            )

    search_records.sort(key=lambda item: (str(item["collection"]), str(item["id"])))
    write_json(
        OUTPUT_ROOT / "search-index.json",
        {
            "schema_version": "1",
            "data_version": version,
            "released_at": released_at,
            "count": len(search_records),
            "records": search_records,
        },
    )

    manifest = {
        "api_version": "v1",
        "data_version": version,
        "released_at": released_at,
        "stage": release["stage"],
        "status": release["status"],
        "collections": manifest_collections,
        "search_index": {
            "count": len(search_records),
            "path": "search-index.json",
        },
    }
    write_json(OUTPUT_ROOT / "manifest.json", manifest)
    print(f"Generated {len(manifest_collections)} collection exports and one search index at {OUTPUT_ROOT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
