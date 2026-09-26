# Product Type: Healthcare

## Responsibility
Reusable domain knowledge for clinical and health-adjacent products
(patient-facing or provider-facing), including specializations like a dental
practice-management system as a sub-case. Applied on top of the
domain-agnostic core per Rule 14 (`config/operating-rules.md`); contains no
individual company's product details (Rule 15) — product-specific knowledge
belongs in a generated Product Builder under `products/`.

## 1. Common product characteristics
Regulatory sensitivity is the defining trait — **never assume a specific
regulatory regime applies unless the source material states it**; mark it as
an open assumption instead (`config/operating-rules.md` Rule 10). Clinical
workflows are safety-critical: a missed edge case can mean a missed or wrong
clinical action, not just a bad UX moment. Scheduling/appointment logic is
usually more complex than a generic calendar (recurring visits, provider
availability, resource/room constraints, cancellation/no-show policy).

## 2. Common users
Patient, provider/clinician, front-desk/scheduling staff, billing staff,
admin/practice manager.

## 3. Common workflows
Schedule appointment → check-in → clinical encounter → documentation →
billing/claim submission is the canonical cross-role workflow. Recurring-visit
scheduling and cancellation/no-show handling are frequent variants worth
designing explicitly, not as afterthoughts.

## 4. Common information structures
Patient-record-centric IA — most other data (appointments, notes, billing)
hangs off the patient record, rather than being siloed by department or
function.

## 5. Common navigation patterns
Back-behavior and recovery paths need extra rigor given the cost of losing
clinical input mid-entry. Deep navigation into a patient's history should
support a direct jump (search, recents) rather than forcing chronological
drill-down every time.

## 6. Common UI patterns
Calm, high-contrast, low-ornamentation register. Critical values (allergies,
alerts) are always paired with an icon and text, never conveyed by color
alone, regardless of how tempting a simple red badge is.

## 7. Common operational concerns
Appointment/resource (room, chair, equipment) conflict prevention; consent
capture and tracking; clinical documentation completeness before billing
submission.

## 8. Common edge cases
A resource is double-booked; a patient arrives without a confirmed
appointment; a clinical note is left in progress and needs safe, faithful
resumption; an insurance/eligibility check fails after service has already
been rendered.

## 9. Domain-specific terminology
Patient, provider, encounter, chart/clinical note, care plan, claim,
eligibility, consent.

## 10. Domain-specific UX risks
Over-densifying clinical screens to fit more data, degrading legibility of
safety-critical values in the process. Automating away a confirmation step on
a clinically significant action purely for the sake of "fewer clicks."

## 11. Domain-specific accessibility considerations
Alerts (allergies, critical values) must be redundantly signaled (color +
icon + text) and announced to screen readers with priority, not just
visually flagged. Forms used during time-pressured clinical work need
forgiving, low-error-rate input patterns rather than strict, punishing
validation.

## 12. Domain-specific scalability considerations
Patient search/lookup must perform at large-practice or multi-location scale
without ambiguous match risk — never resolve a same-name conflict silently.
Scheduling logic must handle many concurrent providers/rooms without race
conditions in double-booking prevention.

## Sub-case: dental practice management
Adds appointment-chair/operatory resource constraints and treatment-plan/
procedure-code line items on top of the general healthcare knowledge above —
apply both layers together, not as a replacement for the general case.

## Explicitly not here
- The general reasoning technique any point above specializes →
  `product-intelligence/user-roles.md` (users), `business-logic.md`
  (workflows), `ux-engine/information-architecture.md` /
  `navigation-system.md` (structures/navigation), `ui-engine/visual-trends.md`
  (UI register), `ux-engine/accessibility.md` / `ui-engine/color-system.md`
  (accessibility), `product-intelligence/dependency-analysis.md`
  (scalability/dependencies).
- Product-specific knowledge for one actual healthcare product → that
  product's generated Product Builder under `products/`.
