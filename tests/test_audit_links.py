from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from unittest import mock

from scripts import audit_links


class AnchorRendererTests(unittest.TestCase):
    def test_mkdocs_page_rejects_github_double_hyphen_slug(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            docs_root = Path(directory) / "docs"
            page = docs_root / "page.md"
            docs_root.mkdir()
            page.write_text(
                "## Belay Failure Whilst Abseiling — helicopter overlay\n",
                encoding="utf-8",
            )

            with mock.patch.object(audit_links, "DOCS_ROOT", docs_root):
                generated = audit_links.anchors(page)

        self.assertIn(
            "belay-failure-whilst-abseiling-helicopter-overlay",
            generated,
        )
        self.assertNotIn(
            "belay-failure-whilst-abseiling--helicopter-overlay",
            generated,
        )

    def test_non_mkdocs_page_keeps_github_slug_rules(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            docs_root = root / "docs"
            page = root / "README.md"
            docs_root.mkdir()
            page.write_text(
                "## Belay Failure Whilst Abseiling — helicopter overlay\n",
                encoding="utf-8",
            )

            with mock.patch.object(audit_links, "DOCS_ROOT", docs_root):
                generated = audit_links.anchors(page)

        self.assertIn(
            "belay-failure-whilst-abseiling--helicopter-overlay",
            generated,
        )
        self.assertNotIn(
            "belay-failure-whilst-abseiling-helicopter-overlay",
            generated,
        )


if __name__ == "__main__":
    unittest.main()
