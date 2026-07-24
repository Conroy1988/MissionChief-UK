#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from collections import Counter
from datetime import date
from pathlib import Path
from typing import Any, Iterable

ROOT = Path(__file__).resolve().parents[1]
INVENTORY_PATH = ROOT / "data" / "sources" / "missionchief-uk" / "vehicle-type-inventory.json"
VEHICLE_ROOT = ROOT / "data" / "uk" / "vehicles"

ALLOWED_LABEL_STATUSES = {"verified", "candidate", "review-required"}
ALLOWED_TYPE_ID_STATUSES = {"verified", "community-candidate", "review-required"}
ALLOWED_RESOURCE_CLASSES = {"vehicle", "aircraft", "vessel", "trailer", "container", "equipment"}


class VehicleInventoryError(ValueError):
    pass


def read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise VehicleInventoryError(f"Required file is missing: {path}") from exc
    except json.JSONDecodeError as exc:
        raise VehicleInventoryError(f"Invalid JSON in {path}: {exc}") from exc


def require(condition: bool, message: str) -> None:
    if not condition:
        raise VehicleInventoryError(message)


def stable_record_key(record: dict[str, Any]) -> tuple[int, str]:
    value = record.get("game_vehicle_type_id")
    numeric = value if isinstance(value, int) else 10**9
    return (numeric, str(record.get("name", "")).casefold())


