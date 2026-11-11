"""시안에서 생성 티(AI 꼴)를 찾는 판단들 — 번호 단계·아이콘 줄·윗줄·회색 한 줄·색 칸·끝 띠·숫자 칸·글상자·원 안 글자 등. site_shape.check_project 가 부른다."""
from __future__ import annotations

import re

from site_tree import *  # noqa: F401,F403  (Node·Tree·style_of·_next_el·PAINT …)
from site_tree import _next_el, _tree  # noqa: F401


STEP_HEADING = re.compile(r"순서|방법|이렇게|과정|단계|\bhow\b|\bsteps?\b", re.I)


NUMERALS = [("1", "2", "3", "4"), ("01", "02", "03", "04"), ("하나", "둘", "셋", "넷"), ("첫째", "둘째", "셋째", "넷째")]


SHORT_LETTERS = re.compile(r"^[가-힣A-Za-z]{1,2}$")


INTERACTIVE = ("a", "button", "label", "select", "nav")


ICON_CLASS = re.compile(r"(^|[-_\s])(icon|ico)([-_\s]|$)", re.I)


ROW_HEAD = ("h2", "h3", "h4", "h5", "strong", "b", "dt")


ROW_HEAD_MAX = 30   # 아이콘 줄 제목 글자 수


ROW_TEXT_MAX = 90   # 두 줄 안쪽 설명 글자 수


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


HEADS_MIN = 3      # 이만큼 구역이 같은 머리(윗줄·제목·한 줄)로 열리면 생성 티 — 2 로는 주소·안내 칸(수학학원 29차)까지 걸렸다


CTA_MAX = 3        # 같은 곳으로 가는 채운 단추가 이보다 많으면 단추 되풀이


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


STAT_TEXT = re.compile(r"^[^\s]{0,3}\d[\d,.]*\s?[^\s]{0,4}$")  # 「8명」「주 3회」「6년」「120+」


STEP_NO = re.compile(r"^(0?\d|\d단계|step\d)$", re.I)


def stat_tiles(tree: Tree) -> Node | None:
    """형제 3~6개가 저마다 짧은 숫자 글(「8명」「주 3회」)로 시작하는 큰 숫자 칸 줄 — 바탕·스킬 없는 AI 둘 다 없던 것(수학학원 26·28차)."""
    for par in tree.root.walk():
        kids = [k for k in par.kids if k.tag in ("li", "div", "article", "dl", "figure")]
        if not 3 <= len(kids) <= 6:
            continue
        hits = 0
        for k in kids:
            first = next((n for n in k.walk() if n is not k and not n.kids and n.visible()), None)
            t = first.visible().replace(" ", "") if first is not None else ""
            if STEP_NO.match(t):  # 1·2·3, 01, 1단계 는 번호 단계(numbered-steps 가 본다)
                continue
            if t and STAT_TEXT.match(t[:10]) and any(ch.isdigit() for ch in t):
                hits += 1
        if hits >= 3 and hits >= len(kids) - 1:
            return par
    return None


OVERLINE_MAX = 30  # 제목 바로 위 이 글자 수 이하의 글 한 줄 = 작은 윗줄


def overline(tree: Tree) -> Node | None:
    """h1·h2 바로 위 짧은 글 한 줄(「11월 11일 수요일 · 오늘 나오는 시간」) — 한 곳만 있어도 생성 티(빵집 34차). 그 제목을 돌려준다."""
    for h in tree.root.walk():
        if h.tag not in ("h1", "h2") or h.inside("a", "header", "footer"):
            continue
        before = _next_el(h, -1)
        if before is not None and before.tag in ("p", "span", "small", "div") and not before.kids and 0 < len(before.visible()) <= OVERLINE_MAX:
            return h
    return None


def cta_box(tree: Tree, css: dict) -> Node | None:
    """첫 화면·머리·바닥 밖에서 색을 깐 칸 안에 제목과 단추 — 「단체 주문 / 전화하기」 남색 칸(빵집 30차). 끝 띠가 아니어도, 안쪽으로 들여도."""
    tops = [n for n in tree.root.walk() if n.tag == "section" and not n.inside("section", "article", "header", "footer")]
    first = tops[0] if tops else None
    for n in tree.root.walk():
        if n.tag not in ("section", "div", "aside") or n.inside("header", "footer") or n is first or (first is not None and n.inside_node(first)):
            continue
        s = style_of(n, css)
        painted = any(PAINT.match(p) and not NO_PAINT.match(v) and "url(" not in v and not NEUTRAL_BG.match(v) for p, v in s.items())
        if not painted:
            continue
        heads = [k for k in n.walk() if k.tag in ("h2", "h3")]
        btns = [k for k in n.walk() if k.tag in ("a", "button") and re.search(r"btn|button|cta", k.attrs.get("class", ""), re.I)]
        links = [k for k in n.walk() if k.tag == "a"]
        if heads and btns and len(links) <= 3 and len(heads) <= 2:
            return n
    return None


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


BASE_ROW = re.compile(r"^\|\s*(\d+)\b", re.M)


def section_map(tree: Tree, base: str) -> list[str]:
    """맨 위 구역마다 data-base="<바탕-구성.md 줄 번호>" 가 있고 그 줄이 구성표에 있는가.
    끝 단추 띠·숫자 칸 줄·색 칸처럼 바탕에 없는 구역을 모델이 덧붙이는 일이 이름만 바꿔 되풀이됐다(21~43차) — 꼴마다 막지 않고 구역째 본다."""
    rows = set(BASE_ROW.findall(base))
    if not rows:
        return []
    tops = [n for n in tree.root.walk() if n.tag == "section" and not n.inside("section", "article", "header", "footer")]
    unmapped = [n for n in tops if not n.attrs.get("data-base")]
    unknown = [n for n in tops if n.attrs.get("data-base") and not set(re.findall(r"\d+", n.attrs["data-base"])) <= rows]
    out = []
    if unmapped:
        out.append(f"{unmapped[0].line}|바탕 줄 표시 없는 구역 {len(unmapped)}개 — 구역마다 data-base=\"<바탕-구성.md 줄 번호>\"")
    for n in unknown:
        out.append(f"{n.line}|data-base=\"{n.attrs['data-base']}\" 는 바탕 구성표에 없는 줄 — 바탕에 없는 구역은 덧붙이지 않는다")
    return out


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
