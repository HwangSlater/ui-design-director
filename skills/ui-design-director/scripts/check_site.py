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

sys.path.insert(0, str(Path(__file__).resolve().parent))
import fonts  # noqa: E402  (글꼴 이름 나누기는 fonts.py 하나로)
from anchor_check import AnchorTracker  # noqa: E402
from block_colours import check_blocks  # noqa: E402
from common import TOOL_DIRS, utf8_console  # noqa: E402
from page_rules import PageTracker, report_photo_reuse  # noqa: E402

HTML_SUFFIXES = {".html", ".htm"}
CSS_SUFFIXES = {".css"}
SKIP_DIRS = TOOL_DIRS | {"dist-cache"}
NON_LABELLED_INPUTS = {"hidden", "submit", "button", "reset", "image"}
VISUAL_TAGS = {"img", "svg", "picture", "video", "canvas"}  # 글자와 상자뿐인 화면을 찾는다
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
# 생성 티(unslop signs.md 참고, Damir Sokolovsky, CC BY 4.0 — github.com/heydamir/unslop): 바탕에 없으면 뺀다
HOVER_SCALE = re.compile(r":hover[^{]*\{[^}]*\bscale\(\s*1\.\d", re.IGNORECASE)
GLOW = re.compile(r"(?<![\d.])0(?:px)?\s+0(?:px)?\s+(\d+)px")  # 가운데서 번지는 그림자(빛남)
EMOJI = re.compile("[\U0001F300-\U0001FAFF\u2600-\u27BF\u2B50\u2728]")
WIDE_TRACKING_EM = 0.1
# 디자인 지식의 숫자 규칙(knowledge-typography·colour-motion): 본문 행간 1.5 안팎(1.4 아래는 빽빽), 본문 14px 미만은 작음, UI 움직임 500ms 넘으면 느림
RULE_BLOCK = re.compile(r"([^{}]+)\{([^{}]*)\}")
BODY_SELECTOR = re.compile(r"(^|[\s,>])(body|p|li|dd|td|article|\.body|\.text|\.desc)\b", re.IGNORECASE)
MIN_BODY_LINE_HEIGHT = 1.4
MIN_BODY_PX = 16  # USWDS·KRDS·Butterick 가 모두 16px
MAX_UI_MOTION_MS = 500


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
        self.emoji_seen = False
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
        self.anchors = AnchorTracker()
        self.page = PageTracker()  # 탭 제목·머리글·사진·시간 문구
        self.visuals = 0  # 로고·엠블럼·아이콘·사진처럼 글자가 아닌 것

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        a = {k: (v or "") for k, v in attrs}
        line = self.getpos()[0]
        self.anchors.start(tag, a, line)
        self.page.start(tag, a, line)
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
        if tag in VISUAL_TAGS:
            self.visuals += 1
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
        self.anchors.end(tag)
        self.page.end(tag)
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
        self.anchors.data(data)
        self.page.data(data)
        if not self.emoji_seen and EMOJI.search(data):
            self.emoji_seen = True  # 한 파일에 한 번
            self.report.add("DRIFT", self.path, self.getpos()[0], "emoji-icon",
                            f"이모지 「{EMOJI.search(data).group(0)}」 — 아이콘·꾸밈으로 쓴 이모지는 생성 티, 선 아이콘 한 벌이나 글로")
        if data.strip():
            for entry in self.name_stack:
                entry["named"] = True

    def finish(self) -> None:
        if not self.saw_html:
            return  # partial or component file; page-level rules do not apply
        self.anchors.report(self.path, self.report)
        if not self.is_board:
            self.page.report(self.path, self.report)
        if not self.has_lang:
            self.report.add("FLOOR", self.path, 1, "html-lang", "<html> has no lang attribute")
        if not self.has_viewport:
            self.report.add("FLOOR", self.path, 1, "viewport", "no <meta name=viewport>")
        if not self.visuals and not self.is_board:
            self.report.add("NOTE", self.path, 1, "no-visual-layer",
                            "no logo, mark, icon or image on the page (only text and boxes) — compare with the reference's visual layers")
        for control_id, line, tag in self.controls:
            if not control_id or control_id not in self.label_targets:
                self.report.add("FLOOR", self.path, line, "form-label",
                                f"<{tag}> has no associated label")


LEFT_INSET = re.compile(r"\binset\s+([2-9]|\d{2,})px\s+0(?:px)?\s+0")  # 안쪽 그림자로 그린 왼쪽 선


def is_left_stroke(prop: str, low: str) -> bool:
    """칸 왼쪽에만 넣은 색 선(사용자 지적: AI 가 자주 쓰는 방식) — 왼쪽 테두리 2px 이상이거나 안쪽 그림자 왼쪽 선."""
    if prop in ("border-left", "border-inline-start"):
        if any(w in low for w in ("none", "transparent", "hidden")):
            return False
        m = re.search(r"([\d.]+)px", low)
        return bool(m) and float(m.group(1)) >= 2
    if prop in ("border-left-width", "border-inline-start-width"):
        m = re.match(r"([\d.]+)px", low)
        return bool(m) and float(m.group(1)) >= 2
    return prop == "box-shadow" and bool(LEFT_INSET.search(low))


