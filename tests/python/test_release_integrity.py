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

        self.assertEqual(metrics["canonical"], 284)
        self.assertEqual(metrics["vehicles"], 48)
        self.assertEqual(metrics["infrastructure"], 18)
        self.assertEqual(metrics["training"], 12)
        self.assertEqual(metrics["search_entities"], 362)

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

        self.assertIn('data-mcuk-metric="fully-canonical">226<', updated)
        self.assertIn('data-mcuk-verification="fully-canonical">226<', updated)
        self.assertIn('data-mcuk-collection="vehicles">48<', updated)
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
                "| **Deployable resources** | **481** |",
                r"^\| \*\*Deployable resources\*\* \| \*\*48\*\* \|",
                "stale count",
            )

    def test_catalogue_refresh_stages_only_durable_outputs(self) -> None:
        workflow = (
            ROOT / ".github" / "workflows" / "import-official-uk-missions.yml"
        ).read_text(encoding="utf-8")
        durable = (
            "data/sources/missionchief-uk/einsaetze.raw.json",
            "data/sources/missionchief-uk/mission-coverage.json",
            "data/sources/missionchief-uk/official-key-inventory.json",
            "docs/assets/data/official/uk-mission-coverage.json",
            "docs/assets/data/official/uk-missions.json",
            "docs/reference/mission-verification-status.md",
            "git add -A -- data/sources/missionchief-uk/official-missions.json",
        )
        for path in durable:
            self.assertIn(path, workflow)

        forbidden = (
            "git add -f data/sources/missionchief-uk",
            "data/sources/missionchief-uk \\",
            "docs/assets/data/official \\",
            "data/sources/missionchief-uk/mission-verification-status.json",
            "docs/assets/data/official/uk-mission-verification.json",
        )
        for path in forbidden:
            self.assertNotIn(path, workflow)

    def test_catalogue_state_lines_accept_exact_values(self) -> None:
        readme = "\n".join(
            (
                "| **Official records awaiting canonical records** | **795** |",
                "| **Canonical-only overlays** | **17** |",
            )
        )
        notes = "\n".join(
            (
                "795 official records awaiting direct canonical records",
                "17 canonical overlay or derived records without standalone official IDs",
            )
        )
        readiness.audit_catalogue_state_lines(readme, notes, 795, 17)

    def test_catalogue_state_lines_reject_stale_values(self) -> None:
        stale_readme = "\n".join(
            (
                "| **Official records awaiting canonical records** | **794** |",
                "| **Canonical-only overlays** | **16** |",
            )
        )
        stale_notes = "\n".join(
            (
                "794 official records awaiting direct canonical records",
                "16 canonical overlay or derived records without standalone official IDs",
            )
        )
        with self.assertRaises(readiness.AuditFailure):
            readiness.audit_catalogue_state_lines(stale_readme, stale_notes, 795, 17)

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
