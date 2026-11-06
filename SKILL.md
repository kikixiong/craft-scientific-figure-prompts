---
name: craft-scientific-figure-prompts
description: Learn reference-figure style, preserve scientific meaning and project-wide visual consistency, and build audited prompts for overview figures, method diagrams, architecture schematics, graphical abstracts, and research posters. For a finished-figure request, continue from the prompt to Image2/image generation and visual inspection in explicit steps. Also use for prompt-only drafting, templates, audits, and targeted figure revisions without copying the reference's scientific content.
---

# Craft Scientific Figure Prompts

Turn references into rendering contracts that preserve scientific meaning,
layout hierarchy, and visual character across projects. For a requested figure,
complete the prompt-to-image workflow in the same task. An explicit prompt-only
request stops after prompt validation.

## Resolve the request

Classify the task before writing:

- **Learn:** explain the reference's transferable prompt grammar.
- **Adapt:** inspect the target research and write a new prompt.
- **Template:** produce a reusable prompt scaffold with placeholders.
- **Audit:** diagnose an existing prompt or generated figure.
- **Iterate:** revise only the failed constraint class while preserving all
  invariants.

Treat a supplied image, prompt, paper, and project as different evidence
sources. State each input's role. A reference image normally supplies visual
grammar; the target paper supplies scientific content.

For **Iterate**, first write a two-column revision contract:

- **change:** only the defect class named by the user;
- **preserve:** accepted scientific relationships, canvas, silhouette,
  density, palette, typography, icons, borders, and unaffected text.

Treat the latest user-accepted prompt or figure as the style authority.
Preferences found in another session are scientific context only unless the
current user explicitly adopts them. Do not turn a semantic correction into a
restyle, simplification, or density change.

Choose delivery separately from the modes above:

- **Prompt only:** requests to write a prompt, Learn, Template, or audit without
  generating a figure. Do not call an image tool or render unresolved templates.
- **Prompt + image:** requests to draw/generate a figure, revise an existing
  image, or "generate the prompt, then use Image2". Finish and audit the prompt,
  then actually call the available image tool; do not stop at a suggested prompt
  or ask for the same generation permission again.
- If the user says "show me the prompt first and wait", respect that checkpoint.
  Otherwise the stages below are progress updates, not approval gates.

Use four visible steps for a figure request:

1. **Scientific content and style** — inspect inputs and establish the contracts
   using core workflow steps 0-4.
2. **Production prompt** — write, save and audit it using steps 5-7.
3. **Image2 / rendering** — submit that full prompt and the relevant images using
   step 8; keep the requested model identity honest.
4. **Visual inspection and delivery** — inspect the actual output using step 9,
   then return the image, prompt and audit note.

This workflow covers conceptual scientific illustrations. Use deterministic
plotting tools for measured data plots, fitted curves or exact quantitative
charts; never have the image model invent or redraw measured values as evidence.

## Follow the core workflow

### 0. Load the project style authority

For any project that has or may have multiple figures, look for:

```text
<project-root>/.codex/figure-style.toml
```

If it exists, read it completely before drafting or revising a prompt. Bind its
profile ID and version in the prompt, and materialize its font, palette,
density, icon, container, arrow, background, and anti-style invariants. The
file reference alone is insufficient because the image model cannot read it.

If it does not exist, create a draft from
[project-figure-style.toml](assets/project-figure-style.toml) after inspecting
the selected reference and user preferences. Mark it accepted only after the
user approves the style or an artifact using it. Never overwrite an accepted
profile silently; increment its version only for an explicitly approved
project-wide style change.

Read [project-style-profile.md](references/project-style-profile.md) for
profile lifecycle, precedence, figure-specific exceptions, and validation.

### 1. Inspect the reference

View every reference image at useful detail. If the input is a screenshot
containing both a figure and a prompt, distinguish the visual region from the
text region.

Extract a **style fingerprint** without copying scientific content:

- canvas and aspect ratio;
- macro silhouette and reading direction;
- phase, panel, bridge, and gutter geometry;
- visual hierarchy and information density;
- typography roles;
- color-to-meaning mappings;
- icon character;
- border, arrow, and connector grammar;
- repeated motifs;
- negative-space behavior;
- explicit prohibitions and anti-styles.

For an iteration, convert the accepted fingerprint into a **style lock**.
Record exact invariants for aspect ratio, macro silhouette, panel count,
internal whitespace or density, dominant palette, typography, icon family,
border grammar, and background. An omitted style property remains preserved;
silence is not permission to redesign it.

When an accepted project style profile exists, use it as the visual authority.
A figure-specific reference may supply composition ideas, but may not silently
replace project fonts, palette, density, icons, borders, arrows, or background.

Read [reference-analysis.md](references/reference-analysis.md) when the
reference is dense, contains multiple visual systems, or needs a formal
style-fingerprint table.

### 2. Establish the scientific source of truth

Inspect the target paper, thesis, repository, or brief before inventing panel
content. Prefer authoritative sources in this order:

