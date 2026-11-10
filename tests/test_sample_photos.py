"""sample_photos.py 시험 — 망에 나가지 않고 받은 응답 모양(고정 JSON)으로 라이선스 거르기·해석·빈 결과를 본다."""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "skills" / "ui-design-director" / "scripts"))
import sample_photos as sp  # noqa: E402


def commons_page(title: str, short: str, artist: str = "<a href='x'>Kim &amp; Lee</a>", nonfree: str = "false",
                 width: int = 1280, desc: str = "") -> dict:
    return {"title": f"File:{title}", "index": 1, "imageinfo": [{
        "thumburl": f"https://upload.wikimedia.org/thumb/{title}", "url": f"https://upload.wikimedia.org/{title}",
        "descriptionurl": f"https://commons.wikimedia.org/wiki/File:{title}", "width": width, "height": 853,
        "extmetadata": {"LicenseShortName": {"value": short}, "Artist": {"value": artist},
                        "NonFree": {"value": nonfree}, "LicenseUrl": {"value": "https://creativecommons.org/licenses/by/4.0"},
                        "ImageDescription": {"value": desc}},
    }]}


@pytest.mark.parametrize("raw, want", [
    ("CC BY-SA 4.0", "CC BY-SA 4.0"), ("CC BY 2.0", "CC BY 2.0"), ("by-sa-2.0", "CC BY-SA 2.0"),
    ("by", "CC BY"), ("CC0", "CC0"), ("cc0-1.0", "CC0"), ("Public domain", "퍼블릭 도메인"), ("pdm", "퍼블릭 도메인"),
    ("CC BY-NC 2.0", None), ("by-nc-sa", None), ("CC BY-ND 4.0", None), ("Fair use", None), ("GFDL", None),
    ("", None), ("All rights reserved", None),
])
def test_licence_name(raw: str, want: str | None) -> None:
    assert sp.licence_name(raw) == want


def test_parse_commons_keeps_free_and_drops_the_rest() -> None:
    data = {"query": {"pages": [
        commons_page("Court.jpg", "CC BY-SA 4.0"),
        commons_page("Shot.jpg", "CC BY-NC 2.0"),                 # 비영리 — 버림
        commons_page("Arena.jpg", "CC BY 4.0", nonfree="true"),   # NonFree — 버림
        commons_page("Nobody.jpg", "CC BY 4.0", artist=""),       # BY 인데 작가 없음 — 버림
        commons_page("Old.jpg", "Public domain", artist=""),      # 퍼블릭 도메인은 작가 없어도 됨
        commons_page("Mystery.jpg", ""),                          # 라이선스 모름 — 버림
    ]}}
    got = sp.parse_commons(data)
    assert [c["title"] for c in got] == ["Court", "Old"]
    assert got[0]["author"] == "Kim & Lee" and got[0]["licence"] == "CC BY-SA 4.0" and got[0]["ext"] == "jpg"
    assert sp.parse_commons({}) == [] and sp.parse_commons({"query": {"pages": {"1": commons_page("A.jpg", "CC0")}}})


def test_parse_openverse() -> None:
    data = {"results": [
        {"title": "Game night", "creator": "Park", "license": "by", "license_version": "2.0", "url": "https://x/1.jpg",
         "foreign_landing_url": "https://flickr/1", "filetype": "jpg", "width": 1024, "height": 683, "provider": "flickr"},
        {"title": "Nc", "creator": "Choi", "license": "by-nc", "license_version": "2.0", "url": "https://x/2.jpg"},
        {"title": "Zero", "creator": "", "license": "cc0", "license_version": "1.0", "url": "https://x/3.png",
         "width": 900, "height": 900},
    ]}
    got = sp.parse_openverse(data)
    assert [(c["title"], c["licence"], c["ext"]) for c in got] == [("Game night", "CC BY 2.0", "jpg"), ("Zero", "CC0", "png")]
    assert got[0]["site"] == "Openverse(flickr)"


