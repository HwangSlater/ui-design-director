#!/usr/bin/env python3
"""참고 사이트를 캡처하지 않고 실제로 띄워 넘겨 보는 화면을 만든다(외부 패키지 없음).

    python make_live_board.py <spec.json> <out.html>

spec: { "title": "참고 사이트 고르기 · 솔담",
        "candidates": [ {"n": "1", "name": "스테이폴리오", "meta": "실제 사이트 · …",
                         "pages": {"숙소": "<주소>", "객실": "<주소>"}, "shot": "<첫 화면 그림, 선택>"} ] }

후보마다 첫 페이지 응답 머리(X-Frame-Options, CSP frame-ancestors)를 보고, 다른 페이지 안에 띄우는 걸
막는 사이트는 「새 창으로 열기」 안내로 바꾼다. 인증서 오류·접속 실패도 같이 알려 준다.
막지 않아도 스크립트로 빠져나가는 사이트가 있으니, 만든 뒤 한 번 열어 보고 확인한다.
막힌 사이트에 "shot"(capture.mjs 로 찍은 첫 화면 그림 경로)이 있으면 빈 안내 대신 그 그림을 보여 준다 —
그림만 볼 수 있는 의뢰인이 「흰 화면에 새 창으로 열기 글만 있다, 왜 넣었냐」고 물었다.
처음에 애니메이션이나 로딩 화면이 있는 사이트는 첫 화면 그림이 까맣게 찍힌다. 그런 후보는 다른 페이지(객실)를 먼저 보이거나 뺀다.
"""
from __future__ import annotations

import html
import json
import ssl
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

TEMPLATE = Path(__file__).resolve().parent.parent / "assets" / "live-board.html"
TIMEOUT_S = 15
UA = "Mozilla/5.0 (compatible; ui-design-director live board)"


def frame_policy(url: str) -> str:
    """'ok' · 'blocked' · 'cert' · 'error' — 다른 페이지 안에 띄울 수 있는지."""
    # 한글이 든 주소(?status=입양가능)는 그대로 보내면 멈춘다 — 퍼센트 인코딩
    safe_url = urllib.parse.quote(url, safe=":/?&=%#+,;@!$'()*~")
    req = urllib.request.Request(safe_url, method="GET", headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT_S) as r:
            xfo = (r.headers.get("X-Frame-Options") or "").lower()
            csp = (r.headers.get("Content-Security-Policy") or "").lower()
    except urllib.error.URLError as e:
        return "cert" if isinstance(getattr(e, "reason", None), ssl.SSLError) else "error"
    except (ssl.SSLError, TimeoutError, OSError, ValueError, UnicodeError):
        return "error"
    if xfo in ("deny", "sameorigin"):
        return "blocked"
    if "frame-ancestors" in csp:
        rule = csp.split("frame-ancestors", 1)[1].split(";", 1)[0]
        if "*" not in rule.split():
            return "blocked"
    return "ok"


NOTE = {"blocked": "다른 페이지 안에 띄우는 걸 막는 사이트예요 → 「새 창으로 열기」",
        "cert": "보안 인증서 오류로 브라우저가 경고를 띄워요",
        "error": "지금 열리지 않아요"}


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print(__doc__.strip(), file=sys.stderr)
        return 2
    spec = json.loads(Path(argv[0]).read_text(encoding="utf-8"))
    cands = spec.get("candidates") or []
    if not cands:
        print("ERROR: candidates 가 비었어요", file=sys.stderr)
        return 2
    for c in cands:
        first = next(iter(c["pages"].values()))
        state = frame_policy(first)
        print(f'{c["n"]} {c["name"]}: {state}')
        if state != "ok":
            c["blocked"] = True
            c["meta"] = f'{c.get("meta", "")} · {NOTE[state]}'.strip(" ·")
    data = json.dumps(cands, ensure_ascii=False, indent=1).replace("</", "<\\/")
    page = TEMPLATE.read_text(encoding="utf-8").replace("__DATA__", data).replace("__TITLE__", html.escape(spec.get("title", "참고 사이트 고르기")))
    Path(argv[1]).write_text(page, encoding="utf-8")
    print(f"wrote {argv[1]}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
