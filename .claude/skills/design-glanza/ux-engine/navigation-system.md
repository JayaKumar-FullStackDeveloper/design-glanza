# Navigation System

## Responsibility
Select and specify the concrete navigation mechanism that exposes
`information-architecture.md`'s hierarchy. Every pattern below is chosen by a
stated rule tied to the IA's actual shape — never applied by default or by
convention. **Breadcrumbs, in particular, are never imposed universally** — see
item 7.

## Selection framework
Before picking any pattern, characterize the IA from `information-architecture.md`:
depth (how many levels), breadth (siblings per level), and shape (strict tree
vs. a graph where a node has multiple valid parents vs. flat/dashboard-centric).
Every pattern choice below is a function of these three properties, not a
default.

## 1. Module entry
How a user first arrives at a module is chosen by that module's **frequency of
use** (`methodology/empathize.md` dimension 7) and **role relevance**
(`product-intelligence/user-roles.md`): a module most roles use often gets a
prominent top-level entry (primary nav item or a dashboard tile); a module used
rarely or by one role only gets a secondary entry (nested under a parent
section, or reached only via a deep link from where it's relevant) rather than
competing for primary nav space it doesn't earn.

Within primary navigation specifically, account/notifications/settings/help
are a distinct **utility navigation** category, not ordinary top-level
entries competing on frequency: they're high-reach (nearly every user needs
them eventually) but low-frequency-per-visit, so they're placed in a
consistent, visually separated location (commonly a corner or a persistent
header/footer zone) rather than mixed into the frequency-ranked primary list,
where their low visit-frequency would otherwise push them out.

Where the order among several equally-important peer items is otherwise
arbitrary (no frequency or role signal breaks the tie), place the
highest-priority items **first or last, never buried mid-list** — first/last
positions are recalled and scanned more reliably than the middle of a list,
independent of any other design choice.

## 2. Sidebar navigation
Use a persistent sidebar when the IA has **both** more than roughly 5 top-level
sections **and** depth beyond 2 levels. A shallow or narrow IA (few sections,
≤2 levels) is better served by a top nav bar (item 3) — a sidebar for a
3-section product wastes screen space communicating a hierarchy that isn't
there.

## 3. Primary navigation
The single top-level wayfinding mechanism — whichever of sidebar or top nav bar
item 2's rule selects — exposing the IA's top-level sections. Only one primary
navigation mechanism exists per product; a product mixing a sidebar *and* an
equally-weighted top nav for the same top-level sections has not made a
decision, it has hedged one — pick one per the rule above.

## 4. Secondary navigation
Sub-navigation within a section (tabs, a sub-sidebar, in-page anchor nav),
chosen by that section's *own* internal depth/breadth using the same logic as
item 2, applied one level down: a section with several sibling sub-pages at one
level uses tabs; a section with its own multi-level sub-hierarchy uses a
sub-sidebar or nested list, not tabs stretched to cover more than they should.

## 5. Deep navigation
A node 3+ levels deep must be reachable without drilling through every
intermediate level on every visit — provide a direct link, a search result, or
a "recently visited" shortcut. Reaching a deep node only by repeatedly
navigating through its full ancestor chain violates the minimal-user-effort
criterion (`user-flow-engine.md`) for anything used more than once.

## 6. Back behavior
Define what "back" means in-product, distinct from the browser's back button:
back returns to the last *meaningful* state, not merely the last literal
navigation history entry — e.g. back from a multi-step workflow's step 3
returns to step 2 with entered data intact, not out of the workflow entirely;
back from a modal returns to the exact scroll position and state of what was
behind it. Back is one of the mechanisms a recovery path
(`user-flow-engine.md`) can use to return a user to a known-good state.

## 7. Breadcrumbs — when appropriate, never universal
Breadcrumbs are used **only when all three** are true:
- IA depth is **3 or more levels** at the point breadcrumbs would appear (below
  3 levels, "back" (item 6) already covers the need — a breadcrumb trail one or
  two crumbs long adds visual noise without adding navigational value).
- The user plausibly needs to **jump to a specific ancestor level**, not just
  step back one level (a genuine need distinct from item 6).
- The hierarchy at that point is a **strict tree** — a node with exactly one
  parent path. Where the IA is a graph (a node reachable via more than one
  valid parent, or a flat/dashboard-centric structure with no consistent
  ancestor chain), a breadcrumb trail is ambiguous or misleading and must not
  be shown.

