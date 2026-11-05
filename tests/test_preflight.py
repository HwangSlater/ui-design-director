"""preflight.py 시험 — 실제 프로젝트에서 잘못 걸리거나 놓친 경우를 그대로 옮겼다.

실행: python -m unittest discover tests
"""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "skills" / "ui-design-director" / "scripts"
sys.path.insert(0, str(SCRIPTS))

import preflight  # noqa: E402


def project(files: dict[str, str]) -> Path:
    root = Path(tempfile.mkdtemp(prefix="preflight-"))
    for name, text in files.items():
        p = root / name
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding="utf-8")
    return root


def found(root: Path, word: str) -> bool:
    return any(word in line for line in preflight.check(root))


class Structure(unittest.TestCase):
    def test_unknown_layout_is_reported_not_passed(self):
        self.assertTrue(found(project({"notes.md": "x"}), "폴더 구조 다름"))


class Channels(unittest.TestCase):
    def test_negated_channel_is_not_a_channel(self):
        # 분식집: 「인스타 없음」을 인스타를 쓴다로 셌다
        root = project({"concept-brief.md": "네이버 지도 있음, 인스타 없음.", "formats/jobs.json": '[{"url": "https://m.place.naver.com/x"}]', "formats/a.jpg": ""})
        self.assertFalse(found(root, "「인스타」"))
        self.assertFalse(found(root, "「네이버」"))

    def test_named_channel_missing_from_references(self):
        root = project({"concept-brief.md": "카카오톡 채널로 주문 받아요", "formats/jobs.json": "[]", "formats/a.jpg": ""})
        self.assertTrue(found(root, "참고 빠짐: 의뢰인이 「카카오」"))

    def test_daangn_link_in_mockup_folder_is_found(self):
        # 깡통구제: 시안에 daangn.com 링크가 있는데 「당근 연결 없음」 — 점 없는 낱말이 걸러졌고, mockup/ 폴더는 아예 안 읽었다
        brief = "인스타, 당근 씀."
        page = '<a href="https://www.instagram.com/x">인스타</a>'
        with_link = project({"concept-brief.md": brief, "mockup/home.html": page, "mockup/data.js": 'daangn: "https://www.daangn.com/kr/x"'})
        self.assertFalse(found(with_link, "「당근」"))
        without = project({"concept-brief.md": brief, "mockup/home.html": page})
        self.assertTrue(found(without, "연결 빠짐: 의뢰인이 「당근」"))


class OwnerScreens(unittest.TestCase):
    def test_not_asked_before_site_plan(self):
        root = project({"concept-brief.md": "사장님 화면에서 오늘 쉬는 날을 바꿔요"})
        self.assertFalse(found(root, "사장님 화면 빠짐"))

    def test_sign_in_and_lost_phone_required_in_plan(self):
        root = project({"concept-brief.md": "사장님 화면", "SITE-PLAN.md": "사장님 화면: 오늘 쉬기"})
        self.assertTrue(found(root, "들어가는 방법"))
        self.assertTrue(found(root, "잃어버렸을 때"))


class Parts(unittest.TestCase):
    def test_button_pair_on_customer_page_only(self):
        pair = '<div><a class="btn main" href="#">전화</a><a class="btn" href="#">카톡</a></div>'
        root = project({"layouts/home-1.html": pair, "layouts/owner.html": pair, "DESIGN.md": "부품 출처"})
        lines = preflight.check(root)
        self.assertTrue(any("home-1.html" in l for l in lines))
        self.assertFalse(any("owner.html" in l for l in lines))

    def test_parts_source_required_once_layouts_exist(self):
        root = project({"layouts/home-1.html": "<p>x</p>", "DESIGN.md": "색 A"})
        self.assertTrue(found(root, "부품 출처 빠짐"))


if __name__ == "__main__":
    unittest.main()
