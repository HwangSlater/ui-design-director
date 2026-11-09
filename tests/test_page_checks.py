"""check_site.py 가 쓰는 페이지 점검 시험 — 같은 페이지 링크(anchor_check), 리뷰 실수(page_rules), 덩어리 색(block_colours).

예전에는 validate_skill.py 안에 있던 자체 시험을 그대로 옮겼다.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "skills" / "ui-design-director" / "scripts"))

from block_colours import check_blocks  # noqa: E402
from check_site import CssSource, PageParser, Report  # noqa: E402
from page_rules import report_photo_reuse, title_looks_like_option  # noqa: E402


ANCHOR_SAMPLE = """<!doctype html><html lang="ko"><head><meta name="viewport" content="width=device-width"></head><body>
<a href="#main">본문으로 건너뛰기</a><main id="main"><a href="#times">수업 시간 보기</a><a href="#gone">없음</a>
<a href="#bare">숨김</a><a href="#fees">수강료 보기</a>
<section id="times"><h2 class="sr">한눈에</h2><h3>초등학생</h3></section>
<section id="bare"><h2 class="sr">숨김</h2></section><section id="fees"><h2>수강료</h2></section></main></body></html>"""

REVIEW_SAMPLE = """<!doctype html><html lang="ko"><head><meta name="viewport" content="width=device-width">
<title>목록 2 거르기 칩 고정 · 쉼터</title></head><body><main>
<h1>가족을 기다리는 아이 <b>52</b>마리</h1><img src="a.jpg" alt="">
<h2>가족을 기다리는 아이들</h2><h2>자주 묻는 질문 <span class="sample">견본</span></h2><h2>자주 묻는 질문</h2>
<p>보통 3주쯤 걸려요.</p>
<p>2주쯤 걸려요 <span class="sample">확인 필요</span></p>
</main></body></html>"""

BLOCK_CSS = (
    ":root { --ink: #064420; --bg: #FDFAF6; } .top .btn { background: var(--ink); }"
    " .band { background: var(--ink); } .panel { background: var(--ink); } .toast { background: #064420; }"
)


def findings(html: str, name: str = "sample.html") -> list:
    report = Report()
    parser = PageParser(name, report)
    parser.feed(html)
    parser.close()
    parser.finish()
    return report.findings


def test_anchor_rules_catch_only_broken_links() -> None:
    got = sorted((f.rule, f.line) for f in findings(ANCHOR_SAMPLE) if f.rule.startswith("anchor-"))
    assert got == [("anchor-heading", 3), ("anchor-label", 2), ("anchor-target", 2)]


def test_text_only_page_has_no_visual_layer() -> None:
    assert [f.rule for f in findings(ANCHOR_SAMPLE) if f.rule == "no-visual-layer"] == ["no-visual-layer"]


def test_one_icon_is_enough_visual_layer() -> None:
    html = ANCHOR_SAMPLE.replace('<main id="main">', '<main id="main"><svg viewBox="0 0 1 1"></svg>', 1)
    assert not any(f.rule == "no-visual-layer" for f in findings(html, "icon.html"))


def test_review_rules() -> None:
    rules = ("title-option-label", "repeated-heading", "unsourced-duration")
    got = sorted((f.rule, f.line) for f in findings(REVIEW_SAMPLE) if f.rule in rules)
    assert got == [
        ("repeated-heading", 4), ("repeated-heading", 4),
        ("title-option-label", 2), ("unsourced-duration", 5), ("unsourced-duration", 5),
    ]


@pytest.mark.parametrize("title", ["입양 · 쉼터", "보리 입양 신청 · 쉼터", "2024년 후원금 쓰임", "새 가족 찾은 아이 3마리"])
def test_real_page_titles_are_not_option_labels(title: str) -> None:
    assert not title_looks_like_option(title)


def test_photo_reuse_across_pages() -> None:
    report = Report()
    pages = {f"p{i}.html": [("dog.jpg", 1, True)] for i in range(3)}
    report_photo_reuse(pages, report)
    assert not report.findings, "a list card on three pages was reported"
    pages["p0.html"].append(("dog.jpg", 9, False))
    report_photo_reuse(pages, report)
    assert [(f.path, f.line) for f in report.findings] == [("p0.html", 9)]


def test_five_blocks_in_one_strong_colour() -> None:
    report = Report()
    check_blocks([CssSource("a.css", 1, BLOCK_CSS + " .give { background: var(--ink); }")], report)
    assert [f.rule for f in report.findings] == ["one-colour-blocks"]


def test_second_block_colour_passes() -> None:
    report = Report()
    css = BLOCK_CSS + " .give { background: #E8A33D; } .hero { background: var(--bg); }"
    check_blocks([CssSource("a.css", 1, css)], report)
    assert not report.findings
