from __future__ import annotations

import re
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def local_targets(markdown: str) -> set[str]:
    markdown_targets = re.findall(r"!?\[[^\]]*\]\(([^)]+)\)", markdown)
    html_targets = re.findall(r'(?:href|src)="([^"]+)"', markdown)
    targets = set(markdown_targets + html_targets)
    return {
        target.split("#", 1)[0]
        for target in targets
        if target
        and not target.startswith(("http://", "https://", "mailto:", "#"))
    }


class RepositoryPackagingTests(unittest.TestCase):
    def test_hero_is_accessible_self_contained_svg(self) -> None:
        hero_path = ROOT / "assets/readme-hero.svg"
        root = ET.parse(hero_path).getroot()
        self.assertEqual(root.tag, "{http://www.w3.org/2000/svg}svg")
        self.assertEqual(root.attrib["viewBox"], "0 0 1440 480")
        svg_text = hero_path.read_text(encoding="utf-8")
        self.assertIn("<title>", svg_text)
        self.assertIn("<desc>", svg_text)
        self.assertIn("Reference", svg_text)
        self.assertIn("Style fingerprint", svg_text)
        self.assertIn("Scientific contract", svg_text)
        self.assertIn("Production prompt", svg_text)
        self.assertIn("Validation", svg_text)
        self.assertNotIn("<image", svg_text)
        self.assertNotIn('href="http', svg_text)

    def test_mit_license_is_present(self) -> None:
        license_text = (ROOT / "LICENSE").read_text(encoding="utf-8")
        self.assertTrue(license_text.startswith("MIT License\n"))
        self.assertIn("Copyright (c) 2026 kikixiong", license_text)
        self.assertIn("THE SOFTWARE IS PROVIDED \"AS IS\"", license_text)

    def test_ci_runs_the_full_unittest_suite(self) -> None:
        workflow = (ROOT / ".github/workflows/tests.yml").read_text(
            encoding="utf-8"
        )
        self.assertIn("name: Tests", workflow)
        self.assertIn("actions/checkout@v7", workflow)
        self.assertIn("actions/setup-python@v7", workflow)
        self.assertIn('python-version: ["3.11", "3.12", "3.13", "3.14"]', workflow)
        self.assertIn(
            "python -m unittest discover -s scripts -p 'test_*.py'", workflow
        )

    def test_english_readme_has_required_structure(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        required = (
            "assets/readme-hero.svg",
            "README.zh-CN.md",
            "## Why this skill",
            "## What it can do",
            "## How it works",
            "## Quick start",
            "## Use it with your agent",
            "## Validate your prompts",
            "## Project structure",
            "## Design principles",
            "## Contributing",
            "## License",
            "Learn",
            "Adapt",
            "Template",
            "Audit",
            "Iterate",
            "Python 3.11+",
        )
        for text in required:
            with self.subTest(text=text):
                self.assertIn(text, readme)

    def test_english_readme_local_links_resolve(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        # The Chinese counterpart is created in the next independently
        # testable task; Task 4 verifies both language-switch links.
        targets = local_targets(readme) - {"README.zh-CN.md"}
        for target in targets:
            with self.subTest(target=target):
                self.assertTrue((ROOT / target).exists(), target)


if __name__ == "__main__":
    unittest.main()
