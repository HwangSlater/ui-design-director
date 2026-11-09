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


def palette_page(heading: str, body: str = "serif") -> str:
    fonts_json = json.dumps([{"id": "1", "name": "후보", "heading": heading, "body": body}], ensure_ascii=False)
    return f'<script src="../palette-switcher.js"></script><script type="application/json" id="fonts">{fonts_json}</script>'


def guard(path: Path, content: str) -> subprocess.CompletedProcess:
    data = {"tool_name": "Write", "tool_input": {"file_path": str(path), "content": content}}
    return subprocess.run([sys.executable, str(ROOT / "hooks" / "guard.py")], input=json.dumps(data, ensure_ascii=False).encode("utf-8"), capture_output=True)


def test_unknown_palette_fonts() -> None:
    assert fonts.unknown_fonts(palette_page('"Made Up Grotesk", "나눔바른고딕", serif', "system-ui, sans-serif")) == ["Made Up Grotesk"]
    assert fonts.unknown_fonts(palette_page('"Made Up Grotesk", serif'), {fonts.norm("Made Up Grotesk")}) == []  # 의뢰인 글꼴
    assert fonts.unknown_fonts("<p>글꼴 후보 없음</p>") == []


def test_hook_blocks_font_not_in_table(tmp_path: Path) -> None:
    (tmp_path / "concept-brief.md").write_text("주 업무", encoding="utf-8")
    r = guard(tmp_path / "palette" / "index.html", palette_page('"Made Up Grotesk", serif'))
    assert r.returncode == 2 and "표에 없는 글꼴: Made Up Grotesk — fonts.py pick 에서 고르세요" in r.stderr.decode("utf-8")
    (tmp_path / "concept-brief.md").write_text("주 업무\n의뢰인 글꼴: Made Up Grotesk", encoding="utf-8")
    r = guard(tmp_path / "palette" / "index.html", palette_page('"Made Up Grotesk", serif'))
    assert "표에 없는 글꼴" not in r.stderr.decode("utf-8")  # 의뢰인 글꼴은 지나간다(앞 단계가 안 돼 막히는 것은 따로)


def test_pick_prints_webfont_and_face_prints_css() -> None:
    out = run(str(SCRIPTS / "fonts.py"), "pick", "--style", "고딕", "--top", "5").stdout
    assert "    웹폰트: font-family" in out
    assert out.rstrip().endswith("후보는 이 목록에서만 — fonts.json 을 직접 읽지 마세요")
    face = run(str(SCRIPTS / "fonts.py"), "face", "G마켓 산스")
    assert face.returncode == 0 and "@font-face" in face.stdout and "GMarketSans" in face.stdout
    assert run(str(SCRIPTS / "fonts.py"), "face", "GMarketSans").returncode == 0  # CSS 이름으로도 찾는다
    missing = run(str(SCRIPTS / "fonts.py"), "face", "Made Up Grotesk")
    assert missing.returncode == 1 and "표에 없는 글꼴" in missing.stderr


def test_webfont_css_name_counts_as_known() -> None:
    assert fonts.unknown_fonts(palette_page("'GMarketSans', sans-serif")) == []


def test_merge_adds_webfont(tmp_path: Path) -> None:
    sys.path.insert(0, str(ROOT / "scripts" / "font-research"))
    import merge  # noqa: E402
    (tmp_path / "366.css").write_text("@font-face { font-family: 'GMarketSans'; }\n", encoding="utf-8")
    rows = [{"name": "G마켓 산스", "noonnu": "https://noonnu.cc/font_page/366"}, {"name": "없음", "noonnu": ""}]
    assert merge.add_webfonts(rows, tmp_path) == 1
    assert rows[0]["webfont"].startswith("@font-face") and "webfont" not in rows[1]
