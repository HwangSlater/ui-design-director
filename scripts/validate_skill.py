#!/usr/bin/env python3
"""Dependency-free structural checks for the ui-design-director skill."""

from __future__ import annotations

import re
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
SKILL_NAME = "ui-design-director"
ROOT = REPO_ROOT / "skills" / SKILL_NAME
REQUIRED_FILES = (
    "SKILL.md",
    "agents/openai.yaml",
    "references/design-selection.md",
    "references/color-selection.md",
    "references/concept-preview.md",
    "references/guided-conversation.md",
    "references/reference-extraction.md",
    "references/design-md-format.md",
    "references/ui-review.md",
    "references/site-plan.md",
    "references/page-design.md",
    "references/site-build.md",
    "references/companion-skills.md",
    "references/comparison-board.md",
    "scripts/make_board.py",
    "scripts/capture.mjs",
    "scripts/wait_choice.mjs",
    "assets/dock.css",
    "assets/dock.js",
    "assets/board.css",
    "assets/board.js",
    "assets/palette-switcher.css",
    "assets/palette-switcher.js",
    "scripts/check_site.py",
    "scripts/anchor_check.py",
)
REPO_MARKDOWN_FILES = ("README.md", "README.en.md")
UNFINISHED_MARKERS = ("TODO", "TBD", "FIXME", "PLACEHOLDER")


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def parse_frontmatter(text: str) -> dict[str, str]:
    match = re.match(r"\A---\n(.*?)\n---(?:\n|\Z)", text, re.DOTALL)
    if not match:
        fail("SKILL.md must begin with YAML frontmatter")

    values: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if ":" not in line or line.startswith((" ", "\t")):
            continue
        key, value = line.split(":", 1)
        values[key.strip()] = value.strip().strip('"\'')
    return values


def check_required_files() -> None:
    missing = [path for path in REQUIRED_FILES if not (ROOT / path).is_file()]
    if missing:
        fail("missing required files: " + ", ".join(missing))


def check_metadata() -> None:
    skill_text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    metadata = parse_frontmatter(skill_text)

    if metadata.get("name") != SKILL_NAME:
        fail(f"frontmatter name must be {SKILL_NAME!r}")
    if not metadata.get("description"):
        fail("frontmatter description is required")
    if not re.fullmatch(r"[a-z0-9-]{1,64}", metadata["name"]):
        fail("frontmatter name must use lowercase letters, digits, and hyphens")

    interface_text = (ROOT / "agents/openai.yaml").read_text(encoding="utf-8")
    if "display_name:" not in interface_text or "short_description:" not in interface_text:
        fail("agents/openai.yaml must define display_name and short_description")
    if f"${SKILL_NAME}" not in interface_text:
        fail(f"agents/openai.yaml default_prompt must mention ${SKILL_NAME}")


def iter_markdown_files() -> list[Path]:
    files = [
        REPO_ROOT / path
        for path in REPO_MARKDOWN_FILES
        if (REPO_ROOT / path).is_file()
    ]
    files.append(ROOT / "SKILL.md")
    files.extend(sorted((ROOT / "references").glob("*.md")))
    return files


def check_markdown() -> None:
    link_pattern = re.compile(r"\[[^\]]+\]\(([^)]+)\)")

    for path in iter_markdown_files():
        text = path.read_text(encoding="utf-8")
        for marker in UNFINISHED_MARKERS:
            if re.search(rf"\b{marker}\b", text, re.IGNORECASE):
                fail(f"unfinished marker {marker!r} found in {path.relative_to(REPO_ROOT)}")

        for target in link_pattern.findall(text):
            if re.match(r"https?://", target):
                continue
            local_target = (path.parent / target).resolve()
            if not local_target.exists():
                fail(
                    f"broken local link in {path.relative_to(REPO_ROOT)}: {target}"
                )


ANCHOR_SAMPLE = """<!doctype html><html lang="ko"><head><meta name="viewport" content="width=device-width"></head><body>
<a href="#main">본문으로 건너뛰기</a><main id="main"><a href="#times">수업 시간 보기</a><a href="#gone">없음</a>
<a href="#bare">숨김</a><a href="#fees">수강료 보기</a>
<section id="times"><h2 class="sr">한눈에</h2><h3>초등학생</h3></section>
<section id="bare"><h2 class="sr">숨김</h2></section><section id="fees"><h2>수강료</h2></section></main></body></html>"""


def check_anchor_rules() -> None:
    """같은 페이지 링크 점검이 잡아야 할 것만 잡는지 본다(빈 문자열 → 결과 규칙 목록)."""
    sys.path.insert(0, str(ROOT / "scripts"))
    from check_site import PageParser, Report

    report = Report()
    parser = PageParser("sample.html", report)
    parser.feed(ANCHOR_SAMPLE)
    parser.close()
    parser.finish()
    got = sorted((f.rule, f.line) for f in report.findings if f.rule.startswith("anchor-"))
    want = [("anchor-heading", 3), ("anchor-label", 2), ("anchor-target", 2)]
    if got != want:
        fail(f"anchor rules: expected {want}, got {got}")
    # 글자와 상자뿐인 화면은 잡고, 아이콘 하나라도 있으면 넘어간다
    if [f.rule for f in report.findings if f.rule == "no-visual-layer"] != ["no-visual-layer"]:
        fail("no-visual-layer: a text-only page was not reported")
    report = Report()
    parser = PageParser("icon.html", report)
    parser.feed(ANCHOR_SAMPLE.replace('<main id="main">', '<main id="main"><svg viewBox="0 0 1 1"></svg>', 1))
    parser.close()
    parser.finish()
    if any(f.rule == "no-visual-layer" for f in report.findings):
        fail("no-visual-layer: a page with an icon was reported")


def main() -> None:
    check_required_files()
    check_metadata()
    check_markdown()
    check_anchor_rules()
    print("Skill validation passed.")


if __name__ == "__main__":
    main()
