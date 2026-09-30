# Research Methodology

## Responsibility
How to actually conduct research: what inputs are available, how to label
what you don't know rather than invent it, and an index into the four
research areas. This is the "how to gather," feeding `evidence-model.md`'s
"how to record what was gathered."

## Research inputs
Use whatever is actually available — never wait for a "real" external
research pass that isn't going to happen for most engagements:

- BRD/PRD/SOW and the full requirement model (`REQ-NNN`, `BR-NNN`).
- User roles and their permissions (`ROLE-NNN`, `product-intelligence/user-roles.md`).
- Domain standards, where matched (`product-types/domain-standards/`,
  Rule 17).
- Existing product patterns — this product's own current UI, if a redesign
  (`workflows/redesign-product.md`).
- Approved references the user supplied
  (`design-reference-engine/reference-analysis.md`'s 13 recognized forms).
- Competitor/reference products named or implied by the user or the domain
  (`competitor-analysis.md`).
- Accessibility standards (`ux-engine/accessibility.md`'s baseline, plus
  any domain-mandated stricter bar).
- Interaction pattern conventions already codified in `ux-engine/*`.
- Visual benchmarks — prior generated screens' own
  `templates/visual-gap-analysis.md` history, where this is not the first
  pass.

## Known / Assumed / Inferred / Unknown
Every piece of research evidence carries exactly one of these four labels —
a sharper vocabulary than a single "confidence" score, because *how* a
research fact is uncertain changes what mitigates the risk:

| Label | Meaning | Example |
|---|---|---|
| **Known** | Directly stated in an available input, or directly observed in a supplied reference/existing product | "The BRD states approvals require two roles in sequence" |
| **Assumed** | No input states it; filled from domain convention or best practice, per Rule 2's tier order | "Assumed inline-edit is preferred for this table density, per `product-types/erp.md`'s convention — no reference confirms this" |
| **Inferred** | A reasonable reading of an input that doesn't state the fact directly | "This screenshot's spacing implies an 8px base unit" |
| **Unknown** | Genuinely no evidence and no safe domain default — an open question, not a guess (per the question-vs-proceed rule, `config/operating-rules.md`) | "Whether this product needs offline support is unknown — not stated, and both domain answers are plausible" |

This maps onto, and does not replace, Rule 10's assumption-tag machinery
(`config/output-contract.md`) — **Known** needs no tag; **Assumed** and
**Inferred** both get the standard `[ASSUMPTION: ... | BASIS: ... |
IMPACT: ...]` tag (Inferred cites the specific input it was read from as its
BASIS, Assumed cites the domain-convention tier); **Unknown** is not
tagged as an assumption at all — it's surfaced as an open question per the
phase-completion report shape (`config/output-contract.md`).

**Never fabricate research evidence.** A Known-labeled fact that turns out
to be Assumed or Inferred is not a shading of confidence, it's a false
citation — the same integrity bar Rule 2's source-of-truth tiers already
enforce for requirements, applied here to design evidence.

## The four research areas
Each has its own file; this file only indexes them:

| Area | What it covers | File |
|---|---|---|
| User | Users, goals, pain points, frequency, context, expertise, constraints | Already owned by `methodology/empathize.md`'s 11-dimension model — cited here, not re-derived |
| Domain | Workflows, terminology, domain-specific patterns, regulatory constraints, information structures | `domain-analysis.md` |
| Interaction | Navigation, search, filters, sorting, bulk actions, forms, tables, dashboards, notifications, feedback, error recovery | `interaction-analysis.md` |
| Visual | Hierarchy, composition, density, typography, color, spacing, navigation, component patterns | `visual-analysis.md` |

Competitor/pattern analysis (`competitor-analysis.md`, `pattern-analysis.md`)
is not a fifth area — it's a technique applied *within* Domain, Interaction,
and Visual research wherever a named reference or competitor exists to
analyze, distinct from researching what's generally conventional.

## Recording a finding
Every research pass produces zero or more `RF-NNN` records
(`templates/research-finding.md`, `research.schema.json`), stored in
`product-builder/research/research-findings.md`. A research pass that
surfaces nothing new (everything already covered by a prior finding, or
genuinely no signal found) still records that explicitly — "researched, no
new finding" — the same disclosed-null posture `product-types/domain-
standards/`'s pending entries already use, never silently skipped.

## Explicitly not here
- The Evidence and Insight record shapes → `evidence-model.md`,
  `insight-model.md`.
- Each research area's own technique → `domain-analysis.md`,
  `interaction-analysis.md`, `visual-analysis.md`.
- Competitor/pattern analysis technique → `competitor-analysis.md`,
  `pattern-analysis.md`.
- How a finding becomes a design decision → `research-to-design.md`.
- The complexity threshold (when full research vs. lightweight applies) →
  `research-engine.md`.
