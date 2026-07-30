# Prompt architecture

## Contents

- [Select a layout pattern](#select-a-layout-pattern)
- [Distinguish architecture relationships](#distinguish-architecture-relationships)
- [Lock style during revision](#lock-style-during-revision)
- [Control visible text](#control-visible-text)
- [Assign semantic visual language](#assign-semantic-visual-language)
- [Use controlled redundancy](#use-controlled-redundancy)
- [Canonical production scaffold](#canonical-production-scaffold)

## Select a layout pattern

### Sequential pipeline

Use for data processing, model stages, or experimental execution.

`inputs → preprocessing → model → outputs → evaluation`

### Two phases with a bridge

Use when two systems are connected by shared interfaces or contracts:

- measurement → intervention;
- training → inference;
- offline construction → online execution;
- discovery → validation.

Place two independent phase containers side by side. Put the shared interface,
contract, memory, or mapping layer across the seam. Do not use this pattern
when the bridge is merely decorative.

### Parallel lanes

Use for arms, baselines, models, or conditions that share inputs but produce
separate downstream artifacts. Keep shared objects outside the lanes. Never
merge outputs when the method requires independent execution.

### Layered stack

Use for provenance, abstraction, network stacks, or hierarchical models.
Arrows should clarify allowed transitions between layers.

### Loop

Use only for real feedback, optimization, monitoring, or human-in-the-loop
cycles. A curved arrow alone must not invent feedback.

### Small multiples

Use for repeated comparable units. Keep scales, labels, and icon grammar
consistent across cells.

## Distinguish architecture relationships

Before drawing a machine-learning architecture, separately record:

- number of models;
- sequential layers per model;
- receptive-field hops;
- real parallel branches;
- output dimension and named components;
- genuinely separate heads or decoders;
- residual base, correction, and corrected object;
- calibration inputs and outputs.

Use separate containers for separate models, stacked internals for layers,
hop rings or progressive graph sheets for receptive field, lanes for real
branches, and one vector/tensor card for one multidimensional output.

Never map layer 1/2/3 to output 1/2/3 merely because both counts equal three.
Only the completed layer stack should emit the final vector unless the source
specifies intermediate supervision or outputs.

Read [architecture-semantics.md](architecture-semantics.md) for the complete
mapping and residual/calibration rules.

## Lock style during revision

For an iteration, insert a short section before the scientific contract:

```text
REVISION SCOPE AND STYLE LOCK
Change only:
- <named semantic, text, layout, status, style, or legibility defect>

Preserve exactly:
- canvas and aspect ratio;
- phase/panel silhouette;
- information density and whitespace rhythm;
- dominant palette and semantic color mappings;
- typography, icon family, borders, tabs, and unaffected content.
```

Do not import a palette, aspect ratio, or density preference from another
session unless the current user explicitly selects it. If a user asks to
simplify one scientific module, preserve overall density by reallocating space
or strengthening hierarchy rather than automatically making the whole figure
sparse.

## Control visible text

Create an exact text inventory:

| Role | Recommended length | Treatment |
|---|---:|---|
| Phase heading | 2–7 words | bold display face |
| Panel title | 2–8 words | title tab or header |
| Module | 1–5 words | short label |
| Annotation | 2–7 words | subordinate size |
| Technical token | minimal | monospaced |
| Status | 1–3 words | semantic badge |

Quote every string that must appear verbatim. Spell unusual names or symbols
when the generator is likely to distort them. Avoid body prose in the figure.

## Assign semantic visual language

Define mappings before hex values:

```text
orange = institutional input or intervention
green = reliability evidence or verification
gray = shared infrastructure or neutral flow
blue = data, task, or node
yellow = pending or caution
red = failed gate or limitation
```

Then specify the restrained palette. Do not assign the same color to
contradictory states. Do not use green success marks for pending outputs.

Define:

- container shape and fill;
- border styles;
- major and minor arrow styles;
- icon family;
- type roles;
- negative-space behavior;
- status markers.

## Use controlled redundancy

Repeat only high-risk invariants:

| Level | Purpose | Example |
|---|---|---|
| Global | Establish the scientific rule | “All end-task results are pending.” |
| Local | Prevent a panel-specific failure | “Use yellow PENDING badges; no green checks.” |
| Final | Catch rendering drift | “Verify no pending output looks successful.” |

Avoid repeating generic style adjectives across every section.

## Canonical production scaffold

```text
Use case: scientific-educational
Asset type: <paper overview / method figure / graphical abstract>
Primary request: <one-sentence semantic spine>

INPUT ROLES
Image 1: <style reference / edit target / content source>.
Use: <specific transferable features>.
Ignore: <scientific labels, page chrome, screenshot prose, unrelated content>.

PROJECT STYLE PROFILE — REQUIRED FOR MULTI-FIGURE PROJECTS
Include when a canonical project profile exists or the project will contain
multiple figures.
Profile ID: "<profile_id>"
Profile version: "<profile_version>"
Status: "<draft / accepted>"
Materialize the profile's canvas family, typography, palette, density, icons,
containers, arrows, background, and anti-style below.

REVISION SCOPE AND STYLE LOCK
Include only for iterations.
Change only:
- <named defect>.
Preserve exactly:
- <accepted canvas, silhouette, density, palette, type, icons, and unaffected content>.

SCIENTIFIC CONTENT CONTRACT — HIGHEST PRIORITY
Must show:
- ...
May show:
- ...
Must not imply:
- ...
Evidence states:
- ...
If content conflicts with style, preserve scientific accuracy.

VISIBLE-ARTIFACT HYGIENE
Exclude scheduler/run IDs, paths, timestamps, and hashes unless the requested
asset is explicitly an operations or provenance figure.

CANVAS AND BACKGROUND
<aspect target, orientation, background, margins, framing prohibitions>

VISUAL STRUCTURE
<layout pattern, phase/panel count, reading order, relative geometry>

TYPOGRAPHY AND EXACT TEXT
Display role: ...
Body-label role: ...
Technical role: ...
Render verbatim:
- "..."

COLOR AND ICON LANGUAGE
<semantic color mapping, palette, icon family, forbidden icon families>

PANEL / PHASE / LANE 1 — <name>
<objects, labels, connectors, local invariants>

PANEL / PHASE / LANE 2 — <name>
<objects, labels, connectors, local invariants>

<repeat only for real structural units>

ARROW AND LINE RULES
<relationship types, directions, widths, colors, crossing rules>

VISUAL DENSITY AND LEGIBILITY
<density target, label length, whitespace, overlap constraints>

STRICT NEGATIVE CONSTRAINTS
Do not:
- leak reference content;
- invent scientific content;
- add plausible but unsupported modules or results;
- violate evidence-status colors;
- use unwanted media or UI styles;
- add watermarks.

FINAL VALIDATION
Verify:
- semantic spine;
- current project style profile ID and version;
- cross-figure typography, palette, density, icons, borders, and arrows;
- model count, depth, hops, branches, and output dimension;
- exact text;
- evidence states;
- shared versus separate artifacts;
- absence of operational metadata;
- preservation of the style lock when iterating;
- recognizable silhouette;
- background and anti-style constraints.
```
