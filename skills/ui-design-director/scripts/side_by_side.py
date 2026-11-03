#!/usr/bin/env python3
"""우리 화면과 기준 사이트 화면을 같은 폭으로 나란히 놓고, 시각 층 대조표를 붙인 HTML을 만든다(외부 패키지 없음).

    python side_by_side.py <out.html> <우리.jpg> <기준.jpg> [<우리2.jpg> <기준2.jpg> ...]

ui-review.md § Site check 5(기준 비교)와 reference-extraction.md § Visual layers 에서 쓴다.
대조표 칸은 비어 있다 — 두 화면을 보면서 층마다 「기준에 있음 / 우리에 있음 / 대신한 것·뺀 이유」를 채운다.
빈 칸이나 「없음」이 둘 넘게 남으면 보여 줄 준비가 안 된 것이다.
"""
from __future__ import annotations

import html
import os
import sys
from pathlib import Path

# 실제 운영 사이트를 「만든 것」처럼 보이게 하는 층. 하나를 빼면 다른 것으로 대신하거나 이유를 적는다
LAYERS = [
    ("정체성", "로고·엠블럼·워드마크, 머리 띠"),
    ("대상의 얼굴", "팀 엠블럼·상품 사진·사람 아바타처럼 목록의 각 항목을 알아보게 하는 그림"),
    ("아이콘", "시간·장소·날짜 같은 반복 정보 앞의 작은 그림"),
    ("색 덩어리", "띠·판·칠한 칸처럼 넓게 칠한 면(버튼 말고)"),
    ("데이터 표시", "승패 칩, 막대, 배지, 진행 표시"),
    ("사진·그림", "분위기를 정하는 큰 그림 또는 그것을 대신한 무늬·일러스트"),
    ("깊이", "그림자, 겹친 판, 진한 판 하나"),
    ("넓은 화면 배치", "1280px에서 단 수와 옆 칸(빈 양옆이 아닌지)"),
    ("글자 대비", "가장 큰 글자와 본문의 크기 차이, 굵기 차이"),
]


def main(argv: list[str]) -> int:
    if len(argv) < 3 or len(argv[1:]) % 2:
        print(__doc__.strip(), file=sys.stderr)
        return 2
    out = Path(argv[0]).resolve()
    pairs = [(Path(argv[i]).resolve(), Path(argv[i + 1]).resolve()) for i in range(1, len(argv), 2)]
    for a, b in pairs:
        for f in (a, b):
            if not f.is_file():
                print(f"ERROR: 없는 파일: {f}", file=sys.stderr)
                return 2
    rel = lambda f: html.escape(Path(os.path.relpath(f, out.parent)).as_posix())
    rows = "".join(f"<figure><div class=pair><div><p>우리</p><img src='{rel(a)}' alt='우리 화면'></div>"
                   f"<div><p>기준</p><img src='{rel(b)}' alt='기준 화면'></div></div></figure>" for a, b in pairs)
    table = "".join(f"<tr><th scope=row>{html.escape(n)}</th><td>{html.escape(d)}</td><td></td><td></td><td></td></tr>"
                    for n, d in LAYERS)
    out.write_text(f"""<!doctype html>
<html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="check-site" content="comparison-board">
<title>기준 사이트와 나란히</title>
<style>
body {{ margin: 0; font: 15px/1.5 system-ui, sans-serif; background: #1f1f1f; color: #eee; word-break: keep-all; }}
figure {{ margin: 0 0 24px; }}
.pair {{ display: grid; grid-template-columns: 1fr 1fr; gap: 16px; padding: 16px; }}
.pair p {{ margin: 0 0 6px; font-weight: 700; }}
.pair img {{ width: 100%; display: block; }}
table {{ border-collapse: collapse; margin: 16px; background: #2a2a2a; }}
th, td {{ border: 1px solid #444; padding: 8px 10px; text-align: left; vertical-align: top; min-width: 120px; }}
</style></head><body>
{rows}
<table><thead><tr><th scope=col>층</th><th scope=col>무엇</th><th scope=col>기준에 있음</th><th scope=col>우리에 있음</th><th scope=col>대신한 것·뺀 이유</th></tr></thead>
<tbody>{table}</tbody></table>
</body></html>
""", encoding="utf-8")
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
