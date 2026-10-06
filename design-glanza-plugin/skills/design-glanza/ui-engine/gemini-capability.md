# Gemini Capability

## Responsibility
A shared, optional, cross-lifecycle capability — not a phase, agent,
pipeline, or gate of its own — that lets specific existing actions call
Google's Gemini API when it materially improves that action's specific
output, with automatic, disclosed, non-blocking fallback to
Design-Glanza's own existing technique whenever Gemini isn't configured,
isn't warranted, or fails. This file is the single source of truth for
*how and when* Gemini gets invoked; it never duplicates the reasoning
technique of the file that consumes its output (`ui-engine/
visual-asset-generation.md`, `design-reference-engine/
reference-analysis.md`, `ui-engine/visual-benchmark.md`,
`ux-engine/localization.md` — each cites this file for the mechanics,
never restates them). Lives under `ui-engine/` for consistency with
`visual-asset-generation.md` (the same kind of shared capability); its
actual consumers span UX, UI, visual QA, and content — not UI alone.

## Availability (checked, never assumed)
`GEMINI_API_KEY` present in the environment, checked at the point of
use, every time — never cached as a standing assumption across actions,
since the environment a Preview & Run/Implement pass executes in is not
guaranteed to be the same one a later Audit pass runs in. Absent or
invalid → every capability below falls back automatically, per-call, no
pause, no manual-approval prompt — the identical posture
`visual-asset-generation.md` already established for its own API path,
generalized here to every Gemini touchpoint.

## The decision rubric
Checked in this order at every potential touchpoint, before any network
call:

1. **Not applicable** — this action has no Gemini-capable sub-task at
   all (true for the great majority of the 41 actions — e.g. Order 1
   "Read all available product requirements"). Stop here; nothing below
   applies.
2. **Already satisfied** — Design-Glanza's own existing technique
   already answers this specific need at sufficient confidence (an
   Explicit-confidence Figma extraction already covers what a
   screenshot-only analysis would only approximate; a clean first-draft
   critique already found nothing a second opinion would plausibly add).
   Skip — reusing what already exists beats repeating the analysis.
3. **Unavailable** — `GEMINI_API_KEY` isn't configured, or the call
   fails (auth, quota, network). Fall back to the cited existing
   technique automatically, log the fallback as a disclosed Note
   (never silently), continue.
