#!/usr/bin/env python3
"""견본 사진 받기 — 의뢰인 사진이 없을 때 쓸 수 있는 사진을 찾아 받고 출처를 적는다.

    python sample_photos.py "<주제, 영어가 잘 찾아짐>" --n 8 --out <프로젝트>/mockups/img/sample
                            [--orient landscape|portrait|square] [--no-people] [--place "Seoul Korea 서울 망원동"]

찾는 순서: Wikimedia Commons API → Openverse API. CC0·퍼블릭 도메인·CC BY·CC BY-SA 만 남기고
NonFree·비영리(NC)·변경 금지(ND)·라이선스 모름은 버린다. svg·로고·엠블럼·문장(crest)·워드마크는 사진이 아니라서 뺀다.
결과: <out>/sample-01.jpg …(긴 변 1600 안쪽 JPEG 로 다시 저장), credits.json(파일·제목·작가·라이선스·주소·출처),
contact.jpg(번호 붙은 한 장짜리 모아 보기 — 이것 하나만 열어 고른다). 줄마다 「파일 · 작가 · 라이선스」, 끝에 바닥글 「견본」 줄.
--no-people 은 제목·설명에 portrait·headshot·selfie 같은 말이 있는 것만 뺀다. 사람 이름이나 그림 속 얼굴은 못 알아본다 —
고른 뒤 모아 보기에서 직접 보고, 허락받지 않은 얼굴은 잘라 낸다(build-rules.md § Content and samples).
--place 는 장소 말을 붙여 먼저 찾고(영어 말 전부 → 첫 말 → 한글 말 → 주제만), 제목·설명·주소에 장소 말(한국 장소면
korea·seoul·한국·서울도)이 있는 사진을 앞에 둔다. 줄마다 「장소 맞음(seoul)」·「장소 표시 없음」을 붙인다.
쓸 사진이 하나도 없으면 1 을 돌려준다. 브라우저를 띄우지 않고 공개 API 만 부른다.
"""
from __future__ import annotations

import argparse
import html
import io
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

from common import utf8_console  # 콘솔 한글 깨짐 막기는 common 하나로

# 두 API 주소와 우리를 밝히는 User-Agent(Wikimedia 정책: 도구 이름과 연락처) — 설정 파일에서
_CFG = json.loads((Path(__file__).resolve().parent.parent / "assets" / "sample-photos.json").read_text(encoding="utf-8"))
UA, COMMONS_API, OPENVERSE_API = _CFG["userAgent"], _CFG["commonsApi"], _CFG["openverseApi"]
TIMEOUT_S = 15
PAUSE_S = 0.5            # 요청 사이 쉬는 시간 — 두 API 모두 익명 요청 속도를 제한한다
RETRY_CAP_S = 10         # 429 의 Retry-After 를 이보다 오래 기다리지 않는다
MAX_BYTES = 15_000_000   # 원본이 이보다 크면 받지 않는다(Openverse 는 원본 주소를 준다)
THUMB_W = 1280           # Commons 에 달라고 할 크기
MAX_SIDE = 1600          # 저장할 때 긴 변
MIN_W = 800              # 이보다 작은 사진은 화면에 쓰기 어렵다
OVERFETCH = 4            # 걸러질 것을 생각해 n 의 몇 배를 찾을지
SHEET_CELL = (320, 220)  # 모아 보기 칸 크기
SHEET_COLS = 4
NOT_PHOTO = re.compile(r"\b(logos?|emblems?|crests?|wordmarks?|icons?|badges?|coat of arms|seal)\b", re.I)
PEOPLE = re.compile(r"\b(portraits?|headshots?|selfies?|mugshots?|faces?|close-up of)\b", re.I)
ORIENT_RATIO = 1.15      # 가로/세로 비가 이보다 크면 가로 사진
KOREA_WORDS = ("korea", "korean", "seoul", "한국", "서울", "대한민국")  # --place 가 한국 장소일 때 함께 찾을 말


def licence_name(raw: str) -> str | None:
    """라이선스 표기를 짧은 이름으로 — 못 쓰는 것이면 None.

    Commons 의 LicenseShortName(「CC BY-SA 4.0」「Public domain」)과 Openverse 의 license·버전(「by-sa」「cc0」「pdm」)을 함께 받는다.
    """
    s = re.sub(r"[\s_]+", "-", (raw or "").strip().lower())
    if not s or "nc" in s.split("-") or "nd" in s.split("-") or "nonfree" in s or "fair-use" in s:
        return None
    if s in ("cc0", "cc-zero") or s.startswith("cc0-"):
        return "CC0"
    if s in ("pd", "pdm") or s.startswith("public-domain") or s.startswith("pd-"):
        return "퍼블릭 도메인"
    m = re.fullmatch(r"(?:cc-)?by(-sa)?(?:-(\d(?:\.\d)?))?(?:-[a-z]{2,3})?", s)
    if m:
        return f"CC BY{'-SA' if m.group(1) else ''}" + (f" {m.group(2)}" if m.group(2) else "")
    return None


