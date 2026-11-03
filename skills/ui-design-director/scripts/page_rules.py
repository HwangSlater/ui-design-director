"""한 페이지의 제목·머리글·사진·문구를 모아 사람이 리뷰에서 잡던 실수를 찾는다 — check_site.py가 쓴다.

- title-option-label (FLOOR): 탭 제목이 화면 이름이 아니라 배치 안 이름이다(「목록 2 거르기 칩 고정」).
- repeated-heading (FLOOR): 같은 제목이 한 페이지에 두 번, 또는 h1과 아래 h2가 앞부분이 거의 같다.
- photo-reused-across-pages (DRIFT): 같은 사진 파일이 다른 역할로 여러 페이지·한 페이지에 두 번 쓰였다.
- date-weekday (FLOOR): 「11월 19일 수요일」처럼 날짜와 요일이 안 맞는다(페이지의 「2026년」, 없으면 올해·내년 기준).
- unsourced-rule (NOTE): 「안 돼요」「불가」「못 해요」 같은 가게 규칙 말투 — 사용자가 준 규칙인지 확인(빵집 시안에 「영어·이모티콘은 안 돼요」를 지어 넣었다).
- unsourced-duration (NOTE): 「보통」「3일 안에」 같은 걸리는 시간 짐작이 견본 표시 없이 들어 있다.
"""

from __future__ import annotations

import datetime as dt
import re
from urllib.parse import unquote, urlsplit

VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr"}
HEADINGS = {"h1", "h2", "h3"}
HIDDEN_CLASSES = {"sr", "sr-only", "visually-hidden"}
MARKER_CLASSES = {"sample"}  # 「견본」「확인 필요」 표시: 사용자가 준 사실이 아니라고 이미 밝힌 자리
MARKER_WORDS = ("견본", "확인 필요")

# 탭 제목 판단. 「 · 」「 | 」「 - 」로 나눈 조각마다 본다. 화면 이름은 「입양」「보리 입양 신청」처럼
# 낱말만으로 되고, 배치 안 이름은 번호가 붙는다. 그래서 (1) 숫자+띄어쓰기로 시작(「2 아이들 먼저」),
# (2) 낱말 뒤에 홀로 선 한 자리 숫자(「목록 2」「상세 1 이름 먼저」 — 「2024년」「3마리」처럼 단위가 붙으면 아님),
# (3) 「시안」「1안」「A안」, 영어 option/layout/variant/draft 낱말만 잡는다.
TITLE_SPLIT = re.compile(r"\s+[·|–—-]\s+")
TITLE_OPTION_PATTERNS = [
    re.compile(r"^\d{1,2}\s+\S"),
    re.compile(r"[가-힣A-Za-z]\s+\d(?=\s|$|[(（])"),
    re.compile(r"시안|(?:^|\s)(?:\d|[A-Z])안(?=\s|$)"),
    re.compile(r"\b(?:option|layout|variant|draft)\b", re.IGNORECASE),
]

MIN_SHARED_HANGUL = 6  # h1과 h2 앞부분이 한글 6자 넘게 같으면 같은 말을 두 번 한 것

# 사진 역할. 목록 카드·작은 그림·그 아이 자기 사진첩에서 같은 사진이 다시 나오는 것은 당연하다.
# 이런 class 낱말이 사진이나 그 조상에 있으면 「카드 자리」로 본다. 나머지(첫 화면·문·소개 사진)는 「큰 자리」.
CARD_CLASS_WORDS = ("pet", "card", "thumb", "mini", "row", "item", "avatar", "media", "gallery", "photos", "gph")
CARD_CLASS_TOKENS = {"th"}
PHOTO_MIN_PAGES = 3
SIZE_PREFIX = re.compile(r"^\d+px-")  # 위키미디어 썸네일 「1280px-이름.jpg」

# 걸리는 시간·빈도 짐작. 사용자가 준 사실이면 그대로 두고, 아니면 견본 표시를 붙이거나 지운다.
DURATION_PATTERNS = [
    re.compile(r"(?<![가-힣])보통(?!의)"),
    re.compile(r"\d+\s*(?:분|시간|일|주|개월|달)\s*(?:쯤|정도|안에|이내|내외|만에)"),
    re.compile(r"(?:몇|한두|두세|며칠)\s*(?:분|시간|일|주|달)?\s*(?:쯤|정도|안에|이내)"),
]
SNIPPET_RADIUS = 24

