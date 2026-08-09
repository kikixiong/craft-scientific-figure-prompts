from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class RepositoryPackagingTests(unittest.TestCase):
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


if __name__ == "__main__":
    unittest.main()
