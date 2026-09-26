# Template: Requirement Matrix

## Purpose
The atomic, uniquely-identified record of every requirement a product must
satisfy — the anchor every other artifact traces back to. Reusable across
every domain: the schema below is fixed regardless of what the requirements
actually say.

## Required inputs
- `product-intelligence/brd-analysis.md`'s extracted, confidence-tagged facts.
- `product-intelligence/requirement-engine.md`'s decomposition technique and
  ID scheme.
- `product-intelligence/user-roles.md`'s `ROLE-NNN` list (for the Actor
  field), `business-logic.md`'s `BR-NNN` list, and
  `dependency-analysis.md`'s `DEP-NNN` list (both cited, not restated).

## Output structure
One row per requirement, fields exactly as defined in
`product-intelligence/requirement-engine.md`:

| Field | Definition |
|---|---|
| ID | `REQ-NNN` |
| Source | Quote, inferred-from-gap note, or `[ASSUMPTION: ...]` tag |
| Description | One atomic, independently testable behavior |
| Type | Behavioral / Data / Business-rule / Permission / Integration / Non-functional |
| Actor | `ROLE-NNN` or `SYSTEM` |
| Action | The verb-level behavior |
| System response | The immediate, observable result |
| Business rule | `BR-NNN` cross-reference |
| Validation | Condition(s), or a `BR-NNN` cross-reference |
| Dependency | Other `REQ-NNN` IDs, or `DEP-NNN` |
| Confidence | Explicit / Inferred / Assumed |
| Priority | Must / Should / Could / Won't (MoSCoW) |
| Status | draft / validated / built / tested / audited / deprecated |
| Downstream artifacts | `USER`, `FLOW-NNN`, `SCREEN-NNN`, `COMPONENT-NNN`, `TEST-NNN` |

## Quality criteria
- Every row has every field populated — no blank cells, no field silently
  omitted because "it didn't seem to apply" (mark `N/A` with a reason
  instead).
- Every row's Source is either a genuine citation or an explicit assumption
  tag — never asserted as fact with no traceable origin.
- No two rows describe the same atomic behavior (duplicate detection per
  `requirement-engine.md`); no row bundles two independently-testable
  behaviors into one (atomicity rule).
- This is exactly what `config/quality-gates.md`'s **B1 — Requirement
  Completeness** gate checks, mechanically, via
  `scripts/validate-requirements.py`.

## Example structure
_Illustrative only — placeholders, not a real product's requirements._

| ID | Source | Description | Type | Actor | Action | System response | Priority | Status |
|---|---|---|---|---|---|---|---|---|
| REQ-001 | BRD §2.1 | `<Actor>` can submit a `<record type>` | Behavioral | ROLE-002 | submits | record created in `pending` status | Must | validated |
| REQ-002 | [ASSUMPTION: uniqueness enforced server-side \| BASIS: tier 6 \| IMPACT: duplicate records possible if wrong] | Every `<record type>` has a unique identifier | Data | SYSTEM | validates uniqueness | rejects duplicate with an error | Must | draft |

## Traceability fields
Owns the `REQ-NNN` scheme itself — the first link in
`product-intelligence/traceability.md`'s `REQ → USER → FLOW → SCREEN →
COMPONENT → TEST` chain. Every other template in this folder that cites a
requirement does so by this ID, never by restating its description.

## Explicitly not here
- How requirements are extracted/decomposed →
  `product-intelligence/brd-analysis.md`, `requirement-engine.md`.
- Business rule *content* → `product-intelligence/business-logic.md`.
- The full chain mechanics beyond this one link →
  `product-intelligence/traceability.md`.
