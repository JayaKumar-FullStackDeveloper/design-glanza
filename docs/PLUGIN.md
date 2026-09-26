# Plugin Overview

Design-Glanza exists in three forms — the same content, packaged three ways:

| Form | Location in this repo | Use case |
|---|---|---|
| **Project-local skill** | `.claude/skills/design-glanza/` | Working inside this exact repository |
| **Portable plugin** | `design-glanza-plugin/` | Distributing/testing as a standalone Claude Code plugin, via `--plugin-dir` or a marketplace |
| **Global "skills-dir" install** | *(not part of this repo — installed to your own `~/.claude/skills/design-glanza/`)* | Using Design-Glanza from any project on your machine, without per-project setup |

All three are kept byte-for-byte identical in content (aside from a handful of
deliberate, documented path-resolution differences — see below) — see
[`design-glanza-plugin/README.md`](../design-glanza-plugin/README.md) for the
plugin package's own detailed overview, manifest, and structure.

## What makes the plugin "the same skill"

Every technique file, agent, workflow, template, and script is identical
across all three forms. The **only** intentional differences are:

1. **`SKILL.md`'s invocation phrasing** — the plugin form documents both
   `/design-glanza:design-glanza` (plugin-installed) and `/design-glanza`
   (project-local) as valid entry points; the project-local form only needs
   to document the latter.
2. **`scripts/_common.py`'s path resolution** — the plugin/global forms use
   a `_resolve_project_root()` function that falls back to the current
   working directory (or an explicit `DESIGN_GLANZA_PROJECT_ROOT` override)
   when it isn't running from inside a real project's own `.claude/` folder
   — including correctly excluding the case where it's installed under the
   user's **home** directory's `.claude/skills/` (the global install), which
   has the same folder shape as a real project but isn't one.

## Plugin manifest

```json
{
  "name": "design-glanza",
  "version": "1.2.0",
  "description": "Master product design and Product Builder factory ...",
  "author": { "name": "Design-Glanza" }
}
```

Note the two independent version numbers: the **plugin package version**
(`plugin.json`, currently `1.2.0` — bumped on each packaging sync) and the
**internal skill capability version** (`config/master-config.md`, currently
`1.0.9` — Design-Glanza's own changelog, tracking every rule/gate/phase
addition).

## Keeping the plugin in sync

The plugin folder is a **manually-synced mirror**, not a symlink — every
change to `.claude/skills/design-glanza/` needs an explicit sync pass to
`design-glanza-plugin/skills/design-glanza/` (content copy, plus reapplying
the two documented adaptations above). This has been done through v1.0.9;
see `config/master-config.md`'s changelog for the exact history of what
was synced and when.

For installation instructions for any of the three forms, see
[`INSTALLATION.md`](INSTALLATION.md).