def cand(title: str, ext: str = "jpg", w: int = 1280, h: int = 853, desc: str = "") -> dict:
    return {"title": title, "description": desc, "ext": ext, "width": w, "height": h}


def test_usable_skips_marks_svg_small_and_people() -> None:
    assert sp.usable(cand("Basketball court at night"), None, False)
    for bad in (cand("Team logo 2020"), cand("Club crest"), cand("Old wordmark"), cand("Emblem of the league")):
        assert not sp.usable(bad, None, False)
    assert not sp.usable(cand("Court", ext="svg"), None, False)
    assert not sp.usable(cand("Court", w=400, h=300), None, False)
    assert not sp.usable(cand("Player", desc="Portrait of the captain"), None, True)
    assert sp.usable(cand("Player", desc="Portrait of the captain"), None, False)
    assert not sp.usable(cand("Court"), "portrait", False) and sp.usable(cand("Court", w=900, h=1300), "portrait", False)


def test_spread_puts_one_per_series_first() -> None:
    got = sp.spread([cand("Game (FL1)"), cand("Game (FL2)"), cand("Arena")])
    assert [c["title"] for c in got] == ["Game (FL1)", "Arena", "Game (FL2)"]


def test_credit_line_groups_authors() -> None:
    line = sp.credit_line([{"author": "A", "licence": "CC0", "site": "Wikimedia Commons"},
                           {"author": "A", "licence": "CC0", "site": "Openverse(flickr)"}])
    assert line == "사진은 견본이에요 — 사진: A(CC0), Wikimedia Commons · Openverse"


def test_cli_no_results(monkeypatch: pytest.MonkeyPatch, tmp_path: Path, capsys: pytest.CaptureFixture) -> None:
    monkeypatch.setattr(sp, "fetch_json", lambda url, params: {"query": {"pages": []}, "results": []})
    monkeypatch.setattr(sp, "PAUSE_S", 0)
    assert sp.main(["없는 주제", "--n", "3", "--out", str(tmp_path / "img")]) == 1
    assert "더 넓은 영어 주제" in capsys.readouterr().out
    assert not (tmp_path / "img").exists()  # 아무것도 만들지 않는다



def test_place_queries_and_words() -> None:
    assert sp.place_queries("flea market", "") == ["flea market"]
    assert sp.place_queries("flea market", "Seoul Korea 서울 망원동") == [
        "flea market Seoul Korea", "flea market Seoul", "flea market 서울 망원동", "flea market"]
    words = sp.place_words("Seoul Korea 서울 망원동")
    assert "망원동" in words and "한국" in words and "korean" in words


def test_place_match_ranks_local_first(monkeypatch: pytest.MonkeyPatch) -> None:
    """장소 말이 있는 사진을 앞에 — 베를린 장터 사진이 망원동 장터 첫 화면에 들어갔다(플리마켓 14차)."""
    berlin = {"title": "Flohmarkt Berlin Mauerpark", "description": "street market", "source": "berlin-page",
              "ext": "jpg", "width": 1280, "height": 800}
    seoul = {"title": "Dongmyo flea market", "description": "Seoul, South Korea", "source": "seoul-page",
             "ext": "jpg", "width": 1280, "height": 800}
    asked: list[str] = []
    monkeypatch.setattr(sp, "search_commons", lambda q, want: asked.append(q) or [dict(berlin), dict(seoul)])
    monkeypatch.setattr(sp, "search_openverse", lambda q, want, orient: [])
    monkeypatch.setattr(sp, "PAUSE_S", 0)
    got = sp.collect("flea market", 4, None, False, "Seoul Korea 서울 망원동")
    assert [c["source"] for c in got] == ["seoul-page", "berlin-page"]
    assert got[0]["place"] == "seoul" and got[1]["place"] == ""
    assert asked[0] == "flea market Seoul Korea" and asked[-1] == "flea market"
    assert sp.place_match({"title": "Seoulful", "description": ""}, ["seoul"]) == ""  # 낱말 속 글자는 맞음 아님
