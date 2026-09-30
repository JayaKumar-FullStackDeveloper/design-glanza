# Composition Patterns

## Responsibility
Pre-populated **organism**-level entries (`ui-engine/component-system.md`'s
atomic-to-composite hierarchy) — which registry atoms/molecules combine,
in what fixed order, to form a named, commonly-needed composite. Distinct
from `ui-engine/layout-system.md`'s composition patterns, which compose
whole **screens** from regions (List+detail, Dashboard grid); this file
composes one **component** from other components. The two operate at
different grains and are used together, not as alternatives.

## Data Table
The organism named in the request that motivated this registry: **Search +
Filters + Sorting + Pagination + Selection + Bulk actions + Empty/Loading/
Error states.**

| Part | Registry entry | Fixed composition rule |
|---|---|---|
| Query | Search | Produces the working result set first (`search-ux.md`) |
| Narrowing | Filter | Applies to Search's result set; resets Pagination to page 1 on change |
| Ordering | Table's own sort (column headers) | Applies after Filter, before Pagination — the fixed **filter → sort → paginate** order (`interaction-design.md`), never a different order per table |
| Display | Table | Row density/responsive technique chosen per `responsive-system.md`'s Data table rule |
| Selection | Table's selectable-row variant | Checkbox column; a "select all" control scoped to the *current page* by default, stated explicitly if it instead means the whole filtered set |
| Bulk actions | Button(s), appearing only once ≥1 row is selected | Destructive bulk actions require Confirmation per the risk matrix, scaled to "N records," not a single-record phrasing |
| Empty | Empty State | Filtered-to-zero variant, offering to clear the filter/query |
| Loading | Loading State | Per-region (the row area only), skeleton rows matching the table's own column layout |
| Error | Error State | Region-level, with a stated recovery action (typically retry) |

**Composition-level rule:** every part above is still independently
gate-checked against its own registry entry — composing them into one
organism doesn't waive any individual part's accessibility/responsive/
content requirements. A Data Table missing bulk-action Confirmation, or
whose Filter doesn't reset Pagination, is an incomplete composition even
if every individual atom looks correct in isolation.

**Common composition-level mistakes** (distinct from any one part's own
mistakes list): Search and Filter implemented as two independent,
uncoordinated narrowing mechanisms instead of one composed result set;
bulk actions appearing before any row is selected (dead/disabled buttons
cluttering the toolbar); a "select all" that silently means something
different (current page vs. whole filtered set) than what its label
implies.

## Form
The organism named in the request: **Field hierarchy + Validation +
Helper text + Error handling + Save/cancel behavior.**

| Part | Registry entry | Fixed composition rule |
|---|---|---|
| Field hierarchy | Input/Select/Date Picker/Upload, grouped | `form-design.md`'s Field-grouping rule — by mental model, never database order; each group nameable |
| Sequencing | Single-page vs. multi-step | `form-design.md`'s single-page vs. multi-step decision rule (≥7–9 fields or sequential dependent decisions) |
| Validation | Each field's own Validation rules field | Inline where cheap, on-submit where round-trip-dependent (`form-design.md`) |
| Helper text | Content rules, stated before an error occurs | Format expectations shown proactively, not only after a rejection |
| Error handling | `form-design.md`'s Error-messaging behavior | Adjacent to the field, all simultaneous errors shown at once, clears the moment its condition resolves |
| Save/cancel | Button (primary = save, secondary = cancel) | Cancel with unsaved changes uses the reversible-high-risk cell of the Undo/confirmation matrix (a lightweight inline confirm), never a silent discard |

**Composition-level rule:** every field traces to a Data-type requirement
(`form-design.md`'s Data-requirement linkage) — a Form organism with a
field that doesn't trace to a `REQ-NNN` is scope creep, caught at the
composition level even if each individual Input entry looks correctly
specified.

**Common composition-level mistakes:** fields grouped by database schema
instead of mental model; validation errors aggregated only at the top
with no inline message; a multi-step form with no way back to a completed
step without losing entered data; Cancel silently discarding entered data
with no confirmation on a form that took real effort to fill in.

## Record Detail View
A third, extremely common organism, composing several registry entries
around one specific record — included because it recurs across nearly
every domain pack (`product-types/*.md`) this engine targets:

| Part | Registry entry | Fixed composition rule |
|---|---|---|
| Structure | Header (record name/identity) + Tabs (peer sub-sections: details, activity, related records) | Tabs only where sections are genuinely peer, per that entry's own "when not to use" |
| Primary content | Form (editable) or a read-only field list (view-only) | Editability follows the current role's permission matrix, not a single fixed mode |
| Related data | Table excerpt or Card list (a related-records section) | Cross-module links use `navigation-system.md` item 12, never a dead-end reference |
| Actions | Button(s) for primary record actions, Dropdown for secondary ones | Destructive actions require Confirmation |

**Common composition-level mistakes:** an edit-mode Form shown to a role
with only view permission; a related-records section with no link back
to the related record's own detail view (a dead end).

## Explicitly not here
- Any individual component's own 13 fields → `components-*.md`.
- Page-level (region) composition → `ui-engine/layout-system.md`.
- The registry-first / reuse-before-invent enforcement → `registry-
  integration.md`.
