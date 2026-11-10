#!/usr/bin/env python3
"""메인 페이지 짜임 점검 — 바탕의 메인 페이지가 아니라 메뉴·생성 티로 짠 곳을 찾는다.

    python site_shape.py <프로젝트 폴더>      # 걸린 것마다 한 줄. 있으면 끝 코드 1 (preflight.py 도 함께 돌린다)

보는 것(mockups/index.html 과 그 CSS, concept-brief.md 의 「사이트 꼴」, formats/바탕-구성.md):
- menu-stuffing: 머리 메뉴가 거의 다 같은 페이지 안 링크(#…) — 여러 쪽 사이트를 한 쪽 랜딩으로 만든 것(꽃집 13차·건축사무소 10차).
  「사이트 꼴: 한 쪽 홍보·모집」이면 보지 않는다. 로고·건너뛰기(#main·#top), 「#」만 적은 자리 링크, 전화·메일,
  걸러 보기 탭(data-cat·data-filter·role=tab·aria-controls)은 메뉴로 세지 않는다(레시피 9차 종류 탭).
- too-many-sections: 맨 위 구역(머리·section·바닥) 수가 바탕-구성.md 구역 표 줄 수보다 2 넘게 많음.
- numbered-steps: 1·2·3(01·02·03, 하나·둘·셋)으로 시작하는 형제 3~4개, 또는 제목에 순서·방법·이렇게·과정·단계가 든
  구역 안 3~4칸 <ol>. 바탕-구성.md 가 주문 순서·단계별 같은 번호 단계를 적었으면 보지 않는다.
- hero-box: 첫 구역에서 사진(img·배경 그림) 위에 겹친(absolute·fixed·같은 grid 칸·음수 여백) 색 상자 안에 제목과
  단추·링크가 함께 있음. 바탕-구성.md 가 「글상자」(또는 첫 화면·사진 위 상자)를 적었으면 보지 않는다.
한계: 그리지 않고 HTML·CSS 만 읽는다. CSS 는 클래스·id 선택자의 마지막 조각만 맞추고 미디어 쿼리를 가리지 않으며,
var() 색은 「칠함」으로 본다. 스크립트가 만드는 마크업, 겹침을 transform 이나 큰 z-index 로만 만든 경우는 못 본다.
"""
from __future__ import annotations

import re
import sys
from html.parser import HTMLParser
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import ONE_PAGE, mock_dir, read, site_kind, utf8_console  # noqa: E402

VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr"}
SKIP_TARGETS = {"#", "#main", "#top", "#content", "#home", "#body"}
FILTER_ATTRS = ("data-cat", "data-filter", "data-tab", "data-sort", "aria-controls")
STEP_HEADING = re.compile(r"순서|방법|이렇게|과정|단계|\bhow\b|\bsteps?\b", re.I)
NUMERALS = [("1", "2", "3", "4"), ("01", "02", "03", "04"), ("하나", "둘", "셋", "넷"), ("첫째", "둘째", "셋째", "넷째")]
# 바탕이 번호 단계를 가졌다는 말. 「순서」만으로는 안 된다 — 바탕-구성.md 표 머리(「순서 | 구획」)와 「같은 순서로」에 늘 나온다
BASE_STEPS = re.compile(r"(주문|이용|진행|예약|작업)\s*(순서|단계)|순서\s*안내|단계별|\d\s*단계|번호\s*(단계|매긴)|\bsteps?\b|how it works", re.I)
BASE_HERO_BOX = re.compile(r"글상자|(첫 화면|사진 위|사진에)[^\n|]{0,30}상자")
EXTRA_SECTIONS = 2
PAINT = re.compile(r"^(background|background-color)$")
NO_PAINT = re.compile(r"^(none|transparent|inherit|initial|unset|rgba\([^)]*,\s*0\)|0)$")
RULE = re.compile(r"([^{}]+)\{([^{}]*)\}")
DECL = re.compile(r"([-\w]+)\s*:\s*([^;]+)")
LAST_PART = re.compile(r"[^\s>+~]+$")


class Node:
    def __init__(self, tag: str, attrs: dict, line: int, parent: "Node | None") -> None:
        self.tag, self.attrs, self.line, self.parent = tag, attrs, line, parent
        self.kids: list[Node] = []
        self.items: list = []  # 글과 하위 요소를 나온 차례대로(보이는 글을 순서대로 잇는다)

    def walk(self):
        yield self
        for k in self.kids:
            yield from k.walk()

    def visible(self) -> str:
        if self.tag in ("script", "style", "svg"):
            return ""
        return " ".join(" ".join(i if isinstance(i, str) else i.visible() for i in self.items).split())

    def inside(self, *tags: str) -> bool:
        p = self.parent
        while p:
            if p.tag in tags:
                return True
            p = p.parent
        return False


