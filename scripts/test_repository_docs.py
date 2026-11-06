from __future__ import annotations

import re
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


LINK_PATTERN = re.compile(
    r'!?\[[^\]]*\]\(([^)]+)\)|(?:href|src)="([^"]+)"'
)


def link_targets(markdown: str) -> tuple[str, ...]:
    return tuple(first or second for first, second in LINK_PATTERN.findall(markdown))


def local_targets(markdown: str) -> set[str]:
    return {
        target.split("#", 1)[0]
        for target in link_targets(markdown)
        if target
        and not target.startswith(("http://", "https://", "mailto:", "#"))
    }


def level_two_headings(markdown: str) -> tuple[str, ...]:
    return tuple(re.findall(r"^## (.+)$", markdown, flags=re.MULTILINE))


def shell_blocks(markdown: str) -> tuple[str, ...]:
    return tuple(
        re.findall(r"^```bash\n(.*?)\n```$", markdown, flags=re.MULTILINE | re.DOTALL)
    )


def shell_command_lines(markdown: str) -> tuple[str, ...]:
    return tuple(
        line.strip()
        for block in shell_blocks(markdown)
        for line in block.splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    )


def command_flags(markdown: str) -> tuple[str, ...]:
    return tuple(
        re.findall(
            r"(?<![\w-])--[a-z][a-z-]*", "\n".join(shell_command_lines(markdown))
        )
    )


def external_targets(markdown: str) -> tuple[str, ...]:
    return tuple(
        target
        for target in link_targets(markdown)
        if target.startswith(("http://", "https://"))
    )


def without_whitespace(text: str) -> str:
    return re.sub(r"\s+", "", text)


def local_link_inventory(markdown: str) -> tuple[str, ...]:
    return tuple(
        "LANGUAGE_README"
        if target in {"README.md", "README.zh-CN.md"}
        else target.split("#", 1)[0]
        for target in link_targets(markdown)
        if target
        and not target.startswith(("http://", "https://", "mailto:", "#"))
    )


