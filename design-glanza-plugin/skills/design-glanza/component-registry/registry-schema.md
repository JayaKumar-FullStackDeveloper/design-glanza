# Registry Entry Schema

## Responsibility
The fixed 13-field shape every registry entry follows, and exactly how
each field maps onto (or extends) `ui-engine/component-system.md`'s
existing 8-point framework — so the registry is legible as an extension
of that framework, never a second, competing one.

## The 13 fields

| # | Field | Relationship to `component-system.md` |
|---|---|---|
| 1 | Purpose | = framework point 1, pre-answered |
| 2 | When to use | **New** — the condition under which this component is the right choice |
| 3 | When NOT to use | **New** — the condition under which a different component/pattern serves better, named specifically, not just "use judgment" |
| 4 | Variants | = framework point 3, pre-answered with the common closed set |
| 5 | States | = framework point 4 — cites `ux-engine/state-design.md`'s 13 mandatory states, naming which apply to this component specifically |
| 6 | Interaction behavior | = framework point 5 — cites the exact `ux-engine/interaction-design.md` (or `form-design.md`/`search-ux.md`) rule, never restates it |
| 7 | Accessibility requirements | = framework point 7 — cites `ux-engine/accessibility.md`'s semantic mapping for this component's role |
| 8 | Responsive behavior | = framework point 8 — cites `ui-engine/responsive-system.md`'s reflow rule for this component |
| 9 | Content rules | = framework point 6 — label/copy conventions, citing `ux-engine/ux-writing.md` where wording is involved |
| 10 | Validation rules | **New** — only populated for input-bearing components; cites `ux-engine/form-design.md`/`product-intelligence/business-logic.md`, states "not applicable" for non-input components |
| 11 | Composition rules | **New** — which other registry entries this one commonly combines with, and the fixed rule governing that combination (cites `composition-patterns.md` for a named organism, or states "atomic — not typically composed") |
| 12 | Common UX mistakes | **New** — a named, checkable anti-pattern list specific to this component, not a restatement of `craft-critique.md`'s visual anti-cliché catalog |
| 13 | Domain-specific usage | **New** — cited pointers into `product-types/*.md`'s UI-pattern point where a domain materially changes this component's default (e.g. dense tables in ERP); "no domain-specific variance" where none applies |

## Conventions every entry follows
- **Values are token paths, never raw values.** Every size/color/spacing/
  radius/motion value an entry's Variants or States implies is a
  `design-tokens/token-schema.md` path (Rule 23) — an entry never states
  "use a light gray background," it states `color.semantic.neutral.background`.
- **Cite, don't restate.** Fields 5–9 point at the file that already owns
  that rule in full; an entry that re-derives interaction/accessibility/
  responsive behavior instead of citing it has drifted from its source and
  will eventually disagree with it.
- **"Not applicable" is a real, stated answer**, not an omission — field 10
  (Validation rules) is legitimately "not applicable" for a Tooltip, and
  field 13 (Domain-specific usage) is legitimately "no domain-specific
  variance" for most atoms. Silence is never the same as "not applicable."

## Reuse-first, per entry
Before a Product Builder specifies a *new* component
(`agents/design-system-expert.md`'s existing reuse-vs-new decision), it
checks whether one of these ~29 entries (or a `composition-patterns.md`
organism) already covers the need — per `registry-integration.md`'s
registry-first rule. An entry's own "When NOT to use" field is itself part
of that check: it names the *other* registry entry that should be reached
for instead, so the check is a lookup, not a fresh judgment call each time.

## Explicitly not here
- The framework itself → `ui-engine/component-system.md`.
- Any specific entry's actual content → `components-*.md`.
- The registry-first enforcement mechanism → `registry-integration.md`.
