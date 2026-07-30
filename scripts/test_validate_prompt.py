#!/usr/bin/env python3
"""Regression tests for validate_prompt.py."""

from __future__ import annotations

import unittest

from test_validate_style_profile import VALID_PROFILE
from validate_prompt import validate_text


BASE_PROMPT = """
SCIENTIFIC CONTENT CONTRACT
Must show: one input to one output.
Must not imply unsupported success.

CANVAS AND BACKGROUND
Use one 4:3 white canvas.

VISUAL STRUCTURE
Use exactly three panels.

TYPOGRAPHY AND EXACT TEXT
Render exactly: "Input" and "Output".

COLOR AND ICON LANGUAGE
Blue means data. Gray means neutral flow.

STRICT NEGATIVE CONSTRAINTS
Do not invent results or copy reference content.

FINAL VALIDATION
Verify exact text, arrows, evidence state, and background.
"""


def warnings_for(text: str, *, iteration: bool = False) -> list[str]:
    _, warnings, _ = validate_text(text, iteration=iteration)
    return warnings


class ValidatePromptTests(unittest.TestCase):
    def test_operational_identifier_warning(self) -> None:
        warnings = warnings_for(BASE_PROMPT + "\nRender Job 250229 on a card.")
        self.assertTrue(any("operational identifier" in item for item in warnings))

    def test_conflicting_aspect_ratio_warning(self) -> None:
        warnings = warnings_for(BASE_PROMPT + "\nAlternative canvas: 2.4:1.")
        self.assertTrue(any("conflicting aspect-ratio" in item for item in warnings))

    def test_conflicting_exact_panel_count_warning(self) -> None:
        warnings = warnings_for(BASE_PROMPT + "\nUse exactly four panels.")
        self.assertTrue(any("conflicting exact panel counts" in item for item in warnings))

    def test_architecture_count_ambiguity_warning(self) -> None:
        prompt = BASE_PROMPT + """
Use a 3-layer GNN and an Output dim = 3 card.
"""
        warnings = warnings_for(prompt)
        self.assertTrue(any("architecture count ambiguity" in item for item in warnings))

    def test_architecture_disambiguation_suppresses_warning(self) -> None:
        prompt = BASE_PROMPT + """
Use a 3-layer GNN and an Output dim = 3 card.
Only the complete layer stack has one outgoing arrow.
Do not map a layer number to an output component.
"""
        warnings = warnings_for(prompt)
        self.assertFalse(any("architecture count ambiguity" in item for item in warnings))

    def test_iteration_requires_style_lock(self) -> None:
        errors, _, _ = validate_text(BASE_PROMPT, iteration=True)
        self.assertTrue(any("STYLE LOCK" in item for item in errors))

    def test_complete_iteration_style_lock(self) -> None:
        prompt = BASE_PROMPT + """
REVISION SCOPE AND STYLE LOCK
Change only the incorrect output arrow.
Preserve the canvas and aspect ratio, information density and whitespace,
palette and color mappings, typography, icon family, and all other content.
"""
        errors, warnings, _ = validate_text(prompt, iteration=True)
        self.assertFalse(errors)
        self.assertFalse(any("style lock" in item for item in warnings))

    def test_style_profile_requires_binding_section(self) -> None:
        errors, _, _ = validate_text(BASE_PROMPT, style_profile=VALID_PROFILE)
        self.assertTrue(any("PROJECT STYLE PROFILE" in item for item in errors))

    def test_style_profile_requires_profile_tokens(self) -> None:
        prompt = BASE_PROMPT + """
PROJECT STYLE PROFILE
Profile ID: "example-paper"
Profile version: "1"
"""
        errors, _, _ = validate_text(prompt, style_profile=VALID_PROFILE)
        self.assertTrue(any("required project-style tokens" in item for item in errors))

    def test_complete_style_profile_binding(self) -> None:
        prompt = BASE_PROMPT + """
PROJECT STYLE PROFILE
Profile ID: "example-paper"
Profile version: "1"
Use #FFFFFF, Example Display, and #F2F2F2 as project-wide invariants.
"""
        errors, _, _ = validate_text(prompt, style_profile=VALID_PROFILE)
        self.assertFalse(errors)


if __name__ == "__main__":
    unittest.main()
