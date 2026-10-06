# Design Direction

## Responsibility
The authoring technique for `product-builder/ui/design-direction.md` —
synthesizing `reference-analysis.md`'s extraction,
`design-questionnaire.md`'s answers, and `reference-selection.md`'s
classification into one complete, internally-consistent document, then
gating it through user approval before Prototype's UI pass may consume it.
The document's exact field list is `templates/design-direction.md`'s job;
this file owns how those fields get filled and confirmed, not their shape.

## Synthesis discipline
Every field traces to one of three sources, and the document states which,
field by field — the same discipline `product-intelligence/brd-analysis.md`
applies to Explicit/Inferred/Assumed facts, applied here to design fields:
- **From a reference** (`reference-analysis.md`, or `figma-reference.md`
  for an inspected Figma source) — cite which reference, and for Figma,
  the specific `figma-context.json` entry by name/path
  (`figma-context-consumption.md`'s citation discipline).
- **From a stated answer** (`design-questionnaire.md`) — direct user input.
- **From a Design-Glanza default** (`design-samples/`, or a plain
  `ui-engine/*` default with no more specific input available) — always the
  lowest-priority source, exactly mirroring Rule 2's tier order.

A field with conflicting input from two sources (a reference implies dense
tables, but the user's questionnaire answer asked for a spacious feel) is
not silently resolved by picking one — name the conflict, resolve it toward
whichever the product's actual audience/use-case supports
(`methodology/empathize.md`'s findings), and record that resolution as a
stated decision, not an unstated average of the two inputs.

## Do / Don't rules — the concrete, checkable core
The Do/Don't section is not a restatement of the Visual style section in
imperative mood — it exists to catch the specific failure mode Rule 18
names: generating from generic assumption instead of the actual established
direction. A useful Do/Don't rule is falsifiable against a finished screen
(`ui-engine/craft-critique.md`'s deletion/specificity tests are the model to
follow here) — "Don't use rounded-full buttons" is checkable; "keep it
clean" is not and does not belong in this section.

## Traceability
`design-direction.md` is itself a citable source from this point forward —
`agents/ui-designer.md`'s register selection and `agents/design-system-
expert.md`'s token establishment both cite it directly, the same way they
already cite `product-types/*.md` conventions. A design decision made later
that contradicts an established direction field without stating why is a
drift `agents/design-system-expert.md`'s ongoing governance should catch,
the same category of problem it already watches for at the token/component
level.

## The approval gate (Step 5)
Once the document is complete, present a **concise** summary — not the full
document — covering: the classified mode (Reference-Driven/Guideline-
Driven/Custom/Default), the core visual style in one or two sentences, the
primary color and typography choice, and the two or three Do/Don't rules
most likely to matter. Ask directly: *"Does this design direction match
your expectations?"*

- **Confirmed** — record the confirmation, gate passes, hand off to
  Prototype.
- **Changes requested** — update the specific questionnaire answers or
  document fields the feedback touches (re-run `design-questionnaire.md` or
  `reference-selection.md` only where the feedback actually implies a
  change — not the whole document from scratch), regenerate the summary,
  and ask again. This can repeat; there is no fixed cycle limit the way
  `methodology/design-thinking.md`'s Prototype↔Test loop has one, because
  this is a single confirmation gate, not an iterative design loop — but a
  request that keeps not landing after several rounds is itself a signal
  worth naming explicitly to the user rather than silently trying variation
  after variation.
- **No user available to confirm** (an unattended/batch run) — record
  explicitly that approval was waived and why, per B13's pass criterion.
  This is not a silent skip; the waiver itself is a stated fact in the
  document.

## Explicitly not here
- What gets extracted and from where → `reference-analysis.md`,
  `design-questionnaire.md`, `reference-selection.md`.
- The document's exact required fields → `templates/design-direction.md`.
- What happens once the direction is approved (applying it to tokens,
  components, screens) → `agents/design-system-expert.md`,
  `agents/ui-designer.md`, `ui-engine/*`.
