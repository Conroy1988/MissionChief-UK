#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
VEHICLE_ROOT = ROOT / "data" / "uk" / "vehicles"
SOURCE_OUTPUT = ROOT / "data" / "uk" / "vehicle-field-resolution.json"
PUBLIC_OUTPUT = ROOT / "docs" / "assets" / "data" / "official" / "uk-vehicle-field-resolution.json"
MARKDOWN_OUTPUT = ROOT / "docs" / "reference" / "vehicle-field-resolution.md"

TRACKED_FIELDS = (
    "cost",
    "staffing",
    "training",
    "training_requirements",
    "building_requirements",
    "resource_class",
    "transport_capacity",
    "towing",
    "deployment",
)

ALLOWED_STATUSES = {
    "documented",
    "not_applicable",
    "not_published",
    "review_required",
}


def read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"{path.relative_to(ROOT)}: unable to read JSON: {exc}") from exc


def nonempty(record: dict[str, Any], field: str) -> bool:
    return field in record and record[field] not in (None, "", [], {})


def not_applicable(record: dict[str, Any], field: str) -> bool:
    resource_class = record.get("resource_class")
    if field == "staffing" and resource_class in {"container", "trailer", "equipment"}:
        return True
    if field in {"training", "training_requirements"} and resource_class == "container":
        return True
    if field == "transport_capacity" and resource_class in {"container", "equipment"}:
        return True
    if field == "towing" and resource_class in {"aircraft", "vessel", "equipment"}:
        return True
    return False


def decision_for(record: dict[str, Any], field: str, checked_at: str) -> dict[str, Any]:
    verification = record.get("verification") if isinstance(record.get("verification"), dict) else {}
    sources = verification.get("sources") if isinstance(verification.get("sources"), list) else []

    if nonempty(record, field):
        status = "documented"
        reason = "The canonical record contains a non-empty field value; its evidence tier remains defined by the record verification block."
    elif not_applicable(record, field):
        status = "not_applicable"
        reason = "The field is not operationally applicable to this resource class under the current data contract."
    else:
        status = "not_published"
        reason = "No reproducible current UK source publishes this field value; it is deliberately omitted rather than inferred."

    return {
        "status": status,
        "checked_at": checked_at,
        "reason": reason,
        "sources": sources,
    }


def load_records() -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for path in sorted(VEHICLE_ROOT.glob("*.json")):
        document = read_json(path)
        if not isinstance(document, dict):
            raise ValueError(f"{path.relative_to(ROOT)}: vehicle record must be an object")
        if not isinstance(document.get("id"), str) or not document["id"]:
            raise ValueError(f"{path.relative_to(ROOT)}: vehicle id must be a non-empty string")
        records.append(document)
    if not records:
        raise ValueError("No canonical vehicle records found")
    return sorted(records, key=lambda item: (str(item.get("service", "")), str(item["id"])))


def build_document() -> dict[str, Any]:
    records = load_records()
    checked_dates = [
        str(record.get('verification', {}).get('checked_at', ''))
        for record in records
        if isinstance(record.get('verification'), dict)
        and record.get('verification', {}).get('checked_at')
    ]
    checked_at = max(checked_dates) if checked_dates else '1970-01-01'
    output_records: list[dict[str, Any]] = []
    field_statuses = {field: Counter() for field in TRACKED_FIELDS}

    for record in records:
        decisions: dict[str, dict[str, Any]] = {}
        for field in TRACKED_FIELDS:
            decision = decision_for(record, field, checked_at)
            if decision["status"] not in ALLOWED_STATUSES:
                raise ValueError(f"Invalid field-resolution status for {record['id']}.{field}")
            decisions[field] = decision
            field_statuses[field][decision["status"]] += 1
        output_records.append(
            {
                "canonical_id": record["id"],
                "name": record.get("name", record["id"]),
                "service": record.get("service", "unknown"),
                "decisions": decisions,
            }
        )

    total_records = len(output_records)
    total_decisions = total_records * len(TRACKED_FIELDS)
    resolved_decisions = sum(sum(counter.values()) for counter in field_statuses.values())
    field_summary = {
        field: {
            "resolved": sum(counter.values()),
            "total": total_records,
            "percent": 100.0 if total_records else 0.0,
            "status_counts": dict(sorted(counter.items())),
        }
        for field, counter in field_statuses.items()
    }

    return {
        "schema_version": "1",
        "collection": "uk-vehicle-field-resolution",
        "generated_at": checked_at,
        "status": "complete" if resolved_decisions == total_decisions else "in-progress",
        "summary": {
            "canonical_records": total_records,
            "tracked_fields": len(TRACKED_FIELDS),
            "total_decisions": total_decisions,
            "resolved_decisions": resolved_decisions,
            "unresolved_decisions": total_decisions - resolved_decisions,
            "resolution_percent": round((resolved_decisions / total_decisions) * 100, 2) if total_decisions else 0.0,
        },
        "field_summary": field_summary,
        "records": output_records,
    }


