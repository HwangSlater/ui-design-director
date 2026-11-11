"""facts.py 시험 — 페이지 사실의 값이 시안에 있는지(네일 43차 「하루 7명」, 「4만5천원」·「여섯 마리」·「09:00」 꼴)."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "skills" / "ui-design-director" / "scripts"))
import facts  # noqa: E402


def project(tmp: Path, brief: str, page: str) -> Path:
    (tmp / "mockups").mkdir(parents=True)
    (tmp / "concept-brief.md").write_text(brief, encoding="utf-8")
    (tmp / "mockups" / "index.html").write_text(page, encoding="utf-8")
    return tmp


BRIEF = "사이트 꼴: 여러 쪽\n\n페이지 사실:\n- 이름: 「정자 손끝」\n- 원컬러 젤 4만5천원, 케어 2만원\n- 오전 11시~오후 9시, 하루 7명까지\n- 주소: 견본\n"


def test_all_facts_present(tmp_path: Path) -> None:
    page = "<h1>정자 손끝</h1><p>원컬러 젤 45,000원 · 케어 20,000원</p><p>11:00–21:00 · 하루 일곱 명까지 받아요</p>"
    assert facts.check_project(project(tmp_path, BRIEF, page)) == []


def test_dropped_fact_flagged(tmp_path: Path) -> None:
    page = "<h1>정자 손끝</h1><p>원컬러 젤 45,000원 · 케어 20,000원</p><p>11:00–21:00 예약제</p>"
    out = facts.check_project(project(tmp_path, BRIEF, page))
    assert len(out) == 1 and "7명" in out[0]


def test_no_facts_block_no_check(tmp_path: Path) -> None:
    assert facts.check_project(project(tmp_path, "사이트 꼴: 여러 쪽", "<p>x</p>")) == []
