# Reference analysis

## Contents

- [Separate content from grammar](#separate-content-from-grammar)
- [Build a style fingerprint](#build-a-style-fingerprint)
- [Infer the prompt's control strategy](#infer-the-prompts-control-strategy)
- [Handle weak or incomplete references](#handle-weak-or-incomplete-references)

## Separate content from grammar

Label each observed feature as one of:

| Class | Question | Transfer rule |
|---|---|---|
| Scientific content | What topic-specific claim or object is shown? | Do not transfer unless the target source supports it. |
| Information architecture | How are inputs, modules, branches, and outcomes organized? | Transfer when the target has the same relationship. |
| Visual grammar | How do color, type, icons, borders, and arrows encode roles? | Transfer while remapping semantics explicitly. |
| Rendering control | Which constraints prevent common generator drift? | Transfer broadly, adapting to the target medium. |
| Artifact noise | What belongs to the screenshot, page, UI, or crop rather than the figure? | Ignore and prohibit if it might leak. |

Never describe “same style” as sufficient. Name the transferable components
and the content that must be ignored.

## Build a style fingerprint

Use this worksheet for dense references:

| Dimension | Observation | Target adaptation | Confidence |
|---|---|---|---|
| Canvas | aspect, background, margins | exact target | high/medium/low |
| Silhouette | phases, panels, bridge, lanes | target layout | |
| Reading order | horizontal, vertical, loop | semantic spine | |
| Density | sparse/moderate/dense | label budget | |
| Typography | display, body, technical | font roles | |
| Palette | colors and meanings | semantic remap | |
| Icons | sticker, line, flat, photo | allowed icon family | |
| Containers | fill, border, radius, tabs | reusable grammar | |
| Arrows | thickness, color, routing | relationship types | |
| Status marks | success, failure, pending | evidence states | |
| Negative space | pure canvas or tinted | background rule | |
| Anti-style | what the reference avoids | negative constraints | |

Distinguish observation from inference. If a precise font, color, or stroke
cannot be known from the image, describe the closest visual role instead of
claiming certainty.

## Infer the prompt's control strategy

When a corresponding prompt is available, analyze its organization:

1. Which constraints appear first?
2. Which constraints are repeated, and at what hierarchy?
3. Does it lock the silhouette before panel content?
4. Does it enumerate exact visible text?
5. Does color have semantic meaning?
6. Are icons described as a coherent family?
7. Are likely failure modes explicitly prohibited?
8. Does the final checklist restate only high-risk invariants?

Summarize the control strategy, not every sentence. A strong long prompt
usually follows:

`semantic contract → canvas → silhouette → typography → palette → panels → connectors → anti-style → final audit`

## Handle weak or incomplete references

- If the image is low resolution, avoid invented measurements.
- If the screenshot includes prose below the figure, mark it as prompt evidence
  or page noise before using it.
- If only a prompt is available, distinguish specified intent from observed
  rendering.
- If only the figure is available, infer cautiously and label uncertain style
  details.
- If the target paper is missing, create a structure-only template with
  explicit placeholders instead of fabricating content.
- If the reference and supplied prompt disagree, report the mismatch and
  prioritize the user's requested output over either artifact.