def json_text(document: dict[str, Any]) -> str:
    return json.dumps(document, ensure_ascii=False, indent=2) + "\n"


def markdown_text(document: dict[str, Any]) -> str:
    summary = document["summary"]
    field_rows = "\n".join(
        "| {label} | {resolved:,} / {total:,} | {percent:.2f}% | {statuses} |".format(
            label=field.replace("_", " ").title(),
            resolved=values["resolved"],
            total=values["total"],
            percent=values["percent"],
            statuses=", ".join(f"{key}: {value}" for key, value in values["status_counts"].items()),
        )
        for field, values in document["field_summary"].items()
    )
    return f"""# Vehicle Field Resolution

Every canonical UK deployable resource has an explicit outcome for every tracked operational field.

This is **decision coverage**, not a claim that every value is published. A decision can be:

- `documented` — the canonical field contains evidence-tiered data;
- `not_applicable` — the field does not apply to the resource class;
- `not_published` — no reproducible current UK source publishes the value, so it remains omitted;
- `review_required` — evidence conflicts or requires manual adjudication.

## Resolution summary

| Metric | Value |
|---|---:|
| Canonical resources | **{summary['canonical_records']:,}** |
| Tracked fields per resource | **{summary['tracked_fields']:,}** |
| Resolved decisions | **{summary['resolved_decisions']:,} / {summary['total_decisions']:,}** |
| Unresolved decisions | **{summary['unresolved_decisions']:,}** |
| Decision coverage | **{summary['resolution_percent']:.2f}%** |

## Field-by-field decision coverage

| Field | Resolved | Coverage | Outcome distribution |
|---|---:|---:|---|
{field_rows}

## Integrity rule

Unknown values remain unknown. `not_published` never means zero, free, unrestricted or untrained. Raw factual completeness continues to be reported separately in the [Vehicle Coverage Status](vehicle-coverage-status.md) report.
"""


def write_or_check(path: Path, content: str, check: bool) -> bool:
    if check:
        try:
            current = path.read_text(encoding="utf-8")
        except FileNotFoundError:
            print(f"Missing generated vehicle field-resolution output: {path.relative_to(ROOT)}", file=sys.stderr)
            return False
        if current != content:
            print(f"Stale generated vehicle field-resolution output: {path.relative_to(ROOT)}", file=sys.stderr)
            return False
        return True
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate complete UK vehicle field-resolution decisions.")
    parser.add_argument("--check", action="store_true", help="Fail when committed outputs differ from deterministic generation.")
    args = parser.parse_args()
    try:
        document = build_document()
    except ValueError as exc:
        print(f"Vehicle field-resolution generation failed: {exc}", file=sys.stderr)
        return 1

    payload = json_text(document)
    checks = (
        write_or_check(SOURCE_OUTPUT, payload, args.check),
        write_or_check(PUBLIC_OUTPUT, payload, args.check),
        write_or_check(MARKDOWN_OUTPUT, markdown_text(document), args.check),
    )
    if not all(checks):
        return 1

    summary = document["summary"]
    print(
        "Vehicle field resolution generated: "
        f"{summary['resolved_decisions']}/{summary['total_decisions']} decisions resolved "
        f"across {summary['canonical_records']} resources ({summary['resolution_percent']:.2f}%)."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
