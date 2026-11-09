"""점검 도구들이 함께 쓰는 파일 읽기와 건너뛸 폴더."""
from __future__ import annotations

from pathlib import Path

# 어느 점검이든 보지 않는 도구·꾸러미 폴더. 도구마다 더 건너뛸 것은 여기에 합쳐 쓴다
TOOL_DIRS = frozenset({"node_modules", ".git", "__pycache__"})


def read(p: Path) -> str:
    """없거나 못 읽는 파일(권한·폴더)은 빈 글로 — 점검 하나 때문에 전체가 멈추지 않게."""
    try:
        return p.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""
