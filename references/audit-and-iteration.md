# Audit and iteration

## Contents

- [Prompt audit rubric](#prompt-audit-rubric)
- [Generated-figure audit](#generated-figure-audit)
- [Revision contract](#revision-contract)
- [Targeted revision protocol](#targeted-revision-protocol)

## Prompt audit rubric

Score each dimension from 0 to 2:

| Dimension | 0 | 1 | 2 |
|---|---|---|---|
| Source grounding | invented or absent | partial | authoritative and explicit |
| Semantic spine | unclear | inferable | concise and complete |
| Content contract | absent | incomplete | must/may/must-not/evidence states |
| Input isolation | reference leaks | ambiguous | roles and ignore rules explicit |
| Layout fit | decorative | partly semantic | relationships determine structure |
| Architecture semantics | counts conflated | partly disambiguated | models/layers/hops/outputs/residuals distinct |
| Exact text | uncontrolled | partial list | complete verbatim inventory |
| Visual semantics | decorative color | mixed | stable mappings |
| Style and density continuity | unrequested redesign | partial preservation | explicit lock and exact preservation |
| Cross-figure continuity | each figure restyled | partial family resemblance | current project profile bound |
| Status integrity | misleading | ambiguous | evidence-licensed and scoped |
| Artifact hygiene | operational metadata visible | partly filtered | semantic labels only |
| Negative constraints | generic | some risks | target-specific failure prevention |
| Final validation | absent | generic | tests high-risk invariants |

Treat a zero in source grounding, content contract, or status integrity as a
blocker. For architecture figures, also treat zero architecture semantics as a
blocker. For iterations, treat zero style and density continuity as a blocker.
For multi-figure projects, treat zero cross-figure continuity as a blocker.
Aim for at least 23/28 before delivery.

## Generated-figure audit

Inspect in this order:

1. **Scientific correctness:** concepts, arrows, branches, claims, numbers.
2. **Status integrity:** verified, pending, preliminary, failed, limitation.
3. **Architecture semantics:** models, layers, hops, branches, outputs,
   residuals, and calibration.
4. **Text accuracy:** spelling, symbols, duplicated or invented words.
5. **Artifact hygiene:** job/run IDs, paths, hashes, timestamps, UI chrome.
6. **Structural fidelity:** panel count, lanes, shared versus separate objects.
7. **Density fidelity:** module scale, whitespace rhythm, compactness.
8. **Cross-figure continuity:** current profile version, fonts, palette, icons,
   borders, arrows, density, and background.
9. **Visual fidelity:** palette, icon family, typography, border grammar.
10. **Legibility:** font size, overlap, whitespace, line crossings.
11. **Anti-style compliance:** background, shadows, gradients, UI framing.

Do not accept a visually attractive figure with a scientific or evidence-state
error.

For every status badge, ask both “what is the state?” and “what exact object or
claim bears that state?” Do not let artifact verification imply scientific
validity, study verification imply deployment readiness, or an overall pending
result imply a specific unfinished internal step.

## Revision contract

Before modifying an accepted prompt or figure, record:

```text
Defect class:
Change:
Preserve:
Source of corrected fact:
Accepted style authority:
```

Default to preserving every property not named by the user. Keep semantic,
layout, status, style, and legibility changes separate. If one correction
requires a second class of change, state that dependency instead of silently
expanding scope.

Do not inherit aesthetic instructions across sessions. Cross-session content
may establish a formula, method role, or evidence state; it does not authorize
changing palette, aspect ratio, density, or silhouette.

## Targeted revision protocol

Classify the dominant defect and issue one narrow revision.

### Semantic error

```text
Change only the scientific relationship between <A> and <B>.
Replace <wrong relationship> with <correct relationship>.
Preserve all text, layout, colors, icons, and other arrows.
```

For architecture-count errors, add:

```text
Render <N layers / H hops / D output dimensions / B branches> as independent
properties. Use <one stacked model / hop rings / one vector card / parallel
lanes>. Explicitly prohibit the incorrect one-to-one mapping. Preserve the
accepted style and density.
```

### Wrong or missing text

```text
Change only the label <wrong>.
Render exactly: "<correct>".
Preserve its size, position, hierarchy, and every other element.
```

### Layout drift

```text
Change only the macro geometry.
Restore <phase/panel/lane relationship>.
Preserve scientific content, exact text, semantic colors, and icon family.
```

### Status-color error

```text
Change only evidence-status encoding.
Render <item> as <PENDING/FAILED/PRELIMINARY> using <marker>.
Do not use <misleading marker>. Preserve all other elements.
```

### Style drift

```text
Change only <typography/icon/border/background> style.
Match <specific fingerprint>.
Preserve content, geometry, exact text, and status markers.
```

### Density drift

```text
Restore the accepted module scale, whitespace percentage, panel-to-gutter
ratio, and label budget. Preserve scientific content, panel geometry, palette,
typography, and icons. Simplifying one module must not make the whole figure
sparse.
```

### Operational metadata leakage

```text
Remove only scheduler IDs, run numbers, paths, hashes, timestamps, and internal
status labels from visible content. Replace them with the licensed semantic
label when needed. Preserve the underlying evidence state and all other
content and style.
```

### Legibility problem

```text
Improve only legibility by shortening line breaks, increasing local spacing,
and preventing overlap. Do not remove required labels or change the macro
structure.
```

After each revision, repeat the scientific and status audits before judging
visual polish. Also compare the revised prompt against the revision contract
and verify that no unrequested style or density property changed.
