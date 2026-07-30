#!/usr/bin/env python3
"""Static checks for layered scientific figure prompts."""

from __future__ import annotations

import argparse
import re
import sys
import tomllib
from pathlib import Path
from typing import Any

from validate_style_profile import load_profile, validate_profile


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
ITERATION_SECTION_RE = re.compile(
    r"(?im)^(?:REVISION\s+SCOPE(?:\s+AND)?\s+STYLE\s+LOCK|STYLE\s+LOCK)\b"
)
STYLE_PROFILE_SECTION_RE = re.compile(r"(?im)^PROJECT\s+STYLE\s+PROFILE\b")
OPERATIONAL_ID_RE = re.compile(
    r"(?i)\b(?:job|run|experiment)\s*(?:id\s*)?(?:[#~:_-]\s*)?\d{4,}\b"
)
OPERATIONAL_HASH_RE = re.compile(
    r"(?i)\b(?:sha(?:-?256)?|commit|artifact\s+hash|hash)\s*[:=]?\s*[0-9a-f]{7,64}\b"
)
ASPECT_RATIO_RE = re.compile(
    r"\b(\d+(?:\.\d+)?)[ \t]*:[ \t]*(\d+(?:\.\d+)?)\b"
)

COUNT_WORDS = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
    "ten": 10,
}
COUNT_TOKEN = r"(?:\d+|one|two|three|four|five|six|seven|eight|nine|ten)"
LAYER_COUNT_RE = re.compile(rf"(?i)\b({COUNT_TOKEN})\s*(?:-| )\s*layers?\b")
OUTPUT_COUNT_RES = (
    re.compile(
        rf"(?i)\b(?:output\s+)?dim(?:ension)?\s*(?:=|of|is)?\s*({COUNT_TOKEN})\b"
    ),
    re.compile(
        rf"(?i)\b({COUNT_TOKEN})\s+(?:distinct\s+)?(?:output\s+)?"
        r"(?:heads?|components?|outputs?)\b"
    ),
)
EXACT_PANEL_COUNT_RE = re.compile(
    rf"(?i)\b(?:contains?\s+)?exactly\s+({COUNT_TOKEN})\s+panels?\b"
)


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
    parser.add_argument(
        "--iteration",
        action="store_true",
        help="Require a revision-scope/style-lock contract and audit its invariants",
    )
    parser.add_argument(
        "--style-profile",
        type=Path,
        help="Validate project-wide style binding against figure-style.toml",
    )
    return parser.parse_args()


def parse_count(token: str) -> int:
    token = token.lower()
    return int(token) if token.isdigit() else COUNT_WORDS[token]


def validate_text(
    text: str,
    *,
    allow_placeholders: bool = False,
    iteration: bool = False,
    style_profile: dict[str, Any] | None = None,
) -> tuple[list[str], list[str], int]:
    errors: list[str] = []
    warnings: list[str] = []

    for name, pattern in SECTION_PATTERNS.items():
        if not re.search(pattern, text):
            errors.append(f"missing section: {name}")

    if iteration and not ITERATION_SECTION_RE.search(text):
        errors.append("iteration prompt missing REVISION SCOPE AND STYLE LOCK section")

    if style_profile is not None:
        profile_errors, profile_warnings = validate_profile(style_profile)
        errors.extend(f"style profile: {item}" for item in profile_errors)
        warnings.extend(f"style profile: {item}" for item in profile_warnings)

        if not STYLE_PROFILE_SECTION_RE.search(text):
            errors.append("prompt missing PROJECT STYLE PROFILE section")

        profile_id = style_profile.get("profile_id")
        if isinstance(profile_id, str) and profile_id.lower() not in text.lower():
            errors.append(f"prompt does not bind style profile ID: {profile_id}")

        profile_version = style_profile.get("profile_version")
        if isinstance(profile_version, int) and not re.search(
            rf"(?i)profile\s+version\s*:\s*[\"']?{profile_version}\b", text
        ):
            errors.append(
                f"prompt does not bind style profile version: {profile_version}"
            )

        validation = style_profile.get("validation", {})
        if isinstance(validation, dict):
            required_tokens = validation.get("required_prompt_tokens", [])
            if isinstance(required_tokens, list):
                missing_tokens = [
                    str(token)
                    for token in required_tokens
                    if str(token).lower() not in text.lower()
                ]
                if missing_tokens:
                    errors.append(
                        "prompt omits required project-style tokens: "
                        + ", ".join(missing_tokens[:8])
                    )

    if not allow_placeholders:
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

    if iteration:
        if "preserve" not in lower:
            warnings.append("style lock does not explicitly say what to preserve")
        lock_categories = {
            "canvas/aspect": ("canvas", "aspect"),
            "density/whitespace": ("density", "whitespace", "white space"),
            "palette/color": ("palette", "color", "colour"),
            "typography/icons": ("typography", "font", "icon"),
        }
        for name, tokens in lock_categories.items():
            if not any(token in lower for token in tokens):
                warnings.append(f"style lock does not mention {name}")

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

    operational_ids = sorted(set(OPERATIONAL_ID_RE.findall(text)))
    if operational_ids:
        warnings.append(
            "operational identifier may leak into visible content: "
            + ", ".join(operational_ids[:3])
        )

    operational_hashes = sorted(set(OPERATIONAL_HASH_RE.findall(text)))
    if operational_hashes:
        warnings.append(
            "operational hash may leak into visible content: "
            + ", ".join(operational_hashes[:3])
        )

    aspect_ratios = {
        f"{left}:{right}" for left, right in ASPECT_RATIO_RE.findall(text)
    }
    if len(aspect_ratios) > 1:
        warnings.append(
            "conflicting aspect-ratio targets: " + ", ".join(sorted(aspect_ratios))
        )

    exact_panel_counts = {
        parse_count(token) for token in EXACT_PANEL_COUNT_RE.findall(text)
    }
    if len(exact_panel_counts) > 1:
        warnings.append(
            "conflicting exact panel counts: "
            + ", ".join(str(value) for value in sorted(exact_panel_counts))
        )

    layer_counts = {parse_count(token) for token in LAYER_COUNT_RE.findall(text)}
    output_counts: set[int] = set()
    for pattern in OUTPUT_COUNT_RES:
        output_counts.update(parse_count(token) for token in pattern.findall(text))

    repeated_counts = layer_counts & output_counts
    architecture_guards = (
        "layer-specific",
        "layer specific",
        "only the complete",
        "one outgoing",
        "single outgoing",
        "do not map",
        "not map",
        "independent properties",
        "not three separate",
    )
    if repeated_counts and not any(token in lower for token in architecture_guards):
        warnings.append(
            "architecture count ambiguity: layer count and output count both use "
            + ", ".join(str(value) for value in sorted(repeated_counts))
            + "; explicitly prohibit a layer-to-output mapping"
        )

    return errors, warnings, word_count


def main() -> int:
    args = parse_args()
    if not args.prompt.is_file():
        print(f"ERROR: prompt file not found: {args.prompt}")
        return 2

    style_profile: dict[str, Any] | None = None
    if args.style_profile is not None:
        if not args.style_profile.is_file():
            print(f"ERROR: style profile not found: {args.style_profile}")
            return 2
        try:
            style_profile = load_profile(args.style_profile)
        except tomllib.TOMLDecodeError as exc:
            print("FAIL")
            print(f"ERROR: invalid style-profile TOML: {exc}")
            return 1

    text = args.prompt.read_text(encoding="utf-8")
    errors, warnings, word_count = validate_text(
        text,
        allow_placeholders=args.allow_placeholders,
        iteration=args.iteration,
        style_profile=style_profile,
    )

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
