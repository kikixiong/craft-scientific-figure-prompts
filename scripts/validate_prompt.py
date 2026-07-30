#!/usr/bin/env python3
"""Static checks for layered scientific figure prompts."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


SECTION_PATTERNS = {
    "scientific content contract": r"(?im)^(?:SCIENTIFIC|SEMANTIC)\s+(?:CONTENT\s+)?CONTRACT\b",
    "canvas/background": r"(?im)^(?:CANVAS|OUTPUT|BACKGROUND).*\b(?:BACKGROUND|CANVAS|FORMAT)\b|^CANVAS\b",
    "visual structure": r"(?im)^(?:VISUAL\s+)?(?:STRUCTURE|LAYOUT|COMPOSITION)\b",
    "typography/exact text": r"(?im)^(?:TYPOGRAPHY|EXACT\s+TEXT|TEXT\s+INVENTORY)\b",
    "visual language": r"(?im)^(?:COLOR|COLOUR|PALETTE|VISUAL\s+LANGUAGE|ICON).*\b",
    "negative constraints": r"(?im)^(?:STRICT\s+)?(?:NEGATIVE|AVOID|PROHIBITED).*\b",
    "final validation": r"(?im)^(?:FINAL\b.*(?:VALIDATION|AUDIT|CHECKLIST|CHECK)\b|(?:VALIDATION|AUDIT|CHECKLIST|CHECK)\b)",
}

PLACEHOLDER_RE = re.compile(r"<[^>\n]{1,100}>|\[(?:TODO|TBD|INSERT|PLACEHOLDER)[^\]]*\]", re.I)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate the structure of a scientific image-generation prompt."
    )
    parser.add_argument("prompt", type=Path, help="Markdown or text prompt to inspect")
    parser.add_argument(
        "--allow-placeholders",
        action="store_true",
        help="Permit unresolved template placeholders",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if not args.prompt.is_file():
        print(f"ERROR: prompt file not found: {args.prompt}")
        return 2

    text = args.prompt.read_text(encoding="utf-8")
    errors: list[str] = []
    warnings: list[str] = []

    for name, pattern in SECTION_PATTERNS.items():
        if not re.search(pattern, text):
            errors.append(f"missing section: {name}")

    if not args.allow_placeholders:
        placeholders = sorted(set(PLACEHOLDER_RE.findall(text)))
        if placeholders:
            preview = ", ".join(placeholders[:5])
            errors.append(f"unresolved placeholders: {preview}")

    word_count = len(re.findall(r"\b[\w'’-]+\b", text, re.UNICODE))
    if word_count < 350:
        warnings.append(
            f"prompt is compact ({word_count} words); verify that local panel rules are sufficient"
        )
    elif word_count > 6000:
        warnings.append(
            f"prompt is very long ({word_count} words); remove adjective repetition and conflicts"
        )

    lower = text.lower()
    if "reference" in lower:
        has_role = any(token in lower for token in ("style reference", "reference only", "input roles"))
        has_isolation = any(token in lower for token in ("ignore", "do not copy", "prohibit", "must not reproduce"))
        if not has_role:
            warnings.append("reference is mentioned without an explicit input role")
        if not has_isolation:
            warnings.append("reference is mentioned without a content-isolation rule")

    if "pending" in lower:
        protects_pending = (
            ("green" in lower and any(token in lower for token in ("no green", "do not use green", "never use green")))
            or any(token in lower for token in ("no winner", "do not imply", "must not imply"))
        )
        if not protects_pending:
            warnings.append("PENDING appears without an explicit anti-success constraint")

    if not re.search(r'["“][^"”\n]{1,100}["”]', text):
        warnings.append("no quoted verbatim visible-text labels found")

    if "arrow" in lower and not any(
        token in lower for token in ("connect", "terminate", "endpoint", "direction")
    ):
        warnings.append("arrows are specified without endpoint or direction rules")

    if not any(token in lower for token in ("must not imply", "do not imply", "never infer")):
        warnings.append("scientific non-claims are not explicitly protected")

    if errors:
        print("FAIL")
        for item in errors:
            print(f"ERROR: {item}")
    else:
        print("PASS")

    for item in warnings:
        print(f"WARNING: {item}")

    print(f"SUMMARY: {len(errors)} error(s), {len(warnings)} warning(s), {word_count} words")
    print("NOTE: static structure checks do not replace semantic or reference-fidelity review")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
