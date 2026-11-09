#!/usr/bin/env python3
"""저장소 검사를 한 번에: 스킬 검사기, 파이썬 시험, node 시험. 부분마다 한 줄씩 결과를 찍고 하나라도 실패하면 1.

    python scripts/check_all.py
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FAIL_LINES = 20  # 실패한 부분에서 보여 줄 마지막 줄 수


def parts() -> list[tuple[str, list[str]]]:
    node_tests = sorted(str(p) for p in (ROOT / "tests").glob("*.mjs"))
    return [
        ("스킬 검사(validate_skill.py)", [sys.executable, "-X", "utf8", str(ROOT / "scripts" / "validate_skill.py")]),
        ("파이썬 시험(pytest)", [sys.executable, "-m", "pytest", "-q", "tests"]),
        ("node 시험", ["node", "--test", *node_tests]),
    ]


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    failed = 0
    for name, cmd in parts():
        try:
            r = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace")
            ok, lines = r.returncode == 0, (r.stdout + r.stderr).strip().splitlines()
        except OSError as err:  # node·파이썬을 못 찾음
            ok, lines = False, [str(err)]
        failed += not ok
        # 요약 줄: pytest 「N passed」, node 「ℹ fail N」처럼 통과·실패 수가 적힌 마지막 줄
        summary = next((ln for ln in reversed(lines) if re.search(r"pass|fail|error", ln, re.I)), lines[-1] if lines else "")
        print(f"{'통과' if ok else '실패'}  {name} — {summary.strip()}")
        if not ok:  # 실패한 부분만 끝부분을 보여 준다
            print("\n".join(f"    {line}" for line in lines[-FAIL_LINES:]))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
