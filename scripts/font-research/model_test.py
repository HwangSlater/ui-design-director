#!/usr/bin/env python3
"""모델이 글꼴 지시 없이 고르는 글꼴을 센다 — AI 글꼴 목록(assets/fonts/ai-fonts.json)의 근거.

    python -X utf8 scripts/font-research/model_test.py <작업 폴더> [--models haiku,sonnet,opus] [--runs 1]

주제마다·모델마다 빈 폴더에서 `claude -p` 로 메인 페이지 index.html 하나를 만들게 한다.
사용자 CLAUDE.md·설정·스킬은 끈다(CLAUDE_CODE_DISABLE_CLAUDE_MDS=1, --setting-sources project, --disable-slash-commands) —
전역 규칙에 「기본 글꼴 금지」가 있어 켜 두면 모델의 기본값이 안 보인다.
끊겨도 다시 돌리면 이미 만든 것은 건너뛴다(<작업 폴더>/<모델>-<주제>-<n>/index.html). 결과: <작업 폴더>/결과.md
"""
from __future__ import annotations

import argparse
import collections
import os
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "skills" / "ui-design-director" / "scripts"))
import fonts  # noqa: E402  (글꼴 선언 읽기는 fonts.py 하나로)

SUBJECTS = {
    "cafe": "동네 카페", "dental": "치과", "architect": "1인 건축사무소", "academy": "수학 학원",
    "shop": "옷 쇼핑몰", "camping": "오토캠핑장", "bookshop": "독립 서점", "festival": "지역 축제",
}
PROMPT = "{name} 홈페이지 메인 페이지를 만들어 줘. 지금 폴더에 index.html 하나로, 브라우저로 바로 열 수 있게."
TIMEOUT_S = 600
NPM_PKG = Path("node_modules") / "@anthropic-ai" / "claude-code"  # npm 으로 깐 claude.cmd 가 부르는 본체가 있는 곳


def claude_cmd() -> list[str]:
    """셸 없이 돌릴 claude 명령. 윈도에서 npm 으로 깔면 claude.cmd 라, 그것이 부르는 본체(bin/claude.exe, 옛 판은 cli.js)를
    직접 부른다(.cmd 를 부르면 인자 따옴표 처리가 cmd.exe 규칙을 타서 프롬프트가 깨질 수 있다)."""
    found = shutil.which("claude")
    if not found:
        raise SystemExit("claude 를 찾지 못했어요(PATH)")
    if Path(found).suffix.lower() not in (".cmd", ".bat"):
        return [found]
    pkg, node = Path(found).parent / NPM_PKG, shutil.which("node")
    if (pkg / "bin" / "claude.exe").is_file():
        return [str(pkg / "bin" / "claude.exe")]
    if (pkg / "cli.js").is_file() and node:
        return [node, str(pkg / "cli.js")]
    raise SystemExit(f"{found} 가 부르는 본체를 찾지 못했어요({pkg}) — 셸 없이 부를 수 있는 claude.exe 가 필요해요")


def run_one(claude: list[str], folder: Path, model: str, subject: str) -> None:
    folder.mkdir(parents=True, exist_ok=True)
    env = {**os.environ, "CLAUDE_CODE_DISABLE_CLAUDE_MDS": "1"}
    cmd = [*claude, "-p", "--model", model, "--setting-sources", "project", "--disable-slash-commands",
           "--tools=Write", "--allowedTools=Write", PROMPT.format(name=SUBJECTS[subject])]
    r = subprocess.run(cmd, cwd=folder, env=env, stdin=subprocess.DEVNULL, capture_output=True, timeout=TIMEOUT_S)
    if r.returncode != 0:
        print(f"실패 {folder.name} (종료 코드 {r.returncode})", flush=True)


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("work")
    ap.add_argument("--models", default="haiku,sonnet,opus")
    ap.add_argument("--runs", type=int, default=1)
    a = ap.parse_args(argv)
    work = Path(a.work)
    tally: dict[str, collections.Counter] = {}
    claude = claude_cmd()
    for model in a.models.split(","):
        tally[model] = collections.Counter()
        for subject in SUBJECTS:
            for n in range(1, a.runs + 1):
                folder = work / f"{model}-{subject}-{n}"
                page = folder / "index.html"
                if not page.is_file():
                    try:
                        run_one(claude, folder, model, subject)
                    except subprocess.TimeoutExpired:  # 한 번 멈춰도 나머지는 이어서 돈다
                        print(f"시간 초과 {folder.name}", flush=True)
                    except OSError as err:
                        print(f"실행 못 함 {folder.name}: {err}", flush=True)
                if not page.is_file():
                    print(f"못 만듦 {folder.name}", flush=True)
                    continue
                fams = []
                for fam in fonts.families(page.read_text(encoding="utf-8", errors="replace")):
                    if fam.lower() not in fonts_generic and fam not in fams:
                        fams.append(fam)
                tally[model].update(fams)
                print(f"{folder.name}: {', '.join(fams) or '(글꼴 선언 없음)'}", flush=True)
    lines = ["# 모델이 지시 없이 고른 글꼴", "", f"주제 {len(SUBJECTS)}개 × {a.runs}번. 사용자 CLAUDE.md·설정·스킬 끔.", ""]
    for model, c in tally.items():
        lines.append(f"- **{model}**: " + ", ".join(f"{k} {v}" for k, v in c.most_common()))
    (work / "결과.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines[4:]))
    return 0


fonts_generic = {"sans-serif", "serif", "monospace", "system-ui", "-apple-system", "blinkmacsystemfont", "apple sd gothic neo",
                 "malgun gothic", "맑은 고딕", "segoe ui", "helvetica", "helvetica neue", "arial", "roboto", "inherit",
                 "ui-sans-serif", "ui-serif", "georgia", "times new roman", "cursive", "dotum", "돋움", "gulim", "굴림"}

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
