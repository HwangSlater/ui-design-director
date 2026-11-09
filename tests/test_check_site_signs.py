"""check_site.py 생성 티 검사 — 넓은 자간·이모지 아이콘·빛나는 그림자·마우스 올리면 커짐(unslop signs.md 참고)."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

CHECK = Path(__file__).resolve().parent.parent / "skills" / "ui-design-director" / "scripts" / "check_site.py"
PAGE = """<!doctype html><html lang="ko"><head><meta name="viewport" content="width=device-width">
<title>솔숲오토캠핑장</title><style>{css}</style></head><body><h1>솔숲</h1><img src="a.jpg" alt="숲">{body}</body></html>"""


def rules(tmp_path: Path, css: str, body: str = "") -> str:
    (tmp_path / "index.html").write_text(PAGE.format(css=css, body=body), encoding="utf-8")
    return subprocess.run([sys.executable, "-X", "utf8", str(CHECK), str(tmp_path)], capture_output=True, text=True, encoding="utf-8").stdout


def test_generated_signs_flagged(tmp_path: Path) -> None:
    out = rules(tmp_path, ".k{letter-spacing:.2em}.c{box-shadow:0 0 24px rgba(0,0,0,.4)}.c:hover{transform:scale(1.04)}",
                "<p>☎ 전화</p>")
    for rule in ("wide-tracking", "glow", "hover-scale", "emoji-icon"):
        assert rule in out, rule


def test_plain_page_not_flagged(tmp_path: Path) -> None:
    out = rules(tmp_path, ".k{letter-spacing:.02em}.c{box-shadow:0 1px 2px rgba(0,0,0,.1)}.c:hover{color:var(--c-a)}", "<p>전화 033-000-0000</p>")
    for rule in ("wide-tracking", "glow", "hover-scale", "emoji-icon"):
        assert rule not in out, rule
