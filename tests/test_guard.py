"""hooks/guard.py 시험 — 공용 틀이 아닌 보기 화면, 순서 어김, 스킬 프로젝트 밖은 통과."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

GUARD = Path(__file__).resolve().parent.parent / "hooks" / "guard.py"


def hook(tool: str, **inp: object) -> subprocess.CompletedProcess:
    data = json.dumps({"tool_name": tool, "tool_input": inp}, ensure_ascii=False).encode("utf-8")
    return subprocess.run([sys.executable, str(GUARD)], input=data, capture_output=True)


def brief(root: Path) -> None:
    (root / "concept-brief.md").write_text("주 업무\n사이트 꼴: 여러 쪽", encoding="utf-8")


def test_outside_project_passes(tmp_path: Path) -> None:
    assert hook("Write", file_path=str(tmp_path / "mockups" / "index.html"), content="<p>x</p>").returncode == 0


def test_own_viewer_blocked_shared_passes(tmp_path: Path) -> None:
    brief(tmp_path)
    (tmp_path / "formats").mkdir()
    own = hook("Write", file_path=str(tmp_path / "formats" / "board.html"), content="<iframe src=x></iframe>")
    assert own.returncode == 2 and "make_live_board.py" in own.stderr.decode("utf-8")
    ok = hook("Write", file_path=str(tmp_path / "formats" / "보기.html"), content='<script id="board-data">{}</script>')
    assert ok.returncode == 0


def test_edit_that_drops_shared_mark_blocked(tmp_path: Path) -> None:
    brief(tmp_path)
    (tmp_path / "formats").mkdir()
    f = tmp_path / "formats" / "보기.html"
    f.write_text('<script id="board-data">{}</script>', encoding="utf-8")
    r = hook("Edit", file_path=str(f), old_string='<script id="board-data">{}</script>', new_string="<iframe></iframe>")
    assert r.returncode == 2


def test_order_blocked_until_decided(tmp_path: Path) -> None:
    brief(tmp_path)
    mock = hook("Write", file_path=str(tmp_path / "mockups" / "index.html"), content="<p>시안</p>")
    assert mock.returncode == 2 and "먼저" in mock.stderr.decode("utf-8")
    pal = hook("Write", file_path=str(tmp_path / "palette" / "index.html"), content="palette-switcher.js")
    assert pal.returncode == 2
    assert hook("Write", file_path=str(tmp_path / "concept-brief.md"), content="고침").returncode == 0


def test_palette_without_published_source_blocked(tmp_path: Path) -> None:
    """모델이 고른 색(출처 없음)은 팔레트 화면에 못 들어간다(애견미용 19차)."""
    brief(tmp_path)
    cands = [{"id": "A", "name": "숲초록과 민트", "source": "바탕 5색 관계", "roles": {"bg": "#f4f1ea", "action": "#1f4b3f"}}]
    body = f'palette-switcher.js<script type="application/json" id="palettes">{json.dumps(cands, ensure_ascii=False)}</script>'
    r = hook("Write", file_path=str(tmp_path / "palette" / "index.html"), content=body)
    assert r.returncode == 2 and "palettes.py pick" in r.stderr.decode("utf-8")
