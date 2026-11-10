#!/usr/bin/env python3
"""시안 승인 뒤 남의 사이트 사본(저장본·캡처·움직임 그림·썸네일)을 지운다. 지우기 전에 점검이 쓰는 바탕 사실을 남긴다.

    python clear_copies.py <project folder>          # 승인(stage.py --decide main) 뒤에만 지운다
    python clear_copies.py <project folder> --dry    # 지울 것만 보여 준다

손으로 지우자 「바탕에도 01–04 가 있었다」는 근거가 사라져 점검이 다시 걸렸고, 단계 표가 「바탕 자료」를 빈칸으로 돌렸다(치과 17차).
그래서 formats/바탕-표지.json 에 사실을 먼저 남기고(site_shape.base_facts), 정해진 사본 폴더만 지운다.
"""
from __future__ import annotations

import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import utf8_console  # noqa: E402
from site_shape import base_facts  # noqa: E402
from stage import decisions  # noqa: E402

# formats/ 안의 사본 폴더 — 바탕 저장본, 바탕·팔레트 캡처, 움직임 그림, 보기 화면 썸네일. 우리 것(구성 표·기록)은 남긴다
# 후보를 고를 때 따로 찍은 캡처 폴더(check·shots)와 formats/ 바로 아래 그림도 사본이다 — 남아서 손으로 지울 뻔했다(애견미용 18차)
COPIES = ("snapshot", "base-cap", "pal-cap", "바탕-움직임-움직임", "thumbs", "check", "shots")
PICTURES = (".jpg", ".jpeg", ".png", ".webp")


def copies(root: Path) -> list[Path]:
    fm = root / "formats"
    if not fm.is_dir():
        return []
    return [fm / name for name in COPIES if (fm / name).is_dir()] + sorted(p for p in fm.iterdir() if p.is_file() and p.suffix.lower() in PICTURES)


def main(argv: list[str]) -> int:
    utf8_console()
    if not argv:
        print(__doc__.strip().splitlines()[2].strip(), file=sys.stderr)
        return 2
    root, dry = Path(argv[0]).resolve(), "--dry" in argv
    found = copies(root)
    if not found:
        print("지울 사본 없음")
        return 0
    if "main" not in decisions(root) and not dry:
        print("아직 시안 승인 전이라 지우지 않음 — 의뢰인이 승인하면: python stage.py . --decide main \"<승인한 말>\"", file=sys.stderr)
        return 1
    marks = base_facts(root)
    for p in found:
        print(f"{'지울 것' if dry else '지움'}: {p.relative_to(root)}")
        if not dry:
            shutil.rmtree(p) if p.is_dir() else p.unlink()
    print(f"바탕 표지 남김: formats/바탕-표지.json (번호 줄 {'있음' if marks.get('numbered') else '없음'}, 아이콘 줄 {'있음' if marks.get('icon_row') else '없음'})")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
