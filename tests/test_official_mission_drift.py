from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import detect_official_mission_drift as drift  # noqa: E402


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


class OfficialMissionDriftTests(unittest.TestCase):
    def workspace(
        self,
        baseline_records: list[dict],
        candidate_records: list[dict],
        *,
        canonical_ids: tuple[int, ...] = (1,),
        fully_canonical_ids: tuple[int, ...] = (1,),
    ) -> tuple[Path, Path, Path, Path, tempfile.TemporaryDirectory]:
        temporary = tempfile.TemporaryDirectory()
        root = Path(temporary.name)
        baseline = root / "baseline.json"
        candidate = root / "candidate.json"
        canonical = root / "canonical"
        registry = root / "registry.json"
        write_json(
            baseline,
            {
                "source_sha256": "baseline-sha",
                "fetched_at": "2026-07-24T00:00:00Z",
                "records": baseline_records,
            },
        )
        write_json(
            candidate,
            {
                "source_sha256": "candidate-sha",
                "fetched_at": "2026-07-25T00:00:00Z",
                "records": candidate_records,
            },
        )
        for mission_id in canonical_ids:
            write_json(
                canonical / f"{mission_id}.json",
                {"id": mission_id, "name": f"Mission {mission_id}"},
            )
        write_json(
            registry,
            {
                "records": {
                    str(mission_id): {"stage": "fully-canonical"}
                    for mission_id in fully_canonical_ids
                }
            },
        )
        return baseline, candidate, canonical, registry, temporary

    def build(
        self,
        baseline_records: list[dict],
        candidate_records: list[dict],
        **kwargs,
    ) -> dict:
        baseline, candidate, canonical, registry, temporary = self.workspace(
            baseline_records,
            candidate_records,
            **kwargs,
        )
        self.addCleanup(temporary.cleanup)
        return drift.build_report(
            baseline,
            candidate,
            canonical,
            registry,
            generated_at="2026-07-25T01:00:00Z",
        )

    def test_semantically_identical_records_are_clean(self) -> None:
        records = [{"id": 1, "name": "Mission 1", "requirements": {"firetrucks": 1}}]
        report = self.build(records, json.loads(json.dumps(records)))
        self.assertFalse(report["has_drift"])
        self.assertEqual(report["status"], "clean")
        self.assertEqual(report["summary"]["review_required_count"], 0)
        self.assertEqual(report["impact"]["projected_fully_canonical_percent"], 100.0)

    def test_added_mission_becomes_new_uncovered_identity(self) -> None:
        report = self.build(
            [{"id": 1, "name": "Mission 1"}],
            [
                {"id": 1, "name": "Mission 1"},
                {"id": 2, "name": "Mission 2", "requirements": {"police_cars": 1}},
            ],
        )
        self.assertTrue(report["has_drift"])
        self.assertEqual(report["summary"]["added_count"], 1)
        self.assertEqual(report["impact"]["new_uncovered_ids"], ["2"])
        self.assertEqual(report["impact"]["projected_fully_canonical_count"], 1)
        self.assertEqual(report["impact"]["projected_fully_canonical_percent"], 50.0)

    def test_nested_requirement_change_invalidates_verified_identity(self) -> None:
        report = self.build(
            [{"id": 1, "name": "Mission 1", "requirements": {"firetrucks": 1}}],
            [{"id": 1, "name": "Mission 1", "requirements": {"firetrucks": 2}}],
        )
        self.assertEqual(report["summary"]["modified_count"], 1)
        modified = report["changes"]["modified"][0]
        self.assertEqual(modified["severity"], "critical")
        self.assertIn("requirements", modified["groups"])
        self.assertEqual(
            [item["path"] for item in modified["changed_paths"]],
            ["requirements.firetrucks"],
        )
        self.assertEqual(report["impact"]["invalidated_fully_canonical_ids"], ["1"])
        self.assertEqual(report["impact"]["projected_fully_canonical_percent"], 0.0)

    def test_removed_mission_invalidates_verified_identity(self) -> None:
        report = self.build(
            [
                {"id": 1, "name": "Mission 1"},
                {"id": 2, "name": "Mission 2"},
            ],
            [{"id": 2, "name": "Mission 2"}],
            canonical_ids=(1, 2),
            fully_canonical_ids=(1, 2),
        )
        self.assertEqual(report["summary"]["removed_count"], 1)
        self.assertEqual(report["impact"]["invalidated_fully_canonical_ids"], ["1"])
        self.assertEqual(report["impact"]["projected_fully_canonical_count"], 1)
        self.assertEqual(report["impact"]["projected_fully_canonical_percent"], 100.0)
        self.assertTrue(report["impact"]["coverage_regression"])

    def test_fingerprint_is_deterministic(self) -> None:
        baseline = [{"id": 1, "name": "Mission 1"}]
        candidate = [{"id": 1, "name": "Mission renamed"}]
        first = self.build(baseline, candidate)
        second = self.build(baseline, candidate)
        self.assertEqual(first["fingerprint"], second["fingerprint"])
        self.assertEqual(
            drift.render_markdown(first),
            drift.render_markdown(second),
        )


if __name__ == "__main__":
    unittest.main()
