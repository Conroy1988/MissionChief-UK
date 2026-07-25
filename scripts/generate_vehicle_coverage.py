#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from vehicle_inventory import (
    INVENTORY_PATH,
    ROOT,
    VEHICLE_ROOT,
    VehicleInventoryError,
    build_vehicle_coverage,
    load_canonical_vehicles,
    load_inventory,
)

SOURCE_OUTPUT = ROOT / "data" / "sources" / "missionchief-uk" / "vehicle-coverage.json"
PUBLIC_OUTPUT = ROOT / "docs" / "assets" / "data" / "official" / "uk-vehicle-coverage.json"
MARKDOWN_OUTPUT = ROOT / "docs" / "reference" / "vehicle-coverage-status.md"


def json_text(report: dict[str, Any]) -> str:
    return json.dumps(report, ensure_ascii=False, indent=2) + "\n"


def markdown_text(report: dict[str, Any]) -> str:
    summary = report["summary"]
    field_rows = "\n".join(
        f"| {field.replace('_', ' ').title()} | {values['complete']:,} / {values['total']:,} | {values['percent']:.2f}% |"
        for field, values in report["field_completeness"].items()
    )
    resolution = report["field_resolution"]
    resolution_rows = "\n".join(
        f"| {field.replace('_', ' ').title()} | {values['resolved']:,} / {values['total']:,} | {values['percent']:.2f}% |"
        for field, values in report["field_resolution_by_field"].items()
    )
    unresolved_rows = "\n".join(
        f"| {record['game_vehicle_type_id']} | {record['name']} | {record['service']} | {record['resource_class']} | {record['label_status']} |"
        for record in report["unresolved_inventory"]
    ) or "| — | None | — | — | — |"
    canonical_rows = "\n".join(
        f"| `{record['canonical_id']}` | {record['name']} | {record['service']} |"
        for record in report["canonical_without_inventory"]
    ) or "| — | None | — |"

    return f"""# UK Vehicle Coverage Status

This report is generated from the Stage 36A vehicle source ledger and the canonical files under `data/uk/vehicles/`.

The source ledger is deliberately evidence-tiered. Community-observed game vehicle type IDs are discovery evidence, not official verification. Exact labels, prices, staffing and market restrictions are promoted only when reproduced from the current UK game or published by the official Help Centre.

## Coverage summary

| Metric | Value |
|---|---:|
| Source-ledger entries | **{summary['inventory_entries']:,}** |
| Canonical deployable-resource records | **{summary['canonical_records']:,}** |
| Ledger entries mapped to canonical records | **{summary['mapped_inventory_entries']:,}** |
| Ledger entries awaiting canonical mapping | **{summary['unresolved_inventory_entries']:,}** |
| Canonical records without a ledger entry | **{summary['canonical_records_without_inventory_entry']:,}** |
| Dangling canonical mappings | **{summary['dangling_canonical_mappings']:,}** |
| Identity coverage | **{summary['identity_coverage_percent']:.2f}%** |
| Verified labels | **{summary['verified_labels']:,}** |
| Community-candidate type IDs | **{summary['candidate_type_ids']:,}** |

**Programme status:** `{report['status']}`

## Canonical field completeness

| Field | Complete | Coverage |
|---|---:|---:|
{field_rows}

An omitted value is unknown, not zero. Field completeness is reported separately from identity coverage so partial records cannot be mistaken for complete economics or staffing data.

## Field decision coverage

| Metric | Value |
|---|---:|
| Resolved field decisions | **{resolution['resolved_decisions']:,} / {resolution['total_decisions']:,}** |
| Unresolved field decisions | **{resolution['unresolved_decisions']:,}** |
| Decision coverage | **{resolution['resolution_percent']:.2f}%** |

| Field | Resolved | Coverage |
|---|---:|---:|
{resolution_rows}

Decision coverage distinguishes documented values, fields that are not applicable, and values that are not published by a reproducible current UK source. It does not convert unknown values into zeroes or guesses.

## Source-ledger entries awaiting canonical mapping

| Game type ID | Observed UK label | Service | Class | Label evidence |
|---:|---|---|---|---|
{unresolved_rows}

## Canonical records awaiting source-ledger mapping

| Canonical ID | UK label | Service |
|---|---|---|
{canonical_rows}

## Evidence policy

- Official MissionChief UK pages and the official Help Centre are primary evidence.
- Current authenticated vehicle-market observations may verify IDs, costs, staffing, training and compatibility.
- Community userscripts may identify candidates and type IDs, but cannot independently verify market values.
- Values are never inferred from another locale or treated as zero when unavailable.
"""


def write_or_check(path: Path, content: str, check: bool) -> bool:
    if check:
        try:
            current = path.read_text(encoding="utf-8")
        except FileNotFoundError:
            print(f"Missing generated vehicle coverage output: {path.relative_to(ROOT)}", file=sys.stderr)
            return False
        if current != content:
            print(f"Stale generated vehicle coverage output: {path.relative_to(ROOT)}", file=sys.stderr)
            return False
        return True

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate UK vehicle identity and enrichment coverage reports.")
    parser.add_argument("--check", action="store_true", help="Fail when committed outputs differ from deterministic generation.")
    args = parser.parse_args()

    try:
        inventory_document, inventory_records = load_inventory(INVENTORY_PATH)
        canonical_records = load_canonical_vehicles(VEHICLE_ROOT)
        report = build_vehicle_coverage(inventory_document, inventory_records, canonical_records)
    except VehicleInventoryError as exc:
        print(f"Vehicle coverage generation failed: {exc}", file=sys.stderr)
        return 1

    payload = json_text(report)
    checks = (
        write_or_check(SOURCE_OUTPUT, payload, args.check),
        write_or_check(PUBLIC_OUTPUT, payload, args.check),
        write_or_check(MARKDOWN_OUTPUT, markdown_text(report), args.check),
    )
    if not all(checks):
        return 1

    summary = report["summary"]
    print(
        "Vehicle coverage generated: "
        f"{summary['mapped_inventory_entries']}/{summary['inventory_entries']} ledger entries mapped, "
        f"{summary['canonical_records']} canonical records, "
        f"{summary['unresolved_inventory_entries']} unresolved identities."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
