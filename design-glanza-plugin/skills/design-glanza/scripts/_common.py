"""
_common.py

Shared, deterministic infrastructure for Design-Glanza's validation scripts:
path resolution, ID-scheme regexes (per product-intelligence/traceability.md),
the mandatory-state list (per Rule 6, config/operating-rules.md), the shared
Finding type (per config/output-contract.md's severity vocabulary), and a
loader for importing a sibling script whose filename isn't a valid Python
identifier (every script in this folder is hyphenated).

Not a validator itself, and not run directly. Imported by
create-product-builder.py, validate-requirements.py, validate-screens.py,
validate-states.py, validate-product.py, and generate-report.py so these
facts are defined exactly once.

Everything here is structural/mechanical (paths, regexes, dataclasses) —
no reasoning, no judgment calls. That boundary is deliberate: see each
validator script's own docstring for what it does and does not check.
"""

from __future__ import annotations

import importlib.util
import os
import re
import sys
from dataclasses import dataclass
from pathlib import Path

# A generated screen's own text (an arrow "→", an em dash, a checkmark) can
# end up in a Finding's message (e.g. quoting an element's rendered text
# excerpt). On Windows, a script's stdout/stderr default to the console's
# legacy code page (cp1252) rather than UTF-8, so printing such a Finding
# crashes with UnicodeEncodeError before the user ever sees the result —
# the validator failing on its own output, not on anything it validated.
# Every script that imports this module gets the safe behavior for free;
# `errors="replace"` degrades an unencodable character to "?" rather than
# crashing, which is the right tradeoff for a diagnostic message.
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass  # a redirected/non-standard stream without reconfigure() — leave it alone

# ---------------------------------------------------------------------------
# Path resolution — supports two deployment modes, since this skill can be
# either project-local (`<root>/.claude/skills/design-glanza/`) or a
# distributable plugin (`<plugin-root>/skills/design-glanza/`, installed
# wherever Claude Code's plugin system puts it — a cache dir, a cloned
# marketplace repo, anywhere unrelated to the host project). Walking a fixed
# number of parent directories from `__file__` only works for the first
# mode; for a plugin, the install path has no relationship to the host
# project the user is actually working in, so PROJECT_ROOT falls back to an
# explicit override or the current working directory instead.
# ---------------------------------------------------------------------------

SCRIPT_DIR = Path(__file__).resolve().parent          # .../design-glanza/scripts
SKILL_ROOT = SCRIPT_DIR.parent                         # .../design-glanza


def _resolve_project_root(skill_root: Path) -> Path:
    # Project-local layout is <root>/.claude/skills/design-glanza — that's
    # two levels up from skill_root (skills/, then .claude/), not one.
    claude_dir = skill_root.parent.parent
    if (
        claude_dir.name == ".claude"
        and claude_dir.parent.is_dir()
        and claude_dir.parent != Path.home()
    ):
        # Project-local layout: the project root is unambiguous, walk
        # straight to it. The home-directory exclusion matters because the
        # user's global `~/.claude/skills/<name>/` ("skills-dir" install,
        # `claude plugin init`'s own convention for a personal plugin) has
        # this exact same shape — but there, the directory containing
        # `.claude` is the user's home, not a project; that install has no
        # more fixed relationship to whatever project the user is actually
        # working in than a marketplace-installed plugin does, so it must
        # fall through to the override/cwd path below, not treat home as
        # the project root.
        return claude_dir.parent
    # Plugin (or any other) layout: no fixed relationship to the host
    # project. Prefer an explicit override; otherwise assume Claude Code
    # invoked this script with cwd already set to the project being worked
    # on, which is the only reliable signal available at that point.
    override = os.environ.get("DESIGN_GLANZA_PROJECT_ROOT")
    if override:
        return Path(override).resolve()
    return Path.cwd()


PROJECT_ROOT = _resolve_project_root(SKILL_ROOT)       # host project root — see _resolve_project_root
DEFAULT_WORKSPACE_ROOT = Path.home() / "Design-Glanza-Workspace"
_workspace_override = os.environ.get("DESIGN_GLANZA_WORKSPACE_ROOT", "").strip()
WORKSPACE_ROOT = Path(_workspace_override).resolve() if _workspace_override else DEFAULT_WORKSPACE_ROOT.resolve()
PRODUCTS_DIR = WORKSPACE_ROOT / "products"


def _assert_workspace_outside_repo(workspace_root: Path, repo_root: Path) -> None:
    """Mandatory safety check: generated products must never land inside
    this skill's own repository, regardless of how WORKSPACE_ROOT resolved."""
    try:
        workspace_root.relative_to(repo_root.resolve())
    except ValueError:
        return  # outside the repo — safe
    raise RuntimeError(
        f"Refusing to proceed: the resolved workspace ({workspace_root}) is "
        f"inside the Design-Glanza repository ({repo_root}). Generated "
        f"products/screens/BRDs/UX/UI/design systems/prototypes/implementation "
        f"artifacts must live outside this repo. Set DESIGN_GLANZA_WORKSPACE_ROOT "
        f"to a path outside it, or unset it to use the default "
        f"({DEFAULT_WORKSPACE_ROOT})."
    )


_assert_workspace_outside_repo(WORKSPACE_ROOT, PROJECT_ROOT)
PRODUCT_TYPES_DIR = SKILL_ROOT / "product-types"
MASTER_CONFIG_PATH = SKILL_ROOT / "config" / "master-config.md"

TOP_LEVEL_DIRS = ["BRD", "product-builder", "output"]
BUILDER_SUBDIRS = ["product", "requirements", "ux", "ui", "domain", "research", "workflows", "qa", "memory"]

