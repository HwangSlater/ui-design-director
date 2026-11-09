"""knowledge.py·stage.py·check_site 숫자 규칙 시험 — 부품별로 꺼내고, 단계 표에 분야를 고루 붙이고, 글꼴 이름은 후보가 아니라고 붙인다."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "skills" / "ui-design-director" / "scripts"
sys.path.insert(0, str(SCRIPTS))
import knowledge  # noqa: E402

ALLOWED_STAGES = {"brief", "board", "palette", "design", "main", "review"}


def run(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, "-X", "utf8", *args], capture_output=True, text=True, encoding="utf-8")


def test_data_is_well_formed() -> None:
    rules = knowledge.rules()
    assert len(rules) > 600
    assert len({r["id"] for r in rules}) == len(rules)
    for r in rules:
        assert r["rule"] and r["parts"] and set(r["stages"]) <= ALLOWED_STAGES


def test_ask_by_part() -> None:
    out = run(str(SCRIPTS / "knowledge.py"), "ask", "--part", "form,input", "--top", "5").stdout
    lines = [ln for ln in out.splitlines() if ln.startswith("[")]
    assert len(lines) == 5 and "knowledge.py show" in out


def test_stage_lines_mix_fields() -> None:
    picked = knowledge.pick(set(), "main", None, [], 200)
    tips = knowledge.stage_lines("main", 4)
    fields = {next(r["field"] for r in picked if t.startswith(f"[{r['id']}]")) for t in tips}
    assert len(tips) == 4 and len(fields) == 4


def test_font_names_are_marked() -> None:
    r = {"id": "x", "rule": "Use Pretendard GOV for body", "values": "", "by": "KRDS", "confidence": "sourced"}
    assert "후보 아님" in knowledge.line(r)


def test_stage_table_shows_rules(tmp_path: Path) -> None:
    out = run(str(SCRIPTS / "stage.py"), str(tmp_path)).stdout
    assert "이 단계에서 볼 규칙" in out


def test_number_rules_in_check_site(tmp_path: Path) -> None:
    css = "body{font-size:13px;line-height:1.2} .b{transition:background .9s ease} .f{transition:opacity 1.2s}"
    (tmp_path / "index.html").write_text(f'<!doctype html><html lang="ko"><head><meta name="viewport" content="width=device-width"><title>가게</title><style>{css}</style></head><body><h1>가게</h1><img src="a.jpg" alt="가게"></body></html>', encoding="utf-8")
    out = run(str(SCRIPTS / "check_site.py"), str(tmp_path)).stdout
    assert "body-size" in out and "line-height" in out
    assert out.count("motion-duration") == 1  # 사진 겹쳐 바꾸기(opacity)는 빼고
    json.dumps(out)


def test_korean_part_names() -> None:
    parts, unknown = knowledge.resolve_parts("단추, 입력 양식,첫화면,색,hero")
    assert parts == {"button", "form", "first-screen", "colour"} and not unknown
    # 별칭은 모두 실제 부품 id 를 가리키고, 모든 id 에 한국어 이름이 하나 이상 있다
    ids = knowledge.part_ids()
    assert set(knowledge.PART_ALIASES.values()) <= ids
    assert ids <= set(knowledge.PART_ALIASES.values())
    out = run(str(SCRIPTS / "knowledge.py"), "ask", "--part", "버튼", "--top", "2").stdout
    assert len([ln for ln in out.splitlines() if ln.startswith("[")]) == 2


def test_unknown_part_suggests_nearest() -> None:
    res = run(str(SCRIPTS / "knowledge.py"), "ask", "--part", "buton")
    assert res.returncode == 1 and "button" in res.stdout and "맞는 규칙 없음" not in res.stdout
    assert "button" in knowledge.nearest_parts("buttons")