def plain(text: str) -> str:
    """Commons 의 Artist·설명은 HTML — 태그를 걷고 한 줄로."""
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", text or ""))).strip()


def orient_of(w: int, h: int) -> str:
    if w >= h * ORIENT_RATIO:
        return "landscape"
    if h >= w * ORIENT_RATIO:
        return "portrait"
    return "square"


def usable(c: dict, orient: str | None, no_people: bool) -> bool:
    """사진이고, 쓸 만한 크기이고, 방향·사람 조건에 맞는지."""
    if c["ext"] not in ("jpg", "jpeg", "png", "webp") or c["width"] < MIN_W:
        return False
    words = f"{c['title']} {c.get('description', '')}"
    if NOT_PHOTO.search(words) or (no_people and PEOPLE.search(words)):
        return False
    return orient is None or orient_of(c["width"], c["height"]) == orient


def needs_author(licence: str) -> bool:
    return licence.startswith("CC BY")


def parse_commons(data: dict) -> list[dict]:
    """Commons generator=search 응답 → 후보. 라이선스가 맞지 않거나 작가를 모르는 BY 는 버린다."""
    pages = (data.get("query") or {}).get("pages") or []
    if isinstance(pages, dict):  # formatversion=1 모양
        pages = list(pages.values())
    out = []
    for p in sorted(pages, key=lambda p: p.get("index", 0)):
        info = (p.get("imageinfo") or [{}])[0]
        meta = {k: (v or {}).get("value", "") for k, v in (info.get("extmetadata") or {}).items()}
        if str(meta.get("NonFree", "")).strip().lower() in ("true", "1", "yes"):
            continue
        lic = licence_name(meta.get("LicenseShortName", "")) or licence_name(meta.get("License", ""))
        author = plain(meta.get("Artist", ""))
        url = info.get("thumburl") or info.get("url") or ""
        if not lic or not url or (needs_author(lic) and not author):
            continue
        title = re.sub(r"^File:", "", p.get("title", ""))
        out.append({
            "title": plain(meta.get("ObjectName", "")) or title.rsplit(".", 1)[0],
            "description": plain(meta.get("ImageDescription", ""))[:300],
            "author": author or "작가 표기 없음",
            "licence": lic,
            "licence_url": meta.get("LicenseUrl", ""),
            "source": info.get("descriptionurl", ""),
            "url": url,
            "ext": title.rsplit(".", 1)[-1].lower() if "." in title else "",
            "width": int(info.get("width") or 0),
            "height": int(info.get("height") or 0),
            "site": "Wikimedia Commons",
        })
    return out


def parse_openverse(data: dict) -> list[dict]:
    """Openverse 검색 응답 → 후보."""
    out = []
    for r in data.get("results") or []:
        lic = licence_name(f"{r.get('license', '')}-{r.get('license_version', '')}".strip("-"))
        author = plain(r.get("creator") or "")
        if not lic or not r.get("url") or (needs_author(lic) and not author):
            continue
        ext = (r.get("filetype") or Path(urllib.parse.urlparse(r["url"]).path).suffix.lstrip(".")).lower()
        out.append({
            "title": plain(r.get("title") or "") or "제목 없음",
            "description": " ".join(t.get("name", "") for t in r.get("tags") or [] if isinstance(t, dict))[:300],
            "author": author or "작가 표기 없음",
            "licence": lic,
            "licence_url": r.get("license_url") or "",
            "source": r.get("foreign_landing_url") or "",
            "url": r["url"],
            "ext": ext,
            "width": int(r.get("width") or 0),
            "height": int(r.get("height") or 0),
            "site": f"Openverse({r.get('provider') or r.get('source') or '?'})",
        })
    return out


def fetch(url: str, limit: int = MAX_BYTES) -> bytes:
    """https 만, 짧은 대기, 429 면 한 번 기다렸다 다시."""
    if urllib.parse.urlparse(url).scheme != "https":
        raise ValueError(f"https 가 아닌 주소: {url}")
    for attempt in (0, 1):
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        try:
            with urllib.request.urlopen(req, timeout=TIMEOUT_S) as r:
                body = r.read(limit + 1)
                if len(body) > limit:
                    raise ValueError("파일이 너무 큼")
                return body
        except urllib.error.HTTPError as e:
            if e.code != 429 or attempt:
                raise
            wait = e.headers.get("Retry-After", "")
            time.sleep(min(float(wait) if wait.isdigit() else 2.0, RETRY_CAP_S))
    raise RuntimeError("닿지 않음")


