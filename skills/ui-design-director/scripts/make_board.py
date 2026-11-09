#!/usr/bin/env python3
"""Build the full-screen candidate viewer (one candidate at a time, PC or phone frame).

Usage:
  python make_board.py <spec.json> --jobs <jobs.json>   # write capture jobs for capture.mjs
  python make_board.py <spec.json> <out.html>           # build the viewer from captured files

Spec (paths relative to the spec file):
  { "project": "...", "step": "뼈대 고르기", "dock": 1 | 2 | 3, "pages_mode": "tabs" | "stack",
    "live": true  -> 실제 사이트 모드: 가운데에 실제 페이지(막힌 곳은 live_proxy.mjs 로), 캡처는 썸네일과 대신 보기로만
    "captures": "captures", "widths": [1280, 390],
    "pages": [{"key": "home", "label": "첫 화면"}, ...],
    "candidates": [{ "id": "1", "slug": "1-craft", "title": "Craft", "meta": "Shopify · 무료",
                     "recommended": true, "demo": "<url>",
                     "urls": {"home": "<url>", "cart": "<url>"},
                     "steps": {"cart": [{"goto": "<url>"}, {"click": "<css>"}]} }] }
Captured files are expected at <captures>/<slug>-<page>-<width>.jpg. A page appears
for a candidate when at least one width was captured; missing pages are disabled.
assets/dock.css, dock.js (shared bottom bar), board.css and board.js are copied next to the output.
In live mode without captures, thumbnails come from <out dir>/thumbs/<candidate id>.jpg, which
live_proxy.mjs shoots in the background after OPEN (board.js retries until they appear).
"""

from __future__ import annotations

import html
import json
import os
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import utf8_console  # noqa: E402  콘솔 한글 깨짐 막기는 common 하나로
from frame_check import frame_policy  # noqa: E402  틀 안에 띄울 수 있는지(실제 사이트 모드)

ASSETS = Path(__file__).resolve().parent.parent / "assets"
DEFAULT_WIDTHS = (1440, 390)
PAGE_MODES = {"tabs", "stack"}  # 화면을 한 장씩 / 이어 붙여 스크롤로
DOCKS = {1, 2, 3}  # 아래 막대 모양: 한 줄 / 두 층 / 세 덩어리
ICONS = {
    "prev": '<path d="M15 6l-6 6 6 6"/>',
    "next": '<path d="M9 6l6 6-6 6"/>',
    "pc": '<rect x="3" y="4" width="18" height="12" rx="2"/><path d="M8 20h8M12 16v4"/>',
    "phone": '<rect x="7" y="3" width="10" height="18" rx="2"/><path d="M11 18h2"/>',
    "demo": '<path d="M14 4h6v6M20 4l-9 9M18 14v5a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1V7a1 1 0 0 1 1-1h5"/>',
    "hide": '<path d="M6 9l6 6 6-6"/>',
    "show": '<path d="M6 15l6-6 6 6"/>',
    "check": '<path d="M5 12.5l4.5 4.5L19 7.5"/>',
}


def icon(name: str) -> str:
    return f'<svg viewBox="0 0 24 24" aria-hidden="true">{ICONS[name]}</svg>'


def load(spec_path: Path) -> dict:
    spec = json.loads(spec_path.read_text(encoding="utf-8"))
    for key in ("pages", "candidates"):
        if not spec.get(key):
            raise ValueError(f"spec needs a non-empty '{key}' list")
    return spec


def jpeg_size(path: Path) -> tuple[int, int] | None:
    """JPEG 머리에서 (가로, 세로)를 읽는다. 이어 보기에서 사진이 오기 전에 자리를 잡아 두려고 쓴다."""
    data = path.read_bytes()
    i = 2
    while i + 9 < len(data):
        if data[i] != 0xFF:
            return None
        marker = data[i + 1]
        length = int.from_bytes(data[i + 2:i + 4], "big")
        if 0xC0 <= marker <= 0xCF and marker not in (0xC4, 0xC8, 0xCC):
            return int.from_bytes(data[i + 7:i + 9], "big"), int.from_bytes(data[i + 5:i + 7], "big")
        i += 2 + length
    return None


