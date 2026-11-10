"""site_shape.py 시험 — 메뉴를 메인에 내려 담기, 구역 수, 번호 단계, 첫 화면 글상자."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "skills" / "ui-design-director" / "scripts"))
import preflight  # noqa: E402
import site_shape  # noqa: E402

HEAD = '<!doctype html><html lang="ko"><head><link rel="stylesheet" href="main.css"></head><body>'
STUFFED = HEAD + """<header><a class="logo" href="#main">꽃집</a><nav>
<a href="#week">꽃다발</a><a href="#daily">꽃바구니</a><a href="#visit">찾아오는 길</a><a href="tel:0200">전화</a></nav></header>
<main id="main"><section id="week"><h2>이번 주</h2></section></main></body></html>"""
PAGES = HEAD + """<header><a href="index.html">꽃집</a><nav>
<a href="bouquet.html">꽃다발</a><a href="basket.html">꽃바구니</a><a href="visit.html">찾아오는 길</a></nav></header>
<main><section><h2>이번 주</h2></section></main></body></html>"""
FILTER_TABS = HEAD + """<header><a href="#">밥</a><ul>
<li><a href="#all" data-cat="">전체</a></li><li><a href="#all" data-cat="side">반찬</a></li>
<li><a href="#all" data-cat="soup">국</a></li><li><a href="#sets">묶음</a></li></ul></header>
<main><section id="all"><h2>전체</h2></section><section id="sets"><h2>묶음</h2></section></main></body></html>"""
STEPS = HEAD + """<main><section><h2>이렇게 주문해요</h2><ol>
<li><span>1</span><div>꽃과 받는 날 고르기</div></li><li><span>2</span><div>카드 문구 남기기</div></li>
<li><span>3</span><div>가게에서 찾기</div></li></ol></section></main></body></html>"""
PROCESS_OL = HEAD + """<main><section><h2>진행 과정</h2><ol><li>상담</li><li>실측과 설계</li><li>견적</li><li>공사</li></ol>
</section></main></body></html>"""
PAGER = HEAD + """<main><section><h2>작업</h2><div class="pager"><a href="#">1</a><a href="#">2</a><a href="#">3</a></div>
<ul><li>10평 상가 공사비</li><li>20평 아파트</li><li>30평 식당</li></ul></section></main></body></html>"""
HERO = HEAD + """<main><section class="hero"><div class="hero-in"><div class="hero-text"><h1>오늘 받아요</h1>
<a class="btn" href="order.html">주문</a></div><img class="hero-photo" src="a.jpg" alt=""></div></section></main></body></html>"""
HERO_CSS = ".hero-photo { position: absolute; inset: 0; }\n.hero-text { position: relative; background: var(--c-action); }\n"
HERO_PLAIN_CSS = ".hero-photo { position: absolute; inset: 0; }\n.hero-text { position: relative; }\n"


def project(tmp: Path, html: str, css: str = "", brief: str = "사이트 꼴: 여러 쪽", base: str = "") -> Path:
    (tmp / "mockups").mkdir(parents=True)
    (tmp / "mockups" / "index.html").write_text(html, encoding="utf-8")
    (tmp / "mockups" / "main.css").write_text(css, encoding="utf-8")
    (tmp / "concept-brief.md").write_text(brief, encoding="utf-8")
    if base:
        (tmp / "formats").mkdir()
        (tmp / "formats" / "바탕-구성.md").write_text(base, encoding="utf-8")
    return tmp


def rules(root: Path) -> list[str]:
    return [line.split()[2] for line in site_shape.check_project(root)]


def test_menu_of_anchors_is_stuffing(tmp_path: Path) -> None:
    lines = site_shape.check_project(project(tmp_path, STUFFED))
    assert any("menu-stuffing" in x and "메뉴를 메인 페이지에 다 내려 담음" in x for x in lines)
    assert any("menu-stuffing" in x for x in preflight.check(tmp_path))  # 보내기 전 점검에도 나온다


def test_one_page_promotion_may_use_anchors(tmp_path: Path) -> None:
    assert "menu-stuffing" not in rules(project(tmp_path, STUFFED, brief="사이트 꼴: 한 쪽 홍보·모집"))


def test_menu_to_pages_and_filter_tabs_pass(tmp_path: Path) -> None:
    assert "menu-stuffing" not in rules(project(tmp_path / "a", PAGES))
    assert "menu-stuffing" not in rules(project(tmp_path / "b", FILTER_TABS))


def test_more_sections_than_base(tmp_path: Path) -> None:
    many = HEAD + "<header></header>" + "<section><h2>x</h2></section>" * 6 + "<footer></footer></body></html>"
    base = "| 구역 | 하는 일 |\n|---|---|\n| 1 머리 | 메뉴 |\n| 2 첫 화면 | 사진 |\n| 3 상품 | 칸 |\n| 4 바닥 | 정보 |\n"
    lines = site_shape.check_project(project(tmp_path, many, base=base))
    assert any("구역이 바탕보다 많음 (8/4)" in x for x in lines)


def test_numbered_steps_and_step_list(tmp_path: Path) -> None:
    assert "numbered-steps" in rules(project(tmp_path / "a", STEPS))
    assert "numbered-steps" in rules(project(tmp_path / "b", PROCESS_OL))
    assert "numbered-steps" not in rules(project(tmp_path / "c", PAGER))


def test_numbered_steps_the_base_has_pass(tmp_path: Path) -> None:
    base = "| 순서 | 구획 |\n|---|---|\n| 1 | 주문 순서 3단계 |\n"
    assert "numbered-steps" not in rules(project(tmp_path / "a", STEPS, base=base))
    # 표 머리의 「순서」만으로는 바탕에 번호 단계가 있다고 보지 않는다
    assert "numbered-steps" in rules(project(tmp_path / "b", STEPS, base="| 순서 | 구획 |\n|---|---|\n| 1 | 작업 목록 |\n"))


def test_hero_box_over_photo(tmp_path: Path) -> None:
    assert "hero-box" in rules(project(tmp_path / "a", HERO, HERO_CSS))
    assert "hero-box" not in rules(project(tmp_path / "b", HERO, HERO_PLAIN_CSS))
    assert "hero-box" not in rules(project(tmp_path / "c", HERO, HERO_CSS, base="| 2 첫 화면 | 사진 위 흰 글상자에 제목 |\n"))



DOCTORS = HEAD + """<main><section><h2>의료진</h2>
<div class="doc"><div class="cover"><span>정</span></div><b>정한결 <small>대표원장</small></b></div>
<div class="doc"><div class="cover"><span>윤</span></div><b>윤서하 <small>원장</small></b></div>
<p><span class="tag">휴진</span><span class="tag">야간</span></p>
<a class="logo" href="index.html"><i>한</i></a></section></main></body></html>"""
DOCTORS_CSS = (":root { --r-pill: 999px; }\n.doc .cover span { width: 44%; aspect-ratio: 1; border-radius: 50%; }\n"
               ".tag { padding: 0 10px; border-radius: var(--r-pill); }\n.logo i { border-radius: 50%; }\n")
ICON_ROW = HEAD + """<main><section><h2>이런 분을 찾아요</h2><ul class="cols">
<li><svg class="i"></svg><h3>핸드메이드 작가</h3><p>직접 만든 물건을 파는 분</p></li>
<li><svg class="i"></svg><h3>빈티지 셀러</h3><p>오래된 옷과 그릇을 다시 내놓는 분</p></li>
<li><svg class="i"></svg><h3>동네 공방</h3><p>근처에서 공방을 꾸리는 분</p></li></ul></section></main></body></html>"""
PHOTO_ROW = ICON_ROW.replace('<svg class="i"></svg>', '<img src="a.jpg" alt="">')


def snapshot(root: Path, html: str) -> None:
    snap = root / "formats" / "snapshot" / "base-home-1280"
    snap.mkdir(parents=True, exist_ok=True)
    (snap / "index.html").write_text(html, encoding="utf-8")


def test_letter_circles_flagged_but_pills_and_logo_pass(tmp_path: Path) -> None:
    lines = site_shape.check_project(project(tmp_path / "a", DOCTORS, DOCTORS_CSS))
    assert any("letter-circle" in x and "(정·윤)" in x for x in lines)  # 알약 꼬리표 「휴진」, 링크 안 로고 「한」은 빼고
    one = DOCTORS.replace('<div class="doc"><div class="cover"><span>윤</span></div><b>윤서하 <small>원장</small></b></div>', "")
    assert "letter-circle" not in rules(project(tmp_path / "b", one, DOCTORS_CSS))


def test_icon_row_flagged_unless_base_has_it(tmp_path: Path) -> None:
    assert "icon-row" in rules(project(tmp_path / "a", ICON_ROW))
    assert "icon-row" not in rules(project(tmp_path / "b", PHOTO_ROW))  # 사진 칸 줄은 아이콘 줄이 아니다
    root = project(tmp_path / "c", ICON_ROW)
    snapshot(root, ICON_ROW.replace("핸드메이드 작가", "Planning"))
    assert "icon-row" not in rules(root)


def test_numbered_steps_the_base_snapshot_has_pass(tmp_path: Path) -> None:
    """바탕 저장본에 01·02·03 이 CSS content 로 있으면 번호 단계를 보지 않는다(세종스타치과, 치과 15차)."""
    root = project(tmp_path / "a", STEPS)
    snapshot(root, '<style>.one::before { content: "01"; } .one::before { content: "01"; } .two::before { content: "02"; }'
                   ' .thr::before { content: "03"; }</style><body></body>')
    assert "numbered-steps" not in rules(root)
    root = project(tmp_path / "b", STEPS)
    snapshot(root, "<body><p>1</p><p>전화 2,987건</p><p>3</p></body>")  # 1·2·3 이 잇달지 않음
    assert "numbered-steps" in rules(root)


def test_sample_mark_outside_the_foot_line(tmp_path: Path) -> None:
    """사진 밑 「견본 사진」 캡션은 걸리고, 바닥글의 「견본」 한 줄과 alt 글은 통과(치과 17차)."""
    body = (HEAD + '<main><figure><img src="a.jpg" alt="진료실(견본 사진)"><figcaption>진료실 — 견본 사진</figcaption></figure></main>'
            '<footer><p>견본: 사진과 소개 글</p></footer></body></html>')
    assert "sample-mark" in rules(project(tmp_path / "a", body))
    plain = HEAD + '<main><img src="a.jpg" alt="견본 사진"></main><p>사진은 견본이에요</p></body></html>'
    assert "sample-mark" not in rules(project(tmp_path / "b", plain))