PRODUCT_JSON_FIELDS = [
    "product_name", "product_slug", "product_type", "domain", "sub_domain",
    "platform", "builder_version", "master_skill_version", "methodology",
    "status",
]

# The 13 mandatory states, per Rule 6 (config/operating-rules.md) and
# ux-engine/state-design.md. Matched case-insensitively, loosely (substring),
# since authored markdown headers vary in exact punctuation/casing.
MANDATORY_STATES = [
    "initial", "loading", "success", "empty", "validation error",
    "system error", "permission denied", "processing", "completed",
    "cancelled", "conflict", "timeout", "offline",
]

# ID schemes, per product-intelligence/traceability.md and the files that
# own each one. RF (Research Finding, design-research/research-to-design.md),
# SCENARIO (ux-scenario-testing/scenario-model.md), and ADR (persisted
# decision record, product-memory/adr-schema.md) are sideways references
# like BR/DEP/EDGE, not chain links — see traceability.md's "Sideways
# references vs. the chain" section. RF and SCENARIO have no validator
# script cross-checking their referential integrity yet (a disclosed
# limitation, see design-research/README.md and ux-scenario-testing/
# README.md) — ADR is the first of the three to get one,
# scripts/validate-memory.py.
ID_SCHEMES = ["REQ", "ROLE", "BR", "DEP", "EDGE", "RF", "SCENARIO", "ADR", "FLOW", "SCREEN", "COMPONENT", "TEST"]
ID_PATTERNS = {scheme: re.compile(rf"\b{scheme}-\d+\b") for scheme in ID_SCHEMES}

SEVERITIES = ("Blocker", "Major", "Minor", "Note")  # config/output-contract.md


@dataclass
class Finding:
    """One validation finding. Severity follows config/output-contract.md's
    shared vocabulary exactly so scripts and agents produce comparable
    findings."""
    severity: str
    message: str
    file: str = ""
    check: str = ""

    def __str__(self) -> str:
        loc = f" ({self.file})" if self.file else ""
        return f"[{self.severity}] {self.message}{loc}"


# WCAG 2.x contrast math, per ui-engine/color-system.md's Contrast
# compliance rule. Defined once here (not in validate-tokens.py, where it
# originated) so scripts/validate-generated-artifact.py's generated-CSS
# contrast scan (B14) uses the exact same arithmetic as
# validate-tokens.py's design-tokens.json contrast check (B8/B6) — one
# implementation, never two independently-written WCAG formulas that could
# silently drift apart.
CONTRAST_MIN_NORMAL = 4.5
CONTRAST_MIN_LARGE = 3.0


def hex_to_rgb(hex_str):
    """Parse a #rgb/#rrggbb string into an (r, g, b) 0-255 tuple, or None if
    it isn't a parseable hex color (e.g. a var()/token reference left
    unresolved) — contrast checks only run against literal hex values."""
    if not isinstance(hex_str, str):
        return None
    h = hex_str.strip().lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    if len(h) != 6 or not re.fullmatch(r"[0-9a-fA-F]{6}", h):
        return None
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def relative_luminance(rgb):
    def chan(c):
        c = c / 255.0
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (chan(c) for c in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast_ratio(hex_a, hex_b):
    """WCAG contrast ratio between two hex colors, or None if either isn't a
    parseable literal hex value."""
    rgb_a, rgb_b = hex_to_rgb(hex_a), hex_to_rgb(hex_b)
    if rgb_a is None or rgb_b is None:
        return None
    la, lb = relative_luminance(rgb_a), relative_luminance(rgb_b)
    lighter, darker = max(la, lb), min(la, lb)
    return (lighter + 0.05) / (darker + 0.05)


def discover_product_types() -> list[str]:
    if not PRODUCT_TYPES_DIR.is_dir():
        return []
    return sorted(p.stem for p in PRODUCT_TYPES_DIR.glob("*.md"))


def read_text(path: Path) -> str | None:
    if not path.is_file():
        return None
    return path.read_text(encoding="utf-8")


def find_ids(text: str, scheme: str) -> list[str]:
    """Every occurrence of an ID scheme anywhere in text — definitions and
    citations both. Use find_row_defined_ids() to isolate definitions."""
    return ID_PATTERNS[scheme].findall(text)


def find_row_defined_ids(text: str, scheme: str) -> list[str]:
    """IDs that appear to be *defined* here: the ID is the first cell of a
    markdown table row (`| REQ-001 | ...`). This is what distinguishes a
    definition from a citation appearing in another column or file."""
    pattern = re.compile(rf"^\s*\|\s*({scheme}-\d+)\s*\|", re.MULTILINE)
    return pattern.findall(text)


def split_table_rows(text: str) -> list[list[str]]:
    """Parse every markdown table row (lines starting with `|`) into a list
    of stripped cells, skipping separator rows (`|---|---|`). Best-effort and
    forgiving — authored markdown varies; this is a structural aid, not a
    strict parser."""
    rows = []
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped.startswith("|"):
            continue
        if re.fullmatch(r"\|[\s:\-\|]+\|?", stripped):
            continue  # separator row
        cells = [c.strip() for c in stripped.strip("|").split("|")]
        rows.append(cells)
    return rows


def load_sibling_module(filename_stem: str):
    """Load another script in this directory as a module, even though its
    filename (like this one's caller) isn't a valid Python identifier. Runs
    the module's top-level code once (functions/constants only — every
    script in this folder guards its CLI behind `if __name__ == "__main__"`,
    which does not fire here since the loaded module's __name__ is its own
    dotted stand-in, never "__main__")."""
    path = SCRIPT_DIR / f"{filename_stem}.py"
    spec = importlib.util.spec_from_file_location(filename_stem.replace("-", "_"), path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module
