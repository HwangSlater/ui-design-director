"""점검 도구들이 함께 쓰는 파일 읽기와 건너뛸 폴더."""
from __future__ import annotations

import sys
from pathlib import Path

# 어느 점검이든 보지 않는 도구·꾸러미 폴더. 도구마다 더 건너뛸 것은 여기에 합쳐 쓴다
TOOL_DIRS = frozenset({"node_modules", ".git", "__pycache__"})


def read(p: Path) -> str:
    """없거나 못 읽는 파일(권한·폴더)은 빈 글로 — 점검 하나 때문에 전체가 멈추지 않게."""
    try:
        return p.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""


def utf8_console() -> None:
    """한글을 찍는 도구는 main 첫 줄에 부른다 — 윈도 콘솔 기본(cp949)으로 찍으면 한글이 깨져 들어갔다."""
    for s in (sys.stdout, sys.stderr):
        try:
            s.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError):  # 시험이 바꿔 끼운 흐름(StringIO 등)은 그대로 둔다
            pass
