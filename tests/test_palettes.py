"""palettes.py 시험 — 색상은 공개 팔레트에서만, 모델 단골 색 무리는 고르기에서 빼고, 출처 없는 후보는 걸린다(애견미용 19차)."""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "skills" / "ui-design-director" / "scripts"))
import palettes  # noqa: E402

CODE = "b82132d2665af2b28cf6ded8"


def page(cands: list[dict]) -> str:
    return f'<script type="application/json" id="palettes">{json.dumps(cands, ensure_ascii=False)}</script>'


def test_sourced_palette_passes_with_neutrals_and_shades() -> None:
    roles = {"bg": "#f6ded8", "surface": "#ffffff", "text": "#1c1c1c", "action": "#9a1b29", "on-action": "#ffffff", "accent": "#f2b28c"}
    assert palettes.problems(page([{"id": "A", "source": f"https://colorhunt.co/palette/{CODE}", "roles": roles}])) == []


def test_model_colours_without_source_are_flagged() -> None:
    roles = {"bg": "#f4f1ea", "action": "#1f4b3f", "accent": "#cfe6da"}  # 19차 「숲초록과 민트」
    out = palettes.problems(page([{"id": "A", "name": "숲초록과 민트", "source": "barkbus 의 5색 관계", "roles": roles}]))
    assert len(out) == 1 and "출처 없음" in out[0]


def test_foreign_colour_in_sourced_palette_is_flagged() -> None:
    roles = {"bg": "#f6ded8", "action": "#2a44b8"}  # 코발트는 이 팔레트 색이 아니다
    out = palettes.problems(page([{"id": "B", "source": f"https://colorhunt.co/palette/{CODE}", "roles": roles}]))
    assert len(out) == 1 and "action #2a44b8" in out[0]


def test_client_colours_are_allowed() -> None:
    assert palettes.problems(page([{"id": "C", "source": "의뢰인 색(간판 빨강)", "roles": {"action": "#d40000"}}])) == []


def test_pick_skips_model_families_and_flat_pastels() -> None:
    rows = palettes.pick([], 60, "시험")
    assert rows
    for p in rows:
        cs = [palettes.rgb(c) for c in p["colors"]]
        assert not palettes.ai_hits(cs)
        assert max(palettes.hls(c)[1] for c in cs) - min(palettes.hls(c)[1] for c in cs) >= palettes.SPREAD


def test_darkened_into_model_green_is_flagged() -> None:
    """쑥색 팔레트를 진하게 해 모델 단골 초록 단추가 됨(애견미용 24차 #4e5b4b)."""
    roles = {"bg": "#f1f3e0", "action": "#4e5b4b"}
    out = palettes.problems(page([{"id": "A", "source": "https://colorhunt.co/palette/f1f3e0d2dcb6a1bc98778873", "roles": roles}]))
    assert any("모델 단골 색" in line for line in out)
