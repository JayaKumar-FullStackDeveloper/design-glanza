# Evaluation Rubric

## Responsibility
Scored (1-5) assessment criteria for grading a generated artifact's
quality — distinct from `config/quality-gates.md` (binary pass/fail
phase-transition checklist) and `test-cases.md` (concrete pass/fail
benchmark scenarios). This file defines the *scored dimensions* those use,
and is the rubric `config/quality-gates.md`'s **B11 (QA)** gate cites
directly ("rubric score meets or exceeds its stated threshold on every
dimension") — this file is what makes that citation concrete.

## Do not optimize only for visual output
This is an enforced weighting rule, not a sentiment. The 27 dimensions are
grouped into three tiers by weight, and **visual/presentation dimensions
are capped at under 5% of the total possible score** — even a perfect
score on every visual dimension cannot compensate for weak product
reasoning:

| Tier | Weight | Dimensions | Max possible contribution |
|---|---|---|---|
| **A — Product Reasoning** | ×3 | Requirement understanding, Business logic, User-role coverage, Edge cases, Traceability, Self-critique, Iteration quality (7) | 105 pts (~36%) |
| **B — Workflow Completeness** | ×2 | Information architecture, Navigation, User flows, Screen architecture, UX quality, State coverage, Accessibility, Responsive behavior, Implementation readiness, Design direction quality, Preview & run verification, Visual benchmark & audit cycle, Research-to-design traceability, UX scenario coverage, Token inheritance integrity, Component registry conformance, Visual regression integrity, Product memory integrity (18) | 180 pts (~61%) |
| **C — Visual/Presentation** | ×1 | UI system, Component reuse (2) | 10 pts (~3%) |

Total possible: 295 points. A product with a flawless design system and
component library but weak requirement understanding or broken traceability
cannot score well overall — Tier A alone outweighs all of Tier C by more
than 10:1. **Design direction quality, Preview & run verification, Visual
benchmark & audit cycle, Research-to-design traceability, UX scenario
coverage, Token inheritance integrity, Component registry conformance,
Visual regression integrity, and Product memory integrity all sit in Tier
B, not Tier C** — they score whether a direction was actually established
(B13), whether the build actually runs (B14), whether the mandatory
audit-and-refinement cycle actually ran (B15), whether research actually
shaped the design rather than merely documenting it (B16), whether the
product was validated as a complete journey rather than a set of screens
(B17), whether the token set is a valid extension of the master rather
than a fork of it (B18), whether components were actually reused from the
master registry rather than reinvented (B19), whether a later pass
silently regressed an already-confirmed screen (B20), and whether
decisions are actually being remembered and consulted rather than
re-derived or silently contradicted (B21) — never how tasteful or
polished the result looks, which would belong in Tier C and is exactly
the kind of visual-preference scoring this rubric caps. **UI system
(dimension 9, Tier C) scores whether tokens are actually *used* correctly
on screen; Token inheritance integrity (Tier B) scores the token *set's
own structural relationship* to the master — a product can score
perfectly on one while failing the other.** The same distinction holds
between **Component reuse** (dimension 10, Tier C) and **Component
registry conformance** (Tier B), and between **Visual benchmark & audit
cycle** (Tier B — did the mandatory point-in-time check run) and **Visual
regression integrity** (Tier B — did anything silently drift from what
that check already confirmed).

## The 27 dimensions
Each dimension is scored 1-5. Seven of these (marked **new**) extend beyond
`config/quality-gates.md`'s 21 named gates because a genuinely complete
evaluation needs them; the rest map directly to a named gate, cited rather
than restated — including the 22nd through 27th dimensions below, which
map to the new **B16**/**B17**/**B18**/**B19**/**B20**/**B21** gates
rather than being themselves unowned. (A prior pass through this file
corrected a pre-existing "six vs. seven" miscount, and a later pass found
and corrected an independent "Nine vs. seven" miscount, both in this same
sentence — see `config/master-config.md`'s changelog for that history;
not repeated here again.)

| # | Dimension | Tier | Maps to | 1 (fails) | 3 (partial) | 5 (complete) |
|---|---|---|---|---|---|---|
| 1 | Requirement understanding | A | B1 | Requirements missing, vague, or unsourced | Atomic and sourced, but some gaps unflagged | Every requirement atomic, sourced-or-assumption-tagged, fully decomposed |
| 2 | Business logic | A | B2 | Rules absent or invented without tags | Major rules captured, some triggers/success-failure incomplete | Full `BR-NNN` coverage: rules, validation, triggers, status, decisions, workflow, success/failure |
| 3 | User-role coverage | A | **new** | Roles missing or no permission matrix | Roles identified, matrix has gaps, no conditional handling | Full `ROLE-NNN` + matrix + hierarchy/delegation + system actors, fail-closed |
| 4 | Information architecture | B | B4 | No clear hierarchy, orphan nodes | Hierarchy exists, depth/breadth rules not applied | Zero orphans, depth justified, permission-aware structure |
| 5 | Navigation | B | **new** | No pattern rationale, arbitrary choice | Pattern chosen but breadcrumbs/others applied by default | Every pattern selected per rule, breadcrumbs correctly omitted when unjustified |
| 6 | User flows | B | B3 | No flows, or missing recovery paths | Flows exist, some branches/recovery paths incomplete | Full canonical notation, every branch named, every failure has a resolution |
| 7 | Screen architecture | B | B5 | No region maps, competing primary actions | Region maps exist, some screens untraced or ambiguous | Exactly one primary action per screen, every region traces to a flow step |
| 8 | UX quality | B | **new** | Fails multiple `methodology/test.md` dims 2-5 | Usable, but discoverability/feedback gaps | Passes usability/discoverability/error-prevention/feedback cleanly |
| 9 | UI system | C | B6 | No design system, ad hoc values | Tokens exist with undocumented one-offs (drift) | Zero drift, full token coverage, contrast-compliant |
| 10 | Component reuse | C | **new** | Duplicated/near-identical components, no shared base | Some reuse, inconsistent variant modeling | Disciplined reuse-vs-new-variant, zero unjustified proliferation |
| 11 | State coverage | B | B7 | Missing multiple mandatory states | Most states present, some blank cells | Zero blank cells, all 12 states + domain states addressed |
| 12 | Edge cases | A | **new** | Edge cases not enumerated | Enumerated, some failure categories empty | Every failure category has scenarios; cross-role/concurrency addressed |
| 13 | Accessibility | B | B8 | Color-only encoding, no keyboard equivalents | Partial conformance, some interactions inaccessible | Full structural+perceptual conformance, 100% keyboard-operable |
| 14 | Responsive behavior | B | B9 | No responsive rules considered | Breakpoints defined, reflow inconsistent | Every composition pattern has a stated, tested reflow rule per breakpoint |
| 15 | Traceability | A | B10 | Orphaned requirements/artifacts, chain broken | Mostly traceable, some gaps | Full `REQ→USER→FLOW→SCREEN→COMPONENT→TEST` chain, zero orphans |
| 16 | Implementation readiness | B | B12 | Specs incomplete, unresolved circular dependencies | Mostly ready, some specs/dependencies unresolved | B12 fully passes, build order defined, zero blockers |
| 17 | Self-critique | A | **new** (Rule 12) | Declared complete with no audit | Audit run, but only checks task completion/happy path | Full 9-dimension self-critique run and honestly reported, including failures |
| 18 | Iteration quality | A | **new** (Rule 13) | Fixes applied without revalidation, or regress other gates | Fixes revalidate the specific issue, no regression check | Fix + revalidate + explicit regression check, per the loop-termination rule |
| 19 | Design direction quality | B | B13 | No `design-direction.md`, or references treated as business requirements | Document exists but reference classification unstated, or approval silently skipped | Complete per template, classification stated with evidence, approval confirmed or explicitly waived with reason |
| 20 | Preview & run verification | B | B14 | Never launched locally, or a known build/runtime failure carried into Test | Launched, but preview report incomplete or a minor issue undocumented | Build succeeds, runtime clean, local URL/port detected, preview report complete, any issue found was fixed before Test |
| 21 | Visual benchmark & audit cycle | B | B15 | No audit run against any generated screen, or a first-pass finding never re-checked | Audit run, but the three-way comparison skipped or a gap left unclassified | Every A-K category checked, three-way comparison run, every gap classified and refined, re-check recorded — even for a clean first pass |
| 22 | Research-to-design traceability | B | B16 | Research exists only as a document; no Critical/High finding traces to a design decision, or evidence fabricated | Findings recorded and prioritized, but some Critical/High findings uncited in the design, or the Anti-Generic Design challenge skipped | Every Critical/High finding has a cited Design Principle, UX Decision/UI Pattern (or reasoned deferral), and Validation result; every common pattern's Anti-Generic Design challenge recorded |
| 23 | UX scenario coverage | B | B17 | No coverage matrix, or scenarios never walked past the primary path | Matrix exists but some flows have blank/unresolved cells, or the walked checkpoint skipped continuity checks | Every flow's matrix row fully populated across all 8 scenario types; every covered scenario walked with 0 unresolved dead ends, missing screens/transitions/actions/validations/feedback, ambiguous CTAs, or inconsistent patterns |
| 24 | Token inheritance integrity | B | B18 | No `design-tokens.json`, a closed master scale redefined, or values written back into `ui-engine/*` | Token file exists and mostly valid, but an unauthorized top-level key or a missing `$inherits` version | Every path a valid master override, recognized extension, or `product.*` addition; 0 closed-scale redefinitions; `$inherits.masterSkillVersion` present and real |
| 25 | Component registry conformance | B | B19 | Components built from scratch with no registry check; obvious registry matches (Button, Table, Form) reinvented | Some components cite a Registry base, others don't, with no stated reason | Every component cites a Registry base, a stated `composition-patterns.md` instance, or a reasoned "no registry match"; 0 components with none of the three |
| 26 | Visual regression integrity | B | B20 | No baseline captured; a regression found and left unaddressed; an "accepted" diff with no logged reason | Baselines exist but some are stale, or a diff is dismissed without a Baseline Update record | Every screen's baseline current; every Critical/High/Medium diff since last confirmed state either fixed or has an approved, reasoned Baseline Update |
| 27 | Product memory integrity | B | B21 | No Product Memory index; significant decisions never recorded as ADRs; a contradicting decision with no supersession | Index exists but incomplete, or a flagged potential contradiction left unreviewed | Every significant decision has an ADR; every supersession chain valid; every flagged potential contradiction reviewed and resolved |

## Aggregation
Score = Σ(dimension score × tier weight). Report both the total (out of
295) and each tier's subtotal separately — a single blended number hides
exactly the failure mode this rubric exists to prevent (a high visual score
masking weak reasoning). `config/quality-gates.md`'s B11 threshold is
checked **per dimension**, not on the aggregate alone: every dimension must
individually clear its stated minimum (recommended: no dimension below 3,
and zero Tier A dimensions below 4) before B11 passes, regardless of how
high the aggregate is.

## Explicitly not here
- Phase-transition go/no-go checklists → `config/quality-gates.md`.
- Concrete test scenarios these dimensions are scored against →
  `test-cases.md`.
- Score tracking over time/versions → `benchmark-matrix.md`.
