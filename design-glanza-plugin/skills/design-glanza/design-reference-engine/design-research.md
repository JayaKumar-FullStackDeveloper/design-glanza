# Design Research

## Responsibility
Design Setup's **first** step (Step 0, before reference detection) — the
entry point into the full **Design Research Engine**, `design-research/*`
(Rule 21, `config/operating-rules.md`), run here so that the questions
asked in `design-questionnaire.md` and the direction written in
`design-direction.md` are informed by real, evidenced pattern knowledge —
never by whatever the first idea that comes to mind happens to be, and
never merely documented alongside a design decision made some other way.
This is where Design-Glanza reasons like a senior product designer who
already knows the landscape, rather than a template generator with no
point of view.

**As of v1.0.10, this step's actual technique is `design-research/*`,
not this file.** This file remains the short, Design-Setup-scoped pointer
`workflows/design-setup.md` and `agents/design-setup-specialist.md` cite for
*when* research runs in the sequence; the full mandatory chain — Research →
Evidence → Insight → Design Principle → UX Decision → UI Pattern →
Validation — its confidence/priority model, the four research areas, and
the Anti-Generic Design challenge are all owned by `design-research/*`. See
`design-research/README.md` for the file map.

## Why this runs even when a reference already exists
`reference-analysis.md` extracts what *one specific reference* does.
Design Research is broader: it establishes what's currently *conventional*
and *appropriate* for this domain in general, which is what makes it
possible to tell whether a supplied reference is worth following faithfully
or is itself an outlier worth deviating from. Skipping this step and going
straight from a reference (or a blank page) to a screen is exactly the
"functional-looking interface with no design reasoning behind it" failure
mode this file exists to prevent.

## What to research, per category
Each row below is now a `design-research/*` research area or technique,
producing real `RF-NNN` findings — not a one-line pattern list:

| Category | Owned by |
|---|---|
| Current product-design patterns, modern SaaS/admin patterns | `design-research/domain-analysis.md`, `design-research/interaction-analysis.md` |
| Domain-specific UI conventions, regulatory constraints | `design-research/domain-analysis.md` (cites `product-types/<domain>.md`, `product-types/domain-standards/` — never re-derives them) |
| Information density, hierarchy, composition, typography, color, spacing | `design-research/visual-analysis.md` |
| Navigation, search, filters, sorting, bulk actions, forms, tables, dashboards, notifications, feedback, error recovery | `design-research/interaction-analysis.md` |
| Named competitor/reference products | `design-research/competitor-analysis.md` |
| Any candidate pattern's purpose, mechanism, and the Anti-Generic Design challenge | `design-research/pattern-analysis.md` |
| Current visual trends | `ui-engine/visual-trends.md`'s registers — current, not timeless, by that file's own design — checked for staleness per its own Staleness check section |

## The anti-trend-slave rule
Researching current trends is not the same as adopting them. Every pattern
surfaced here still has to clear `ui-engine/visual-trends.md`'s 3-point
trend-adoption gate and `methodology/design-judgment.md`'s anti-fashion
strip-away test before it's used — Design Research's job is to make sure
the *option set* considered is current and complete, not to pre-select the
fashionable option from it. A pattern that's common right now but doesn't
fit this product's density/audience/domain is a researched-and-rejected
option, recorded as such (`design-research/pattern-analysis.md`'s Anti-
Generic Design challenge), not silently adopted because "that's what
everyone does now."

## Output
Real, `RF-NNN`-tagged Research Finding records
(`design-research/templates/research-finding.md`), stored in
`product-builder/research/research-findings.md`, rolled up in
`product-builder/research/research-summary.md`
(`design-research/templates/research-summary.md`) — **not** a one-line
pattern list, and **not** folded silently into `design-direction.md` with
nothing else surviving (the prior v1.0.9 posture). The condensed,
Critical/High-priority subset of that summary still feeds
`design-questionnaire.md`'s answers (a researched pattern can pre-answer a
question the same way a reference does) and `design-direction.md`'s Design
principles field — but the full evidence trail persists in `research/`,
addressable by `RF-NNN` from any later artifact (Rule 21).

## Explicitly not here
- Extracting what one specific supplied reference does →
  `reference-analysis.md`.
- The domain's own stated conventions (cited here, not re-derived) →
  `product-types/*.md`, `product-types/domain-standards/`.
- The actual trend-adoption gate and register definitions →
  `ui-engine/visual-trends.md`.
- The anti-fashion reasoning discipline itself →
  `methodology/design-judgment.md`.
- The full research technique, the confidence/priority model, and the
  mandatory Finding → Insight → Principle → Decision → Pattern → Validation
  mapping → `design-research/*` (see `design-research/README.md`).
