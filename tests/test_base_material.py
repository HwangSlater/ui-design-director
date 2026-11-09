"""base_material.py 시험 — 두 파일을 만들고, 추출값으로 글자 크기를 채우고, 있는 파일은 덮어쓰지 않는다."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent.parent / "skills" / "ui-design-director" / "scripts" / "base_material.py"
URL = "https://example.com/shop/"  # lint:allow url 시험용 가짜 주소(접속하지 않음)


def run(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, "-X", "utf8", str(SCRIPT), *args], capture_output=True, text=True, encoding="utf-8")


def test_creates_both_files(tmp_path: Path) -> None:
    fm = tmp_path / "formats"
    fm.mkdir()
    extract = {"roles": {"heading": [{"tag": "h1", "size": "56px"}, {"tag": "h2", "size": "32px"}, {"tag": "h2", "size": "32px"}],
                         "body": [{"tag": "p", "size": "17px"}]}}
    (fm / "추출-1280.json").write_text(json.dumps(extract), encoding="utf-8")
    r = run(str(tmp_path), URL, "--name", "3 Norm")
    assert r.returncode == 0, r.stderr
    jobs = json.loads((fm / "jobs-base.json").read_text(encoding="utf-8"))
    assert [j["url"] for j in jobs] == [URL, "https://example.com/"]  # lint:allow url 시험용 가짜 주소
    assert all(j["id"] for j in jobs)
    md = (fm / "바탕-구성.md").read_text(encoding="utf-8")
    assert "| 구역(위→아래) | 높이 비율 | 사진 비율 | 글자 크기(제목/본문) | 칸 수 | 하는 일 |" in md
    assert "## 시각 층" in md and "## 바꿀 곳(n/N)" in md and "3 Norm" in md
    assert "56px / 17px" in md and "32px / 17px" in md
    assert "skeleton.mjs" in r.stdout and "--base" in r.stdout and "snapshot.mjs" in r.stdout


def test_does_not_overwrite(tmp_path: Path) -> None:
    fm = tmp_path / "formats"
    fm.mkdir()
    (fm / "바탕-구성.md").write_text("내가 쓴 구성", encoding="utf-8")
    r = run(str(tmp_path), URL)
    assert r.returncode == 0
    assert "있음, 건너뜀" in r.stdout
    assert (fm / "바탕-구성.md").read_text(encoding="utf-8") == "내가 쓴 구성"
    assert (fm / "jobs-base.json").is_file()


def test_rejects_non_http(tmp_path: Path) -> None:
    assert run(str(tmp_path), "file:///etc/passwd").returncode == 2
