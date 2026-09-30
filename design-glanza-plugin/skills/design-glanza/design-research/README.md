# Design Research Engine

## Responsibility
A structured research discipline that makes research an **active input to
design decisions**, not a documentation exercise run alongside them. Every
file in this folder serves one mandatory chain:

```
RESEARCH → EVIDENCE → INSIGHT → DESIGN PRINCIPLE → UX DECISION → UI PATTERN → VALIDATION
```

This is the elaboration of Rule 21 (`config/operating-rules.md`) and the
technique `agents/design-setup-specialist.md` runs at Design Setup's Step 0
(`workflows/design-setup.md`) — the same position `design-reference-engine/
design-research.md` already occupied, now with real rigor instead of a
folded-in pattern list. It does not replace Design Setup; it is what Design
Setup's Step 0 actually executes from this version forward.

## Why this exists as its own folder, not a deeper `design-reference-engine/` file
`design-reference-engine/*` extracts and classifies **this product's own
visual direction** — from a supplied reference, a questionnaire, or a
selected default. `design-research/*` is broader and prior to that: it
establishes **what's true about users, the domain, interaction conventions,
and the visual landscape in general**, evidenced rather than assumed, so
that `reference-analysis.md`'s extraction and `reference-selection.md`'s
classification are informed choices rather than the first idea that came to
mind. The two folders are sequenced, not parallel: this folder's output
(Design Principles, and any Critical/High finding's design implication)
feeds `design-reference-engine/design-research.md` as its actual technique,
which in turn feeds `design-direction.md`. Neither folder duplicates the
other; see each file's own "Explicitly not here" section for the exact
boundary.

## File map

| File | Owns |
|---|---|
| `research-engine.md` | The mandatory chain's mechanics, the complexity threshold (full vs. lightweight research), and how the chain connects to the 12-phase lifecycle |
| `research-methodology.md` | How to conduct research: inputs, the Known/Assumed/Inferred/Unknown confidence model, the four research areas index |
| `evidence-model.md` | What counts as evidence, sourced against Rule 2's tier order, and the Evidence record shape |
| `insight-model.md` | How raw Evidence becomes an actionable Insight — the Evidence → Insight transformation itself |
| `domain-analysis.md` | The Domain research area: workflows, terminology, domain-specific patterns, regulatory constraints, information structures |
| `interaction-analysis.md` | The Interaction research area: navigation, search, filters, sorting, bulk actions, forms, tables, dashboards, notifications, feedback, error recovery |
| `visual-analysis.md` | The Visual research area: hierarchy, composition, density, typography, color, spacing, navigation, component patterns — principles, not styles |
| `pattern-analysis.md` | Recognizing a UI/UX pattern's *purpose*, not just its name, and the Anti-Generic Design challenge |
| `competitor-analysis.md` | Applying pattern analysis to a named competitor/reference product specifically |
| `research-to-design.md` | The mandatory mapping mechanism — Finding → Insight → Principle → Decision → Pattern → Validation, worked example, priority-driven influence rule, traceability |
| `research.schema.json` | The machine-checkable shape of one Research Finding record (`RF-NNN`) |
| `templates/*` | Fill-in-the-blank instances: a Research Brief, one Finding, a Competitor Analysis, a Pattern Analysis, and the roll-up Research Summary |

## The User research area — deliberately not a separate file
Unlike Domain/Interaction/Visual, "User" research (users, goals, pain
points, frequency, context, expertise, constraints) already has a complete,
rigorous owner: `methodology/empathize.md`'s 11-dimension model, run at the
Empathize phase, well before Design Setup. Duplicating that model here would
create two competing user-research techniques. Instead,
`research-methodology.md` cites Empathize's output as this engine's User
evidence directly — carried forward, not re-derived.

## Relationship to Product Memory (traceability)
Every Research Finding gets an `RF-NNN` ID
(`product-intelligence/traceability.md`'s sideways-reference model, the same
category as `BR-NNN`/`EDGE-NNN`/`DEP-NNN`) and is stored in
`product-builder/research/research-findings.md` — a first-class, durable
artifact, never conversation-only reasoning. A Critical/High finding with no
downstream Design Principle/UX Decision/UI Pattern is a defect, checked by
**B16** (`config/quality-gates.md`), the same way an orphaned requirement is
a defect under B10.

## Explicitly not here
- This product's own visual-direction extraction/classification/authoring →
  `design-reference-engine/*`.
- The domain pack's own stated conventions (cited, not re-derived) →
  `product-types/*.md`, `product-types/domain-standards/`.
- The actual UX/UI technique a Design Principle resolves into → `ux-engine/*`,
  `ui-engine/*` (this folder feeds them, it doesn't replace them).
- The trend-adoption gate and register definitions → `ui-engine/visual-trends.md`.
- The anti-fashion reasoning discipline for an important pattern decision →
  `methodology/design-judgment.md` (this folder's Anti-Generic Design
  challenge is the research-stage counterpart, applied earlier and to a
  broader set of decisions — see `pattern-analysis.md`).
