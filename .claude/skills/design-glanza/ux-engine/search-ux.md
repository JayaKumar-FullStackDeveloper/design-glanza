# Search UX

## Responsibility
The design of search itself — query input, results, and ranking — as a
distinct capability from `information-architecture.md`'s Breadth rule, which
only names search/filter as an *alternative to browsing* when a level gets
too wide, without specifying what that search actually is. Where an IA
decision routes a user to search instead of drilling through a wide
hierarchy, this file is what that search consists of. Distinct from
`interaction-design.md`'s filter→sort→paginate rule, which governs a fixed
result *set* a user is already looking at — this file governs how that set
gets found/narrowed by a query in the first place; the two compose (search
first produces a result set, which filter/sort/paginate then operate on),
they don't duplicate each other.

## Query input
State what's actually searched (titles only, full content, a specific field)
rather than leaving "search" ambiguous — a search box that silently searches
less than the user assumes is a discoverability defect indistinguishable
from a broken search. Where the corpus is large enough that a query can
plausibly match nothing typed so far, offer autocomplete/suggestions once a
minimal number of characters is entered — this reduces the cost of a query
that would otherwise return zero results only after being fully typed and
submitted.

## Zero-results handling
A `state-design.md` `empty` state, not a blank list indistinguishable from
"still loading" or a bug (the same distinction `interaction-design.md`
already requires for a zero-result filter). State plainly that nothing
matched, and where feasible offer a next step (a broadened query suggestion,
a link to browse instead) rather than leaving the user at a dead end —
`user-flow-engine.md`'s recovery-path discipline applied to a null result,
not just to a failure.

## Ranking and relevance
State the ranking principle a result list actually uses (most-recent-first,
best-textual-match, most-frequently-accessed-by-this-role) rather than
leaving order unspecified — an unstated ranking is effectively random from
the user's perspective even if the underlying implementation is
deterministic. Where a business rule affects what a role is even allowed to
see in results (`product-intelligence/user-roles.md`'s permission matrix),
that filtering happens before ranking, not after — a result a role can't
access must not appear and then get removed, which would let its existence
leak information the permission model is supposed to withhold.

## Filter facets
Where results can be narrowed by facets (category, date range, status),
each facet's available options are scoped to what actually exists in the
current result set, not a static full list that includes options yielding
zero results once combined with the current query — a facet offering an
option that would produce nothing is a discoverability trap, not a neutral
default.

## Composing with filter → sort → paginate
A query first produces the working result set; `interaction-design.md`'s
fixed filter → sort → paginate order then applies to that set exactly as
already specified there (changing the query, like changing a filter, resets
pagination back to page 1). Search does not introduce a second, competing
ordering mechanism — a ranked search result list *is* the sort step for that
result set, not an additional stage before or after it.

## Loop position
Entered from `information-architecture.md`'s Breadth rule (a level too wide
for pure browsing) or directly from a Define/Empathize finding that
search-and-retrieve, not browse, is this actor's primary interaction model
(`methodology/ideate.md` item 2's frequency-driven model choice). Re-entered
when a Test discoverability finding (`methodology/test.md` dimension 3)
traces to search's own ranking/query behavior rather than the surrounding
IA/navigation structure.

## Explicitly not here
- Whether search is the right entry mechanism at all for a given IA level →
  `ux-engine/information-architecture.md`'s Breadth rule.
- The fixed filter→sort→paginate order and its pagination/loading behavior →
  `ux-engine/interaction-design.md`.
- The visual layout of a search box or results list → `ui-engine/*`.
- The `empty`/`loading` state definitions themselves → `ux-engine/state-design.md`.
