# Output Contract

## Responsibility
The universal shape every phase-completion report and generated artifact must
follow, regardless of which phase, agent, or domain produced it. This is the
*meta*-structure ("every output must state X, Y, Z"); concrete per-artifact
fill-in-the-blank structures live in `templates/`.

## Assumption tag (Rule 10)
Every assumption, anywhere it appears — inline in an artifact, in a requirement
row, in a persona field — uses this literal format:

```
[ASSUMPTION: <what was assumed> | BASIS: <why this was the best available guess,
citing the Rule 2 source-of-truth tier used> | IMPACT: <what breaks or changes if
this assumption is wrong>]
```

Rules for its use:
- Never omit `IMPACT` — an assumption without a stated consequence is not a
  complete assumption record.
- The tag is **carried forward**, not resolved-and-dropped: any downstream
  artifact built on an assumption-tagged fact repeats a reference to the same
  tag (e.g. `[SEE ASSUMPTION #A-003]`) rather than presenting the fact as
  confirmed.
- Aggregated in full in `templates/qa-report.md`'s assumption log so a reviewer
  can see every open assumption in one place without hunting through artifacts.

## Severity / priority vocabulary
One shared scale, used consistently everywhere a severity or priority is recorded
(`templates/requirement-matrix.md`, `templates/qa-report.md`,
`evals/evaluation-rubric.md`, `config/quality-gates.md` failures) — no template or
workflow may invent its own scale:

| Level | Meaning | Gate effect |
|---|---|---|
| **Blocker** | Breaks a core user/business outcome, or violates an Operating Rule | Fails the gate; cannot proceed |
| **Major** | Materially degrades correctness, usability, or consistency | Fails the gate unless explicitly waived with a logged reason |
| **Minor** | Noticeable but doesn't undermine the outcome | Logged; does not fail the gate |
| **Note** | Observation, opportunity, or non-binding suggestion | Logged only |

## Phase-completion report shape
Every phase, when it stops (per the no-auto-advance rule in
`operating-rules.md`), reports:
1. **What was produced** — files/artifacts touched or created this phase.
2. **Assumptions made** — new assumption tags introduced this phase, in full.
3. **Open questions** — ambiguities not resolved by an assumption (i.e. judged too
   costly to guess at; see the question-vs-proceed rule in `operating-rules.md`).
4. **Gate status** — pass/fail against this phase's exit gate
   (`config/quality-gates.md`), and if fail, which finding(s) blocked it.
5. **Not proceeding automatically** — an explicit statement that the phase has
   stopped for review, unless an end-to-end run was requested.

## Artifact header shape
Every generated artifact (persona, flow, screen spec, component spec, etc.) opens
with:

```
Source: <requirement ID(s), or "ASSUMPTION" with tag reference>
Owning agent: <agents/*.md file responsible>
Version: <date or version marker>
```

## Self-critique report shape (Rule 12)
Before a feature is declared complete, the self-critique check produces one row
per dimension, using the Rule 12 checklist mapped onto the measurable dimensions
owned by `config/quality-gates.md`:

| Dimension | Status | Findings (if any, with severity) |
|---|---|---|
| Requirements | pass/fail | |
| UX | pass/fail | |
| UI | pass/fail | |
| Accessibility | pass/fail | |
| States | pass/fail | |
| Responsiveness | pass/fail | |
| Edge cases | pass/fail | |

A feature is "complete" only when every row passes or every failing row's findings
are Minor/Note (per the severity vocabulary above) — any Blocker or un-waived
Major keeps the feature open, per Rule 13 (fix and revalidate).

## Explicitly not here
- Per-artifact field lists (e.g. what fields a persona has) → `templates/*.md`.
- Whether an output is *allowed* to proceed and the 21 measurable quality-gate
  dimensions → `quality-gates.md`.
- The rules that generate the content being reported on → `operating-rules.md`.