1. title, abstract, research questions, and contribution statement;
2. method and research-design sections;
3. results, limitations, and conclusion;
4. figures, tables, protocols, and evidence ledgers;
5. informal notes only when clearly labelled.

Write a one-sentence **semantic spine**: input → transformation → intermediate
state → output → evaluation or implication.

Create a **scientific content contract** with:

- must show;
- may show;
- must not imply;
- exact terminology;
- exact numerical or symbolic text;
- evidence state and its exact bearer for each outcome;
- known unknowns and unresolved choices.

Never infer an absent formula, result, direction, winner, or causal mechanism.
Use explicit markers such as `PENDING`, `PRELIMINARY`, `LIMITATION`, or
`TO BE FROZEN` when licensed by the source.

Scope every status to the object it actually describes. For example, a
verified study result is not clinical validity, a verified artifact is not a
verified scientific claim, and a pending lane does not identify which internal
stage is unfinished unless the source says so.

Keep evidence provenance separate from visible method content. Scheduler IDs,
run numbers, paths, timestamps, and hashes may locate evidence but must not
appear in a scientific method figure unless the user explicitly requests an
operations or provenance view. Translate them into semantic labels.

### 3. Choose structure from semantics

Select a layout because it fits the semantic spine, not merely because the
reference used it.

- Use a left-to-right pipeline for sequential transformations.
- Use two phase containers plus a seam-crossing bridge for
  measurement-to-intervention, training-to-inference, or
  construction-to-deployment stories.
- Use parallel lanes for controlled arms, models, or conditions.
- Use a loop only when feedback or iteration is scientifically real.
- Use stacked layers for hierarchy, abstraction, or provenance.
- Use small multiples for comparable repeated units.

Preserve the reference's recognizable visual grammar while adapting its
silhouette when the target logic requires it. Do not force every project into
the two-phase bridge pattern.

Read [prompt-architecture.md](references/prompt-architecture.md) before writing
a full production prompt. It contains the section order, layout patterns,
controlled redundancy rules, and the canonical scaffold.

Read [architecture-semantics.md](references/architecture-semantics.md) whenever
the figure contains model depth, hops, output dimensions, heads, branches,
residuals, or calibration. Declare these counts independently before drawing.
In particular, layers are not models, hops are not branches, output components
are not layer-specific outputs, and a prediction residual is not an internal
skip connection.

### 4. Build the information architecture

Map each scientific object to a visual role:

- inputs → cards, files, datasets, or nodes;
- transformations → modules or arrows;
- shared contracts → bridge or enclosing strip;
- alternatives → aligned lanes;
- outputs → terminal cards;
- diagnostics → side badges or audit panels;
- pending states → yellow or hollow status marks;
- failed gates → red marks;
- verified success → green marks only when evidence licenses them.

Map structural quantities independently:

- model count → separate model containers;
- sequential depth → layers inside one model container;
- receptive field → hop rings or progressive graph layers;
- real computation branches → diverging arrows or lanes;
- output dimension → one vector/tensor card with named components;
- additive residual → base + delta → corrected object.

Keep visible labels short. Prefer one to five words; use a second line only
when it adds essential meaning. Move explanatory prose into the prompt, not
the figure. Define a verbatim text inventory before styling.

### 5. Write the prompt as a rendering contract

Order the prompt from global invariants to local detail:

1. use case, asset type, and primary request;
2. input-image roles and content-isolation rule;
3. project style profile ID, version, and invariants;
4. revision scope and style lock when iterating;
5. scientific content contract;
6. visible-artifact hygiene;
7. canvas and background;
8. macro visual structure;
9. typography and exact text;
10. semantic color and icon language;
11. one section per panel, lane, or module;
12. arrow and line rules;
13. density and legibility;
14. strict negative constraints;
15. final validation checklist.

Use controlled redundancy only at hierarchy boundaries:

- state an invariant globally;
- repeat it locally where a panel is especially failure-prone;
- restate it once in final validation.

Do not pad a prompt by repeating adjectives. Long prompts work when they
resolve ambiguity, not because they are long.

Apply this conflict priority:

1. scientific truth and evidence status;
2. explicit current-turn user instruction;
3. exact required text;
4. causal or procedural structure;
5. accepted project style profile;
6. legibility and non-overlap;
7. figure-specific reference suggestions;
8. decoration.

If a lower-priority rule conflicts with a higher-priority rule, preserve the
higher-priority rule and say so in the prompt.

### 6. Make the prompt robust

Add constraints against the generator's most plausible mistakes:

- reference-content leakage;
- invented panels, agents, arms, legends, or metrics;
- success marks on pending outputs;
- evidence states silently changing scope across layers;
- a pending outcome being attached to an invented unfinished stage;
- decorative arrows without endpoints;
- semantics-free color use;
- excessive prose or tiny labels;
- merged shared and arm-specific artifacts;
- background tint, texture, mockup framing, or global gradients;
- generic icon substitution;
- 3D, photorealistic, dashboard, poster, or SaaS styling when inappropriate.
- operational IDs, paths, hashes, or timestamps leaking into visible content;
- accepted palette, density, aspect ratio, or silhouette drifting during a
  local revision;
