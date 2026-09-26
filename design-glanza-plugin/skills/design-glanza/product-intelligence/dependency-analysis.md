# Dependency Analysis

## Responsibility
Map dependencies (item 7 of `brd-analysis.md`'s checklist), integration
assumptions (item 19), and cross-module dependencies (item 20) so build order and
integration risk can be reasoned about before Implement starts.

## Dependency ID scheme
Every distinct dependency gets a unique ID: **`DEP-NNN`**, sequential.
Requirements (`requirement-engine.md`) cite a dependency by this ID in their
Dependency field when it's external/module-level rather than another `REQ-NNN`.

## Dependency types
Every `DEP-NNN` is classified by type, since each implies a different risk:

- **Data dependency** — this requires data that another requirement/module
  produces (e.g. can't validate a discount code before the promotions module
  defines what a valid code looks like).
- **Sequencing dependency** — this must be built after another, independent of
  data (e.g. auth must exist before any permission-gated feature can be
  meaningfully tested, even if no data is shared).
- **Shared-component dependency** — this relies on a component
  (`ui-engine/component-system.md`) or pattern that must be established first
  (Rule 5, `config/operating-rules.md`: system before screen).
- **External-integration dependency** — this relies on a system outside the
  product's own build (a payment processor, an identity provider, a third-party
  API).

## Cross-module dependencies (item 20)
For every pair of modules/features that interact, produce an explicit
dependency table entry rather than leaving the interaction implicit in
scattered requirements:

| From module | To module | Nature of dependency | DEP-NNN |
|---|---|---|---|
| Billing | Accounts | reads account tier to compute pricing | `DEP-004` |
| Notifications | every module | subscribes to state-change triggers (`business-logic.md` §3) from any module | `DEP-005` |

A module with dependents but no dependencies of its own is a good candidate for
the critical path (build it first); a module depending on many others is a
late-build candidate — this table is what makes that visible instead of
discovered by surprise at Implement.

## Integration assumptions (item 19)
For every external system named or implied in the source, capture — even when
unstated — the assumptions the product design is resting on, each tagged per
`config/output-contract.md`'s assumption format when not explicitly confirmed:
- **Availability/uptime** assumed for this integration.
- **Response format** assumed (schema, encoding).
- **Latency** assumed — does the product's interaction design
  (`ux-engine/interaction-design.md`) account for this integration being slow?
- **Failure mode** assumed — does it fail loudly (error returned) or silently
  (times out, returns stale/cached data)? A product designed only for the
  happy-path response from an integration is missing edge cases that
  `edge-case-engine.md`'s external-dependency-failure category must cover.

An integration assumption left unconfirmed and unflagged is exactly the kind of
backend assumption Rule 10 (`config/operating-rules.md`) is meant to catch —
this file is where integration-specific instances of that rule are enforced.

## Dependency graph and critical-path identification
Construct the full graph from `DEP-NNN` entries plus `REQ-NNN`-to-`REQ-NNN`
dependencies. The critical path is whatever has the most things depending on it
with nothing itself depending on — typically auth/roles
(`user-roles.md`), core entity CRUD, and any shared component
(`ui-engine/component-system.md`) three or more features rely on.

## Risk flagging
A dependency resting on an **Assumed** (not Explicit/Inferred) fact — per the
confidence tags from `brd-analysis.md`/`business-logic.md` — is flagged as
higher-risk build order: if the assumption turns out wrong, everything
downstream of it needs to be revisited, so sequence it early enough that a
wrong assumption is discovered before much is built on top of it, not late
enough that unwinding it is expensive.

## Handoff shape
This file's graph is what `workflows/build-product.md` sequences against
directly, and what `methodology/ideate.md`'s implementation-complexity criterion
(item 7) and constraint-injection step consult when eliminating infeasible
approaches before scoring the rest.

## Loop position
Consumes `dependency-analysis.md`-relevant facts from `brd-analysis.md` and
`business-logic.md`'s triggers at Architect; re-invoked when Ideate reports no
feasible direction fits current constraints (signal: the dependency graph itself
needs revisiting, e.g. a dependency assumed optional turns out mandatory).

## Explicitly not here
- The requirements themselves → `requirement-engine.md`.
- Architecture/module shaping decisions that use this graph → Architect phase,
  orchestrated by `workflows/create-product.md`.
- Build-phase step ordering procedure itself → `workflows/build-product.md`.
- The specific edge-case scenarios an integration failure produces →
  `edge-case-engine.md` (this file flags the assumption; that file enumerates
  the scenario).
