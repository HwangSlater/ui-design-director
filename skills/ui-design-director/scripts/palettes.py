#!/usr/bin/env python3
"""색상 조합은 사람이 만든 공개 팔레트(assets/palettes/palettes.json, Color Hunt)에서만 고른다.

    python palettes.py pick [--tags warm,earth] [--n 8] [--project .]   # 후보 팔레트(출처 주소·색·밝기 순 자리 제안)
    python palettes.py check <palette/index.html>                      # 팔레트 화면 후보마다 출처와 색이 맞는지

모델이 직접 고르면 크림 바탕에 숲초록·벽돌 단추, 버터 강조로 쏠렸다(지난 팔레트 62개 중 숲초록 12·벽돌 12·버터 10,
애견미용 19차 사용자 「AI 특유의 색조합」). 그래서 색 관계(몇 색·밝기 단계·어느 색이 어디를 맡나)는 바탕에서 재고,
색상은 이 표의 팔레트 하나에서 가져온다. 흰색·거의 검정·옅은 회색 같은 무채색은 어느 팔레트에도 더해도 된다.
"""
from __future__ import annotations

import colorsys
import hashlib
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import read, utf8_console  # noqa: E402

ASSETS = Path(__file__).resolve().parent.parent / "assets" / "palettes"
SOURCE = re.compile(r"colorhunt\.co/palette/([0-9a-fA-F]{24})")
HEX = re.compile(r"^#?([0-9a-fA-F]{6})$")
NEAR = 0.09          # 팔레트 색과 「같은 색」으로 보는 거리(RGB 0~1 공간, 밝기·채도 조금 다듬은 것 허용)
NEUTRAL_SAT = 0.12   # 이보다 채도가 낮으면 무채색 — 어느 팔레트에 더해도 된다
SKIP_ROLES = {"on-action"}
CLIENT = "의뢰인 색"   # source 가 이것으로 시작하면 의뢰인이 정한 색 — 출처를 묻지 않는다
SPREAD = 0.4         # 팔레트 안 가장 밝은 색과 가장 진한 색의 밝기 차 — 이보다 작으면 단추·글자를 못 나눈다  # 단추 위 글자(흰색·검정)는 대비로 정한다


def load() -> list[dict]:
    return json.loads(read(ASSETS / "palettes.json") or '{"palettes": []}')["palettes"]


def families() -> list[dict]:
    return json.loads(read(ASSETS / "ai-palettes.json") or '{"families": []}')["families"]


def rgb(hexcode: str) -> tuple[float, float, float] | None:
    m = HEX.match(hexcode.strip())
    if not m:
        return None
    x = m.group(1)
    return tuple(int(x[i:i + 2], 16) / 255 for i in (0, 2, 4))  # type: ignore[return-value]


def hls(c: tuple[float, float, float]) -> tuple[float, float, float]:
    h, l, s = colorsys.rgb_to_hls(*c)
    return h * 360, l, s


def chroma(c) -> float:
    """보이는 색의 진함 — 거의 흰색은 채도 숫자가 높아도 0 에 가깝다."""
    _, l, s = hls(c)
    return s * (1 - abs(2 * l - 1))


def same_hue(c, o) -> bool:
    """같은 색상의 진하기만 바꾼 것(단추 글자 대비를 맞추려 팔레트 색을 진하게) — 색상 ±10°, 진함이 비슷."""
    (h1, _, _), (h2, _, _) = hls(c), hls(o)
    gap = min(abs(h1 - h2), 360 - abs(h1 - h2))
    return gap <= 10 and chroma(o) > 0.05 and abs(chroma(c) - chroma(o)) <= 0.3


def dist(a, b) -> float:
    return sum((x - y) ** 2 for x, y in zip(a, b)) ** 0.5


def neutral(c) -> bool:
    _, l, s = hls(c)
    return s < NEUTRAL_SAT or l > 0.96 or l < 0.08


def in_family(c, fam: dict) -> bool:
    h, l, s = hls(c)
    lo, hi = fam["hue"]
    hue_ok = lo <= h <= hi if lo <= hi else (h >= lo or h <= hi)
    return hue_ok and fam["light"][0] <= l <= fam["light"][1] and fam["sat"][0] <= s <= fam["sat"][1]


