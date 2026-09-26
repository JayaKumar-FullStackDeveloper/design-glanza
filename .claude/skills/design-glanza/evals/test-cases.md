# Test Cases

## Responsibility
Concrete test scenarios that check Design-Glanza's own outputs and its own
*decision to act at all* — not the product being designed. ("Given input X,
does the requirement matrix contain Y? Given input Z, does Design-Glanza
correctly decline to engage?") This is internal quality assurance for the
master skill, evaluated against `evaluation-rubric.md`'s 21 dimensions and
tracked over time in `benchmark-matrix.md` — distinct from
`methodology/test.md`, which validates a *product design* against user
needs, not Design-Glanza's own reasoning quality.

## The 10 benchmark scenarios
Scenarios 1-7 reuse the worked examples already validated in `use-cases/*.md`
as their input/expected-behavior basis — this file does not re-describe
them, it names what each one is a **benchmark for** and its specific
pitfall. Scenarios 8-10 are new, format/quality stress tests not tied to one
named domain.

| # | Scenario | Reuses | Primary pitfall this scenario catches |
|---|---|---|---|
| 1 | SaaS | `use-cases/new-saas.md` | Silently inventing structure instead of tagging domain-convention assumptions under sparse input |
| 2 | Admin Panel | `use-cases/admin-panel.md` | Skipping business-logic extraction because the request "sounded like just a CRUD screen" |
| 3 | ERP | `use-cases/erp.md` | Losing cross-module dependency integrity as module count grows |
| 4 | E-commerce | `use-cases/ecommerce.md` | Treating out-of-stock/payment-failure as optional rather than mandatory states |
| 5 | Healthcare | `use-cases/healthcare.md` | Assuming a specific regulatory regime instead of tagging the gap |
| 6 | HRMS | `use-cases/hrms.md` | Modeling permissions at feature level only, missing field-level sensitivity |
| 7 | Existing product | `use-cases/existing-product.md` | Overstating confidence on inferred (not explicit) facts |
| 8 | Ambiguous requirement | new (below) | Silently assuming instead of asking, *or* over-asking indiscriminately |
| 9 | Large BRD | new (below) | Degrading (duplicate IDs, orphaned requirements, dropped sections) at scale |
| 10 | Multi-role enterprise workflow | new (below) | Missing cross-role edge cases and per-role flow branching |

### Scenario 8 — Ambiguous requirement
**Input:** a requirement with no safe default, e.g. *"the system should
notify the right people when something urgent happens."* Neither "right
people" nor "urgent" has a domain-convention answer `product-types/*.md`
can supply — this is not the same as a SaaS input's *sparse-but-fillable*
gaps (scenario 1).

**Expected behavior:** `config/operating-rules.md`'s question-vs-proceed
decision rule correctly classifies this as ask-worthy (cost of guessing
wrong is high, no tier-6+ convention resolves it) — Design-Glanza surfaces
an explicit open question rather than picking a definition of "urgent" and
silently proceeding. **Failure mode A:** silently assumes a definition and
proceeds. **Failure mode B:** asks about *everything* in the input
indiscriminately, including things that did have a safe default — both are
scored against the rubric's Requirement Understanding and Self-Critique
dimensions.

### Scenario 9 — Large BRD
**Input:** a lengthy, multi-section BRD — dozens of requirements, several
roles, many implied edge cases — large enough to stress volume, not just
technique.

**Expected behavior:** `product-intelligence/requirement-engine.md`'s
atomicity and ID-uniqueness hold at scale (no duplicate `REQ-NNN`, no
section silently skipped), `product-intelligence/traceability.md`'s chain
stays intact (no orphaned requirement from a later section that got less
attention than the first), and `scripts/validate-requirements.py` actually
catches any degradation that does occur — this scenario is also a real
stress test of the deterministic tooling itself, not just the reasoning.

### Scenario 10 — Multi-role enterprise workflow
**Input:** a single workflow spanning several roles in sequence, with
delegation and escalation (e.g. a request requiring review by three
different roles in order, one of whom may delegate).

**Expected behavior:** `product-intelligence/user-roles.md`'s hierarchy/
delegation modeling and `edge-case-engine.md`'s cross-role category are both
exercised; `ux-engine/user-flow-engine.md`'s branch-handling-for-role-
variation rule produces genuinely separate `FLOW-NNN` instances per role
rather than one flow with brittle conditional steps; `traceability.md`'s
REQ×USER trace rows correctly show one requirement serving multiple roles
differently.

## Coverage across the 21 evaluation dimensions
Every dimension in `evaluation-rubric.md` is exercised by at least one
scenario above; several are exercised primarily by a specific one. (This
table's header previously undercounted at "19" even before this pass —
corrected now while the file is open for the Visual benchmark & audit
cycle addition, per the same disclosed-fix precedent
`config/master-config.md`'s changelog uses elsewhere.)

| Dimension | Primarily stressed by |
|---|---|
| Requirement understanding | 1, 8, 9 |
| Business logic | 2, 5 |
| User-role coverage | 6, 10 |
| Information architecture | 3, 6 |
| Navigation | 3 |
| User flows | 10 |
| Screen architecture | 4 |
| UX quality | 1, 4 |
| UI system | 4 |
| Component reuse | 2 |
| State coverage | 4 |
| Edge cases | 4, 10 |
| Accessibility | 5, 6 |
| Responsive behavior | 2, 4 |
| Traceability | 7, 9, 10 |
| Implementation readiness | 3, 9 |
| Self-critique | 5, 8 |
| Iteration quality | 6 |
| Design direction quality | 1, 2 |
| Preview & run verification | 3, 9 |
| Visual benchmark & audit cycle | 1, 4 |

## Triggering behavior test cases
Distinct from the 10 scenarios above: these test whether Design-Glanza (or a
generated Product Builder) correctly decides *whether to engage at all*,
not the quality of its output once engaged.

### Should trigger
"Build me a SaaS product for X," "here's our BRD, generate the product
spec," "I need a UX/UI plan for this admin panel," "analyze this existing
app's screenshots and tell me what's missing" — any request carrying
product-definition or product-design intent.

### Should not trigger
"Fix this bug in my script," "what's the capital of France," "refactor this
function for performance," "write a unit test for this existing function" —
general coding/knowledge tasks with no product-definition intent. Also: a
request to change one small, already-scoped visual detail in an established
codebase ("change this button's color") — invoking the full 10-phase
lifecycle for a trivial, already-understood change is a false trigger, not
appropriate thoroughness.

### Should ask for missing critical information
A product definition missing `product_name`/`domain` with no way to infer
either (near-blank input) — `scripts/create-product-builder.py`'s
`validate_definition()` already refuses to generate in this case; the
reasoning layer above it should ask rather than fabricate a name/domain to
get past the check. Also: `product-intelligence/domain-classifier.md`
returning two strong, contradictory domain signals with no way to
disambiguate from the input alone.

### Should use the appropriate product-type pack
Each of scenarios 1-7 above is itself a test that `domain-classifier.md`
routes to its named pack with stated confidence. Scenario 8/9 are good
additional tests of the *opposite* case — weak or absent domain signal
correctly falling through to `product-types/custom-domain.md`'s procedure
rather than being forced into a poor-fit classification.

## Explicitly not here
- The scoring dimensions and their 1-5 anchors → `evaluation-rubric.md`.
- Tracking scores/failures over time and across versions →
  `benchmark-matrix.md`.
- The worked examples themselves → `use-cases/*.md`.
