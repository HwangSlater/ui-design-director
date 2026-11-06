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
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
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


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print(__doc__.strip(), file=sys.stderr)
        return 2
    spec_path = Path(argv[0])
    spec = normalise(json.loads(spec_path.read_text(encoding="utf-8")))
    # make_board 는 spec 파일 위치 기준으로 캡처를 찾는다 — 바꾼 spec 을 원래 자리 옆에 두고 넘긴다(live_proxy.mjs 에도 그대로 쓴다)
    live_spec = spec_path.with_name(spec_path.stem + "-live.json")
    live_spec.write_text(json.dumps(spec, ensure_ascii=False, indent=1), encoding="utf-8")
    code = make_board.main([str(live_spec), argv[1]])
    return code


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