def write_jobs(spec: dict, jobs_path: Path) -> int:
    jobs = []
    for c in spec["candidates"]:
        for page, url in c.get("urls", {}).items():
            job = {"id": f'{c["slug"]}-{page}', "url": url}
            steps = c.get("steps", {}).get(page)  # 찍기 전에 할 일(예: 상품 담기)
            if steps:
                job["steps"] = steps
            jobs.append(job)
    jobs_path.write_text(json.dumps(jobs, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"wrote {len(jobs)} jobs to {jobs_path}")
    return 0


def resolve_pages(spec: dict, spec_dir: Path, out_dir: Path) -> list[dict]:
    widths = list(spec.get("widths", DEFAULT_WIDTHS))
    # 폭을 하나만 주면(휴대폰 화면만 비교할 때) 그 폭을 휴대폰으로 본다. 둘이면 넓은 쪽이 PC
    if not widths:
        widths = list(DEFAULT_WIDTHS)
    phone_w = min(widths)
    desktop_w = max(widths) if len(widths) > 1 else None
    cap_dir = spec_dir / spec.get("captures", "captures")
    candidates = []
    for c in spec["candidates"]:
        pages = {}
        for p in spec["pages"]:
            entry = {"url": c.get("urls", {}).get(p["key"], "")}
            for kind, width in (("desktop", desktop_w), ("phone", phone_w)):
                if width is None:
                    continue
                f = cap_dir / f'{c["slug"]}-{p["key"]}-{width}.jpg'
                if f.is_file():
                    entry[kind] = Path(os.path.relpath(f, out_dir)).as_posix()
                    size = jpeg_size(f)
                    if size:
                        entry[f"{kind}_size"] = size
            if "desktop" in entry or "phone" in entry or (spec.get("live") and entry["url"]):
                pages[p["key"]] = entry
        if not pages:
            print(f'WARN: no captures for candidate {c["id"]} ({c["slug"]}); skipped', file=sys.stderr)
            continue
        item = {k: c[k] for k in ("id", "title", "meta", "recommended", "demo") if k in c}
        item["pages"] = pages
        if spec.get("live"):
            # 실제 사이트 모드: 틀 안 띄우기를 막거나 열리지 않는 후보는 우회(live_proxy.mjs)로 띄운다
            first = next((e["url"] for e in pages.values() if e.get("url")), "")
            state = frame_policy(first) if first else "error"
            print(f'{c["id"]} {c.get("title", "")}: {state}')
            if state != "ok":
                item["blocked"] = True
        candidates.append(item)
    if not candidates:
        raise ValueError("no candidate has any captured page")
    return candidates


def build(spec: dict, candidates: list[dict]) -> str:
    dock = spec.get("dock", 1)
    if dock not in DOCKS:
        raise ValueError(f"dock must be one of {sorted(DOCKS)}")
    mode = spec.get("pages_mode", "tabs")
    if mode not in PAGE_MODES:
        raise ValueError(f"pages_mode must be one of {sorted(PAGE_MODES)}")
    data = {"step": spec.get("step", ""), "mode": mode, "pages": spec["pages"], "candidates": candidates, "live": bool(spec.get("live"))}
    total = len(candidates)
    payload = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")  # 데이터 안의 </script> 가 태그를 닫지 않게
    project = html.escape(spec.get("project", ""))
    step = html.escape(spec.get("step", ""))
    return f"""<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="check-site" content="comparison-board">
<title>{step} · {project}</title>
<link rel="stylesheet" href="dock.css">
<link rel="stylesheet" href="board.css">
</head>
<body class="dock-{dock}">
<main class="v-stage" aria-label="{step}">
<div class="v-desktop"><div class="v-scroll" tabindex="0" aria-label="PC 화면"></div></div>
<div class="v-phone"><div class="v-scroll" tabindex="0" aria-label="휴대폰 화면"></div></div>
</main>
<nav class="v-nav" aria-label="후보와 화면 고르기">
<div class="v-bar-main v-bar">
<div class="v-group v-g-cands"><button class="v-btn icon v-prev" type="button" aria-label="이전 후보" data-tip="이전 후보|←">{icon("prev")}</button><ol class="v-thumbs" aria-label="후보"></ol><button class="v-btn icon v-next" type="button" aria-label="다음 후보" data-tip="다음 후보|→">{icon("next")}</button></div>
<span class="v-rule" aria-hidden="true"></span>
<div class="v-info" aria-live="polite"><span class="v-title"><b>{step}</b><span class="v-title-hint"> · {total}개 중 하나를 골라 주세요</span></span><p class="v-name"></p><span class="v-meta"></span><span class="v-count"></span></div>
<span class="v-rule" aria-hidden="true"></span>
<div class="v-group v-g-pages"><div class="v-seg v-pages" role="tablist" aria-label="화면"></div></div>
<span class="v-rule" aria-hidden="true"></span>
<div class="v-group v-g-tools"><div class="v-seg v-view" role="group" aria-label="PC 또는 휴대폰"><button class="v-btn" type="button" data-view="pc" data-tip="PC 화면으로 보기|M">{icon("pc")}PC</button><button class="v-btn" type="button" data-view="phone" data-tip="휴대폰 화면으로 보기|M">{icon("phone")}휴대폰</button></div><a class="v-btn icon v-demo" href="#" target="_blank" rel="noopener" aria-label="데모 사이트 새 창으로 열기" data-tip="실제 데모 사이트를 새 창으로 열기">{icon("demo")}</a><button class="v-btn v-confirm" type="button">{icon("check")}<span class="v-label">확정</span></button><button class="v-btn icon v-hide" type="button" aria-label="막대 숨기기" data-tip="막대 숨기기|H">{icon("hide")}</button></div>
<p class="v-keys"><kbd>←</kbd> <kbd>→</kbd> 후보 · <kbd>↑</kbd> <kbd>↓</kbd> 화면 · <kbd>M</kbd> 휴대폰 · <kbd>H</kbd> 숨기기</p>
</div>
<button class="v-btn v-bar v-reveal" type="button" aria-label="조작 막대 다시 열기"><span class="v-reveal-where"><b></b><span></span></span><span class="v-reveal-open">{icon("show")}열기 H</span></button>
</nav>
<script type="application/json" id="board-data">{payload}</script>
<script src="dock.js"></script>
<script src="board.js"></script>
</body>
</html>
"""


def main(argv: list[str]) -> int:
    utf8_console()
    if len(argv) == 3 and argv[1] == "--jobs":
        mode, spec_path, target = "jobs", Path(argv[0]), Path(argv[2])
    elif len(argv) == 2:
        mode, spec_path, target = "board", Path(argv[0]), Path(argv[1])
    else:
        print(__doc__.strip(), file=sys.stderr)
        return 2
    try:
        spec = load(spec_path)
        if mode == "jobs":
            return write_jobs(spec, target)
        target.parent.mkdir(parents=True, exist_ok=True)
        candidates = resolve_pages(spec, spec_path.parent, target.parent)
        target.write_text(build(spec, candidates), encoding="utf-8")
    except (OSError, ValueError, KeyError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    for name in ("dock.css", "dock.js", "board.css", "board.js"):
        shutil.copyfile(ASSETS / name, target.parent / name)
    print(f"wrote {target} ({len(candidates)} candidates)")
    if spec.get("live") and not os.environ.get("UIDD_FROM_PROXY"):
        # 보기 화면은 늘 live_proxy 로 연다 — 막힌 후보 우회와 「확정」 기록을 한 주소에서 한다
        print(f"다음 → node {Path(__file__).resolve().parent.as_posix()}/live_proxy.mjs <spec.json> 이 찍는 OPEN 주소 하나를 의뢰인에게 주세요")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
