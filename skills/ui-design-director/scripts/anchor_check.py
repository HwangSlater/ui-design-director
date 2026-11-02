"""같은 페이지 안 링크(href="#…")가 누른 사람이 기대한 곳으로 가는지 본다 — check_site.py가 쓴다.

누르면 그 이름의 제목이 보여야 한다. 셋을 잡는다.
- anchor-target (FLOOR): 그런 id가 없다.
- anchor-heading (FLOOR): 도착한 구획에 눈에 보이는 제목이 없다(화면 읽기 전용 .sr 제목만 있는 것 포함).
- anchor-label (NOTE): 링크 글자와 도착한 제목이 한 낱말도 겹치지 않는다(「수업 시간 보기」 → 「초등학생」).
"""

from __future__ import annotations

import re

HEADINGS = {"h1", "h2", "h3", "h4", "h5", "h6"}
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr"}
NO_HEADING_NEEDED = {"main", "body"}  # 본문 건너뛰기 링크의 도착점
HIDDEN_CLASSES = {"sr", "sr-only", "visually-hidden"}
LINK_FILLER = re.compile(r"보기|바로\s*가기|알아보기|더\s*보기|자세히|확인하기|→|›|»")


def _pairs(text: str) -> set[str]:
    s = re.sub(r"\s+", "", text)
    return {s[i:i + 2] for i in range(len(s) - 1)}


class AnchorTracker:
    def __init__(self) -> None:
        self.links: list[dict] = []
        self.targets: dict[str, dict] = {}
        self.open: list[dict] = []
        self.link: dict | None = None
        self.heading: dict | None = None

    def start(self, tag: str, a: dict[str, str], line: int) -> None:
        href = a.get("href", "")
        if tag == "a" and href.startswith("#") and len(href) > 1:
            self.link = {"target": href[1:], "line": line, "text": ""}
            self.links.append(self.link)
        for entry in self.open:
            if entry["tag"] == tag:
                entry["depth"] += 1
        if a.get("id") and tag not in VOID:
            entry = {"tag": tag, "depth": 1, "heading": None}
            self.targets.setdefault(a["id"], entry)
            self.open.append(entry)
        if tag in HEADINGS:
            hidden = bool(HIDDEN_CLASSES & set(a.get("class", "").split()))
            self.heading = {"text": "", "hidden": hidden}

    def data(self, text: str) -> None:
        if self.link is not None:
            self.link["text"] += text
        if self.heading is not None:
            self.heading["text"] += text

    def end(self, tag: str) -> None:
        if tag == "a":
            self.link = None
        if tag in HEADINGS and self.heading is not None:
            h = self.heading
            self.heading = None
            if not h["hidden"] and h["text"].strip():
                for entry in self.open:
                    if entry["heading"] is None:
                        entry["heading"] = " ".join(h["text"].split())
        for entry in self.open:
            if entry["tag"] == tag:
                entry["depth"] -= 1
        self.open = [e for e in self.open if e["depth"] > 0]

    def report(self, path: str, report) -> None:
        for link in self.links:
            target = self.targets.get(link["target"])
            text = " ".join(link["text"].split())
            if target is None:
                report.add("FLOOR", path, link["line"], "anchor-target",
                           f'「{text}」 goes to #{link["target"]}, which does not exist')
            elif target["tag"] in NO_HEADING_NEEDED:
                continue
            elif target["heading"] is None:
                report.add("FLOOR", path, link["line"], "anchor-heading",
                           f'「{text}」 lands on #{link["target"]} with no visible heading')
            elif text and not (_pairs(LINK_FILLER.sub("", text)) & _pairs(target["heading"])):
                report.add("NOTE", path, link["line"], "anchor-label",
                           f'「{text}」 lands on heading 「{target["heading"]}」')
