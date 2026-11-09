"""다른 페이지 안(iframe)에 띄울 수 있는 사이트인지 응답 머리로 본다 — 보기 화면이 바로 띄울지, 우회로 띄울지 정한다."""
from __future__ import annotations

import json
import ssl
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

TIMEOUT_S = 15
# 봇 이름으로 가면 네이버 지도가 막아 「열리지 않아요」로 잘못 나왔다 — 측정 도구(browser.mjs)와 같은 파일의 컴퓨터 브라우저 이름
UA = json.loads((Path(__file__).resolve().parent.parent / "assets" / "browser.json").read_text(encoding="utf-8"))["desktopUA"]


def frame_policy(url: str) -> str:
    """'ok' · 'blocked' · 'cert' · 'error'."""
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