# 가게 규칙 말투. 사용자가 준 규칙이면 그대로 두고, 아니면 지운다 — 견본 표시로도 덮지 않는다(손님이 그대로 믿는다)
RULE_PATTERNS = [re.compile(r"(?:안|못)\s*(?:돼요|됩니다|해요|합니다)(?![가-힣])"), re.compile(r"불가(?:능)?(?:해요|합니다)?"), re.compile(r"금지")]

# 날짜와 요일: 의뢰인이 준 견본 문구 「11월 19일 수요일」이 2026년엔 목요일이었다
DATE_WEEKDAY = re.compile(r"(\d{1,2})월\s*(\d{1,2})일\s*\(?([월화수목금토일])(?:요일|\))")
YEAR = re.compile(r"(20\d\d)년")
WEEKDAYS = "월화수목금토일"


def _classes(a: dict[str, str]) -> list[str]:
    return a.get("class", "").lower().split()


def _norm(text: str) -> str:
    return " ".join(text.split())


def photo_key(src: str) -> str:
    """주소에서 쿼리·경로·크기 앞붙이를 떼어 파일 이름만 남긴다."""
    name = unquote(urlsplit(src).path.rsplit("/", 1)[-1]).lower()
    return SIZE_PREFIX.sub("", name)


def title_looks_like_option(title: str) -> bool:
    return any(p.search(part) for part in TITLE_SPLIT.split(title) for p in TITLE_OPTION_PATTERNS)


def shared_hangul_prefix(a: str, b: str) -> int:
    a, b = re.sub(r"\s+", "", a), re.sub(r"\s+", "", b)
    n = 0
    while n < min(len(a), len(b)) and a[n] == b[n]:
        n += 1
    return len(re.findall(r"[가-힣]", a[:n]))


