# Registry Integration

## Responsibility
How the Component Intelligence Registry actually changes UI generation —
registry-first reuse, duplication prevention, mandatory token usage, and
the wiring into the Quality Engine (`config/quality-gates.md`) and UX
Scenario Testing (`ux-scenario-testing/*`) — rather than existing as
reference material nobody is required to consult.

## Master Registry ↔ Product Inventory
The same two-layer model `design-tokens/token-inheritance.md` already
established for tokens, applied to components:

```
MASTER COMPONENT REGISTRY (component-registry/*)  ──inherited by──▶  PRODUCT COMPONENT INVENTORY (product-builder/ui/components.md)
```

A product's `templates/component-spec.md` instance **starts from** a
registry entry (cites it as its "Registry base") and fills in only what's
genuinely product-specific — content/copy, the exact variant subset this
product actually uses, domain-specific detail. The registry entry's
Purpose/When-to-use/When-NOT-to-use/Common-mistakes fields are inherited,
not re-derived per product. Nothing product-specific is ever written back
into `component-registry/*` (Rule 15) — a recurring product-specific need
with no registry match graduates into a new registry entry deliberately
(the same graduation discipline `product-types/custom-domain.md` already
uses for domain packs), never silently absorbed.

## Registry-first reuse (the actual enforcement point)
`agents/design-system-expert.md`'s existing reuse-vs-new decision
(`component-system.md`'s Reuse rule) now runs in two steps, not one:

1. **Check the master registry first.** Does one of the ~29
   `component-registry/components-*.md` entries (or a
   `composition-patterns.md` organism) already cover this need? If yes,
   instantiate it — cite the registry entry, fill in product-specific
   content only.
2. **Check the product's own inventory second**, exactly as before — does
   an existing *product* variant/size/state combination already meet the
   need?

Only when **both** checks come back negative is a genuinely new
component justified — and even then, its Purpose (point 1) must not match
anything already in the registry, per that framework's own point-1 test.
This is what prevents the specific failure mode Rule 24 exists to catch:
inventing a bespoke "data grid" component from scratch when Table already
covers the need, just because the registry wasn't consulted.

## Matching a Figma component (where a Figma Design Context exists)
Where `figma-context.json` (`design-reference-engine/figma-reference.md`)
is present, step 1 above (check the master registry first) runs against
each `components.components[]` entry too: a Figma component is matched
against the ~29 registry entries by name/purpose before anything is
accepted as new, citing the match as `matchedRegistryEntry`
(`figma-context.schema.json`). Rule 24 is unchanged by this — the same
"logged, never silent" treatment already applies to a Figma component with
no genuine registry match, exactly as it already applies to any other new
component. A Figma variant maps onto the matched entry's own Variants
field (point 4, `registry-schema.md`) where the shape fits; a variant with
no registry equivalent is logged the same way an undocumented raw token
value is (`design-tokens/token-audit.md`), never silently dropped.

## Preventing unnecessary duplication
Two distinct duplication risks, both routed through
`agents/design-system-expert.md`'s existing drift review (`component-
system.md` step 4), not a new mechanism:
- **Duplicating a registry entry** — a product invents its own "Button"-
  equivalent instead of instantiating the registry's Button. Caught by
  the registry-first check above.
- **Duplicating within a product** — two product-specific components with
  overlapping Purpose, only one of which cites its registry base
  correctly. Caught by the existing reuse-vs-new drift review, now
  additionally checking each component's stated registry base for
  consistency.

## Enforcing design-token usage
Every registry entry's Variants/States fields are already stated as
token paths (`registry-schema.md`'s conventions section) — a product
instantiating a registry entry inherits that discipline automatically.
`scripts/validate-tokens.py` (`design-tokens/token-audit.md`) still runs
against the product's actual `components.md`/`ui/*.md` content exactly as
before; the registry doesn't add a second token-checking mechanism, it
just means a registry-derived component starts compliant instead of
needing correction.

## Integration with UX Scenario Testing
`ux-scenario-testing/scenario-model.md`'s **UI interactions** field (the
one genuinely new field that binding introduced — which `SCREEN-NNN`/
`COMPONENT-NNN` realizes each scenario step) now resolves against a real,
reasoned registry entry rather than an arbitrary component choice made in
isolation. Concretely: `gap-detection.md`'s "missing action" check (a
Decision branch with no corresponding UI control) is resolved by
consulting the registry for the *right* control, not just *a* control —
e.g. a bulk-approval scenario step resolves to the Data Table
composition's bulk-action Button, not an improvised one-off. A
`continuity-audit.md` **inconsistent interaction pattern** finding (the
same task handled two different ways across screens) is very often
exactly a registry-first violation caught late — this integration is what
lets `agents/design-system-expert.md` catch it *before* Prototype-UI
finishes, not only at Audit.

## Integration with the Quality Engine
- **`config/quality-gates.md`**'s **B6 (Design System)** gains one more
  concrete check: a component with no stated registry base (or an
  explicit, reasoned "no registry match" note) is treated the same as an
  undocumented one-off value — logged, not silent.
- New **B19 (Component Registry Conformance)** measures the master↔product
  relationship itself, mirroring B18's role for tokens: every product
  component either instantiates a registry entry, is a stated composition
  of registry entries (`composition-patterns.md`), or is logged as a
  deliberate new component with a stated reason its Purpose doesn't match
  anything in the registry.
- **`evals/evaluation-rubric.md`** gains a matching Tier B dimension.

## Recording a registry-first decision
A "no registry match — new component" call, or a registry entry
instantiated with a materially product-specific variant, is always
significant per `product-memory/auto-recording.md` — it gets a persisted
`ADR-NNN`, indexed in `product-builder/memory/product-memory.md`, so a
*different* screen's later pass can find the existing decision rather
than independently re-discovering the same gap and possibly resolving it
differently (exactly the contradiction `product-memory/
contradiction-prevention.md` exists to catch).

**Concretely, for a "no registry match" call** (added v1.0.32, closing a
gap a real benchmark run found — the mechanism above was stated but never
shown with an actual record): write one `ADR-NNN` per
`product-memory/adr-schema.md`'s record shape, filled this way for this
specific decision type —

```
ID: ADR-NNN
Context: <what this component needs to do, and for which screen/flow>
Problem: Neither component-registry/* (~29 entries + composition-
  patterns.md organisms) nor this product's own ui/components.md
  inventory has an entry whose Purpose matches this need.
Decision: A new, product-specific component is justified: <component
  name>, specified in ui/components.md (never written back into
  component-registry/*, per Rule 15).
Reason: <why the closest registry entries don't fit — name the entries
  actually checked and what specifically didn't match their Purpose>
Alternatives considered: <each registry entry/composition pattern
  actually checked and rejected, one line each>
Impact: <what depends on this component existing — which screens reuse
  it, so a later pass finds this ADR instead of re-deciding>
Status: accepted
Related: COMPONENT-NNN [, SCREEN-NNN, REQ-NNN]
Recorded: <pass/date, agent: design-system-expert>
```

For a Figma-sourced component specifically
(`figma-context.json.components.components[].matchedRegistryEntry: null`
— `design-reference-engine/figma-reference.md`), the Reason field also
states which Figma component this traces to by name, so the decision
reads as "this Figma component has no Design-Glanza registry equivalent,"
not an unexplained new invention — the same citation discipline
`figma-context-consumption.md` already requires everywhere else a Figma
source informs a decision.

## Preserving existing architecture
No new lifecycle phase, no new agent, no new action row in
`workflows/execute-product-builder.md`'s table — registry consultation
folds into the *existing* "Build component architecture" action
(`component-system.md`'s own step), the same restrained choice
`design-tokens/*` made for token generation. No new ID scheme — a
registry entry is referenced by name (e.g. `button`, `data-table`), not a
sequential ID; a product's own components still use `COMPONENT-NNN`
exactly as `product-intelligence/traceability.md` already defines,
now with an added "Registry base" citation field.

## Explicitly not here
- Any individual registry entry's content → `components-*.md`,
  `composition-patterns.md`.
- The entry schema itself → `registry-schema.md`.
- B19's exact pass criterion → `config/quality-gates.md`.
- Rule 24's full statement → `config/operating-rules.md`.
