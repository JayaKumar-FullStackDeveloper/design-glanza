# Design-Glanza — Project Instructions

This repository hosts **Design-Glanza**, a master Claude Code skill that generates
domain-specific Product Builder skills from raw product requirements. See `README.md`
at the project root for the full pitch.

## What Claude Code should know when working in this repo

- The master skill lives at `.claude/skills/design-glanza/SKILL.md`. Treat it as the
  single source of truth for Design-Glanza's reasoning process — don't duplicate its
  logic elsewhere.
- Generated Product Builder skills never live in this repo — they're written to an
  external local workspace (`~/Design-Glanza-Workspace/products/<slug>/` by default,
  `DESIGN_GLANZA_WORKSPACE_ROOT` override), each a self-contained, domain-specific
  skill (its own SKILL.md and supporting files). `scripts/_common.py` refuses to
  proceed if that path ever resolves inside this repo. Design-Glanza's core logic
  must never be written to assume any one of these domains — the core stays generic;
  domain specifics live only in the external workspace's generated folders.
- Currently only an architecture shell exists. No phase logic (Intake, Empathize,
  Define, Ideate, Architect, Prototype, Implement, Test, Audit, Iterate) has been
  implemented yet — do not assume it's there.

## Working rules

1. **No invented business rules.** When source material (BRD/PRD/SOW/stories/etc.)
   doesn't specify a rule, mark it as an explicit assumption rather than filling the
   gap silently.
2. **Understand before generating UI.** Intake, Empathize, and Define come before any
   visual or code output.
3. **Keep the core domain-agnostic.** Extending Design-Glanza to a new domain should
   only ever mean generating a new skill into the external workspace, never editing
   the core orchestration logic to special-case that domain.
4. **Don't auto-advance phases.** Each phase's output should be reviewable before the
   next phase starts, unless the user explicitly asks for a full end-to-end run.
5. **Stay in sync with generated Product Builders.** If a Product Builder skill's
   structure changes, revisit whether Design-Glanza's generation template needs
   updating to match.
