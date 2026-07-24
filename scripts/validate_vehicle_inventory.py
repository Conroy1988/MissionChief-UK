#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys

from vehicle_inventory import (
    INVENTORY_PATH,
    VEHICLE_ROOT,
    VehicleInventoryError,
    build_vehicle_coverage,
    load_canonical_vehicles,
    load_inventory,
)


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate the UK vehicle source ledger and canonical identity mappings.")
    parser.add_argument(
        "--require-complete",
        action="store_true",
        help="Require every source-ledger and canonical record to be mapped. Intended for Stage 36A completion.",
    )
    args = parser.parse_args()

    try:
        inventory_document, inventory_records = load_inventory(INVENTORY_PATH)
        canonical_records = load_canonical_vehicles(VEHICLE_ROOT)
        report = build_vehicle_coverage(inventory_document, inventory_records, canonical_records)
    except VehicleInventoryError as exc:
        print(f"Vehicle inventory validation failed: {exc}", file=sys.stderr)
        return 1

    summary = report["summary"]
    if summary["dangling_canonical_mappings"]:
        print("Vehicle inventory validation failed: dangling canonical mappings exist.", file=sys.stderr)
        return 1

    if args.require_complete and report["status"] != "complete":
        print(
            "Vehicle inventory is not complete: "
            f"{summary['unresolved_inventory_entries']} unresolved ledger entries and "
            f"{summary['canonical_records_without_inventory_entry']} canonical-only records.",
            file=sys.stderr,
        )
        return 1

    print(
        "Vehicle inventory validation passed: "
        f"{summary['inventory_entries']} source-ledger entries, "
        f"{summary['mapped_inventory_entries']} mapped, "
        f"{summary['canonical_records']} canonical records."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
