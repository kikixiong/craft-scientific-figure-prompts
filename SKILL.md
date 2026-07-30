---
name: craft-scientific-figure-prompts
description: Analyze reference figures and their prompts, extract transferable visual and organizational grammar, and produce robust model-agnostic prompts for scientific overview figures, method diagrams, architecture schematics, graphical abstracts, and research posters. Use when Codex must learn a figure's style or prompt structure, adapt that structure to a paper, thesis, proposal, or technical project, rewrite or audit a long image-generation prompt, preserve scientific evidence states, or iteratively improve a generated figure without copying the reference's scientific content.
---

# Craft Scientific Figure Prompts

Turn references into rendering contracts that preserve scientific meaning,
layout hierarchy, and visual character across projects. Produce prompts by
default; do not generate an image unless the user separately requests it.

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

If the request is prompt-only, do not call an image-generation tool. If image
generation is also requested, finish and audit the prompt first, then use the
applicable image-generation workflow separately.

## Follow the core workflow

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

Keep visible labels short. Prefer one to five words; use a second line only
when it adds essential meaning. Move explanatory prose into the prompt, not
the figure. Define a verbatim text inventory before styling.

### 5. Write the prompt as a rendering contract

Order the prompt from global invariants to local detail:

1. use case, asset type, and primary request;
2. input-image roles and content-isolation rule;
3. scientific content contract;
4. canvas and background;
5. macro visual structure;
6. typography and exact text;
7. semantic color and icon language;
8. one section per panel, lane, or module;
9. arrow and line rules;
10. density and legibility;
11. strict negative constraints;
12. final validation checklist.

Use controlled redundancy only at hierarchy boundaries:

- state an invariant globally;
- repeat it locally where a panel is especially failure-prone;
- restate it once in final validation.

Do not pad a prompt by repeating adjectives. Long prompts work when they
resolve ambiguity, not because they are long.

Apply this conflict priority:

1. scientific truth and evidence status;
2. exact required text;
3. causal or procedural structure;
4. legibility and non-overlap;
5. reference silhouette;
6. visual style;
7. decoration.

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

Express dimensions and percentages as composition targets, not guaranteed
pixel-perfect controls, unless the selected generation system exposes exact
controls.

### 7. Audit before delivery

Run:

```bash
python scripts/validate_prompt.py <prompt.md>
```

Fix all errors. Review warnings with judgment; a warning can be acceptable
when the task intentionally omits that feature.

Then perform a semantic audit:

- Does every arrow have a scientific meaning?
- Are shared and branch-specific objects correctly separated?
- Are all status colors evidence-licensed?
- Does exact text match the source?
- Can a reader recover the semantic spine without the caption?
- Does the prompt prohibit the reference's original scientific content?
- Are unknowns visibly unknown rather than aesthetically completed?

Read [audit-and-iteration.md](references/audit-and-iteration.md) for the full
rubric and targeted revision protocol.

## Deliver useful artifacts

Unless the user requests another format, return:

1. a concise **learned visual grammar** summary;
2. a **scientific content contract**;
3. the complete copy-paste **production prompt**;
4. a short **audit note** listing assumptions and intentionally pending items.

When saving files, use descriptive names such as:

- `<project>-figure-grammar.md`
- `<project>-scientific-content-contract.md`
- `<project>-imagegen-prompt.md`

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

Revise one defect class at a time. Repeat all invariants affected by the edit
and explicitly preserve everything else. Do not rewrite the whole prompt for a
local defect unless the macro structure failed.

Use [worked-example.md](references/worked-example.md) only when a concrete
example of the full layered format is helpful; do not copy its subject matter
into unrelated work.
