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
    h = copy_check.FIRST_SCREEN.get(width, 900)
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
    assert any("베낀 티(PC)" in line for line in copy_check.check_project(root))


def test_own_colours_pass(tmp_path: Path) -> None:
    root = project(tmp_path, ("#f4efe6", "#ffffff", "#c2410c"))
    assert copy_check.check_project(root) == []


def test_palette_candidate_equal_to_base(tmp_path: Path) -> None:
    pals = [{"id": "A", "name": "검정과 파랑", "roles": {"bg": "#0b0b0b", "action": "#1a73e8"}},
            {"id": "B", "name": "우리 색", "roles": {"bg": "#f4efe6", "action": "#c2410c"}}]
    out = copy_check.palette_copies(project(tmp_path, ("#f4efe6", "#ffffff", "#c2410c"), pals))
    assert len(out) == 1 and "A 검정과 파랑" in out[0]


def design(tmp: Path, body: str) -> Path:
    (tmp / "DESIGN.md").write_text(f"# 디자인\n\n## 바탕에서 바꾼 곳\n{body}\n## 부품 출처\n색 계열 이름 처리 칸 마감 대표 요소\n", encoding="utf-8")
    return tmp


def test_own_finish_needs_two(tmp_path: Path) -> None:
    out = copy_check.own_finish(design(tmp_path, "우리 것(마감)\n- 색 계열: 주황\n"))
    assert len(out) == 1 and "우리 것 마감이 둘 미만" in out[0]  # 다음 절(부품 출처)의 낱말은 세지 않는다
    assert copy_check.own_finish(design(tmp_path, "우리 것(마감)\n- 색 계열: 주황\n- 칸 마감: 둥근 칸\n")) == []


def test_real_logo_name_layer_not_ours(tmp_path: Path) -> None:
    body = "우리 것(마감)\n- 색 계열: 주황\n- 이름 처리: 팀 이름\n\n의뢰인 요청으로 실제 로고를 견본으로 씀\n"
    out = copy_check.own_finish(design(tmp_path, body))
    assert len(out) == 1 and "이름 처리는 세지 않음" in out[0]


def test_no_section_left_to_preflight(tmp_path: Path) -> None:
    (tmp_path / "DESIGN.md").write_text("# 디자인\n", encoding="utf-8")
    assert copy_check.own_finish(tmp_path) == []


def test_desktop_width_may_differ(tmp_path: Path) -> None:
    """바탕은 1280, 우리는 1440 으로 찍어도 PC 끼리 견준다(NBA 12차에서 PC 를 건너뛰었다)."""
    page(tmp_path / "formats" / "base-cap" / "base-home-1280.jpg", "#0b0b0b", "#1c1c1c", "#1a73e8")
    page(tmp_path / "mockups" / "보낼-그림" / "main-1440.jpg", "#0b0b0b", "#1c1c1c", "#1a73e8", width=1440)
    assert any("베낀 티(PC)" in line for line in copy_check.check_project(tmp_path))


def long_page(path: Path, band: str | None, width: int = 1280) -> Path:
    """흰 페이지 전체 — band 가 있으면 폭 가득한 옅은 색 띠(300px)와 그 안 가운데 글줄."""
    im = Image.new("RGB", (width, 2400), "#ffffff")
    d = ImageDraw.Draw(im)
    d.rectangle((0, 0, width, 600), fill="#203040")  # 첫 화면 사진 자리(진한 색)
    if band:
        d.rectangle((0, 1200, width, 1500), fill=band)
        d.rectangle((100, 1260, width - 100, 1290), fill="#333333")  # 띠 안 글은 가운데에
    path.parent.mkdir(parents=True, exist_ok=True)
    im.save(path)
    return path


def test_pale_band_missing_in_base_is_flagged(tmp_path: Path) -> None:
    base = long_page(tmp_path / "formats" / "base-cap" / "base-home-1280.png", None)
    ours = long_page(tmp_path / "mockups" / "보낼-그림" / "main-1280.png", "#eef4f2")
    assert copy_check.pale_bands(base, 1280, ours, 1280) == [("#eef4f2", 1)]
    assert any(line.startswith("옅은 띠(PC): #eef4f2 줄 1개 — 바탕에 없음") for line in copy_check.check_project(tmp_path))


