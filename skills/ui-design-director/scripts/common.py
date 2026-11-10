"""점검 도구들이 함께 쓰는 파일 읽기와 건너뛸 폴더."""
from __future__ import annotations

import re
import sys
from pathlib import Path

# 어느 점검이든 보지 않는 도구·꾸러미 폴더. 도구마다 더 건너뛸 것은 여기에 합쳐 쓴다
TOOL_DIRS = frozenset({"node_modules", ".git", "__pycache__"})


# concept-brief.md 의 사이트 꼴 줄 — 「여러 쪽」(가게·서비스·회사·기록) 또는 「한 쪽 홍보·모집」(행사·모집·캠페인 하나)
SITE_KIND = re.compile(r"사이트 꼴\s*[:：]\s*(여러 쪽|한 쪽)")
ONE_PAGE = "한 쪽"


def site_kind(brief: str) -> str | None:
    """맥락 정리에 적힌 사이트 꼴(「여러 쪽」·「한 쪽」). 줄이 없으면 None — 점검은 여러 쪽으로 본다."""
    m = SITE_KIND.search(brief)
    return m.group(1) if m else None


def mock_dir(root: Path) -> Path:
    """시안 폴더 — mockups/ 가 기본, 없으면 mockup/(깡통구제 시안이 이 이름이라 채널·사장님 화면 검사를 통째로 건너뜀)."""
    return root / "mockups" if (root / "mockups").is_dir() else root / "mockup"


# 바탕 사본(남의 사이트 저장본·캡처)을 지운 뒤에도 남기는 사실 — 「바탕에도 1·2·3 이 있었다」 같은 예외와 「바탕 자료를 모았다」.
# 승인 뒤 사본을 지우자 예외 근거가 사라져 바탕에 있던 01–04 가 다시 걸렸고 단계 표가 「순서 어김」으로 돌아갔다(치과 17차)
BASE_MARKS = Path("formats") / "바탕-표지.json"


def base_marks(root: Path) -> dict:
    """저장해 둔 바탕 표지. 없거나 깨졌으면 빈 dict."""
    import json
    try:
        d = json.loads(read(root / BASE_MARKS) or "{}")
    except ValueError:
        return {}
    return d if isinstance(d, dict) else {}


def save_base_marks(root: Path, marks: dict) -> None:
    import json
    p = root / BASE_MARKS
    if p.parent.is_dir() and base_marks(root) != marks:
        p.write_text(json.dumps(marks, ensure_ascii=False, indent=1), encoding="utf-8")


def base_snapshots(root: Path) -> list[Path]:
    """바탕 사이트를 통째로 저장한 페이지(formats/snapshot/**/index.html) — 「바탕에도 있나」를 HTML 로 볼 때."""
    snap = root / "formats" / "snapshot"
    return sorted(snap.glob("**/index.html")) if snap.is_dir() else []


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
