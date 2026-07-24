from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_ROOT = ROOT / "scripts"
if str(SCRIPTS_ROOT) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_ROOT))

import check_validation_worktree as worktree  # noqa: E402


class ValidationWorktreeTests(unittest.TestCase):
    def test_strict_phase_rejects_every_change(self) -> None:
        tracked, untracked = worktree.unexpected_changes(
            {"data/uk/mission-verification-registry.json", "README.md"},
            {"docs/assets/data/v1/manifest.json"},
            allow_validation_generated_outputs=False,
        )

        self.assertEqual(
            tracked,
            ["README.md", "data/uk/mission-verification-registry.json"],
        )
        self.assertEqual(untracked, ["docs/assets/data/v1/manifest.json"])

    def test_final_phase_allows_only_enumerated_transient_outputs(self) -> None:
        tracked, untracked = worktree.unexpected_changes(
            {
                "data/uk/mission-verification-registry.json",
                "data/sources/missionchief-uk/mission-coverage.json",
            },
            {
                "docs/assets/data/v1/manifest.json",
                "unexpected-report.json",
            },
            allow_validation_generated_outputs=True,
        )

        self.assertEqual(
            tracked,
            ["data/sources/missionchief-uk/mission-coverage.json"],
        )
        self.assertEqual(untracked, ["unexpected-report.json"])


if __name__ == "__main__":
    unittest.main()
