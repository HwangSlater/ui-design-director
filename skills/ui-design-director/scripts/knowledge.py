#!/usr/bin/env python3
"""디자인 지식 꺼내 보기 — 실제 디자이너·연구 기관의 규칙 약 630개(assets/knowledge/rules.json)에서 지금 필요한 것만.

    python knowledge.py ask --part button,form [--stage main] [--field ux] [--q 예약] [--top 8]
    python knowledge.py stage <brief|board|palette|design|main|review> [--top 4]    # stage.py 가 단계 표 끝에 붙인다
    python knowledge.py show <id>                                                    # 한 규칙의 근거·출처 전부
    python knowledge.py parts                                                        # 쓸 수 있는 부품 이름

긴 문서(references/knowledge-*.md)를 통째로 읽으면 절마다 3천~8천 토큰이 들고, 필요한 순간에 떠올리지 못하면 안 쓰였다.
한 줄에 규칙 · 값 · 출처 이름, 끝에 자료끼리 다른 곳(있으면 바탕 값을 따른다).
"""
from __future__ import annotations

import argparse
import json
import sys
from functools import lru_cache
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "assets" / "knowledge" / "rules.json"
PRIORITY_WEIGHT = {1: 3, 2: 2, 3: 1}
# 자료가 권하는 글꼴 이름(KRDS 의 Pretendard GOV 등)이 후보처럼 읽히지 않게 — 목록은 fonts.py 와 같은 파일
AI_FONT_NAMES = tuple(n for f in json.loads((DATA.parent.parent / "fonts" / "ai-fonts.json").read_text(encoding="utf-8"))["fonts"]
                      for n in [f["name"], *f.get("aliases", [])] if len(n) > 3)
# 스킬 단계(stage.py) → 지식의 단계
STAGE_MAP = {"brief": "brief", "board": "board", "base": "board", "material": "design", "palette": "palette",
             "design": "design", "main": "main", "review": "review"}


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
    for s in (sys.stdout, sys.stderr):
        s.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser(description="디자인 지식 꺼내 보기")
    sub = ap.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("ask")
    a.add_argument("--part", default="", help="쉼표로: button,form,first-screen …(parts 로 목록)")
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
    parts = {p.strip() for p in args.part.split(",") if p.strip()}
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
