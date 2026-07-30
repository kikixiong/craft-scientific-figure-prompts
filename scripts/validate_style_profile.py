#!/usr/bin/env python3
"""Validate a project-level scientific figure style profile."""

from __future__ import annotations

import argparse
import re
import sys
import tomllib
from pathlib import Path
from typing import Any


REQUIRED_TOP_LEVEL = (
    "profile_version",
    "profile_id",
    "project",
    "status",
    "authority",
    "updated",
)
REQUIRED_SECTIONS = {
    "canvas": (
        "default_aspect_ratio",
        "allowed_aspect_ratios",
        "orientation",
        "background",
        "margin_behavior",
    ),
    "typography": ("display", "label", "technical", "equation", "casing"),
    "palette": ("dominant", "accents", "semantic", "forbidden"),
    "density": ("level", "internal_whitespace", "label_budget", "module_scale"),
    "icons": ("family", "outline", "shading"),
    "containers": ("border", "title_tabs", "corner_style", "panel_fill_behavior"),
    "arrows": ("major", "minor", "crossing_policy"),
    "anti_style": ("forbidden",),
    "validation": ("required_prompt_tokens",),
}
PLACEHOLDER_RE = re.compile(r"REPLACE_ME|YYYY-MM-DD|<[^>]+>|\b(?:TODO|TBD)\b", re.I)
HEX_COLOR_RE = re.compile(r"^#[0-9A-Fa-f]{6}$")
ISO_DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate a project-level figure-style TOML profile."
    )
    parser.add_argument("profile", type=Path, help="Path to figure-style.toml")
    return parser.parse_args()


def load_profile(path: Path) -> dict[str, Any]:
    with path.open("rb") as handle:
        return tomllib.load(handle)


def _is_blank(value: Any) -> bool:
    return value is None or value == "" or value == []


def _find_placeholders(value: Any, path: str = "") -> list[str]:
    found: list[str] = []
    if isinstance(value, dict):
        for key, child in value.items():
            child_path = f"{path}.{key}" if path else key
            found.extend(_find_placeholders(child, child_path))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            found.extend(_find_placeholders(child, f"{path}[{index}]"))
    elif isinstance(value, str) and PLACEHOLDER_RE.search(value):
        found.append(path)
    return found


def validate_profile(profile: dict[str, Any]) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    for key in REQUIRED_TOP_LEVEL:
        if key not in profile:
            errors.append(f"missing top-level field: {key}")
        elif _is_blank(profile[key]):
            errors.append(f"blank top-level field: {key}")

    version = profile.get("profile_version")
    if version is not None and (not isinstance(version, int) or version < 1):
        errors.append("profile_version must be a positive integer")

    status = profile.get("status")
    if status not in (None, "draft", "accepted"):
        errors.append("status must be 'draft' or 'accepted'")
    elif status == "draft":
        warnings.append("style profile is draft; obtain user acceptance before freezing it")

    updated = profile.get("updated")
    if isinstance(updated, str) and not ISO_DATE_RE.fullmatch(updated):
        errors.append("updated must use YYYY-MM-DD")

    for section_name, keys in REQUIRED_SECTIONS.items():
        section = profile.get(section_name)
        if not isinstance(section, dict):
            errors.append(f"missing section: {section_name}")
            continue
        for key in keys:
            if key not in section:
                errors.append(f"missing field: {section_name}.{key}")
            elif _is_blank(section[key]):
                errors.append(f"blank field: {section_name}.{key}")

    placeholders = _find_placeholders(profile)
    if placeholders:
        errors.append(
            "unresolved placeholders: " + ", ".join(sorted(placeholders)[:8])
        )

    canvas = profile.get("canvas", {})
    if isinstance(canvas, dict):
        default_aspect = canvas.get("default_aspect_ratio")
        allowed_aspects = canvas.get("allowed_aspect_ratios")
        if (
            isinstance(default_aspect, str)
            and isinstance(allowed_aspects, list)
            and default_aspect not in allowed_aspects
        ):
            errors.append(
                "canvas.default_aspect_ratio must appear in allowed_aspect_ratios"
            )
        background = canvas.get("background")
        if isinstance(background, str) and not HEX_COLOR_RE.fullmatch(background):
            errors.append("canvas.background must be a #RRGGBB color")

    palette = profile.get("palette", {})
    if isinstance(palette, dict):
        for key in ("dominant", "accents"):
            colors = palette.get(key)
            if isinstance(colors, list):
                invalid = [
                    str(color)
                    for color in colors
                    if not isinstance(color, str) or not HEX_COLOR_RE.fullmatch(color)
                ]
                if invalid:
                    errors.append(
                        f"palette.{key} contains non-#RRGGBB colors: "
                        + ", ".join(invalid[:5])
                    )

    validation = profile.get("validation", {})
    if isinstance(validation, dict):
        required_tokens = validation.get("required_prompt_tokens")
        if isinstance(required_tokens, list):
            if len(required_tokens) > 20:
                warnings.append(
                    "validation.required_prompt_tokens is large; keep only "
                    "project-wide invariants"
                )
            duplicates = {
                token
                for token in required_tokens
                if required_tokens.count(token) > 1
            }
            if duplicates:
                warnings.append(
                    "duplicate required_prompt_tokens: "
                    + ", ".join(sorted(str(item) for item in duplicates))
                )

    return errors, warnings


def main() -> int:
    args = parse_args()
    if not args.profile.is_file():
        print(f"ERROR: style profile not found: {args.profile}")
        return 2

    try:
        profile = load_profile(args.profile)
    except tomllib.TOMLDecodeError as exc:
        print("FAIL")
        print(f"ERROR: invalid TOML: {exc}")
        return 1

    errors, warnings = validate_profile(profile)

    print("FAIL" if errors else "PASS")
    for item in errors:
        print(f"ERROR: {item}")
    for item in warnings:
        print(f"WARNING: {item}")
    print(f"SUMMARY: {len(errors)} error(s), {len(warnings)} warning(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
