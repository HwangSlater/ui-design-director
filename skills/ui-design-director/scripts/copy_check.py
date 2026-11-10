#!/usr/bin/env python3
"""베낀 티 재기 — 우리 시안의 첫 화면이 바탕 사이트와 짜임·색 둘 다 거의 같은지.

    python copy_check.py <프로젝트 폴더>            # 폭마다 점수와 판정. 「베낀 티」가 있으면 종료 코드 1
    python copy_check.py --pair <바탕.jpg> <우리.png> [--width 1280]

바탕을 따르라는 규칙만 있고 「얼마나 같으면 베낀 것인가」가 없어서, 짜임 도구가 「바꿀 곳 0곳」을 내자
디자이너가 색·마감까지 그대로 옮겼다(NBA 11차: theScore 한국어판). 짜임은 바탕을 따르는 것이 스킬의 방식이라,
판정은 색(마감)으로 한다: 첫 화면 주요 색 6개와 비율이 바탕과 거의 같으면(COLOUR_COPY 이상) 베낀 티.
- 색: 0~1. 2026-11-09 시안 4개로 맞춤 — 베낀 NBA 0.97·1.00, 바탕을 따르되 우리 색을 쓴 시안 0.74~0.88
- 짜임: 참고로만 찍는다(위아래로 밀어 가며 맞춘 가장자리 배치 상관). 글 내용이 다르면 낮게 나와 판정에 쓰지 못했다
바탕 캡처: formats/base-cap/ · 우리 캡처: mockups/보낼-그림/ (같은 폭, 상태 화면 제외)
옅은 띠: 같은 두 캡처의 페이지 전체에서 폭 가득한 옅은 색 띠(높이 120px 이상, 흰색·페이지 바탕색이 아님)를 찾아
바탕 캡처에 같은 색 띠가 없으면 알린다 — 바탕에 없는 연한 청록 띠를 구역 뒤에 깐 것(꽃집 13차). 띠 안의 글·카드는
가운데에 있으므로 양쪽 끝(각 20px 안팎)이 같은 색인 줄을 띠로 본다. 가운데만 칠한 상자 띠는 보지 않는다.
색 띠 쌓기: 같은 방법으로 진한 색(밝기 0.75 아래, 흰색·페이지 바탕색 아님, 바닥글 빼고) 띠가 2개 이상 잇달아 바탕보다 많고(사이의 바탕·흰 구역은
끊지 않음, 다른 옅은 띠는 끊음) 바탕 캡처는 그렇지 않으면 알린다 — 갈색·벽돌·짙은 갈색 판을 줄줄이 깐 것(플리마켓 14차).
캡처 이름에 폭이 없으면 「휴대폰·모바일·폰·mobile·phone」「PC·데스크톱·컴퓨터·desktop」으로 찾고 폭은 그림 너비로 짐작한다.
"""
from __future__ import annotations

import argparse
import colorsys
import json
import math
import re
import sys
from pathlib import Path

from common import read, utf8_console  # 콘솔 한글 깨짐 막기·파일 읽기는 common 하나로

from PIL import Image, ImageFilter

FIRST_SCREEN = {390: 844, 1280: 900}  # 첫 화면 높이(CSS px) — capture.mjs 와 같은 기기 크기
# 화면 종류마다 찾을 폭 — 디자이너가 PC 를 1440 으로 찍어 1280 만 찾던 검사가 PC 를 건너뛰었다(NBA 12차)
VIEWS = {"휴대폰": (390, 375, 360, 414, 430), "PC": (1280, 1440, 1366, 1536, 1600, 1920)}
VIEW_HEIGHT = {"휴대폰": 844, "PC": 900}
VIEW_RANGE = {"휴대폰": (320, 480), "PC": (1024, 2000)}  # 그림 너비로 폭을 짐작할 때 한 화면으로 볼 CSS 폭
VIEW_WORDS = {"휴대폰": re.compile(r"휴대폰|모바일|폰|mobile|phone", re.I),
              "PC": re.compile(r"(^|[^a-z])pc([^a-z]|$)|데스크톱|컴퓨터|desktop", re.I)}
GRID_W = 48                            # 짜임 비교 칸 수(가로)
PALETTE_N = 6
# NBA 11차(theScore 를 그대로 옮김)가 걸리고, 바탕을 따르되 우리 색·마감을 쓴 시안은 지나가게 잡은 값(2026-11-09 시안 8개로 맞춤)
COLOUR_COPY = 0.92
STATE_WORDS = re.compile(r"empty|offline|error|loading|judge|빈|오류|실패", re.I)


