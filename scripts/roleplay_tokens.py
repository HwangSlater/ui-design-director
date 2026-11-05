#!/usr/bin/env python3
"""역할극 디자이너 세션의 토큰을 구간별로 센다(하위 에이전트 포함).

사용: python -X utf8 scripts/roleplay_tokens.py <세션 ID> <phases.txt> [--project-dir <~/.claude/projects/… 폴더>]
  phases.txt: 한 줄에 「ISO 시각<TAB>구간 이름」. 의뢰인 역할이 디자이너 메시지를 받을 때마다 한 줄씩 더한다:
    python -c "import datetime as dt;print(dt.datetime.now(dt.timezone.utc).isoformat())" | sed 's/$/\t3 배치/' >> phases.txt
  --project-dir 를 안 주면 지금 폴더 이름에서 Claude Code 의 대화 기록 폴더를 찾는다.
  「응답」은 하위 에이전트 응답을 포함한 수, 「하위」는 그중 하위 에이전트 응답 수.
비용은 거의 다 「캐시 읽기」다 — 응답마다 앞의 대화를 통째로 다시 읽으므로 대화가 길어질수록 커진다(docs/역할극-기록.md).
"""
from __future__ import annotations

import datetime as dt
import json
import re
import sys
from pathlib import Path

KEYS = ("input_tokens", "cache_creation_input_tokens", "cache_read_input_tokens", "output_tokens")


def default_project_dir() -> Path:
    # Claude Code 는 작업 폴더 경로의 글자 아닌 것을 「-」로 바꾼 이름으로 대화 기록을 둔다
    return Path.home() / ".claude" / "projects" / re.sub(r"[^A-Za-z0-9]", "-", str(Path.cwd()))


def usage_rows(project: Path, session: str):
    files = [project / f"{session}.jsonl", *sorted((project / session / "subagents").glob("*.jsonl"))]
    for f in files:
        if not f.is_file():
            continue
        sub = "subagents" in f.parts
        seen: set[str] = set()
        for line in f.open(encoding="utf-8"):
            try:
                o = json.loads(line)
            except json.JSONDecodeError:
                continue
            m = o.get("message", {}) if o.get("type") == "assistant" else {}
            u = m.get("usage")
            # 한 응답이 생각·글·도구 호출마다 따로 한 줄씩 기록되고 줄마다 같은 usage 가 붙는다 — 응답 id 로 한 번만 센다
            mid = m.get("id")
            if mid in seen:
                continue
            if mid:
                seen.add(mid)
            if u:
                yield dt.datetime.fromisoformat(o["timestamp"].replace("Z", "+00:00")), sub, u


def main(argv: list[str]) -> int:
    for s in (sys.stdout, sys.stderr):
        s.reconfigure(errors="replace")
    args = [a for a in argv if not a.startswith("--")]
    if len(args) < 2:
        print(__doc__.strip(), file=sys.stderr)
        return 2
    project = Path(argv[argv.index("--project-dir") + 1]) if "--project-dir" in argv else default_project_dir()
    session, phases_file = args[0], Path(args[1])
    rows = list(usage_rows(project, session))
    if not rows:
        print(f"기록 없음: {project / (session + '.jsonl')}", file=sys.stderr)
        return 1
    phases = [line.rstrip("\n").split("\t", 1) for line in phases_file.open(encoding="utf-8") if line.strip()]
    phases = [(dt.datetime.fromisoformat(t), n) for t, n in phases]
    end = dt.datetime.max.replace(tzinfo=dt.timezone.utc)
    print(f"{'구간':<22}{'응답':>5}{'새 입력':>10}{'캐시 쓰기':>11}{'캐시 읽기':>13}{'출력':>9}{'하위':>6}")
    total = [0] * 6
    for i, (t0, name) in enumerate(phases):
        t1 = phases[i + 1][0] if i + 1 < len(phases) else end
        sel = [(s, u) for t, s, u in rows if t0 <= t < t1]
        v = [len(sel), *(sum(u.get(k, 0) for _, u in sel) for k in KEYS), sum(1 for s, _ in sel if s)]
        total = [a + b for a, b in zip(total, v)]
        print(f"{name:<22}{v[0]:>5}{v[1]:>10,}{v[2]:>11,}{v[3]:>13,}{v[4]:>9,}{v[5]:>6}")
    print(f"{'합계':<22}{total[0]:>5}{total[1]:>10,}{total[2]:>11,}{total[3]:>13,}{total[4]:>9,}{total[5]:>6}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
