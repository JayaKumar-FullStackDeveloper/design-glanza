# Component System

## Responsibility
Component taxonomy and anatomy, and the 8-point analysis framework every
component must satisfy before it's considered spec-complete. Behavioral states
(loading/error/empty) are defined in `ux-engine/state-design.md` — this file
owns how each is expressed *visually* per component.

## Atomic-to-composite hierarchy
**Atom** (a button, an icon, an input) → **molecule** (a form field: label +
input + error text) → **organism** (a data table, a full form, a nav bar) —
the naming convention used across every `templates/component-spec.md` entry.
A component's category determines how much it's allowed to vary: atoms have
the tightest, smallest variant sets; organisms are compositions of
already-specified atoms/molecules, not places to introduce new one-off styling.

## The 8-point component analysis framework
Every component in the inventory is specified against all eight points below.
A component missing any point is not yet spec-complete.

### 1. Purpose
The single job this component does. A button triggers an action; it does not
also carry navigation semantics (that's a link, styled differently even if
visually similar) — a component accumulating unrelated responsibilities is a
sign it should split into two.

### 2. Anatomy
Named parts, e.g. a button: `container`, `icon-slot` (optional, leading or
trailing), `label`. Anatomy is what `templates/component-spec.md` enumerates
per component, and what the variants below are allowed to vary.

### 3. Variants
A closed set — never an open-ended "and other styles as needed":
- **Emphasis:** primary / secondary / tertiary / destructive (per
  `visual-hierarchy.md`'s primary/secondary-action rules).
- **Size:** sm / md / lg, using `layout-system.md`'s spacing scale for
  internal padding at each size.

### 4. States
The visual expression of `ux-engine/state-design.md`'s behavioral states, per
component: `default`, `hover`, `focus` (always visually distinct from hover —
focus must remain visible for keyboard users even when hover has no meaning),
`active`, `disabled`, and — where the component can trigger an action —
`loading`. Every variant × state combination is either specified or explicitly
inherited from a base rule; none are left undefined.

### 5. Behavior
Cross-reference, not redefinition: cite the specific
`ux-engine/interaction-design.md` rule that applies to this component type
(e.g. a button's click-feedback timing, per that file's action-feedback
table) rather than restating the behavior rule here.

### 6. Content rules
Concrete text conventions, fixed once and applied everywhere:
- Button labels: verb-led ("Save changes," not "Changes"), sentence case, not
  Title Case.
- Truncation: single-line text truncates with an ellipsis at a defined max
  width; multi-line content (table cells, cards) defines a max line count
  before truncating.
- Empty/zero-content handling: what a component shows when it has nothing to
  display (distinct from `ux-engine/state-design.md`'s `empty` *state* — this
  is the component's own content-level fallback, e.g. a user-avatar
  component's initials fallback when no image exists).

### 7. Accessibility
Cite `ux-engine/accessibility.md`'s semantic mapping table for this
component's role and keyboard behavior rather than restating it; add only
what's specific to this component (e.g. a button's accessible name must match
its visible label, or explain the mismatch if using an icon-only button —
see Iconography below).

### 8. Responsive behavior
Cite `responsive-system.md`'s general reflow rule and state how *this*
component specifically adapts — e.g. a data table (organism) collapses to
stacked cards on mobile per that file's content-reflow rule; a button
(atom) rarely changes shape across breakpoints beyond touch-target sizing.

## Iconography
Icons are a component type in their own right, with the same rigor as any
other atom:
- **Size:** from `design-system.md`'s icon size scale — never an arbitrary
  pixel value.
- **Stroke/fill convention:** pick one style (e.g. 1.5–2px outline stroke) and
  apply it everywhere — never mix filled and outline icon styles within one
  product.
- **Color inheritance:** an icon inherits `currentColor` (the surrounding
  text/label color) by default; it only takes an explicit semantic color
  (`color-system.md`) when it is itself conveying status (a `danger`-colored
  warning icon), not as a decorative choice.
- **Interactive vs. decorative:** an icon-only interactive element (an
  icon-only button) requires an accessible name via a label, not just visual
  recognizability; a decorative icon paired with visible text is hidden from
  assistive tech (`aria-hidden`) so it isn't announced redundantly — this is
  the concrete instance of accessibility point 7 above, applied to icons
  specifically.

## Data visualization
Charts are a component type in their own right, specified against the same
8-point framework — chart-type selection specifically is a function of what
relationship the data has, not visual preference:

| Data shape | Chart type |
|---|---|
| Change over time | Line (continuous trend) or bar (discrete periods) |
| Part-to-whole at one point in time | Stacked bar or a single pie/donut — never a pie for more than ~5–6 slices, a stacked bar reads better past that count |
| Comparison across categories | Bar (horizontal when category labels are long) |
| Correlation between two variables | Scatter |
| Distribution | Histogram or box plot |

A chart's color draws from `color-system.md`'s data-visualization ramps
(sequential/diverging/categorical — matched to the same data-shape logic
above, not chosen independently), and every data-bearing color additionally
carries a non-color channel (direct labels, a legend with pattern/texture, or
hover-revealed values) per the color-blind safety rule. A chart's `empty`
state (`state-design.md`) shows a stated reason ("no data for this period"),
never a blank axis with no data indistinguishable from a loading failure.
Bar and column charts specifically start their value axis at **zero** — a
truncated/non-zero baseline visually exaggerates the difference between
values and is a defect regardless of how much clearer it makes a small
difference look; a line chart's axis may legitimately start elsewhere when
trend shape, not magnitude comparison, is the point, per the data-shape
table above.

## Motion at the component level
Which specific state transitions use `design-system.md`'s motion tokens is
decided here, per component: a modal's enter/exit uses `motion-base`; a
dropdown's open/close uses `motion-fast`; a toast's enter/exit uses
`motion-base`. High-frequency, low-stakes state changes (a checkbox toggle, a
hover color shift) either use `motion-fast` or no transition at all — never a
slower token, which would make frequent interactions feel sluggish rather than
polished.

## Reuse rule
A new screen's need is met by an existing component variant whenever the need
fits within an already-specified variant/size/state combination; a genuinely
new component is justified only when the purpose (point 1) doesn't match
anything in the inventory — checked first against the master
`component-registry/*` (Rule 24, `config/operating-rules.md`), then against
the product's own inventory. `agents/design-system-expert.md` governs this
decision on an ongoing basis, not just at a component's creation.

## Loop position
Consumes `design-system.md`'s tokens and `ux-engine/state-design.md`'s
behavioral states at the feature-level loop. Re-entered when a Test usability
or accessibility finding traces to a specific component's execution, or when
`agents/design-system-expert.md` flags drift, per
`methodology/design-thinking.md`'s routing table.

## Explicitly not here
- Which behavioral states exist and why → `ux-engine/state-design.md`.
- Page-level composition of multiple components → `layout-system.md`.
- The concrete spec document per component → `templates/component-spec.md`.
- Token values (radius, elevation, motion durations, icon sizes) →
  `design-system.md`.
- Pre-populated, professionally-reasoned instances of this framework for
  ~24 common components and their composition patterns →
  `component-registry/*` (this file remains the single source for the
  framework itself; that folder never restates it, only instantiates it).
