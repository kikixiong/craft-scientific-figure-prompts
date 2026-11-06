# Prompt to Image2: generation and inspection

Read this after preparing the scientific contract and before rendering a figure.
This is an agent workflow, not a bundled image service. Tool names, parameters
and model availability must come from the current host's actual capabilities.

## Step 1 — Establish content and style

Inspect the target research, references and any accepted figure/style profile.
Separate a style reference from an edit target and from scientific evidence.
If no reference is supplied, derive a draft style from the brief without
pretending to have viewed a reference. Do not invent missing scientific facts.
Use ordinary plotting tools for data charts requiring exact numerical fidelity.

## Step 2 — Save and audit the production prompt

Write the full rendering contract using the core workflow. Include the exact
visible text, evidence states, scientific relationships, canvas, materialized
style invariants, image roles and negative constraints. Run the relevant prompt
and style validators, then review scientific meaning. Unresolved production
placeholders must be resolved or intentionally represented as unknowns, never
sent as a Template-mode scaffold to the renderer.

Save a versioned prompt in the target project when files are part of the task.
Briefly announce that prompt preparation is complete, then continue rendering
when requested. "First write the prompt, then generate" authorizes both steps;
"write the prompt and wait for me" does not authorize the second step yet.

## Step 3 — Call the real image-generation tool

Prefer the host's native image tool, such as Codex `image_gen`, following its
current instructions and the installed `imagegen` skill when available. This
native path does not require the user to provide an API key. Do not respond with
only a tool-call example, or replace requested raster output with an SVG sketch.

Use the complete audited prompt as the tool input, not a condensed paraphrase.
The image model cannot open a prompt/style file just because its path appears
in the request. Explicitly carry over the text and style invariants.

Before the call:

- Inspect local reference/edit images with the available image-viewing tool.
- Attach the required images using the current tool's supported mechanism.
  If it supports local paths, pass the verified paths; if it uses conversation
  images, include only the relevant available images. Do not combine mutually
  exclusive reference mechanisms or silently omit an edit target.
- For edits, preserve the accepted figure and specify only the intended changes.
- Use actual transparency controls when available; preserve existing alpha on
  edits unless the user requests otherwise.
- Map size, format and quality only to controls the selected tool supports.
  Otherwise state composition targets in the prompt without claiming exact
  pixel dimensions are guaranteed. Never pass API-only fields to a native tool.

### Image2 identity and exact-model requests

The API model ID for GPT Image 2 is `gpt-image-2`. If a tool exposes a supported
model selector, use that ID when requested. Do not automatically upgrade to a
different model merely because a documentation page recommends a newer one.

Some native tools expose no model selector or backend version. For a request
using "Image2" as the name of the normal image-generation step, use the available
native renderer and disclose that its exact backend version is not exposed.
Do not claim to have pinned `gpt-image-2`. If the user explicitly requires that
exact model/version, treat model selection as a requirement: use an authorized
tool that can select it or explain the missing capability before rendering.

An API/CLI path is a separate execution choice, not a silent fallback. Use it
only when the user explicitly requests or confirms it. In Codex, prefer the
installed imagegen skill's supported CLI over a new ad hoc SDK runner, and pass
the requested model explicitly. Read its current CLI documentation, check its
availability and use credentials already configured in the environment; never
ask the user to paste a secret. Without credentials or the exact requested
capability, keep the ready prompt and report the blocker. Other agents should
use their available authorized image connector; installing this skill alone
does not add an image tool to Claude Code, Cursor or a server.

If native generation fails, report the failure and preserve the prompt. Do not
switch models, enter a paid API workflow or repeatedly regenerate without the
required authorization. Follow the host's documented asynchronous wait/display
protocol and report success only when a usable image is returned.

## Step 4 — Inspect, correct narrowly, deliver

View the returned image, using the actual returned file or image resource when
needed. Compare the pixels against the prompt: scientific relationships, exact
text, object counts, arrows, evidence colors, style, clipping and readability.
Treat a visually polished but scientifically incorrect image as needing repair.

Within the existing request and budget, allow one focused edit of a clear defect
and recheck it. Keep the accepted style and all unaffected content fixed. If the
tool is unavailable, the correction fails or the defect persists, stop and state
the unresolved issue rather than entering an unbounded generation loop.

Deliver the rendered image, saved production prompt and concise visual audit.
For project work, copy the selected image from the tool's actual output location
into the workspace with a versioned name; do not overwrite accepted artifacts.
For preview-only work, an inline image is sufficient. Report actual paths and
tool/model information only when known. Image inspection is not experimental
validation of the science depicted.

## Official model reference

- [GPT Image 2](https://developers.openai.com/api/docs/models/gpt-image-2)
- [Image generation guide](https://developers.openai.com/api/docs/guides/image-generation)

Consult current documentation for the chosen API route. The native tool's schema
is authoritative for native calls; API examples do not define its arguments.
