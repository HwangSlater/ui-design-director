#!/usr/bin/env python3
"""Claude Code 플러그인 훅 — 디자이너가 스킬 순서와 공용 틀을 건너뛰지 못하게 파일 쓰기를 막는다.

PreToolUse(Write·Edit·MultiEdit) 입력을 표준 입력으로 받아, ui-design-director 프로젝트 안의 파일일 때만 본다.
  - formats/ 의 보기 화면 HTML: 공용 틀 표시(board-data)가 없으면 막는다 — make_live_board.py 로만 만든다
  - palette/ 의 HTML: palette-switcher.js 틀이 아니면 막는다
  - 바탕-구성.md·바탕-움직임.md, palette/, DESIGN.md, layouts/·mockups/: 앞 단계가 확정되지 않았으면 막는다
막을 때는 종료 코드 2와 이유(표준 오류)를 돌려준다. Claude Code 는 그 이유를 디자이너에게 보여 준다.
SKILL.md 의 frontmatter 에 hooks 를 넣지 않은 까닭: claude.ai·API 에 올릴 때 모르는 항목이면 업로드가 실패한다.
Bash 로 쓰는 파일(스크립트 출력)은 보지 않는다 — 스크립트는 공용 틀로만 쓴다.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "skills" / "ui-design-director" / "scripts"))
import stage  # noqa: E402  (단계 판단은 stage.py 하나로)

PROJECT_MARKS = ("concept-brief.md", "decisions.json", "formats/board-spec.json")
MATERIAL = {"바탕-구성.md", "바탕-움직임.md"}


def project_root(path: Path) -> Path | None:
    """파일 위쪽 폴더 가운데 스킬 프로젝트(맥락 정리·확정 기록·후보 spec 이 있는 곳)를 찾는다."""
    for folder in path.parents:
        if any((folder / m).is_file() for m in PROJECT_MARKS):
            return folder
    return None


def text_after(tool: str, inp: dict, path: Path) -> str | None:
    """쓰기가 끝난 뒤 파일 내용. 알 수 없으면 None."""
    if tool == "Write":
        return inp.get("content", "")
    edits = inp.get("edits") if tool == "MultiEdit" else [inp]
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None
    for e in edits or []:
        old, new = e.get("old_string", ""), e.get("new_string", "")
        text = text.replace(old, new) if e.get("replace_all") else text.replace(old, new, 1)
    return text


def check(tool: str, inp: dict) -> str | None:
    """막을 이유. 괜찮으면 None."""
    raw = inp.get("file_path")
    if not raw:
        return None
    path = Path(raw).resolve()
    root = project_root(path)
    if root is None:
        return None
    rel = path.relative_to(root).parts
    top = rel[0] if rel else ""
    need = None
    if top == "formats" and len(rel) == 2:
        if path.suffix == ".html":
            body = text_after(tool, inp, path)
            if body is not None and stage.SHARED_VIEWER not in body:
                return ("보기 화면을 직접 만들 수 없습니다. 후보 spec 을 쓰고 "
                        f"python {stage.S}/make_live_board.py formats/board-spec.json formats/보기.html 로 만드세요.")
        if path.name in MATERIAL:
            need = "material"
    elif top == "palette":
        need = "palette"
        if path.suffix == ".html":
            body = text_after(tool, inp, path)
            if body is not None and stage.PALETTE_VIEWER not in body:
                return "팔레트 화면은 palette-switcher.js 틀로만 만듭니다(comparison-board.md § Palettes)."
    elif rel == ("DESIGN.md",):
        need = "design"
    elif top in ("layouts", "mockups"):
        need = "main"
    if need is None:
        return None
    done, _ = stage.status(root)
    missing = [s for s in stage.STAGES[:stage.STAGES.index(need)] if not done[s]]
    if missing:
        return (f"아직 {stage.LABEL[need]} 단계를 만들 수 없습니다 — 먼저: {', '.join(stage.LABEL[s] for s in missing)}. "
                f"python {stage.S}/stage.py {root.as_posix()} 로 다음 명령을 보세요.")
    return None


def main() -> int:
    for s in (sys.stdout, sys.stderr):
        s.reconfigure(encoding="utf-8", errors="replace")
    try:
        data = json.loads(sys.stdin.buffer.read().decode("utf-8", errors="replace") or "{}")
    except json.JSONDecodeError:
        return 0  # 입력을 못 읽으면 막지 않는다(훅이 고장 나도 작업은 이어진다)
    reason = check(data.get("tool_name", ""), data.get("tool_input") or {})
    if reason:
        print(reason, file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
