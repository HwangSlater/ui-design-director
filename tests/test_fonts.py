"""fonts.py·preflight·훅 시험 — AI 글꼴은 후보에서 빠지고, 글꼴 선언에 쓰면 걸리고, 의뢰인 글꼴은 풀린다."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "skills" / "ui-design-director" / "scripts"
sys.path.insert(0, str(SCRIPTS))
import fonts  # noqa: E402


def run(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, "-X", "utf8", *args], capture_output=True, text=True, encoding="utf-8")


def test_pick_leaves_out_ai_fonts() -> None:
    out = run(str(SCRIPTS / "fonts.py"), "pick", "--style", "고딕", "--top", "40").stdout
    assert "글꼴 후보" in out
    for name in ("Pretendard", "본고딕", "스포카", "나눔고딕"):
        assert f"- {name}" not in out
    assert "나눔바른고딕" in out  # 상위 사이트에서 쓰는 무료 글꼴은 남는다


def test_declarations_only() -> None:
    css = 'body{font-family:"Pretendard Variable",sans-serif} :root{--f-heading:"Wanted Sans"}'
    assert fonts.ai_fonts_in(css) == ["Pretendard", "Wanted Sans"]
    assert fonts.ai_fonts_in("<p>Inter 같은 글꼴은 쓰지 않았습니다</p>") == []  # 본문 글은 걸지 않는다
    assert fonts.ai_fonts_in('<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400">') == ["Noto Sans KR"]
    assert fonts.ai_fonts_in('{"heading": "\\"G마켓 산스\\", sans-serif"}') == []


def test_client_font_is_allowed(tmp_path: Path) -> None:
    (tmp_path / "concept-brief.md").write_text("의뢰인 글꼴: Pretendard", encoding="utf-8")
    (tmp_path / "mockups").mkdir()
    css = tmp_path / "mockups" / "tokens.css"
    css.write_text('body{font-family:"Pretendard",sans-serif;--f-x:"SUIT"}', encoding="utf-8")
    r = run(str(SCRIPTS / "fonts.py"), "check", str(tmp_path / "mockups"))
    assert r.returncode == 1 and "SUIT" in r.stdout and "Pretendard" not in r.stdout


def test_hook_blocks_ai_font_in_mockup(tmp_path: Path) -> None:
    (tmp_path / "concept-brief.md").write_text("주 업무", encoding="utf-8")
    data = {"tool_name": "Write", "tool_input": {"file_path": str(tmp_path / "DESIGN.md"),
            "content": "--f-body: \"Noto Sans KR\", sans-serif;"}}
    r = subprocess.run([sys.executable, str(ROOT / "hooks" / "guard.py")], input=json.dumps(data, ensure_ascii=False).encode("utf-8"), capture_output=True)
    assert r.returncode == 2 and "AI 글꼴" in r.stderr.decode("utf-8")


def test_preflight_flags_ai_font(tmp_path: Path) -> None:
    (tmp_path / "concept-brief.md").write_text("주 업무", encoding="utf-8")
    (tmp_path / "palette").mkdir()
    (tmp_path / "palette" / "index.html").write_text('<script id="fonts">[{"heading": "SUIT, sans-serif"}]</script>', encoding="utf-8")
    out = run(str(SCRIPTS / "preflight.py"), str(tmp_path)).stdout
    assert "AI 글꼴: palette" in out and "SUIT" in out