def test_pale_band_the_base_has_passes(tmp_path: Path) -> None:
    base = long_page(tmp_path / "base.png", "#f4f0ef")
    ours = long_page(tmp_path / "ours.png", "#f3f1ee")
    assert copy_check.pale_bands(base, 1280, ours, 1280) == []


def test_white_and_dark_bands_are_not_pale(tmp_path: Path) -> None:
    base = long_page(tmp_path / "base.png", None)
    assert copy_check.pale_bands(base, 1280, long_page(tmp_path / "w.png", "#fcfcfc"), 1280) == []
    assert copy_check.pale_bands(base, 1280, long_page(tmp_path / "d.png", "#1f4a50"), 1280) == []



def stacked_page(path: Path, bands: list[str], width: int = 1280) -> Path:
    """흰 페이지에 폭 가득 띠를 차례로(띠 사이에 흰 구역 200px)."""
    im = Image.new("RGB", (width, 600 + len(bands) * 500 + 200), "#ffffff")
    d = ImageDraw.Draw(im)
    for i, colour in enumerate(bands):
        y = 600 + i * 500
        d.rectangle((0, y, width, y + 300), fill=colour)
    path.parent.mkdir(parents=True, exist_ok=True)
    im.save(path)
    return path


def test_stacked_strong_bands_flagged(tmp_path: Path) -> None:
    """갈색·벽돌·짙은 갈색 띠가 잇달고 바탕은 하나뿐이면 색 띠 쌓기(플리마켓 14차). 맨 아래 흰 구역은 바닥글로 빠진다."""
    stacked_page(tmp_path / "formats" / "base-cap" / "base-home-1280.png", ["#383838"])
    stacked_page(tmp_path / "mockups" / "보낼-그림" / "main-1280.png", ["#6d5a54", "#7f3a2a", "#2b2225"])
    assert any(line.startswith("색 띠 쌓기(PC): 진한 띠 3개") for line in copy_check.check_project(tmp_path))


def test_stacked_bands_the_base_has_or_broken_pass(tmp_path: Path) -> None:
    base = stacked_page(tmp_path / "base.png", ["#203040", "#304050", "#102030"])
    ours = stacked_page(tmp_path / "ours.png", ["#6d5a54", "#7f3a2a", "#2b2225"])
    assert copy_check.stacked_bands(base, 1280, ours, 1280) == ([], 0)
    plain = stacked_page(tmp_path / "plain.png", [])
    broken = stacked_page(tmp_path / "broken.png", ["#6d5a54", "#eef4f2", "#7f3a2a", "#eef4f2", "#2b2225"])  # 옅은 띠가 하나씩 끊음
    assert copy_check.stacked_bands(plain, 1280, broken, 1280) == ([], 0)


def test_captures_named_by_view(tmp_path: Path) -> None:
    """「1-휴대폰.jpg」「2-PC.jpg」처럼 폭 없이 화면 종류로 적은 캡처도 찾고, 폭은 그림 너비로(치과 15차)."""
    folder = tmp_path / "보낼-그림"
    page(folder / "1-휴대폰.jpg", "#ffffff", "#eeeeee", "#000000", width=780)  # 2배 캡처
    page(folder / "2-PC.jpg", "#ffffff", "#eeeeee", "#000000", width=1300)
    page(folder / "3-spec.jpg", "#ffffff", "#eeeeee", "#000000", width=900)  # spec 안의 pc 는 PC 가 아니다
    assert copy_check.find_view(folder, "휴대폰") == (folder / "1-휴대폰.jpg", 390)
    assert copy_check.find_view(folder, "PC") == (folder / "2-PC.jpg", 1300)
    (folder / "2-PC.jpg").unlink()
    page(folder / "모바일-이어붙임.jpg", "#ffffff", "#eeeeee", "#000000", width=1210)
    assert copy_check.find_view(folder, "PC") == (None, None)
    assert copy_check.css_width(folder / "모바일-이어붙임.jpg", "휴대폰") == 390  # 이어 붙인 그림은 기본 폭
