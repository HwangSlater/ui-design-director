#!/usr/bin/env python3
"""보내기 전 점검 — 프로젝트 폴더를 읽고, 새 세션이 규칙을 알고도 의뢰인이 짚은 뒤에야 고치던 것을 이름으로 알린다.

사용: python preflight.py <프로젝트 폴더>
  읽는 것: concept-brief.md · SITE-PLAN.md · DESIGN.md · formats/(참고 캡처·jobs*.json·뼈대 표) · layouts/ · mockups/
  있는 파일만 본다 — 단계가 앞이면 그 단계 것만 걸린다. 걸린 게 있으면 끝 코드 1.

왜 글이 아니라 도구인가(사용자 2026-11-04): 스킬 글이 길어질수록 새 세션이 놓친다. 마당집 카페 역할극에서
의뢰인이 말한 인스타·네이버를 참고에서 빠뜨림, 참고 공통점을 물어봐야 말함, 사장님 들어가기·폰 분실 화면 빠짐,
같은 크기 채운 단추·선 단추 한 쌍을 시안까지 끌고 감 — 넷 다 규칙은 있었다.
"""

from __future__ import annotations

import re
import sys
from html.parser import HTMLParser
from pathlib import Path

# 의뢰인 글에 나오는 말 → 참고·시안에서 찾을 주소 조각
CHANNELS = {
    "인스타": ("instagram", ["instagram.com", "ig-"]),
    "네이버": ("naver", ["naver.com", "naver.me", "np-"]),
    "카카오": ("kakao", ["kakao", "pf.kakao"]),
    "당근": ("daangn", ["daangn", "karrot"]),
    "유튜브": ("youtube", ["youtube.com", "youtu.be"]),
    "블로그": ("blog", ["blog.naver", "tistory", "brunch"]),
}
OWNER_WORDS = re.compile(r"사장님 화면|관리 화면|관리자|사장님이 (고치|바꾸|올리)")
LOGIN_WORDS = re.compile(r"들어가기|로그인|문자로 온|인증 번호|비밀번호")
LOST_WORDS = re.compile(r"잃어버|분실|폰을 바꾸|비밀번호를 잊|비밀번호 찾기")
COUNT_MARK = re.compile(r"\d+\s*/\s*\d+\s*곳|\(\d+/\d+\)")
SKELETON_HEAD = re.compile(r"# 뼈대 비교 — (\d+)px")
BTN_CLASS = re.compile(r"\b(btn|button|cta)\b", re.I)
WORK_PAGE = re.compile(r"owner|admin|login|code|lost|confirm|check|404|not-found", re.I)  # 확인 창·오류 화면의 두 단추는 정상
SKIP = {"node_modules", ".git", "__pycache__", "cap", "captures", "blind"}


def read(p: Path) -> str:
    return p.read_text(encoding="utf-8", errors="replace") if p.is_file() else ""


def files(root: Path, pattern: str) -> list[Path]:
    return [p for p in root.rglob(pattern) if p.is_file() and not SKIP & set(p.parts)] if root.is_dir() else []


NEGATED = re.compile(r"^[^.\n]{0,8}(안 ?해|안 ?써|없어|없음|안 함|안 씀)")  # 「인스타는 안 해요」·「인스타 없음」은 쓰지 않는다는 말 — 한 번이라도 그렇게 말했으면 그 채널은 뺀다(분식집 역할극에서 잘못 걸림)


def client_channels(text: str) -> list[str]:
    found = []
    for k in CHANNELS:
        spots = [m.end() for m in re.finditer(k, text)]
        if spots and not any(NEGATED.match(text[e:]) for e in spots):
            found.append(k)
    return found


class ButtonPairs(HTMLParser):
    """같은 부모 안에 단추 모양 링크·단추가 딱 둘 나란히 있는 곳 — 채운 것과 선만 있는 것의 같은 크기 쌍."""

    def __init__(self) -> None:
        super().__init__()
        self.stack: list[list[str]] = [[]]
        self.pairs: list[tuple[int, str]] = []

    def handle_starttag(self, tag, attrs):
        cls = dict(attrs).get("class") or ""
        if tag in ("a", "button") and BTN_CLASS.search(cls):
            self.stack[-1].append(cls)
        if tag not in ("br", "img", "input", "meta", "link", "hr", "source", "wbr"):
            self.stack.append([])

    def handle_endtag(self, tag):
        if len(self.stack) > 1 and tag not in ("br", "img", "input", "meta", "link", "hr", "source", "wbr"):
            kids = self.stack.pop()
            if len(kids) == 2 and kids[0] != kids[1]:
                self.pairs.append((self.getpos()[0], " / ".join(kids)))


