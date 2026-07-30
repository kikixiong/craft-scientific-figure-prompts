# Audit and iteration

## Contents

- [Prompt audit rubric](#prompt-audit-rubric)
- [Generated-figure audit](#generated-figure-audit)
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
| Exact text | uncontrolled | partial list | complete verbatim inventory |
| Visual semantics | decorative color | mixed | stable mappings |
| Status integrity | misleading | ambiguous | evidence-licensed and scoped |
| Negative constraints | generic | some risks | target-specific failure prevention |
| Final validation | absent | generic | tests high-risk invariants |

Treat a zero in source grounding, content contract, or status integrity as a
blocker. Aim for at least 16/20 before delivery.

## Generated-figure audit

Inspect in this order:

1. **Scientific correctness:** concepts, arrows, branches, claims, numbers.
2. **Status integrity:** verified, pending, preliminary, failed, limitation.
3. **Text accuracy:** spelling, symbols, duplicated or invented words.
4. **Structural fidelity:** panel count, lanes, shared versus separate objects.
5. **Legibility:** font size, overlap, whitespace, line crossings.
6. **Visual fidelity:** palette, icon family, typography, border grammar.
7. **Anti-style compliance:** background, shadows, gradients, UI framing.

Do not accept a visually attractive figure with a scientific or evidence-state
error.

For every status badge, ask both “what is the state?” and “what exact object or
claim bears that state?” Do not let artifact verification imply scientific
validity, study verification imply deployment readiness, or an overall pending
result imply a specific unfinished internal step.

## Targeted revision protocol

Classify the dominant defect and issue one narrow revision.

### Semantic error

```text
Change only the scientific relationship between <A> and <B>.
Replace <wrong relationship> with <correct relationship>.
Preserve all text, layout, colors, icons, and other arrows.
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

### Legibility problem

```text
Improve only legibility by shortening line breaks, increasing local spacing,
and preventing overlap. Do not remove required labels or change the macro
structure.
```

After each revision, repeat the scientific and status audits before judging
visual polish.
