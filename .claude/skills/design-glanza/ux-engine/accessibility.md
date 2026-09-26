# Accessibility (UX)

## Responsibility
Structural and behavioral accessibility: how the interface is navigable and
operable without relying on sight or a mouse. Perceptual accessibility (color
contrast, color-blind-safe palettes) is owned by `ui-engine/color-system.md`;
this file owns structure and interaction, applied concretely to every other
`ux-engine/*` output.

## Focus order rule
Focus order follows the **visual-hierarchy reading order**
(`ui-engine/visual-hierarchy.md`), not raw DOM/insertion order — a screen-reader
or keyboard user should encounter content in the same priority order a sighted
user visually scans it in, even if the underlying markup was authored in a
different order for layout convenience. Worked check: if the primary action is
visually first/most prominent, it must also be focus-reachable early, not
buried after secondary content in tab order.

## Keyboard-operability rule
Every interaction defined in `interaction-design.md` and `form-design.md` has a
keyboard equivalent — this file states the equivalence table those files
implement (see `interaction-design.md`'s gesture/input-modality table for the
concrete mapping). No interaction may ship with a mouse/touch path and no
keyboard path, full stop; this is checked at the same point
`methodology/ideate.md` checks accessibility-by-construction, and again here at
structural design time.

## Semantic / ARIA-role mapping
Map each structural concept to its semantic role so assistive technology
announces it correctly:

| Concept | Semantic mapping |
|---|---|
| Primary/secondary navigation (`navigation-system.md` items 3–4) | `nav` landmark, labeled distinctly if more than one exists on a screen |
| Modal (`navigation-system.md` item 8) | `dialog` role, with a focus trap and a return-focus target on close |
| Drawer (`navigation-system.md` item 9) | `dialog` or `complementary` role depending on whether it interrupts (dialog) or supplements (complementary) |
| Breadcrumbs (`navigation-system.md` item 7, when used) | `nav` with an explicit accessible label (e.g. "breadcrumb"), not a generic list |
| Tabs (`navigation-system.md` item 4) | `tablist` / `tab` / `tabpanel` triad, not a set of unrelated buttons |
| Multi-step workflow (`navigation-system.md` item 11) | progress/step indicator exposed as a status, not decorative-only text |

## Screen-reader flow
Reading order for a screen is derived from `ui-engine/visual-hierarchy.md`'s
emphasis structure without assuming the user can visually scan — every
non-text state indicator (a color-only badge, an icon-only action) must have an
accompanying text/label announced alongside it, mirroring the color-only-
encoding prohibition in `ui-engine/color-system.md` at the structural level.

## Recovery-path accessibility
Every recovery path (`user-flow-engine.md`) must be reachable and announced
non-visually — a `system error` state's retry action
(`state-design.md`) must be keyboard-focusable and identified by an accessible
name, not conveyed only through a visual icon or color change.

## Permission-denied accessibility
A `permission denied` state (`state-design.md`) is communicated with an
explicit accessible reason (e.g. `aria-disabled` plus a descriptive label),
never merely grayed out with no announced explanation — a sighted user infers
meaning from visual disabling; a screen-reader user needs the same meaning
stated directly.

## Zoom and text scaling
Pinch-zoom and browser/OS-level text-resize are never disabled to preserve a
fixed layout — a layout that only holds together at one fixed scale has
pushed a visual-polish preference ahead of a user's actual ability to read
the content, which this file's responsibility explicitly ranks above. Where
reflow at a larger text size would break a layout, that is a
`ui-engine/responsive-system.md` gap to fix, not grounds for locking the
zoom/text-scale level itself.

## Conformance target
The baseline standard (stated once here, at the level the product commits to —
e.g. WCAG AA) applies to every product unless a domain
(`product-types/*.md`) requires a stricter bar, in which case that overlay's
stricter target supersedes this default for that product only.

## WCAG 2.2-specific rules
Concrete, frequently-missed criteria worth stating explicitly rather than
leaving to a generic "meets WCAG AA" target:
- **Focus not obscured.** A focused element must not be hidden behind a
  sticky header, a cookie banner, or another overlay — at minimum partially
  visible (the AA form of this criterion); fully visible is the stricter AAA
  form. Do not treat the AAA wording as the baseline requirement by mistake.
- **Focus appearance.** A visible-focus indicator needs a minimum 2px-
  equivalent perimeter around the focused element with at least 3:1 contrast
  against the adjacent colors — a 1px outline in a similar hue to the
  background does not satisfy this even if "something" is technically
  focused.
- **Dragging movements.** Any drag-based interaction (already required to
  have a non-drag alternative per `interaction-design.md`'s direct-
  manipulation rule) must specifically offer a **single-pointer** alternative
  (e.g. tap-to-select-then-tap-target, not just "use the keyboard") — drag
  can require fine motor control a single-pointer path doesn't.
- **Target size minimum.** 24×24 CSS px minimum for any interactive target,
  with exceptions for inline text links and targets already spaced far enough
  apart that mis-tapping a neighbor is impossible — this is the general web
  minimum; it does not replace platform-specific touch-target minimums
  (iOS ~44pt, Android ~48dp) where a product targets those platforms
  specifically, which are stricter and take precedence there.
- **Consistent help.** Where a help mechanism (chat, contact link, FAQ) is
  available across multiple screens, it appears in the same relative
  navigation position on each rather than moving — inconsistent placement
  itself becomes a discoverability defect.
- **Redundant entry.** Never require a user to re-enter information already
  supplied earlier in the same flow, unless it's a genuine security
  re-verification (e.g. re-entering a password to confirm a destructive
  action) — this sharpens `user-flow-engine.md` criterion 4's existing
  no-re-entry rule with its specific accessibility framing.
- **Accessible authentication.** No step in an authentication or
  re-verification flow may rely on a cognitive-function test alone (solving a
  puzzle, transcribing a distorted image) with no alternative — allow
  password-manager autofill and paste into credential fields rather than
  blocking them.

## High-contrast / forced-colors mode
Distinct from the light/dark theming `color-system.md` already covers: an
OS-level forced-colors or high-contrast mode overrides a product's own color
values with a small, user-chosen palette. Any visual distinction that relies
purely on a background-color or shadow difference (a card's subtle elevation,
a hover-state tint) disappears under forced-colors — verify that meaning
conveyed this way still has a non-color fallback (a visible border, an icon,
text) so the interface stays usable rather than just re-themed.

## Loop position
Applied continuously across the feature-level loop, not as a single pass —
re-checked by `agents/accessibility-expert.md` at every Prototype cycle and
again at Audit. A Test accessibility finding (dimension 6) traces here for
structural causes, or to `ui-engine/color-system.md` for perceptual causes, per
`methodology/design-thinking.md`'s routing table.

## Explicitly not here
- Color contrast ratios and color-blind-safe palette construction →
  `ui-engine/color-system.md`.
- The persona/role that enforces both halves of accessibility during review →
  `agents/accessibility-expert.md`.
- Domain-specific compliance mandates (e.g. healthcare) → the relevant
  `product-types/*.md`.
- The interactions being made accessible → `interaction-design.md`, `form-design.md`.
