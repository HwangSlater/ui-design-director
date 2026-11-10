"""clear_copies.py 시험 — 승인 전에는 지우지 않고, 지운 뒤에도 바탕 사실(번호 줄)과 「바탕 자료를 모았다」가 남는다(치과 17차)."""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "skills" / "ui-design-director" / "scripts"))
import clear_copies  # noqa: E402
import site_shape  # noqa: E402
import stage  # noqa: E402


def project(root: Path) -> Path:
    fm = root / "formats"
    (fm / "snapshot" / "base-1280").mkdir(parents=True)
    (fm / "snapshot" / "base-1280" / "index.html").write_text("<p>01</p><p>02</p><p>03</p>", encoding="utf-8")
    (fm / "base-cap").mkdir()
    (fm / "shots").mkdir()
    (fm / "check-sheet.jpg").write_bytes(b"x")
    (fm / "바탕-구성.md").write_text("# 구성", encoding="utf-8")
    (fm / "바탕-움직임.md").write_text("움직임", encoding="utf-8")
    return root


def test_not_before_approval(tmp_path: Path) -> None:
    root = project(tmp_path)
    assert clear_copies.main([str(root)]) == 1
    assert (root / "formats" / "snapshot").is_dir()


def test_facts_survive_deletion(tmp_path: Path) -> None:
    root = project(tmp_path)
    (root / "decisions.json").write_text(json.dumps({"main": "좋아요"}), encoding="utf-8")
    assert clear_copies.main([str(root)]) == 0
    assert not any((root / "formats" / n).exists() for n in ("snapshot", "base-cap", "shots", "check-sheet.jpg"))
    assert (root / "formats" / "바탕-구성.md").is_file()  # 우리 것은 남긴다
    assert site_shape.base_numbered(root) is True
    assert stage.status(root)[0]["material"] is True


def test_hand_deletion_after_a_check_keeps_facts(tmp_path: Path) -> None:
    """점검이 한 번이라도 돌았으면 손으로 지워도 사실이 남는다."""
    root = project(tmp_path)
    assert site_shape.base_numbered(root) is True
    import shutil
    shutil.rmtree(root / "formats" / "snapshot")
    assert site_shape.base_numbered(root) is True
