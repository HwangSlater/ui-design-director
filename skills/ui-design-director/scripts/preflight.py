#!/usr/bin/env python3
"""보내기 전 점검 — 프로젝트 폴더를 읽고, 새 세션이 규칙을 알고도 의뢰인이 짚은 뒤에야 고치던 것을 이름으로 알린다.

사용: python preflight.py <프로젝트 폴더>
  읽는 것: concept-brief.md · SITE-PLAN.md · DESIGN.md · formats/(참고 캡처·jobs*.json·뼈대 표) · layouts/ · mockups/
  있는 파일만 본다 — 단계가 앞이면 그 단계 것만 걸린다. 걸린 게 있으면 끝 코드 1.
  시안 폴더에는 check_site.py 를 다시 돌려 FLOOR·DRIFT 를 함께 알리고(점검 뒤 고친 것까지), compose_metrics.mjs 의
  구성-기록.json 에서 미달 뒤 비교 사이트를 바꾼 곳을 「비교 사이트를 바꿈」으로 알린다.

왜 글이 아니라 도구인가(사용자 2026-11-04): 스킬 글이 길어질수록 새 세션이 놓친다. 마당집 카페 역할극에서
의뢰인이 말한 인스타·네이버를 참고에서 빠뜨림, 참고 공통점을 물어봐야 말함, 사장님 들어가기·폰 분실 화면 빠짐,
같은 크기 채운 단추·선 단추 한 쌍을 시안까지 끌고 감 — 넷 다 규칙은 있었다.
"""

from __future__ import annotations