- different figures in one project silently using different fonts, palettes,
  icon families, border grammar, or density;
- model layers becoming separate models or outputs;
- equal layer, hop, and output counts becoming a false one-to-one mapping;
- prediction-space residuals becoming skip connections or improvement claims.

Express dimensions and percentages as composition targets, not guaranteed
pixel-perfect controls, unless the selected generation system exposes exact
controls.

### 7. Audit before delivery

Run:

```bash
python scripts/validate_prompt.py <prompt.md>
```

For a revision prompt that contains an explicit style lock, run:

```bash
python scripts/validate_prompt.py --iteration <prompt.md>
```

When a project style profile exists, validate both artifacts:

```bash
python scripts/validate_style_profile.py <project-root>/.codex/figure-style.toml
python scripts/validate_prompt.py \
  --style-profile <project-root>/.codex/figure-style.toml \
  <prompt.md>
```

Fix all errors. Review warnings with judgment; a warning can be acceptable
when the task intentionally omits that feature.

Then perform a semantic audit:

- Does every arrow have a scientific meaning?
- Are model count, depth, hops, branches, and output dimension visually
  distinct?
- Are shared and branch-specific objects correctly separated?
- Are all status colors evidence-licensed?
- Does exact text match the source?
- Can a reader recover the semantic spine without the caption?
- Does the prompt prohibit the reference's original scientific content?
- Are unknowns visibly unknown rather than aesthetically completed?
- Is operational provenance absent from visible method content?
- For an iteration, did every preserved style and density invariant survive?
- Does the prompt bind the current project profile version and remain visually
  coherent with previously accepted project figures?

Read [audit-and-iteration.md](references/audit-and-iteration.md) for the full
rubric and targeted revision protocol.

### 8. Render with Image2 or the available image tool

For **Prompt + image** delivery, read
[image2-workflow.md](references/image2-workflow.md) and the available imagegen
skill/tool instructions. Call the actual tool with the audited production
prompt and the required reference/edit images. The prompt must materialize the
style profile and exact visible text; a file path or a summary is not enough.

Use the native image-generation tool when available. When a supported model
selector is exposed and Image2 is requested, select `gpt-image-2`. Do not invent
a model parameter for a tool that has none, or claim its hidden backend is a
verified Image2 version. Preserve explicit model requirements; do not silently
substitute another model. See the reference for exact-model and unavailable-tool
handling, including the separately authorized API/CLI path.

### 9. Inspect the generated figure and deliver

Inspect the actual pixels against the content contract, text inventory and style
lock. Check scientific relationships, arrows, counts, labels, evidence states,
legibility, clipping and consistency with accepted figures. Static prompt checks
do not certify the generated image. If no image is returned or viewable, report
that limitation rather than claiming visual verification.

For a clear defect, make at most one targeted correction within the authorized
scope and budget, then inspect again; preserve accepted invariants. Stop if the
same defect remains, the tool fails, or the budget is exhausted, and report the
remaining issue. Save a new version rather than replacing an accepted image.

Display the resulting image. For project deliverables, copy the actual returned
artifact into the project and report its real path; do not invent a download
link or file location. Keep the prompt and brief audit beside it. Record the
tool used and model/version only when the tool or request actually establishes it.

## Deliver useful artifacts

Unless the user requests another format, return:

1. the project style profile path, ID, and version when one is used;
2. a concise **learned visual grammar** summary;
3. a **scientific content contract**;
4. the complete copy-paste **production prompt**;
5. a short **audit note** listing assumptions and intentionally pending items.

For **Prompt + image**, also return the generated image and its actual saved
location when available, with the visual inspection outcome. A prompt alone is
an incomplete result when generation was requested; explain any tool blocker.

When saving files, use descriptive names such as:

- `<project>-figure-grammar.md`
- `<project>-scientific-content-contract.md`
- `<project>-imagegen-prompt.md`
- `<project>-figure-v1.png` (or the format actually returned)
- `<project>-figure-audit.md`

Keep project facts out of the global skill itself. Add reusable failure modes
or layout knowledge here only after they generalize across tasks.

## Iterate from evidence

When a generated figure is supplied, compare it against the prompt and classify
defects before revising:

- semantic error;
- missing or wrong text;
- layout drift;
- status-color error;
- style drift;
- legibility problem;
- unwanted element.

Freeze accepted invariants before editing. Revise one defect class at a time.
Repeat all invariants affected by the edit and explicitly preserve everything
else. Do not rewrite the whole prompt for a local defect unless the macro
structure failed. Simplifying scientific content does not authorize lower
information density; adding distinguishable concepts does not authorize a new
palette.

Use [worked-example.md](references/worked-example.md) only when a concrete
example of the full layered format is helpful; do not copy its subject matter
into unrelated work.
