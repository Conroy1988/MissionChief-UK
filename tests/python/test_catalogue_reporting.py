from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import generate_ready_canonical_batch as batch_generator
import report_canonical_candidates as candidate_report
import report_key_mapping_backlog as backlog_report


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def independent_catalogue_state() -> tuple[set[str], set[str], set[str]]:
    official = read_json(
        ROOT / "data" / "sources" / "missionchief-uk" / "einsaetze.raw.json"
    )
    official_ids = {
        str(record["id"])
        for record in official["records"]
        if isinstance(record, dict) and record.get("id") is not None
    }
    canonical_ids = {
        str(document["id"])
        for path in (ROOT / "data" / "uk" / "missions").glob("*.json")
        if isinstance((document := read_json(path)), dict)
        and document.get("id") is not None
    }

    registry_paths = [
        ROOT / "data" / "uk" / "mission-verification-registry.json",
        *sorted(
            (ROOT / "data" / "uk" / "mission-verification-batches").glob("*.json")
        ),
    ]
    decisions = {}
    for path in registry_paths:
        for mission_id, decision in read_json(path)["records"].items():
            key = str(mission_id)
            if key in decisions:
                if decisions[key] != decision:
                    raise AssertionError(
                        f"Conflicting independent verification decision for {key}"
                    )
                continue
            decisions[key] = decision
    fully_canonical_ids = {
        mission_id
        for mission_id, decision in decisions.items()
        if mission_id in official_ids and decision.get("stage") == "fully-canonical"
    }
    return official_ids, canonical_ids, fully_canonical_ids


class CandidateReportTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.report = candidate_report.report()
        (
            cls.official_ids,
            cls.canonical_ids,
            cls.fully_canonical_ids,
        ) = independent_catalogue_state()

    def test_catalogue_partition_is_complete_and_disjoint(self) -> None:
        new_records = self.report["new_records"]
        existing_records = self.report["existing_records"]
        new_ids = {
            str(item["id"])
            for item in [*new_records["ready"], *new_records["blocked"]]
        }
        existing_ids = {
            str(item["id"])
            for item in [
                *existing_records["equivalence_audit_required"],
                *existing_records["blocked"],
            ]
        }

        self.assertFalse(new_ids & existing_ids)
        self.assertFalse(new_ids & self.fully_canonical_ids)
        self.assertFalse(existing_ids & self.fully_canonical_ids)
        self.assertEqual(
            self.official_ids,
            new_ids | existing_ids | self.fully_canonical_ids,
        )
        self.assertEqual(
            existing_ids,
            (self.official_ids & self.canonical_ids)
            - self.fully_canonical_ids,
        )

    def test_legacy_creation_aliases_never_include_canonical_ids(self) -> None:
        self.assertEqual(self.report["ready"], self.report["new_records"]["ready"])
        self.assertEqual(self.report["blocked"], self.report["new_records"]["blocked"])
        ready_ids = {str(item["id"]) for item in self.report["ready"]}
        self.assertFalse(ready_ids & self.canonical_ids)

    def test_summary_count_invariants(self) -> None:
        self.assertEqual(
            self.report["official_count"],
            self.report["fully_canonical_count"]
            + self.report["new_records"]["count"]
            + self.report["existing_records"]["count"],
        )
        self.assertEqual(
            self.report["canonical_count"],
            self.report["direct_canonical_count"]
            + self.report["canonical_only_count"],
        )
        self.assertEqual(
            self.report["remaining_to_fully_canonical_count"],
            self.report["new_records"]["count"]
            + self.report["existing_records"]["count"],
        )

    def test_cli_limits_do_not_change_summary_counts(self) -> None:
        limited = candidate_report.limited_report(self.report, 1, 2, 1)
        for key in (
            "official_count",
            "canonical_count",
            "fully_canonical_count",
            "ready_count",
            "blocked_count",
        ):
            self.assertEqual(limited[key], self.report[key])
        self.assertLessEqual(len(limited["new_records"]["ready"]), 1)
        self.assertLessEqual(len(limited["new_records"]["blocked"]), 2)
        self.assertLessEqual(
            len(limited["existing_records"]["equivalence_audit_required"]), 1
        )
        self.assertLessEqual(len(limited["existing_records"]["blocked"]), 1)
        self.assertEqual(limited["ready"], limited["new_records"]["ready"])
        self.assertEqual(limited["blocked"], limited["new_records"]["blocked"])

    def test_registry_union_accepts_idempotent_duplicates(self) -> None:
        decision = {"stage": "fully-canonical", "strict_key_equivalence": True}
        documents = [
            (
                "base.json",
                {"schema_version": "1", "records": {"7": decision}},
            ),
            (
                "batch.json",
                {"schema_version": "1", "records": {"7": dict(decision)}},
            ),
        ]
        self.assertEqual(
            candidate_report.merge_verification_decision_documents(documents),
            {"7": decision},
        )

    def test_registry_union_rejects_conflicting_duplicates(self) -> None:
        documents = [
            (
                "base.json",
                {"schema_version": "1", "records": {"7": {"stage": "captured"}}},
            ),
            (
                "batch.json",
                {
                    "schema_version": "1",
                    "records": {"7": {"stage": "fully-canonical"}},
                },
            ),
        ]
        with self.assertRaisesRegex(
            ValueError, "Conflicting mission verification decision 7"
        ):
            candidate_report.merge_verification_decision_documents(documents)


