from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

from classify_ci_changes import classify  # noqa: E402


class ChangeClassifierTests(unittest.TestCase):
    def test_markdown_service_page_uses_guide_only_lane(self) -> None:
        result = classify(["docs/services/fire-and-rescue.md"])
        self.assertTrue(result["docs"])
        self.assertTrue(result["guide_only"])
        self.assertFalse(result["data"])
        self.assertFalse(result["interface"])
        self.assertFalse(result["full_required"])

    def test_javascript_change_uses_interface_lane(self) -> None:
        result = classify(["docs/javascripts/command-palette.js"])
        self.assertTrue(result["docs"])
        self.assertTrue(result["interface"])
        self.assertFalse(result["guide_only"])

    def test_vehicle_contract_change_is_vehicle_only(self) -> None:
        result = classify([
            "data/uk/vehicles/fire-engine.json",
            "tests/python/test_vehicle_inventory.py",
        ])
        self.assertTrue(result["data"])
        self.assertTrue(result["vehicle"])
        self.assertTrue(result["vehicle_only"])

    def test_release_metadata_requires_full_audit(self) -> None:
        result = classify(["data/version.json", "docs/releases/v1.4.0.md"])
        self.assertTrue(result["release"])
        self.assertTrue(result["full_required"])

    def test_workflow_change_requires_full_audit(self) -> None:
        result = classify([".github/workflows/validate.yml"])
        self.assertTrue(result["workflow"])
        self.assertTrue(result["full_required"])

    def test_unknown_root_file_fails_closed(self) -> None:
        result = classify(["unexpected-runtime.conf"])
        self.assertTrue(result["unknown"])
        self.assertTrue(result["full_required"])


if __name__ == "__main__":
    unittest.main()
