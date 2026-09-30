# Information Architecture

## Responsibility
Organize the product's content and features — and their **screen hierarchy** —
into a coherent structure: grouping, labeling, and depth, built from what
`user-flow-engine.md`'s flows revealed is needed. This is the structure
`navigation-system.md` then exposes as an actual navigation UI, and the
structure `product-types/*.md`'s domain conventions are checked against.

## Grouping/taxonomy technique
Cluster features and content by the user's mental model
(`methodology/empathize.md`'s goals and JTBD dimensions), never by internal
system/database structure. Two entities related in the data model but unrelated
in the user's job-to-be-done belong in different groups; two entities unrelated
in the data model but always used together in the same job belong in the same
group.

## Screen hierarchy and depth
Every node in the hierarchy is a screen or a group of screens, nested to a
depth justified by need, not habit:
- **Depth rule:** a node exists at a given depth only if flattening it (moving
  it up a level) would *increase* cognitive load per
  `user-flow-engine.md`'s optimization criteria — not because "that's how deep
  admin panels usually go." Depth beyond 3 levels needs specific justification;
  reflexively deep nesting is a usability cost, not free organization.
- **Breadth rule:** a level with more than roughly 7–9 siblings is a candidate
  for either sub-grouping (added depth, justified per above) or a
  search/filter mechanism instead of pure browsing (`ux-engine/search-ux.md`
  specifies what that search actually is) — very wide *and* very deep
  simultaneously is the combination most likely to fail discoverability
  (`methodology/test.md` dimension 3).
- **Findability heuristic** (distinct from raw depth): any node a
  frequently-used flow depends on should be reachable in roughly 3 or
  fewer navigational actions (clicks/taps) from that flow's natural entry
  point — a node that technically sits at depth 2 but requires several
  intermediate disambiguation screens to actually reach still fails this,
  and a node at depth 4 reachable via a direct link/shortcut
  (`navigation-system.md` item 5) can still pass it. Depth measures the
  hierarchy's shape; this measures the actual path a user walks.
- Each node is provisionally assigned a `SCREEN-NNN` once `templates/
  screen-architecture.md` formalizes it — this file establishes the node and
  its position in the hierarchy; the screen-level detail is that file's job.

## Labeling convention
Labels use the user's own vocabulary, drawn from
`methodology/empathize.md`'s findings — not internal jargon, not the entity
name from the data model. If the source material's own terms conflict with
plain domain convention (`product-types/*.md`), prefer what the actual users
call it, sourced from Empathize, over what the spec calls it.

## Permission-aware structure
A node's *existence* in the hierarchy — not just its later navigational
visibility — depends on role: if no role can access a section per
`product-intelligence/user-roles.md`'s permission matrix, it isn't part of the
IA at all for those roles' variant of the sitemap. Distinguish this from
`navigation-system.md`'s role-based navigation (item 13 there), which handles
*visibility of an existing, reachable-by-some-roles* node — this file decides
what nodes exist per role-scoped view of the product; that file decides how
each role reaches the nodes that exist for them.

## Cross-module placement
Using `product-intelligence/dependency-analysis.md`'s cross-module dependency
table, decide for every piece of content whether it belongs primarily to one
module (and is merely *referenced* from another) or is genuinely shared. A
node referenced from multiple modules should have one canonical home in the
hierarchy, with cross-module access handled as a navigation affordance
(`navigation-system.md`'s cross-module navigation, item 12) rather than
duplicating the node in multiple places in the IA itself.

## Handoff shape
This file's output fills `templates/sitemap.md` and is the direct input to
`navigation-system.md` (which decides *how* the hierarchy is exposed) and to
`templates/screen-architecture.md` (which decides what's on each resulting
page).

## Loop position
Consumes `user-flow-engine.md`'s flows at the feature-level loop. Re-entered
when a Test discoverability finding (dimension 3) traces to structural
placement rather than visual prominence, per
`methodology/design-thinking.md`'s routing table.

## Explicitly not here
- The sitemap document structure → `templates/sitemap.md`.
- Choosing nav pattern (sidebar vs. tabs vs. breadcrumbs) → `navigation-system.md`.
- Per-screen layout/content detail → `templates/screen-architecture.md`.
- Flow derivation itself → `user-flow-engine.md`.
