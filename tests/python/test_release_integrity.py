#!/usr/bin/env python3

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

import release_readiness as readiness  # noqa: E402
import sync_public_verification_metrics as sync  # noqa: E402


class PublicMetricSyncTests(unittest.TestCase):
    def test_collection_counts_are_named_and_complete(self) -> None:
        metrics = sync.load_metrics()

        self.assertEqual(metrics["canonical"], 1079)
        self.assertEqual(metrics["vehicles"], 92)
        self.assertEqual(metrics["infrastructure"], 19)
        self.assertEqual(metrics["training"], 12)
        self.assertEqual(metrics["search_entities"], 1202)

    def test_home_sync_targets_hero_and_board_independently(self) -> None:
        metrics = sync.load_metrics()
        fixture = "\n".join(
            (
                '<strong data-mcuk-metric="missions">1</strong>',
                '<strong data-mcuk-metric="fully-canonical">2</strong>',
                "alongside 3 higher-trust canonical mappings",
                '<strong data-mcuk-collection="missions">4</strong>',
                '<strong data-mcuk-verification="fully-canonical">5</strong>',
                '<strong data-mcuk-collection="vehicles">6</strong>',
                '<strong data-mcuk-collection="infrastructure">7</strong>',
                '<strong data-mcuk-collection="training">8</strong>',
                "<span><b>9</b> direct ID matches</span>",
                "<b data-mcuk-search-count>10</b>",
            )
        )

        updated = sync.sync_home(fixture, metrics)

        self.assertIn('data-mcuk-metric="fully-canonical">1,062<', updated)
        self.assertIn('data-mcuk-verification="fully-canonical">1,062<', updated)
        self.assertIn('data-mcuk-collection="vehicles">92<', updated)
        self.assertIn('data-mcuk-collection="training">12<', updated)
        self.assertEqual(sync.sync_home(updated, metrics), updated)

    def test_publication_files_are_synchronized_and_idempotent(self) -> None:
        metrics = sync.load_metrics()
        batches = sync.load_batches()
        readme = sync.README_PATH.read_text(encoding="utf-8")
        home = sync.HOME_PATH.read_text(encoding="utf-8")
        release = sync.RELEASE_PATH.read_text(encoding="utf-8")

        self.assertEqual(sync.sync_readme(readme, metrics, batches), readme)
        self.assertEqual(sync.sync_home(home, metrics), home)
        self.assertEqual(sync.sync_release(release, metrics, batches), release)


class ReleaseReadinessTests(unittest.TestCase):
    def test_structured_marker_does_not_accept_number_substrings(self) -> None:
        with self.assertRaises(readiness.AuditFailure):
            readiness.require_pattern(
                "| **Deployable resources** | **591** |",
                r"^\| \*\*Deployable resources\*\* \| \*\*59\*\* \|",
                "stale count",
            )

    def test_catalogue_refresh_is_fail_closed_on_drift(self) -> None:
        workflow = (
            ROOT / ".github" / "workflows" / "import-official-uk-missions.yml"
        ).read_text(encoding="utf-8")
        required = (
            'echo "CANDIDATE_DIR=$RUNNER_TEMP/official-uk-candidate" >> "$GITHUB_ENV"',
            'echo "DRIFT_DIR=$RUNNER_TEMP/official-uk-drift" >> "$GITHUB_ENV"',
            "detect_official_mission_drift.py",
            "steps.drift.outputs.has_drift == 'false'",
            "steps.drift.outputs.has_drift == 'true'",
            "data/sources/missionchief-uk/einsaetze.raw.json",
            "data/sources/missionchief-uk/mission-coverage.json",
            "data/sources/missionchief-uk/official-key-inventory.json",
            "data/validation/official-catalogue-drift.json",
            "automation/official-catalogue-drift-${FINGERPRINT_SHORT}",
            "gh issue create",
            "gh pr create",
            "Fail closed on official drift",
        )
        for marker in required:
            self.assertIn(marker, workflow)

        forbidden = (
            "git push origin HEAD:main",
            "gh workflow run deploy-pages.yml",
            "Deploy refreshed catalogue",
            "git add -f",
        )
        for marker in forbidden:
            self.assertNotIn(marker, workflow)

    def test_catalogue_state_lines_accept_exact_values(self) -> None:
        readme = "\n".join(
            (
                "| **Official records awaiting canonical records** | **0** |",
                "| **Canonical-only overlays** | **17** |",
            )
        )
        notes = "\n".join(
            (
                "0 official records awaiting direct canonical records",
                "17 canonical overlay or derived records without standalone official IDs",
            )
        )
        readiness.audit_catalogue_state_lines(readme, notes, 0, 17)

    def test_catalogue_state_lines_reject_stale_awaiting_count(self) -> None:
        stale_readme = "\n".join(
            (
                "| **Official records awaiting canonical records** | **1** |",
                "| **Canonical-only overlays** | **17** |",
            )
        )
        stale_notes = "\n".join(
            (
                "1 official records awaiting direct canonical records",
                "17 canonical overlay or derived records without standalone official IDs",
            )
        )
        with self.assertRaises(readiness.AuditFailure):
            readiness.audit_catalogue_state_lines(stale_readme, stale_notes, 0, 17)

    def test_catalogue_state_lines_reject_stale_overlay_count(self) -> None:
        stale_readme = "\n".join(
            (
                "| **Official records awaiting canonical records** | **0** |",
                "| **Canonical-only overlays** | **16** |",
            )
        )
        stale_notes = "\n".join(
            (
                "0 official records awaiting direct canonical records",
                "16 canonical overlay or derived records without standalone official IDs",
            )
        )
        with self.assertRaises(readiness.AuditFailure):
            readiness.audit_catalogue_state_lines(stale_readme, stale_notes, 0, 17)

    def test_publication_metadata_matches_release_source(self) -> None:
        release = readiness.release_metadata()
        counts = {
            name: len(list(path.glob("*.json")))
            for name, path in readiness.COLLECTIONS.items()
        }
        verification = readiness.read_json(
            readiness.OFFICIAL_OUTPUT_ROOT / "uk-mission-verification.json"
        )
        summary = verification.get("summary")
        self.assertIsInstance(summary, dict)

        readiness.audit_publication_metadata(release, counts, summary)


if __name__ == "__main__":
    unittest.main()
