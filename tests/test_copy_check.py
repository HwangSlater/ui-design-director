"""copy_check.py 시험 — 첫 화면 색·마감이 바탕과 같으면 베낀 티, 우리 색이면 통과, 바탕 그대로인 팔레트 후보를 잡는다."""
from __future__ import annotations

import json
import sys
from pathlib import Path

from PIL import Image, ImageDraw

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "skills" / "ui-design-director" / "scripts"))
import copy_check  # noqa: E402


def page(path: Path, bg: str, card: str, accent: str, width: int = 1280) -> Path:
    """머리 띠·카드 두 줄·강조 단추가 있는 첫 화면 그림."""
    h = copy_check.FIRST_SCREEN[width]
    im = Image.new("RGB", (width, h), bg)
    d = ImageDraw.Draw(im)
    d.rectangle((0, 0, width, 70), fill=card)
    for row in range(4):
        for col in range(2):
            x, y = 60 + col * (width // 2), 120 + row * 180
            d.rectangle((x, y, x + width // 2 - 120, y + 150), fill=card)
            d.rectangle((x + 20, y + 20, x + 220, y + 40), fill="#dddddd")
    d.rectangle((width - 220, 18, width - 40, 52), fill=accent)
    path.parent.mkdir(parents=True, exist_ok=True)
    im.save(path)
    return path


def project(tmp: Path, ours: tuple[str, str, str], palettes: list[dict] | None = None) -> Path:
    page(tmp / "formats" / "base-cap" / "base-home-1280.jpg", "#0b0b0b", "#1c1c1c", "#1a73e8")
    page(tmp / "mockups" / "보낼-그림" / "main-1280.png", *ours)
    if palettes is not None:
        (tmp / "palette").mkdir()
        (tmp / "palette" / "index.html").write_text(f'<script type="application/json" id="palettes">{json.dumps(palettes, ensure_ascii=False)}</script>', encoding="utf-8")
    return tmp


def test_same_finish_is_copy(tmp_path: Path) -> None:
    root = project(tmp_path, ("#0b0b0b", "#1c1c1c", "#1a73e8"))
    assert any("베낀 티(1280px)" in line for line in copy_check.check_project(root))


def test_own_colours_pass(tmp_path: Path) -> None:
    root = project(tmp_path, ("#f4efe6", "#ffffff", "#c2410c"))
    assert copy_check.check_project(root) == []


def test_palette_candidate_equal_to_base(tmp_path: Path) -> None:
    pals = [{"id": "A", "name": "검정과 파랑", "roles": {"bg": "#0b0b0b", "action": "#1a73e8"}},
            {"id": "B", "name": "우리 색", "roles": {"bg": "#f4efe6", "action": "#c2410c"}}]
    out = copy_check.palette_copies(project(tmp_path, ("#f4efe6", "#ffffff", "#c2410c"), pals))
    assert len(out) == 1 and "A 검정과 파랑" in out[0]
