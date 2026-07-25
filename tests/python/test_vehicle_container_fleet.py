from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
VEHICLE_ROOT = ROOT / "data" / "uk" / "vehicles"


def records():
    output = {}
    for path in VEHICLE_ROOT.glob("*.json"):
        document = json.loads(path.read_text(encoding="utf-8"))
        output[document["id"]] = document
    return output


class ContainerFleetTests(unittest.TestCase):
    def test_complete_official_container_fleet(self):
        data = records()
        expected = {
            "water_container": 17300,
            "bulk_foam_container": 17300,
            "rescue_container": 25500,
            "command_container": 25500,
            "welfare_container": 15000,
            "basu_container": 11680,
            "misting_container": 5000,
            "hazmat_container": 19200,
            "operational_support_unit_container": 30000,
            "high_volume_pump_container": 20000,
        }
        carrier = data["container_vehicle"]
        self.assertEqual(carrier["staffing"], {"minimum": 1, "maximum": 2})
        self.assertEqual(carrier["cost"], {"credits": 10000, "coins": 10})
        self.assertEqual(set(carrier["towing"]["can_tow"]), set(expected))
        for canonical_id, credits in expected.items():
            record = data[canonical_id]
            self.assertEqual(record["resource_class"], "container")
            self.assertEqual(record["cost"], {"credits": credits, "coins": 8})
            self.assertEqual(record["towing"], {"towable_by": ["container_vehicle"]})
            self.assertIn("Fire Station with Container Extension", record["building_requirements"])

    def test_container_extension_exists(self):
        extension = json.loads((ROOT / "data" / "uk" / "infrastructure" / "container-extension.json").read_text(encoding="utf-8"))
        self.assertEqual(extension["id"], "container_extension")
        self.assertIn("Fire Station", extension["parent_buildings"])
        self.assertIn("container_storage", extension["capabilities"])


if __name__ == "__main__":
    unittest.main()