class GeneratorSafetyTests(unittest.TestCase):
    def test_generator_reads_only_the_new_record_creation_pool(self) -> None:
        creation_candidate = {
            "id": "unit-test-new",
            "suggested_path": "data/uk/missions/unit-test-new.json",
        }
        existing_candidate = {
            "id": "unit-test-existing",
            "suggested_path": "data/uk/missions/unit-test-existing.json",
        }
        document = {
            "ready": [existing_candidate],
            "new_records": {"ready": [creation_candidate]},
            "existing_records": {
                "equivalence_audit_required": [existing_candidate]
            },
        }
        self.assertEqual(
            batch_generator.creation_ready_candidates(document),
            [creation_candidate],
        )

    def test_duplicate_canonical_id_is_rejected_before_check_mode_returns(self) -> None:
        official_ids, canonical_ids, _ = independent_catalogue_state()
        mission_id = sorted(official_ids & canonical_ids)[0]
        document = {
            "new_records": {
                "ready": [
                    {
                        "id": mission_id,
                        "suggested_path": "data/uk/missions/never-write-unit-test.json",
                    }
                ]
            }
        }
        with mock.patch.object(
            batch_generator, "candidate_report", return_value=document
        ):
            with self.assertRaisesRegex(ValueError, "already has canonical record"):
                batch_generator.generate(1, True)

    def test_duplicate_creation_paths_are_rejected(self) -> None:
        candidates = [
            {
                "id": "unit-test-a",
                "suggested_path": "data/uk/missions/unit-test-shared.json",
            },
            {
                "id": "unit-test-b",
                "suggested_path": "data/uk/missions/unit-test-shared.json",
            },
        ]
        official = {
            "unit-test-a": {"id": "unit-test-a"},
            "unit-test-b": {"id": "unit-test-b"},
        }
        with self.assertRaisesRegex(ValueError, "path is repeated"):
            batch_generator.validate_creation_candidates(candidates, official, {})


class BacklogReportTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.report = backlog_report.build_report(1)

    def test_occurrences_and_state_counts_reconcile(self) -> None:
        catalogue_occurrences = 0
        state_occurrences = {
            "official-only": 0,
            "canonical-unpromoted": 0,
            "fully-canonical": 0,
        }
        for entry in self.report["entries"]:
            state_total = (
                entry["official_only_mission_count"]
                + entry["canonical_unpromoted_mission_count"]
                + entry["fully_canonical_mission_count"]
            )
            self.assertEqual(entry["catalogue_mission_count"], state_total)
            catalogue_occurrences += entry["catalogue_mission_count"]
            state_occurrences["official-only"] += entry[
                "official_only_mission_count"
            ]
            state_occurrences["canonical-unpromoted"] += entry[
                "canonical_unpromoted_mission_count"
            ]
            state_occurrences["fully-canonical"] += entry[
                "fully_canonical_mission_count"
            ]

        self.assertEqual(
            catalogue_occurrences,
            self.report["catalogue_unmapped_occurrence_count"],
        )
        self.assertEqual(
            state_occurrences["official-only"],
            self.report["official_only_unmapped_occurrence_count"],
        )
        self.assertEqual(
            state_occurrences["canonical-unpromoted"],
            self.report["canonical_unpromoted_unmapped_occurrence_count"],
        )
        self.assertEqual(
            state_occurrences["fully-canonical"],
            self.report["fully_canonical_unmapped_occurrence_count"],
        )

    def test_allow_list_blocker_prevents_false_single_key_unlock(self) -> None:
        blockers = [
            "unmapped requirements.height_rescue_units",
            "prerequisites.main_building=28 outside allow-list [0]",
        ]
        self.assertIsNone(
            backlog_report.single_key_unlock_bucket(
                "official-only",
                blockers,
                "requirements",
                "height_rescue_units",
            )
        )

    def test_single_key_unlocks_use_separate_creation_and_audit_buckets(self) -> None:
        blockers = ["unmapped requirements.unit_test_resource"]
        self.assertEqual(
            backlog_report.single_key_unlock_bucket(
                "official-only",
                blockers,
                "requirements",
                "unit_test_resource",
            ),
            "creation",
        )
        self.assertEqual(
            backlog_report.single_key_unlock_bucket(
                "canonical-unpromoted",
                blockers,
                "requirements",
                "unit_test_resource",
            ),
            "existing-audit",
        )
        self.assertIsNone(
            backlog_report.single_key_unlock_bucket(
                "fully-canonical",
                blockers,
                "requirements",
                "unit_test_resource",
            )
        )

    def test_known_false_unlocks_are_zero_and_show_the_remaining_blocker(self) -> None:
        entries = {
            (entry["group"], entry["key"]): entry for entry in self.report["entries"]
        }
        for key in ("height_rescue_units", "coastal_support"):
            entry = entries[("requirements", key)]
            self.assertEqual(entry["single_key_creation_unlock_count"], 0)
            examples = entry["examples_by_state"]["official-only"]
            self.assertTrue(
                any(
                    "outside allow-list" in blocker
                    for example in examples
                    for blocker in example["other_blockers"]
                )
            )


if __name__ == "__main__":
    unittest.main()
