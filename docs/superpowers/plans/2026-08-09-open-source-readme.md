# Open-Source README Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Publish `craft-scientific-figure-prompts` as a polished, bilingual, MIT-licensed Agent Skill repository with truthful documentation, a distinctive scientific identity, and passing CI.

**Architecture:** Keep the existing skill and validators unchanged. Add a documentation layer made of two parity-checked READMEs and one self-contained SVG, plus a small repository-contract test that protects links, translation structure, license text, and CI wiring. Push verified commits while the repository is still private, then update metadata and make visibility Public as the final state change.

**Tech Stack:** GitHub-flavored Markdown, SVG 1.1-compatible XML, Python 3.11+ standard library, GitHub Actions, GitHub CLI.

## Global Constraints

- `README.md` is the canonical English document; `README.zh-CN.md` is a complete Simplified Chinese counterpart.
- Primary audience is users of general AI agents, not only Codex users.
- The visual palette is white, indigo, violet, cyan, and slate; body text remains native GitHub Markdown.
- The skill creates and audits scientific image-generation prompts by default; it does not claim to generate images itself.
- Existing `SKILL.md`, references, validators, and validator tests remain behaviorally unchanged.
- The license is MIT with `Copyright (c) 2026 kikixiong`.
- CI uses `actions/checkout@v7` and `actions/setup-python@v7`, the current stable action majors verified on 2026-08-09.
- Python 3.11 is the minimum because the validators import `tomllib` from the standard library.
- Codex paths and behavior link to the current [official OpenAI documentation](https://developers.openai.com/codex/skills).
- Claude Code paths and behavior link to the current [official Claude Code documentation](https://code.claude.com/docs/en/skills).
- Cursor compatibility links to the current [official Cursor Agent Skills documentation](https://cursor.com/docs/skills).
- No benchmark, endorsement, compatibility, or status claim may be invented.
- Repository visibility changes from Private to Public only after remote tests pass.

## File map

- Create `scripts/test_repository_docs.py`: standard-library contract tests for packaging, bilingual documentation, links, and the hero asset.
- Create `LICENSE`: MIT license text.
- Create `.github/workflows/tests.yml`: run every `scripts/test_*.py` test on Python 3.11–3.14.
- Create `assets/readme-hero.svg`: self-contained scientific workflow hero.
- Create `README.md`: canonical English overview and usage guide.
- Create `README.zh-CN.md`: full Simplified Chinese translation.
- Preserve `SKILL.md`, `references/**`, `scripts/validate_*.py`, and their existing tests.

---

### Task 1: Repository contract, MIT license, and CI

**Files:**

- Create: `scripts/test_repository_docs.py`
- Create: `LICENSE`
- Create: `.github/workflows/tests.yml`

**Interfaces:**

- Consumes: repository root resolved from `Path(__file__).resolve().parents[1]`.
- Produces: `RepositoryPackagingTests`, the MIT license file, and a workflow named `Tests` that later README badges can reference as `tests.yml`.

- [ ] **Step 1: Write failing packaging tests**

Create `scripts/test_repository_docs.py` with:

```python
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
```

- [ ] **Step 2: Run the packaging tests and verify failure**

Run:

```bash
python -m unittest scripts.test_repository_docs -v
```

Expected: two errors caused by missing `LICENSE` and `.github/workflows/tests.yml`.

- [ ] **Step 3: Add the MIT license**

Create `LICENSE` with the standard MIT text and this exact header:

```text
MIT License

Copyright (c) 2026 kikixiong
```

The permission grant and warranty disclaimer must be the unmodified standard MIT License text.

- [ ] **Step 4: Add the GitHub Actions workflow**

Create `.github/workflows/tests.yml`:

```yaml
name: Tests

on:
  push:
    branches: [main]
  pull_request:

permissions:
  contents: read

jobs:
  test:
    name: Python ${{ matrix.python-version }}
    runs-on: ubuntu-latest
    strategy:
      fail-fast: false
      matrix:
        python-version: ["3.11", "3.12", "3.13", "3.14"]
    steps:
      - name: Check out repository
        uses: actions/checkout@v7
      - name: Set up Python
        uses: actions/setup-python@v7
        with:
          python-version: ${{ matrix.python-version }}
      - name: Run tests
        run: python -m unittest discover -s scripts -p 'test_*.py'
```

- [ ] **Step 5: Run tests and verify pass**

Run:

```bash
python -m unittest discover -s scripts -p 'test_*.py'
```

Expected: 17 tests pass.

- [ ] **Step 6: Commit the packaging foundation**

```bash
git add LICENSE .github/workflows/tests.yml scripts/test_repository_docs.py
git commit -m "chore: add MIT license and test workflow"
```

---

### Task 2: Scientific hero asset

**Files:**

- Modify: `scripts/test_repository_docs.py`
- Create: `assets/readme-hero.svg`

**Interfaces:**

- Consumes: the indigo-violet-cyan visual system from the approved design.
- Produces: a self-contained `1440 × 480` SVG with accessible title and description, referenced by both READMEs.

- [ ] **Step 1: Add a failing hero contract test**

Add `import xml.etree.ElementTree as ET` and this test method:

```python
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
```

- [ ] **Step 2: Run the hero test and verify failure**

Run:

```bash
python -m unittest scripts.test_repository_docs.RepositoryPackagingTests.test_hero_is_accessible_self_contained_svg -v
```

Expected: error because `assets/readme-hero.svg` does not exist.

- [ ] **Step 3: Create the hero SVG**

Create a self-contained `assets/readme-hero.svg` with:

```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1440 480" role="img" aria-labelledby="title desc">
  <title id="title">Scientific Figure Prompt Engineer</title>
  <desc id="desc">A five-stage workflow from reference analysis to validated scientific image-generation prompts.</desc>
  <defs>
    <linearGradient id="background" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#F8FAFF"/>
      <stop offset="0.55" stop-color="#F4F1FF"/>
      <stop offset="1" stop-color="#ECFEFF"/>
    </linearGradient>
    <linearGradient id="brand" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#4F46E5"/>
      <stop offset="0.55" stop-color="#7C3AED"/>
      <stop offset="1" stop-color="#0891B2"/>
    </linearGradient>
    <filter id="shadow" x="-20%" y="-20%" width="140%" height="160%">
      <feDropShadow dx="0" dy="8" stdDeviation="12" flood-color="#312E81" flood-opacity="0.10"/>
    </filter>
  </defs>
  <rect width="1440" height="480" rx="28" fill="url(#background)"/>
  <circle cx="118" cy="92" r="54" fill="#C7D2FE" opacity="0.45"/>
  <circle cx="1320" cy="386" r="82" fill="#A5F3FC" opacity="0.38"/>
  <text x="720" y="78" text-anchor="middle" font-family="Inter, ui-sans-serif, system-ui, sans-serif" font-size="18" font-weight="700" letter-spacing="3" fill="#6366F1">AGENT SKILL</text>
  <text x="720" y="130" text-anchor="middle" font-family="Inter, ui-sans-serif, system-ui, sans-serif" font-size="42" font-weight="750" fill="#172554">Scientific Figure Prompt Engineer</text>
  <text x="720" y="168" text-anchor="middle" font-family="Inter, ui-sans-serif, system-ui, sans-serif" font-size="20" fill="#475569">Reference-aware · Evidence-grounded · Style-consistent</text>
  <path d="M252 300H1188" stroke="url(#brand)" stroke-width="5" stroke-linecap="round" opacity="0.28"/>
  <g font-family="Inter, ui-sans-serif, system-ui, sans-serif" filter="url(#shadow)">
    <g transform="translate(84 232)">
      <rect width="220" height="140" rx="20" fill="#FFFFFF" stroke="#C7D2FE"/>
      <circle cx="34" cy="34" r="13" fill="#4F46E5"/>
      <text x="58" y="41" font-size="15" font-weight="700" fill="#4338CA">01</text>
      <text x="24" y="88" font-size="20" font-weight="700" fill="#1E293B">Reference</text>
      <text x="24" y="116" font-size="14" fill="#64748B">visual grammar</text>
    </g>
    <g transform="translate(347 232)">
      <rect width="220" height="140" rx="20" fill="#FFFFFF" stroke="#DDD6FE"/>
      <circle cx="34" cy="34" r="13" fill="#6366F1"/>
      <text x="58" y="41" font-size="15" font-weight="700" fill="#4F46E5">02</text>
      <text x="24" y="88" font-size="20" font-weight="700" fill="#1E293B">Style fingerprint</text>
      <text x="24" y="116" font-size="14" fill="#64748B">transferable invariants</text>
    </g>
    <g transform="translate(610 232)">
      <rect width="220" height="140" rx="20" fill="#FFFFFF" stroke="#E9D5FF"/>
      <circle cx="34" cy="34" r="13" fill="#7C3AED"/>
      <text x="58" y="41" font-size="15" font-weight="700" fill="#6D28D9">03</text>
      <text x="24" y="88" font-size="20" font-weight="700" fill="#1E293B">Scientific contract</text>
      <text x="24" y="116" font-size="14" fill="#64748B">evidence and semantics</text>
    </g>
    <g transform="translate(873 232)">
      <rect width="220" height="140" rx="20" fill="#FFFFFF" stroke="#CFFAFE"/>
      <circle cx="34" cy="34" r="13" fill="#0E7490"/>
      <text x="58" y="41" font-size="15" font-weight="700" fill="#0E7490">04</text>
      <text x="24" y="88" font-size="20" font-weight="700" fill="#1E293B">Production prompt</text>
      <text x="24" y="116" font-size="14" fill="#64748B">rendering contract</text>
    </g>
    <g transform="translate(1136 232)">
      <rect width="220" height="140" rx="20" fill="#FFFFFF" stroke="#A5F3FC"/>
      <circle cx="34" cy="34" r="13" fill="#0891B2"/>
      <text x="58" y="41" font-size="15" font-weight="700" fill="#0E7490">05</text>
      <text x="24" y="88" font-size="20" font-weight="700" fill="#1E293B">Validation</text>
      <text x="24" y="116" font-size="14" fill="#64748B">semantic audit</text>
    </g>
  </g>
  <g fill="#FFFFFF" stroke="#6366F1" stroke-width="3">
    <circle cx="325" cy="301" r="7"/><circle cx="588" cy="301" r="7"/>
    <circle cx="851" cy="301" r="7"/><circle cx="1114" cy="301" r="7"/>
  </g>
  <text x="720" y="430" text-anchor="middle" font-family="Inter, ui-sans-serif, system-ui, sans-serif" font-size="15" font-weight="600" fill="#475569">Scientific truth first. Visual consistency throughout.</text>
</svg>
```

- [ ] **Step 4: Validate the SVG and all tests**

Run:

```bash
python -m unittest discover -s scripts -p 'test_*.py'
python -c "import xml.etree.ElementTree as ET; ET.parse('assets/readme-hero.svg')"
```

Expected: 18 tests pass and XML parsing exits 0.

- [ ] **Step 5: Commit the visual identity**

```bash
git add assets/readme-hero.svg scripts/test_repository_docs.py
git commit -m "docs: add scientific README identity"
```

---

### Task 3: Canonical English README

**Files:**

- Modify: `scripts/test_repository_docs.py`
- Create: `README.md`

**Interfaces:**

- Consumes: `assets/readme-hero.svg`, `SKILL.md`, existing references and validators, and official vendor documentation URLs.
- Produces: the canonical public documentation and the badge target for `.github/workflows/tests.yml`.

- [ ] **Step 1: Add failing English README tests**

Add `import re` and the helper:

```python
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
```

Add methods:

```python
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
```

- [ ] **Step 2: Run English README tests and verify failure**

Run:

```bash
python -m unittest \
  scripts.test_repository_docs.RepositoryPackagingTests.test_english_readme_has_required_structure \
  scripts.test_repository_docs.RepositoryPackagingTests.test_english_readme_local_links_resolve -v
```

Expected: errors because `README.md` does not exist.

- [ ] **Step 3: Write the hero and badge block**

Start `README.md` with this structure and exact claims:

```markdown
<p align="center">
  <img src="assets/readme-hero.svg" width="100%" alt="Scientific Figure Prompt Engineer — a five-stage workflow from reference analysis to prompt validation">
</p>

<p align="center"><strong>Turn reference figures into scientifically faithful, style-consistent image-generation prompts.</strong></p>

<p align="center">
  <strong>English</strong> · <a href="README.zh-CN.md">简体中文</a>
</p>

<p align="center">
  <a href="https://github.com/kikixiong/craft-scientific-figure-prompts/actions/workflows/tests.yml"><img alt="Tests" src="https://github.com/kikixiong/craft-scientific-figure-prompts/actions/workflows/tests.yml/badge.svg"></a>
  <a href="LICENSE"><img alt="MIT License" src="https://img.shields.io/github/license/kikixiong/craft-scientific-figure-prompts?color=4F46E5"></a>
  <img alt="Agent Skill" src="https://img.shields.io/badge/Agent%20Skill-SKILL.md-7C3AED">
  <img alt="Python 3.11+" src="https://img.shields.io/badge/Python-3.11%2B-0891B2">
</p>
```

- [ ] **Step 4: Write the English content in the approved order**

Use these exact level-two headings:

```markdown
## Why this skill
## What it can do
## How it works
## Quick start
## Use it with your agent
## Validate your prompts
## Project-wide visual consistency
## Project structure
## Design principles
## Contributing
## License
```

Required content:

- Explain the failure mode: visually polished prompts can still leak reference content, invent evidence, collapse model/layer/hop semantics, or drift between figures.
- Define the five modes in a compact table: Learn, Adapt, Template, Audit, Iterate.
- Render the five-stage workflow as a Mermaid `flowchart LR` matching the hero labels.
- State the portable flow: install the complete folder, let the agent discover `SKILL.md`, provide a reference and scientific source, choose a mode, validate saved artifacts.
- Give a Codex/Cursor-compatible user install command:

```bash
mkdir -p ~/.agents/skills
git clone https://github.com/kikixiong/craft-scientific-figure-prompts.git \
  ~/.agents/skills/craft-scientific-figure-prompts
```

- Give a Claude Code user install command:

```bash
mkdir -p ~/.claude/skills
git clone https://github.com/kikixiong/craft-scientific-figure-prompts.git \
  ~/.claude/skills/craft-scientific-figure-prompts
```

- Give a generic fallback: clone anywhere, then explicitly tell the agent to read the repository's `SKILL.md` and follow it for the task.
- Link the product names in the integration table to their official skill documentation.
- Use this truthful invocation example:

```text
Use craft-scientific-figure-prompts in Adapt mode.

Treat the attached figure as visual grammar only. Use my paper as the
scientific source of truth. Produce a style fingerprint, a scientific content
contract, a copy-paste production prompt, and an audit note. Do not generate
an image yet.
```

- Show both validator commands exactly:

```bash
python scripts/validate_style_profile.py .codex/figure-style.toml
python scripts/validate_prompt.py \
  --style-profile .codex/figure-style.toml \
  path/to/production-prompt.md
```

- Link every item in the project map to a real repository path.
- State that contributions should preserve scientific truth, evidence-state scoping, and semantic distinctions.
- End with `Released under the [MIT License](LICENSE).`

- [ ] **Step 5: Run English documentation tests**

Run:

```bash
python -m unittest scripts.test_repository_docs -v
```

Expected: all repository-document tests pass at this stage.

- [ ] **Step 6: Commit the English README**

```bash
git add README.md scripts/test_repository_docs.py
git commit -m "docs: add agent-neutral project guide"
```

---

### Task 4: Full Simplified Chinese README

**Files:**

- Modify: `scripts/test_repository_docs.py`
- Create: `README.zh-CN.md`

**Interfaces:**

- Consumes: the final English README structure and all paths, commands, capability boundaries, and official links.
- Produces: a complete translation with matching major-section count and identical local targets.

- [ ] **Step 1: Add failing Chinese and parity tests**

Add methods:

```python
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

    def test_bilingual_readmes_have_section_parity(self) -> None:
        english = (ROOT / "README.md").read_text(encoding="utf-8")
        chinese = (ROOT / "README.zh-CN.md").read_text(encoding="utf-8")
        self.assertEqual(english.count("\n## "), chinese.count("\n## "))
        english_targets = local_targets(english)
        chinese_targets = local_targets(chinese)
        self.assertIn("README.zh-CN.md", english_targets)
        self.assertIn("README.md", chinese_targets)
        self.assertEqual(
            english_targets - {"README.zh-CN.md"},
            chinese_targets - {"README.md"},
        )
```

- [ ] **Step 2: Run Chinese tests and verify failure**

Run:

```bash
python -m unittest \
  scripts.test_repository_docs.RepositoryPackagingTests.test_chinese_readme_has_required_structure \
  scripts.test_repository_docs.RepositoryPackagingTests.test_chinese_readme_local_links_resolve \
  scripts.test_repository_docs.RepositoryPackagingTests.test_bilingual_readmes_have_section_parity -v
```

Expected: errors because `README.zh-CN.md` does not exist.

- [ ] **Step 3: Write the complete Chinese counterpart**

Mirror every English section and keep all commands, paths, product names, links, Mermaid node IDs, and capability names unchanged. Use these headings in matching order:

```markdown
## 为什么需要这个技能
## 它能做什么
## 工作原理
## 快速开始
## 在不同 Agent 中使用
## 验证提示词
## 项目级视觉一致性
## 项目结构
## 设计原则
## 参与贡献
## 许可证
```

Start with the same hero and badges, but switch the language line to:

```html
<p align="center">
  <a href="README.md">English</a> · <strong>简体中文</strong>
</p>
```

Translate prose idiomatically rather than word-for-word. Preserve these distinctions explicitly:

- reference visual grammar versus target scientific content;
- verified, preliminary, pending, limitation, and failed evidence states;
- model count, sequential depth, hops, branches, and output dimensions;
- local revision versus project-wide style change;
- prompt generation versus image generation.

End with `本项目采用 [MIT 许可证](LICENSE) 发布。`

- [ ] **Step 4: Run bilingual tests**

Run:

```bash
python -m unittest discover -s scripts -p 'test_*.py'
```

Expected: 23 tests pass.

- [ ] **Step 5: Commit the Chinese README**

```bash
git add README.zh-CN.md scripts/test_repository_docs.py
git commit -m "docs: add complete Chinese README"
```

---

### Task 5: Verify, push, and publish the repository

**Files:**

- Verify: all tracked files
- External state: `kikixiong/craft-scientific-figure-prompts` metadata and visibility

**Interfaces:**

- Consumes: all local implementation commits and authenticated `gh` access for owner `kikixiong`.
- Produces: remote `main` at the local HEAD, passing GitHub Actions, updated description/topics, and Public visibility.

- [ ] **Step 1: Run the complete local verification suite**

Run:

```bash
python -m unittest discover -s scripts -p 'test_*.py'
python scripts/validate_prompt.py --help >/dev/null
python scripts/validate_style_profile.py --help >/dev/null
python -c "import xml.etree.ElementTree as ET; ET.parse('assets/readme-hero.svg')"
ruby -e 'require "yaml"; YAML.load_file(".github/workflows/tests.yml")'
git diff --check
git status --short --branch
```

Expected: 23 tests pass; every command exits 0; the branch is ahead of `origin/main` with no uncommitted files.

- [ ] **Step 2: Review the aggregate diff and repository claims**

Run:

```bash
git diff origin/main...HEAD --stat
git diff origin/main...HEAD -- README.md README.zh-CN.md LICENSE .github/workflows/tests.yml
```

Confirm no core skill or validator behavior changed and no private path, token, draft placeholder, fake metric, or unsupported compatibility claim appears.

- [ ] **Step 3: Push all commits to `main`**

Run:

```bash
git push origin main
```

Verify exact SHA agreement:

```bash
local_commit=$(git rev-parse HEAD)
remote_commit=$(git ls-remote origin refs/heads/main | cut -f1)
test "$local_commit" = "$remote_commit"
```

- [ ] **Step 4: Wait for the pushed GitHub Actions workflow**

Run:

```bash
run_id=$(gh run list --repo kikixiong/craft-scientific-figure-prompts \
  --workflow tests.yml --branch main --limit 1 \
  --json databaseId --jq '.[0].databaseId')
test -n "$run_id"
gh run watch "$run_id" --repo kikixiong/craft-scientific-figure-prompts --exit-status
```

Expected: all Python matrix jobs pass. If no run appears immediately, query `gh run list` again rather than publishing an unverified badge.

- [ ] **Step 5: Update repository description and topics while still private**

Run:

```bash
gh repo edit kikixiong/craft-scientific-figure-prompts \
  --description "An Agent Skill for turning reference figures into scientifically faithful, style-consistent image-generation prompts." \
  --add-topic agent-skills \
  --add-topic scientific-figures \
  --add-topic prompt-engineering \
  --add-topic scientific-visualization \
  --add-topic research-tools \
  --add-topic image-generation
```

Verify with:

```bash
gh repo view kikixiong/craft-scientific-figure-prompts \
  --json description,repositoryTopics,visibility,url
```

- [ ] **Step 6: Make the repository public as the final state change**

Run:

```bash
gh repo edit kikixiong/craft-scientific-figure-prompts \
  --visibility public \
  --accept-visibility-change-consequences
```

- [ ] **Step 7: Verify public release state**

Run:

```bash
gh repo view kikixiong/craft-scientific-figure-prompts \
  --json defaultBranchRef,description,licenseInfo,repositoryTopics,url,visibility
curl -fsSL https://raw.githubusercontent.com/kikixiong/craft-scientific-figure-prompts/main/README.md >/dev/null
curl -fsSL https://raw.githubusercontent.com/kikixiong/craft-scientific-figure-prompts/main/README.zh-CN.md >/dev/null
git status --short --branch
```

Expected: visibility is `PUBLIC`, both anonymous raw README requests succeed, license is MIT once GitHub indexing completes, and local `main` matches `origin/main` with a clean tree.
