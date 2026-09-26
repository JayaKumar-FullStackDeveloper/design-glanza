# UI Design Principles

## Responsibility
A single, practical index of 22 senior-level UI design principles, each
translated into an **actionable rule** rather than a restated slogan.
Most of these principles are already enforced by an existing `ui-engine/*`
or `ux-engine/*` file under a different name — this file's real job is to
name the principle explicitly, point to where it's actually enforced, and
supply the handful of genuinely new rules that had no owner yet. Nothing
here is a new competing system; it's the citable checklist a senior
reviewer would mentally run through, made concrete.

## The 22 principles

### 1. Negative space
Whitespace is priority signal, not decoration — deployed deliberately
around what matters most. **Enforced by:** `visual-hierarchy.md`'s
Whitespace section.

### 2. Simplicity
Every element earns its place; nothing survives because it's merely
possible to include. **Enforced by:** `craft-critique.md`'s deletion test,
`methodology/design-judgment.md`'s strip-away test.

### 3. Visual hierarchy
Size, weight, color, spacing, and position jointly signal importance — one
primary action, capped emphasis levels. **Enforced by:**
`visual-hierarchy.md` in full.

### 4. Progressive disclosure
Show what's needed now; defer the rest behind an explicit, visibly-clickable
affordance. **Enforced by:** `visual-hierarchy.md`'s Progressive disclosure
section.

### 5. Consistency
The same value, component, and pattern is used everywhere the same need
recurs — never a one-off. **Enforced by:** `design-system.md`'s Consistency
rule, `agents/design-system-expert.md`'s drift governance.

### 6. Predictability
A control behaves the same way everywhere it appears, and a pattern already
established elsewhere in the category is followed unless a stated failure
justifies departing from it. **Enforced by:** `design-system.md` (same
component, same behavior, everywhere) and `methodology/design-judgment.md`'s
Convention/familiarity factor (favor an established convention unless a
tested reason says otherwise). A product that behaves differently for the
same action on two different screens has failed this principle regardless
of how good either screen looks alone.

### 7. Recognition over recall
Show the options rather than requiring the user to remember a command,
label, or location from a previous session. Use the user's own vocabulary
(`information-architecture.md`'s labeling convention) rather than internal
jargon, and surface a default/recommended choice rather than an unlabeled
blank field the user must recall the right answer for
(`interaction-design.md`'s Fast decision-making section). A power-user
shortcut is additive, never a replacement for the visible, recognizable
path.

### 8. Clear calls to action
Exactly one primary action per screen, visually dominant, verb-first and
specific in its label. **Enforced by:** `visual-hierarchy.md`'s Primary
action rule, `ux-writing.md`'s CTA wording section.

### 9. Meaningful feedback
Every action gets feedback timed to what it's waiting on, and every error
states what happened, why, and what to do next. **Enforced by:**
`interaction-design.md`'s Action-feedback rules, `ux-writing.md`'s
error-message formula.

### 10. Contextual guidance
Help appears at the point of the decision it clarifies, not in a separate
help center the user has to leave the task to consult — an inline hint,
a field-level description, or a tooltip anchored to the specific control it
explains. Reserve this for genuine ambiguity (a field whose expected format
or consequence isn't obvious from its label); a product covered in tooltips
because every label felt slightly unclear is a content-writing problem
(`ux-writing.md`), not one this principle should paper over.

### 11. Design-system consistency
A screen's tokens, components, and content rules all trace to the governed
system — zero undocumented one-offs. **Enforced by:** `design-system.md`,
`component-system.md`, `agents/design-system-expert.md`.

### 12. Appropriate use of color
Color carries semantic meaning first, decoration second; never the sole
channel for a meaningful distinction. **Enforced by:** `color-system.md`'s
semantic mapping and color-blind safety rule, `craft-critique.md`'s
anti-cliché catalog (the "AI gradient" entry specifically flags color used
with no semantic reason).

### 13. Typography hierarchy
A fixed type scale expresses role and importance, not ad hoc per-screen
sizing. **Enforced by:** `typography.md` in full.

### 14. Grid/layout discipline
Every element aligns to the grid; a fractional-column component is a sign
the grid needs revisiting, not the component. **Enforced by:**
`layout-system.md`'s Grid definition and Alignment rules.

### 15. Information grouping
Related things sit closer together than unrelated things, checked against
all five Gestalt signals, not proximity alone. **Enforced by:**
`visual-hierarchy.md`'s Grouping section.

### 16. Scannability
The layout supports the scan pattern (F or Z) it committed to, at the
density that pattern can actually support. **Enforced by:**
`visual-hierarchy.md`'s Scanning section, `craft-critique.md` check 9
(cognitive load and scanning fit).

### 17. Clear focal points
A viewer can name the primary element in under two seconds. **Enforced by:**
`craft-critique.md` check 1 (hierarchy squint test) and check 2 (hero
subtraction test).

### 18. Reduced cognitive load
Minimize how many decisions and information sources the user must hold in
mind at once, at every step. **Enforced by:** `methodology/ideate.md` item
4, `craft-critique.md` check 9.

### 19. Responsive consistency
Priority content stays reachable and the composition pattern's reflow rule
is defined at every mandatory breakpoint — never an afterthought pass.
**Enforced by:** `responsive-system.md` in full.

### 20. Purposeful motion
Motion states a reason (spatial consistency, state indication, feedback) or
it doesn't ship — never decoration, never on a high-frequency interaction.
**Enforced by:** `interaction-design.md`'s Motion and animation section,
`craft-critique.md`'s anti-cliché catalog (constant ambient motion, generic
entrance animation).

### 21. Appropriate imagery
Photography, illustration, or iconography is chosen to fit the selected
visual register and this product's actual content — never a generic stock
image or an unrelated illustration style bolted on for visual interest.
Illustration-forward treatments are register-scoped (`visual-trends.md`'s
Consumer Playful register names this explicitly; Dense Enterprise and most
Modern SaaS surfaces should default to none-or-minimal). A fabricated or
unrelated image is the same class of defect `craft-critique.md`'s
anti-cliché catalog already names for fabricated metrics/logos — extended
here to imagery specifically.

### 22. Accessibility
Structural and perceptual accessibility apply from the start, never as a
final pass. **Enforced by:** `ux-engine/accessibility.md`,
`ui-engine/color-system.md`, Rule 7.

## How this file is used
Cited from `agents/ui-designer.md`'s and `agents/design-system-expert.md`'s
self-critique steps, and from `ui-engine/ui-audit-framework.md`'s audit
categories — this file supplies the *principle*, those files supply *when
it's checked* and *what specific numeric/structural test operationalizes
it*. Principles 6, 7, 10, and 21 are the only genuinely new rules this file
adds; the rest are named pointers to already-enforced technique, gathered
here so a reviewer has one place to scan the full senior-designer checklist
without hunting across a dozen files.

## Explicitly not here
- The numeric/structural tests that operationalize several of these →
  `ui-engine/craft-critique.md`.
- The structured audit that checks all of these against a finished screen →
  `ui-engine/ui-audit-framework.md`.
- The systematic rules this file cites rather than restates → each named
  `ui-engine/*` / `ux-engine/*` file above.
