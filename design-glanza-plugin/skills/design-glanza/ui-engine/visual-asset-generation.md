# Visual Asset Generation

## Responsibility
A shared, cross-lifecycle capability — not a step tied to one phase or
action — for producing real (non-placeholder) photographic/illustrative
imagery wherever any of the 41 actions in
`workflows/execute-product-builder.md` contextually needs it: a landing
page's hero image, a product screenshot composite, an empty-state
illustration, a marketing OG card's background, an avatar/persona image.
This file is invoked by whichever action needs imagery (most often Order
28-29, Design System/Component Architecture, and Order 34, Implement) —
it does not introduce a new row, phase, gate, or agent of its own. Distinct
from `ui-engine/asset-pipeline.md`: that file owns mechanical processing
and custom SVG icon sets, neither of which needs a generative model; this
file owns the harder case — imagery with photographic or illustrative
content a token/shape composition can't produce.

## Step 0: is generation actually required here?
Not every action needs this capability, and it never runs
speculatively. Before invoking anything below, the acting
agent/workflow asks:
- Does this specific artifact (this screen, this card, this section)
  actually call for photographic/illustrative imagery, per its own spec
  (`templates/screen-specification.md`, `component-spec.md`,
  `product-types/landing-page.md`'s section library) or an explicit
  Figma-sourced asset (`figma-context.json`)?
- Is the need already satisfied by something that exists — a reusable
  asset already generated earlier in this product's lifecycle (see
  Reuse below), a Figma-exported asset, or a user-supplied image? If so,
  reuse it; generation is the fallback, not the default.
- Would an icon, a token-driven shape/gradient composition
  (`ui-engine/asset-pipeline.md`), or no image at all satisfy the actual
  design intent just as well? If so, that is the right answer, not a
  generated photo — generating imagery nobody asked for is the same
  defect category as any other invented content (Rule 10).

Only when the answer is genuinely yes does the capability below run.

## The two generation paths

