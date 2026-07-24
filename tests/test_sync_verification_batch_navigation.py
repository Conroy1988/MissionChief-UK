from __future__ import annotations

import io
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_ROOT = ROOT / "scripts"
if str(SCRIPTS_ROOT) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_ROOT))

import sync_verification_batch_navigation as navigation  # noqa: E402


class VerificationBatchNavigationTests(unittest.TestCase):
    def test_synchronization_normalises_blank_lines_and_is_idempotent(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            reference_root = root / "reference"
            reference_root.mkdir()
            for number in range(1, 4):
                (reference_root / f"fully-canonical-mission-batch-{number}.md").write_text(
                    f"# Batch {number}\n",
                    encoding="utf-8",
                )

            mkdocs_path = root / "mkdocs.yml"
            mkdocs_path.write_text(
                """nav:
  - Reference Database:
      - Mission Intelligence:
          - Mission Database: reference/mission-database.md
          - Fully Canonical Batch 1: reference/fully-canonical-mission-batch-1.md

          - Fully Canonical Batch 2: reference/fully-canonical-mission-batch-2.md



          - Fully Canonical Batch 3: reference/fully-canonical-mission-batch-3.md


          - Verified Mission Records: reference/verified-mission-records.md
          - Mission Batch 2: reference/verified-mission-batch-2.md
""",
                encoding="utf-8",
            )

            with (
                patch.object(navigation, "REFERENCE_ROOT", reference_root),
                patch.object(navigation, "MKDOCS_PATH", mkdocs_path),
                redirect_stdout(io.StringIO()),
            ):
                self.assertEqual(navigation.main(), 0)
                first_result = mkdocs_path.read_text(encoding="utf-8")
                self.assertEqual(navigation.main(), 0)
                second_result = mkdocs_path.read_text(encoding="utf-8")

            expected_block = """          - Fully Canonical Batch 1: reference/fully-canonical-mission-batch-1.md
          - Fully Canonical Batch 2: reference/fully-canonical-mission-batch-2.md
          - Fully Canonical Batch 3: reference/fully-canonical-mission-batch-3.md
          - Verified Mission Records: reference/verified-mission-records.md
"""
            self.assertIn(expected_block, first_result)
            self.assertEqual(first_result, second_result)
            self.assertNotIn("\n\n          - Fully Canonical Batch", first_result)


if __name__ == "__main__":
    unittest.main()
