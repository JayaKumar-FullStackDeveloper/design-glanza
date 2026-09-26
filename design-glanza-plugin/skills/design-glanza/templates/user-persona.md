# Template: User Persona

## Purpose
The document form of one actor's Empathy Model — a reference other artifacts
consult to check a decision against a real, sourced user rather than an
imagined one. Reusable across every domain: it holds behavioral/contextual
fields only, never a domain-specific role list (that's
`product-intelligence/user-roles.md`'s job for this product, or
`product-types/*.md`'s job for what's typical in a domain).

## Required inputs
- A `ROLE-NNN` from `product-intelligence/user-roles.md` this persona
  represents.
- `methodology/empathize.md`'s 11-dimension analysis for that role.

## Output structure
- **Header** — per `config/output-contract.md`.
- **Role/title** — the `ROLE-NNN` cross-reference.
- **Primary job-to-be-done** — in the "When `<situation>`, I want to
  `<motivation>`, so I can `<outcome>`" form.
- **Goals and motivations** — stated (from source) vs. underlying (from
  goal-laddering), kept distinct.
- **Pain points** — stated vs. inferred, each tagged.
- **Context of use** — device, environment, frequency of use (Empathize
  dimensions 6-8).
- **Constraints and decision-making** — the user-side limits and authority
  (Empathize dimensions 9-10).
- **Relationship to other personas** — who they depend on, who depends on
  them.

## Quality criteria
- Every field is sourced or assumption-tagged — a persona built entirely
  from inference without a single explicit source is a signal Empathize
  didn't have enough input, not a finished persona.
- The JTBD statement names a situation and an outcome, not a feature ("wants
  a dashboard" is not a JTBD; "wants to know at a glance whether anything
  needs their attention today" is).
- Stated vs. inferred vs. assumed content is visibly distinguished, not
  merged into one undifferentiated paragraph.
- Traces to a real `ROLE-NNN` — a persona with no corresponding role entry
  in `user-roles.md` is an orphan, the same defect class
  `product-intelligence/traceability.md` flags for any other artifact.

## Example structure
_Illustrative only — placeholders, not a real user._

```
Role: ROLE-002 (<role name>)
JTBD: When <situation>, I want to <motivation>, so I can <outcome>.
Goals:        stated - <goal from source>; underlying - <goal from laddering>
Pain points:  stated - <named friction>; inferred - <implied by a workaround>
Context:      device <x>, environment <y>, frequency <daily/weekly/rare>
Constraints:  <time pressure / authority limit>
Relationship: depends on ROLE-001 for <x>; ROLE-003 depends on this role for <y>
```

## Traceability fields
Cites `ROLE-NNN` (`product-intelligence/user-roles.md`); optionally cites the
`REQ-NNN`(s) whose Actor field this persona justifies.

## Explicitly not here
- Jobs-to-be-done derivation technique → `methodology/empathize.md`.
- Formal role/permission modeling → `product-intelligence/user-roles.md`.
- Domain-typical role sets → the relevant `product-types/*.md`.
