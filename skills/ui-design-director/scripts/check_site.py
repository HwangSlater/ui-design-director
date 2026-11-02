#!/usr/bin/env python3
"""Static checks for mockups and built sites: accessibility floor and token drift.

Usage: python check_site.py <directory> [--quiet]
Exit code 1 when any FLOOR finding exists. Reads HTML and CSS only; it does not
render pages, so contrast, layout, and overflow need the render pass.
"""

from __future__ import annotations

import re
import sys
from bisect import bisect_right
from dataclasses import dataclass
from html.parser import HTMLParser
from pathlib import Path

HTML_SUFFIXES = {".html", ".htm"}
CSS_SUFFIXES = {".css"}
SKIP_DIRS = {"node_modules", ".git", "dist-cache", "__pycache__"}
NON_LABELLED_INPUTS = {"hidden", "submit", "button", "reset", "image"}
GENERIC_FAMILIES = {
    "serif", "sans-serif", "monospace", "cursive", "fantasy", "system-ui",
    "ui-serif", "ui-sans-serif", "ui-monospace", "ui-rounded", "emoji", "math",
    "-apple-system", "blinkmacsystemfont", "inherit", "initial", "unset",
}
MAX_PRIMARY_FAMILIES = 2
BOARD_MARK = "comparison-board"

DECLARATION = re.compile(r"([-\w]+)\s*:\s*([^;{}]+)(?=[;}])")
COLOR_LITERAL = re.compile(r"#[0-9a-fA-F]{3,8}\b|\b(?:rgba?|hsla?|oklch|oklab|lab|lch)\(")
SIZE_LITERAL = re.compile(r"\d(?:px|rem|em|pt)\b")
CSS_COMMENT = re.compile(r"/\*.*?\*/", re.DOTALL)


@dataclass(frozen=True)
class Finding:
    tier: str
    path: str
    line: int
    rule: str
    message: str


@dataclass
class CssSource:
    path: str
    first_line: int
    text: str
    board: bool = False  # 색 견본이 곧 내용인 비교판: 날 색 값 경고를 끈다


class Report:
    def __init__(self) -> None:
        self.findings: list[Finding] = []

    def add(self, tier: str, path: str, line: int, rule: str, message: str) -> None:
        self.findings.append(Finding(tier, path, line, rule, message))


def blank_comments(text: str) -> str:
    """Remove comments but keep newlines so line numbers stay correct."""
    return CSS_COMMENT.sub(lambda m: re.sub(r"[^\n]", " ", m.group(0)), text)


def line_index(text: str) -> list[int]:
    return [i for i, ch in enumerate(text) if ch == "\n"]