def check(root: Path) -> list[str]:
    out: list[str] = []
    brief = read(root / "concept-brief.md")
    plan = read(root / "SITE-PLAN.md")
    design = read(root / "DESIGN.md")
    said = brief + plan
    formats = root / "formats"
    known = ["concept-brief.md", "formats", "DESIGN.md", "SITE-PLAN.md", "layouts", "mockups"]
    if not any((root / k).exists() for k in known):
        return [f"폴더 구조 다름: {', '.join(known)} 중 아무것도 없음 — SKILL.md § Durable outputs 의 이름으로 두어야 이 점검이 돈다(지금은 아무것도 보지 못함)"]

    # 1. 의뢰인이 말한 채널이 참고에 있는가
    if formats.is_dir():
        ref_text = " ".join(str(p.name) for p in files(formats, "*")) + " ".join(read(p) for p in files(formats, "jobs*.json"))
        for name in client_channels(said):
            if not any(s in ref_text for s in CHANNELS[name][1]):
                out.append(f"참고 빠짐: 의뢰인이 「{name}」를 말했는데 참고 캡처·jobs 에 {CHANNELS[name][0]} 화면이 없음 — 손님이 실제로 보는 그 화면을 참고에 넣을 것")

        # 2. 공통점 — 뼈대 표(폰·컴퓨터)와 n/N곳 기록
        widths = {m.group(1) for p in files(formats, "*.md") for m in [SKELETON_HEAD.search(read(p))] if m}
        if files(formats, "*.jpg") or files(formats, "*.png"):
            for w, label in (("390", "폰"), ("1280", "컴퓨터")):
                if w not in widths:
                    out.append(f"공통점 빠짐: formats/ 에 {label}({w}px) 뼈대 표가 없음 — node scripts/skeleton.mjs 로 재고 의뢰인에게 먼저 말할 것")
            if design and not COUNT_MARK.search(design):
                out.append("공통점 빠짐: DESIGN.md 에 「n/N곳」으로 센 참고 공통점이 없음 — 묻기 전에 어느 공통점을 왜 썼는지 적고 말할 것")

    # 2b. 부품 출처 — 부품 모양을 스킬 예시가 아니라 이번 참고·가게 물건에서 골랐는지(카페·분식집이 같은 부품으로 나옴)
    if files(root / "layouts", "*.html") and design and "부품 출처" not in design:
        out.append("부품 출처 빠짐: DESIGN.md 에 「부품 출처」(부품 → 모양 → 참고 n/N곳 또는 가게 물건)가 없음 — 이름·영업 상태·연락·알림·메뉴·찾아오는 길 모양을 이번 참고에서 골랐는지 적을 것")

    # 3. 사장님 화면이 있으면 들어가기·폰 분실
    if OWNER_WORDS.search(said) and plan:  # 계획을 쓰기 전에는 묻지 않는다
        if not LOGIN_WORDS.search(plan):
            out.append("사장님 화면 빠짐: SITE-PLAN.md 에 들어가는 방법(문자 번호·로그인)이 없음")
        if not LOST_WORDS.search(plan):
            out.append("사장님 화면 빠짐: SITE-PLAN.md 에 폰을 잃어버렸을 때 할 일이 없음")
        mock_html = " ".join(read(p) for p in files(root / "mockups", "*.html"))
        if mock_html:
            if not LOGIN_WORDS.search(mock_html):
                out.append("사장님 화면 빠짐: mockups/ 에 들어가기 화면이 없음")
            if not LOST_WORDS.search(mock_html):
                out.append("사장님 화면 빠짐: mockups/ 에 폰 분실 안내가 없음")

    # 4. 시안에 의뢰인이 말한 채널 연결이 있는가
    pages = list((root / "mockups").glob("*.html")) if (root / "mockups").is_dir() else []  # 시안 쪽이 생긴 뒤에만(공유 부품만 있을 때는 묻지 않음)
    mock_html = " ".join(read(p) for pat in ("*.html", "*.js") for p in files(root / "mockups", pat)) if pages else ""
    if mock_html:
        for name in client_channels(brief):
            if not any(s in mock_html for s in CHANNELS[name][1] if "." in s or s == "kakao"):
                out.append(f"연결 빠짐: 의뢰인이 「{name}」를 말했는데 시안에 {CHANNELS[name][0]} 연결이 없음(견본 주소라도 자리를 둘 것)")

    # 5. 같은 크기 단추 한 쌍(채운 것 + 선)
    for folder in ("layouts", "mockups"):
        for p in files(root / folder, "*.html"):
            if WORK_PAGE.search(p.name):
                continue
            bp = ButtonPairs()
            bp.feed(read(p))
            for line, cls in bp.pairs[:1]:  # 한 파일에 하나만 — 같은 부품이 반복될 뿐
                out.append(f"단추 한 쌍: {p.relative_to(root)}:{line} ({cls}) — 같은 크기 채운·선 단추 쌍은 키트 티. 연락 수단을 참고들이 어떻게 놓는지 보고 고를 것")
    return out


def main(argv: list[str]) -> int:
    for s in (sys.stdout, sys.stderr):
        s.reconfigure(errors="replace")
    if len(argv) != 1 or not Path(argv[0]).is_dir():
        print(__doc__.strip(), file=sys.stderr)
        return 2
    found = check(Path(argv[0]))
    for f in found:
        print(f"- {f}")
    print(f"걸린 것 {len(found)}" if found else "걸린 것 없음")
    return 1 if found else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
