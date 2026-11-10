"""palettes.py 시험 — 색상은 공개 팔레트에서만, 모델 단골 색 무리는 고르기에서 빼고, 출처 없는 후보는 걸린다(애견미용 19차)."""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "skills" / "ui-design-director" / "scripts"))
import palettes  # noqa: E402

CODE = "5f6f52a9b388fefae0b99470"


def page(cands: list[dict]) -> str:
    return f'<script type="application/json" id="palettes">{json.dumps(cands, ensure_ascii=False)}</script>'


def test_sourced_palette_passes_with_neutrals_and_shades() -> None:
    roles = {"bg": "#fefae0", "surface": "#ffffff", "text": "#1c1c1c", "action": "#4b5841", "on-action": "#ffffff", "accent": "#b99470"}
    assert palettes.problems(page([{"id": "A", "source": f"https://colorhunt.co/palette/{CODE}", "roles": roles}])) == []


def test_model_colours_without_source_are_flagged() -> None:
    roles = {"bg": "#f4f1ea", "action": "#1f4b3f", "accent": "#cfe6da"}  # 19차 「숲초록과 민트」
    out = palettes.problems(page([{"id": "A", "name": "숲초록과 민트", "source": "barkbus 의 5색 관계", "roles": roles}]))
    assert len(out) == 1 and "출처 없음" in out[0]


def test_foreign_colour_in_sourced_palette_is_flagged() -> None:
    roles = {"bg": "#fefae0", "action": "#8c3626"}  # 벽돌은 이 팔레트 색이 아니다
    out = palettes.problems(page([{"id": "B", "source": f"https://colorhunt.co/palette/{CODE}", "roles": roles}]))
    assert len(out) == 1 and "action #8c3626" in out[0]


def test_client_colours_are_allowed() -> None:
    assert palettes.problems(page([{"id": "C", "source": "의뢰인 색(간판 빨강)", "roles": {"action": "#d40000"}}])) == []


def test_pick_skips_model_families_and_flat_pastels() -> None:
    rows = palettes.pick([], 60, "시험")
    assert rows
    for p in rows:
        cs = [palettes.rgb(c) for c in p["colors"]]
        assert not palettes.ai_hits(cs)
        assert max(palettes.hls(c)[1] for c in cs) - min(palettes.hls(c)[1] for c in cs) >= palettes.SPREAD
