# Frontend Implementation Technique

## Responsibility
The concrete, stack-specific execution technique `workflows/build-product.md` step 3
("build it into `output/`") applies once a screen/component spec is already
gate-passed. This file never decides *what* to build — that is already
settled by `ui-engine/*`, `component-registry/*`, and
`templates/component-spec.md` before Implement begins — it only closes the
gap between "the spec is correct" and "the first implementation attempt
doesn't trip over a well-known stack-specific pitfall." Used only when the
product's actual chosen stack matches a section below; a product on a
different stack uses none of this file, and `build-product.md`'s generic
step 3 procedure is unaffected.

## Stack detection first
Before applying any section below, confirm the product's actual stack from
its own declared dependencies (`package.json`, an existing `output/*`
config file) — the same "observe, don't assume" posture
`workflows/preview-run.md` step 1 already applies one phase later. Do not
default to React/Tailwind/shadcn because they're common; apply them only
when the product's own architecture decision (Architect, or a Custom
Design/Reference-Driven direction specifying them) actually selected them.

## Tailwind v4 CSS-variable theming
When the stack is Tailwind v4, this exact order is mandatory — skipping or
reordering steps breaks the theme:
1. Define every semantic color token (`ui-engine/color-system.md`'s
   triplets, `design-tokens/*`'s full set) as a CSS variable **at root
   level** (`:root { --primary: hsl(…); }` and `.dark { --primary: hsl(…); }`),
   never inside `@layer base` — v4 strips what isn't inside `@theme`/
   `@layer`, and `:root` must stay at root level to persist.
2. Map every variable through a single `@theme inline` block
   (`--color-primary: var(--primary);`) — without it, Tailwind has no
   knowledge of the variable and `bg-primary`-style utilities are never
   generated. Never nest `@theme` inside `.dark` (v4 doesn't support it);
   one `@theme inline` block maps both modes via the variables' own
   values.
3. Apply base styles referencing the variable directly
   (`background-color: var(--background);`) — never double-wrap
   (`hsl(var(--background))`, which produces `hsl(hsl(...))` since the
   variable already contains the `hsl()` call).
4. Wire a theme provider that toggles the `.dark` class on `<html>` — CSS
   variables update automatically, no `dark:` variant needed on semantic
   color classes.

Use the `@tailwindcss/vite` plugin, never the old PostCSS pipeline; delete
`tailwind.config.ts` entirely (v4 ignores `theme.extend.colors` there) and
set `components.json`'s `"tailwind.config"` to `""`.

**High-frequency gotchas** (each has cost a real build cycle before):
Radix `<SelectItem>` rejects an empty-string `value` — use a sentinel
(`value="__any__"`) and translate it back, never `value=""`; a duplicate
`@layer base` block appears after `shadcn init` runs — merge it into the
product's own single block rather than leaving two; `tailwindcss-animate`
is deprecated under v4 — use `tw-animate-css` instead, or the build fails
on the animation import. Every color pairing this produces still owes
`color-system.md`'s contrast rule, in both themes — this section is
architecture, not a shortcut around that check.

## shadcn/ui component architecture
Only after the theming layer above exists (CSS variables, `cn()` utility,
`components.json`). Install foundation atoms first (button, input, label,
card), then only the feature components the current unit's
`component-spec.md` actually calls for — never the full catalog
speculatively. A component this product doesn't need is dead weight, not
future-proofing.

**Known gotchas, each a real-build failure mode, not theoretical:**
- React Hook Form's `{...field}` spreads a `null` value into `<Input>`,
  which rejects it — bind explicitly
  (`value={field.value ?? ''}`, `onChange`, `onBlur`, `name`, `ref`
  individually) rather than spreading.
- A dynamic icon lookup (`LucideIcons[iconName]`) tree-shakes away in a
  production build — use an explicit `Record<string, LucideIcon>` map.
- `<DialogContent className="max-w-6xl">` is silently overridden by the
  default `sm:max-w-lg` — override at the **same breakpoint prefix**
  (`sm:max-w-6xl`), not an unprefixed class.
- A custom variant (a `brand` button) extends the component's own `cva`
  variants map in `src/components/ui/*`, never a one-off className
  override that drifts from the registry — the same registry-first
  discipline `component-registry/registry-integration.md` already applies
  at the spec level, applied here at the implementation level.
- Every color class on a shadcn primitive is a semantic token
  (`bg-primary`, `bg-card`) — a raw Tailwind color
  (`bg-blue-500`) on one of these components is the implementation-level
  instance of the no-raw-value rule `design-tokens/*` already states at
  the token level.

## React 19 performance and composition — build-time checklist
Applied once a unit is implemented, before it's handed to
`scripts/validate-screens.py`/`validate-states.py` (build-product.md step
3) and again by Design System Expert's drift review during Audit
(`workflows/audit-product.md` step 6):
- **Waterfalls** — sequential `await`s that could run in parallel are the
  single highest-impact defect category; `Promise.all` independent
  fetches, hoist a child's fetch to the nearest common ancestor rather
  than letting parent→child→grandchild each fetch in turn.
- **Composition over boolean-prop explosion** — a component accumulating
  more than ~5 boolean props (`isCompact isClickable showBorder hasIcon`)
  is the implementation-level sign that point 1 (Purpose) of
  `component-system.md`'s 8-point framework was violated; split into
  named variants or compound components instead of one component doing
  several jobs behind flags.
- **Bundle discipline** — a direct import (`from '@/components/ui/button'`)
  instead of a barrel import, an explicit icon map instead of a wildcard
  icon import, and `React.lazy`/`Suspense` for a component not needed on
  initial render.
- **Re-render discipline** — hoist a default object/array prop out of the
  render body (a fresh `[]` reference every render defeats memoization),
  derive filtered/computed state during render (`useMemo`) rather than in
  an effect that re-sets state, and never define a child component inside
  its parent's function body (it remounts every render).
- React 19 API notes worth getting right on the first pass: `ref` is a
  regular prop (no `forwardRef` needed), `use(Context)` replaces
  `useContext` where a conditional/loop call is needed, and
  `<title>`/`<meta>` in component JSX are hoisted to `<head>`
  automatically — no Helmet-equivalent library required.

This checklist is a build-time/audit cross-reference, not a new quality
gate — a finding here routes the same way any other Implement-phase or
Audit-phase finding already does
(`methodology/design-thinking.md`'s routing table).

## Vitest code-level test scaffolding
Distinct from, and complementary to, `methodology/test.md`'s 9-dimension
UX evaluation (Order 37) — that dimension validates the product *works for
its users*; this is ordinary code-level regression testing (does this
function/component/route behave correctly in isolation), run once during
Implement so later iterations don't silently regress something already
proven correct:
1. Detect the project shape from its own `package.json`/config
   (React+Vite → `jsdom` environment + Testing Library; a Node/API layer
   → `node` environment; already has a `vite.config.ts` → add the `test`
   block there rather than a separate config file).
2. Generate `vitest.config.ts` (or extend the existing Vite config),
   `src/test/setup.ts` for React projects
   (`import "@testing-library/jest-dom/vitest";`), and package.json test
   scripts — merged with existing scripts, never overwritten.
3. Write one real test against an actual implemented file for this unit
   (a component's rendered-output assertion, a route's response-shape
   assertion) — never a fabricated placeholder module. The test must
   pass on first run; if it doesn't, fix it before the unit is considered
   implemented.
4. This scaffolding is additive per-unit, not a one-time project setup
   step — each newly-implemented unit with meaningful logic (not a purely
   presentational atom) gets its own test alongside it.

## When none of these stacks apply
A product whose Architect/Design-Setup decisions selected a different
framework, CSS approach, component library, or test runner uses none of
the sections above — `workflows/build-product.md`'s generic step 3
procedure (spec-gated, validated against `validate-screens.py`/
`validate-states.py`) is complete on its own and is never blocked waiting
for a stack-specific technique that doesn't apply.

## Explicitly not here
- What gets built and in what order → `workflows/build-product.md`,
  `agents/product-architect.md`'s dependency graph.
- Component purpose/anatomy/variants/states spec itself →
  `ui-engine/component-system.md`.
- Token values → `design-tokens/*`, `ui-engine/design-system.md`.
- Icon/favicon/image asset generation → `ui-engine/asset-pipeline.md`.
- Real imagery generation (native + API dual-path) →
  `ui-engine/visual-asset-generation.md`.
- The 9-dimension UX validation pass → `methodology/test.md`.