def first_screen(path: Path, width: int, height: int | None = None) -> Image.Image:
    im = Image.open(path).convert("RGB")
    scale = im.width / width  # 2배 캡처도 같은 비율로
    h = min(im.height, int((height or FIRST_SCREEN.get(width, 900)) * scale))
    return im.crop((0, 0, im.width, h))


def edge_map(im: Image.Image, gw: int, gh: int) -> list[list[float]]:
    small = im.convert("L").filter(ImageFilter.FIND_EDGES).filter(ImageFilter.GaussianBlur(2)).resize((gw, gh), Image.BOX)
    flat = list(small.get_flattened_data() if hasattr(small, "get_flattened_data") else small.getdata())
    return [flat[r * gw:(r + 1) * gw] for r in range(gh)]


def corr(xs: list[float], ys: list[float]) -> float:
    n = len(xs)
    if not n:
        return 0.0
    mx, my = sum(xs) / n, sum(ys) / n
    cov = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    vx = math.sqrt(sum((x - mx) ** 2 for x in xs))
    vy = math.sqrt(sum((y - my) ** 2 for y in ys))
    return cov / (vx * vy) if vx and vy else 0.0


def layout_similarity(a: Image.Image, b: Image.Image) -> float:
    """위아래로 밀어 가며 가장 잘 맞는 자리의 상관 — 머리 띠 높이가 달라 내용이 통째로 밀리면 위치만 다르고 짜임은 같다."""
    gw = GRID_W
    gh = max(8, round(a.height * gw / a.width))
    ea, eb = edge_map(a, gw, gh), edge_map(b.resize(a.size), gw, gh)
    best = -1.0
    for shift in range(-gh // 3, gh // 3 + 1):
        rows = [(ea[r], eb[r + shift]) for r in range(gh) if 0 <= r + shift < gh]
        if len(rows) < gh * 2 // 3:
            continue
        best = max(best, corr([v for x, _ in rows for v in x], [v for _, y in rows for v in y]))
    return best


def palette(im: Image.Image, n: int = PALETTE_N, method=Image.Quantize.MEDIANCUT) -> list[tuple[tuple[int, int, int], float]]:
    q = im.resize((160, max(1, round(im.height * 160 / im.width)))).quantize(colors=n, method=method)
    pal = q.getpalette()[: n * 3]
    counts = q.getcolors() or []
    total = sum(c for c, _ in counts) or 1
    return [((pal[i * 3], pal[i * 3 + 1], pal[i * 3 + 2]), c / total) for c, i in counts]


def colour_similarity(a: Image.Image, b: Image.Image) -> float:
    pa, pb = palette(a), palette(b)
    dist = lambda x, y: math.dist(x, y) / 441.7  # RGB 최대 거리로 나눔
    # 서로 가장 가까운 색까지의 거리를 비율로 평균 — 양쪽에서 재서 평균
    one = sum(w * min(dist(c, d) for d, _ in pb) for c, w in pa)
    two = sum(w * min(dist(c, d) for d, _ in pa) for c, w in pb)
    return max(0.0, 1 - (one + two) / 2 * 4)  # 평균 거리 0.25(꽤 다른 색)면 0


def judge(base: Path, ours: Path, width: int, ours_width: int | None = None, height: int | None = None) -> tuple[float, float, bool]:
    a, b = first_screen(base, width, height), first_screen(ours, ours_width or width, height)
    lay, col = layout_similarity(a, b), colour_similarity(a, b)
    return lay, col, col >= COLOUR_COPY


def find_view(folder: Path, view: str, prefer: str = "") -> tuple[Path, int] | tuple[None, None]:
    """그 화면 종류(휴대폰·PC)로 찍은 캡처와 그 폭 — 이름에 폭이 있는 것 먼저, 없으면 이름에 화면 종류 말
    (「1-휴대폰.jpg」「2-PC.jpg」 — 치과 15차가 이렇게 적어 캡처 없음으로 건너뛰었다). 폭은 그림 너비로 짐작한다."""
    for width in VIEWS[view]:
        f = find(folder, width, prefer)
        if f:
            return f, width
    if folder.is_dir():
        files = sorted((f for f in folder.iterdir() if f.suffix.lower() in (".png", ".jpg", ".jpeg")
                        and VIEW_WORDS[view].search(f.stem) and not STATE_WORDS.search(f.name)),
                       key=lambda f: (prefer not in f.name, len(f.name)))
        if files:
            return files[0], css_width(files[0], view)
    return None, None


def css_width(path: Path, view: str) -> int:
    """그림 너비로 CSS 폭 짐작 — 1배·2배 캡처면 그 폭, 아니면(여러 화면을 이어 붙인 그림 등) 기본 폭."""
    lo, hi = VIEW_RANGE[view]
    with Image.open(path) as im:
        w = im.width
    for k in (1, 2):
        if lo <= w / k <= hi:
            return round(w / k)
    return VIEWS[view][0]


def pairs(root: Path):
    """화면 종류마다 (종류, 바탕, 바탕 폭, 우리, 우리 폭) — 하나라도 없으면 None 자리."""
    for view in VIEWS:
        base, bw = find_view(root / "formats" / "base-cap", view, prefer="home")
        ours, ow = find_view(root / "mockups" / "보낼-그림", view, prefer="main")
        yield view, base, bw, ours, ow


def find(folder: Path, width: int, prefer: str = "") -> Path | None:
    if not folder.is_dir():
        return None
    files = [f for f in folder.iterdir() if f.suffix.lower() in (".png", ".jpg", ".jpeg") and re.search(rf"(^|[-_]){width}([-_.]|$)", f.name) and not STATE_WORDS.search(f.name)]
    files.sort(key=lambda f: (prefer not in f.name, len(f.name)))
    return files[0] if files else None


PALETTE_SAME = 0.06  # 바탕 색과 이만큼(RGB 최대 거리 비율) 가까우면 같은 색


def hex_rgb(h: str) -> tuple[int, int, int] | None:
    m = re.fullmatch(r"#?([0-9a-fA-F]{6})", str(h).strip())
    return tuple(int(m.group(1)[i:i + 2], 16) for i in (0, 2, 4)) if m else None


def palette_copies(root: Path) -> list[str]:
    """팔레트 화면의 후보 가운데 바탕 색을 그대로 쓴 것 — 「바탕 그대로」 후보를 의뢰인이 매번 골라 바탕 사이트처럼 보였다."""
    page = root / "palette" / "index.html"
    base, bw = find_view(root / "formats" / "base-cap", "PC", prefer="home")
    if not base:
        base, bw = find_view(root / "formats" / "base-cap", "휴대폰", prefer="home")
    if not page.is_file():
        return []
    m = re.search(r'id="palettes"[^>]*>(.*?)</script>', page.read_text(encoding="utf-8", errors="replace"), re.S)
    try:
        cands = json.loads(m.group(1)) if m else []
    except json.JSONDecodeError:
        return []
    # 강조색은 면적이 작아(단추 하나) 6색으로 줄이면 회색에 섞였다 — 후보와 견줄 때는 16색까지
    base_cols = [c for c, w in palette(first_screen(base, bw), 16, Image.Quantize.FASTOCTREE) if w > 0.002] if base else []
    out = []
    for c in cands:
        roles = c.get("roles") or {}
        main = [hex_rgb(roles.get(k, "")) for k in ("bg", "action")]
        same = base_cols and all(x and min(math.dist(x, b) / 441.7 for b in base_cols) < PALETTE_SAME for x in main)
        if same or "바탕 그대로" in str(c.get("name", "")):
            out.append(f"바탕 그대로인 팔레트 후보: {c.get('id', '?')} {c.get('name', '')} — 바탕의 색 관계는 지키고 색은 우리 것으로(color-selection.md)")
    return out


OWN_HEADING = "바탕에서 바꾼 곳"
OWN_LAYERS = ("색 계열", "이름 처리", "칸 마감", "대표 요소")  # build-rules.md § Make it ours 의 네 가지
OWN_MIN = 2
REAL_LOGO = re.compile(r"실제 로고|견본 로고")  # 의뢰인이 실제 로고·사진을 쓰라 했으면 이름 처리는 바탕(남의 것) 그대로다


def own_finish(root: Path) -> list[str]:
    """DESIGN.md § 바탕에서 바꾼 곳의 「우리 것(마감)」에 네 가지 중 둘 이상이 있는가. 절이 없으면 preflight 가 따로 알린다."""
    text = read(root / "DESIGN.md")
    m = re.search(rf"^##\s*{OWN_HEADING}[^\n]*\n(.*?)(?=^##\s|\Z)", text, re.M | re.S)
    if not m:
        return []
    layers = [k for k in OWN_LAYERS if k in m.group(1)]
    if REAL_LOGO.search(text) and "이름 처리" in layers:
        layers.remove("이름 처리")
    if len(layers) >= OWN_MIN:
        return []
    note = " (실제·견본 로고를 쓰므로 이름 처리는 세지 않음)" if REAL_LOGO.search(text) else ""
    return [f"우리 것 마감이 둘 미만: DESIGN.md § {OWN_HEADING} 「우리 것(마감)」에 {', '.join(layers) or '없음'}{note} — "
            f"{'·'.join(OWN_LAYERS)} 중 둘 이상을 우리 것으로 정해 적을 것(build-rules.md § Make it ours)"]


BAND_COLS = 128        # 띠를 찾을 때 줄인 가로 칸 수
BAND_EDGE = 2          # 양쪽 끝 이만큼 칸이 같은 색이면 폭 가득 띠의 줄
BAND_MIN_CSS = 120     # 이 높이(CSS px) 이상만 띠
BAND_SAME = 0.015      # 이어지는 줄을 같은 띠로 볼 색 거리(jpg 얼룩보다 조금 큼)
BAND_LIGHT = 0.88      # 밝기가 이보다 높으면 옅은 색
BAND_NOT_WHITE = 0.02  # 흰색과 이만큼 떨어져야 색 띠
BAND_NOT_BG = 0.03     # 페이지 바탕색과 이만큼 떨어져야 따로 깐 띠
BAND_IN_BASE = 0.04    # 바탕 띠와 이만큼 가까우면 바탕에 있는 색
BAND_STRONG_L = 0.75   # 밝기가 이보다 낮으면 진한 띠(색 띠 쌓기)
STACK_MIN = 2          # 진한 띠가 이만큼 잇달고 바탕보다 많으면 색 띠 쌓기(플리마켓 14차: 갈색·벽돌, 바닥글 빼고) — 시안 16개 중 이것만 걸림


def cdist(a, b) -> float:
    return math.dist(a, b) / 441.7


def colour_runs(path: Path, width: int) -> list[tuple[tuple[int, int, int], float, float]]:
    """페이지 전체에서 폭 가득 같은 색인 줄이 이어진 곳 (색, 위 CSS px, 높이 CSS px) — 높이와 상관없이 전부."""
    im = Image.open(path).convert("RGB")
    rows = max(1, round(im.height * BAND_COLS / im.width))
    px = im.resize((BAND_COLS, rows), Image.BOX).load()
    css = width / BAND_COLS
    runs, start, col = [], 0, None
    for y in range(rows + 1):
        c = None
        if y < rows:
            edge = [px[x, y] for x in (*range(BAND_EDGE), *range(BAND_COLS - BAND_EDGE, BAND_COLS))]
            mean = tuple(sum(p[i] for p in edge) // len(edge) for i in range(3))
            c = mean if all(cdist(p, mean) < BAND_SAME * 2 for p in edge) else None
        if c is not None and col is not None and cdist(c, col) < BAND_SAME:
            continue
        if col is not None:
            runs.append((col, start * css, (y - start) * css))
        start, col = y, c
    return runs


def page_bg(runs) -> tuple[int, int, int]:
    """가장 길게 깔린 띠 색 = 페이지 바탕색."""
    return max((r[0] for r in runs), key=lambda c: sum(h for d, _, h in runs if cdist(c, d) < BAND_SAME))


def lightness(c) -> float:
    return colorsys.rgb_to_hls(*(v / 255 for v in c))[1]


def strong_stack(path: Path, width: int) -> list[tuple[int, int, int]]:
    """진한 색(옅지 않고 흰색 아닌) 폭 가득 띠가 잇달아 쌓인 가장 긴 묶음의 색들. 사이의 페이지 바탕·흰 구역은
    묶음을 끊지 않고(갈색·벽돌·갈색이 바탕 구역을 끼고 번갈아 나온 것도 쌓기), 다른 옅은 색 띠가 끊는다."""
    runs = colour_runs(path, width)
    if not runs:
        return []
    bg, best, cur = page_bg(runs), [], []
    # 맨 아래 띠(바닥글)는 세지 않는다 — 진한 바닥글은 흔해서 셋째 띠로 잘못 셌다(플리마켓 14차의 #2b2225)
    body = runs[:-1] if len(runs) > 1 else runs
    for c, _, h in body:
        if h < BAND_MIN_CSS or cdist(c, bg) < BAND_NOT_BG or cdist(c, (255, 255, 255)) < BAND_NOT_WHITE:
            continue
        if lightness(c) < BAND_STRONG_L:
            cur.append(c)
            best = max(best, cur, key=len)
        else:
            cur = []
    return list(best)


def stacked_bands(base: Path, bw: int, ours: Path, ow: int) -> tuple[list[str], int]:
    """우리 페이지에 진한 띠가 STACK_MIN 개 이상 잇달고 바탕보다 많으면 (#색들, 바탕 묶음 수). 아니면 ([], 0)."""
    ours_stack, base_n = strong_stack(ours, ow), len(strong_stack(base, bw))
    if len(ours_stack) < STACK_MIN or len(ours_stack) <= base_n:
        return [], 0
    return ["#%02x%02x%02x" % c for c in ours_stack], base_n


def pale_bands(base: Path, bw: int, ours: Path, ow: int) -> list[tuple[str, int]]:
    """우리 페이지의 옅은 색 띠 가운데 바탕에 없는 색 — (#색, 띠 수)."""
    runs = colour_runs(ours, ow)
    if not runs:
        return []
    bg = page_bg(runs)
    base_cols = [c for c, _, h in colour_runs(base, bw) if h >= BAND_MIN_CSS]
    found: list[list] = []
    for c, _, h in runs:
        light = lightness(c) > BAND_LIGHT
        if (h < BAND_MIN_CSS or not light or cdist(c, (255, 255, 255)) < BAND_NOT_WHITE or cdist(c, bg) < BAND_NOT_BG
                or any(cdist(c, b) < BAND_IN_BASE for b in base_cols)):
            continue
        same = next((f for f in found if cdist(f[0], c) < BAND_IN_BASE), None)
        if same:
            same[1] += 1
        else:
            found.append([c, 1])
    return [("#%02x%02x%02x" % c, n) for c, n in found]


def band_lines(view: str, base: Path, bw: int, ours: Path, ow: int) -> list[str]:
    out = [f"옅은 띠({view}): {hex_} 줄 {n}개 — 바탕에 없음. 바탕에 없는 색 띠는 생성 티, 구역은 페이지 바탕 위에(build-rules.md § What reads as generated)"
           for hex_, n in pale_bands(base, bw, ours, ow)]
    stack, base_n = stacked_bands(base, bw, ours, ow)
    if stack:
        out.append(f"색 띠 쌓기({view}): 진한 띠 {len(stack)}개 잇달아({'·'.join(stack)}), 바탕은 {base_n}개 — 진한 색 판은 "
                   "바탕이 깐 자리에만, 나머지 구역은 페이지 바탕 위에(build-rules.md § What reads as generated)")
    return out


def check_project(root: Path) -> list[str]:
    """preflight.py 도 부른다 — 바탕 그대로인 팔레트 후보, 우리 것 마감 수, 베낀 티·옅은 띠가 있는 폭마다 한 줄."""
    out = palette_copies(root) + own_finish(root)
    for view, base, bw, ours, ow in pairs(root):
        if not base or not ours:
            continue
        out += band_lines(view, base, bw, ours, ow)
        lay, col, copied = judge(base, ours, bw, ow, VIEW_HEIGHT[view])
        if copied:
            out.append(f"베낀 티({view}): 색 {col:.2f}(짜임 {lay:.2f}) — 첫 화면 색·마감이 바탕과 거의 같음. "
                       "짜임은 따라도 되지만 색 계열·이름 처리·칸 마감·대표 요소 중 둘 이상을 우리 것으로(build-rules.md § Make it ours)")
    return out


def main(argv: list[str]) -> int:
    utf8_console()
    ap = argparse.ArgumentParser(description="베낀 티 재기")
    ap.add_argument("project", nargs="?")
    ap.add_argument("--pair", nargs=2)
    ap.add_argument("--width", type=int, default=1280)
    a = ap.parse_args(argv)
    if a.pair:
        lay, col, copied = judge(Path(a.pair[0]), Path(a.pair[1]), a.width)
        print(f"짜임 {lay:.2f} · 색 {col:.2f} → {'베낀 티' if copied else '괜찮음'}")
        return 1 if copied else 0
    root = Path(a.project or ".")
    pal = palette_copies(root) + own_finish(root)
    for line in pal:
        print(line)
    rows = len(pal)
    for view, base, bw, ours, ow in pairs(root):
        if not base or not ours:
            print(f"{view}: 캡처 없음(바탕 {base.name if base else '-'} · 우리 {ours.name if ours else '-'})")
            continue
        lay, col, copied = judge(base, ours, bw, ow, VIEW_HEIGHT[view])
        bands = band_lines(view, base, bw, ours, ow)
        rows += copied + len(bands)
        print(f"{view}: 짜임 {lay:.2f} · 색 {col:.2f} → {'베낀 티' if copied else '괜찮음'} ({base.name} ↔ {ours.name})")
        for line in bands:
            print(line)
    return 1 if rows else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
