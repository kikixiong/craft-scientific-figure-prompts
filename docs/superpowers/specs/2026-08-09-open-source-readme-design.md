# Open-Source README Design

## Goal

Turn `craft-scientific-figure-prompts` into a polished public repository that
helps a new AI-agent user understand, install, and validate the skill within
minutes. The presentation should feel like a modern scientific tool: precise,
calm, visually distinctive, and free of unsupported claims.

## Audience and language

- Primary audience: users of general-purpose AI agents, including but not
  limited to Codex, Claude Code, Cursor, and agents that can load Markdown
  skills or instruction files.
- Primary README: English (`README.md`) for broad discovery.
- Full translation: Simplified Chinese (`README.zh-CN.md`) with the same
  structure and substantive content.
- Both READMEs include a prominent language switch near the top.

## Deliverables

1. `README.md`: the canonical English documentation.
2. `README.zh-CN.md`: a complete Simplified Chinese counterpart.
3. `assets/readme-hero.svg`: an original, lightweight hero graphic.
4. `LICENSE`: the MIT License, copyright 2026 `kikixiong`.
5. `.github/workflows/tests.yml`: a small CI workflow that runs the existing
   Python unit tests so the README can show a truthful build-status badge.
6. GitHub repository metadata: a concise description and relevant topics.
7. Repository visibility changed from Private to Public only after the pushed
   commit and remote checks succeed.

## README information architecture

The two READMEs will follow the same order:

1. Hero, language switch, badges, and one-sentence value proposition.
2. A concise explanation of the problem the skill solves.
3. Core capabilities: Learn, Adapt, Template, Audit, and Iterate.
4. A workflow diagram:
   `Reference -> Style fingerprint -> Scientific content contract -> Production prompt -> Validation`.
5. Quick start with a portable, agent-neutral installation path first.
6. Integration notes for popular AI-agent conventions, clearly distinguishing
   verified conventions from generic manual loading.
7. A copy-paste usage example that reflects the actual `SKILL.md` behavior.
8. Project-wide style profiles and the two validator commands.
9. Repository map linking the most useful references and scripts.
10. Design principles and explicit capability boundaries.
11. Testing, contributing, and MIT license sections.

The first screen should answer three questions without scrolling far: what the
skill does, who it is for, and how to start.

## Visual design

- Use a white canvas with restrained indigo, violet, cyan, and slate accents.
- The SVG hero will depict a five-stage scientific prompting pipeline using
  crisp cards, nodes, and connectors rather than decorative artwork.
- Keep typography dependent on GitHub's native README rendering.
- Use a small number of truthful shields: CI, MIT license, and skill category.
- Avoid badge walls, animated assets, gradients behind body text, fake product
  screenshots, and claims that depend on unpublished benchmarks.
- Supply useful alt text and ensure that all essential information is present
  as Markdown text rather than only inside the hero image.

## Behavioral accuracy

The documentation will preserve these boundaries from `SKILL.md`:

- The skill produces and audits scientific image-generation prompts by
  default; it does not generate an image unless that is separately requested.
- Reference images provide transferable visual grammar, while target research
  provides scientific content.
- Scientific truth and evidence state outrank aesthetics.
- Project-wide style profiles are versioned authorities, not optional mood
  boards.
- Architecture counts such as models, layers, hops, branches, and output
  dimensions remain semantically distinct.

Examples will use generic scientific language and will not invent research
results, performance numbers, endorsements, or compatibility guarantees.

## Installation and usage flow

The canonical path is intentionally portable:

1. Clone or download the repository.
2. Place the repository in the agent's supported skills or instructions
   directory, or explicitly ask the agent to load `SKILL.md`.
3. Supply a reference figure and a target scientific source or brief.
4. Ask for one of the five supported modes.
5. Run the included validators on saved production prompts and style profiles.

Exact tool-specific paths will be included only when supported by current
first-party documentation. Otherwise, the README will use the portable flow
and avoid guessing at unstable product conventions.

## CI and failure handling

The GitHub Actions workflow will use a current stable Python runtime and run:

```bash
python -m unittest discover -s scripts -p 'test_*.py'
```

The workflow adds no runtime dependency and changes no validator behavior. If
CI creation is blocked by repository or account policy, the README will omit
the CI badge rather than display an unverified status.

Before publication, local checks will cover:

- all existing unit tests;
- validator command help and representative validator execution;
- relative links and referenced local assets in both READMEs;
- YAML syntax for the workflow;
- parity of major sections between English and Chinese documents;
- clean Git state after commit and agreement between local and remote `main`.

If push succeeds but the visibility change fails, the repository remains
Private and the failure is reported explicitly. Visibility is the final
external-state change.

## Repository metadata

The repository description will stay concise and agent-neutral. Topics will
cover scientific figures, prompt engineering, agent skills, research
communication, and image generation without keyword stuffing. No homepage URL
will be invented.

## Scope boundaries

This release will not change `SKILL.md`, the reference guides, validators, or
their tests except where a documentation link requires a factual correction.
It will not add generated scientific examples, package publishing, a website,
analytics, or new validator features.

## Release sequence

1. Implement the documentation, SVG asset, license, and CI workflow.
2. Run local verification and inspect the rendered-document structure.
3. Commit all implementation changes on `main` with a focused message.
4. Push `main` to `origin`.
5. Verify the remote commit and Actions workflow registration.
6. Update repository description and topics.
7. Change repository visibility to Public.
8. Re-open the public repository and verify README, license, metadata, and
   visibility.

## Acceptance criteria

- Both languages give a first-time user equivalent, accurate guidance.
- The README has a distinctive scientific visual identity and remains easy to
  scan on desktop and mobile GitHub views.
- Every badge and compatibility statement is backed by repository state or
  first-party documentation.
- Existing tests pass and no existing skill behavior changes.
- The repository contains an MIT license, has useful topics, and is publicly
  accessible after the final verification.
