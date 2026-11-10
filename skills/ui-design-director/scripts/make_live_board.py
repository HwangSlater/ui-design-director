#!/usr/bin/env python3
"""참고 사이트를 실제로 띄워 넘겨 보는 화면 — 공용 보기 화면(make_board.py)의 실제 사이트 모드로 만든다.

    python make_live_board.py <spec.json> <out.html>

보기 화면은 늘 하나다: 아래 막대·썸네일·확정 단추·단축키가 같은 make_board.py 의 틀. 따로 화면을 짜지 않는다
(따로 만든 화면은 썸네일·확정이 빠져 사용자가 「우리 템플릿을 안 따랐다」고 짚었다).
spec: make_board.py 의 spec(id·title·urls·pages)을 그대로 쓰거나, 예전 꼴
      {"title": "…", "candidates": [{"n": "1", "name": "…", "meta": "…", "pages": {"홈": "<주소>"}}]} 도 받는다.
가운데에는 실제 페이지가 뜨고, 틀 안 띄우기를 막는 사이트는 live_proxy.mjs 로(OPEN 주소의 ?proxy=) 띄운다.
<captures> 폴더에 capture.mjs 그림이 있으면 썸네일과 「우회가 꺼졌을 때 대신 보기」로 쓴다.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import utf8_console  # noqa: E402  콘솔 한글 깨짐 막기는 common 하나로
import make_board  # noqa: E402


def normalise(spec: dict) -> dict:
    """예전 꼴(n·name·pages{이름: 주소})을 make_board 꼴(id·title·urls·pages[{key,label}])로."""
    spec = dict(spec)
    spec["live"] = True
    spec.setdefault("step", spec.get("title") or "참고 사이트 고르기")
    cands = spec.get("candidates") or []
    if cands and "urls" not in cands[0]:
        labels: list[str] = []
        for c in cands:
            for k in c.get("pages", {}):
                if k not in labels:
                    labels.append(k)
        keys = {lab: f"p{i + 1}" for i, lab in enumerate(labels)}
        spec["pages"] = [{"key": keys[lab], "label": lab} for lab in labels]
        spec["candidates"] = [{"id": str(c.get("n", i + 1)), "slug": f'{c.get("n", i + 1)}-live', "title": c.get("name", ""),
                               "meta": c.get("meta", ""), "urls": {keys[k]: u for k, u in c.get("pages", {}).items()},
                               **({"recommended": True} if c.get("recommended") else {})} for i, c in enumerate(cands)]
    spec.setdefault("pages", [{"key": "home", "label": "첫 화면"}])
    return spec


# 이름난 근거 없이 동네 가게·작은 해외 가게만 후보로 올리면 바탕부터 처진다(애견미용 18차: 일본 동네 미용실 둘·관악구 미용실·템플릿 —
# 사용자 「디자인 구리다, 바탕부터 일본 특유의 디자인」). 후보마다 kind·known·region 을 적게 하고 빠지면 알린다
REAL = ("real", "neighbour")
CHANNEL_URL = re.compile(r"(map|place|m\.place|booking)\.naver\.com|naver\.me|instagram\.com|pf\.kakao\.com")
MIN_KNOWN = 3


def candidate_issues(spec: dict) -> list[str]:
    """후보 점검 — 이름난 근거(known), 종류(kind), 추천 후보가 손님 지역과 맞는지(region·fit)."""
    cands = spec.get("candidates") or []
    market = spec.get("market", "")
    out = []
    no_kind = [c.get("title", "?") for c in cands if not c.get("kind")]
    if no_kind:
        out.append(f"종류(kind: real·neighbour·award·template)가 없음: {', '.join(no_kind)}")
    weak = [c.get("title", "?") for c in cands if c.get("kind") in REAL and not c.get("known")]
    if weak:
        out.append(f"이름난 근거(known: 방문 규모·이름난 브랜드·수상)가 없는 실제 사이트: {', '.join(weak)} — 동네 가게 사이트는 바탕 후보가 아니다. "
                   "같은 일을 하는 이웃 분야 선두로 바꾼다(design-selection.md § 2)")
    channels = [c.get("title", "?") for c in cands if c.get("kind") == "channel" or any(
        CHANNEL_URL.search(u) for u in (c.get("urls") or {}).values())]
    if channels:
        out.append(f"플랫폼 화면은 후보가 아님: {', '.join(channels)} — 네이버 지도·플레이스·예약, 인스타, 카카오 채널은 빼고 시안에서 그리로 보내는 연결만 둔다(design-selection.md § 3)")
    known = [c for c in cands if c.get("known")]
    if cands and len(known) < MIN_KNOWN:
        out.append(f"이름난 후보가 {len(known)}개 — {MIN_KNOWN}개 이상으로(이웃 분야 선두를 더한다)")
    rec = next((c for c in cands if c.get("recommended")), None)
    if rec and (rec.get("kind") in ("template", "channel") or not rec.get("known")):
        out.append(f"추천 후보 「{rec.get('title', '?')}」에 이름난 근거가 없음 — 추천은 이름난 후보 가운데서")
    if rec and market and rec.get("region") and rec["region"] != market and not rec.get("fit"):
        out.append(f"추천 후보 「{rec.get('title', '?')}」는 {rec['region']} 사이트인데 손님은 {market} — 그 나라 특유의 꼴이 손님에게 맞는 까닭(fit)을 적거나 다른 후보를 추천")
    return out


def main(argv: list[str]) -> int:
    utf8_console()
    if len(argv) != 2:
        print(__doc__.strip(), file=sys.stderr)
        return 2
    spec_path = Path(argv[0])
    spec = normalise(json.loads(spec_path.read_text(encoding="utf-8")))
    # make_board 는 spec 파일 위치 기준으로 캡처를 찾는다 — 바꾼 spec 을 원래 자리 옆에 두고 넘긴다(live_proxy.mjs 에도 그대로 쓴다)
    live_spec = spec_path.with_name(spec_path.stem + "-live.json")
    live_spec.write_text(json.dumps(spec, ensure_ascii=False, indent=1), encoding="utf-8")
    code = make_board.main([str(live_spec), argv[1]])
    for line in candidate_issues(spec):
        print(f"후보 점검: {line}")
    return code


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
