#!/usr/bin/env python3

from __future__ import annotations

import json
from datetime import date
from pathlib import Path
from typing import Any


def _read_json(path: Path, root: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"{path.relative_to(root)}: unable to read JSON: {exc}") from exc


def _iso_date(value: Any, label: str) -> str:
    if not isinstance(value, str):
        raise ValueError(f"{label} must be an ISO date")
    try:
        date.fromisoformat(value)
    except ValueError as exc:
        raise ValueError(f"{label} must be an ISO date") from exc
    return value


def load_verification_registry(root: Path, base_path: Path, batch_root: Path) -> dict[str, Any]:
    base = _read_json(base_path, root)
    if not isinstance(base, dict):
        raise ValueError("Mission verification registry must be an object")
    if base.get("schema_version") != "1":
        raise ValueError("Mission verification registry schema_version must be '1'")
    _iso_date(base.get("updated_at"), "Mission verification registry updated_at")
    base_records = base.get("records")
    if not isinstance(base_records, dict):
        raise ValueError("Mission verification registry records must be an object")

    merged = dict(base)
    merged_records = dict(base_records)
    newest = str(base["updated_at"])
    source_files = [base_path.relative_to(root).as_posix()]

    if batch_root.exists():
        for path in sorted(batch_root.glob("*.json")):
            batch = _read_json(path, root)
            label = path.relative_to(root).as_posix()
            if not isinstance(batch, dict) or batch.get("schema_version") != "1":
                raise ValueError(f"{label}: schema_version must be '1'")
            updated_at = _iso_date(batch.get("updated_at"), f"{label} updated_at")
            records = batch.get("records")
            if not isinstance(records, dict) or not records:
                raise ValueError(f"{label}: records must be a non-empty object")
            for mission_id, decision in records.items():
                key = str(mission_id)
                if key in merged_records:
                    raise ValueError(f"Duplicate mission verification decision {key} in {label}")
                merged_records[key] = decision
            newest = max(newest, updated_at)
            source_files.append(label)

    merged["updated_at"] = newest
    merged["records"] = merged_records
    merged["source_files"] = source_files
    return merged
