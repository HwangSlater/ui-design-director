"""시안·바탕 HTML 을 읽는 작은 나무와 CSS 색인 — site_shape·site_tells 가 함께 쓴다."""
from __future__ import annotations

import re
import sys
from html.parser import HTMLParser
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import read  # noqa: E402


VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr"}


PAINT = re.compile(r"^(background|background-color)$")


NEUTRAL_BG = re.compile(r"^(#fff(fff)?|white|#fefefe|#fafafa|var\(--[\w-]*(bg|surface|paper|page)[\w-]*\))", re.I)  # 바탕·흰 면은 「색을 깐 칸」이 아니다


NO_PAINT = re.compile(r"^(none|transparent|inherit|initial|unset|rgba\([^)]*,\s*0\)|0)$")


RULE = re.compile(r"([^{}]+)\{([^{}]*)\}")


DECL = re.compile(r"([-\w]+)\s*:\s*([^;]+)")


BARE_TAG = re.compile(r"^[a-z][a-z0-9]*$")


VAR = re.compile(r"var\(\s*(--[-\w]+)\s*(?:,\s*([^)]+))?\)")


CUSTOM_PROP = re.compile(r"(--[-\w]+)\s*:\s*([^;{}]+)")


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

    def inside_node(self, node: "Node") -> bool:
        p = self.parent
        while p:
            if p is node:
                return True
            p = p.parent
        return False

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
