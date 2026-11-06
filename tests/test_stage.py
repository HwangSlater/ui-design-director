"""stage.py 시험 — 단계 판단, 순서 어김, 공용 틀이 아닌 화면, --require·--decide."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

STAGE = Path(__file__).resolve().parent.parent / "skills" / "ui-design-director" / "scripts" / "stage.py"


def run(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, "-X", "utf8", str(STAGE), *args], capture_output=True, text=True, encoding="utf-8")


def test_empty_project_starts_at_brief(tmp_path: Path) -> None:
    r = run(str(tmp_path))
    assert r.returncode == 0
    assert "[ ] 맥락 정리" in r.stdout and "다음: concept-brief.md" in r.stdout


def test_own_viewer_and_order_are_flagged(tmp_path: Path) -> None:
    (tmp_path / "concept-brief.md").write_text("주 업무", encoding="utf-8")
    (tmp_path / "formats").mkdir()
    (tmp_path / "formats" / "own.html").write_text("<iframe src=x></iframe>", encoding="utf-8")
    (tmp_path / "mockups").mkdir()
    (tmp_path / "mockups" / "index.html").write_text("<p>시안</p>", encoding="utf-8")
    out = run(str(tmp_path)).stdout
    assert "공용 틀이 아님: formats" in out
    assert "순서 어김: 메인 페이지 시안" in out


def test_require_and_decide(tmp_path: Path) -> None:
    (tmp_path / "concept-brief.md").write_text("주 업무", encoding="utf-8")
    (tmp_path / "formats").mkdir()
    (tmp_path / "formats" / "보기.html").write_text('<script id="board-data">{}</script>', encoding="utf-8")
    assert run(str(tmp_path), "--require", "material").returncode == 1
    assert run(str(tmp_path), "--decide", "base", "3 Norm").returncode == 0
    assert json.loads((tmp_path / "decisions.json").read_text(encoding="utf-8"))["base"] == "3 Norm"
    assert run(str(tmp_path), "--require", "material").returncode == 0
    assert "[x] 바탕 확정" in run(str(tmp_path)).stdout