def fetch_json(url: str, params: dict) -> dict:
    return json.loads(fetch(f"{url}?{urllib.parse.urlencode(params)}", limit=5_000_000))


def search_commons(subject: str, want: int) -> list[dict]:
    return parse_commons(fetch_json(COMMONS_API, {
        "action": "query", "format": "json", "formatversion": 2, "generator": "search",
        "gsrsearch": f"{subject} filetype:bitmap", "gsrnamespace": 6, "gsrlimit": min(50, want),
        "prop": "imageinfo", "iiprop": "url|size|mime|extmetadata", "iiurlwidth": THUMB_W,
        "iiextmetadatafilter": "LicenseShortName|License|LicenseUrl|Artist|NonFree|ImageDescription|ObjectName",
    }))


def search_openverse(subject: str, want: int, orient: str | None) -> list[dict]:
    params = {"q": subject, "license": "cc0,pdm,by,by-sa", "category": "photograph", "page_size": min(20, want)}
    if orient:
        params["aspect_ratio"] = {"landscape": "wide", "portrait": "tall", "square": "square"}[orient]
    return parse_openverse(fetch_json(OPENVERSE_API, params))


def to_jpeg(body: bytes) -> bytes:
    """받은 파일을 Pillow 로 열어 다시 저장 — 그림이 아니면 여기서 걸리고, 메타데이터도 걷힌다."""
    from PIL import Image
    with Image.open(io.BytesIO(body)) as im:
        im = im.convert("RGB")
        im.thumbnail((MAX_SIDE, MAX_SIDE))
        buf = io.BytesIO()
        im.save(buf, "JPEG", quality=85, optimize=True)
        return buf.getvalue()