import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import check_site  # noqa: E402  (접근성 바닥·토큰 어긋남은 check_site.py 하나로 — 마지막 점검 뒤 고친 것도 보낼 때 다시 잡게)
import copy_check  # noqa: E402  (베낀 티 판단은 copy_check.py 하나로)
import fonts  # noqa: E402  (AI 글꼴 판단은 fonts.py 하나로)
import facts  # noqa: E402
import site_shape  # noqa: E402  (메인 페이지 짜임 — 메뉴 내려 담기·구역 수·번호 단계·첫 화면 글상자·원 안 글자·아이콘 줄)
from common import TOOL_DIRS, mock_dir, read, utf8_console  # noqa: E402  (read 는 권한 오류에도 빈 글 — stage.read 와 같게)

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
SKIP = TOOL_DIRS | {"cap", "captures", "blind"}
HISTORY_NAME = "구성-기록.json"  # compose_metrics.mjs 가 결과 .md 옆에 쌓는 기록(같은 이름을 쓴다)
SITE_LINES_MAX = 20  # check_site 결과를 이보다 많이 늘어놓지 않는다(나머지는 수만)


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
    known = ["concept-brief.md", "formats", "DESIGN.md", "SITE-PLAN.md", "layouts", "mockups", "mockup"]
    if not any((root / k).exists() for k in known):
        return [f"폴더 구조 다름: {', '.join(known)} 중 아무것도 없음 — SKILL.md § Project folder 의 이름으로 두어야 이 점검이 돈다(지금은 아무것도 보지 못함)"]

    # 의뢰인이 말한 채널(네이버 플레이스·인스타)은 참고·후보가 아니다 — 시안에서 그리로 보내는 연결만 본다(아래 「연결 빠짐」).
    # 예전엔 참고에 넣으라고 했다가 보기 화면에 네이버 지도 화면이 후보로 올라왔다(애견미용 18차, 사용자 「빼야 하지 않을까」)
    if formats.is_dir():
        # 공통점 — 뼈대 표(폰·컴퓨터)와 n/N곳 기록
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
    # 2c. 바탕 — 의뢰인이 고른 템플릿 하나의 디자인·레이아웃을 따르고, 관련 사이트 여럿이 다르게 하는 곳만 바꾼다(사용자 2026-11-05).
    # 공통점만으로 짜니 카페·분식집·구제 가게가 같은 평균 웹사이트로 나왔다.
    if files(root / "layouts", "*.html") and design and "바탕에서 바꾼 곳" not in design:
        out.append("바탕 빠짐: DESIGN.md 에 「바탕에서 바꾼 곳」이 없음 — 의뢰인이 고른 템플릿(바탕) 이름과, skeleton.mjs --base 가 뽑은 바꿀 곳 중 고른 것·뺀 것을 n/N과 함께 적을 것")

    # 3. 사장님 화면이 있으면 들어가기·폰 분실
    if OWNER_WORDS.search(said) and plan:  # 계획을 쓰기 전에는 묻지 않는다
        if not LOGIN_WORDS.search(plan):
            out.append("사장님 화면 빠짐: SITE-PLAN.md 에 들어가는 방법(문자 번호·로그인)이 없음")
        if not LOST_WORDS.search(plan):
            out.append("사장님 화면 빠짐: SITE-PLAN.md 에 폰을 잃어버렸을 때 할 일이 없음")
        mock_html = " ".join(read(p) for p in files(mock_dir(root), "*.html"))
        if mock_html:
            if not LOGIN_WORDS.search(mock_html):
                out.append("사장님 화면 빠짐: mockups/ 에 들어가기 화면이 없음")
            if not LOST_WORDS.search(mock_html):
                out.append("사장님 화면 빠짐: mockups/ 에 폰 분실 안내가 없음")

    # 4. 시안에 의뢰인이 말한 채널 연결이 있는가
    pages = list((mock_dir(root)).glob("*.html")) if (mock_dir(root)).is_dir() else []  # 시안 쪽이 생긴 뒤에만(공유 부품만 있을 때는 묻지 않음)
    mock_html = " ".join(read(p) for pat in ("*.html", "*.js") for p in files(mock_dir(root), pat)) if pages else ""
    if mock_html:
        for name in client_channels(brief):
            if not any(s in mock_html for s in CHANNELS[name][1] if not s.endswith("-")):  # 「ig-」「np-」은 캡처 파일 이름 조각 — 시안 주소에는 안 씀(점 없는 daangn 이 빠지던 것)
                out.append(f"연결 빠짐: 의뢰인이 「{name}」를 말했는데 시안에 {CHANNELS[name][0]} 연결이 없음(견본 주소라도 자리를 둘 것)")

    # 5. 같은 크기 단추 한 쌍(채운 것 + 선)
    for folder in (root / "layouts", mock_dir(root)):
        for p in files(folder, "*.html"):
            if WORK_PAGE.search(p.name):
                continue
            bp = ButtonPairs()
            bp.feed(read(p))
            for line, cls in bp.pairs[:1]:  # 한 파일에 하나만 — 같은 부품이 반복될 뿐
                out.append(f"단추 한 쌍: {p.relative_to(root)}:{line} ({cls}) — 같은 크기 채운·선 단추 쌍은 키트 티. 연락 수단을 참고들이 어떻게 놓는지 보고 고를 것")

    # 5b. 베낀 티 — 짜임은 바탕을 따라도 되지만 첫 화면 색·마감까지 같으면 바탕 사이트로 보였다(NBA 11차)
    out += copy_check.check_project(root)

    # 6. AI 글꼴 — 기억으로 고른 글꼴은 늘 같은 기본 글꼴이었다(10차·재연 둘 다). 판단은 fonts.py 하나로
    allowed = fonts.client_fonts(root)
    for folder in (root / "palette", root / "layouts", mock_dir(root)):
        for pat in ("*.html", "*.css", "*.json"):
            for p in files(folder, pat):
                if p.name == "decision.json":
                    continue
                hits = fonts.ai_fonts_in(read(p), allowed)
                if hits:
                    out.append(f"AI 글꼴: {p.relative_to(root)} — {', '.join(hits)} · references/fonts.md 대로 fonts.py pick 에서 고를 것")
    out += site_checks(mock_dir(root), root)
    out += site_shape.check_project(root)
    out += facts.check_project(root)  # 의뢰인이 준 값이 시안에 다 있나(네일 43차 「하루 7명」을 뺐다)
    out += probe_lines(root)
    out += changed_refs(root)
    return out


