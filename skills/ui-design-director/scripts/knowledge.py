#!/usr/bin/env python3
"""디자인 지식 꺼내 보기 — 실제 디자이너·연구 기관의 규칙 약 630개(assets/knowledge/rules.json)에서 지금 필요한 것만.

    python knowledge.py ask --part button,form [--stage main] [--field ux] [--q 예약] [--top 8]
    python knowledge.py stage <brief|board|palette|design|main|review> [--top 4]    # stage.py 가 단계 표 끝에 붙인다
    python knowledge.py show <id>                                                    # 한 규칙의 근거·출처 전부
    python knowledge.py parts                                                        # 쓸 수 있는 부품 이름
    부품 이름은 한국어로도 된다: --part 단추,입력 양식,첫 화면 (PART_ALIASES)

긴 문서(references/knowledge-*.md)를 통째로 읽으면 절마다 3천~8천 토큰이 들고, 필요한 순간에 떠올리지 못하면 안 쓰였다.
한 줄에 규칙 · 값 · 출처 이름, 끝에 자료끼리 다른 곳(있으면 바탕 값을 따른다).
"""
from __future__ import annotations

import argparse
import difflib
import json
import sys
from functools import lru_cache
from pathlib import Path

from common import utf8_console  # 콘솔 한글 깨짐 막기는 common 하나로

DATA = Path(__file__).resolve().parent.parent / "assets" / "knowledge" / "rules.json"
PRIORITY_WEIGHT = {1: 3, 2: 2, 3: 1}
# 자료가 권하는 글꼴 이름(KRDS 의 Pretendard GOV 등)이 후보처럼 읽히지 않게 — 목록은 fonts.py 와 같은 파일
AI_FONT_NAMES = tuple(n for f in json.loads((DATA.parent.parent / "fonts" / "ai-fonts.json").read_text(encoding="utf-8"))["fonts"]
                      for n in [f["name"], *f.get("aliases", [])] if len(n) > 3)
# 스킬 단계(stage.py) → 지식의 단계
STAGE_MAP = {"brief": "brief", "board": "board", "base": "board", "material": "design", "palette": "palette",
             "design": "design", "main": "main", "review": "review"}

# 한국어 부품 이름 → 규칙 표의 부품 id. 의뢰인·디자이너가 쓰는 말로 물어도 맞는 규칙이 나오게
PART_ALIASES = {
    "머리": "header", "머리글": "header", "헤더": "header", "상단": "header",
    "메뉴": "nav", "내비": "nav", "내비게이션": "nav", "네비": "nav",
    "첫 화면": "first-screen", "첫화면": "first-screen", "히어로": "first-screen",
    "바닥": "footer", "바닥글": "footer", "푸터": "footer", "하단": "footer",
    "제목": "heading", "본문": "body-text", "숫자": "numbers", "한글": "korean-text",
    "단추": "button", "버튼": "button", "링크": "link", "카드": "card",
    "폼": "form", "입력 양식": "form", "입력양식": "form", "양식": "form",
    "입력칸": "input", "입력": "input", "오류": "error-state", "에러": "error-state",
    "빈 화면": "empty-state", "빈화면": "empty-state", "불러오는 중": "loading", "로딩": "loading",
    "목록": "list", "리스트": "list", "표": "table", "테이블": "table",
    "사진": "image", "이미지": "image", "아이콘": "icon", "로고": "logo",
    "색": "colour", "색깔": "colour", "색상": "colour", "대비": "contrast", "명암비": "contrast",
    "어두운 구역": "dark-section", "어두운구역": "dark-section",
    "간격": "spacing", "여백": "spacing", "격자": "grid", "그리드": "grid", "반응형": "responsive",
    "움직임": "motion", "모션": "motion", "애니메이션": "motion", "마우스 올림": "hover", "호버": "hover",
    "문구": "copy", "카피": "copy", "신뢰": "trust", "예약": "booking",
    "쇼핑": "shop", "가게": "shop", "쇼핑몰": "shop", "접근성": "accessibility",
    "생성 티": "generated-look", "ai 티": "generated-look", "글꼴": "font-choice", "폰트": "font-choice",
    "페이지": "page", "화면": "page",
    # 자주 쓰는 영어 이름 중 id 와 다른 것
    "hero": "first-screen", "menu": "nav", "navigation": "nav", "color": "colour", "font": "font-choice",
    "typography": "font-choice", "photo": "image", "footer-nav": "footer", "body": "body-text", "text": "body-text",
    "cta": "button", "error": "error-state", "empty": "empty-state", "animation": "motion",
}


def part_ids() -> set[str]:
    return {p for r in rules() for p in r.get("parts", [])}


def resolve_parts(raw: str) -> tuple[set[str], list[str]]:
    """쉼표로 받은 부품 이름을 id 로. 한국어 이름도 받고, 모르는 이름은 따로 돌려준다."""
    ids, unknown = part_ids(), []
    out: set[str] = set()
    for name in (x.strip() for x in raw.split(",")):
        if not name:
            continue
        key = " ".join(name.lower().split())
        pid = key if key in ids else PART_ALIASES.get(key) or PART_ALIASES.get(key.replace(" ", ""))
        if pid:
            out.add(pid)
        else:
            unknown.append(name)
    return out, unknown


