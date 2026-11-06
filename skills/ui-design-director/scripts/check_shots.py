#!/usr/bin/env python3
"""보내기 전 그림 확인 — 비어 있거나 한 색뿐인 캡처(불러오는 중, 로고만 있는 입구 화면, 검은 첫 화면)를 잡는다.

    python check_shots.py <그림 또는 폴더> [...] [--height 900]

그림마다 맨 위 한 화면(기본 900px)을 보고 「통과 / 의심」을 적는다. 의심이면 사람이 열어 보고 다시 찍는다.
「모든 그림을 열어 보라」는 규칙이 글로만 있을 때 두 번 빠뜨렸다(빵집 후보 그림에 빙글빙글 도는 화면·쿠키 창).
쿠키 창 같은 덮개는 글자를 읽어야 해서 여기서는 못 잡는다 — capture.mjs 가 기본으로 걷어 낸다.
"""
from __future__ import annotations

import sys
from pathlib import Path

import re
from PIL import Image, ImageStat

FLAT_STD = 14          # 밝기 표준편차가 이보다 작으면 거의 한 색
ONE_COLOUR_SHARE = 0.82  # 가장 흔한 밝기 부근(±10)이 이 비율을 넘으면 한 색 화면
SMALL = 64             # 비교용으로 줄이는 크기


def verdict(path: Path, height: int) -> str:
    im = Image.open(path).convert("L")
    # capture.mjs 는 2배로 찍는다: 파일 이름 끝의 폭(-1280.jpg)으로 배율을 알아내 첫 화면 높이를 맞춘다
    m = re.search(r"-(\d{3,4})(?:-\d+)?\.(?:jpg|png)$", path.name)
    scale = im.width / int(m.group(1)) if m and int(m.group(1)) else 1
    top = im.crop((0, 0, im.width, min(im.height, round(height * scale))))
    std = ImageStat.Stat(top).stddev[0]
    hist = top.resize((SMALL, SMALL)).histogram()
    peak = max(range(256), key=lambda v: hist[v])
    near = sum(hist[max(0, peak - 10):min(256, peak + 11)]) / (SMALL * SMALL)
    if std < FLAT_STD:
        return f"의심  거의 빈 화면(밝기 편차 {std:.0f})"
    if near > ONE_COLOUR_SHARE:
        return f"의심  한 색이 {near:.0%} — 불러오는 중·입구 화면일 수 있음"
    return "통과"


def main() -> int:
    args = sys.argv[1:]
    height = int(args[args.index("--height") + 1]) if "--height" in args else 900
    paths = []
    for a in args:
        if a.startswith("--") or a.isdigit():
            continue
        p = Path(a)
        paths += sorted(p.glob("*.jpg")) + sorted(p.glob("*.png")) if p.is_dir() else [p]
    bad = 0
    for p in paths:
        v = verdict(p, height)
        bad += v.startswith("의심")
        print(f"{v:<40} {p.name}")
    print(f"의심 {bad} / {len(paths)}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
