"""
validate-generated-artifact.py

Responsibility
--------------
Deterministic, structural validation of what Implement actually produced
(`output/*`) — gate **B14**'s new structural-validation layer, run before
FINALIZE and before Preview & Run's own build/runtime checks
(`workflows/preview-run.md`). A benchmark run found two real defects a
build step alone didn't catch because the file still parsed/rendered: a
duplicate CSS custom-property declaration inside one rule block, and a
selector list that illegally mixed a selector with an `@media` at-rule
token — neither broke the build, both are genuinely invalid/fragile CSS.

This script performs lightweight, regex-and-stack-based structural checks
— it is **not** a real CSS/HTML/JS parser, and says so at every check
that is a heuristic rather than a guarantee. It complements, and never
replaces, `workflows/preview-run.md`'s existing build/runtime checks
(Rule 19, gate B14's original scope): a build succeeding and a page
rendering with no console error is still required separately — this
script catches structural defects that *don't* necessarily break either
of those (malformed-but-tolerated CSS, a duplicate id a browser silently
accepts, a missing `alt` attribute) and that a human visual pass is the
only other way to catch today.

Checks performed
----------------
CSS (from `<style>` blocks in .html, or .css files directly):
- Brace balance (a real syntax error almost always unbalances braces).
- Malformed selector list: a selector list that mixes a selector with an
  `@`-rule token (e.g. `.foo, @media (...){ ... }`) — invalid CSS that
  some engines silently drop rather than error on.
- Duplicate custom-property declarations within one rule block (the same
  `--name:` declared twice in one `{...}`) — the second silently wins,
  the first is dead code nobody will notice went unused.
- `@media` conditions with unbalanced parens.
- Raw hex/`rgb()` color literals with no adjacent token reference — the
  generated-code-level counterpart to `scripts/validate-tokens.py`'s own
  raw-value scan over markdown spec files (Rule 23), extended to the
  actual implementation.

HTML:
- Tag balance (stack-based, respecting the standard void-element set and
  self-closing syntax) — heuristic, not a full HTML5 parser.
- Duplicate `id` attributes.
- `<img>` with no `alt` and no `aria-hidden="true"`.
- A same-document `href="#x"` / `aria-describedby`/`aria-labelledby`/`for`
  citing an `id` that doesn't exist anywhere in the document.
- A `<button>`/`<a>` with empty text content and no `aria-label`/
  `aria-labelledby` — best-effort, non-nested cases only.

JS (from inline `<script>` blocks with no `src`, or .js files directly):
- Bracket/paren/brace balance, skipping over string and comment content —
  a safety net against the single most common structural mistake, not a
  substitute for actually running the code. Explicitly heuristic.

Assets:
- A local (non-`http(s)://`, non-`data:`) `src`/`href` reference whose
  target file doesn't exist relative to the artifact.

What this deliberately does NOT check
--------------------------------------
Runtime behavior (console errors, failed network requests, an unhandled
exception at render time) — those require actually executing the page,
which is `workflows/preview-run.md`'s existing job (Rule 19, step 6), not
reinvented here as a static check that can't actually observe them. A
syntactically valid but semantically wrong script (a variable used before
assignment, a typo'd function name that's still valid JS) — full
unresolved-reference checking needs a real JS parser/type-checker, out of
scope for a stdlib-only structural script per every other validator in
this folder. Whether the generated code matches its own `screen-
specification.md`/`component-spec.md` — that's `agents/qa-expert.md`'s
spot-check (Audit, analysis procedure step 6), a judgment call this
script doesn't make.

Status: implemented.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from urllib.parse import urlparse

import _common
from _common import Finding, read_text

VOID_ELEMENTS = {
    "area", "base", "br", "col", "embed", "hr", "img", "input",
    "link", "meta", "param", "source", "track", "wbr",
}

STYLE_BLOCK_RE = re.compile(r"<style\b[^>]*>(.*?)</style>", re.IGNORECASE | re.DOTALL)
SCRIPT_BLOCK_RE = re.compile(
    r"<script(?![^>]*\bsrc=)[^>]*>(.*?)</script>", re.IGNORECASE | re.DOTALL
)
TAG_RE = re.compile(r"<(/?)([a-zA-Z][a-zA-Z0-9-]*)((?:[^>\"']|\"[^\"]*\"|'[^']*')*?)(/?)>")
ID_ATTR_RE = re.compile(r"""\bid\s*=\s*["']([^"']+)["']""")
IMG_TAG_RE = re.compile(r"<img\b((?:[^>\"']|\"[^\"]*\"|'[^']*')*?)/?>", re.IGNORECASE)
HEX_COLOR_RE = re.compile(r"#[0-9a-fA-F]{3}(?:[0-9a-fA-F]{3}([0-9a-fA-F]{2})?)?\b")
RGB_FUNC_RE = re.compile(r"\brgba?\(\s*[\d.]+\s*,\s*[\d.]+\s*,\s*[\d.]+")


# ---------------------------------------------------------------------------
# CSS checks
# ---------------------------------------------------------------------------

def _extract_style_blocks(text: str) -> list[str]:
    return STYLE_BLOCK_RE.findall(text)


def _strip_css_comments(css: str) -> str:
    return re.sub(r"/\*.*?\*/", "", css, flags=re.DOTALL)


def _check_css_brace_balance(css: str, rel: str) -> list[Finding]:
    stripped = _strip_css_comments(css)
    opens, closes = stripped.count("{"), stripped.count("}")
    if opens != closes:
        return [Finding(
            "Blocker",
            f"Unbalanced CSS braces: {opens} '{{' vs {closes} '}}' — a real "
            "syntax error, not a style preference",
            rel, "css-brace-imbalance",
        )]
    return []


def _check_css_malformed_selector_list(css: str, rel: str) -> list[Finding]:
    """A selector list (comma-separated) must never contain an `@`-rule
    token as one of its members — e.g. `.foo, @media (...) {...}` is not
    valid CSS, even though some engines silently ignore the broken rule
    rather than raising. Detected as a comma followed by optional
    whitespace/newlines then an `@`, before the next `{`."""
    findings = []
    stripped = _strip_css_comments(css)
    for m in re.finditer(r",\s*@[a-zA-Z-]+[^{]*\{", stripped):
        snippet = m.group(0)[:80].replace("\n", " ")
        findings.append(Finding(
            "Blocker",
            f"Malformed selector list mixes a selector with an at-rule: "
            f"'{snippet}...' — a comma-separated selector list may never "
            "contain an @-rule token as a member",
            rel, "css-malformed-selector-list",
        ))
    return findings


def _iter_css_rule_blocks(css: str):
    """Yield each top-level `{ ... }` block's raw declaration text. Naive
    (doesn't handle nested @media bodies specially beyond brace counting),
    sufficient for the duplicate-custom-property check, which only cares
    about what's declared inside one block at a time."""
    depth = 0
    start = None
    for i, ch in enumerate(css):
        if ch == "{":
            if depth == 0:
                start = i + 1
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0 and start is not None:
                yield css[start:i]
                start = None


def _check_css_duplicate_custom_properties(css: str, rel: str) -> list[Finding]:
    findings = []
    stripped = _strip_css_comments(css)
    for block in _iter_css_rule_blocks(stripped):
        seen: dict[str, int] = {}
        for m in re.finditer(r"(--[a-zA-Z0-9_-]+)\s*:", block):
            name = m.group(1)
            seen[name] = seen.get(name, 0) + 1
        for name, count in seen.items():
            if count > 1:
                findings.append(Finding(
                    "Major",
                    f"Custom property '{name}' declared {count} times in "
                    "the same rule block — the last declaration silently "
                    "wins, the earlier one(s) are dead and misleading",
                    rel, "css-duplicate-custom-property",
                ))
    return findings


def _check_css_media_queries(css: str, rel: str) -> list[Finding]:
    findings = []
    stripped = _strip_css_comments(css)
    for m in re.finditer(r"@media\s*([^{]*)\{", stripped):
        condition = m.group(1)
        if condition.count("(") != condition.count(")"):
            findings.append(Finding(
                "Blocker",
                f"@media condition has unbalanced parens: '{condition.strip()[:80]}'",
                rel, "css-invalid-media-query",
            ))
    return findings


CUSTOM_PROPERTY_DECLARATION_RE = re.compile(r"--[a-zA-Z0-9_-]+\s*:\s*[^;{}]*")


def _check_css_raw_colors(css: str, rel: str) -> list[Finding]:
    """Flags a raw hex/rgb() color used as a regular property's *value*
    (e.g. `color: #1E8F5B` or `border-color: rgba(0,0,0,.1)`) — the
    generated-code-level counterpart to `scripts/validate-tokens.py`'s own
    raw-value scan over markdown spec files. A custom-property
    *definition* (`--good: #1E8F5B;`, including several on one line) is
    never flagged: that is the token's own declaration, literally where a
    raw value is supposed to live — flagging it would be noise against
    every token file's own :root block, not a real instance of 'used
    instead of a token'. Found by masking out every `--name: value`
    declaration's own span first, then scanning only what's left."""
    findings = []
    stripped = _strip_css_comments(css)
    # Replace each custom-property declaration's matched span with spaces
    # of the same length (preserves line/column numbering for the scan
    # below) so its own literal color value is never seen by the regexes.
    masked = CUSTOM_PROPERTY_DECLARATION_RE.sub(lambda m: " " * len(m.group(0)), stripped)
    for lineno, line in enumerate(masked.splitlines(), start=1):
        for match in HEX_COLOR_RE.finditer(line):
            findings.append(Finding(
                "Minor",
                f"Raw hex color '{match.group(0)}' in generated CSS with no "
                f"token reference nearby (line {lineno})",
                rel, "css-raw-value",
            ))
        for match in RGB_FUNC_RE.finditer(line):
            findings.append(Finding(
                "Minor",
                f"Raw rgb()/rgba() value '{match.group(0)}...' in generated "
                f"CSS with no token reference nearby (line {lineno})",
                rel, "css-raw-value",
            ))
    return findings


def check_css(css: str, rel: str) -> list[Finding]:
    findings = []
    findings += _check_css_brace_balance(css, rel)
    findings += _check_css_malformed_selector_list(css, rel)
    findings += _check_css_duplicate_custom_properties(css, rel)
    findings += _check_css_media_queries(css, rel)
    findings += _check_css_raw_colors(css, rel)
    return findings


# ---------------------------------------------------------------------------
# JS checks (heuristic — see module docstring)
# ---------------------------------------------------------------------------

def _strip_js_strings_and_comments(js: str) -> str:
    """Best-effort removal of string/template-literal/comment content so
    bracket-balance counting doesn't trip on a literal brace inside a
    string. Not a real tokenizer — doesn't handle every edge case (nested
    template-literal `${}` expressions are replaced wholesale, which is
    conservative/safe for a balance check since it removes matched pairs
    together)."""
    out = []
    i, n = 0, len(js)
    while i < n:
        c = js[i]
        if c == "/" and i + 1 < n and js[i + 1] == "/":
            j = js.find("\n", i)
            i = n if j == -1 else j
            continue
        if c == "/" and i + 1 < n and js[i + 1] == "*":
            j = js.find("*/", i + 2)
            i = n if j == -1 else j + 2
            continue
        if c in "\"'`":
            quote = c
            j = i + 1
            while j < n and js[j] != quote:
                if js[j] == "\\":
                    j += 1
                j += 1
            i = j + 1
            continue
        out.append(c)
        i += 1
    return "".join(out)


def _check_js_bracket_balance(js: str, rel: str) -> list[Finding]:
    stripped = _strip_js_strings_and_comments(js)
    findings = []
    for open_ch, close_ch, name in (("{", "}", "braces"), ("(", ")", "parens"), ("[", "]", "brackets")):
        o, c = stripped.count(open_ch), stripped.count(close_ch)
        if o != c:
            findings.append(Finding(
                "Blocker",
                f"Unbalanced JS {name}: {o} '{open_ch}' vs {c} '{close_ch}' "
                "(heuristic check — string/comment content excluded, but "
                "this is not a full parser)",
                rel, "js-bracket-imbalance",
            ))
    return findings


def check_js(js: str, rel: str) -> list[Finding]:
    return _check_js_bracket_balance(js, rel)


# ---------------------------------------------------------------------------
# HTML checks
# ---------------------------------------------------------------------------

def _check_html_tag_balance(html: str, rel: str) -> list[Finding]:
    stack: list[str] = []
    findings: list[Finding] = []
    for m in TAG_RE.finditer(html):
        closing, name, _attrs, self_close = m.group(1), m.group(2).lower(), m.group(3), m.group(4)
        if name in VOID_ELEMENTS or self_close == "/":
            continue
        if closing:
            if stack and stack[-1] == name:
                stack.pop()
            elif name in stack:
                # Closes an ancestor out of order — pop the mismatched ones.
                while stack and stack[-1] != name:
                    stack.pop()
                if stack:
                    stack.pop()
            else:
                findings.append(Finding(
                    "Major",
                    f"Closing tag </{name}> with no matching open tag "
                    "(heuristic scan, not a full HTML parser)",
                    rel, "html-unmatched-close-tag",
                ))
        else:
            stack.append(name)
    for name in stack:
        findings.append(Finding(
            "Major",
            f"<{name}> never closed (heuristic scan, not a full HTML parser)",
            rel, "html-unclosed-tag",
        ))
    return findings


def _check_html_duplicate_ids(html: str, rel: str) -> list[Finding]:
    seen: dict[str, int] = {}
    for m in ID_ATTR_RE.finditer(html):
        seen[m.group(1)] = seen.get(m.group(1), 0) + 1
    return [
        Finding("Major", f"Duplicate id '{id_}' ({count} occurrences)", rel, "html-duplicate-id")
        for id_, count in seen.items() if count > 1
    ]


def _check_html_img_alt(html: str, rel: str) -> list[Finding]:
    findings = []
    for m in IMG_TAG_RE.finditer(html):
        attrs = m.group(1)
        has_alt = re.search(r"""\balt\s*=\s*["']""", attrs) is not None
        is_hidden = re.search(r"""\baria-hidden\s*=\s*["']true["']""", attrs) is not None
        if not has_alt and not is_hidden:
            findings.append(Finding(
                "Major",
                "<img> with no alt attribute and no aria-hidden=\"true\" — "
                "missing accessible name",
                rel, "html-missing-alt",
            ))
    return findings


def _check_html_broken_internal_refs(html: str, rel: str) -> list[Finding]:
    ids_present = set(ID_ATTR_RE.findall(html))
    findings = []
    ref_patterns = [
        (re.compile(r"""href\s*=\s*["']#([^"'\s]+)["']"""), "href"),
        (re.compile(r"""aria-describedby\s*=\s*["']([^"']+)["']"""), "aria-describedby"),
        (re.compile(r"""aria-labelledby\s*=\s*["']([^"']+)["']"""), "aria-labelledby"),
        (re.compile(r"""\bfor\s*=\s*["']([^"']+)["']"""), "for"),
    ]
    for pattern, attr_name in ref_patterns:
        for m in pattern.finditer(html):
            for ref_id in m.group(1).split():  # aria-describedby may be space-separated
                if ref_id and ref_id not in ids_present:
                    findings.append(Finding(
                        "Major",
                        f"{attr_name}=\"{ref_id}\" references an id that "
                        "doesn't exist anywhere in this document",
                        rel, "html-broken-reference",
                    ))
    return findings


def _check_html_accessible_name(html: str, rel: str) -> list[Finding]:
    """Best-effort, non-nested-case check: a <button> or <a> whose own
    inner text is empty and which carries no aria-label/aria-labelledby
    has no accessible name. Does not attempt to resolve nested markup
    (an icon-only button with a nested <svg> and no text) — flagged only
    when the *entire* tag-to-tag span has no text content with no ARIA
    label present either, which is the unambiguous case."""
    findings = []
    for tag in ("button", "a"):
        for m in re.finditer(rf"<{tag}\b([^>]*)>(.*?)</{tag}>", html, re.IGNORECASE | re.DOTALL):
            attrs, inner = m.group(1), m.group(2)
            has_label = re.search(r"""aria-label\s*=\s*["'][^"']+["']""", attrs) or \
                re.search(r"""aria-labelledby\s*=\s*["'][^"']+["']""", attrs)
            has_svg_or_img = "<svg" in inner.lower() or "<img" in inner.lower()
            text_only = re.sub(r"<[^>]+>", "", inner).strip()
            if not text_only and not has_label and not has_svg_or_img:
                findings.append(Finding(
                    "Major",
                    f"<{tag}> has no text content, no icon/image child, and "
                    "no aria-label/aria-labelledby — no accessible name",
                    rel, "html-missing-accessible-name",
                ))
    return findings


def check_html(html: str, rel: str) -> list[Finding]:
    findings = []
    findings += _check_html_tag_balance(html, rel)
    findings += _check_html_duplicate_ids(html, rel)
    findings += _check_html_img_alt(html, rel)
    findings += _check_html_broken_internal_refs(html, rel)
    findings += _check_html_accessible_name(html, rel)
    for css in _extract_style_blocks(html):
        findings += check_css(css, rel)
    for js in SCRIPT_BLOCK_RE.findall(html):
        findings += check_js(js, rel)
    return findings


# ---------------------------------------------------------------------------
# Asset reference checks
# ---------------------------------------------------------------------------

ASSET_REF_RE = re.compile(r"""\b(?:src|href)\s*=\s*["']([^"']+)["']""")


def _is_local_path(value: str) -> bool:
    if value.startswith("#") or value.startswith("data:") or value.startswith("mailto:"):
        return False
    parsed = urlparse(value)
    return parsed.scheme == "" and not value.startswith("//")


def check_assets(html: str, base_dir: Path, rel: str) -> list[Finding]:
    findings = []
    for m in ASSET_REF_RE.finditer(html):
        value = m.group(1)
        if not _is_local_path(value):
            continue
        target = (base_dir / value.split("?", 1)[0].split("#", 1)[0]).resolve()
        if not target.is_file():
            findings.append(Finding(
                "Major",
                f"Local asset reference '{value}' does not resolve to an "
                "existing file",
                rel, "missing-asset-reference",
            ))
    return findings


# ---------------------------------------------------------------------------
# Top-level scan
# ---------------------------------------------------------------------------

def validate_file(path: Path, rel: str) -> list[Finding]:
    text = read_text(path)
    if text is None:
        return []
    suffix = path.suffix.lower()
    if suffix in (".html", ".htm"):
        findings = check_html(text, rel)
        findings += check_assets(text, path.parent, rel)
        return findings
    if suffix == ".css":
        return check_css(text, rel)
    if suffix in (".js", ".jsx", ".ts", ".tsx"):
        return check_js(text, rel)
    return []


def validate(output_dir: Path) -> list[Finding]:
    findings: list[Finding] = []
    if not output_dir.is_dir():
        return findings
    for path in sorted(output_dir.rglob("*")):
        if path.is_dir() or path.suffix.lower() not in (".html", ".htm", ".css", ".js", ".jsx", ".ts", ".tsx"):
            continue
        if "node_modules" in path.parts:
            continue
        rel = str(path.relative_to(output_dir.parent))
        findings += validate_file(path, rel)
    return findings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("target", help="Path to a product-builder's output/ directory, or a single file.")
    args = parser.parse_args(argv)

    target = Path(args.target)
    findings = validate_file(target, target.name) if target.is_file() else validate(target)

    if not findings:
        print("validate-generated-artifact: no findings.")
        return 0
    for f in findings:
        print(f)
    return 1 if any(f.severity in ("Blocker", "Major") for f in findings) else 0


if __name__ == "__main__":
    sys.exit(main())
