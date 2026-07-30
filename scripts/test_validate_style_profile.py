#!/usr/bin/env python3
"""Regression tests for validate_style_profile.py."""

from __future__ import annotations

import copy
import unittest

from validate_style_profile import validate_profile


VALID_PROFILE = {
    "profile_version": 1,
    "profile_id": "example-paper",
    "project": "Example Paper",
    "status": "accepted",
    "authority": "user-approved first figure",
    "updated": "2026-07-30",
    "canvas": {
        "default_aspect_ratio": "4:3",
        "allowed_aspect_ratios": ["4:3", "2:1"],
        "orientation": "landscape",
        "background": "#FFFFFF",
        "margin_behavior": "narrow outer margins",
    },
    "typography": {
        "display": "Example Display",
        "label": "Example Label",
        "technical": "Example Mono",
        "equation": "math typesetting",
        "casing": "sentence case",
    },
    "palette": {
        "dominant": ["#F2F2F2", "#DAE3F3"],
        "accents": ["#588E32", "#D98C55"],
        "semantic": ["blue = data", "green = correction"],
        "forbidden": ["neon"],
    },
    "density": {
        "level": "compact",
        "internal_whitespace": "8-12%",
        "label_budget": "1-5 words",
        "module_scale": "small",
    },
    "icons": {
        "family": "sticker-like scientific icons",
        "outline": "thin charcoal",
        "shading": "minimal",
    },
    "containers": {
        "border": "medium-gray dashed",
        "title_tabs": "white overlapping tabs",
        "corner_style": "rounded",
        "panel_fill_behavior": "pastel only",
    },
    "arrows": {
        "major": "shallow filled",
        "minor": "thin curved",
        "crossing_policy": "avoid crossings",
    },
    "anti_style": {"forbidden": ["3D", "dashboard", "global gradient"]},
    "validation": {
        "required_prompt_tokens": [
            "example-paper",
            "#FFFFFF",
            "Example Display",
            "#F2F2F2",
        ]
    },
}


class ValidateStyleProfileTests(unittest.TestCase):
    def test_valid_profile(self) -> None:
        errors, warnings = validate_profile(VALID_PROFILE)
        self.assertFalse(errors)
        self.assertFalse(warnings)

    def test_placeholder_is_rejected(self) -> None:
        profile = copy.deepcopy(VALID_PROFILE)
        profile["profile_id"] = "REPLACE_ME"
        errors, _ = validate_profile(profile)
        self.assertTrue(any("unresolved placeholders" in item for item in errors))

    def test_default_aspect_must_be_allowed(self) -> None:
        profile = copy.deepcopy(VALID_PROFILE)
        profile["canvas"]["allowed_aspect_ratios"] = ["2:1"]
        errors, _ = validate_profile(profile)
        self.assertTrue(any("default_aspect_ratio" in item for item in errors))

    def test_palette_requires_hex_colors(self) -> None:
        profile = copy.deepcopy(VALID_PROFILE)
        profile["palette"]["dominant"] = ["dust gray"]
        errors, _ = validate_profile(profile)
        self.assertTrue(any("palette.dominant" in item for item in errors))

    def test_draft_profile_warns(self) -> None:
        profile = copy.deepcopy(VALID_PROFILE)
        profile["status"] = "draft"
        errors, warnings = validate_profile(profile)
        self.assertFalse(errors)
        self.assertTrue(any("profile is draft" in item for item in warnings))


if __name__ == "__main__":
    unittest.main()
