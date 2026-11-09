#!/usr/bin/env python3
"""글꼴 조사 두 갈래를 스킬이 읽는 fonts.json 하나로 합친다.

    python -X utf8 scripts/font-research/merge.py <조사 폴더> skills/ui-design-director/assets/fonts/fonts.json [--webfont <웹폰트 폴더>]
    python -X utf8 scripts/font-research/merge.py --webfont <웹폰트 폴더> skills/ui-design-director/assets/fonts/fonts.json
        (조사를 다시 하지 않고 지금 fonts.json 에 웹폰트 글만 붙인다)

<조사 폴더> 에는 how-to-rerun.md 대로 만든 결과가 있어야 한다:
  licenses.json, fonts.json            방문 상위 사이트에서 잰 글꼴과 라이선스(measure.mjs·analyze.mjs)
  company/company-fonts.json           눈누 전체에서 회사·기관·단체가 낸 웹 임베딩 가능 글꼴(company/build.py)
<웹폰트 폴더> 는 company/webfont.py 가 눈누 상세 페이지에서 받은 「웹폰트로 사용」 글(<눈누 id>.css)이다 → 각 글꼴의 webfont.
AI 글꼴(assets/fonts/ai-fonts.json)은 여기서 빼지 않는다 — 고르는 도구(fonts.py)가 뺀다. 목록이 바뀌어도 다시 합칠 필요가 없게.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

# 상위 사이트에서 잰 CSS 이름 → 눈누 이름(같은 글꼴을 한 줄로)
SITE_TO_NOONNU = {
    "Gmarket Sans": "G마켓 산스", "S-Core Dream": "에스코어드림", "Esamanru": "이사만루", "11StreetGothic": "11번가 고딕",
    "KakaoBig": "카카오 큰글씨", "KakaoSmall": "카카오 작은글씨", "Arita": "아리따돋움", "NanumBarunGothic": "나눔바른고딕",
    "NanumSquare": "나눔스퀘어", "NanumSquare Neo": "나눔스퀘어 네오", "Flight Sans": "플라이트 산스", "Nanum Gothic": "나눔고딕",
    "Spoqa Han Sans Neo": "스포카 한 산스 네오", "Noto Sans KR": "본고딕 (Noto Sans)",
}


def load(p: Path):
    return json.loads(p.read_text(encoding="utf-8"))


def save(data: dict, out: Path) -> None:
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(data, ensure_ascii=False, indent=0), encoding="utf-8")


def add_webfonts(rows, folder: Path) -> int:
    """눈누 id 로 웹폰트 글을 붙인다. 붙인 글꼴 수."""
    n = 0
    for row in rows:
        m = re.search(r"/font_page/(\d+)", row.get("noonnu") or "")
        f = folder / f"{m.group(1)}.css" if m else None
        if f and f.is_file() and f.read_text(encoding="utf-8").strip():
            row["webfont"] = f.read_text(encoding="utf-8").strip()
            n += 1
    return n


def main(argv: list[str]) -> int:
    webfont = None
    if "--webfont" in argv:
        i = argv.index("--webfont")
        webfont = Path(argv[i + 1]) if i + 1 < len(argv) else None
        argv = argv[:i] + argv[i + 2:]
        if webfont is None or not webfont.is_dir():
            print("--webfont 뒤에 company/webfont.py 가 만든 폴더를 주세요", file=sys.stderr)
            return 2
    if webfont and len(argv) == 1:  # 지금 표에 웹폰트만
        out = Path(argv[0])
        data = load(out)
        n = add_webfonts(data["fonts"], webfont)
        save(data, out)
        print(f"웹폰트 글 {n}개 / 글꼴 {len(data['fonts'])}개 → {out}")
        return 0
    if len(argv) != 2:
        print(__doc__.strip(), file=sys.stderr)
        return 2
    src, out = Path(argv[0]), Path(argv[1])
    lic = load(src / "licenses.json")
    sites = {f["font"]: f for f in load(src / "fonts.json")}
    company = load(src / "company" / "company-fonts.json")
    rows: dict[str, dict] = {}
    for c in company["fonts"]:
        rows[c["글꼴"]] = {
            "name": c["글꼴"], "aliases": [], "maker": c["만든 곳"], "kind": c["갈래"],
            "style": c.get("형태 태그") or [s.strip() for s in c.get("성격", "").split(",") if s.strip()],
            "weights": c.get("굵기", ""), "conditions": c.get("조건") or [],
            "license": c.get("라이선스 출처", ""), "download": c.get("받는 곳", ""),
            "noonnu": c.get("눈누", ""), "views": c.get("조회수(수)") or 0, "top_sites": 0, "sites": [],
            "read": c.get("읽은 날", ""),
        }
    for en, v in lic.items():
        if v.get("free") != "무료" or v.get("korean") != "있음":
            continue
        ko = SITE_TO_NOONNU.get(en)
        row = rows.get(ko) if ko else None
        if row is None:  # 눈누에 없는 오픈 라이선스 글꼴(Pretendard, SUITE 등)
            row = rows.setdefault(en, {
                "name": en, "aliases": [], "maker": v.get("maker", ""), "kind": v.get("sourceType", "오픈 라이선스"),
                "style": [s.strip() for s in v.get("character", "").split(",")[:1]], "weights": v.get("character", ""),
                "conditions": [v.get("conditions", "")] if v.get("conditions") else [], "license": v.get("source", "").split(" ; ")[0],
                "download": v.get("download", ""), "noonnu": "", "views": 0, "top_sites": 0, "sites": [], "read": v.get("readDate", ""),
            })
        if en != row["name"]:
            row["aliases"].append(en)
        s = sites.get(en, {})
        row["top_sites"] = s.get("count", 0)
        row["sites"] = s.get("sites", [])[:5]
    data = {
        "made": company["summary"].get("작성일", ""),
        "source": "방문 상위 사이트 186곳 실측 + 눈누 전체 중 회사·기관·단체 공개 글꼴(웹 임베딩 가능)",
        "fonts": sorted(rows.values(), key=lambda r: (-r["top_sites"], -r["views"], r["name"])),
    }
    n = add_webfonts(data["fonts"], webfont) if webfont else 0
    save(data, out)
    print(f"글꼴 {len(data['fonts'])}개(웹폰트 글 {n}개) → {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
