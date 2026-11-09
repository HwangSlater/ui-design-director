#!/usr/bin/env python3
"""글꼴 후보 고르기와 AI 글꼴 검사 — 근거 있는 글꼴만 후보로 낸다.

    python fonts.py pick --style 명조 [--style 손글씨] [--top 8] [--kind 회사]
        assets/fonts/fonts.json(방문 상위 사이트 실측 + 회사·기관 공개, 웹 임베딩 가능)에서
        성격이 맞는 글꼴을 고른다. AI 글꼴(assets/fonts/ai-fonts.json)은 뺀다.
        차례: 상위 사이트에서 쓰는 곳 수 → 눈누 조회수. 한 줄에 이름 · 만든 곳 · 성격 · 굵기 · 조건 · 근거 · 받는 곳,
        그 아래 웹폰트 줄(눈누 「웹폰트로 사용」의 CSS 이름·굵기 — 팔레트 화면 heading·body 에 그 이름을 쓴다).
    python fonts.py face <이름>
        그 글꼴의 @font-face 전체(또는 CSS 주소)를 찍는다 — 팔레트 화면 faces·시안 CSS 에 그대로 붙인다.
    python fonts.py check <파일 또는 폴더>...
        CSS·HTML·JSON 의 글꼴 선언(font-family, --f-*, Google Fonts family=, 팔레트 화면의 heading·body)에서
        AI 글꼴을 찾는다. 있으면 종료 코드 1. 의뢰인이 이미 쓰는 글꼴은 concept-brief.md 의 「의뢰인 글꼴: 이름」으로 푼다.

글꼴 후보를 기억으로 내면 늘 같은 기본 글꼴(Pretendard·Noto·Wanted Sans·SUIT)이 나왔다 — 10차와 재연 둘 다.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from functools import lru_cache
from pathlib import Path

from common import utf8_console  # 콘솔 한글 깨짐 막기는 common 하나로

ASSETS = Path(__file__).resolve().parent.parent / "assets" / "fonts"
TEXT_SUFFIXES = {".css", ".html", ".htm", ".json", ".md", ".js"}
CLIENT_FONT = re.compile(r"의뢰인 글꼴\s*[:：]\s*(.+)")
# 글꼴 이름이 오는 자리만 본다 — 본문 글에 「Inter」 같은 낱말이 있어도 걸리지 않게
DECLS = [
    re.compile(r"font-family\s*:\s*([^;}{\n]+)", re.I),
    re.compile(r"--[\w-]*(?:font|f-)[\w-]*\s*:\s*([^;}{\n]+)", re.I),
    re.compile(r"[?&]family=([^&\"'\s)]+)"),
    re.compile(r'"(?:heading|body|family)"\s*:\s*"([^"]+)"'),
]


def norm(s: str) -> str:
    return re.sub(r"[\s_\-'\"]+", "", s).lower()


@lru_cache(maxsize=1)
def load_ai() -> tuple[dict, ...]:
    """AI 글꼴 목록 — 훅·점검이 파일마다 부르므로 한 번만 읽는다(knowledge.rules() 와 같은 방식)."""
    return tuple(json.loads((ASSETS / "ai-fonts.json").read_text(encoding="utf-8"))["fonts"])


def ai_keys(allowed: set[str] = frozenset()) -> dict[str, str]:
    """정규화한 이름 → 대표 이름. allowed(의뢰인 글꼴)는 뺀다."""
    keys = {}
    for f in load_ai():
        names = [f["name"], *f.get("aliases", [])]
        if any(norm(n) in allowed for n in names):
            continue
        for n in names:
            keys[norm(n)] = f["name"]
    return keys


FONT_SHORTHAND_SIZE = re.compile(r"^(?:[\d.]+\S*\s+)+")  # font 단축 속성 앞의 굵기·크기·행간


def family_names(value: str, shorthand: bool = False) -> list[str]:
    """글꼴 목록 값 하나(「'Inter', sans-serif」)를 이름들로. check_site.py 도 이 함수를 쓴다.
    shorthand 면 「600 16px/1.4 Inter」 같은 font 단축 속성의 앞 숫자를 걷어 낸다."""
    out = []
    for part in re.split(r"[,|]", value):
        name = part.split(":")[0].strip()
        if shorthand:
            name = FONT_SHORTHAND_SIZE.sub("", name)
        name = name.strip("'\"")
        if name and not name.startswith("var("):
            out.append(name)
    return out


def families(text: str) -> list[str]:
    out = []
    for rx in DECLS:
        for m in rx.finditer(text):
            out += family_names(m.group(1).replace("+", " ").replace("%20", " "))
    return out


def ai_fonts_in(text: str, allowed: set[str] = frozenset()) -> list[str]:
    """글꼴 선언 안의 AI 글꼴(대표 이름). guard.py 훅도 이 함수를 쓴다."""
    keys = ai_keys(allowed)
    found = []
    for fam in families(text):
        n = norm(fam)
        hit = keys.get(n) or next((v for k, v in keys.items() if n.startswith(k) and len(k) >= 4), None)
        if hit and hit not in found:
            found.append(hit)
    return found


def client_fonts(start: Path) -> set[str]:
    """프로젝트 맥락 정리에 적힌 의뢰인 글꼴(이미 쓰는 글꼴은 막지 않는다)."""
    for folder in [start, *start.parents]:
        brief = folder / "concept-brief.md"
        if brief.is_file():
            text = brief.read_text(encoding="utf-8", errors="replace")
            return {norm(n) for m in CLIENT_FONT.finditer(text) for n in re.split(r"[,·/]", m.group(1)) if n.strip()}
    return set()


def cmd_check(paths: list[str]) -> int:
    bad = 0
    for p in map(Path, paths):
        files = [f for f in p.rglob("*") if f.suffix.lower() in TEXT_SUFFIXES] if p.is_dir() else [p]
        for f in files:
            if any(part in ("snapshot", "res", "node_modules") for part in f.parts):
                continue  # 남의 사이트 사본은 보지 않는다
            hits = ai_fonts_in(f.read_text(encoding="utf-8", errors="replace"), client_fonts(f.resolve().parent))
            if hits:
                bad += 1
                print(f"AI 글꼴: {f} — {', '.join(hits)}")
    if bad:
        print(f"→ python {Path(__file__).as_posix()} pick --style <성격> 으로 근거 있는 글꼴로 바꾼다")
    return 1 if bad else 0


@lru_cache(maxsize=1)
def load_table() -> dict:
    """근거 있는 글꼴 표(assets/fonts/fonts.json) — 훅이 팔레트 화면마다 부르므로 한 번만 읽는다."""
    return json.loads((ASSETS / "fonts.json").read_text(encoding="utf-8"))


FACE_FAMILY = re.compile(r"font-family\s*:\s*['\"]?([^;'\"\n]+)", re.I)
FACE_WEIGHT = re.compile(r"font-weight\s*:\s*([\w ]+)", re.I)
FACE_SRC = re.compile(r"url\(\s*['\"]?([^'\")]+)")


def face_families(webfont: str) -> list[str]:
    """@font-face 글에 적힌 CSS 글꼴 이름들(겹친 것은 한 번). CSS 주소면 주소의 family= 이름."""
    if webfont.startswith("http"):
        return [n for m in DECLS[2].finditer(webfont) for n in family_names(m.group(1).replace("+", " "))]
    return list(dict.fromkeys(m.group(1).strip() for m in FACE_FAMILY.finditer(webfont)))


@lru_cache(maxsize=1)
def known_keys() -> frozenset[str]:
    """표에 있는 글꼴의 정규화한 이름 — 이름·다른 이름·웹폰트 CSS 이름."""
    keys = set()
    for r in load_table()["fonts"]:
        for n in [r["name"], *r.get("aliases", []), *face_families(r.get("webfont") or "")]:
            keys.add(norm(n))
    return frozenset(keys)


def palette_families(text: str) -> list[str]:
    """팔레트 화면의 글꼴 후보(<script type="application/json" id="fonts">)의 heading·body 글꼴 이름들."""
    m = re.search(r'<script[^>]*id=["\']fonts["\'][^>]*>([\s\S]*?)</script>', text, re.I)
    try:
        items = json.loads(m.group(1)) if m else []
    except json.JSONDecodeError:
        return []
    out = []
    for f in items if isinstance(items, list) else []:
        for key in ("heading", "body"):
            if isinstance(f, dict) and isinstance(f.get(key), str):
                out += [n for n in family_names(f[key]) if n not in out]
    return out


def unknown_fonts(text: str, allowed: set[str] = frozenset()) -> list[str]:
    """팔레트 화면 글꼴 가운데 표(fonts.json)에도 의뢰인 글꼴에도 없는 것. serif 같은 일반 이름은 괜찮다(guard.py 훅이 쓴다)."""
    from check_site import GENERIC_FAMILIES  # 일반 글꼴 이름은 check_site.py 하나로(그쪽이 이 파일을 먼저 불러 맨 위에서는 못 부른다)
    known = known_keys()
    return [n for n in palette_families(text)
            if n.lower() not in GENERIC_FAMILIES and norm(n) not in known and norm(n) not in allowed]


def find(name: str) -> dict | None:
    """이름·다른 이름·웹폰트 CSS 이름으로 표의 글꼴 하나."""
    key = norm(name)
    rows = load_table()["fonts"]
    return (next((r for r in rows if key in {norm(n) for n in [r["name"], *r.get("aliases", [])]}), None)
            or next((r for r in rows if key in {norm(n) for n in face_families(r.get("webfont") or "")}), None))


def webfont_line(r: dict) -> str:
    """후보 아래 한 줄: CSS 이름 · 굵기 · 파일 형식 — 전체 글은 fonts.py face."""
    wf = r.get("webfont") or ""
    if not wf:
        return "웹폰트 글 없음 — 받는 곳에서 파일을 받아 직접 @font-face 로"
    if wf.startswith("http"):
        return f"CSS 주소 {wf} · 이름 {', '.join(face_families(wf)) or '?'}"
    weights = sorted({w.strip() for w in FACE_WEIGHT.findall(wf)}, key=lambda w: (not w.isdigit(), w.zfill(4)))
    kinds = sorted({u.rsplit(".", 1)[-1].lower() for u in FACE_SRC.findall(wf) if "." in u.rsplit("/", 1)[-1]})
    names = ", ".join(f"'{n}'" for n in face_families(wf))
    return f"font-family {names} · 굵기 {'/'.join(weights) or '?'} · {'·'.join(kinds) or '?'} · 전체: fonts.py face \"{r['name']}\""


def cmd_face(name: str) -> int:
    r = find(name)
    if r is None:
        print(f"표에 없는 글꼴: {name} — fonts.py pick 에서 고르세요", file=sys.stderr)
        return 1
    wf = r.get("webfont") or ""
    if not wf:
        print(f"{r['name']}: 웹폰트 글 없음 — {r.get('download') or r.get('noonnu') or '받는 곳 표기 없음'} 에서 파일을 받아 직접 @font-face 로", file=sys.stderr)
        return 1
    print(f"/* {r['name']} · {r.get('maker', '')} · 출처 {r.get('noonnu') or r.get('download')} — 실제 사이트는 공식 파일을 직접 올려 쓴다 */")
    print(f'@import url("{wf}");' if wf.startswith("http") else wf.strip())
    return 0


def cmd_pick(styles: list[str], top: int, kind: str | None) -> int:
    data = load_table()
    keys = ai_keys()
    rows = []
    for r in data["fonts"]:
        if any(norm(n) in keys for n in [r["name"], *r.get("aliases", [])]):
            continue
        tags = " ".join(r.get("style", []))
        if styles and not any(s in tags for s in styles):
            continue
        if kind and kind not in r.get("kind", ""):
            continue
        rows.append(r)
    print(f"글꼴 후보 — {', '.join(styles) or '전체'} · {len(rows)}개 중 {min(top, len(rows))}개 (조사 {data['made']}, AI 글꼴 뺌)")
    for r in rows[:top]:
        why = f"상위 사이트 {r['top_sites']}곳({', '.join(r['sites'][:3])})" if r["top_sites"] else f"눈누 조회 {r['views']:,}"
        cond = "; ".join(r.get("conditions") or []) or "조건 표기 없음"
        print(f"- {r['name']} · {r['maker']}({r['kind']}) · {'/'.join(r.get('style', [])[:3])} · {r.get('weights', '')} · {cond[:80]} · {why} · {r.get('download') or r.get('noonnu')}")
        print(f"    웹폰트: {webfont_line(r)}")
    print("후보는 이 목록에서만 — fonts.json 을 직접 읽지 마세요")
    return 0


def main(argv: list[str]) -> int:
    utf8_console()
    ap = argparse.ArgumentParser(description="글꼴 후보 고르기와 AI 글꼴 검사")
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("pick")
    p.add_argument("--style", action="append", default=[], help="고딕·명조·손글씨·제목용·장식체 등(여러 번)")
    p.add_argument("--top", type=int, default=8)
    p.add_argument("--kind", help="회사·공공기관·단체·오픈 라이선스")
    c = sub.add_parser("check")
    c.add_argument("paths", nargs="+")
    f = sub.add_parser("face")
    f.add_argument("name", help="표의 이름·다른 이름·CSS 이름")
    a = ap.parse_args(argv)
    if a.cmd == "face":
        return cmd_face(a.name)
    return cmd_pick(a.style, a.top, a.kind) if a.cmd == "pick" else cmd_check(a.paths)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
