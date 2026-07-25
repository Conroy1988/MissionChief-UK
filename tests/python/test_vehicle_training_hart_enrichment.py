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


def requirement(document, course):
    return next(item for item in document["training_requirements"] if item["course"] == course)


class VehicleTrainingHartTests(unittest.TestCase):
    def test_official_training_durations(self):
        data = records()
        self.assertEqual(requirement(data["hazmat_unit"], "HazMat")["duration_days"], 3)
        self.assertEqual(requirement(data["iccu"], "Mobile command")["duration_days"], 5)
        self.assertEqual(requirement(data["air_ambulance"], "Critical care")["duration_days"], 5)
        self.assertEqual(requirement(data["prv"], "HART Training")["duration_days"], 5)
        self.assertEqual(requirement(data["ambulance_control_unit"], "Tactical Command Course")["duration_days"], 5)
        self.assertEqual(requirement(data["mass_casualty_equipment"], "SORT Training")["duration_days"], 3)
        self.assertEqual(requirement(data["police_helicopter"], "Police aviation")["duration_days"], 7)
        self.assertEqual(requirement(data["traffic_car"], "Roads Policing Officer Training")["duration_days"], 3)
        self.assertEqual(requirement(data["mounted_unit"], "Mounted Training")["duration_days"], 4)

    def test_specialist_building_compatibility(self):
        data = records()
        self.assertIn("HART Base", data["prv"]["building_requirements"])
        self.assertIn("HART Base", data["welfare_vehicle"]["building_requirements"])
        self.assertNotIn("HART Training", data["welfare_vehicle"].get("training", []))
        self.assertIn("Large Police Depot", data["armed_response_vehicle"]["building_requirements"])
        self.assertIn("Police Helicopter Station", data["police_helicopter"]["building_requirements"])
        self.assertIn("Helicopter Station", data["air_ambulance"]["building_requirements"])

    def test_schema_supports_structured_training(self):
        schema = json.loads((ROOT / "data" / "schema" / "vehicle.schema.json").read_text(encoding="utf-8"))
        self.assertIn("training_requirements", schema["properties"])
        self.assertIn("trainingRequirement", schema["$defs"])


if __name__ == "__main__":
    unittest.main()
