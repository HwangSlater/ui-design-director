"""stage.py --decide 시험 — 깨진 decisions.json 을 덮어쓰지 않는지, 모르는 단계를 거절하는지, missing_before."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent.parent / "skills" / "ui-design-director" / "scripts"
STAGE = SCRIPTS / "stage.py"
sys.path.insert(0, str(SCRIPTS))
import stage  # noqa: E402


def run(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, "-X", "utf8", str(STAGE), *args], capture_output=True, text=True, encoding="utf-8")


def test_broken_decisions_not_overwritten(tmp_path: Path) -> None:
    broken = '{"base": "3 Norm",'  # 끝이 잘린 JSON
    (tmp_path / "decisions.json").write_text(broken, encoding="utf-8")
    r = run(str(tmp_path), "--decide", "palette", "B 숲")
    assert r.returncode == 1 and "깨짐" in r.stderr
    assert (tmp_path / "decisions.json").read_text(encoding="utf-8") == broken
    assert "깨짐" in run(str(tmp_path)).stdout


def test_unknown_stage_rejected(tmp_path: Path) -> None:
    r = run(str(tmp_path), "--decide", "colour", "B 숲")
    assert r.returncode == 2 and "모르는 단계" in r.stderr
    assert not (tmp_path / "decisions.json").exists()


def test_missing_before(tmp_path: Path) -> None:
    assert stage.missing_before(tmp_path, "brief") == []
    assert stage.missing_before(tmp_path, "base") == ["brief", "board"]
    (tmp_path / "concept-brief.md").write_text("주 업무\n사이트 꼴: 여러 쪽", encoding="utf-8")
    assert stage.missing_before(tmp_path, "base") == ["board"]


def test_unfilled_template_is_not_material(tmp_path: Path) -> None:
    fm = tmp_path / "formats"
    (fm / "snapshot" / "base-1280").mkdir(parents=True)
    (fm / "snapshot" / "base-1280" / "index.html").write_text("<p></p>", encoding="utf-8")
    (fm / "바탕-움직임.md").write_text("움직임", encoding="utf-8")
    (fm / "바탕-구성.md").write_text(f"{stage.TEMPLATE_MARK}\n# 구성", encoding="utf-8")
    assert stage.status(tmp_path)[0]["material"] is False
    (fm / "바탕-구성.md").write_text("# 구성", encoding="utf-8")
    assert stage.status(tmp_path)[0]["material"] is True


def test_decide_only_base_and_palette(tmp_path: Path) -> None:
    # 디자이너가 --decide board 로 남겨 바탕이 안 정해진 채 남았다
    r = run(str(tmp_path), "--decide", "board", "3 Norm")
    assert r.returncode == 2 and '--decide base "<번호 이름>"' in r.stderr
    assert not (tmp_path / "decisions.json").exists()
    assert run(str(tmp_path), "--decide", "palette", "B 숲").returncode == 0
    assert run(str(tmp_path), "--decide", "main", "좋아요, 이대로").returncode == 0  # 시안 승인(그 뒤 clear_copies.py)


def project_with_board(root: Path) -> None:
    (root / "concept-brief.md").write_text("주 업무\n사이트 꼴: 여러 쪽", encoding="utf-8")
    (root / "formats").mkdir()
    (root / "formats" / "보기.html").write_text('<script id="board-data">{}</script>', encoding="utf-8")


def test_guard_blocks_material_before_base(tmp_path: Path) -> None:
    project_with_board(tmp_path)
    out = tmp_path / "formats" / "snapshot"
    assert "바탕 확정" in (stage.output_block(out, "material") or "")
    r = run("--guard", "material", str(out))
    assert r.returncode == 1 and "바탕 확정" in r.stderr
    assert stage.output_block(tmp_path / "mockups" / "x.md", "material") is None  # formats/ 밖은 보지 않는다
    (tmp_path / "decisions.json").write_text('{"base": "1 가"}', encoding="utf-8")
    assert stage.output_block(out, "material") is None
    assert run("--guard", "material", str(out)).returncode == 0


def test_guard_ignores_folders_outside_projects(tmp_path: Path) -> None:
    (tmp_path / "formats").mkdir()  # 표시 파일(concept-brief.md·decisions.json·board-spec.json)이 없으면 스킬 프로젝트가 아니다
    assert stage.output_block(tmp_path / "formats" / "snapshot", "material") is None
    assert run("--guard", "material", str(tmp_path / "formats" / "a.md")).returncode == 0
