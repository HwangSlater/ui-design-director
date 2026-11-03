"""다른 프로젝트 시안과 너무 닮았는지 본다 — check_site.py가 쓴다.

같은 사람이 만든 시안은 「따뜻하게」 같은 말 하나로 같은 답(크림 바탕·갈색 버튼·같은 제목 글꼴)으로 모인다.
도자기 공방과 피아노 교습소가 한 회사 사이트처럼 보였다. 그래서 시안 폴더(`<프로젝트>-시안`) 옆의
다른 `*-시안` 폴더에서 tokens.css를 찾아 넷을 견준다: 바탕색, 버튼색, 제목 글꼴, 본문 글꼴.

- sibling-look (NOTE): 넷 중 SAME_LIMIT개 이상이 같다. 이유(사용자가 고른 글꼴 등)를 DESIGN.md에 적거나 다르게 만든다.

본문 글꼴은 한국어 사이트라면 거의 늘 같으므로 혼자서는 걸리지 않게 한도를 셋으로 둔다.
첫 화면 구성은 파일로 알 수 없다 — ui-review.md § Site check 6에서 눈으로 견준다.
"""

from __future__ import annotations

import math
import re
from pathlib import Path

MOCKUP_SUFFIX = "-시안"
SAME_LIMIT = 3
# 바탕은 OKLab 거리로 본다(크림 #FFF8F0 · #FAF6EE 는 0.009).
BG_NEAR = 0.04
# 버튼은 거리만 보면 갈색과 자주색(#6E4B6B)도 0.085로 가깝다 — 색상각·밝기·채도를 따로 본다.
# 갈색 #8C5A3C · #6B4A35 는 색상각 2°, 밝기 0.08, 채도 0.02 차이. 갈색과 벽돌색 #B5543C 는 색상각 18°.
ACTION_HUE_DEG = 12
ACTION_L = 0.12
ACTION_C = 0.05
SKIP_DIRS = {"captures", "node_modules", "__pycache__", ".git"}

ROLES = {
    "바탕색": re.compile(r"^--(c-)?(bg|paper|canvas|background)$"),
    "버튼색": re.compile(r"^--(c-)?(action|primary|brand)$"),
    "제목 글꼴": re.compile(r"^--(f|font)-(heading|display|title)$"),
    "본문 글꼴": re.compile(r"^--(f|font)-(body|text|base)$"),
}
VAR_DECL = re.compile(r"(--[\w-]+)\s*:\s*([^;]+);")
VAR_REF = re.compile(r"^var\((--[\w-]+)\)$")
HEX = re.compile(r"^#([0-9a-fA-F]{3}|[0-9a-fA-F]{6})$")


def _tokens_file(folder: Path) -> Path | None:
    found = [p for p in folder.rglob("tokens.css") if not SKIP_DIRS & set(p.parts)]
    return max(found, key=lambda p: p.stat().st_mtime) if found else None


def _roles(css: Path) -> dict[str, str]:
    decl = {k: v.strip() for k, v in VAR_DECL.findall(css.read_text(encoding="utf-8", errors="replace"))}
    out: dict[str, str] = {}
    for role, pat in ROLES.items():
        name = next((k for k in decl if pat.match(k)), None)
        value = decl.get(name or "", "")
        ref = VAR_REF.match(value)
        out[role] = decl.get(ref.group(1), "") if ref else value
    return out


def _oklab(hex_value: str) -> tuple[float, float, float] | None:
    m = HEX.match(hex_value)
    if not m:
        return None
    h = m.group(1)
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    lin = []
    for i in (0, 2, 4):
        c = int(h[i:i + 2], 16) / 255
        lin.append(c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4)
    r, g, b = lin
    l_ = (0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b) ** (1 / 3)
    m_ = (0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b) ** (1 / 3)
    s_ = (0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b) ** (1 / 3)
    return (0.2104542553 * l_ + 0.7936177850 * m_ - 0.0040720468 * s_,
            1.9779984951 * l_ - 2.4285922050 * m_ + 0.4505937099 * s_,
            0.0259040371 * l_ + 0.7827717662 * m_ - 0.8086757660 * s_)


def _first_family(value: str) -> str:
    return value.split(",")[0].strip().strip("'\"").lower()


def _same(role: str, a: str, b: str) -> bool:
    if not a or not b:
        return False
    if "글꼴" in role:
        return _first_family(a) == _first_family(b)
    la, lb = _oklab(a), _oklab(b)
    if la is None or lb is None:
        return a.lower() == b.lower()
    if role == "바탕색":
        return math.dist(la, lb) < BG_NEAR
    (l1, c1, h1), (l2, c2, h2) = _lch(la), _lch(lb)
    hue_gap = abs((h1 - h2 + 180) % 360 - 180)
    return hue_gap < ACTION_HUE_DEG and abs(l1 - l2) < ACTION_L and abs(c1 - c2) < ACTION_C


def _lch(lab: tuple[float, float, float]) -> tuple[float, float, float]:
    l, a, b = lab
    return l, math.hypot(a, b), math.degrees(math.atan2(b, a)) % 360


def _project(root: Path) -> Path | None:
    for p in [root, *root.parents]:
        if p.name.endswith(MOCKUP_SUFFIX):
            return p
    return None


def check(root: Path, report) -> None:
    """root가 `*-시안` 폴더 안에 있을 때만 본다. 아니면 조용히 넘어간다."""
    root = root.resolve()
    project = _project(root)
    mine = _tokens_file(root)
    if project is None or mine is None:
        return
    my_roles = _roles(mine)
    for other in sorted(project.parent.iterdir()):
        if other == project or not other.is_dir() or not other.name.endswith(MOCKUP_SUFFIX):
            continue
        theirs = _tokens_file(other)
        if theirs is None:
            continue
        their_roles = _roles(theirs)
        same = [r for r in ROLES if _same(r, my_roles[r], their_roles[r])]
        if len(same) >= SAME_LIMIT:
            report.add("NOTE", str(mine.relative_to(root)), 1, "sibling-look",
                       f"「{other.name}」 시안과 {len(same)}가지가 같다({', '.join(same)}) — 이유를 DESIGN.md에 적거나 바꾼다")
