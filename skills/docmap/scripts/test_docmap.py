#!/usr/bin/env python3
"""Tests for docmap.py. Run: python3 scripts/test_docmap.py"""

import os
import shutil
import tempfile
import unittest

from docmap import audit, extract_links, is_relative_link


class TempRepo(unittest.TestCase):
    def make_repo(self, files):
        root = tempfile.mkdtemp(prefix="docmap-")
        self.addCleanup(shutil.rmtree, root, True)
        for rel, contents in files.items():
            full = os.path.join(root, rel)
            os.makedirs(os.path.dirname(full), exist_ok=True)
            with open(full, "w", encoding="utf-8") as handle:
                handle.write(contents)
        return root

    def keys(self, root):
        return {f'{f["kind"]} {f["file"]}' for f in audit(root)}


class TestLinks(TempRepo):
    def test_extract_links_skips_fences_and_titles(self):
        links = extract_links('[real](a.md)\n[title](b.md "note")\n```\n[fenced](c.md)\n```\n')
        self.assertEqual(links, ["a.md", "b.md"])

    def test_is_relative_link(self):
        self.assertTrue(is_relative_link("x/y.md"))
        self.assertTrue(is_relative_link("./y.md"))
        self.assertFalse(is_relative_link("https://e.com/x"))
        self.assertFalse(is_relative_link("mailto:a@b.c"))
        self.assertFalse(is_relative_link("#section"))
        self.assertFalse(is_relative_link("/abs/path"))


class TestAudit(TempRepo):
    def test_missing_readme_and_broken_link(self):
        root = self.make_repo({
            "docs/guide.md": "[broken](nope.md)\n[ok](reference.md)\n",
            "docs/reference.md": "# Reference\n",
        })
        keys = self.keys(root)
        self.assertIn("MISSING README.md", keys)
        self.assertIn("BROKEN-LINK docs/guide.md", keys)

    def test_skill_md_format_is_not_audited_links_are(self):
        root = self.make_repo({
            "README.md": "# Repo\n",
            "some-skill/SKILL.md": "no frontmatter at all, links [here](missing.md)\n",
        })
        keys = self.keys(root)
        self.assertNotIn("INVALID some-skill/SKILL.md", keys)
        self.assertIn("BROKEN-LINK some-skill/SKILL.md", keys)

    def test_clean_repo_has_no_blocking_findings(self):
        root = self.make_repo({
            "README.md": "# Repo\n\nSee [the guide](docs/guide.md) and the [index](docs/index.md).\n",
            "docs/guide.md": "# Guide\n\nBack to [README](../README.md).\n",
            "docs/index.md": "# Index\n",
        })
        blocking = [f for f in audit(root) if f["kind"] != "INFO"]
        self.assertEqual(blocking, [])

    def test_docs_without_index_is_info_only(self):
        root = self.make_repo({
            "README.md": "# Repo\n",
            "docs/a.md": "# A\n",
        })
        keys = self.keys(root)
        self.assertIn("INFO docs", keys)


if __name__ == "__main__":
    unittest.main()