class Tree(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.root = Node("#doc", {}, 0, None)
        self.cur = self.root
        self.css: list[str] = []
        self.links: list[str] = []

    def handle_starttag(self, tag, attrs):
        a = {k: (v or "") for k, v in attrs}
        node = Node(tag, a, self.getpos()[0], self.cur)
        self.cur.kids.append(node)
        self.cur.items.append(node)
        if tag == "link" and "stylesheet" in a.get("rel", ""):
            self.links.append(a.get("href", ""))
        if tag not in VOID:
            self.cur = node

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in VOID and self.cur.tag == tag:
            self.cur = self.cur.parent or self.root

    def handle_endtag(self, tag):
        n = self.cur
        while n is not self.root and n.tag != tag:
            n = n.parent
        if n is not self.root:
            self.cur = n.parent or self.root

    def handle_data(self, data):
        if self.cur.tag == "style":
            self.css.append(data)
        self.cur.items.append(data)


def parse(page: Path) -> Tree:
    t = Tree()
    t.feed(read(page))
    t.close()
    for href in t.links:  # 같은 폴더의 CSS 만(주소로 받는 글꼴 CSS 등은 건너뜀)
        if href and "://" not in href and not href.startswith("//"):
            t.css.append(read(page.parent / href.split("?")[0]))
    return t


def css_index(texts: list[str]) -> dict[str, dict[str, str]]:
    """「.클래스」·「#id」 → 선언. 선택자의 마지막 조각만 보고, :hover 같은 상태 선택자는 뺀다."""
    out: dict[str, dict[str, str]] = {}
    for text in texts:
        text = re.sub(r"/\*.*?\*/", "", text, flags=re.S)
        for m in RULE.finditer(text):
            decls = {p.lower(): v.strip().lower() for p, v in DECL.findall(m.group(2))}
            for sel in m.group(1).split(","):
                last = LAST_PART.search(sel.strip())
                if not last or ":" in last.group(0) or "@" in sel:
                    continue
                for key in re.findall(r"[.#][-\w]+", last.group(0)):
                    out.setdefault(key, {}).update(decls)
    return out


def style_of(node: Node, css: dict) -> dict[str, str]:
    s: dict[str, str] = {}
    for c in node.attrs.get("class", "").split():
        s.update(css.get("." + c, {}))
    if node.attrs.get("id"):
        s.update(css.get("#" + node.attrs["id"], {}))
    s.update({p.lower(): v.strip().lower() for p, v in DECL.findall(node.attrs.get("style", ""))})
    return s


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


def step_rows(tree: Tree) -> Node | None:
    for n in tree.root.walk():
        kids = [k for k in n.kids if k.tag not in ("script", "style")]
        if 3 <= len(kids) <= 4 and len({k.tag for k in kids}) == 1 and not n.inside("nav") and n.tag != "nav":
            texts = [k.visible() for k in kids]
            for nums in NUMERALS:
                if all(t.startswith(num) and not re.match(r"[\d,.:/]", t[len(num):len(num) + 1]) and len(t) > len(num) + 2
                       for t, num in zip(texts, nums)):
                    return n
        if n.tag == "ol" and 3 <= len([k for k in n.kids if k.tag == "li"]) <= 4:
            sec = n.parent
            while sec and sec.tag not in ("section", "article", "main", "#doc"):
                sec = sec.parent
            heads = [h.visible() for h in (sec.walk() if sec else []) if h.tag in ("h1", "h2", "h3")][:1]
            if heads and STEP_HEADING.search(heads[0]):
                return n
    return None


def overlaps(s: dict[str, str]) -> bool:
    return (s.get("position") in ("absolute", "fixed") or s.get("margin-top", "").startswith("-")
            or "grid-area" in s or ("grid-row" in s and "grid-column" in s))


def hero_box(tree: Tree, css: dict) -> Node | None:
    first = next((n for n in tree.root.walk() if n.tag == "section"), None)
    if not first:
        return None
    pics = [n for n in first.walk() if n.tag in ("img", "picture", "video")
            or "url(" in style_of(n, css).get("background", "") + style_of(n, css).get("background-image", "")]
    if not pics:
        return None
    for n in first.walk():
        if n is first or n in pics:
            continue
        s = style_of(n, css)
        paint = [v for p, v in s.items() if PAINT.match(p) and not NO_PAINT.match(v) and "gradient" not in v and "url(" not in v]
        inner = list(n.walk())
        if not paint or any(k in pics for k in inner):
            continue
        has_head = any(k.tag in ("h1", "h2", "h3") for k in inner)
        has_act = any(k.tag in ("a", "button") for k in inner)
        pic_over = any(overlaps(style_of(p, css)) or (p.parent and p.parent is not first and overlaps(style_of(p.parent, css))) for p in pics)
        if has_head and has_act and (overlaps(s) or pic_over):
            return n
    return None


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
    steps = None if BASE_STEPS.search(base) else step_rows(tree)
    if steps:
        out.append(f"DRIFT {where}:{steps.line} numbered-steps — 1·2·3 번호 단계 줄은 생성 티, 바탕에 없으면 뺀다(build-rules.md § What reads as generated)")
    box = None if BASE_HERO_BOX.search(base) else hero_box(tree, css)
    if box:
        out.append(f"DRIFT {where}:{box.line} hero-box — 첫 화면 사진 위 글상자(제목·단추를 담은 색 상자)는 바탕에 없으면 생성 티, 글은 사진 위에 바로 또는 사진 옆에")
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
