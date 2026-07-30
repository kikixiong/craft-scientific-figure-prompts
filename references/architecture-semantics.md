# Architecture semantics

## Contents

- [Declare counts independently](#declare-counts-independently)
- [Map each relationship to a visual grammar](#map-each-relationship-to-a-visual-grammar)
- [Disambiguate high-risk combinations](#disambiguate-high-risk-combinations)
- [Keep method artifacts clean](#keep-method-artifacts-clean)
- [Audit architecture diagrams](#audit-architecture-diagrams)

## Declare counts independently

Do not let one repeated number silently bind unrelated concepts. Record each
count and its meaning before choosing a visual representation:

| Concept | Question | Example |
|---|---|---|
| Model count | How many independently executed models exist? | one GNN |
| Depth | How many sequential transformations occur inside one model? | three layers |
| Receptive field | How far can information propagate? | three hops |
| Branch count | How many genuinely parallel computation paths exist? | no parallel branch |
| Output dimension | How many values leave the model? | one vector with dim = 3 |
| Output heads | Are there distinct learned decoders, or only vector components? | source-dependent |
| Residual | What base object receives what additive correction? | \(\tilde q=q+\Delta\) |
| Calibration | Which held-out data modifies which output? | corrected bounds + calibration set |

Use the target paper and implementation to distinguish architecture from
training targets. Do not infer separate heads merely because different output
components use different losses.

## Map each relationship to a visual grammar

### Multiple models

Use separate containers or parallel lanes only when models execute
independently or represent real experimental alternatives.

### Sequential layers inside one model

Use one enclosing model region containing:

- overlapping graph sheets;
- stacked internal layers;
- or a short internal sequence.

Keep one model label over the complete stack. Draw one final output arrow
unless the source exposes real intermediate outputs. Layer count does not
determine output count.

### Multi-hop propagation

Use expanding neighbourhood rings, progressively highlighted neighbours, or
overlapping graph layers labelled with hop reach. Hops describe receptive
field, not independent models, branches, datasets, or predictions.

### Output dimension

Use one vector, tensor, or output card labelled with its dimension. Place
named components inside the card. For example:

```text
one 3-layer GNN → one "Output dim = 3" card
                     ├ midpoint
                     ├ lower quantile
                     └ upper quantile
```

Do not draw three model boxes or three layer-specific arrows merely because
the output dimension is three.

### Genuine output heads

Use branches only if the source specifies distinct learned heads or decoders
and showing that distinction matters. Branch after the shared backbone, never
from successive backbone layers unless that is the actual architecture.

If a single final projection emits a vector whose components receive different
loss terms, prefer one output card with component labels. State the training
target beside the relevant component.

### Prediction-space residual

Use a three-object addition motif:

```text
base prediction q + additive correction Δ → corrected prediction q-tilde
```

Show the producer of \(\Delta\) separately. Do not render a prediction-space
residual as:

- an internal neural-network skip connection;
- a feedback loop;
- a recurrent update;
- or a before/after improvement claim.

### Calibration

Show held-out calibration labels entering the calibration module, not the
inference model. Make the order explicit:

```text
predictions + held-out calibration → calibrated interval
```

If calibration follows a residual correction, route the corrected output into
calibration. Never place truth labels on the inference path.

## Disambiguate high-risk combinations

Whenever a prompt contains two or more numeric architecture properties, add a
local non-equivalence rule and repeat it in final validation.

Example:

```text
The model has three sequential message-passing layers, a three-hop receptive
field, and one dim=3 output vector. These repeated threes are independent:
do not map layer 1/2/3 to output component 1/2/3. Only the complete layer stack
emits one output arrow.
```

Protect these common confusions:

- layers ≠ models;
- layers ≠ heads;
- hops ≠ layers unless the source explicitly equates them;
- output components ≠ execution branches;
- loss terms ≠ architectural modules;
- residual correction ≠ skip connection;
- calibration input ≠ inference label.

## Keep method artifacts clean

Operational provenance can support scientific grounding without becoming
visible figure content. Exclude the following from method diagrams unless the
user explicitly requests an audit, provenance, or operations figure:

- scheduler and job identifiers;
- run or experiment numbers;
- filenames and absolute paths;
- timestamps;
- commit and artifact hashes;
- internal queue, host, or status labels.

Translate operational evidence into semantic labels such as "held-out
calibration", "formal shift audit", or "preliminary diagnostic". Do not expose
the internal identifier that located the evidence.

## Audit architecture diagrams

Before delivery, answer:

1. How many models, layers, hops, branches, and output values exist?
2. Does each visual repetition correspond to the correct count?
3. Does every output arrow leave the scientifically correct object?
4. Are vector components contained in one output artifact when appropriate?
5. Is every residual attached to its correct base object?
6. Are calibration labels separated from inference?
7. Could any repeated number cause the generator to invent a one-to-one
   mapping?
8. Is operational provenance absent from visible method content?
