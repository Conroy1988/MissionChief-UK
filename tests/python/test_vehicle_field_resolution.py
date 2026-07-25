#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

import generate_vehicle_field_resolution as resolution  # noqa: E402


class VehicleFieldResolutionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.document = resolution.build_document()

    def test_every_resource_and_field_has_a_resolution(self) -> None:
        vehicle_count = len(list((ROOT / "data" / "uk" / "vehicles").glob("*.json")))
        summary = self.document["summary"]
        self.assertEqual(summary["canonical_records"], vehicle_count)
        self.assertEqual(summary["tracked_fields"], len(resolution.TRACKED_FIELDS))
        self.assertEqual(summary["resolved_decisions"], summary["total_decisions"])
        self.assertEqual(summary["unresolved_decisions"], 0)
        self.assertEqual(summary["resolution_percent"], 100.0)
        self.assertEqual(self.document["status"], "complete")

        for record in self.document["records"]:
            self.assertEqual(set(record["decisions"]), set(resolution.TRACKED_FIELDS))
            for decision in record["decisions"].values():
                self.assertIn(decision["status"], resolution.ALLOWED_STATUSES)
                self.assertTrue(decision["reason"])

    def test_generated_registry_is_current(self) -> None:
        committed = json.loads(
            (ROOT / "data" / "uk" / "vehicle-field-resolution.json").read_text(encoding="utf-8")
        )
        self.assertEqual(committed, self.document)

    def test_water_ladder_with_cafs_is_officially_documented(self) -> None:
        record = json.loads(
            (ROOT / "data" / "uk" / "vehicles" / "water-ladder-with-cafs.json").read_text(encoding="utf-8")
        )
        self.assertEqual(record["cost"], {"credits": 17300, "coins": 10})
        self.assertEqual(record["staffing"], {"minimum": 2, "maximum": 9})
        self.assertIn("Fire Station with Fire Support", record["building_requirements"])
        self.assertEqual(record["verification"]["status"], "verified")


if __name__ == "__main__":
    unittest.main()
