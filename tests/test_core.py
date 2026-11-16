from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from link_auditor.core import audit, links

class LinkTests(unittest.TestCase):
    def test_extraction_and_code(self):
        text = '[ok](a.md)\n```md\n[skip](b.md)\n```\n`[skip](c.md)`\n![image](d.png)'
        self.assertEqual(list(links(text)), [(1, "a.md"), (6, "d.png")])

    def test_url_encoded_paths_and_fragments(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "a b.md").write_text("# Target", encoding="utf-8")
            (root / "index.md").write_text('[ok](a%20b.md#target) [anchor](#missing) [web](https://example.com)', encoding="utf-8")
            self.assertEqual(audit(root), [])

    def test_missing_and_escape(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "index.md").write_text('[bad](missing.md) [escape](../secret.md)', encoding="utf-8")
            self.assertEqual([x["code"] for x in audit(root)], ["missing_target", "outside_root"])

    def test_root_relative_and_title(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "index.md").write_text('[self](/index.md "Title")', encoding="utf-8")
            self.assertEqual(audit(root), [])

    def test_invalid_root(self):
        with self.assertRaises(ValueError):
            audit(Path("missing-directory"))

    def test_cli(self):
        result = subprocess.run([sys.executable, "-m", "link_auditor", "examples/docs"],
                                text=True, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stderr)
