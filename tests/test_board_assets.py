"""보기 화면 자산(board·dock) 시험 — 고른 상태에 왼쪽 색 줄을 쓰지 않는지, 휴대폰 폭 규칙과 실제 사이트 썸네일·막대 자리 비우기가 남아 있는지."""
from __future__ import annotations

import re
from pathlib import Path

ASSETS = Path(__file__).resolve().parent.parent / "skills" / "ui-design-director" / "assets"
CSS = {name: (ASSETS / name).read_text(encoding="utf-8") for name in ("board.css", "dock.css")}

# 왼쪽 가장자리 색 줄: box-shadow: inset 3px 0 0 … / border-left: 3px solid …
LEFT_STROKE = re.compile(r"box-shadow:[^;]*inset\s+[1-9]\d*px\s+0(px)?\s+0|border-left(-color)?\s*:\s*(?!0|none)", re.I)


def test_no_left_edge_stroke() -> None:
    for name, css in CSS.items():
        assert not LEFT_STROKE.search(css), f"{name}: 고른 상태는 채움·굵기·체크로 — 왼쪽 색 줄을 쓰지 않는다"


def test_phone_width_rules() -> None:
    dock = CSS["dock.css"]
    m = re.search(r"@media \(max-width: 600px\) \{(.*?)\n\}", dock, re.S)
    assert m, "dock.css 에 휴대폰 폭 규칙이 없음"
    block = m.group(1)
    assert "flex-wrap: wrap" in block, "휴대폰 폭에서 막대가 줄을 바꾸지 않음"
    assert "--v-ctl: var(--v-touch)" in block and "--v-touch: 44px" in dock, "휴대폰 폭 누르는 자리가 44px 가 아님"
    assert "@media (max-width: 600px)" in CSS["board.css"], "board.css 에 휴대폰 폭 틀 규칙이 없음"


def test_stage_reserves_dock_space() -> None:
    assert re.search(r"\.v-stage \{[^}]*bottom: calc\(var\(--v-dock-space", CSS["board.css"]), "무대가 막대 높이만큼 비우지 않음"
    dock_js = (ASSETS / "dock.js").read_text(encoding="utf-8")
    assert "--v-dock-space" in dock_js and "ResizeObserver" in dock_js


def test_board_live_thumbs_and_resize() -> None:
    js = (ASSETS / "board.js").read_text(encoding="utf-8")
    assert "thumbs/${encodeURIComponent(cand.id)}.jpg" in js, "실제 사이트 모드 썸네일을 thumbs/ 에서 찾지 않음"
    assert "THUMB_RETRY_MS" in js, "썸네일이 생길 때까지 다시 불러 보지 않음"
    assert "new ResizeObserver" in js, "칸 크기가 바뀌어도 틀을 다시 맞추지 않음"
    assert 'matchMedia(NARROW)' in js, "좁은 창에서 휴대폰 보기로 시작하지 않음"


def test_candidate_issues_flag_unknown_local_sites() -> None:
    """이름난 근거 없는 동네 사이트·해외 추천을 알린다(애견미용 18차)."""
    import make_live_board as mlb
    weak = {"market": "한국", "candidates": [
        {"title": "Dog Salon V.I.D.", "kind": "real", "region": "일본", "recommended": True},
        {"title": "도그넷", "kind": "real", "region": "한국"},
        {"title": "Groomora", "kind": "template"}]}
    lines = " ".join(mlb.candidate_issues(weak))
    assert "이름난 근거" in lines and "이름난 후보가 0개" in lines and "추천 후보 「Dog Salon V.I.D.」" in lines
    good = {"market": "한국", "candidates": [
        {"title": "카카오헤어샵", "kind": "neighbour", "known": "예약 앱 선두", "region": "한국", "recommended": True},
        {"title": "핏펫", "kind": "neighbour", "known": "반려 브랜드", "region": "한국"},
        {"title": "Rover", "kind": "neighbour", "known": "미국 반려 돌봄 선두", "region": "미국"},
        {"title": "Groomora", "kind": "template"}]}
    assert mlb.candidate_issues(good) == []
