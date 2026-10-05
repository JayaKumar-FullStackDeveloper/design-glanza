# Figma Reference

## Responsibility
The extraction technique for the one reference form, of the 13
`reference-analysis.md` names, whose source is often *structurally
inspectable* rather than only visible as pixels — a Figma design file. This
file is a sibling to `reference-analysis.md`, never a replacement for it:
where a Figma reference can only be viewed as a flat image (export,
screenshot, or structural inspection genuinely unavailable), that file's
generic technique still applies unchanged, at its existing Inferred/Medium
confidence. This file exists for the case `reference-analysis.md` could only
gesture at — extracting the *actual* variables, components, variants, and
auto-layout data a Figma file holds, at Explicit confidence, instead of
inferring them from pixels.

Where the extracted context is then *used* — how it's folded into
`ui/design-direction.md` and, from there, into the existing UI-generation
action pipeline — is `figma-context-consumption.md`'s job, not this file's.
This file only owns getting from "a Figma reference was detected" to a
normalized `figma-context.json`.

## Mandatory tool-invocation procedure
This is binding, not optional, whenever a Figma reference is detected
(`product-intelligence/brd-analysis.md`'s input-recognition step):

1. **Load the `figma-use` skill first.** That skill's own mandatory
   prerequisite ("invoke this skill BEFORE every `use_figma` tool call") is
   binding here too — never call `use_figma` directly without it. Where a
   live file/node needs `get_design_context` specifically, load
   `figma-design-to-code` first, by the same rule.
2. **Call it read-only.** Inspect only — list/read nodes, variables,
   components, styles. Never create, edit, or otherwise mutate a Figma
   node. This technique has no write path at all; there is nothing in this
   file that ever instructs a create/edit call.
3. **Prefer structured inspection over a flat image whenever the file's own
   structure is actually inspectable** — named layers, bound variables,
   component/variant definitions, auto-layout properties are a strictly
   stronger signal than a screenshot of the same frame, per
   `product-intelligence/brd-analysis.md`'s existing Figma row. Do not fall
   back to image-only extraction just because it's simpler when structural
   data is genuinely available.
4. **On any auth/availability/permission failure, degrade explicitly.** Set
   `figma-context.json`'s `source.inspectionMode` to `"image-fallback"`,
   record `source.fallbackReason` (what failed and why), and continue via
   `reference-analysis.md`'s existing image-only technique at its existing
   Medium confidence — never silently substitute one mode for the other,
   and never block the rest of Design Setup because Figma access failed.
   This is the same degrade-with-a-disclosed-Note posture
   `scripts/capture-render.py` already uses when Playwright isn't
   installed.

## The Figma → Design-Glanza mapping table
The concrete correspondence this technique extracts, field by field. Every
row's "Extracted as" column is a `figma-context.schema.json` path; every
value at that path carries its own `confidence` tag (explicit when backed
by inspected structure, inferred/assumed per the rules below) — this table
does not restate that discipline per row, see "Confidence rules" below
once.

| Figma concept | Extracted as | Cites (existing file, never restated here) |
|---|---|---|
| Variable collection + mode (color) | `tokens.colors` | `ui-engine/color-system.md`, `design-tokens/semantic-tokens.md` |
| Variable collection + mode (type/spacing/radius/elevation/sizing) | `tokens.typography/spacing/radius/elevation/sizing` | `ui-engine/{typography,layout-system,design-system}.md`, `design-tokens/token-schema.md` |
| Component + its variant axis | `components.components[]` + `components.variants[]` | `component-registry/*` |
| Component property/prop definition | `components.properties[]` | `component-registry/registry-schema.md`'s field 4 (Variants) |
| A variant mapping to a resting/loading/empty/error/etc. treatment | `components.states[]` | `ux-engine/state-design.md`'s 13 mandatory states |
| A recurring multi-component grouping (e.g. filter bar + table) | `patterns[]` | `component-registry/composition-patterns.md` |
| Frame auto-layout (direction/gap/padding/alignment) | `layouts[].autoLayout` | `ui-engine/layout-system.md`'s grid/spacing vocabulary |
| A distinct breakpoint-variant frame | `responsive[]` | `ui-engine/responsive-system.md`'s seven adaptation decisions |
| A stated/inferable hover/press/transition behavior | `interactions[]` | `ux-engine/interaction-design.md` |
| Icon stroke/fill convention, size consistency | `iconography` | `ui-engine/visual-hierarchy.md` |
| Photography vs. illustration use | `imagery` | `ui-engine/visual-trends.md` |
| Consistent emphasis signal across frames; layer/component naming pattern | `visualRules.hierarchySignals` / `.namingConventions` | `ui-engine/visual-hierarchy.md` |
| A frame matching the new screen's role closely enough to serve as the comparison target | `screens[]` (`role` field) | `ui-engine/visual-benchmark.md`'s Reference column |

## Confidence rules
- **Explicit** — read directly from Figma's own structured data: a bound
  variable's resolved value, a component's actual variant/prop
  definition, an auto-layout's actual direction/gap/padding. This is the
  tier `reference-analysis.md`'s generic technique cannot reach from a
  flat image alone — it is the entire reason this file exists.
- **Inferred** — a reasonable reading with no bound structural data behind
  it (e.g. a visual rhythm that looks like an 8px base unit but isn't
  backed by an actual spacing variable) — same meaning as
  `reference-analysis.md`'s existing Inferred tag, same handling
  downstream.
- **Assumed** — no signal at all; a Design-Glanza default was used, per
  `figma-context-consumption.md`'s fallback rule.

A field extracted at Explicit confidence is never silently downgraded to
read as Inferred later, and an Inferred/Assumed field is never upgraded to
read as Explicit just because it happens to match what a human would guess
anyway — the tag records how the value was actually obtained, not how
confident it feels in hindsight.

## Extract the language, not the screen — strengthened for this source
`reference-analysis.md`'s existing rule ("the goal is the underlying visual
*system* a reference implies, not a literal copy of what's on screen")
applies here with one addition, stated explicitly because this source makes
the opposite mistake easier to make than a screenshot does: **exact,
structurally-extracted data is *easier* to clone verbatim than a flat
image, not harder** — a bound color variable or an auto-layout's exact gap
value can be copied pixel-for-pixel with zero interpretation required,
which is precisely why this is the discipline that most needs restating
here, not relaxing. Extracting a Figma file's token/component *vocabulary*
for reuse across a genuinely new screen is this technique's job;
reproducing one of its existing frames unchanged under a new label is not —
see `figma-context-consumption.md`'s non-negotiable output rule for how
this is enforced at the point a new screen is actually generated.

## Explicitly not here
- The generic, image-only extraction technique used when no Figma
  structure is inspectable → `reference-analysis.md`.
- The structured context's exact shape → `figma-context.schema.json`.
- How the extracted context is applied once Design Setup has it — the
  precedence rule, the field-by-field influence on UI generation → `figma-
  context-consumption.md`.
- Classifying Reference-Driven vs. Guideline-Driven vs. Custom vs. Default →
  `reference-selection.md` (a Figma reference is the strongest instance of
  Reference-Driven, never a 5th mode).
- The document shape this ultimately feeds → `design-direction.md`,
  `templates/design-direction.md`.
- Comparing the eventual generated screen back against this extraction →
  `ui-engine/visual-benchmark.md`'s Level A/Level B Figma comparison.
- Business-logic facts drawn from the same Figma file → `product-
  intelligence/brd-analysis.md` (a separate extraction, same boundary rule
  `reference-analysis.md` already states for every other reference form).