def contact_sheet(files: list[Path], dest: Path) -> None:
    """번호 붙은 모아 보기 한 장."""
    from PIL import Image, ImageDraw
    cw, ch = SHEET_CELL
    rows = (len(files) + SHEET_COLS - 1) // SHEET_COLS
    sheet = Image.new("RGB", (cw * min(SHEET_COLS, len(files)), ch * rows), "white")
    draw = ImageDraw.Draw(sheet)
    for i, f in enumerate(files):
        with Image.open(f) as im:
            im = im.convert("RGB")
            im.thumbnail((cw - 8, ch - 8))
            x, y = (i % SHEET_COLS) * cw, (i // SHEET_COLS) * ch
            sheet.paste(im, (x + (cw - im.width) // 2, y + (ch - im.height) // 2))
        draw.rectangle((x + 4, y + 4, x + 34, y + 24), fill="black")
        draw.text((x + 10, y + 8), f"{i + 1:02d}", fill="white")
    sheet.save(dest, "JPEG", quality=82)


def spread(cands: list[dict]) -> list[dict]:
    """같은 제목 묶음(한 경기·한 행사 연작)이 앞을 다 차지하지 않게 — 제목마다 한 장씩 먼저, 나머지는 뒤로."""
    firsts, rest, seen = [], [], set()
    for c in cands:
        key = re.sub(r"[\W\d_]+", " ", c["title"].lower()).strip()
        (rest if key in seen else firsts).append(c)
        seen.add(key)
    return firsts + rest


def credit_line(credits: list[dict]) -> str:
    who = ", ".join(dict.fromkeys(f"{c['author']}({c['licence']})" for c in credits))
    sites = " · ".join(dict.fromkeys(c["site"].split("(")[0] for c in credits))
    return f"사진은 견본이에요 — 사진: {who}, {sites}"


def place_words(place: str) -> list[str]:
    """--place 의 말과, 한국 장소면 한국·서울 같은 말을 함께 — 제목·설명에서 찾을 말(소문자)."""
    words = [w.lower() for w in re.split(r"[\s,·]+", place or "") if len(w) > 1]
    if any(w in KOREA_WORDS for w in words):
        words += [w for w in KOREA_WORDS if w not in words]
    return words


def place_match(c: dict, words: list[str]) -> str:
    """후보의 제목·설명·주소에 나온 장소 말(처음 하나). 없으면 빈 글."""
    text = f"{c['title']} {c.get('description', '')} {urllib.parse.unquote(c.get('source', ''))}".lower()
    return next((w for w in words if re.search(rf"(?<![a-z]){re.escape(w)}(?![a-z])", text)), "")


def place_queries(subject: str, place: str) -> list[str]:
    """장소를 붙인 검색어 먼저(영어 장소 말 전부 → 첫 말 → 한글 장소 말), 마지막에 주제만."""
    if not place:
        return [subject]
    en = [w for w in place.split() if w.isascii()]
    ko = [w for w in place.split() if not w.isascii()]
    qs = [f"{subject} {' '.join(en)}" if en else "", f"{subject} {en[0]}" if len(en) > 1 else "",
          f"{subject} {' '.join(ko)}" if ko else "", subject]
    return list(dict.fromkeys(q for q in qs if q))


def collect(subject: str, n: int, orient: str | None, no_people: bool, place: str = "") -> list[dict]:
    """두 곳을 차례로 찾아 조건에 맞는 후보를 모은다. 한 곳이 실패해도 다른 곳은 본다.
    Commons 가 충분해도 Openverse 를 본다 — 「basketball game」 상위가 한 경기 연작뿐이라 세 장이 같은 장면이었다.
    --place 가 있으면 장소를 붙여 먼저 찾고, 제목·설명에 장소 말이 있는 후보를 앞에 둔다 — 「망원동 골목」 장터에
    독일 간판(KÜCHE)이 보이는 베를린 장터 사진이 첫 화면에 들어갔다(플리마켓 14차)."""
    found, seen = [], set()
    for q in place_queries(subject, place):
        for name, search in (("Wikimedia Commons", lambda: search_commons(q, n * OVERFETCH)),
                             ("Openverse", lambda: search_openverse(q, n * OVERFETCH, orient))):
            try:
                cands = search()
            except (urllib.error.URLError, OSError, ValueError, RuntimeError) as e:
                print(f"{name} 검색 실패({q}): {e}", file=sys.stderr)
                continue
            for c in cands:
                if c["source"] not in seen and usable(c, orient, no_people):
                    seen.add(c["source"])
                    found.append(c)
            time.sleep(PAUSE_S)
    words = place_words(place)
    for c in found:
        c["place"] = place_match(c, words) if words else ""
    return spread([c for c in found if c["place"]]) + spread([c for c in found if not c["place"]])


def main(argv: list[str] | None = None) -> int:
    utf8_console()
    ap = argparse.ArgumentParser(description="견본 사진 받기")
    ap.add_argument("subject")
    ap.add_argument("--n", type=int, default=8)
    ap.add_argument("--out", required=True)
    ap.add_argument("--orient", choices=("landscape", "portrait", "square"))
    ap.add_argument("--no-people", action="store_true")
    ap.add_argument("--place", default="", help="장소 말(예: \"Seoul Korea 서울 망원동\") — 이 장소 사진을 앞에")
    a = ap.parse_args(argv)
    n = max(1, min(a.n, 24))
    cands = collect(a.subject, n, a.orient, a.no_people, a.place)
    out = Path(a.out)
    credits: list[dict] = []
    for c in cands:
        if len(credits) >= n:
            break
        try:
            body = to_jpeg(fetch(c["url"]))
        except Exception as e:  # noqa: BLE001 — 한 장이 깨져도 다음 후보로(망·크기·그림 아님)
            print(f"건너뜀: {c['title'][:60]} — {e}", file=sys.stderr)
            continue
        out.mkdir(parents=True, exist_ok=True)
        name = f"sample-{len(credits) + 1:02d}.jpg"
        (out / name).write_bytes(body)
        credits.append({"file": name, **{k: c[k] for k in ("title", "author", "licence", "licence_url", "source", "site", "place")}})
        time.sleep(PAUSE_S)
    if not credits:
        print(f"「{a.subject}」로 쓸 수 있는 견본 사진을 찾지 못했어요. 더 넓은 영어 주제로 다시 찾아 보세요"
              f"(예: 「basketball」, 「bakery interior」). 그래도 없으면 그 칸을 빼고 의뢰인에게 사진을 부탁해요.")
        return 1
    keep = {c["file"] for c in credits}
    for old in out.glob("sample-[0-9][0-9].jpg"):  # 지난번에 더 많이 받았던 같은 이름 파일
        if old.name not in keep:
            old.unlink()
    (out / "credits.json").write_text(json.dumps(credits, ensure_ascii=False, indent=2), encoding="utf-8")
    contact_sheet([out / c["file"] for c in credits], out / "contact.jpg")
    for c in credits:
        where = (f" · 장소 맞음({c['place']})" if c["place"] else " · 장소 표시 없음") if a.place else ""
        print(f"{c['file']} · {c['author'][:60]} · {c['licence']}{where}")
    if a.place and not any(c["place"] for c in credits):
        print(f"「{a.place}」 사진을 찾지 못했어요 — 모아 보기에서 다른 나라 간판·건물이 보이는 사진은 빼고, "
              "「견본」 줄에 「동네 사진은 못 찾아 다른 곳 사진」이라고 밝혀요(sample-photos.md)")
    print(f"모아 보기: {out / 'contact.jpg'}")
    print(f"견본 줄: {credit_line(credits)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