class PageTracker:
    def __init__(self) -> None:
        self.stack: list[dict] = []
        self.title: str | None = None
        self.title_line = 1
        self.in_title = False
        self.in_body = False
        self.heading: dict | None = None
        self.headings: list[dict] = []
        self.photos: list[tuple[str, int, bool]] = []  # (파일, 줄, 카드 자리인가)
        self.durations: list[dict] = []
        self.rules: list[dict] = []
        self.marker_depth = 0
        self.dated: list[tuple[int, int, str, int]] = []  # (월, 일, 요일, 줄)
        self.years: set[int] = set()

    def start(self, tag: str, a: dict[str, str], line: int) -> None:
        classes = _classes(a)
        if tag == "title":
            self.in_title, self.title, self.title_line = True, "", line
        elif tag == "body":
            self.in_body = True
        if tag == "img" and a.get("src"):
            self.photos.append((photo_key(a["src"]), line, self._in_card(classes)))
        if tag in HEADINGS and not (HIDDEN_CLASSES & set(classes)):
            self.heading = {"tag": tag, "line": line, "text": ""}
        is_marker = bool(MARKER_CLASSES & set(classes))
        if is_marker and self.stack:
            self.stack[-1]["marker"] = True
        if tag in VOID:
            return
        parent = self.stack[-1] if self.stack else None
        self.stack.append({"tag": tag, "classes": classes, "line": line, "text": "",
                           "marker": is_marker, "parent": parent, "is_marker": is_marker})
        if is_marker:
            self.marker_depth += 1

    def _in_card(self, own: list[str]) -> bool:
        names = own + [c for e in self.stack for c in e["classes"]]
        return any(c in CARD_CLASS_TOKENS or any(w in c for w in CARD_CLASS_WORDS) for c in names)

    def data(self, text: str) -> None:
        if self.in_title:
            self.title += text
            return
        if self.marker_depth:
            return  # 견본 표시 글자는 제목·문구 비교에서 뺀다
        if self.heading is not None:
            self.heading["text"] += text
        if self.in_body and self.stack:
            self.stack[-1]["text"] += text
            if any(w in text for w in MARKER_WORDS):
                self.stack[-1]["marker"] = True

    def end(self, tag: str) -> None:
        if tag == "title":
            self.in_title = False
        if tag in HEADINGS and self.heading is not None and self.heading["tag"] == tag:
            self.heading["text"] = _norm(self.heading["text"])
            if self.heading["text"]:
                self.headings.append(self.heading)
            self.heading = None
        if not any(e["tag"] == tag for e in self.stack):
            return  # 짝이 없는 닫는 태그
        while self.stack:
            entry = self.stack.pop()
            if entry["is_marker"]:
                self.marker_depth -= 1
            text = _norm(entry["text"])
            self.years.update(int(y) for y in YEAR.findall(text))
            for m in DATE_WEEKDAY.finditer(text):
                self.dated.append((int(m.group(1)), int(m.group(2)), m.group(3), entry["line"]))
            for pattern in DURATION_PATTERNS:
                for m in pattern.finditer(text):
                    self.durations.append({"entry": entry, "text": text, "at": m.start()})
            for pattern in RULE_PATTERNS:
                for m in pattern.finditer(text):
                    self.rules.append({"entry": entry, "text": text, "at": m.start()})
            if entry["tag"] == tag:
                break

    def report(self, path: str, report) -> None:
        if self.title is not None and title_looks_like_option(_norm(self.title)):
            report.add("FLOOR", path, self.title_line, "title-option-label",
                       f"<title> 「{_norm(self.title)}」 reads like a layout option, not the page's heading")
        self._report_headings(path, report)
        self._report_weekdays(path, report)
        self._report_rules(path, report)
        for d in self.durations:
            entry = d["entry"]
            if entry["marker"] or (entry["parent"] and entry["parent"]["marker"]):
                continue
            lo = max(0, d["at"] - SNIPPET_RADIUS)
            snippet = d["text"][lo:d["at"] + SNIPPET_RADIUS]
            report.add("NOTE", path, entry["line"], "unsourced-duration",
                       f"「{snippet}」 — a time or frequency guess with no 견본 mark; keep only if the user gave it")

    def _report_rules(self, path: str, report) -> None:
        seen = set()
        for r in self.rules:
            lo = max(0, r["at"] - SNIPPET_RADIUS)
            snippet = r["text"][lo:r["at"] + SNIPPET_RADIUS // 2]
            if snippet in seen:
                continue
            seen.add(snippet)
            report.add("NOTE", path, r["entry"]["line"], "unsourced-rule",
                       f"「{snippet}」 — a shop rule; keep only if the user gave it (a 견본 mark does not make an invented rule safe)")

    def _report_weekdays(self, path: str, report) -> None:
        this_year = dt.date.today().year
        years = sorted(self.years) or [this_year, this_year + 1]
        seen = set()
        for mon, d, wd, line in self.dated:
            if (mon, d, wd) in seen:
                continue
            seen.add((mon, d, wd))
            real = []
            for y in years:
                try:
                    real.append(WEEKDAYS[dt.date(y, mon, d).weekday()])
                except ValueError:
                    continue  # 2월 30일 같은 없는 날
            if real and wd not in real:
                report.add("FLOOR", path, line, "date-weekday",
                           f"「{mon}월 {d}일 {wd}요일」 — that date is a {'/'.join(real)}요일 in {'/'.join(map(str, years))}; compute the weekday from the date")

    def _report_headings(self, path: str, report) -> None:
        seen: dict[str, int] = {}
        for h in self.headings:
            if h["text"] in seen:
                report.add("FLOOR", path, h["line"], "repeated-heading",
                           f"「{h['text']}」 already used as a heading on line {seen[h['text']]}")
            else:
                seen[h["text"]] = h["line"]
        firsts = [h for h in self.headings if h["tag"] == "h1"][:1]
        for top in firsts:
            for h in self.headings:
                if h["tag"] == "h1" or h["line"] < top["line"] or h["text"] == top["text"]:
                    continue
                if shared_hangul_prefix(top["text"], h["text"]) >= MIN_SHARED_HANGUL:
                    report.add("FLOOR", path, h["line"], "repeated-heading",
                               f"「{h['text']}」 repeats the page title 「{top['text']}」 (line {top['line']})")


def report_photo_reuse(pages: dict[str, list[tuple[str, int, bool]]], report) -> None:
    """같은 사진이 큰 자리에서 한 페이지 두 번, 또는 3개 넘는 페이지에 나오면서 한 번이라도 큰 자리면 알린다."""
    by_photo: dict[str, dict[str, list[tuple[int, bool]]]] = {}
    for path, photos in pages.items():
        for key, line, card in photos:
            if key:
                by_photo.setdefault(key, {}).setdefault(path, []).append((line, card))
    for key, uses in sorted(by_photo.items()):
        for path, here in uses.items():
            large = [line for line, card in here if not card]
            if len(large) >= 2:
                report.add("DRIFT", path, large[1], "photo-reused-across-pages",
                           f"{key} shown twice on this page (line {large[0]}) outside a card")
        large_pages = sorted(p for p, here in uses.items() if any(not card for _, card in here))
        if len(uses) >= PHOTO_MIN_PAGES and large_pages:
            path = large_pages[0]
            line = next(line for line, card in uses[path] if not card)
            report.add("DRIFT", path, line, "photo-reused-across-pages",
                       f"{key} used on {len(uses)} pages ({', '.join(sorted(uses))}), as a large photo here — "
                       "a sample photo should appear once in the flow")
