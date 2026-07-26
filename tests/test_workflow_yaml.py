from __future__ import annotations

import unittest
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]


class WorkflowYamlTests(unittest.TestCase):
    def test_every_workflow_is_valid_yaml_with_jobs(self) -> None:
        workflows = sorted((ROOT / ".github" / "workflows").glob("*.yml"))
        self.assertTrue(workflows, "No GitHub Actions workflows were found")

        for path in workflows:
            with self.subTest(path=path.name):
                document = yaml.load(path.read_text(encoding="utf-8"), Loader=yaml.BaseLoader)
                self.assertIsInstance(document, dict)
                self.assertIn("on", document)
                self.assertIsInstance(document.get("jobs"), dict)
                self.assertTrue(document["jobs"], "Workflow jobs mapping must not be empty")


if __name__ == "__main__":
    unittest.main()
