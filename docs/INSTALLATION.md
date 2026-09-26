# Installation & Usage

## Option 1 — Project-local (this repo)

Already installed. Clone this repository and open it in Claude Code — the
skill at `.claude/skills/design-glanza/` is picked up automatically.

Invoke it with:

```
/design-glanza
```

(explicit invocation only — `disable-model-invocation: true` in `SKILL.md`'s
frontmatter means it never auto-loads from a passing mention of UI/UX/SaaS.)

## Option 2 — Portable plugin, session-scoped (no install)

Test the plugin for a single session directly from a local clone, no
marketplace required:

```bash
claude --plugin-dir ./design-glanza-plugin
```

Validate the manifest first, if you want a standalone check:

```bash
claude plugin validate ./design-glanza-plugin
```

Invoke it as `/design-glanza:design-glanza` (the `<plugin-name>:<skill-name>` form).

## Option 3 — Global install (available from any project)

Uses Claude Code's built-in personal-plugin convention — no marketplace
registration needed. Copy the plugin's skill content, flattened, into your
own global skills directory:

```bash
# from a clone of this repo
mkdir -p ~/.claude/skills/design-glanza
cp -R design-glanza-plugin/skills/design-glanza/. ~/.claude/skills/design-glanza/
mkdir -p ~/.claude/skills/design-glanza/.claude-plugin
cp design-glanza-plugin/.claude-plugin/plugin.json ~/.claude/skills/design-glanza/.claude-plugin/plugin.json
```

Then either restart Claude Code, or run `/reload-plugins` in an active
session. It loads as `design-glanza@skills-dir`.

Validate it once installed:

```bash
claude plugin validate ~/.claude/skills/design-glanza
```

## Requirements

- Claude Code (any recent version supporting skills/plugins)
- Python 3.x on `PATH` (for `scripts/*.py` — standard library only, no `pip install` needed)
- No other runtime dependencies

## First real use

1. Type `/design-glanza` (or the plugin-scoped equivalent).
2. Provide a product requirement — a BRD/PRD/SOW, user stories, an existing
   product's screenshots, or a plain-language idea.
3. Design-Glanza runs Intake → Empathize → Define → Ideate → Architect →
   **Design Setup** → Prototype → Implement → **Preview & Run** → Test →
   Audit → Iterate, stopping for review between phases unless you
   explicitly ask for an end-to-end run.
4. A generated **Product Builder** appears under `products/<your-product-slug>/`.

See [`WORKFLOW.md`](WORKFLOW.md) for exactly what happens at each phase.