class RepositoryPackagingTests(unittest.TestCase):
    def test_hero_is_accessible_self_contained_svg(self) -> None:
        hero_path = ROOT / "assets/readme-hero.svg"
        root = ET.parse(hero_path).getroot()
        self.assertEqual(root.tag, "{http://www.w3.org/2000/svg}svg")
        self.assertEqual(root.attrib["viewBox"], "0 0 1440 480")
        self.assertEqual(root.attrib["role"], "img")
        self.assertEqual(root.attrib["aria-labelledby"], "title desc")
        self.assertNotIn("aria-label", root.attrib)
        namespace = {"svg": "http://www.w3.org/2000/svg"}
        title = root.find("svg:title", namespace)
        description = root.find("svg:desc", namespace)
        self.assertIsNotNone(title)
        self.assertIsNotNone(description)
        assert title is not None
        assert description is not None
        self.assertEqual(title.attrib["id"], "title")
        self.assertEqual(description.attrib["id"], "desc")
        self.assertEqual(title.text, "Scientific Figure Prompt Engineer")
        self.assertIn("five-stage workflow", description.text or "")
        svg_text = hero_path.read_text(encoding="utf-8")
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

    def test_chinese_readme_has_required_structure(self) -> None:
        readme = (ROOT / "README.zh-CN.md").read_text(encoding="utf-8")
        required = (
            "assets/readme-hero.svg",
            "README.md",
            "## 为什么需要这个技能",
            "## 它能做什么",
            "## 工作原理",
            "## 快速开始",
            "## 在不同 Agent 中使用",
            "## 验证提示词",
            "## 项目结构",
            "## 设计原则",
            "## 参与贡献",
            "## 许可证",
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

    def test_chinese_readme_local_links_resolve(self) -> None:
        readme = (ROOT / "README.zh-CN.md").read_text(encoding="utf-8")
        for target in local_targets(readme):
            with self.subTest(target=target):
                self.assertTrue((ROOT / target).exists(), target)

    def test_bilingual_readmes_have_ordered_section_parity(self) -> None:
        english = (ROOT / "README.md").read_text(encoding="utf-8")
        chinese = (ROOT / "README.zh-CN.md").read_text(encoding="utf-8")
        expected_heading_pairs = (
            ("Why this skill", "为什么需要这个技能"),
            ("What it can do", "它能做什么"),
            ("How it works", "工作原理"),
            ("Quick start", "快速开始"),
            ("Use it with your agent", "在不同 Agent 中使用"),
            ("Validate your prompts", "验证提示词"),
            ("Project-wide visual consistency", "项目级视觉一致性"),
            ("Project structure", "项目结构"),
            ("Design principles", "设计原则"),
            ("Contributing", "参与贡献"),
            ("License", "许可证"),
        )
        self.assertEqual(
            level_two_headings(english),
            tuple(pair[0] for pair in expected_heading_pairs),
        )
        self.assertEqual(
            level_two_headings(chinese),
            tuple(pair[1] for pair in expected_heading_pairs),
        )

    def test_bilingual_readmes_have_command_flag_and_link_parity(self) -> None:
        english = (ROOT / "README.md").read_text(encoding="utf-8")
        chinese = (ROOT / "README.zh-CN.md").read_text(encoding="utf-8")
        self.assertEqual(shell_command_lines(english), shell_command_lines(chinese))
        self.assertEqual(command_flags(english), command_flags(chinese))
        self.assertIn("--allow-placeholders", command_flags(english))
        self.assertIn("--iteration", command_flags(english))
        self.assertEqual(external_targets(english), external_targets(chinese))
        self.assertEqual(
            local_link_inventory(english),
            local_link_inventory(chinese),
        )
        english_targets = local_targets(english)
        chinese_targets = local_targets(chinese)
        self.assertIn("README.zh-CN.md", english_targets)
        self.assertIn("README.md", chinese_targets)
        self.assertEqual(
            english_targets - {"README.zh-CN.md"},
            chinese_targets - {"README.md"},
        )

    def test_bilingual_readmes_preserve_behavioral_boundaries(self) -> None:
        english = (ROOT / "README.md").read_text(encoding="utf-8")
        chinese = (ROOT / "README.zh-CN.md").read_text(encoding="utf-8")
        required_pairs = (
            (
                "Explicit prompt-only requests stop after validation",
                "明确要求只要提示词时，会在验证后停止",
            ),
            (
                "reference normally supplies visual grammar",
                "参考图通常只提供视觉语法",
            ),
            (
                "Scientific truth and evidence state outrank aesthetics",
                "科学事实和证据状态的优先级都高于美观",
            ),
            (
                "versioned authority",
                "版本化权威依据",
            ),
            (
                "Model count, sequential depth, graph hops, computation branches, "
                "output dimensions",
                "模型数量、顺序深度、图跳数、计算分支、输出维度",
            ),
        )
        for english_phrase, chinese_phrase in required_pairs:
            with self.subTest(english_phrase=english_phrase):
                self.assertIn(
                    without_whitespace(english_phrase), without_whitespace(english)
                )
                self.assertIn(
                    without_whitespace(chinese_phrase), without_whitespace(chinese)
                )

    def test_opening_block_links_to_quick_start(self) -> None:
        readmes = (
            ("README.md", '<a href="#quick-start">Start with the quick start</a>'),
            ("README.zh-CN.md", '<a href="#快速开始">从快速开始入门</a>'),
        )
        for filename, link in readmes:
            with self.subTest(filename=filename):
                readme = (ROOT / filename).read_text(encoding="utf-8")
                self.assertIn(link, readme)
                self.assertLess(readme.index(link), readme.index("\n## "))

    def test_documented_validator_commands_match_installed_layout(self) -> None:
        for filename in ("README.md", "README.zh-CN.md"):
            with self.subTest(filename=filename):
                readme = (ROOT / filename).read_text(encoding="utf-8")
                commands = "\n".join(shell_blocks(readme))
                self.assertIn(
                    'SKILL_ROOT="$HOME/.agents/skills/craft-scientific-figure-prompts"',
                    commands,
                )
                self.assertIn(
                    '# SKILL_ROOT="$HOME/.claude/skills/craft-scientific-figure-prompts"',
                    commands,
                )
                self.assertIn('# SKILL_ROOT="/absolute/path/to/', commands)
                self.assertIn(
                    'python3 "$SKILL_ROOT/scripts/validate_style_profile.py"',
                    commands,
                )
                self.assertIn(
                    'python3 "$SKILL_ROOT/scripts/validate_prompt.py"',
                    commands,
                )
                self.assertNotIn("python scripts/validate_", commands)

    def test_template_mode_documents_placeholder_validation_contract(self) -> None:
        for filename in ("README.md", "README.zh-CN.md"):
            with self.subTest(filename=filename):
                readme = (ROOT / filename).read_text(encoding="utf-8")
                self.assertIn("**Template**", readme)
                commands = "\n".join(shell_blocks(readme))
                self.assertRegex(
                    commands,
                    r'python3 "\$SKILL_ROOT/scripts/validate_prompt\.py" \\\n'
                    r'(?:.*\n)*?  --allow-placeholders \\\n'
                    r'  path/to/template-prompt\.md',
                )

    def test_chinese_copy_paste_request_is_translated(self) -> None:
        chinese = (ROOT / "README.zh-CN.md").read_text(encoding="utf-8")
        self.assertIn("请以 Adapt 模式使用 craft-scientific-figure-prompts。", chinese)
        self.assertIn("只把附带的图作为视觉语法参考。", chinese)
        self.assertIn("暂时不要生成图像。", chinese)
        self.assertNotIn("Treat the attached figure as visual grammar only.", chinese)


if __name__ == "__main__":
    unittest.main()
