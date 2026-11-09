#!/usr/bin/env python3
"""고른 바탕의 자료를 모으기 전에 할 일을 한 번에 깐다.

    python base_material.py <project folder> [<바탕 주소>] [--name <이름>]

주소를 안 주면 확정에서 읽는다: decisions.json 의 base(--decide) 또는 formats/decision.json(보기 화면 「확정」)을
formats/board-spec.json 의 후보와 맞춰, 보기 화면이 띄운 그 페이지 주소를 쓴다(사이트 첫 화면 주소가 아니라 — 첫 화면이
쇼핑 탭으로 열려 바탕 자료를 세 번 모았다). 쓴 주소는 「바탕 주소:」 줄로 찍는다.
스킬 프로젝트에서 바탕이 아직 확정되지 않았으면 아무것도 만들지 않고 1 로 끝난다(stage.py 의 단계 판단).

- formats/jobs-base.json: capture.mjs·snapshot.mjs 가 읽는 일 목록(바탕 홈, 주소가 사이트 첫 화면이 아니면 첫 화면도)
- formats/바탕-구성.md: 구역 표·시각 층·바꿀 곳(n/N)을 채우는 빈 틀. formats/추출-1280.json(extract_styles.mjs)이
  있으면 글자 크기를 미리 적는다. 맨 위 「채우기 전」 줄을 지우기 전에는 stage.py 가 바탕 자료를 안 된 것으로 본다.
이미 있는 파일은 덮어쓰지 않는다(「있음, 건너뜀」). 끝에 다음에 돌릴 명령을 실제 경로로 찍는다.
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path
from urllib.parse import urlsplit

import stage  # 단계 판단·확정 읽기는 stage.py 하나로
from make_live_board import normalise  # 후보 spec 의 두 꼴은 보기 화면을 만드는 쪽과 같게 읽는다
from stage import S, TEMPLATE_MARK  # 다음 명령의 실제 경로와 빈 틀 표시는 stage.py 와 같게

EXTRACT = "추출-1280.json"
ROWS = ["머리(메뉴)", "첫 화면", "", "", "", "바닥"]  # 빈 이름 줄은 바탕을 보며 채운다 — 구역 수는 바탕대로 늘리거나 줄인다
LAYERS = ["정체성(로고·이름 표기)", "항목 얼굴(카드·목록 한 칸 모양)", "아이콘", "색 덩어리", "데이터 표시(숫자·별점·뱃지)",
          "사진·그림", "깊이(그림자·겹침)", "넓은 화면 단 나눔"]


def candidates(spec: dict) -> list[tuple[str, str, str]]:
    """board-spec 의 후보를 (번호, 이름, 보기 화면이 처음 띄우는 페이지 주소)로. 예전 꼴(n·name·pages)은 make_live_board 가 바꾸는 대로."""
    spec = normalise(spec)
    order = [p.get("key") for p in spec.get("pages") or [] if isinstance(p, dict)]
    out = []
    for i, c in enumerate(spec.get("candidates") or [], 1):
        urls = c.get("urls") if isinstance(c, dict) else None
        if not isinstance(urls, dict) or not urls:
            continue
        first = next((urls[k] for k in order if urls.get(k)), None) or next(iter(urls.values()))
        out.append((str(c.get("id") or i), str(c.get("title") or ""), first))
    return out


def chosen(root: Path) -> str:
    """확정된 바탕을 가리키는 글 — decisions.json 의 base 가 먼저(stage.decisions 와 같은 차례), 없으면 formats/decision.json."""
    text = (stage.saved(root) or {}).get("base")
    if text:
        return str(text)
    try:
        d = json.loads((root / "formats" / "decision.json").read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return ""
    c = d.get("choice") if isinstance(d, dict) else None
    if isinstance(c, dict) and c.get("candidate"):
        return f"{c['candidate']} {c.get('title', '')}".strip()
    return str(d.get("label", "")) if isinstance(d, dict) else ""


def decided_url(root: Path) -> tuple[str, str] | None:
    """확정된 바탕의 (주소, 「번호 이름」). 확정이 없거나 후보와 맞지 않으면 None."""
    text = chosen(root)
    try:
        spec = json.loads((root / "formats" / "board-spec.json").read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    if not text or not isinstance(spec, dict):
        return None
    head = text.strip().split()[0].rstrip("번.") if text.strip() else ""
    rows = candidates(spec)
    hit = next((r for r in rows if r[0] == head), None) or next((r for r in rows if r[1] and r[1] in text), None)
    return (hit[2], f"{hit[0]} {hit[1]}".strip()) if hit else None


def jobs(url: str) -> list[dict]:
    """바탕 홈과(다르면) 사이트 첫 화면."""
    parts = urlsplit(url)
    out = [{"id": "base-home", "url": url}]
    root = f"{parts.scheme}://{parts.netloc}/"
    if url.rstrip("/") != root.rstrip("/"):
        out.append({"id": "base-root", "url": root})
    return out


def type_sizes(extract: Path) -> tuple[str, str, str]:
    """추출 결과에서 (첫 화면 제목, 구역 제목, 본문) 글자 크기. 없으면 빈 글자."""
    try:
        roles = json.loads(extract.read_text(encoding="utf-8")).get("roles", {})
    except (OSError, json.JSONDecodeError, AttributeError):
        return "", "", ""

    def common(items: list[dict]) -> str:
        sizes = Counter(i.get("size") for i in items if isinstance(i, dict) and i.get("size"))
        return sizes.most_common(1)[0][0] if sizes else ""

    heads = roles.get("heading") or []
    return (common([h for h in heads if h.get("tag") == "h1"]) or common(heads),
            common([h for h in heads if h.get("tag") in ("h2", "h3")]),
            common(roles.get("body") or []))


def template(name: str, url: str, sizes: tuple[str, str, str]) -> str:
    hero, head, body = sizes
    src = f"(formats/{EXTRACT} 에서 — 맞는지 스냅샷으로 확인)" if any(sizes) else f"(formats/{EXTRACT} 이 아직 없어 비워 둠 — 추출 뒤 옮겨 적는다)"
    # 첫 화면 줄에는 가장 큰 제목, 나머지 구역에는 구역 제목 크기를 먼저 적어 둔다
    rows = [f"| {i + 1} {r} | | | {f'{hero if i == 1 else head} / {body}' if any(sizes) else ''} | | |" for i, r in enumerate(ROWS)]
    layers = [f"| {layer} | | |" for layer in LAYERS]
    return "\n".join([
        f"{TEMPLATE_MARK} 다 채우면 이 줄을 지운다",
        f"# 바탕 구성 — {name}", "",
        f"주소: {url}", f"글자 크기 {src}", "",
        "## 구역", "", "높이 비율은 첫 화면 높이(1280×900) 기준, 사진 비율은 가로:세로.", "",
        "| 구역(위→아래) | 높이 비율 | 사진 비율 | 글자 크기(제목/본문) | 칸 수 | 하는 일 |",
        "|---|---|---|---|---|---|", *rows, "",
        "## 시각 층", "", "바탕에서 본 것을 적고 지킴·바꿈·뺌 가운데 하나를 고른다.", "",
        "| 층 | 바탕에서 본 것 | 지킴·바꿈·뺌 |", "|---|---|---|", *layers, "",
        "## 바꿀 곳(n/N)", "", "skeleton.mjs --base 결과에서 관련 사이트 N곳 가운데 n곳이 함께 다르게 하는 곳만 적는다. 나머지는 바탕을 따른다.", "",
        "| 곳 | n/N | 바탕은 | 바꿀 모습 |", "|---|---|---|---|", "| | | | |", "",
    ])


def write_new(path: Path, text: str) -> None:
    if path.exists():
        print(f"있음, 건너뜀: {path}")
        return
    path.write_text(text, encoding="utf-8")
    print(f"만듦: {path}")


def main(argv: list[str]) -> int:
    for s in (sys.stdout, sys.stderr):
        s.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser(description="바탕 자료 준비: jobs-base.json·바탕-구성.md 빈 틀")
    ap.add_argument("project")
    ap.add_argument("url", nargs="?", default="", help="안 주면 확정된 바탕의 페이지 주소")
    ap.add_argument("--name", default="")
    a = ap.parse_args(argv)
    root = Path(a.project)
    fm = root / "formats"
    why = stage.output_block(fm / "바탕-구성.md", "material")
    if why:
        print(f"멈춤: {why}", file=sys.stderr)
        return 1
    if not a.url:
        found = decided_url(root.resolve())
        if not found:
            print("바탕 주소를 찾지 못했어요 — 확정(decisions.json 의 base 또는 formats/decision.json)과 formats/board-spec.json 의 후보가 맞지 않음. "
                  "주소를 직접 주세요: base_material.py <project> <바탕 주소>", file=sys.stderr)
            return 2
        a.url, label = found
        a.name = a.name or label
        print(f"바탕 주소: {a.url} (확정 「{label}」 — 보기 화면이 띄운 페이지)")
    else:
        print(f"바탕 주소: {a.url}")
    parts = urlsplit(a.url)
    if parts.scheme not in ("http", "https") or not parts.netloc:
        print(f"바탕 주소가 http(s) 주소가 아니에요: {a.url}", file=sys.stderr)
        return 2
    fm.mkdir(parents=True, exist_ok=True)
    write_new(fm / "jobs-base.json", json.dumps(jobs(a.url), ensure_ascii=False, indent=1) + "\n")
    write_new(fm / "바탕-구성.md", template(a.name or parts.netloc, a.url, type_sizes(fm / EXTRACT)))
    f = fm.as_posix() if a.project != "." else "formats"
    print("다음:")
    for cmd in (f"node {S}/snapshot.mjs {f}/jobs-base.json {f}/snapshot",
                f"node {S}/motion.mjs {a.url} {f}/바탕-움직임.md",
                f"node {S}/capture.mjs {f}/jobs-base.json {f}/base-cap",
                f"node {S}/extract_styles.mjs {a.url} {f}/{EXTRACT} --width 1280",
                f"node {S}/skeleton.mjs {f}/뼈대.md --width 1280 base={a.url} <이름=관련 사이트 주소> ... --base base"):
        print(f"  {cmd}")
    print(f"  → {f}/바탕-구성.md 를 채우고 맨 위 「채우기 전」 줄을 지운다")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
