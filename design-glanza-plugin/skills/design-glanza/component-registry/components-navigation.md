# Registry: Navigation

Tabs, Navigation, Sidebar, Header, Dropdown, Pagination — per
`registry-schema.md`'s 13-field shape. Every value cited is a
`design-tokens/token-schema.md` path, never a raw value.

---

## Tabs
1. **Purpose:** Switch between peer content views within one section
   without leaving it.
2. **When to use:** `navigation-system.md` item 4 — a section has several
   sibling sub-pages at one level.
3. **When NOT to use:** The "tabs" would exceed roughly 6–7 (switch to a
   sub-sidebar/nested list per item 4); the content isn't actually peer
   (a wizard's sequential steps use item 11's stepper, not tabs).
4. **Variants:** underline, pill, boxed treatment (visual only —
   selection behavior is fixed regardless).
5. **States:** default, hover, selected, focus, disabled (a tab whose
   content isn't available yet, e.g. permission-gated).
6. **Interaction behavior:** Arrow-key navigation between tabs, Enter/
   Space activates; selected tab persists across a back-navigation
   (`navigation-system.md` item 6).
7. **Accessibility:** `role=tablist`/`tab`/`tabpanel` semantics; selected
   state conveyed by `aria-selected`, not visual style alone.
8. **Responsive:** Overflow tabs scroll horizontally with a visible
   affordance, never silently clipped, on narrow viewports.
9. **Content rules:** Short, scannable labels; a count badge where the
   underlying list's size is itself useful information.
10. **Validation rules:** Not applicable.
11. **Composition rules:** Commonly wraps a Table or Card grid per tab;
    each tab's content still independently follows its own state rules
    (a tab showing `loading` doesn't block the others).
12. **Common UX mistakes:** More tabs than fit without scrolling and no
    overflow affordance; using tabs for a sequential (not peer) process;
    losing the selected tab on navigation-back.
13. **Domain-specific usage:** No domain-specific variance.

---

## Navigation (primary)
1. **Purpose:** Expose the IA's top-level sections and provide
   wayfinding.
2. **When to use:** Always — every product has exactly one primary
   navigation mechanism (`navigation-system.md` item 3).
3. **When NOT to use:** Never omitted; but never duplicated either — a
   product mixing sidebar and top-nav for the same top-level sections
   has hedged, not decided (item 3's own rule).
4. **Variants:** Sidebar vs. top nav bar, chosen by `navigation-system.md`
   item 2's IA-depth/breadth rule — not a stylistic choice.
5. **States:** default, active-section indication, collapsed (sidebar
   variant, where screen space is prioritized).
6. **Interaction behavior:** Role-based item visibility/order
   (`navigation-system.md` item 13) — a **Deny**-permission item is
   hidden, not disabled, unless deliberately advertising an upgrade path.
7. **Accessibility:** Landmark role (`nav`), current section announced,
   fully keyboard-traversable in visual order.
8. **Responsive:** Collapses to an overlay/drawer pattern at mobile
   (`responsive-system.md`); the wayfinding four-question check
   (`navigation-system.md`) still holds at every breakpoint.
9. **Content rules:** Section labels match the IA's own naming, never a
   marketing rename that diverges from what the section actually is.
10. **Validation rules:** Not applicable.
11. **Composition rules:** Always paired with Header (utility nav) and,
    where the IA is deep, Sidebar's own secondary-nav composition.
12. **Common UX mistakes:** Two competing primary nav mechanisms; nav
    items visible to a role that has no access (should be hidden, not
    shown-then-denied); active-section indication missing or ambiguous.
13. **Domain-specific usage:** Cite the matched `product-types/*.md`
    pack's own navigation-density convention (e.g. ERP/Admin favor dense
    sidebars; consumer-facing surfaces favor minimal top nav).

---

## Sidebar
1. **Purpose:** Persistent secondary/structural navigation alongside
   primary content (a folder tree, a filter rail, a master list).
2. **When to use:** `navigation-system.md` item 2's sidebar threshold
   (>5 top-level sections **and** depth beyond 2 levels), or as the
   Master-detail composition pattern's master pane (`layout-system.md`).
3. **When NOT to use:** A shallow, narrow IA — a top nav bar serves it
   better without wasting screen width on an unearned hierarchy.
4. **Variants:** Fixed-width, collapsible/expandable, resizable.
5. **States:** default, collapsed, item-active, item-hover.
6. **Interaction behavior:** Collapse/expand uses `motion-fast`/`motion-
   base` per `design-system.md`'s motion tokens; collapsed state persists
   across navigation, not reset on every screen load.
7. **Accessibility:** Landmark role, keyboard-traversable, collapse
   control has an accessible name (not icon-only with no label).
8. **Responsive:** Becomes an overlay/drawer below the tablet breakpoint
   (`responsive-system.md`), never squeezed to an unusable narrow column.
9. **Content rules:** Section/item labels match the IA exactly.
10. **Validation rules:** Not applicable.
11. **Composition rules:** The master pane of `layout-system.md`'s
    Master-detail pattern; may itself contain Tabs or a Search input for
    filtering its own list.
12. **Common UX mistakes:** A sidebar used for a shallow, narrow IA where
    a top nav would fit better; collapse state resetting unexpectedly;
    no visual indication of the active item.
13. **Domain-specific usage:** ERP/Admin domains typically default to
    sidebar navigation per their own `product-types/*.md` conventions.

---

## Header
1. **Purpose:** Persistent utility surface — branding, global search,
   notifications, account/settings access.
2. **When to use:** Always, paired with primary Navigation.
3. **When NOT to use:** Never used to carry primary navigation items
   competing with the actual primary nav mechanism.
4. **Variants:** With/without global search, with/without breadcrumb
   trail (per `navigation-system.md` item 7's three-condition rule).
5. **States:** default; notification-badge present/absent.
6. **Interaction behavior:** Utility-nav items (account/notifications/
   settings/help) are grouped and visually separated from primary nav
   per `navigation-system.md` item 1's utility-navigation category.
7. **Accessibility:** Landmark role (`banner`), all interactive elements
   keyboard-reachable in a stable tab order.
8. **Responsive:** Utility items collapse into an overflow menu before
   the primary action space is ever displaced (`responsive-system.md`'s
   priority-preservation rule).
9. **Content rules:** Product/section name reflects actual current
   location, not a static logo-only header with no context.
10. **Validation rules:** Not applicable.
11. **Composition rules:** Frequently composes a Search input (global) and
    a Dropdown (account menu, notifications).
12. **Common UX mistakes:** Utility items mixed into the frequency-
    ranked primary nav list, pushing them out at small breakpoints;
    a breadcrumb shown when item 7's three conditions aren't all met.
13. **Domain-specific usage:** No domain-specific variance.

---

## Dropdown
1. **Purpose:** A transient, dismissible menu of actions or options
   anchored to a trigger control.
2. **When to use:** `navigation-system.md` item 10 — a genuinely
   transient action list (a row's "more actions" menu, an account menu).
3. **When NOT to use:** The content takes real time or can fail (needs a
   `processing`/error state) — that needs a real screen, drawer, or modal,
   never an overlay (item 10's own rule).
4. **Variants:** Action menu, single-select menu (a lighter-weight
   alternative to Select for a small, non-form option set).
5. **States:** default, open, item-hover, item-disabled (permission-
   gated).
6. **Interaction behavior:** Opens/closes on trigger; closes on outside
   click, Escape, or item selection; exit path mirrors entry path
   (`interaction-design.md`'s spatial-consistency rule).
7. **Accessibility:** `role=menu`/`menuitem`; arrow-key navigation,
   Escape closes and returns focus to the trigger.
8. **Responsive:** Repositions to stay on-screen rather than clipping;
   may become a bottom-sheet on mobile.
9. **Content rules:** Destructive items visually and semantically
   separated from ordinary ones (not just adjacent in the same list).
10. **Validation rules:** Not applicable.
11. **Composition rules:** Composes with Header (account/notifications)
    and Table rows (row-level actions).
12. **Common UX mistakes:** A dropdown used for content that can fail or
    take time (should be a modal/drawer instead); focus not returned to
    the trigger on close; a destructive action with no visual separation
    from ordinary ones.
13. **Domain-specific usage:** No domain-specific variance.

---

## Pagination
1. **Purpose:** Navigate a large result set in fixed-size pages.
2. **When to use:** The result set is too large to render/scan at once
   and the total count is knowable.
3. **When NOT to use:** A small, bounded list (paginating 8 items adds
   overhead with no benefit); a feed-like, open-ended list — use
   infinite-scroll/"load more" instead, cited as the same pattern under
   `interaction-design.md`'s Pagination rule.
4. **Variants:** Numbered pages, next/previous only, "load more."
5. **States:** default, loading (affected content region only, never a
   full-page reload), boundary-disabled (previous on page 1, next on
   last page).
6. **Interaction behavior:** `interaction-design.md`'s Pagination section
   in full — fixed filter→sort→paginate order, resets to page 1 on
   filter/search change, current page + total always visible.
7. **Accessibility:** Tab-navigable in reading order; current page
   announced, not just visually highlighted.
8. **Responsive:** Condenses to "Page X of Y" with next/previous only on
   mobile rather than a full numbered control.
9. **Content rules:** States total items/pages, never just "next"/
   "previous" with no sense of scale.
10. **Validation rules:** Not applicable.
11. **Composition rules:** The terminal stage of `composition-
    patterns.md`'s Data Table organism, downstream of Search/Filter/sort.
12. **Common UX mistakes:** Silently showing a stale page number after a
    filter change; a boundary control that's inert instead of visibly
    disabled; a full-page reload feel on page change.
13. **Domain-specific usage:** No domain-specific variance.
