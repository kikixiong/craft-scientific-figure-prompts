# Project style profile

## Contents

- [Use one canonical profile per project](#use-one-canonical-profile-per-project)
- [Create and accept the profile](#create-and-accept-the-profile)
- [Apply it to every figure](#apply-it-to-every-figure)
- [Handle exceptions and revisions](#handle-exceptions-and-revisions)
- [Profile fields](#profile-fields)
- [Validate consistency](#validate-consistency)

## Use one canonical profile per project

Store project-wide figure style at:

```text
<project-root>/.codex/figure-style.toml
```

Use the repository containing the target paper, thesis, report, or figure
source as `<project-root>`. Do not store project-specific colors, fonts, or
layout choices in the global skill. Do not maintain multiple competing style
profiles inside one project.

Before creating or revising any figure prompt:

1. Search the target project root for `.codex/figure-style.toml`.
2. If it exists, read it completely before inspecting figure-specific style.
3. Treat an accepted profile as the default style authority for every figure
   in the project.
4. State the profile ID and version in the production prompt.

The project profile controls visual continuity. The paper and implementation
remain the authority for scientific content.

## Create and accept the profile

If no profile exists and the project may contain multiple figures:

1. Start from
   [project-figure-style.toml](../assets/project-figure-style.toml).
2. Fill every field from the user's explicit preferences, the selected
   reference, and the latest accepted figure or prompt.
3. Save it at the canonical project path with `status = "draft"`.
4. Use the draft to create the first production prompt.
5. After the user explicitly accepts the style or accepts a generated figure,
   set `status = "accepted"`, record its authority, and keep
   `profile_version = 1`.

Do not mark a profile accepted merely because a prompt validates. Acceptance is
a user decision or is inherited from an artifact the user explicitly approved.

Use exact values where possible:

- named fonts and fallbacks;
- hex colors plus semantic roles;
- density and whitespace targets;
- border, tab, icon, and arrow grammar;
- background and anti-style rules.

## Apply it to every figure

Materialize the profile inside every image-generation prompt. An image model
cannot read the external TOML file, so a profile reference alone is
insufficient.

Add:

```text
PROJECT STYLE PROFILE — REQUIRED
Profile ID: "<profile_id>"
Profile version: "<profile_version>"
Status: "<status>"
Use the project-wide canvas family, typography, palette, density, icon,
container, arrow, and anti-style rules below. Figure-specific content may
change; these visual invariants may not.
```

Then restate all relevant style values in the normal canvas, typography,
palette, density, icon, container, arrow, and negative-constraint sections.

The profile does not force identical layouts across every figure. It creates a
family resemblance:

- the same font roles;
- the same dominant and accent palette;
- the same icon and outline character;
- the same border, tab, and arrow grammar;
- the same information-density rhythm;
- the same background and anti-style;
- a controlled family of allowed aspect ratios.

Choose a figure-specific layout from scientific semantics while keeping that
family resemblance.

## Handle exceptions and revisions

Use a figure-specific exception only when scientific content genuinely needs
it. Declare:

```text
FIGURE-SPECIFIC STYLE EXCEPTION
Property:
Reason:
Scope:
Preserve all other project-profile invariants.
```

Do not write an exception back into the project profile unless it should apply
to future figures too.

When the user changes project-wide style:

1. update the canonical profile;
2. increment `profile_version`;
3. update `authority`, `updated`, and the affected fields;
4. identify existing prompts or figures that now use an older version;
5. do not silently restyle old figures unless the user asks for migration.

When the user changes only one figure, keep the profile version unchanged.

Apply this precedence:

1. scientific truth and evidence status;
2. explicit current-turn user instruction;
3. accepted project style profile;
4. figure-specific reference suggestions;
5. decoration.

## Profile fields

The TOML template records:

- identity, version, status, authority, and update date;
- default and allowed canvas aspect ratios;
- typography roles and casing;
- dominant, accent, semantic, and forbidden colors;
- density, whitespace, label budget, and module scale;
- icon family, outline, and shading;
- borders, title tabs, corners, and panel fills;
- major/minor arrows and crossing policy;
- anti-style constraints;
- tokens that every production prompt must repeat.

Put only true project-wide invariants in `validation.required_prompt_tokens`.
Examples include the profile ID, background hex, principal font, and dominant
palette colors. Do not require a figure-specific panel title or scientific
label.

## Validate consistency

Validate the profile:

```bash
python scripts/validate_style_profile.py \
  <project-root>/.codex/figure-style.toml
```

Validate a production prompt against it:

```bash
python scripts/validate_prompt.py \
  --style-profile <project-root>/.codex/figure-style.toml \
  <prompt.md>
```

For a revision, combine both modes:

```bash
python scripts/validate_prompt.py \
  --iteration \
  --style-profile <project-root>/.codex/figure-style.toml \
  <prompt.md>
```

The static check verifies profile identity, version, status, and required
tokens. Finish with a visual audit across at least one previously accepted
project figure: fonts, colors, density, icons, borders, arrows, and background
should read as one coherent family.