### Native path — always runs when generation is warranted
Design-Glanza's own method: compose the needed imagery from the
product's already-established visual language — token-driven
gradients/shape compositions, illustrated-icon arrangements built through
`asset-pipeline.md`'s SVG discipline, or an abstracted/geometric
illustration consistent with `ui-engine/visual-trends.md`'s selected
register. It needs no external model, no API key, no network access —
only `Read`/`Write`/`Edit`, matching Design-Glanza's own restricted tool
surface — so it is always available and always runs first, as the
baseline candidate. It cannot produce photorealism, but it is always
on-brand by construction (it draws from the product's own tokens) and
never blocks on anything external.

### API path — runs in parallel, only when an image-generation API is actually configured
Detection, SDK/REST mechanics, the execution boundary, and the full
security posture (never log/hardcode/commit/transmit the key) are
`ui-engine/gemini-capability.md`'s GC-1 entry — this section states only
the image-generation-specific decision, not the mechanics it already
covers. When the Product Builder's own environment has a configured
image-generation credential (`GEMINI_API_KEY`, the default/primary path
via the official Google GenAI SDK; `OPENAI_API_KEY` as an alternative
path when its specific strengths below are actually needed) — checked,
never assumed — the API path runs *alongside* the native path, not
instead of it, producing a second candidate:
- **Model selection by need, not default**: a photorealistic scene or
  stock-photo-style image uses a Gemini image model (verified against a
  live model list, per `gemini-capability.md`, not a hardcoded id); any
  image where readable text must render (a pricing card, an OG card with
  a headline, an infographic) and Gemini's available models don't render
  text reliably enough uses a GPT image model instead; a
  transparent-background icon/logo asset uses whichever configured model
  actually supports alpha transparency — not every image model does, and
  this is checked before generation, not discovered after.
- **Prompting** states image type, subject, environment, technical
  specs (framing/lighting), and explicit exclusions (no placeholder
  watermarks/logos/fabricated text) — grounded in this specific
  product's actual `product/product-definition.md`, `ui/
  design-direction.md`, and (where one exists) `figma-context.json`'s
  described scene/subject, never a generic stock-photo prompt that could
  belong to any product.
- **Unavailable or failing** — no configured credential, a failed call,
  or an auth/quota error: continue automatically on the native path
  alone. This is never a blocking condition, never a reason to pause the
  lifecycle, and never surfaced as an error requiring manual approval —
  it is a normal, expected fallback, logged as such in the asset
  manifest (below), not hidden.

## Selection: compare, never default to the API result
Producing two candidates is only useful if both are actually evaluated —
the API result is never auto-selected for its photorealism alone. The
acting agent compares both candidates against, in order:
1. **BRD/requirement fit** — does the image actually depict what the
   governing `REQ-NNN`/product-definition content describes, not a
   generic stand-in for the same category of business?
2. **Figma reference fit** — where a Figma Design Context exists, does
   the candidate match its structural composition, subject matter, and
   asset treatment (`design-reference-engine/figma-context-
   consumption.md`'s imagery-fidelity rule — never a generic gradient or
   emoji substituting for a real illustrated asset the reference
   actually shows)?
3. **Design direction & token fit** — does it sit comfortably inside the
   approved `ui/design-direction.md` register and the product's color
   ramps (`ui-engine/color-system.md`), rather than importing a visual
   style (lighting, palette, mood) that clashes with the rest of the
   product?
4. **Accessibility** — any text baked into the image is also available
   as real text/alt content (an image is never the only carrier of
   essential information); a color-coded element inside the image still
   clears the color-blind-safety rule; sufficient contrast exists
   wherever UI content (a CTA, a label) will sit on top of it.
5. **Product consistency** — does it match the visual treatment of
   every other already-generated/selected asset in this product (same
   lighting mood, same illustration style), rather than each image
   looking like it came from a different source?
6. **Current action/gate context** — does it satisfy the specific gate
   this action is working toward (e.g. B15's visual-benchmark cycle,
   B9's responsive behavior if the image must crop sensibly across
   breakpoints)?

Aesthetic preference alone never decides between two candidates that
differ on any of the above — the more-fitting candidate wins even when
the other is more polished-looking. The non-selected candidate is kept
(see Provenance), not discarded, in case a later action's different
criteria make it the better fit after all.

## Reuse before regenerating
Before generating anything, check the product's own asset manifest
(below) for an existing `ASSET-NNN` already serving the same need (the
same screen's hero image needed again at Audit's refinement pass, or a
shared illustration style other screens already established) — reuse it
rather than regenerating a fresh candidate that might drift from an
already-approved visual language. Regeneration is warranted only when the
existing asset's content genuinely doesn't fit the new need (a different
subject, not just a stylistic re-roll).

## Asset manifest — traceability, provenance, QA
Every generated-or-selected asset is recorded as an `ASSET-NNN` entry (a
seventh sideways reference alongside `RF-NNN`/`SCENARIO-NNN`/`ADR-NNN`,
per `product-intelligence/traceability.md`) in
`product-builder/ui/visual-assets/asset-manifest.json`, one entry per
asset:

```json
{
  "id": "ASSET-014",
  "phase": "PROTOTYPE (UI)",
  "action_order": 29,
  "serves": ["REQ-021", "SCREEN-009"],
  "figma_source": "figma-context.json#/screens/SCREEN-009/hero",
  "paths_attempted": ["native", "api:gemini-3.1-flash-image-preview"],
  "selected": "api:gemini-3.1-flash-image-preview",
  "selection_reason": "Native composition couldn't depict the specific onboarding scene REQ-021 describes; API candidate matched design-direction register and cleared contrast check with the overlay CTA.",
  "rejected": [
    {"path": "native", "reason": "On-brand but too abstract to convey the specific scene — logged, not discarded."}
  ],
  "file": "output/public/images/hero-onboarding.webp",
  "reused_by": [],
  "qa_deviation": null
}
```

- **`qa_deviation`** records anything a later QA/Audit pass flagged
  against this asset (a contrast regression after a token change, a
  structural mismatch a Figma re-check found) — never silently
  regenerated without a logged reason, the same no-silent-change
  discipline `visual-regression/*` already applies to screen baselines.
- **`reused_by`** lists every later `ASSET-NNN`/screen that reused this
  entry instead of regenerating — the concrete evidence the reuse rule
  above is actually followed, not just stated.
- An asset with no `serves` citation is an orphaned asset — the same
  defect category `traceability.md` already treats an uncited
  requirement/artifact as being, applied here to generated imagery.

## Explicitly not here
- Gemini-specific detection/SDK/security mechanics, and the other
  non-imagery Gemini capabilities (reference analysis, visual-QA second
  opinion, content/localization) → `ui-engine/gemini-capability.md`.
- Mechanical image processing (resize/optimize/OG-card) and custom SVG
  icon sets → `ui-engine/asset-pipeline.md`.
- The Figma imagery-fidelity rule this file's selection step 2 checks
  against → `design-reference-engine/figma-context-consumption.md`.
- Where in the pipeline this capability gets invoked from →
  `workflows/build-product.md` (Implement's asset step),
  `ui-engine/component-system.md` (Prototype's visual-asset guidance).
- The ID-scheme registry this file's `ASSET-NNN` joins →
  `product-intelligence/traceability.md`.