def normalise_label(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", value.casefold()).strip()


def validate_inventory_document(document: Any) -> list[dict[str, Any]]:
    require(isinstance(document, dict), "Vehicle source ledger must be an object")
    require(document.get("schema_version") == "1", "Vehicle source ledger schema_version must be '1'")
    require(document.get("collection") == "uk-vehicle-source-ledger", "Vehicle source ledger collection is invalid")
    updated_at = document.get("updated_at")
    require(isinstance(updated_at, str), "Vehicle source ledger updated_at must be an ISO date")
    try:
        date.fromisoformat(updated_at)
    except ValueError as exc:
        raise VehicleInventoryError("Vehicle source ledger updated_at must be an ISO date") from exc

    source_map = document.get("sources")
    require(isinstance(source_map, dict) and source_map, "Vehicle source ledger sources must be a non-empty object")
    require(
        all(isinstance(key, str) and key and isinstance(value, str) and value for key, value in source_map.items()),
        "Vehicle source ledger sources must map non-empty keys to non-empty URLs",
    )

    columns = document.get("columns")
    required_columns = [
        "game_vehicle_type_id",
        "name",
        "canonical_id",
        "service",
        "resource_class",
        "label_status",
        "source_keys",
        "notes",
    ]
    require(columns == required_columns, f"Vehicle source ledger columns must be {required_columns}")

    raw_records = document.get("records")
    require(isinstance(raw_records, list) and raw_records, "Vehicle source ledger records must be a non-empty array")

    records: list[dict[str, Any]] = []
    type_ids: set[int] = set()
    canonical_ids: set[str] = set()
    for index, row in enumerate(raw_records):
        label = f"Vehicle source ledger record {index + 1}"
        require(isinstance(row, list) and len(row) == len(columns), f"{label} must match the declared columns")
        record = dict(zip(columns, row, strict=True))
        type_id = record["game_vehicle_type_id"]
        require(isinstance(type_id, int) and type_id >= 0, f"{label} game_vehicle_type_id must be a non-negative integer")
        require(type_id not in type_ids, f"Duplicate game vehicle type ID {type_id}")
        type_ids.add(type_id)

        name = record["name"]
        require(isinstance(name, str) and name.strip(), f"{label} name must be a non-empty string")
        service = record["service"]
        require(isinstance(service, str) and service.strip(), f"{label} service must be a non-empty string")
        require(record["resource_class"] in ALLOWED_RESOURCE_CLASSES, f"{label} resource_class is invalid")

        canonical_id = record["canonical_id"]
        require(canonical_id is None or (isinstance(canonical_id, str) and canonical_id.strip()), f"{label} canonical_id must be null or a non-empty string")
        if canonical_id is not None:
            require(canonical_id not in canonical_ids, f"Duplicate canonical mapping {canonical_id}")
            canonical_ids.add(canonical_id)

        require(record["label_status"] in ALLOWED_LABEL_STATUSES, f"{label} label_status is invalid")
        source_keys = record["source_keys"]
        require(isinstance(source_keys, list) and source_keys, f"{label} source_keys must be a non-empty array")
        require(all(isinstance(source_key, str) and source_key in source_map for source_key in source_keys), f"{label} references an unknown source key")
        notes = record["notes"]
        require(isinstance(notes, list) and all(isinstance(note, str) for note in notes), f"{label} notes must be an array of strings")

        record["type_id_status"] = document.get("type_id_status_default")
        require(record["type_id_status"] in ALLOWED_TYPE_ID_STATUSES, f"{label} type_id_status is invalid")
        record["sources"] = [source_map[key] for key in source_keys]
        records.append(record)

    return sorted(records, key=stable_record_key)

def load_inventory(path: Path = INVENTORY_PATH) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    document = read_json(path)
    return document, validate_inventory_document(document)


def load_canonical_vehicles(root: Path = VEHICLE_ROOT) -> dict[str, dict[str, Any]]:
    require(root.is_dir(), f"Canonical vehicle directory is missing: {root}")
    records: dict[str, dict[str, Any]] = {}
    for path in sorted(root.glob("*.json")):
        document = read_json(path)
        require(isinstance(document, dict), f"{path}: vehicle record must be an object")
        canonical_id = document.get("id")
        require(isinstance(canonical_id, str) and canonical_id, f"{path}: canonical vehicle id must be a non-empty string")
        require(canonical_id not in records, f"Duplicate canonical vehicle id {canonical_id}")
        records[canonical_id] = document
    require(bool(records), "Canonical vehicle directory contains no records")
    return records


def count_present(records: Iterable[dict[str, Any]], field: str, *, nonempty: bool = False) -> int:
    total = 0
    for record in records:
        if field not in record:
            continue
        value = record[field]
        if nonempty and value in (None, "", [], {}):
            continue
        total += 1
    return total


def build_vehicle_coverage(
    inventory_document: dict[str, Any],
    inventory_records: list[dict[str, Any]],
    canonical_records: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    canonical_ids = set(canonical_records)
    mapped_entries = [record for record in inventory_records if record.get("canonical_id")]
    mapped_ids = {str(record["canonical_id"]) for record in mapped_entries}
    unresolved = [record for record in inventory_records if not record.get("canonical_id")]
    dangling = [record for record in mapped_entries if record["canonical_id"] not in canonical_ids]
    canonical_only = [canonical_records[canonical_id] for canonical_id in sorted(canonical_ids - mapped_ids)]

    canonical_values = list(canonical_records.values())
    field_counts = {
        "cost": count_present(canonical_values, "cost", nonempty=True),
        "staffing": count_present(canonical_values, "staffing", nonempty=True),
        "training": count_present(canonical_values, "training", nonempty=True),
        "building_requirements": count_present(canonical_values, "building_requirements", nonempty=True),
        "deployment": count_present(canonical_values, "deployment", nonempty=True),
        "capabilities": count_present(canonical_values, "capabilities", nonempty=True),
        "verification_sources": sum(
            1
            for record in canonical_values
            if isinstance(record.get("verification"), dict)
            and bool(record["verification"].get("sources"))
        ),
    }
    canonical_total = len(canonical_values)
    field_completeness = {
        key: {
            "complete": count,
            "total": canonical_total,
            "percent": round((count / canonical_total) * 100, 2) if canonical_total else 0.0,
        }
        for key, count in field_counts.items()
    }

    inventory_count = len(inventory_records)
    mapped_count = len(mapped_entries) - len(dangling)
    summary = {
        "inventory_entries": inventory_count,
        "canonical_records": len(canonical_records),
        "mapped_inventory_entries": mapped_count,
        "unresolved_inventory_entries": len(unresolved),
        "dangling_canonical_mappings": len(dangling),
        "canonical_records_without_inventory_entry": len(canonical_only),
        "identity_coverage_percent": round((mapped_count / inventory_count) * 100, 2),
        "verified_labels": sum(1 for record in inventory_records if record["label_status"] == "verified"),
        "candidate_labels": sum(1 for record in inventory_records if record["label_status"] == "candidate"),
        "verified_type_ids": sum(
            1
            for record in inventory_records
            if record.get("type_id_status", inventory_document.get("type_id_status_default")) == "verified"
        ),
        "candidate_type_ids": sum(
            1
            for record in inventory_records
            if record.get("type_id_status", inventory_document.get("type_id_status_default")) == "community-candidate"
        ),
    }

    return {
        "schema_version": "1",
        "collection": "uk-vehicle-coverage",
        "source_updated_at": inventory_document["updated_at"],
        "status": "complete"
        if not unresolved and not dangling and not canonical_only
        else "in-progress",
        "summary": summary,
        "field_completeness": field_completeness,
        "service_inventory_counts": dict(sorted(Counter(record["service"] for record in inventory_records).items())),
        "resource_class_counts": dict(sorted(Counter(record["resource_class"] for record in inventory_records).items())),
        "unresolved_inventory": [
            {
                "game_vehicle_type_id": record["game_vehicle_type_id"],
                "name": record["name"],
                "service": record["service"],
                "resource_class": record["resource_class"],
                "label_status": record["label_status"],
                "type_id_status": record.get("type_id_status", inventory_document.get("type_id_status_default")),
                "sources": record.get(
                    "sources",
                    [inventory_document["sources"][key] for key in record.get("source_keys", [])],
                ),
                "notes": record.get("notes", []),
            }
            for record in unresolved
        ],
        "dangling_mappings": [
            {
                "game_vehicle_type_id": record["game_vehicle_type_id"],
                "name": record["name"],
                "canonical_id": record["canonical_id"],
            }
            for record in dangling
        ],
        "canonical_without_inventory": [
            {
                "canonical_id": record["id"],
                "name": record["name"],
                "service": record["service"],
            }
            for record in canonical_only
        ],
    }
