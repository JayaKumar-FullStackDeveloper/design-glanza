# Skill Workflow

## The 12-phase lifecycle

```
INTAKE → EMPATHIZE → DEFINE → IDEATE → ARCHITECT → DESIGN SETUP →
PROTOTYPE → IMPLEMENT → PREVIEW & RUN → TEST → AUDIT → ITERATE
```

Five of these are the **core design-thinking loop** (Empathize → Define →
Ideate → Prototype → Test) — real technique, re-entered whenever a Test
finding reveals that an earlier phase's *understanding*, not just its
*execution*, was wrong. The other seven (Intake, Architect, Design Setup,
Implement, Preview & Run, Audit, Iterate) are production-pipeline phases
with no design-thinking counterpart of their own.

| Phase | What happens | Owning agent(s) |
|---|---|---|
| Intake | Recognize input type, run the 20-point extraction checklist | `agents/brd-analyst.md` |
| Empathize | Build an 11-dimension actor model per role | — (methodology only) |
| Define | Converge to 8 falsifiable outputs (problem, objectives, success criteria) | — |
| Ideate | Generate 3+ structurally different approaches, score on evidence | — |
| Architect | Confirm domain (both the 12-pack system and the 122-entry standards registry), sequence dependencies | `agents/product-architect.md` |
| **Design Setup** | Detect/analyze design references, run the design questionnaire, classify Reference-Driven / Guideline-Driven / Custom / Default, produce and get approval on `design-direction.md` | `agents/design-setup-specialist.md` |
| Prototype (UX) | Flows, IA, navigation, screen architecture, interaction/state detail | `agents/ux-architect.md`, `interaction-designer.md` |
| Prototype (UI) | Tokens, components, visual register, responsive rules | `agents/design-system-expert.md`, `ui-designer.md` |
| Implement | Build the already-fully-specified plan into `output/` | — (no dedicated specialist; executes what's already spec'd) |
| **Preview & Run** | Start the local dev server, verify the build, detect the URL/port, check runtime errors, fix issues | — (verification by execution, same posture as Implement) |
| Test | 9 evaluation dimensions, every time — never task completion alone | `agents/qa-expert.md` |
| Audit | Aggregate validators, traceability, drift, accessibility conformance | `agents/qa-expert.md`, `design-system-expert.md`, `accessibility-expert.md` |
| Iterate | Route every finding to its owning phase/file, revalidate only that gate | — |

## The pipeline actions

The concrete, artifact-by-artifact runbook lives in
[`.claude/skills/design-glanza/workflows/execute-product-builder.md`](../.claude/skills/design-glanza/workflows/execute-product-builder.md)
— 37 total table rows (24 map to the originally-specified numbered actions;
13 were added since, marked `-`, including Design Setup's 6 — now including
a Design Research step — Preview & Run's 2, and a mandatory Visual
Benchmark & Audit Cycle action). Execution order follows the engine's
actual dependency chain, not raw numeric order — e.g. flows are built
before the information architecture that consumes them.

## Quality gates

- **Section A** — 12 phase-transition gates (one between every pair of
  adjacent phases above).
- **Section B** — 15 measurable dimensions, **B1–B15**, each with a stated
  pass criterion and a named owner (a script, an agent, or — for Implement
  and Preview & Run — "the executing session," since neither phase involves
  new design reasoning to assign a specialist to).

Full detail: [`.claude/skills/design-glanza/config/quality-gates.md`](../.claude/skills/design-glanza/config/quality-gates.md).

## Scored evaluation

Beyond pass/fail, `evals/evaluation-rubric.md` scores 21 dimensions 1–5,
grouped into three weighted tiers so visual polish is mathematically capped
under 5% of the 235-point total — a flawless design system with weak
requirement understanding or broken traceability cannot score well overall.

## The constitution

20 Operating Rules (`config/operating-rules.md`) apply to every phase, every
domain, every agent — from Rule 1 (Requirement First) through Rule 20
(Design Research & Visual Quality Assurance). Every other file in the skill
cites these by number rather than restating them.