class PageParser(HTMLParser):
    def __init__(self, path: str, report: Report) -> None:
        super().__init__(convert_charrefs=True)
        self.path = path
        self.report = report
        self.css: list[CssSource] = []
        self.has_lang = False
        self.has_viewport = False
        self.saw_html = False
        self.is_board = False
        self.ids: dict[str, int] = {}
        self.label_targets: set[str] = set()
        self.controls: list[tuple[str, int, str]] = []
        self.label_depth = 0
        self.raw_tag: str | None = None
        self.name_stack: list[dict] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        a = {k: (v or "") for k, v in attrs}
        line = self.getpos()[0]
        if tag == "html":
            self.saw_html = True
            self.has_lang = bool(a.get("lang", "").strip())
        elif tag == "meta" and a.get("name", "").lower() == "viewport":
            self.has_viewport = True
        elif tag == "meta" and a.get("name", "").lower() == "check-site":
            self.is_board = a.get("content", "").lower() == BOARD_MARK
        elif tag in ("style", "script"):
            self.raw_tag = tag
        if "id" in a and a["id"]:
            if a["id"] in self.ids:
                self.report.add("FLOOR", self.path, line, "duplicate-id",
                                f'id "{a["id"]}" already used on line {self.ids[a["id"]]}')
            else:
                self.ids[a["id"]] = line
        if "style" in a and a["style"].strip():
            self.css.append(CssSource(self.path, line, a["style"] + ";"))
        if tag == "img":
            if "alt" not in a:
                self.report.add("FLOOR", self.path, line, "img-alt",
                                'img has no alt attribute (use alt="" only for decoration)')
            elif a["alt"].strip():
                for entry in self.name_stack:
                    entry["named"] = True
        if tag == "label":
            self.label_depth += 1
            if a.get("for"):
                self.label_targets.add(a["for"])
        if tag in ("input", "select", "textarea"):
            kind = a.get("type", "text").lower()
            labelled = (self.label_depth > 0 or a.get("aria-label") or a.get("aria-labelledby")
                        or a.get("title"))
            if kind not in NON_LABELLED_INPUTS and not labelled:
                self.controls.append((a.get("id", ""), line, tag))
        if tag in ("button", "a") and not (tag == "a" and "href" not in a):
            named = bool(a.get("aria-label") or a.get("aria-labelledby") or a.get("title"))
            self.name_stack.append({"tag": tag, "line": line, "named": named})

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.handle_starttag(tag, attrs)

    def handle_endtag(self, tag: str) -> None:
        if tag == self.raw_tag:
            self.raw_tag = None
        if tag == "label" and self.label_depth:
            self.label_depth -= 1
        if tag in ("button", "a") and self.name_stack and self.name_stack[-1]["tag"] == tag:
            entry = self.name_stack.pop()
            if not entry["named"]:
                self.report.add("FLOOR", self.path, entry["line"], "accessible-name",
                                f"<{tag}> has no text or aria-label")

    def handle_data(self, data: str) -> None:
        if self.raw_tag == "style":
            self.css.append(CssSource(self.path, self.getpos()[0], data))
            return
        if self.raw_tag == "script":
            return
        if data.strip():
            for entry in self.name_stack:
                entry["named"] = True

    def finish(self) -> None:
        if not self.saw_html:
            return  # partial or component file; page-level rules do not apply
        if not self.has_lang:
            self.report.add("FLOOR", self.path, 1, "html-lang", "<html> has no lang attribute")
        if not self.has_viewport:
            self.report.add("FLOOR", self.path, 1, "viewport", "no <meta name=viewport>")
        for control_id, line, tag in self.controls:
            if not control_id or control_id not in self.label_targets:
                self.report.add("FLOOR", self.path, line, "form-label",
                                f"<{tag}> has no associated label")


def check_css(sources: list[CssSource], report: Report) -> None:
    outline_removals: list[tuple[str, int]] = []
    motion: list[tuple[str, int]] = []
    families: set[str] = set()
    has_focus_visible = has_reduced_motion = False

    for src in sources:
        text = blank_comments(src.text)
        has_focus_visible |= ":focus-visible" in text
        has_reduced_motion |= "prefers-reduced-motion" in text
        breaks = line_index(text)
        for m in DECLARATION.finditer(text):
            prop, value = m.group(1).lower(), m.group(2).strip()
            low = value.lower()
            line = src.first_line + bisect_right(breaks, m.start())
            if "!important" in low:
                report.add("DRIFT", src.path, line, "important", f"{prop}: {value}")
            if prop.startswith("--"):
                if "font" in prop and "family" in prop:
                    families.add(primary_family(value))
                continue  # token definitions are where literals belong
            if prop == "outline" and low.split()[0] in ("none", "0"):
                outline_removals.append((src.path, line))
            if prop in ("transition", "transition-property") and re.match(r"all\b", low):
                report.add("DRIFT", src.path, line, "transition-all", f"{prop}: {value}")
            if (prop.startswith("animation") or prop.startswith("transition")) and low not in ("none", "0s"):
                motion.append((src.path, line))
            if prop in ("background-clip", "-webkit-background-clip") and low == "text":
                report.add("NOTE", src.path, line, "gradient-text", "text filled with a background")
            if prop in ("font-family", "font"):
                if "var(" not in low:
                    if prop == "font":  # 글꼴 이름은 마지막 크기(/행간) 뒤에 온다
                        value = re.split(r"\d[\w.%]*(?:/\S+)?\s+", value)[-1]
                    families.add(primary_family(value))
            if "var(" in low or src.board:
                continue
            if COLOR_LITERAL.search(value):
                report.add("DRIFT", src.path, line, "raw-color", f"{prop}: {value} (use a token)")
            if prop == "font-size" and SIZE_LITERAL.search(value):
                report.add("DRIFT", src.path, line, "raw-font-size", f"{prop}: {value} (use a token)")

    if outline_removals and not has_focus_visible:
        for path, line in outline_removals:
            report.add("FLOOR", path, line, "focus-removed",
                       "outline removed and no :focus-visible style exists")
    if motion and not has_reduced_motion:
        path, line = motion[0]
        report.add("FLOOR", path, line, "reduced-motion",
                   f"{len(motion)} animation/transition rules and no prefers-reduced-motion query")
    families.discard("")
    if len(families) > MAX_PRIMARY_FAMILIES:
        report.add("NOTE", sources[0].path, 1, "font-families",
                   f"{len(families)} primary font families: {', '.join(sorted(families))}")


