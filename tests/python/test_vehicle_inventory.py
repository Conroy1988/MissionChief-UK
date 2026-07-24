from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

from vehicle_inventory import (  # noqa: E402
    VehicleInventoryError,
    build_vehicle_coverage,
    load_canonical_vehicles,
    load_inventory,
    validate_inventory_document,
)


def inventory_record(type_id: int, name: str, canonical_id: str | None) -> list:
    return [type_id, name, canonical_id, "fire", "vehicle", "candidate", ["example"], []]



class VehicleInventoryTests(unittest.TestCase):
    def document(self, records: list[dict]) -> dict:
        return {
            "schema_version": "1",
            "collection": "uk-vehicle-source-ledger",
            "updated_at": "2026-07-24",
            "type_id_status_default": "community-candidate",
            "sources": {"example": "https://example.test/source"},
            "columns": [
                "game_vehicle_type_id",
                "name",
                "canonical_id",
                "service",
                "resource_class",
                "label_status",
                "source_keys",
                "notes",
            ],
            "records": records,
        }

    def test_duplicate_type_ids_are_rejected(self) -> None:
        document = self.document(
            [
                inventory_record(1, "One", "one"),
                inventory_record(1, "Two", "two"),
            ]
        )
        with self.assertRaisesRegex(VehicleInventoryError, "Duplicate game vehicle type ID"):
            validate_inventory_document(document)

    def test_duplicate_canonical_mappings_are_rejected(self) -> None:
        document = self.document(
            [
                inventory_record(1, "One", "shared"),
                inventory_record(2, "Two", "shared"),
            ]
        )
        with self.assertRaisesRegex(VehicleInventoryError, "Duplicate canonical mapping"):
            validate_inventory_document(document)

    def test_report_separates_identity_and_field_completeness(self) -> None:
        document = self.document(
            [
                inventory_record(1, "Mapped", "mapped"),
                inventory_record(2, "Unresolved", None),
            ]
        )
        records = validate_inventory_document(document)
        canonical = {
            "mapped": {
                "id": "mapped",
                "name": "Mapped",
                "service": "fire",
                "cost": {"credits": 1000},
                "verification": {"status": "verified", "checked_at": "2026-07-24", "sources": ["https://example.test"]},
            },
            "canonical_only": {
                "id": "canonical_only",
                "name": "Canonical only",
                "service": "police",
                "verification": {"status": "verified", "checked_at": "2026-07-24", "sources": ["https://example.test"]},
            },
        }

        report = build_vehicle_coverage(document, records, canonical)

        self.assertEqual(report["status"], "in-progress")
        self.assertEqual(report["summary"]["mapped_inventory_entries"], 1)
        self.assertEqual(report["summary"]["unresolved_inventory_entries"], 1)
        self.assertEqual(report["summary"]["canonical_records_without_inventory_entry"], 1)
        self.assertEqual(report["field_completeness"]["cost"]["complete"], 1)
        self.assertEqual(report["field_completeness"]["staffing"]["complete"], 0)
        self.assertEqual(report["field_completeness"]["transport_capacity"]["complete"], 0)

    def test_dangling_mapping_is_reported(self) -> None:
        document = self.document([inventory_record(1, "Missing", "not_present")])
        records = validate_inventory_document(document)
        report = build_vehicle_coverage(document, records, {})
        self.assertEqual(report["summary"]["dangling_canonical_mappings"], 1)

    def test_loaders_read_realistic_files(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            inventory_path = root / "inventory.json"
            vehicle_root = root / "vehicles"
            vehicle_root.mkdir()
            inventory_path.write_text(
                json.dumps(self.document([inventory_record(1, "Mapped", "mapped")])),
                encoding="utf-8",
            )
            (vehicle_root / "mapped.json").write_text(
                json.dumps(
                    {
                        "id": "mapped",
                        "name": "Mapped",
                        "service": "fire",
                        "verification": {"status": "verified", "checked_at": "2026-07-24"},
                    }
                ),
                encoding="utf-8",
            )

            document, records = load_inventory(inventory_path)
            vehicles = load_canonical_vehicles(vehicle_root)

            self.assertEqual(document["collection"], "uk-vehicle-source-ledger")
            self.assertEqual(records[0]["game_vehicle_type_id"], 1)
            self.assertIn("mapped", vehicles)


if __name__ == "__main__":
    unittest.main()