def probe_lines(root: Path) -> list[str]:
    """바탕과 우리 시안을 같은 브라우저로 띄워 짜임 특징을 견준다(page_probe.mjs) — 세 쪽 비교와 같은 잣대.
    점검은 HTML·캡처로, 판정은 화면으로 재서 점검은 통과하고 판정에서 떨어졌다(빵집 32~36차). UIDD_NO_PROBE=1 이면 건너뛴다(시험)."""
    import os
    import shutil
    import subprocess
    if os.environ.get("UIDD_NO_PROBE") or not (mock_dir(root) / "index.html").is_file() or not shutil.which("node"):
        return []
    r = subprocess.run(["node", str(Path(__file__).resolve().parent / "page_probe.mjs"), "--check", str(root)],
                       capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=600)
    return [line for line in r.stdout.splitlines() if line.startswith("DRIFT ")]


def site_checks(mock: Path, root: Path) -> list[str]:
    """시안 폴더에 check_site.py 를 다시 돌린 FLOOR·DRIFT — 점검을 돌린 뒤 고친 곳이 새로 어긋나도 보내기 전에 잡는다."""
    if not files(mock, "*.html"):
        return []
    found = [f for f in check_site.run(mock).findings if f.tier in ("FLOOR", "DRIFT")]
    found.sort(key=lambda f: (f.tier != "FLOOR", f.path, f.line))
    where = mock.relative_to(root).as_posix()
    out = [f"{f.tier} {where}/{Path(f.path).as_posix()}:{f.line} {f.rule} — {f.message}" for f in found[:SITE_LINES_MAX]]
    if len(found) > SITE_LINES_MAX:
        out.append(f"FLOOR·DRIFT 그 밖 {len(found) - SITE_LINES_MAX}개 — python check_site.py {where} 로 전부 볼 것")
    return out


def changed_refs(root: Path) -> list[str]:
    """같은 폭의 구성 비교에서 미달이 나온 뒤 기준 사이트를 바꿨는가 — 기준을 바꿔 통과시키면 의뢰인에게 까닭을 말해야 한다."""
    out = []
    for hist in files(root, HISTORY_NAME):
        try:
            runs = json.loads(read(hist) or "[]")
        except json.JSONDecodeError:
            continue
        by_width: dict[str, list[dict]] = {}
        for r in runs if isinstance(runs, list) else []:
            if isinstance(r, dict):
                by_width.setdefault(str(r.get("width")), []).append(r)
        for width, rs in by_width.items():
            first = next((i for i, r in enumerate(rs) if isinstance(r.get("short"), int) and r["short"] > 0), None)
            if first is None or first == len(rs) - 1:
                continue
            pair = (rs[first], rs[-1])
            sites = [[s for s in r.get("sites") or [] if isinstance(s, dict)] for r in pair]
            if {s.get("url") for s in sites[0]} != {s.get("url") for s in sites[1]}:
                names = [", ".join(str(s.get("name", "")) for s in group) for group in sites]
                # compose_metrics.mjs --why 로 적은 까닭(가장 최근 것). 있으면 그 까닭을 의뢰인에게 그대로 말한다
                why = next((str(r["why"]).strip() for r in reversed(rs[first + 1:]) if str(r.get("why") or "").strip()), "")
                tail = (f"적은 까닭: 「{why}」 — 이 까닭을 의뢰인에게 말할 것" if why
                        else "왜 바꿨는지 의뢰인에게 말할 것(기준을 바꿔 통과시킨 것으로 보인다)")
                out.append(f"비교 사이트를 바꿈: {hist.relative_to(root).as_posix()} {width}px — 미달이 나온 뒤 기준이 「{names[0]}」에서 "
                           f"「{names[1]}」로 바뀜. {tail}")
    return out


def main(argv: list[str]) -> int:
    utf8_console()
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
