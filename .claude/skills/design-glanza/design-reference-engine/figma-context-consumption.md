# Figma Context Consumption

## Responsibility
The explicit contract for how a produced `figma-context.json`
(`figma-reference.md`) is actually *used* once Design Setup has it — how:

```
New Screen Requirement + Figma Design Context + Existing Design-Glanza Standards
```

flows through the existing UI-generation action pipeline to produce a new
screen. `figma-reference.md` owns getting *to* the context; this file owns
what happens *with* it from that point forward. Without this file, Figma
integration would be "just another input that's vaguely richer" — this file
is what makes it a concrete, checkable precedence rule instead.

## Governing statement
- **BRD** = requirements / functionality / screen purpose — the source of
  truth for **WHAT** needs to be designed. Unchanged by anything below;
  never overridden by Figma.
- **Figma Design Context** = the existing product's visual/design-system
  language — the source of truth for **HOW** the new screen should look.
  Never a source of IA, flows, or screen purpose.
- **Design-Glanza** = the complete, unmodified UX/UI methodology and
  generation process — remains fully responsible for all design reasoning
  and execution. Figma is an additional input to that process, never a
  substitute for any part of it.

This is already structurally enforced elsewhere, not newly invented here:
`reference-analysis.md`'s boundary rule already separates "design
direction" facts from "business requirement" facts extracted from the same
reference; `reference-selection.md` already states, for Reference-Driven
mode generally, that "this product's actual IA/flows/content still come
from `ux-engine/*`, not from the reference's own structure." This file
exists so the statement is checkable in one place, at the point it actually
governs a decision, rather than only implied across several files.

## The precedence rule
Applied once, consistently, by whichever existing agent already owns the
decision at that point in the pipeline (`agents/design-system-expert.md`
for tokens/components, `agents/ui-designer.md` for visual
hierarchy/responsive application — no new agent, see "No new agent" below):

1. **If a genuine Figma pattern/component/token exists for this specific
   need, prefer it.** Cite the specific `figma-context.json` entry (path +
   `sourceRef`) the same way `reference-analysis.md`'s confidence tagging
   already requires citing a source.
2. **If no matching Figma pattern exists, use the existing Design-Glanza
   standard** (`design-tokens/*`, `component-registry/*`, `ui-engine/*`)
   **while maintaining consistency with the extracted Figma design
   language** — same density/register/radius-and-elevation feel, even
   where the specific value is Design-Glanza's own default. A
   Design-Glanza default that technically "passes" its own rules but
   visibly clashes with the established Figma language (e.g. a sharp,
   dense enterprise register defaulting into a soft, spacious one just
   because no Figma radius token happened to exist for this exact
   component) has not satisfied this rule.

Nothing here changes *who* makes the decision or *which file* they
consult — it changes what they prefer when a Figma-sourced answer and a
Design-Glanza default both exist, and requires a citation either way.

## Field-by-field influence table
Each row cites the specific `figma-context.json` section and the specific
existing consumer file that already owns that decision — no new consumer
file is introduced by this table; every citation resolves to a file that
exists today.

| Influenced area | figma-context.json source | Existing consumer (unchanged) |
|---|---|---|
| Typography | `tokens.typography` | `ui-engine/typography.md`, `design-tokens/token-schema.md` |
| Colors | `tokens.colors` | `ui-engine/color-system.md`, `design-tokens/semantic-tokens.md` |
| Spacing | `tokens.spacing` | `ui-engine/layout-system.md`, `design-tokens/token-schema.md` |
| Radius / elevation | `tokens.radius` / `tokens.elevation` | `design-tokens/token-schema.md` |
| Sizing | `tokens.sizing` | `design-tokens/token-schema.md` |
| Layout / grid | `layouts` | `ui-engine/layout-system.md` |
| Components | `components.components` | `component-registry/*` |
| Variants | `components.variants` | `component-registry/registry-schema.md` |
| States | `components.states` | `ux-engine/state-design.md` |
| Visual hierarchy | `visualRules` | `ui-engine/visual-hierarchy.md` |
| Responsive behavior | `responsive` | `ui-engine/responsive-system.md` |
| Interaction patterns | `interactions` | `ux-engine/interaction-design.md` |

A row with no matching entry in `figma-context.json` (the Figma file simply
has nothing to say about, e.g., a screen-specific empty state it never
depicted) falls through to step 2 of the precedence rule above — existing
Design-Glanza technique, kept consistent with whatever Figma language was
extracted elsewhere on the same screen.

## Non-negotiable output rule
The result of applying this contract is always a **new** screen serving
the new screen requirement — never a literal reproduction of an existing
Figma frame, even when that frame is an extremely close match to the new
requirement. This restates, scoped specifically to this contract so it
cannot be read as implied permission to "just reuse the closest frame,"
`reference-analysis.md`'s and Rule 18's existing anti-literal-copy
discipline, strengthened in `figma-reference.md` for this source
specifically. A screen that satisfies the BRD requirement while reading as
if it belongs to the same product as the Figma reference has succeeded; a
screen that is recognizably a copy of one existing frame, relabeled, has
not — regardless of how well it otherwise scores.

## No new agent
`agents/design-setup-specialist.md` already owns "detect and analyze any
design references the user provided" — a Figma reference is one more
reference form it handles (`agents/design-setup-specialist.md`'s Input
section already named Figma links/files before this capability existed).
`agents/design-system-expert.md` and `agents/ui-designer.md` already own
token establishment and screen/component application from
`design-direction.md` + `design-tokens.json` + `components.md` — this
contract is resolved **before** those three artifacts are written (at
Design Setup, rows 15-18 of `workflows/execute-product-builder.md`), so by
the time those two agents run, the preference is already folded into their
existing inputs. Neither agent needed a new capability of its own; both
needed only a richer, better-cited input, which this file supplies the
rule for. No new generation agent was introduced, and none should be —
reaching that conclusion required tracing this contract through to row 34
(Implement) and confirming no step in between needs a Figma-specific
branch of its own, not merely assuming it.

## Explicitly not here
- How a Figma reference is detected and normalized into `figma-
  context.json` in the first place → `figma-reference.md`.
- The structured context's exact shape → `figma-context.schema.json`.
- Classifying Reference-Driven vs. Guideline-Driven vs. Custom vs. Default
  → `reference-selection.md`.
- The document this contract's output is folded into → `design-
  direction.md`, `templates/design-direction.md`.
- Comparing the eventual generated screen back against the Figma context →
  `ui-engine/visual-benchmark.md`'s Level A/Level B Figma comparison.
- The existing UI-generation action pipeline's own row-by-row mechanics →
  `workflows/execute-product-builder.md` (this file is cited *from* that
  table's rows 15-18, it does not restate or reorder them).
