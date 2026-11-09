#!/usr/bin/env python3
"""지금 어느 단계인지, 앞 단계가 확정됐는지, 다음에 정확히 돌릴 명령은 무엇인지 알려 준다.

    python stage.py <project folder>            # 단계 표 + 다음 명령 (늘 종료 코드 0 — 스킬을 열 때 자동으로 돈다)
    python stage.py <project folder> --require <단계>   # 그 단계를 만들어도 되는지: 앞 단계가 다 됐으면 0, 아니면 1
    python stage.py <project folder> --decide <base|palette> "<고른 것>"   # 채팅으로 받은 확정을 decisions.json 에 남긴다
    python stage.py --guard <단계> <쓸 곳>   # 스크립트(snapshot·motion·capture)가 프로젝트 formats/ 에 쓰기 전에: 되면 0, 아니면 1

단계(메인 페이지만): brief → board → base → material → palette → design → main
단계는 파일로 판단한다 — 규칙 글만으로는 디자이너가 틀을 건너뛰거나(직접 짠 보기 화면) 앞 단계 확정 없이 다음 화면을 만들었다.
확정은 보기 화면의 「확정」(live_proxy.mjs·wait_choice.mjs 가 쓰는 decision.json)이나 --decide 로 남긴 decisions.json 에서 읽는다.
decisions.json 이 깨져 있으면(JSON 이 아님) 알리고, --decide 는 덮어쓰지 않고 1 로 끝난다.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import utf8_console  # noqa: E402  콘솔 한글 깨짐 막기는 common 하나로
import knowledge  # noqa: E402  (단계마다 볼 규칙은 knowledge.py 하나로)

SKILL = Path(__file__).resolve().parent.parent
S = (SKILL / "scripts").as_posix()  # 다음 명령에 실제 경로를 찍는다(${CLAUDE_SKILL_DIR} 를 글자로 찍으면 그대로 남았다)
STAGES = ["brief", "board", "base", "material", "palette", "design", "main"]
LABEL = {"brief": "맥락 정리", "board": "바탕 고르기 화면", "base": "바탕 확정", "material": "바탕 자료(스냅샷·움직임·구성)",
         "palette": "색·글꼴 확정", "design": "DESIGN.md", "main": "메인 페이지 시안"}
SHARED_VIEWER = "board-data"  # make_board.py 공용 틀 표시
PALETTE_VIEWER = "palette-switcher.js"
TEMPLATE_MARK = "<!-- 채우기 전 -->"  # base_material.py 가 만든 빈 틀 표시 — 다 채우고 지우기 전에는 바탕 자료가 안 된 것으로 본다
DECIDABLE = ("base", "palette")  # --decide 로 남기는 확정은 이 둘뿐 — 「board」로 남겨 바탕이 안 정해진 채 남았다
PROJECT_MARKS = ("concept-brief.md", "decisions.json", "formats/board-spec.json")  # 스킬 프로젝트 폴더 표시
BROKEN = "decisions.json 을 읽을 수 없어요(JSON 형식이 깨짐) — 손으로 고치기 전에는 --decide 로 쓰지 않습니다"


def read(p: Path) -> str:
    try:
        return p.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""


def saved(root: Path) -> dict | None:
    """decisions.json 의 내용. 없으면 빈 dict, 깨졌으면(JSON 이 아니거나 객체가 아님) None."""
    text = read(root / "decisions.json")
    if not text.strip():
        return {}
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        return None
    return data if isinstance(data, dict) else None


def decisions(root: Path) -> dict:
    out = dict(saved(root) or {})
    # 보기 화면의 「확정」 — live_proxy.mjs(후보)·wait_choice.mjs(팔레트)가 쓴 decision.json
    for key, where in (("base", root / "formats" / "decision.json"), ("palette", root / "palette" / "decision.json")):
        if key not in out and where.is_file():
            try:
                d = json.loads(read(where))
                out[key] = d.get("label") or d.get("choice") or "확정됨"
            except (json.JSONDecodeError, AttributeError):
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
    filled = TEMPLATE_MARK not in read(material[0])
    snap = any((fm / "snapshot").glob("*/index.html")) if (fm / "snapshot").is_dir() else False
    design = read(root / "DESIGN.md")
    done = {
        "brief": bool(read(root / "concept-brief.md").strip()),
        "board": bool(boards),
        "base": "base" in d,
        "material": all(p.is_file() for p in material) and snap and filled,
        "palette": "palette" in d,
        "design": "바탕에서 바꾼 곳" in design and "부품 출처" in design,
        "main": (root / "mockups" / "index.html").is_file(),
    }
    issues = [BROKEN] if saved(root) is None else []
    issues += [f"공용 틀이 아님: {p.relative_to(root)} — 보기 화면은 make_live_board.py 로만 만든다" for p in own_boards]
    issues += [f"공용 틀이 아님: {p.relative_to(root)} — 팔레트 화면은 palette-switcher.js 틀로만 만든다(comparison-board.md § Palettes)" for p in own_pals]
    # 순서 어김: 뒤 단계의 결과물이 앞 단계 확정 없이 생겼다
    made = {"board": done["board"], "material": any(p.is_file() for p in material) or snap,
            "palette": bool(pals or own_pals), "design": bool(design), "main": done["main"]}
    for st in STAGES:
        if made.get(st):
            missing = _missing(done, st)
            if missing:
                issues.append(f"순서 어김: {LABEL[st]}이(가) 있는데 앞 단계가 안 됨 — {', '.join(LABEL[s] for s in missing)}")
    return done, issues


def _missing(done: dict, stage: str) -> list[str]:
    return [s for s in STAGES[:STAGES.index(stage)] if not done[s]]


def missing_before(root: Path, stage: str) -> list[str]:
    """stage 를 만들기 전에 끝나야 하는데 아직 안 된 앞 단계들(stage.py --require 와 hooks/guard.py 가 함께 쓴다)."""
    return _missing(status(root)[0], stage)


def project_root(path: Path) -> Path | None:
    """파일 위쪽 폴더 가운데 스킬 프로젝트(맥락 정리·확정 기록·후보 spec 이 있는 곳). 없으면 None(hooks/guard.py 도 쓴다)."""
    for folder in path.parents:
        if any((folder / m).is_file() for m in PROJECT_MARKS):
            return folder
    return None


def output_block(out: Path, need: str) -> str | None:
    """스크립트가 프로젝트 formats/ 안에 쓰려는데 need 단계의 앞 단계가 안 됐으면 막을 이유. 프로젝트 밖이면 None.
    훅(guard.py)은 Write·Edit 만 보므로 바탕 자료를 만드는 스크립트는 이것으로 스스로 멈춘다."""
    out = Path(out).resolve()
    root = project_root(out / "_")  # out 이 폴더여도 그 자신부터 위로 찾는다
    if root is None or out == root or out.relative_to(root).parts[0] != "formats":
        return None
    missing = missing_before(root, need)
    if not missing:
        return None
    return (f"아직 {LABEL[need]}을(를) 만들 수 없음 — 먼저: {', '.join(LABEL[s] for s in missing)}. "
            f"python {S}/stage.py {root.as_posix()} 로 다음 명령을 보세요.")


NEXT = {
    "brief": "concept-brief.md 에 맥락(주 업무·손님·싫은 것·사진 누구 것)을 적는다 — 질문은 한 번에 하나",
    "board": f"후보 spec(formats/board-spec.json) → node {S}/live_proxy.mjs formats/board-spec.json (공용 틀 보기 화면을 만들고 OPEN 주소 하나를 찍는다 — 그 주소만 의뢰인에게. 「확정」은 DECISION 줄과 formats/decision.json 으로 온다). 의뢰인이 채팅으로 고르면: python {S}/stage.py . --decide base \"<번호 이름>\"",
    "base": f"의뢰인이 보기 화면에서 「확정」을 누르기를 기다린다(live_proxy.mjs 가 DECISION 줄을 찍고 formats/decision.json 을 쓴다). 채팅으로 답하면: python {S}/stage.py . --decide base \"<번호 이름>\"",
    "material": f"고른 바탕에 대해 먼저: python {S}/base_material.py . (바탕 주소는 확정과 board-spec.json 에서 읽어 「바탕 주소:」로 찍는다 — 그 주소를 아래 <바탕 주소> 에. jobs-base.json·바탕-구성.md 틀) → node {S}/snapshot.mjs formats/jobs-base.json formats/snapshot · node {S}/motion.mjs <바탕 주소> formats/바탕-움직임.md · node {S}/capture.mjs formats/jobs-base.json formats/base-cap · node {S}/extract_styles.mjs <바탕 주소> formats/추출-1280.json --width 1280 → formats/바탕-구성.md 를 채우고 맨 위 「채우기 전」 줄을 지운다",
    "palette": f"palette/index.html 을 palette-switcher.js 틀로(comparison-board.md § Palettes, 바탕의 4~6색 조합에서 출발), 글꼴은 python {S}/fonts.py pick --style <고딕|명조|손글씨|제목용> 에서만(references/fonts.md) → python {S}/fonts.py check palette → wait_choice.mjs palette/index.html palette/decision.json",
    "design": "DESIGN.md 를 design-md-format.md 틀로 — § 바탕에서 바꾼 곳, § 부품 출처 포함",
    "main": f"references/build-rules.md 를 따라 mockups/ 에 메인 페이지 — 완성 시안은 하위 에이전트 하나에 파일 경로와 build-rules.md 경로를 넘긴다 → python {S}/preflight.py .",
}


def main(argv: list[str]) -> int:
    utf8_console()
    if not argv:
        print(__doc__.strip(), file=sys.stderr)
        return 0
    if argv[0] == "--guard":
        if len(argv) < 3 or argv[1] not in STAGES:
            print(f"사용: stage.py --guard <단계> <쓸 곳> ({', '.join(STAGES)})", file=sys.stderr)
            return 2
        reason = output_block(Path(argv[2]), argv[1])
        if reason:
            print(reason, file=sys.stderr)
        return 1 if reason else 0
    root = Path(argv[0]).resolve()
    if len(argv) >= 4 and argv[1] == "--decide":
        if argv[2] not in DECIDABLE:
            what = "" if argv[2] in STAGES else f"모르는 단계: {argv[2]}. "
            print(f"{what}--decide 는 {'·'.join(DECIDABLE)} 만 받습니다. 후보 고르기는 base 로 남깁니다: --decide base \"<번호 이름>\"", file=sys.stderr)
            return 2
        if saved(root) is None:
            print(f"! {BROKEN}: {root / 'decisions.json'}", file=sys.stderr)
            return 1
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
        missing = _missing(done, st)
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
    # 그 단계에서 자주 결정을 가르는 규칙 몇 개 — 긴 지식 문서를 찾아 읽지 않아도 필요한 때 눈앞에 오게
    tips = knowledge.stage_lines(nxt or "review")
    if tips:
        print("이 단계에서 볼 규칙(부품별로 더: python " + f"{S}/knowledge.py ask --part <부품>):")
        for t in tips:
            print(f"  {t}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