def primary_family(value: str) -> str:
    for part in value.split(","):
        name = re.sub(r"^(?:[\d.]+\S*\s+)+", "", part.strip())  # font 단축 속성의 크기·행간
        name = name.strip("'\"").lower()
        if name and name not in GENERIC_FAMILIES and "var(" not in name:
            return name
    return ""


def collect(root: Path) -> tuple[list[Path], list[Path]]:
    html, css = [], []
    for path in sorted(root.rglob("*")):
        if any(part in SKIP_DIRS for part in path.parts) or not path.is_file():
            continue
        if path.suffix.lower() in HTML_SUFFIXES:
            html.append(path)
        elif path.suffix.lower() in CSS_SUFFIXES:
            css.append(path)
    return html, css


def run(root: Path) -> Report:
    report = Report()
    html_files, css_files = collect(root)
    sources: list[CssSource] = []
    for path in html_files:
        rel = str(path.relative_to(root))
        parser = PageParser(rel, report)
        parser.feed(path.read_text(encoding="utf-8", errors="replace"))
        parser.close()
        parser.finish()
        for css in parser.css:
            css.board = parser.is_board
        sources.extend(parser.css)
    for path in css_files:
        sources.append(CssSource(str(path.relative_to(root)), 1,
                                 path.read_text(encoding="utf-8", errors="replace")))
    if sources:
        check_css(sources, report)
    if not html_files and not css_files:
        report.add("FLOOR", str(root), 0, "no-files", "no HTML or CSS files found")
    return report


def main(argv: list[str]) -> int:
    for stream in (sys.stdout, sys.stderr):
        stream.reconfigure(errors="replace")
    args = [a for a in argv if not a.startswith("--")]
    if len(args) != 1:
        print(__doc__.strip(), file=sys.stderr)
        return 2
    if not Path(args[0]).is_dir():
        print(f"ERROR: not a directory: {args[0]}", file=sys.stderr)
        return 2
    report = run(Path(args[0]))
    order = {"FLOOR": 0, "DRIFT": 1, "NOTE": 2}
    findings = sorted(report.findings, key=lambda f: (order[f.tier], f.path, f.line))
    if "--quiet" not in argv:
        for f in findings:
            print(f"{f.tier:<5}  {f.path}:{f.line}  {f.rule}  {f.message}")
    counts = {tier: sum(f.tier == tier for f in findings) for tier in order}
    print(f"FLOOR {counts['FLOOR']} | DRIFT {counts['DRIFT']} | NOTE {counts['NOTE']}")
    return 1 if counts["FLOOR"] else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
