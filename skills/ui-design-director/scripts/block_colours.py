"""큰 덩어리(머리 단추·상태 띠·후원 판·알림…)를 칠한 진한 색이 하나뿐인지 본다 — check_site.py가 쓴다.

- one-colour-blocks (NOTE): 진한 색 하나가 덩어리 역할 다섯 군데 넘게 칠하고, 두 번째 진한 덩어리 색이 없다. 고칠 곳은 둘째 색이 아니라 칠한 자리 줄이기(강조색 하나 — 둘이면 원칙 없어 보임).
  색이 한 가지면 단추·띠·판이 모두 같은 무게로 보여 무엇이 먼저인지 흐려진다(color-selection.md).
"""

from __future__ import annotations

import re

# 덩어리 역할로 보는 class 낱말. 선택자의 마지막 class 묶음에서 찾는다.
BLOCK_CLASS_WORDS = ("band", "panel", "give", "top", "hero", "btn", "button", "cta", "call",
                     "toast", "banner", "st-ok", "badge", "foot", "header", "sheet")
MIN_ROLES = 5
STRONG_LUMINANCE = 0.6  # WCAG 상대 휘도. 이보다 어두우면 진한 색
STRONG_CHROMA = 0.5     # 밝아도 채도가 높으면(노랑 단추 등) 진한 색
SAME_COLOUR = 0.12      # 채널 차이 합이 이보다 작으면 같은 색으로 본다
NAMED = {"white": (1.0, 1.0, 1.0), "black": (0.0, 0.0, 0.0)}

RULE = re.compile(r"([^{}]+)\{([^{}]*)\}")
DECL = re.compile(r"([-\w]+)\s*:\s*([^;]+)")
VAR = re.compile(r"var\(\s*(--[\w-]+)\s*(?:,\s*([^()]*(?:\([^()]*\))?[^()]*))?\)")
HEX = re.compile(r"#([0-9a-fA-F]{3,8})\b")
RGB = re.compile(r"rgba?\(\s*([\d.]+)[\s,]+([\d.]+)[\s,]+([\d.]+)(?:[\s,/]+([\d.]+%?))?\s*\)")
COMMENT = re.compile(r"/\*.*?\*/", re.DOTALL)
MIX = re.compile(r"color-mix\(\s*in\s+srgb\s*,(.*)\)\s*$", re.DOTALL)


