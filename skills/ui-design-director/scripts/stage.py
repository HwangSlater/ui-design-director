#!/usr/bin/env python3
"""지금 어느 단계인지, 앞 단계가 확정됐는지, 다음에 정확히 돌릴 명령은 무엇인지 알려 준다.

    python stage.py <project folder>            # 단계 표 + 다음 명령 (늘 종료 코드 0 — 스킬을 열 때 자동으로 돈다)
    python stage.py <project folder> --require <단계>   # 그 단계를 만들어도 되는지: 앞 단계가 다 됐으면 0, 아니면 1
    python stage.py <project folder> --decide <단계> "<고른 것>"   # 채팅으로 받은 확정을 decisions.json 에 남긴다

단계(메인 페이지만): brief → board → base → material → palette → design → main
단계는 파일로 판단한다 — 규칙 글만으로는 디자이너가 틀을 건너뛰거나(직접 짠 보기 화면) 앞 단계 확정 없이 다음 화면을 만들었다.
확정은 보기 화면의 「확정」(wait_choice.mjs 가 쓰는 decision.json)이나 --decide 로 남긴 decisions.json 에서 읽는다.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

SKILL = Path(__file__).resolve().parent.parent
S = (SKILL / "scripts").as_posix()  # 다음 명령에 실제 경로를 찍는다(${CLAUDE_SKILL_DIR} 를 글자로 찍으면 그대로 남았다)
STAGES = ["brief", "board", "base", "material", "palette", "design", "main"]
LABEL = {"brief": "맥락 정리", "board": "바탕 고르기 화면", "base": "바탕 확정", "material": "바탕 자료(스냅샷·움직임·구성)",
         "palette": "색·글꼴 확정", "design": "DESIGN.md", "main": "메인 페이지 시안"}
SHARED_VIEWER = "board-data"  # make_board.py 공용 틀 표시
PALETTE_VIEWER = "palette-switcher.js"


def read(p: Path) -> str:
    try:
        return p.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""


def decisions(root: Path) -> dict:
    out = {}
    try:
        out.update(json.loads(read(root / "decisions.json") or "{}"))
    except json.JSONDecodeError:
        pass
    # 보기 화면의 「확정」 — wait_choice.mjs 가 쓴 decision.json
    for key, where in (("base", root / "formats" / "decision.json"), ("palette", root / "palette" / "decision.json")):
        if key not in out and where.is_file():
            try:
                d = json.loads(read(where))
                out[key] = d.get("label") or d.get("choice") or "확정됨"
            except json.JSONDecodeError:
                pass
    return out


def viewers(folder: Path, mark: str) -> tuple[list[Path], list[Path]]:
    """폴더 안 HTML 가운데 공용 틀로 만든 것과 아닌 것."""
    ok, own = [], []
    for f in sorted(folder.glob("*.html")) if folder.is_dir() else []:
        text = read(f)
        if mark in text:
            ok.append(f)
        elif "<iframe" in text or text.count("<img") >= 3:
            own.append(f)  # 후보·팔레트를 보여 주는 화면인데 공용 틀이 아님
    return ok, own


def status(root: Path) -> tuple[dict, list[str]]:
    d = decisions(root)
    fm = root / "formats"
    boards, own_boards = viewers(fm, SHARED_VIEWER)
    pals, own_pals = viewers(root / "palette", PALETTE_VIEWER)
    material = [fm / "바탕-구성.md", fm / "바탕-움직임.md"]
    snap = any((fm / "snapshot").glob("*/index.html")) if (fm / "snapshot").is_dir() else False
    design = read(root / "DESIGN.md")
    done = {
        "brief": bool(read(root / "concept-brief.md").strip()),
        "board": bool(boards),
        "base": "base" in d,
        "material": all(p.is_file() for p in material) and snap,
        "palette": "palette" in d,
        "design": "바탕에서 바꾼 곳" in design and "부품 출처" in design,
        "main": (root / "mockups" / "index.html").is_file(),
    }
    issues = [f"공용 틀이 아님: {p.relative_to(root)} — 보기 화면은 make_live_board.py 로만 만든다" for p in own_boards]
    issues += [f"공용 틀이 아님: {p.relative_to(root)} — 팔레트 화면은 palette-switcher.js 틀로만 만든다(comparison-board.md § Palettes)" for p in own_pals]
    # 순서 어김: 뒤 단계의 결과물이 앞 단계 확정 없이 생겼다
    made = {"board": done["board"], "material": any(p.is_file() for p in material) or snap,
            "palette": bool(pals or own_pals), "design": bool(design), "main": done["main"]}
    for i, st in enumerate(STAGES):
        if made.get(st):
            missing = [s for s in STAGES[:i] if not done[s]]
            if missing:
                issues.append(f"순서 어김: {LABEL[st]}이(가) 있는데 앞 단계가 안 됨 — {', '.join(LABEL[s] for s in missing)}")
    return done, issues


NEXT = {
    "brief": "concept-brief.md 에 맥락(주 업무·손님·싫은 것·사진 누구 것)을 적는다 — 질문은 한 번에 하나",
    "board": f"후보 spec(formats/board-spec.json) → python {S}/make_live_board.py formats/board-spec.json formats/보기.html → node {S}/live_proxy.mjs formats/board-spec.json (OPEN 주소를 의뢰인에게) → node {S}/wait_choice.mjs formats/보기.html formats/decision.json",
    "base": f"의뢰인이 보기 화면에서 「확정」을 누르기를 기다린다(wait_choice.mjs). 채팅으로 답하면: python {S}/stage.py . --decide base \"<번호 이름>\"",
    "material": f"고른 바탕에 대해: node {S}/snapshot.mjs formats/jobs-base.json formats/snapshot · node {S}/motion.mjs <바탕 주소> formats/바탕-움직임.md · node {S}/capture.mjs formats/jobs-base.json formats/base-cap · node {S}/extract_styles.mjs <바탕 주소> formats/추출-1280.json --width 1280 → formats/바탕-구성.md 를 쓴다",
    "palette": "palette/index.html 을 palette-switcher.js 틀로(comparison-board.md § Palettes, 바탕의 4~6색 조합에서 출발) → wait_choice.mjs palette/index.html palette/decision.json",
    "design": "DESIGN.md 를 design-md-format.md 틀로 — § 바탕에서 바꾼 곳, § 부품 출처 포함",
    "main": f"references/build-rules.md 를 따라 mockups/ 에 메인 페이지 — 완성 시안은 하위 에이전트 하나에 파일 경로와 build-rules.md 경로를 넘긴다 → python {S}/preflight.py .",
}


def main(argv: list[str]) -> int:
    for s in (sys.stdout, sys.stderr):
        s.reconfigure(encoding="utf-8", errors="replace")  # 윈도 기본(cp949)으로 찍으면 스킬 지시문에 한글이 깨져 들어갔다
    if not argv:
        print(__doc__.strip(), file=sys.stderr)
        return 0
    root = Path(argv[0]).resolve()
    if len(argv) >= 4 and argv[1] == "--decide":
        d = decisions(root)
        d[argv[2]] = argv[3]
        (root / "decisions.json").write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"확정 남김: {argv[2]} = {argv[3]}")
        return 0
    done, issues = status(root)
    if len(argv) >= 3 and argv[1] == "--require":
        st = argv[2]
        if st not in STAGES:
            print(f"모르는 단계: {st} ({', '.join(STAGES)})", file=sys.stderr)
            return 2
        missing = [s for s in STAGES[:STAGES.index(st)] if not done[s]]
        if missing:
            print(f"아직 {LABEL[st]}을(를) 만들 수 없음 — 먼저: {', '.join(LABEL[s] for s in missing)}")
            return 1
        return 0
    print(f"단계 — {root.name}")
    for st in STAGES:
        print(f"  [{'x' if done[st] else ' '}] {LABEL[st]}")
    for line in issues:
        print(f"  ! {line}")
    nxt = next((s for s in STAGES if not done[s]), None)
    print(f"다음: {NEXT[nxt]}" if nxt else "다음: 메인 페이지까지 끝 — 의뢰인 판별을 받는다")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