def check_reading_rules(src: CssSource, text: str, report: Report) -> None:
    """디자인 지식(knowledge.py)의 숫자 규칙 중 CSS 로 바로 잴 수 있는 것 — 본문 행간·글자 크기, 움직임 길이."""
    for m in RULE_BLOCK.finditer(text):
        selector, body = m.group(1), m.group(2)
        line = src.first_line + text.count("\n", 0, m.start())
        body_text = bool(BODY_SELECTOR.search(selector))
        for prop, value in DECLARATION.findall(body + ";"):
            prop, low = prop.lower(), value.strip().lower()
            if body_text and prop == "line-height":
                n = re.match(r"([\d.]+)(%|px)?$", low)
                if n and not n.group(2) and float(n.group(1)) < MIN_BODY_LINE_HEIGHT:
                    report.add("DRIFT", src.path, line, "line-height",
                               f"{selector.strip()[:40]} line-height {low} — 본문은 {MIN_BODY_LINE_HEIGHT} 이상(knowledge.py ask --part body-text)")
            if body_text and prop == "font-size":
                n = re.match(r"([\d.]+)px$", low)
                if n and float(n.group(1)) < MIN_BODY_PX:
                    report.add("DRIFT", src.path, line, "body-size",
                               f"{selector.strip()[:40]} font-size {low} — 본문은 {MIN_BODY_PX}px 이상(knowledge.py ask --part body-text)")
            if prop in ("transition", "transition-duration") and not low.startswith("opacity"):  # 사진 겹쳐 바꾸기는 느려도 된다
                for num, unit in re.findall(r"(\d*\.?\d+)(ms|s)\b", low):
                    ms = float(num) * (1000 if unit == "s" else 1)
                    if ms > MAX_UI_MOTION_MS:
                        report.add("DRIFT", src.path, line, "motion-duration",
                                   f"{prop}: {value.strip()} — 화면 전환·마우스 반응은 {MAX_UI_MOTION_MS}ms 안쪽(knowledge.py ask --part motion)")
                        break


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
            if prop == "letter-spacing":
                em = re.match(r"(-?[\d.]+)(em|px)", low)
                if em and (float(em.group(1)) >= WIDE_TRACKING_EM if em.group(2) == "em" else float(em.group(1)) >= 2):
                    report.add("DRIFT", src.path, line, "wide-tracking", f"{prop}: {value} — 넓게 벌린 대문자·제목은 생성 티, 바탕에 없으면 보통 자간")
            if is_left_stroke(prop, low):
                report.add("DRIFT", src.path, line, "left-stroke", f"{prop}: {value} — 칸·글·목록 왼쪽에만 넣은 색 선은 생성 티, 바탕에 없으면 면·굵기·표시로")
            if prop in ("box-shadow", "filter") and any(int(g) >= 12 for g in GLOW.findall(low)):
                report.add("DRIFT", src.path, line, "glow", f"{prop}: {value} — 가운데서 번지는 빛, 깊이는 면의 단계와 가는 선으로")
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

    for src in sources:
        text = blank_comments(src.text)
        m = HOVER_SCALE.search(text)
        if m:
            line = src.first_line + text.count("\n", 0, m.start())
            report.add("DRIFT", src.path, line, "hover-scale", "마우스를 올리면 커지는 카드·단추 — 바탕에 없으면 색·면 단계로")
        check_reading_rules(src, text, report)
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
    """글꼴 목록에서 첫 실제 글꼴(소문자). 이름 나누기는 fonts.family_names 하나로."""
    names = (n.lower() for n in fonts.family_names(value, shorthand=True))
    return next((n for n in names if n not in GENERIC_FAMILIES and "var(" not in n), "")


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
    photos: dict[str, list[tuple[str, int, bool]]] = {}
    for path in html_files:
        rel = str(path.relative_to(root))
        parser = PageParser(rel, report)
        parser.feed(path.read_text(encoding="utf-8", errors="replace"))
        parser.close()
        parser.finish()
        for css in parser.css:
            css.board = parser.is_board
        sources.extend(parser.css)
        if parser.saw_html and not parser.is_board:
            photos[rel] = parser.page.photos
    for path in css_files:
        sources.append(CssSource(str(path.relative_to(root)), 1,
                                 path.read_text(encoding="utf-8", errors="replace")))
    report_photo_reuse(photos, report)
    if sources:
        check_css(sources, report)
        check_blocks(sources, report)
    if not html_files and not css_files:
        report.add("FLOOR", str(root), 0, "no-files", "no HTML or CSS files found")
    return report


def main(argv: list[str]) -> int:
    utf8_console()
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