def _hex(h: str) -> tuple[float, ...] | None:
    if len(h) in (3, 4):
        h = "".join(c * 2 for c in h)
    if len(h) not in (6, 8):
        return None
    rgb = tuple(int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
    alpha = int(h[6:8], 16) / 255 if len(h) == 8 else 1.0
    return rgb + (alpha,)


def _split_top(text: str) -> list[str]:
    parts, depth, cur = [], 0, ""
    for ch in text:
        depth += (ch == "(") - (ch == ")")
        if ch == "," and depth == 0:
            parts.append(cur)
            cur = ""
        else:
            cur += ch
    return parts + [cur]


def parse_colour(value: str, tokens: dict[str, str], depth: int = 0) -> tuple[float, ...] | None:
    """(r, g, b, a) 0~1. var()·color-mix(in srgb)·#hex·rgb()·white/black만 푼다."""
    value = value.strip().lower()
    if depth > 8 or not value or value in ("none", "transparent", "inherit", "initial", "unset"):
        return None if value != "transparent" else (0.0, 0.0, 0.0, 0.0)
    m = VAR.fullmatch(value)
    if m:
        ref = tokens.get(m.group(1), m.group(2) or "")
        return parse_colour(ref, tokens, depth + 1)
    m = MIX.match(value)
    if m:
        parts = _split_top(m.group(1))
        if len(parts) != 2:
            return None
        cols, weights = [], []
        for part in parts:
            pm = re.match(r"(.*?)\s+([\d.]+)%\s*$", part.strip())
            colour = parse_colour(pm.group(1) if pm else part, tokens, depth + 1)
            if colour is None:
                return None
            cols.append(colour)
            weights.append(float(pm.group(2)) / 100 if pm else None)
        w0 = weights[0] if weights[0] is not None else 1 - (weights[1] if weights[1] is not None else 0.5)
        return tuple(a * w0 + b * (1 - w0) for a, b in zip(cols[0], cols[1]))
    m = HEX.fullmatch(value)
    if m:
        return _hex(m.group(1))
    m = RGB.fullmatch(value)
    if m:
        a = m.group(4) or "1"
        alpha = float(a[:-1]) / 100 if a.endswith("%") else float(a)
        return tuple(float(m.group(i)) / 255 for i in (1, 2, 3)) + (alpha,)
    if value in NAMED:
        return NAMED[value] + (1.0,)
    return None


def _first_colour(value: str, tokens: dict[str, str]) -> tuple[float, ...] | None:
    """background 단축 속성에서 색 조각 하나를 고른다(그림·그라디언트는 건너뜀)."""
    if "gradient" in value or "url(" in value:
        return None
    for part in re.findall(r"(?:var|color-mix|rgba?)\([^()]*(?:\([^()]*\)[^()]*)*\)|#[0-9a-fA-F]{3,8}\b|\b[a-z]+\b", value):
        colour = parse_colour(part, tokens)
        if colour is not None:
            return colour
    return None


def is_strong(colour: tuple[float, ...]) -> bool:
    r, g, b, alpha = colour
    if alpha < 0.6:
        return False
    lin = [c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in (r, g, b)]
    luminance = 0.2126 * lin[0] + 0.7152 * lin[1] + 0.0722 * lin[2]
    return luminance < STRONG_LUMINANCE or max(r, g, b) - min(r, g, b) >= STRONG_CHROMA


def block_role(selector: str) -> str | None:
    last = selector.strip().split()[-1] if selector.strip() else ""
    names = re.findall(r"\.([-\w]+)", last) or re.findall(r"\.([-\w]+)", selector)
    for name in names:
        if any(w in name.lower() for w in BLOCK_CLASS_WORDS):
            return name
    return None


def check_blocks(sources, report) -> None:
    # 주석은 지우되 줄 바꿈은 남겨 줄 번호를 지킨다
    texts = [(src, COMMENT.sub(lambda m: re.sub(r"[^\n]", " ", m.group(0)), src.text))
             for src in sources if not src.board]
    tokens: dict[str, str] = {}
    for _, text in texts:
        for m in RULE.finditer(text):
            if re.search(r":root|\bhtml\b", m.group(1)):
                for d in DECL.finditer(m.group(2)):
                    if d.group(1).startswith("--"):
                        tokens[d.group(1)] = d.group(2).strip()
    groups: list[dict] = []  # 같은 색끼리: {"colour", "roles", "where"}
    for src, text in texts:
        for m in RULE.finditer(text):
            for selector in m.group(1).split(","):
                role = block_role(selector)
                if role is None or ":hover" in selector or ":focus" in selector:
                    continue
                for d in DECL.finditer(m.group(2)):
                    if d.group(1).lower() not in ("background", "background-color"):
                        continue
                    colour = _first_colour(d.group(2), tokens)
                    if colour is None or not is_strong(colour):
                        continue
                    group = next((g for g in groups if sum(abs(a - b) for a, b in
                                  zip(g["colour"][:3], colour[:3])) < SAME_COLOUR), None)
                    if group is None:
                        line = src.first_line + text.count("\n", 0, m.start(2))
                        group = {"colour": colour, "roles": [], "where": (src.path, line)}
                        groups.append(group)
                    if role not in group["roles"]:
                        group["roles"].append(role)
    if len(groups) == 1 and len(groups[0]["roles"]) >= MIN_ROLES:
        g = groups[0]
        hexcode = "#" + "".join(f"{round(c * 255):02X}" for c in g["colour"][:3])
        report.add("NOTE", g["where"][0], g["where"][1], "one-colour-blocks",
                   f"same strong colour {hexcode} on {len(g['roles'])} block roles: {', '.join(g['roles'])} — "
                   "keep it for the main button and status, and let bands and panels go white with lines (one accent — color-selection.md)")
