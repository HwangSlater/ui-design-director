#!/usr/bin/env python3
"""fonts.json 의 눈누 글꼴마다 눈누 상세 페이지의 「웹폰트로 사용」 @font-face 글을 모은다.

    python -I webfont.py <fonts.json> [<임시 폴더>]

- 요청은 하나씩, 사이에 config.json 의 delay_sec(1.2초) — 눈누는 빠르게 받으면 429 를 돌려준다.
- 받은 글은 임시 폴더(기본: 시스템 임시 폴더/uidd-noonnu-webfont)에 <id>.css 로만 둔다. 웹폰트 글이 없는 페이지는 <id>.none.
  끊겨도 다시 돌리면 이미 있는 파일은 건너뛴다(checkpoint). 원본 HTML 은 남기지 않는다.
- 합치기: python -X utf8 scripts/font-research/merge.py --webfont <임시 폴더> skills/ui-design-director/assets/fonts/fonts.json
"""
from __future__ import annotations

import html
import json
import re
import sys
import tempfile
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from crawl import CFG, get  # noqa: E402  (요청 머리·다시 시도는 crawl.py 와 같게)

PAGE_ID = re.compile(r"/font_page/(\d+)")
# 상세 페이지의 「웹폰트로 사용」 칸 — <pre name="webfontSource" …>@font-face {…}</pre>
SOURCE = re.compile(r'<pre[^>]*name="webfontSource"[^>]*>(.*?)</pre>', re.S)
DEFAULT_DIR = Path(tempfile.gettempdir()) / "uidd-noonnu-webfont"


def snippet(page: str) -> str:
    """페이지에서 웹폰트 글(첫 칸). 없으면 빈 글."""
    m = SOURCE.search(page)
    return html.unescape(re.sub(r"<[^>]+>", "", m.group(1))).strip() if m else ""


def ids(fonts_json: Path) -> list[str]:
    data = json.loads(fonts_json.read_text(encoding="utf-8"))
    out = []
    for r in data["fonts"]:
        m = PAGE_ID.search(r.get("noonnu") or "")
        if m and m.group(1) not in out:
            out.append(m.group(1))
    return out


def main(argv: list[str]) -> int:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if not argv:
        print(__doc__.strip(), file=sys.stderr)
        return 2
    out = Path(argv[1]) if len(argv) > 1 else DEFAULT_DIR
    out.mkdir(parents=True, exist_ok=True)
    todo = [i for i in ids(Path(argv[0])) if not (out / f"{i}.css").exists() and not (out / f"{i}.none").exists()]
    print(f"받을 페이지 {len(todo)}개 → {out}", flush=True)
    fails = []
    for n, fid in enumerate(todo, 1):
        try:
            text = snippet(get(f"{CFG['base']}/font_page/{fid}"))
        except Exception as err:  # 다음 실행에서 다시 받는다
            fails.append(fid)
            print(f"실패 {fid}: {err}", flush=True)
            continue
        finally:
            time.sleep(CFG["delay_sec"])
        if text:
            (out / f"{fid}.css").write_text(text + "\n", encoding="utf-8")
        else:
            (out / f"{fid}.none").write_text("", encoding="utf-8")
        if n % 50 == 0:
            print(f"{n}/{len(todo)}", flush=True)
    print(f"끝 — 실패 {len(fails)} {fails[:20]}")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