Where these conditions aren't met, omit breadcrumbs — this is a stated decision
recorded in the screen's architecture (`templates/screen-architecture.md`), not
a default that happens to be absent.

## 8. Modal behavior
Use a modal for a short, focused, interrupting task with small scope that
doesn't warrant leaving the current context (a confirmation, a quick create-one-
thing form). Do not use a modal for a multi-step workflow (item 11 handles
that separately) or for anything requiring its own deep navigation — a modal
that itself needs a nav pattern is a sign the task has outgrown "modal."

## 9. Drawers
Use a slide-in side panel when the task benefits from keeping the originating
context visible alongside it — viewing or editing a record's detail while the
list behind it stays in view. This is the structural difference from a modal:
a drawer preserves context, a modal fully interrupts it. Choose a drawer when
the user is likely to reference the list/context while acting on the detail;
choose a modal when they aren't.

## 10. Overlays
The umbrella term for transient, dismissible layers — tooltips, popovers,
dropdown menus, toasts. Reserve overlays for genuinely transient
information/actions; never route anything requiring a `state-design.md`
"processing" state (something that takes real time or can fail) through an
overlay — that needs a real screen, drawer, or modal that can hold a loading
or error state properly.

## 11. Multi-step workflows
Use a dedicated stepper/progress indicator showing current position out of the
total, with explicit back-navigation between *already-completed* steps that
preserves entered data — never silently discard input by navigating back.
Whether back-navigation is allowed at all past a given step is a
`product-intelligence/business-logic.md` business-rule question (some
workflows, once a step is committed, cannot be un-stepped) — state that
constraint explicitly rather than assuming free movement.

**Resuming an interrupted workflow** (the user leaves and returns later):
the return point names the specific uncompleted state ("Resume: Step 3 of
5 — Payment details"), not a generic "Welcome back" with no reference to
where they left off. Where more than one workflow is left incomplete at
once, surface only the 1–2 most relevant open ones prominently (e.g. the
most recent, or the one closest to completion) rather than an
undifferentiated list of every unfinished thing — too many surfaced open
loops at once reads as clutter/guilt rather than a helpful nudge back in.

## 12. Cross-module navigation
Using `product-intelligence/dependency-analysis.md`'s `DEP-NNN` cross-module
table, provide an explicit in-context link/action where a user legitimately
needs to move from one module's screen to a related entity in another module
(e.g. from an Order screen to its Customer record) — never force a return to
primary navigation and a fresh drill-down to reach something directly related
to what's already on screen.

## 13. Role-based navigation
Nav item visibility and order is filtered by the current role's permission
matrix (`product-intelligence/user-roles.md`): an item the role has **Deny**
on is hidden entirely, not shown disabled — unless deliberately advertising a
permission-gated upgrade path is an explicit, stated product decision (e.g. a
visible-but-locked premium feature), never a silent default. An item the role
has **Conditional** access to is shown with that condition's context applied
(e.g. "Approve" only appears on records actually eligible for this role to
approve).

## Wayfinding aids
Active-state indication (what's currently selected/open) and section
landmarks are present regardless of which primary pattern is chosen — these
are not optional polish, they're what makes "where am I" answerable at a
glance, feeding `methodology/test.md` dimension 3 (discoverability) and
dimension 8 (operational clarity, `user-flow-engine.md`).

A concrete check for whether wayfinding is actually complete on a given
screen: a user should be able to answer, without hesitation, **where am I,
where can I go from here, what's on this screen, and how do I get out** (back
out of a modal/drawer/workflow to a known state, per item 6). Any pattern
chosen above that leaves one of these four unanswerable — the most common
failure being "how do I get out" inside a multi-step workflow or nested
drawer — is incomplete regardless of how visually polished it is.

## Loop position
Consumes `information-architecture.md`'s hierarchy at the feature-level loop.
Re-entered when a Test discoverability or operational-clarity finding traces to
the navigation mechanism itself rather than the underlying IA structure, per
`methodology/design-thinking.md`'s routing table.

## Explicitly not here
- The IA hierarchy itself → `information-architecture.md`.
- Visual styling of nav components (color, spacing, iconography) →
  `ui-engine/component-system.md` and `ui-engine/visual-hierarchy.md`.
- Keyboard/focus-order behavior of nav → `accessibility.md`.
- The permission matrix content itself → `product-intelligence/user-roles.md`.