def nearest_parts(name: str, n: int = 4) -> list[str]:
    """모르는 부품 이름과 가까운 id — 영어 id 와 한국어 이름 모두에서 찾는다."""
    ids = sorted(part_ids())
    key = name.lower().strip()
    found = difflib.get_close_matches(key, ids, n=n, cutoff=0.4)
    for alias in difflib.get_close_matches(key, list(PART_ALIASES), n=n, cutoff=0.4):
        if PART_ALIASES[alias] not in found:
            found.append(PART_ALIASES[alias])
    found += [i for i in ids if (key in i or i in key) and i not in found]
    return found[:n]


@lru_cache(maxsize=1)
def rules() -> list[dict]:
    return json.loads(DATA.read_text(encoding="utf-8"))["rules"]


def score(r: dict, parts: set[str], stage: str | None, field: str | None, words: list[str]) -> int:
    s = PRIORITY_WEIGHT.get(r.get("priority", 2), 2)
    hit = len(parts & set(r.get("parts", [])))
    if parts and not hit:
        return -1
    s += hit * 3
    if stage:
        if stage not in r.get("stages", []):
            return -1
        s += 1
    if field and r.get("field") != field:
        return -1
    if words:
        text = " ".join(str(r.get(k, "")) for k in ("rule", "values", "why", "by")).lower()
        found = sum(w in text for w in words)
        if not found:
            return -1
        s += found * 2
    if r.get("confidence") == "sourced":
        s += 1
    return s


def line(r: dict) -> str:
    out = f"[{r['id']}] {r['rule']}"
    if r.get("values"):
        out += f" ({r['values']})"
    mark = "" if r.get("confidence") == "sourced" else f" · {'추정' if r.get('confidence') == 'inference' else '확인 안 됨'}"
    out += f" — {r.get('by', '')}{mark}"
    if any(n in r["rule"] + r.get("values", "") for n in AI_FONT_NAMES):
        out += " · 글꼴 이름은 후보 아님(fonts.py pick)"
    if r.get("conflict"):
        out += f" · 다름: {r['conflict']} → 바탕 값을 따름"
    return out


def pick(parts: set[str], stage: str | None, field: str | None, words: list[str], top: int) -> list[dict]:
    scored = [(score(r, parts, stage, field, words), i, r) for i, r in enumerate(rules())]
    scored = [x for x in scored if x[0] >= 0]
    scored.sort(key=lambda x: (-x[0], x[1]))
    seen, out = set(), []
    for _, _, r in scored:  # 같은 말을 한 규칙이 여러 출처에 있으면 한 번만
        key = r["rule"].lower()[:60]
        if key in seen:
            continue
        seen.add(key)
        out.append(r)
        if len(out) >= top:
            break
    return out


def stage_lines(stage: str, top: int = 4) -> list[str]:
    """stage.py 가 부른다 — 그 단계에서 결정을 자주 가르는 규칙 몇 개, 분야를 고루(한 분야만 나오면 나머지를 놓쳤다)."""
    if not DATA.is_file():
        return []
    st = STAGE_MAP.get(stage, stage)
    pool = [r for r in pick(set(), st, None, [], 200) if r.get("priority") == 1 and r.get("confidence") == "sourced"]
    out, fields = [], set()
    for r in pool:  # 분야마다 하나씩 먼저
        if r["field"] not in fields:
            fields.add(r["field"])
            out.append(r)
        if len(out) >= top:
            break
    return [line(r) for r in out]


def main(argv: list[str]) -> int:
    utf8_console()
    ap = argparse.ArgumentParser(description="디자인 지식 꺼내 보기")
    sub = ap.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("ask")
    a.add_argument("--part", default="", help="쉼표로: button,form,first-screen … 한국어(단추,입력 양식)도 됨(parts 로 목록)")
    a.add_argument("--stage")
    a.add_argument("--field")
    a.add_argument("--q", default="", help="낱말(영어·한국어)")
    a.add_argument("--top", type=int, default=8)
    s = sub.add_parser("stage")
    s.add_argument("stage")
    s.add_argument("--top", type=int, default=4)
    w = sub.add_parser("show")
    w.add_argument("id")
    sub.add_parser("parts")
    args = ap.parse_args(argv)
    if args.cmd == "parts":
        counts: dict[str, int] = {}
        for r in rules():
            for p in r.get("parts", []):
                counts[p] = counts.get(p, 0) + 1
        print(", ".join(f"{k} {v}" for k, v in sorted(counts.items(), key=lambda x: -x[1])))
        return 0
    if args.cmd == "show":
        r = next((r for r in rules() if r["id"] == args.id), None)
        if not r:
            print(f"없는 규칙: {args.id}", file=sys.stderr)
            return 1
        print(json.dumps(r, ensure_ascii=False, indent=1))
        return 0
    if args.cmd == "stage":
        for ln in stage_lines(args.stage, args.top):
            print(ln)
        return 0
    parts, unknown = resolve_parts(args.part)
    if unknown:
        for name in unknown:
            near = nearest_parts(name)
            hint = ", ".join(near) if near else "knowledge.py parts 로 목록을 볼 것"
            print(f"모르는 부품 이름: {name} → 가까운 이름: {hint}")
        if not parts:
            return 1
    words = [x.lower() for x in args.q.split() if x]
    found = pick(parts, STAGE_MAP.get(args.stage, args.stage) if args.stage else None, args.field, words, args.top)
    if not found:
        print("맞는 규칙 없음 — knowledge.py parts 로 부품 이름을 보거나 --q 를 바꿀 것")
        return 0
    for r in found:
        print(line(r))
    print("근거·출처: knowledge.py show <id>")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
