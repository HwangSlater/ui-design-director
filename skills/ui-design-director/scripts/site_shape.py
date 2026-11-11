#!/usr/bin/env python3
"""메인 페이지 짜임 점검 — 바탕의 메인 페이지가 아니라 메뉴·생성 티로 짠 곳을 찾는다.

    python site_shape.py <프로젝트 폴더>      # 걸린 것마다 한 줄. 있으면 끝 코드 1 (preflight.py 도 함께 돌린다)

보는 것(mockups/index.html 과 그 CSS, concept-brief.md 의 「사이트 꼴」, formats/바탕-구성.md):
- menu-stuffing: 머리 메뉴가 거의 다 같은 페이지 안 링크(#…) — 여러 쪽 사이트를 한 쪽 랜딩으로 만든 것(꽃집 13차·건축사무소 10차).
  「사이트 꼴: 한 쪽 홍보·모집」이면 보지 않는다. 로고·건너뛰기(#main·#top), 「#」만 적은 자리 링크, 전화·메일,
  걸러 보기 탭(data-cat·data-filter·role=tab·aria-controls)은 메뉴로 세지 않는다(레시피 9차 종류 탭).
- too-many-sections: 맨 위 구역(머리·section·바닥) 수가 바탕-구성.md 구역 표 줄 수보다 2 넘게 많음.
- numbered-steps: 1·2·3(01·02·03, 하나·둘·셋)으로 시작하는 형제 3~4개, 또는 제목에 순서·방법·이렇게·과정·단계가 든
  구역 안 3~4칸 <ol>.
- hero-box: 첫 구역에서 사진(img·배경 그림) 위에 겹친(absolute·fixed·같은 grid 칸·음수 여백) 색 상자 안에 제목과
  단추·링크가 함께 있음.
- letter-circle: 둥글게 깎은(border-radius 40% 이상·999px) 칸의 글이 한두 글자(한글·영문)인 것이 2개 이상 —
  사람 사진 대신 이름 첫 글자를 원에 넣은 것(치과 15차 「정」「윤」). 링크·단추·메뉴 안은 세지 않는다(로고·언어 단추).
- icon-row: 형제 3~4칸이 저마다 아이콘(svg·아이콘 클래스) → 짧은 제목 → 두 줄 안쪽 글로만 된 줄(플리마켓 14차
  「핸드메이드 작가 / 빈티지 셀러 / 동네 공방」).
생성 티로 판별한 꼴은 바탕에 있어도 걸린다(사용자 2026-11-11 「요즘 AI 로 만든 사이트가 많으니」).
한계: 그리지 않고 HTML·CSS 만 읽는다. CSS 는 클래스·id 선택자의 마지막 조각만 맞추고 미디어 쿼리를 가리지 않으며,
var() 색은 「칠함」으로 본다. 스크립트가 만드는 마크업, 겹침을 transform 이나 큰 z-index 로만 만든 경우는 못 본다.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import ONE_PAGE, base_marks, base_snapshots, mock_dir, read, save_base_marks, site_kind, utf8_console  # noqa: E402
# 나무·꼴 판단은 둘로 나눴다(파일 길이 한도) — 예전 이름(site_shape.parse·section_heads …)도 그대로 쓰이게 다시 내보낸다
from site_tree import *  # noqa: E402,F401,F403
from site_tree import _next_el, _tree  # noqa: E402,F401
from site_tells import *  # noqa: E402,F401,F403
from site_tells import _icon_item, _is_icon  # noqa: E402,F401


SKIP_TARGETS = {"#", "#main", "#top", "#content", "#home", "#body"}


FILTER_ATTRS = ("data-cat", "data-filter", "data-tab", "data-sort", "aria-controls")


EXTRA_SECTIONS = 2


# 바탕 저장본의 번호 칸 — CSS content:"01", 또는 글 칸 「01」「1.」
BASE_NUMBER = re.compile(r"""content\s*:\s*["'](\d{1,2})\.?["']|>\s*(\d{1,2})(?:\.\s|\.?\s*<)""")


def menu_links(tree: Tree) -> list[str]:
    """머리 메뉴 링크 주소 — <header> 안과 본문·바닥 밖 <nav> 의 <a>, 메뉴가 아닌 것은 뺀다."""
    out = []
    for n in tree.root.walk():
        if n.tag != "a" or not (n.inside("header") or (n.inside("nav") and not n.inside("main", "footer", "section"))):
            continue
        href = n.attrs.get("href", "").strip()
        if (not href or href.lower() in SKIP_TARGETS or href.startswith(("tel:", "mailto:", "sms:"))
                or any(k in n.attrs for k in FILTER_ATTRS) or n.attrs.get("role") == "tab"):
            continue
        out.append(href)
    return out


def menu_stuffed(links: list[str]) -> bool:
    anchors = {h for h in links if h.startswith("#")}
    return len(anchors) >= 3 or (len(links) >= 3 and len(anchors) * 2 >= len(links))


def top_sections(tree: Tree) -> int:
    """맨 위 구역 수 — 머리·바닥(구역 안이 아닌 것)과, 다른 구역 안에 들지 않은 section."""
    return sum(1 for n in tree.root.walk()
               if n.tag in ("header", "footer", "section") and not n.inside("section", "article", "header", "footer"))


def base_rows(text: str) -> int:
    """바탕-구성.md 첫 구역 표의 줄 수 — 첫 칸이 숫자로 시작하는 연이은 줄."""
    count = 0
    for line in text.splitlines():
        if re.match(r"\|\s*\d+\b", line):
            count += 1
        elif count:
            break
    return count


def base_facts(root: Path) -> dict:
    """바탕 저장본이 있으면 재서 formats/바탕-표지.json 에 남기고, 지워졌으면 남긴 것을 읽는다."""
    if not base_snapshots(root):
        return base_marks(root)
    trees = [_tree(p) for p in base_snapshots(root)]
    marks = {"snapshot": True, "numbered": _numbered(root), "icon_row": _icon_row(root),
             "section_heads": max((len(section_heads(t)) for t in trees), default=0),
             "cta_repeat": max((cta_repeat(t)[1] for t in trees), default=0),
             "faq": max((faq_items(t) for t in trees), default=0),
             "closing": any(closing_band(t, css_index(t.css)) for t in trees),
             "stats": any(stat_tiles(t) is not None for t in trees),
             "cta_box": any(cta_box(t, css_index(t.css)) is not None for t in trees),
             "overline": any(overline(t) is not None for t in trees)}
    save_base_marks(root, marks)
    return marks


def base_numbered(root: Path) -> bool:
    return bool(base_facts(root).get("numbered"))


def base_icon_row(root: Path) -> bool:
    return bool(base_facts(root).get("icon_row"))


def _numbered(root: Path) -> bool:
    """바탕 저장본에 1·2·3 이 잇달아 나오는가 — 같은 숫자가 겹쳐 적힌 것(같은 CSS 두 벌)은 하나로 본다."""
    for page in base_snapshots(root):
        html = re.sub(r"<script\b.*?</script>", "", read(page), flags=re.S | re.I)
        nums = [int(a or b) for a, b in BASE_NUMBER.findall(html)]
        nums = [n for i, n in enumerate(nums) if not i or n != nums[i - 1]]
        if any(nums[i:i + 3] == [1, 2, 3] for i in range(len(nums) - 2)):
            return True
    return False


def _icon_row(root: Path) -> bool:
    """바탕 저장본에 같은 짜임(아이콘·제목·짧은 글 3~4칸)의 줄이 있는가."""
    for page in base_snapshots(root):
        t = Tree()
        t.feed(read(page))
        t.close()
        if icon_row(t):
            return True
    return False


def check_project(root: Path) -> list[str]:
    """preflight.py 가 부른다 — 걸린 것마다 「DRIFT <쪽>:<줄> <규칙> — <말>」 한 줄."""
    page = mock_dir(root) / "index.html"
    if not page.is_file():
        return []
    tree = parse(page)
    css = css_index(tree.css)
    base = read(root / "formats" / "바탕-구성.md")
    where = page.relative_to(root).as_posix()
    out = []
    links = menu_links(tree)
    if site_kind(read(root / "concept-brief.md")) != ONE_PAGE and menu_stuffed(links):
        n = sum(h.startswith("#") for h in links)
        out.append(f"DRIFT {where}:1 menu-stuffing — 메뉴를 메인 페이지에 다 내려 담음 — 여러 쪽 사이트는 메뉴마다 쪽(링크) "
                   f"(메뉴 {len(links)}개 중 페이지 안 링크 {n}개, build-rules.md § Follow the base)")
    rows = base_rows(base)
    ours = top_sections(tree)
    if rows and ours > rows + EXTRA_SECTIONS:
        out.append(f"DRIFT {where}:1 too-many-sections — 구역이 바탕보다 많음 ({ours}/{rows}) — 메인은 바탕 메인의 구역과 순서대로")
    # AI 티로 판별한 꼴은 바탕에 있어도 걸린다(사용자 2026-11-11 「요즘 AI 로 만든 사이트가 많으니」, 자전거 39차의 Swapfiets)
    steps = step_rows(tree)
    if steps:
        out.append(f"DRIFT {where}:{steps.line} numbered-steps — 1·2·3 번호 단계 줄은 생성 티, 바탕에 없으면 뺀다(build-rules.md § What reads as generated)")
    box = hero_box(tree, css)
    if box:
        out.append(f"DRIFT {where}:{box.line} hero-box — 첫 화면 사진 위 글상자(제목·단추를 담은 색 상자)는 바탕에 없으면 생성 티, 글은 사진 위에 바로 또는 사진 옆에")
    circles = letter_circles(tree, css, custom_props(tree.css))
    if len(circles) >= 2:
        shown = "·".join(c.visible() for c in circles[:4])
        out.append(f"DRIFT {where}:{circles[0].line} letter-circle — 원 안 이름 첫 글자({shown})는 생성 티 — 사람 사진이 없으면 "
                   "이름·역할·한 줄을 글로만 두거나 그 칸을 빼고 「견본」 줄에 적는다(build-rules.md § Content and samples)")
    row = icon_row(tree)
    if row:
        out.append(f"DRIFT {where}:{row.line} icon-row — 아이콘·제목·짧은 글 칸 3~4개 줄은 생성 티, 바탕에 없으면 "
                   "바탕의 같은 자리 짜임으로(build-rules.md § What reads as generated)")
    for item in section_map(tree, base):
        line, msg = item.split("|", 1)
        out.append(f"DRIFT {where}:{line} section-map — {msg}(build-rules.md § Follow the base 2)")
    stats = stat_tiles(tree)
    if stats is not None:
        out.append(f"DRIFT {where}:{stats.line} stat-tiles — 큰 숫자 칸 줄(「8명 · 주 3회 · 3명」)은 생성 티 — 바탕에 없으면 숫자는 문장 속에"
                   "(build-rules.md § What reads as generated)")
    over = overline(tree)
    if over is not None:
        out.append(f"DRIFT {where}:{over.line} overline — 제목 「{over.visible()[:16]}」 위 작은 윗줄은 생성 티 — 바탕에 없으면 그 말은 제목 아래 문장이나 제목 안으로"
                   "(build-rules.md § What reads as generated)")
    box = cta_box(tree, css)
    if box is not None:
        out.append(f"DRIFT {where}:{box.line} cta-box — 색을 깐 칸 안의 제목·단추(「단체 주문 / 전화하기」 칸)는 생성 티 — 바탕에 없으면 "
                   "칸을 걷고 바탕 구역처럼 페이지 위에 글과 링크로(build-rules.md § What reads as generated)")
    close = closing_band(tree, css)
    if close is not None:
        out.append(f"DRIFT {where}:{close.line} closing-band — 바닥글 바로 위 색 칸에 제목·단추(「…로 먼저 만나요」 띠)는 스킬 없는 AI 시안의 끝맺음 — "
                   "바탕에 없으면 빼고 바탕의 마지막 구역대로(build-rules.md § What reads as generated)")
    reviews = made_up_reviews(tree, read(root / "concept-brief.md"))
    if reviews:
        out.append(f"DRIFT {where}:{reviews.line} made-up-reviews — 「{reviews.visible()[:20]}」 — 의뢰인이 준 후기가 없으면 후기 칸은 빼고 「견본」으로도 지어 넣지 않는다"
                   "(build-rules.md § Content and samples)")
    faq = faq_items(tree)
    if faq > FAQ_MAX:
        out.append(f"DRIFT {where}:1 faq-long — 메인 페이지에 펼침 질문 {faq}개 — 바탕 수만큼(많아도 {FAQ_MAX}개), 나머지는 자주 묻는 질문 쪽(링크)으로")
    name = placeholder_name(tree)
    if name:
        out.append(f"DRIFT {where}:1 placeholder-name — 이름 자리에 「{name}」 — 의뢰인에게 이름(임시라도)·가격·영업시간·예약처를 한 번에 묻고 넣는다"
                   "(guided-conversation.md § Ask for the page's facts)")
    heads = section_heads(tree)
    if len(heads) >= HEADS_MIN:
        out.append(f"DRIFT {where}:{heads[0].line} section-heads — 구역 {len(heads)}곳이 제목 밑 회색 한 줄(또는 제목 위 작은 윗줄)로 열림 — "
                   "바탕에 없으면 생성 티, 제목만 두거나 바탕의 구역 머리대로(build-rules.md § What reads as generated)")
    href, n_cta = cta_repeat(tree)
    if n_cta > CTA_MAX:
        out.append(f"DRIFT {where}:1 cta-repeat — 같은 곳({href[:40]})으로 가는 단추 {n_cta}개 — 바탕 수만큼만, 머리와 첫 화면·끝에 하나씩")
    marks = sample_marks(tree)
    if marks:
        out.append(f"DRIFT {where}:{marks[0].line} sample-mark — 페이지 안에 「견본」 표시 {len(marks)}곳 — 견본은 바닥글 「견본」 한 줄에만 "
                   "(build-rules.md § Content and samples)")
    return out


def main(argv: list[str]) -> int:
    utf8_console()
    if len(argv) != 1 or not Path(argv[0]).is_dir():
        print(__doc__.strip(), file=sys.stderr)
        return 2
    found = check_project(Path(argv[0]))
    for line in found:
        print(f"- {line}")
    print(f"걸린 것 {len(found)}" if found else "걸린 것 없음")
    return 1 if found else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