def action_colour(colors: list):
    """팔레트에서 단추가 될 색 — 가장 진한 유채색(roles_hint 와 같은 판단)."""
    return max(colors, key=chroma) if colors else None


def ai_hits(colors: list) -> list[str]:
    """단추가 될 색이 모델 단골 무리에 드는가. 팔레트의 모든 색을 보니 글자색이 남색이라는 이유만으로 빠지는 팔레트가
    145개였고 고를 수 있는 것이 35% 로 줄었다(검토 2026-11-11) — 단추 자리 색만 본다."""
    act = action_colour(colors)
    return [fam["name"] for fam in families() if fam["role"] == "action" and act is not None and in_family(act, fam)]


def roles_hint(colors: list) -> str:
    """밝기 순으로 자리 제안 — 가장 밝은 색은 바탕·면, 가장 진한 색은 글자·진한 면, 채도 높은 색은 단추·강조."""
    by_light = sorted(colors, key=lambda c: hls(c)[1])
    by_sat = sorted(colors, key=lambda c: -chroma(c))
    hx = lambda c: "#%02x%02x%02x" % tuple(round(v * 255) for v in c)  # noqa: E731
    return f"밝은 쪽 {hx(by_light[-1])} → 바탕·면, 진한 쪽 {hx(by_light[0])} → 글자·진한 면, 채도 높은 {hx(by_sat[0])} → 단추·강조"


def pick(tags: list[str], n: int, project: str) -> list[dict]:
    rows = [p for p in load() if not tags or set(tags) & set(p["tags"])]
    # 모델 단골 무리는 빼고, 밝은 색과 진한 색이 함께 있어 바탕·글자·단추를 나눌 수 있는 것만(파스텔 넷은 단추가 안 된다)
    spread = lambda cs: max(hls(c)[1] for c in cs) - min(hls(c)[1] for c in cs)  # noqa: E731
    clean = [p for p in rows if not ai_hits([rgb(c) for c in p["colors"]]) and spread([rgb(c) for c in p["colors"]]) >= SPREAD]
    # 늘 맨 위 몇 개만 고르지 않게 — 인기 상위 60개 안에서 프로젝트마다 다르게 섞는다
    top = clean[:60]
    key = lambda p: hashlib.sha1((project + p["code"]).encode()).hexdigest()  # noqa: E731
    return sorted(top, key=key)[:n]


def candidates(html: str) -> list[dict]:
    m = re.search(r'id="palettes"[^>]*>(.*?)</script>', html, re.S)
    if not m:
        return []
    try:
        data = json.loads(m.group(1))
    except ValueError:
        return []
    return data if isinstance(data, list) else []


def problems(html: str) -> list[str]:
    """팔레트 화면 후보마다: Color Hunt 출처가 있고 표에 있는가, 유채색 자리 색이 그 팔레트 색인가."""
    table = {p["code"].lower(): p for p in load()}
    out = []
    for cand in candidates(html):
        name = f"{cand.get('id', '?')} {cand.get('name', '')}".strip()
        if str(cand.get("source", "")).startswith(CLIENT):  # 의뢰인이 이미 쓰는 색(간판·로고)은 그대로
            continue
        m = SOURCE.search(str(cand.get("source", "")))
        if not m:
            out.append(f"{name}: 출처 없음 — 색상은 palettes.py pick 의 팔레트에서, source 에 그 colorhunt.co/palette/… 주소")
            continue
        pal = table.get(m.group(1).lower())
        if not pal:
            out.append(f"{name}: 표에 없는 팔레트 {m.group(1)} — palettes.py pick 이 내놓은 것만")
            continue
        own = [rgb(c) for c in pal["colors"]]
        act = rgb(str((cand.get("roles") or {}).get("action", "")))
        hit = [f["name"] for f in families() if f["role"] == "action" and act and in_family(act, f)]
        if hit:  # 팔레트 색을 진하게 만들다 모델 단골 색이 됐다(24차 쑥색 → #4e5b4b)
            out.append(f"{name}: 단추 {cand['roles']['action']} 이(가) 모델 단골 색({hit[0]}) — 같은 팔레트의 다른 색을 단추로")
        for role, value in (cand.get("roles") or {}).items():
            c = rgb(str(value))
            if role in SKIP_ROLES or c is None or neutral(c):
                continue
            if min(dist(c, o) for o in own) > NEAR and not any(same_hue(c, o) for o in own):
                out.append(f"{name}: {role} {value} 이(가) 팔레트 {pal['code']} 의 색({', '.join(pal['colors'])})이 아님")
    return out