4. **Required** — scoped narrowly to the one case where no other path
   produces the distinguishing deliverable at all: real
   photographic/illustrative image *generation* (GC-1's API path). Even
   here "Required" means only that *this specific candidate* needs
   Gemini to exist — the overarching action is never blocked, since the
   native method (`visual-asset-generation.md`'s always-available path)
   already satisfies the action on its own.
5. **Useful** — every other case (GC-2/3/4): Gemini would add real,
   material value beyond what Design-Glanza's own technique already
   produces, judged against the specific trigger condition stated per
   capability below — never invoked as a blanket default just because a
   key is configured.

## Official SDK / API (current, non-deprecated)
Use the unified **Google GenAI SDK** (`google-genai` on PyPI, `from
google import genai`) — the current official client for the Gemini
Developer API, superseding the deprecated `google-generativeai` package.
Pattern, adapted to the specific call at each use point below:

```python
import os
from google import genai

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])  # never a literal key

response = client.models.generate_content(
    model=MODEL_ID,       # verified against a live ListModels call, never hardcoded to one guessed id
    contents=CONTENTS,    # text, or [text, image_part] for multimodal input
)
```

Where the SDK isn't installed in the current environment (`pip install
google-genai` not run, or unavailable), the equivalent plain REST call
against `generativelanguage.googleapis.com` (stdlib `urllib` only, no
extra dependency) is an acceptable fallback mechanism for the *same*
call — not a different capability, the same one with a lighter-weight
transport. Either way: verify the actual available model IDs via a
live `ListModels`-equivalent call before the first real request in a
session, never a hardcoded model id assumed stable (model availability
and naming changes over time, same caution `ai-image-generator`-derived
technique already carries in `visual-asset-generation.md`).

## Execution boundary (no new tool grant)
Every Gemini call happens inside the same execution boundary
`scripts/capture-render.py`'s Playwright calls and `ui-engine/
asset-pipeline.md`'s favicon/image tooling already use: Implement/
Preview & Run/Audit are carried out by "whatever capability is actually
invoking this workflow" (`workflows/build-product.md`'s own stated
posture), not by Design-Glanza's own narrowly-scoped self-invocation
tool surface (`SKILL.md`'s `allowed-tools`, unchanged by this
capability). No new Bash allowlist entry, no new MCP/network tool grant
on `SKILL.md` itself — this capability adds no tool surface, it only
documents a technique available within the execution boundary that
already exists.

## Security — never expose, hardcode, log, commit, or transmit unnecessarily
- Read `GEMINI_API_KEY` from the environment only, at the point of the
  call — never from a file this repo or a generated product's `output/`
  could contain, never pasted into a prompt, artifact, or conversation.
- Never write the key's value into any file: not a config, not a token
  file, not `asset-manifest.json`, not a log, not a generated `output/*`
  file, not a commit. A report records only *that* Gemini was used (or
  unavailable) and *which model* — never the credential.
- Never embed the key in generated frontend code — it is a build-time
  generation credential only; a shipped product never makes its own
  client-side call to Gemini with this key.
- Never print the key in an error message — a caught exception's message
  is logged/displayed with the key redacted, matching
  `capture-render.py`'s existing "degrade to a disclosed Note, never a
  crash" posture, extended here to "disclosed, never a leaked secret."
- If a key is ever pasted into a conversation by mistake, that key is
  compromised by the exposure itself (independent of whether it's ever
  called) — flag it to the user and recommend rotation; never store it
  anywhere to "remember" it for later.

## Gemini Capability catalog

### GC-1 — Real image generation (API path)
```
Trigger:          ui-engine/visual-asset-generation.md's Step 0 determines
                   real imagery is warranted AND no existing reusable
                   ASSET-NNN already serves the same need.
Input:             The asset's required style/subject (BRD + design-
                   direction.md + figma-context.json's imagery field,
                   where present).
Execution Point:   Order 29 (Build component architecture), Order 34
                   (Implement) — both already-cited rows, no new row.
Model/API:         A Gemini image-capable model (verified via a live
                   model list, e.g. the gemini-*-image family) via the
                   official SDK; REST fallback if the SDK isn't
                   installed.
Output:            A real generated image file — one candidate alongside
                   the always-available native candidate.
Consumer:          ui/visual-assets/asset-manifest.json (ASSET-NNN),
                   ui/components.md — selection against all 6 criteria
                   is visual-asset-generation.md's own job, not restated
                   here.
Fallback:          The native, token-driven composition method — always
                   available, never blocked by this capability's absence.
Validation:        Existing gates B14 (Preview & Run Verification) / B15
                   (Visual Benchmark & Audit Cycle) — no new gate.
```

### GC-2 — Multimodal design-reference analysis
```
Trigger:           A supplied design reference is screenshot/image-only
                   (no inspectable Figma structure, per reference-
                   analysis.md's "From a Screenshot Only" path) AND
                   Design-Glanza's own direct visual reading leaves a
                   material field (color/typography/component pattern)
                   at Inferred/Assumed confidence a second, independent
                   multimodal read could narrow — including, where the
                   source material is an unusually large/complex
                   document, an optional structured-extraction cross-
                   check against product-intelligence/brd-analysis.md's
                   own extraction (a disclosed reconciliation note on
                   any discrepancy, never a silent override).
Input:             The reference image(s)/document.
Execution Point:   Order 15 (Detect and analyze design references).
Model/API:         A Gemini multimodal text+vision model via the SDK,
                   the image/document passed as inline input alongside
                   a prompt scoped to reference-analysis.md's own
                   extraction table (colors/typography/components/
                   spacing/etc.) — never a freeform "describe this
                   image" prompt with no structure to check against.
Output:            A structured extraction note, still tagged Inferred
                   (never silently upgraded to Explicit — Gemini's read
                   is a second opinion on an ambiguous image, not a
                   structural data source the way an inspected Figma
                   file is).
Consumer:          design-reference-engine/reference-analysis.md's
                   extraction table, ui/design-direction.md.
Fallback:          Design-Glanza's own direct visual reading of the same
                   image/document — already the default, always-
                   available method.
Validation:        Existing gate B13 (Design Direction Completeness) —
                   no new gate.
```

### GC-3 — Independent visual/QA second opinion
```
Trigger:           ui-engine/visual-benchmark.md's mandatory refinement
                   step 1 (CRITIQUE) has run and produced a result the
                   acting agent judges could genuinely benefit from an
                   independent cross-check — e.g. a screen that passed
                   every mechanical check but still reads uncertain on
                   craft-critique.md's qualitative anti-cliché catalog,
                   or an explicit user request for extra scrutiny. Never
                   invoked as a default second pass on every screen —
                   that would be noise, not signal, and the existing
                   single-model critique is already mandatory and
                   sufficient for the ordinary case.
Input:             The real rendered screenshot (capture-render.py's
                   output), ui/design-direction.md, the component spec.
Execution Point:   Order 32 (the mandatory visual-benchmark-and-audit
                   cycle), Order 39 (Audit) — both already-cited rows.
Model/API:         A Gemini multimodal model via the SDK, prompted
                   directly against craft-critique.md's anti-cliché
                   catalog and ui-audit-framework.md's A-K categories —
                   the same checklist the primary critique already uses,
                   not a different, uncalibrated rubric.
Output:            A labeled "Gemini second opinion" note — additive
                   evidence, never a gate-deciding verdict on its own;
                   a disagreement between the two reads is logged as a
                   finding to resolve, not silently reconciled toward
                   whichever is more convenient.
Consumer:          ui/visual-gap-analysis.md (an additional, clearly-
                   labeled field), qa/qa-report.md.
Fallback:          The existing single-model critique alone — already
                   mandatory per Rule 20/gate B15, entirely unaffected
                   by this capability's absence.
Validation:        Existing gate B15 (Visual Benchmark & Audit Cycle
                   Completeness) — no new gate.
```

### GC-4 — Content/localization second-pass
```
Trigger:           ux-engine/localization.md applies (a non-Latin-script
                   or multi-locale product, per that file's "When this
                   file applies" section) AND the volume/complexity of
                   interface copy makes a second-pass check on a
                   specific script/locale's naturalness genuinely
                   worthwhile — never invoked for a single-locale,
                   Latin-script product, where this file has nothing to
                   apply in the first place.
Input:             The drafted UI copy/interface strings for the
                   target locale.
Execution Point:   Whichever action is already producing that copy
                   (folded into Order 24's interaction/content work, or
                   wherever ux-writing.md/localization.md is already
                   cited) — no new row.
Model/API:         A Gemini text model via the SDK.
Output:            A suggested refinement list — never auto-applied;
                   reviewed against ux-writing.md's existing content
                   rules (error-message formula, tone-by-state, CTA
                   wording) before any acceptance.
Consumer:          Whichever screen/component's content fields the copy
                   belongs to (ux/ux-rules.md and friends).
Fallback:          Design-Glanza's own existing content-authoring
                   process — the default, always-available path.
Validation:        methodology/test.md's usability dimension (existing,
                   no new gate) — a locale-naturalness issue surfaces
                   there if the refinement was skipped incorrectly.
```

## Explicitly not here
- The image-processing/icon-generation technique that needs no
  generative model at all → `ui-engine/asset-pipeline.md`.
- The native-method composition and the full 6-criteria selection logic
  for GC-1 → `ui-engine/visual-asset-generation.md` (this file documents
  only the Gemini-specific mechanics that capability's API path uses).
- The extraction table GC-2 feeds → `design-reference-engine/
  reference-analysis.md`.
- The critique checklist GC-3 cross-checks against → `ui-engine/
  craft-critique.md`, `ui-engine/ui-audit-framework.md`.
- The content rules GC-4's suggestions are reviewed against →
  `ux-engine/ux-writing.md`, `ux-engine/localization.md`.
