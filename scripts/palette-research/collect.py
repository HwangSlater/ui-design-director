#!/usr/bin/env python3
"""Color Hunt 의 공개 팔레트(사람이 만들고 좋아요를 받은 4색 조합)를 모아 assets/palettes/palettes.json 으로.

    python -X utf8 scripts/palette-research/collect.py [--pages 10] [--tag-pages 3]

모델이 고른 색은 늘 크림+숲초록·벽돌+버터 같은 조합으로 쏠렸다(애견미용 19차, 사용자 「AI 특유의 색조합」).
그래서 색상 조합은 사람이 만든 공개 팔레트에서만 가져온다. 색 조합 자체는 저작물이 아니지만 출처 주소는 남긴다.
요청은 1초 간격, 쪽당 40개. 다시 돌리면 덮어쓴다.
"""
from __future__ import annotations

import json
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

FEED = "https://colorhunt.co/php/feed.php"
PAGE = "https://colorhunt.co/palette/{code}"
TAGS = ["warm", "cold", "earth", "nature", "pastel", "vintage", "retro", "cream", "coffee", "dark", "light",
        "sea", "sky", "spring", "summer", "fall", "winter", "food", "kids", "wedding", "night", "sunset", "skin", "gold", "happy"]
OUT = Path(__file__).resolve().parents[2] / "skills" / "ui-design-director" / "assets" / "palettes" / "palettes.json"


def feed(step: int, tag: str) -> list[dict]:
    data = urllib.parse.urlencode({"step": step, "sort": "popular", "tags": tag, "timeframe": 4000}).encode()
    req = urllib.request.Request(FEED, data=data, headers={"User-Agent": "Mozilla/5.0", "X-Requested-With": "XMLHttpRequest",
                                                           "Referer": "https://colorhunt.co/"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode("utf-8") or "[]")


def main(argv: list[str]) -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    pages = int(argv[argv.index("--pages") + 1]) if "--pages" in argv else 10
    tag_pages = int(argv[argv.index("--tag-pages") + 1]) if "--tag-pages" in argv else 3
    found: dict[str, dict] = {}
    jobs = [("", s) for s in range(pages)] + [(t, s) for t in TAGS for s in range(tag_pages)]
    for tag, step in jobs:
        try:
            rows = feed(step, tag)
        except OSError as e:
            print(f"건너뜀 {tag or '전체'} {step}: {e}")
            rows = []
        for r in rows:
            code = r.get("code", "")
            if len(code) != 24:
                continue
            p = found.setdefault(code, {"code": code, "colors": ["#" + code[i:i + 6] for i in range(0, 24, 6)],
                                        "likes": int(r.get("likes") or 0), "tags": [], "url": PAGE.format(code=code)})
            if tag and tag not in p["tags"]:
                p["tags"].append(tag)
        time.sleep(1)
    rows = sorted(found.values(), key=lambda p: -p["likes"])
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps({"source": "Color Hunt (colorhunt.co) 인기 팔레트", "collected": time.strftime("%Y-%m-%d"),
                               "palettes": rows}, ensure_ascii=False, indent=0), encoding="utf-8")
    print(f"팔레트 {len(rows)}개 → {OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