def base_is_white(root: Path) -> bool:
    """바탕 캡처(formats/base-cap)나 남긴 띠 사실로 본 바탕의 페이지 바탕이 흰색인가."""
    import copy_check
    bands = copy_check.cached_bands(root)
    bgs = [tuple(v["bg"]) for v in bands.values() if v.get("bg")]
    return bool(bgs) and all(copy_check.cdist(b, (255, 255, 255)) < copy_check.BAND_NOT_WHITE for b in bgs)


def base_is_dark(root: Path) -> bool:
    """바탕 페이지가 어두운 바탕(먹색 등)인가 — 남긴 띠 사실의 바탕색으로."""
    import copy_check
    bgs = [tuple(v["bg"]) for v in copy_check.cached_bands(root).values() if v.get("bg")]
    return bool(bgs) and all(copy_check.is_dark(b) for b in bgs)


def bg_problems(html: str, root: Path) -> list[str]:
    """바탕이 흰 바탕인데 크림 페이지 바탕을 낸 후보 — 끝에 가서 걸리면 의뢰인이 이미 골라 버렸다(빵집 33차). 팔레트 단계에서 막는다."""
    import copy_check
    if not copy_check.cached_bands(root):  # 바탕 캡처도 남긴 사실도 없으면 조용히 통과하던 것(검토 2026-11-11)
        return ["바탕 페이지 밝기를 못 봄 — 바탕 캡처(formats/base-cap)가 없어요. capture.mjs 로 바탕을 찍은 뒤 팔레트를 만드세요"]
    if base_is_dark(root):  # 어두운 바탕이면 밝은 페이지 바탕 후보를 막는다(맥주집 41차)
        out = []
        for cand in candidates(html):
            bg = rgb(str((cand.get("roles") or {}).get("bg", "")))
            if bg and not copy_check.is_dark(tuple(round(v * 255) for v in bg)):
                out.append(f"{cand.get('id', '?')} {cand.get('name', '')}: 바탕은 어두운 바탕인데 페이지 바탕 {cand['roles']['bg']} 이 밝음 — bg 는 어둡게")
        return out
    if not base_is_white(root):
        return []
    import copy_check
    out = []
    for cand in candidates(html):
        bg = rgb(str((cand.get("roles") or {}).get("bg", "")))
        if bg and copy_check.is_cream(tuple(round(v * 255) for v in bg)):
            out.append(f"{cand.get('id', '?')} {cand.get('name', '')}: 바탕이 흰 바탕인데 페이지 바탕 {cand['roles']['bg']} 이 크림 — bg 는 흰색(또는 거의 흰 회색), 크림은 면·강조에")
    return out


def main(argv: list[str]) -> int:
    utf8_console()
    if not argv or argv[0] not in ("pick", "check"):
        print(__doc__.strip(), file=sys.stderr)
        return 2
    opt = lambda k, d: argv[argv.index(k) + 1] if k in argv and argv.index(k) + 1 < len(argv) else d  # noqa: E731
    if argv[0] == "check":
        lines = problems(read(Path(argv[1]))) if len(argv) > 1 else ["파일을 주세요"]
        for line in lines:
            print(line)
        return 1 if lines else 0
    tags = [t for t in opt("--tags", "").split(",") if t]
    rows = pick(tags, int(opt("--n", "8")), str(Path(opt("--project", ".")).resolve().name))
    if not rows:
        print(f"맞는 팔레트 없음 — 쓸 수 있는 꼬리표: {', '.join(sorted({t for p in load() for t in p['tags']}))}")
        return 1
    for p in rows:
        print(f"{p['code']}  좋아요 {p['likes']:,}  {' '.join(p['colors'])}  [{', '.join(p['tags'])}]")
        print(f"    출처 {p['url']}")
        print(f"    {roles_hint([rgb(c) for c in p['colors']])}")
    print("색 관계(몇 색·밝기 단계)는 바탕을 따르고, 유채색은 고른 팔레트의 색(대비를 맞추려 같은 색상을 진하게·옅게 한 것까지)만. 무채색(흰색·먹색·옅은 회색)은 더해도 된다.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
