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


def test_refresh_fills_only_empty_size_cells(tmp_path: Path) -> None:
    fm = tmp_path / "formats"
    fm.mkdir()
    r = run(str(tmp_path), URL)  # 추출 없이 만든 빈 틀
    assert r.returncode == 0 and "--refresh" in r.stdout
    md = fm / "바탕-구성.md"
    text = md.read_text(encoding="utf-8").replace("| 1 머리(메뉴) | | |  |","| 1 머리(메뉴) | 8% | | 15px / 13px |")
    md.write_text(text + "\n디자이너 메모\n", encoding="utf-8")
    extract = {"roles": {"heading": [{"tag": "h1", "size": "56px"}, {"tag": "h2", "size": "32px"}], "body": [{"tag": "p", "size": "17px"}]}}
    (fm / "추출-390.json").write_text(json.dumps(extract), encoding="utf-8")
    r = run(str(tmp_path), "--refresh")
    assert r.returncode == 0, r.stderr
    out = md.read_text(encoding="utf-8")
    assert "| 1 머리(메뉴) | 8% | | 15px / 13px |" in out  # 적은 칸은 그대로
    assert "| 2 첫 화면 | | | 56px / 17px |" in out and "32px / 17px" in out
    assert "디자이너 메모" in out and "추출-390.json 에서" in out
    assert "| 구역(위→아래) | 높이 비율 | 사진 비율 | 글자 크기(제목/본문) | 칸 수 | 하는 일 |" in out


def test_refresh_without_extraction_says_so(tmp_path: Path) -> None:
    fm = tmp_path / "formats"
    fm.mkdir()
    run(str(tmp_path), URL)
    r = run(str(tmp_path), "--refresh")
    assert r.returncode == 1 and "추출-1280.json" in r.stderr


def test_rejects_non_http(tmp_path: Path) -> None:
    assert run(str(tmp_path), "file:///etc/passwd").returncode == 2


A = "https://a.example"  # lint:allow url 시험용 가짜 주소(접속하지 않음)
B = "https://b.example"  # lint:allow url 시험용 가짜 주소(접속하지 않음)
SPEC = {"pages": [{"key": "home", "label": "첫 화면"}, {"key": "work", "label": "작업"}],
        "market": "한국",
        "candidates": [{"id": "1", "title": "가람", "kind": "real", "known": "x", "region": "한국", "recommended": True,
                        "urls": {"home": f"{A}/ko/home", "work": f"{A}/work"}},
                       {"id": "2", "title": "Norm Architects", "kind": "real", "known": "x", "region": "한국", "urls": {"work": f"{B}/w", "home": f"{B}/studio"}},
                       {"id": "3", "title": "셋째", "kind": "real", "known": "x", "region": "한국", "urls": {"home": f"{A}/3"}}]}


def decided_project(root: Path) -> Path:
    fm = root / "formats"
    fm.mkdir()
    (root / "concept-brief.md").write_text("주 업무\n사이트 꼴: 여러 쪽", encoding="utf-8")
    (fm / "보기.html").write_text('<script id="board-data">{}</script>', encoding="utf-8")
    (fm / "board-spec.json").write_text(json.dumps(SPEC), encoding="utf-8")
    return fm


def test_url_from_board_decision(tmp_path: Path) -> None:
    # 보기 화면 「확정」: 사이트 첫 화면이 아니라 보기 화면이 띄운 페이지(첫 화면 칸) 주소를 쓴다
    fm = decided_project(tmp_path)
    (fm / "decision.json").write_text(json.dumps({"label": "2 Norm Architects", "choice": {"candidate": "2", "title": "Norm Architects"}}), encoding="utf-8")
    r = run(str(tmp_path))
    assert r.returncode == 0, r.stderr
    assert f"바탕 주소: {B}/studio" in r.stdout
    assert json.loads((fm / "jobs-base.json").read_text(encoding="utf-8"))[0]["url"] == f"{B}/studio"
    assert "2 Norm Architects" in (fm / "바탕-구성.md").read_text(encoding="utf-8")


def test_url_from_decide_text(tmp_path: Path) -> None:
    decided_project(tmp_path)
    (tmp_path / "decisions.json").write_text(json.dumps({"base": "1번 가람"}, ensure_ascii=False), encoding="utf-8")
    r = run(str(tmp_path))
    assert r.returncode == 0, r.stderr
    assert f"바탕 주소: {A}/ko/home" in r.stdout


def test_url_from_old_spec_form(tmp_path: Path) -> None:
    fm = decided_project(tmp_path)
    (fm / "board-spec.json").write_text(json.dumps({"market": "한국", "candidates": [
        {"n": "3", "name": "오후", "pages": {"홈": f"{A}/shop/home"}, "kind": "real", "known": "x", "region": "한국", "recommended": True},
        {"n": "4", "name": "넷", "pages": {"홈": f"{A}/4"}, "kind": "real", "known": "x", "region": "한국"},
        {"n": "5", "name": "다섯", "pages": {"홈": f"{A}/5"}, "kind": "real", "known": "x", "region": "한국"}]}, ensure_ascii=False), encoding="utf-8")
    (fm / "decision.json").write_text(json.dumps({"label": "3 오후", "choice": {"candidate": "3"}}, ensure_ascii=False), encoding="utf-8")
    assert f"바탕 주소: {A}/shop/home" in run(str(tmp_path)).stdout


def test_stops_before_base_is_decided(tmp_path: Path) -> None:
    fm = decided_project(tmp_path)
    r = run(str(tmp_path), URL)
    assert r.returncode == 1 and "바탕 확정" in r.stderr
    assert not (fm / "jobs-base.json").exists() and not (fm / "바탕-구성.md").exists()
