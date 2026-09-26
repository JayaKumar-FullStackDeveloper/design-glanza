# Workflow: Redesign Product

## Responsibility
The Iterate-phase procedure for an **existing** product (brownfield) — how Intake
and Empathize differ when the input is a live/existing application rather than a
requirements document, while the rest of the pipeline (`create-ux.md`,
`create-ui.md`, `build-product.md`, `audit-product.md`) still applies.

## Owns
- Reverse-engineering Intake: how `product-intelligence/brd-analysis.md`'s
  input-type recognition handles an existing app/screenshot set — extracting
  implied requirements, roles, and business logic from observed behavior rather
  than a written spec, and marking everything reconstructed this way with lower
  source-confidence per `brd-analysis.md`'s confidence tagging.
- Baseline-as-prototype rule: per `methodology/prototype.md`, the current product
  *is* the low-fidelity baseline — this workflow skips straight to evaluating it
  against `methodology/test.md` heuristics rather than building a new low-fidelity
  pass from scratch.
- Delta-scoping: identifying which parts of the existing product are in scope for
  redesign vs. carried over unchanged — an explicit boundary decision logged like
  any other assumption if not stated by the user.
- Migration/continuity concerns specific to redesign: preserving user familiarity
  where it isn't actively harmful, and flagging breaking changes to existing flows.

## Classify the redesign before touching anything
Before Delta-scoping (above), classify the request as one of three:
**Extension** (new capability added alongside the existing product, nothing
existing intentionally changes), **Redesign·Preserve** (existing
surfaces are reworked but named behaviors/identifiers must survive
unchanged), or **Redesign·Overhaul** (an explicit, stated intent to replace
existing behavior/structure). This classification is itself an assumption if
not stated by the user (Rule 10) and determines how strictly Protected
Contracts, below, apply.

## Protected Contracts
Independent of delta-scoping's in-scope/carried-over split, name explicitly
which of the following must never change as a side effect of redesign work,
even within in-scope areas, unless the classification above is
Redesign·Overhaul and the change is the stated point of the work: route/URL
slugs and deep-link targets, form field names/API contract shapes, analytics
event names, accessibility wins already in place (a fixed keyboard trap, a
contrast fix), legal/compliance copy, and brand/logo assets. A redesign that
silently breaks one of these has introduced a regression under cover of
"redesign," not delivered one — flag any in-scope change that would touch a
Protected Contract back to the user rather than resolving it silently.

## Scaffolding the Product Builder for a redesign
Two cases, both handled by `scripts/create-product-builder.py`:
- **No product builder exists yet** for the product being redesigned (the
  live app predates Design-Glanza) — run `generate` exactly as
  `create-product.md` does, seeding `purpose`/`domain`/etc. from the
  reverse-engineered facts above, each carrying their lower source-confidence
  tag.
- **A product builder already exists** (this is at least the second pass
  through Iterate on the same product) — always use `--update`, never a bare
  `generate`; the generator's conflict guard exists precisely so a redesign
  pass can't accidentally wipe prior product-specific content instead of
  building on it. Supply only the sections this redesign pass actually
  changed — per delta-scoping above, unchanged sections are left alone rather
  than resupplied.

## Explicitly not here
- The greenfield version of this same pipeline → `create-product.md`.
- The reverse-engineering extraction technique's categories →
  `product-intelligence/brd-analysis.md`.
- A worked example of the no-builder-yet case →
  `use-cases/existing-product.md`.
- A worked example of the builder-already-exists case →
  `use-cases/product-redesign.md`.
- The generator's own scaffolding/validation logic → `scripts/create-product-builder.py`.
