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
  numbered-steps 는 바탕 통째 저장(formats/snapshot/**/index.html)에 1·2·3(01·02·03, 1.·2.·3.)이 잇달아 나와도
  (글이든 CSS content 든) 보지 않는다 — 세종스타치과의 01–04 띠가 CSS ::before 에 있었는데 걸렸다(치과 15차).
- letter-circle: 둥글게 깎은(border-radius 40% 이상·999px) 칸의 글이 한두 글자(한글·영문)인 것이 2개 이상 —
  사람 사진 대신 이름 첫 글자를 원에 넣은 것(치과 15차 「정」「윤」). 링크·단추·메뉴 안은 세지 않는다(로고·언어 단추).
- icon-row: 형제 3~4칸이 저마다 아이콘(svg·아이콘 클래스) → 짧은 제목 → 두 줄 안쪽 글로만 된 줄(플리마켓 14차
  「핸드메이드 작가 / 빈티지 셀러 / 동네 공방」). 바탕 통째 저장에 같은 짜임의 줄이 있으면 보지 않는다.
한계: 그리지 않고 HTML·CSS 만 읽는다. CSS 는 클래스·id 선택자의 마지막 조각만 맞추고 미디어 쿼리를 가리지 않으며,
var() 색은 「칠함」으로 본다. 스크립트가 만드는 마크업, 겹침을 transform 이나 큰 z-index 로만 만든 경우는 못 본다.
"""
from __future__ import annotations

import re
import sys
from html.parser import HTMLParser
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import ONE_PAGE, base_marks, base_snapshots, mock_dir, read, save_base_marks, site_kind, utf8_console  # noqa: E402

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
BARE_TAG = re.compile(r"^[a-z][a-z0-9]*$")
VAR = re.compile(r"var\(\s*(--[-\w]+)\s*(?:,\s*([^)]+))?\)")
CUSTOM_PROP = re.compile(r"(--[-\w]+)\s*:\s*([^;{}]+)")
# 바탕 저장본의 번호 칸 — CSS content:"01", 또는 글 칸 「01」「1.」
BASE_NUMBER = re.compile(r"""content\s*:\s*["'](\d{1,2})\.?["']|>\s*(\d{1,2})(?:\.\s|\.?\s*<)""")
SHORT_LETTERS = re.compile(r"^[가-힣A-Za-z]{1,2}$")
INTERACTIVE = ("a", "button", "label", "select", "nav")
ICON_CLASS = re.compile(r"(^|[-_\s])(icon|ico)([-_\s]|$)", re.I)
ROW_HEAD = ("h2", "h3", "h4", "h5", "strong", "b", "dt")
ROW_HEAD_MAX = 30   # 아이콘 줄 제목 글자 수
ROW_TEXT_MAX = 90   # 두 줄 안쪽 설명 글자 수
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
                keys = re.findall(r"[.#][-\w]+", last.group(0))
                before = sel.strip()[:last.start()].split()
                if not keys and BARE_TAG.match(last.group(0)) and before:  # 「.cover span」 → 부모 클래스 아래 태그 열쇠
                    keys = [f"{k} {last.group(0)}" for k in re.findall(r"\.[-\w]+", before[-1])[-1:]]
                for key in keys:
                    out.setdefault(key, {}).update(decls)
    return out


def custom_props(texts: list[str]) -> dict[str, str]:
    """CSS 변수(--이름: 값) — 둥근 모서리가 var(--r-pill) 로 적혀 있어 값을 풀어 본다."""
    out: dict[str, str] = {}
    for text in texts:
        out.update({k: v.strip().lower() for k, v in CUSTOM_PROP.findall(re.sub(r"/\*.*?\*/", "", text, flags=re.S))})
    return out


def style_of(node: Node, css: dict) -> dict[str, str]:
    s: dict[str, str] = {}
    p, depth = node.parent, 0
    while p and depth < 3:  # 「.부모 태그」 규칙 — 가까운 부모 것이 이기게 먼 부모 것은 빈 자리만 채운다
        for c in p.attrs.get("class", "").split():
            for k, v in css.get(f".{c} {node.tag}", {}).items():
                s.setdefault(k, v)
        p, depth = p.parent, depth + 1
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


def base_facts(root: Path) -> dict:
    """바탕 저장본이 있으면 재서 formats/바탕-표지.json 에 남기고, 지워졌으면 남긴 것을 읽는다."""
    if not base_snapshots(root):
        return base_marks(root)
    trees = [_tree(p) for p in base_snapshots(root)]
    marks = {"snapshot": True, "numbered": _numbered(root), "icon_row": _icon_row(root),
             "section_heads": max((len(section_heads(t)) for t in trees), default=0),
             "cta_repeat": max((cta_repeat(t)[1] for t in trees), default=0),
             "faq": max((faq_items(t) for t in trees), default=0),
             "closing": any(closing_band(t, css_index(t.css)) for t in trees)}
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


def is_round(s: dict[str, str], props: dict[str, str]) -> bool:
    r = s.get("border-radius", "")
    for _ in range(3):  # var() 를 몇 겹까지 푼다
        r = VAR.sub(lambda m: props.get(m.group(1), m.group(2) or ""), r)
    m = re.match(r"\s*([\d.]+)(%|px|r?em)", r)
    if not m:
        return False
    v, unit = float(m.group(1)), m.group(2)
    if unit == "%":
        return v >= 40
    # 999px 는 알약 꼬리표(「휴진」)에도 쓴다 — 가로세로가 같다고 적힌 것만 원으로
    square = s.get("aspect-ratio", "").replace(" ", "") in ("1", "1/1") or (s.get("width") and s.get("width") == s.get("height"))
    return bool(square) and v >= (999 if unit == "px" else 50)


def letter_circles(tree: Tree, css: dict, props: dict[str, str]) -> list[Node]:
    """둥근 칸 안 한두 글자. 링크·단추·메뉴 안은 뺀다. 원 안의 span 처럼 겹친 것은 하나로."""
    out: list[Node] = []
    for n in tree.root.walk():
        if n.tag in INTERACTIVE or n.inside(*INTERACTIVE) or not SHORT_LETTERS.match(n.visible()):
            continue
        if is_round(style_of(n, css), props) and not any(o is n or n in list(o.walk()) for o in out):
            out.append(n)
    return out


def _is_icon(n: Node) -> bool:
    if n.tag == "svg":
        return True
    cls = n.attrs.get("class", "")
    if n.tag == "img":
        return bool(ICON_CLASS.search(cls) or re.search(r"icon|\.svg($|\?)", n.attrs.get("src", ""), re.I))
    return not n.visible() and (bool(ICON_CLASS.search(cls)) or any(k.tag == "svg" for k in n.walk()))


def _icon_item(n: Node) -> bool:
    """아이콘 → 짧은 제목 → (두 줄 안쪽 글) 한 칸."""
    kids = [k for k in n.kids if k.tag not in ("script", "style")]
    if not 2 <= len(kids) <= 3 or not _is_icon(kids[0]):
        return False
    head = kids[1]
    if head.tag not in ROW_HEAD or not 0 < len(head.visible()) <= ROW_HEAD_MAX:
        return False
    return len(kids) == 2 or (not any(k.tag in ROW_HEAD for k in kids[2].walk()) and len(kids[2].visible()) <= ROW_TEXT_MAX)


LEAD_MAX = 45      # 제목 바로 밑 이 글자 수 이하 = 「회색 한 줄 설명」
EYEBROW_MAX = 24   # 제목 바로 위 이 글자 수 이하 = 작은 윗줄
HEADS_MIN = 3      # 이만큼 구역이 같은 머리(윗줄·제목·한 줄)로 열리면 생성 티
CTA_MAX = 3        # 같은 곳으로 가는 채운 단추가 이보다 많으면 단추 되풀이


def _tree(page: Path) -> Tree:
    t = Tree()
    t.feed(read(page))
    t.close()
    return t


def _next_el(n: Node, step: int) -> Node | None:
    if not n.parent:
        return None
    kids = n.parent.kids
    i = kids.index(n) + step
    return kids[i] if 0 <= i < len(kids) else None


def section_heads(tree: Tree) -> list[Node]:
    """제목(h2) 바로 밑 짧은 한 줄, 또는 바로 위 작은 윗줄로 여는 구역 머리 — 애견미용 19차 4번, 스킬 없는 AI 시안은 윗줄 5번."""
    out = []
    for h in (n for n in tree.root.walk() if n.tag == "h2" and not n.inside("a")):  # 링크 칸 안 제목은 구역 머리가 아니다
        after, before = _next_el(h, 1), _next_el(h, -1)
        lead = after is not None and after.tag == "p" and 0 < len(after.visible()) <= LEAD_MAX
        brow = before is not None and before.tag in ("p", "span", "div", "small") and 0 < len(before.visible()) <= EYEBROW_MAX and not before.kids
        if lead or brow:
            out.append(h)
    return out


def cta_repeat(tree: Tree) -> tuple[str, int]:
    """같은 주소로 가는 단추 꼴 링크가 가장 많은 것 (주소, 수) — 19차는 네이버 예약 단추 5개, 바탕은 2개."""
    count: dict[str, int] = {}
    for n in tree.root.walk():
        cls = n.attrs.get("class", "")
        if n.tag in ("a", "button") and re.search(r"btn|button|cta", cls, re.I) and n.attrs.get("href", "#") not in ("", "#"):
            count[n.attrs["href"]] = count.get(n.attrs["href"], 0) + 1
    return max(count.items(), key=lambda kv: kv[1], default=("", 0))


PLACEHOLDER_NAME = re.compile(r"가게\s*이름|상호\s*명|업체\s*명|브랜드\s*명|회사\s*이름|your\s*(brand|company|logo)|\blogo\b|사이트\s*이름", re.I)


FAQ_MAX = 6   # 메인 페이지의 펼침 질문이 이보다 많고 바탕보다 많으면 — 21차는 11개, 바탕·스킬 없는 AI 는 0


def faq_items(tree: Tree) -> int:
    """펼침 질문 수 — details, aria-expanded 단추."""
    return sum(1 for n in tree.root.walk() if n.tag == "details" or (n.tag == "button" and "aria-expanded" in n.attrs))


REVIEW_HEAD = re.compile(r"후기|리뷰|review|testimonial|고객\s*(이야기|한마디)|보호자\s*이야기", re.I)
REVIEW_GIVEN = re.compile(r"(실제|받은|보내 준|준)\s*후기|후기\s*[:：]|리뷰\s*[:：]")


def made_up_reviews(tree: Tree, brief: str) -> Node | None:
    """후기 제목이 있는데 맥락 정리에 의뢰인이 준 후기가 없으면 그 제목(애견미용 24차 「보호자 후기」 견본)."""
    if REVIEW_GIVEN.search(brief):
        return None
    return next((n for n in tree.root.walk() if n.tag in ("h2", "h3") and REVIEW_HEAD.search(n.visible())), None)


def closing_band(tree: Tree, css: dict) -> Node | None:
    """바닥글 바로 앞 덩어리가 색을 깐 칸에 제목·단추를 담은 마무리 띠면 그 칸 — 스킬 없는 AI 시안의 끝맺음(애견미용 25차·수학학원 26차)."""
    foot = next((n for n in tree.root.walk() if n.tag == "footer" and not n.inside("footer")), None)
    if not foot or not foot.parent:
        return None
    sibs = [k for k in foot.parent.kids if k.tag not in ("script", "style", "link")]
    i = sibs.index(foot)
    prev = sibs[i - 1] if i else None
    if prev is not None and prev.tag == "main":
        inner = [k for k in prev.kids if k.tag not in ("script", "style")]
        prev = inner[-1] if inner else None
    if prev is None:
        return None
    for n in prev.walk():
        if n.tag not in ("section", "div", "aside"):
            continue
        s = style_of(n, css)
        painted = any(PAINT.match(p) and not NO_PAINT.match(v) and "url(" not in v for p, v in s.items())
        has_head = any(k.tag in ("h2", "h3") for k in n.walk())
        has_btn = any(k.tag in ("a", "button") and re.search(r"btn|button|cta", k.attrs.get("class", ""), re.I) for k in n.walk())
        if painted and has_head and has_btn:
            return n
    return None


def placeholder_name(tree: Tree) -> str | None:
    """제목(title)·머리 로고 글에 이름 대신 빈칸 말(「가게 이름」)이 있으면 그 말."""
    for n in tree.root.walk():
        if n.tag == "title" or (n.tag == "header" and not n.inside("header")):
            m = PLACEHOLDER_NAME.search(" ".join(i for i in n.items if isinstance(i, str)) if n.tag == "title" else n.visible())
            if m:
                return m.group(0)
    return None


def icon_row(tree: Tree) -> Node | None:
    for n in tree.root.walk():
        kids = [k for k in n.kids if k.tag not in ("script", "style")]
        if 3 <= len(kids) <= 4 and len({k.tag for k in kids}) == 1 and all(_icon_item(k) for k in kids):
            return n
    return None


def _icon_row(root: Path) -> bool:
    """바탕 저장본에 같은 짜임(아이콘·제목·짧은 글 3~4칸)의 줄이 있는가."""
    for page in base_snapshots(root):
        t = Tree()
        t.feed(read(page))
        t.close()
        if icon_row(t):
            return True
    return False


def sample_marks(tree: Tree) -> list[Node]:
    """페이지 끝 「견본」 한 줄 밖에서 글로 「견본」을 단 곳(사진 밑 「진료실 — 견본 사진」, 「…(견본)」).
    바닥글 안과 맨 마지막 「견본」 글(바닥글 태그가 없는 쪽의 끝 줄)은 그 한 줄로 본다. alt·aria 글은 보이지 않으니 세지 않는다."""
    found = []
    for n in tree.root.walk():
        own = " ".join(i for i in n.items if isinstance(i, str))
        if "견본" in own and n.tag not in ("script", "style", "title") and not n.inside("script", "style", "title"):
            found.append(n)
    return [n for n in found[:-1] if n.tag != "footer" and not n.inside("footer")]


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
    if steps and base_numbered(root):
        steps = None
    if steps:
        out.append(f"DRIFT {where}:{steps.line} numbered-steps — 1·2·3 번호 단계 줄은 생성 티, 바탕에 없으면 뺀다(build-rules.md § What reads as generated)")
    box = None if BASE_HERO_BOX.search(base) else hero_box(tree, css)
    if box:
        out.append(f"DRIFT {where}:{box.line} hero-box — 첫 화면 사진 위 글상자(제목·단추를 담은 색 상자)는 바탕에 없으면 생성 티, 글은 사진 위에 바로 또는 사진 옆에")
    circles = letter_circles(tree, css, custom_props(tree.css))
    if len(circles) >= 2:
        shown = "·".join(c.visible() for c in circles[:4])
        out.append(f"DRIFT {where}:{circles[0].line} letter-circle — 원 안 이름 첫 글자({shown})는 생성 티 — 사람 사진이 없으면 "
                   "이름·역할·한 줄을 글로만 두거나 그 칸을 빼고 「견본」 줄에 적는다(build-rules.md § Content and samples)")
    row = icon_row(tree)
    if row and not base_icon_row(root):
        out.append(f"DRIFT {where}:{row.line} icon-row — 아이콘·제목·짧은 글 칸 3~4개 줄은 생성 티, 바탕에 없으면 "
                   "바탕의 같은 자리 짜임으로(build-rules.md § What reads as generated)")
    close = closing_band(tree, css)
    if close is not None and not base_facts(root).get("closing"):
        out.append(f"DRIFT {where}:{close.line} closing-band — 바닥글 바로 위 색 칸에 제목·단추(「…로 먼저 만나요」 띠)는 스킬 없는 AI 시안의 끝맺음 — "
                   "바탕에 없으면 빼고 바탕의 마지막 구역대로(build-rules.md § What reads as generated)")
    reviews = made_up_reviews(tree, read(root / "concept-brief.md"))
    if reviews:
        out.append(f"DRIFT {where}:{reviews.line} made-up-reviews — 「{reviews.visible()[:20]}」 — 의뢰인이 준 후기가 없으면 후기 칸은 빼고 「견본」으로도 지어 넣지 않는다"
                   "(build-rules.md § Content and samples)")
    faq = faq_items(tree)
    if faq > max(FAQ_MAX, base_facts(root).get("faq", 0)):
        out.append(f"DRIFT {where}:1 faq-long — 메인 페이지에 펼침 질문 {faq}개 — 바탕 수만큼(많아도 {FAQ_MAX}개), 나머지는 자주 묻는 질문 쪽(링크)으로")
    name = placeholder_name(tree)
    if name:
        out.append(f"DRIFT {where}:1 placeholder-name — 이름 자리에 「{name}」 — 의뢰인에게 이름(임시라도)·가격·영업시간·예약처를 한 번에 묻고 넣는다"
                   "(guided-conversation.md § Ask for the page's facts)")
    heads = section_heads(tree)
    if len(heads) >= HEADS_MIN and base_facts(root).get("section_heads", 0) < HEADS_MIN:
        out.append(f"DRIFT {where}:{heads[0].line} section-heads — 구역 {len(heads)}곳이 제목 밑 회색 한 줄(또는 제목 위 작은 윗줄)로 열림 — "
                   "바탕에 없으면 생성 티, 제목만 두거나 바탕의 구역 머리대로(build-rules.md § What reads as generated)")
    href, n_cta = cta_repeat(tree)
    if n_cta > max(CTA_MAX, base_facts(root).get("cta_repeat", 0)):
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
