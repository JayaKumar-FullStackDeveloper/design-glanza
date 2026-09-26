# Use Case: HRMS (Greenfield)

## Responsibility
A validated, concrete worked example of Design-Glanza building a greenfield
HRMS product, applying the `product-types/hrms.md` overlay.

## Routes through Design-Glanza — not a separate skill
Executed by the same master skill as every other use case here — only the
applied `product-types/*.md` pack and the specific emphases below differ.

## Input
Usually a described process ("we need leave requests and approval") with an
*implied* organizational structure rarely spelled out in full.

## Classification
Signals: "employee," "org chart," "leave," "payroll," "review cycle" →
`product-types/hrms.md`.

## Analysis
`product-intelligence/user-roles.md` needs finer-grained, **field-level**
permission modeling here — not just per-feature access — because
compensation and review data are sensitive in a way most other domains
aren't; this is `hrms.md`'s named UX risk and is treated as a first-class
requirement, not an afterthought. `business-logic.md`'s trigger-condition
analysis is dedicated real attention for cyclical, time-triggered processes
(payroll runs, review cycles, leave-year resets).

## Required artifacts
Two internally-separated IA branches within **one** builder: an
org-chart-anchored sitemap for HR/admin views, and a flat,
personal-record-anchored sitemap for employee self-service — per
`hrms.md`'s explicit framing, never one hierarchy forced to serve both.

## Design-thinking phases
- **Ideate** weights *learnability* heavily for self-service flows (a
  once-a-year benefits enrollment gets no returning-user familiarity) and
  *efficiency* heavily for HR/admin flows (used constantly) — the same
  criteria set, opposite weighting, within one product.
- **Accessibility Expert**'s pass on the org-chart visualization requires a
  non-visual list/table equivalent providing the same navigation — flagged
  explicitly in `hrms.md`, not discovered late.

## Product Builder generation
`scripts/create-product-builder.py generate`, `product_type: hrms`, domain
naming the specific scope (e.g. "leave management and org structure").

## Implementation
The org-hierarchy data model and the field-level permission engine are
built and tested before any compensation/review feature ships, given the
sensitivity of that data.

## QA
Audit specifically checks mid-cycle reorganization edge cases — an employee
transferred department mid-review-cycle, a manager changed mid-leave-
approval — since `hrms.md` flags these as commonly missed, not rare.

## Completion criteria
Standard nine-dimension coverage, plus an explicit field-level (not merely
feature-level) permission-coverage check as part of the Accessibility/
Requirement gates — a role correctly denied a *feature* but still able to
see a sensitive *field* within it is not complete.

## How this differs from other use cases
Unlike `ecommerce.md`'s storefront/operations split (by process stage),
HRMS's two-branch IA splits by *audience* (self-service vs. HR/admin) — the
same "two registers, one product" pattern, different underlying cause.

## Explicitly not here
- The HRMS domain reference data itself → `product-types/hrms.md`.
- The generic pipeline being demonstrated → `workflows/create-product.md`.
