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


class OfficialVehicleEnrichmentTests(unittest.TestCase):
    def test_search_and_rescue_contracts(self):
        data = records()
        self.assertEqual(data["coastguard_rescue_helicopter"]["transport_capacity"]["patients"], 16)
        self.assertEqual(data["inshore_lifeboat"]["transport_capacity"], {"patients": 3, "prisoners": 2})
        self.assertEqual(data["all_weather_lifeboat"]["transport_capacity"], {"patients": 6, "prisoners": 4})
        self.assertIn("flood_rescue_unit_trailer", data["coastguard_rescue_vehicle"]["towing"]["can_tow"])
        self.assertEqual(data["hovercraft_trailer"]["towing"]["towable_by"], ["hovercraft_transporter"])

    def test_foam_and_drone_contracts(self):
        data = records()
        self.assertEqual(data["bulk_foam_unit"]["cost"], {"credits": 17300, "coins": 10})
        self.assertEqual(data["water_foam_carrier"]["staffing"], {"minimum": 1, "maximum": 2})
        self.assertEqual(data["rescue_pump_with_cafs"]["staffing"], {"minimum": 2, "maximum": 9})
        self.assertEqual(data["drone"]["resource_class"], "equipment")
        self.assertIn("Drone Operator", data["drone"]["training"])

    def test_schema_supports_enrichment_contracts(self):
        schema = json.loads((ROOT / "data" / "schema" / "vehicle.schema.json").read_text(encoding="utf-8"))
        self.assertIn("resource_class", schema["properties"])
        self.assertIn("towing", schema["properties"])
        self.assertIn("patients", schema["properties"]["transport_capacity"]["properties"])


if __name__ == "__main__":
    unittest.main()
