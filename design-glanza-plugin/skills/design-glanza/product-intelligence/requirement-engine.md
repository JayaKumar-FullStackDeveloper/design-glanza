# Requirement Engine

## Responsibility
Turn `brd-analysis.md`'s raw extracted facts into atomic, uniquely-identified,
fully-fielded requirements — the structuring layer between raw extraction and the
`templates/requirement-matrix.md` deliverable, and the anchor point every other
product-intelligence file and the traceability chain refers back to.

## Requirement ID scheme
Every requirement gets a unique ID: **`REQ-NNN`**, zero-padded, sequential within
the product (`REQ-001`, `REQ-002`, `REQ-003`, …). For a large product with
clearly separated modules, a module-prefixed variant is allowed —
**`REQ-<MODULE>-NNN`** (e.g. `REQ-BILLING-014`) — chosen once at Architect and
applied consistently; never mix bare and module-prefixed IDs within one product.
IDs are never reused, renumbered, or reassigned after creation, even if a
requirement is later deprecated — a deprecated requirement keeps its ID with
status `deprecated` (see Status field) so historical trace links don't break.

## The requirement field schema
Every `REQ-NNN` carries all of the following. A requirement missing any field
below fails `scripts/validate-requirements.py` and the Requirement Completeness
gate (`config/quality-gates.md`, B1).

| Field | Definition |
|---|---|
| **ID** | `REQ-NNN` per the scheme above. |
| **Source** | Where this came from: a quote/location from the input, or `[ASSUMPTION: ...]` per `config/output-contract.md`'s tag format. Never blank. |
| **Description** | One atomic, independently testable behavior, in plain language. |
| **Actor** | The role (`user-roles.md` `ROLE-NNN`) that initiates this, or `SYSTEM` for a requirement with no human initiator (a scheduled job, an automatic transition, an incoming webhook). |
| **Action** | The verb-level behavior being performed (item 5 of `brd-analysis.md`'s checklist) — "submits," "approves," "exports," "the system auto-cancels." |
| **System response** | What the system does in direct, observable response to the action — not the eventual downstream effect, the *immediate* response. |
| **Business rule** | The specific rule governing this requirement's behavior, cited by ID (`BR-NNN` from `business-logic.md`) rather than restated in prose here. |
| **Validation** | The specific validation condition(s) applied, cited from `business-logic.md`'s validation rules, or stated inline if the requirement *is* the validation rule itself. |
| **Dependency** | Other `REQ-NNN` IDs, or a `DEP-NNN` reference (`dependency-analysis.md`) for an external/module-level dependency. |
| **Priority** | Must / Should / Could / Won't (MoSCoW) — see note below; this is a distinct scale from the Blocker/Major/Minor/Note severity vocabulary in `config/output-contract.md`, which grades defects, not requirement priority. |
| **Status** | `draft` → `validated` → `built` → `tested` → `audited`, or `deprecated`. Moves forward only when the corresponding gate in `config/quality-gates.md` passes for it. |
| **Downstream artifacts** | The forward links of the traceability chain: linked `USER` (role), `FLOW-NNN`, `SCREEN-NNN`, `COMPONENT-NNN`, `TEST-NNN` IDs, per `traceability.md`. Empty until those phases run — never silently omitted from the field once they exist. |

**On Priority using MoSCoW, not the severity scale:** the severity vocabulary in
`config/output-contract.md` (Blocker/Major/Minor/Note) answers "how bad is this
defect"; MoSCoW answers "how important is this requirement to ship." A
Should-have requirement can still produce a Blocker-severity defect if it's
built wrong. Keep the two scales separate — do not substitute one for the other.

Where many Should/Could requirements compete for limited scope and MoSCoW
alone doesn't settle the ranking among them, a structured scoring method
(e.g. RICE — reach/impact/confidence/effort, or Kano's basic/performance/
delighter split) can be applied as an explicit, citable tiebreaker — optional,
and only worth the overhead when the competing set is large enough that an
unstated ranking would otherwise be arbitrary.

## Requirement type
Every requirement is additionally classified by type, which determines which
engine file consumes it downstream:

- **Behavioral** — an actor performs an action, system responds (the default type).
- **Data** — defines an entity/field/type/required-optional-ness (from
  `brd-analysis.md` item 18) rather than an action; feeds data-model decisions
  at Architect and `ux-engine/form-design.md` field requirements.
- **Business-rule** — the requirement *is* a rule (e.g. "orders over $500 require
  manager approval") rather than a described user action; still gets a `REQ-NNN`
  and cites its `BR-NNN` counterpart in `business-logic.md`.
- **Permission** — the requirement *is* an access restriction; cites its
  `ROLE-NNN`/permission-matrix entry in `user-roles.md`.
- **Integration** — the requirement depends on or describes behavior of an
  external system; cites its `DEP-NNN` in `dependency-analysis.md`.
- **Non-functional** — performance, availability, compliance, or other
  cross-cutting quality attribute not tied to one action.

## Atomicity — the decomposition rule
Split any compound statement into independently testable units before assigning
an ID. Example: *"Users can filter and export orders"* is not one requirement —
it decomposes into at minimum:
- `REQ-010` — Actor: Member. Action: filters the order list by a supported
  field. System response: list re-renders to match the filter.
- `REQ-011` — Actor: Member. Action: exports the current (possibly filtered)
  order list. System response: a file is generated and offered for download.

Test: if two clauses of a sentence could pass or fail independently of each
other, they are two requirements, not one.

## Requirement-to-source linkage
Every requirement's Source field is what makes it auditable: a requirement
sourced from an explicit quote is distinct from one inferred from a gap
(`brd-analysis.md`'s gap detection) or one that is a pure assumption. This
linkage is what `traceability.md` chains forward from — a requirement's Source
field is the start of the chain, not an aside.

## Duplicate/conflict detection
Two extracted facts producing contradictory requirements (e.g. one part of a BRD
implies self-service refunds are allowed, another implies all refunds need
manager approval) are **not** silently merged or silently resolved by picking
one. Both are recorded as separate requirements, flagged as conflicting, and
surfaced in the phase-completion report (`config/output-contract.md`) as an open
question — resolution is `methodology/define.md`'s conflict-resolution
technique, not this file's.

## Loop position
Consumes `brd-analysis.md`'s extracted facts (feeding Empathize/Define at the
product-level loop) and is re-invoked at the feature-level loop whenever new
requirements surface mid-cycle (e.g. Ideate reveals a requirement implied by the
chosen approach that wasn't in the original extraction) — new requirements get
the next sequential ID, they never renumber existing ones.

## Explicitly not here
- Raw fact extraction → `brd-analysis.md`.
- Business rule *content* (only cited here by ID) → `business-logic.md`.
- Role/permission *content* (only cited here by ID) → `user-roles.md`.
- Dependency graph *content* (only cited here by ID) → `dependency-analysis.md`.
- The requirement-matrix document layout → `templates/requirement-matrix.md`.
- The full REQ→USER→FLOW→SCREEN→COMPONENT→TEST chain mechanics → `traceability.md`.
