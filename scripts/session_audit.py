#!/usr/bin/env python3
"""디자이너 세션이 의도대로 움직였는지 대화 기록으로 확인한다 — 단계마다 정해진 도구를 제때·순서대로 썼는가.

사용: python -X utf8 scripts/session_audit.py <프로젝트 폴더> [--session <세션 ID>] [--memo <의뢰인 메모.md>]
  세션을 안 주면 ~/.claude/projects 의 대화 기록 가운데 이 폴더 이름이 나오는 가장 최근 것을 쓴다.
  하위 에이전트 기록(<세션>/subagents/*.jsonl)도 함께 읽는다. 세션이 도는 중에도 돌릴 수 있다(그때까지의 기록).
  --memo: 메모의 「」 안 이름과 숫자 값(2만원·40개·10시 …)이 메인 시안(mockups/index.html)에 있는지 본다.

손으로 하던 검토(레시피 9차·NBA 12차 「도구를 제자리에 썼나」)를 매번 같은 기준으로 하려고 만들었다.
기대하는 일은 아래 STEPS 하나에만 적는다 — 스킬 흐름(stage.py 의 다음 명령)이 바뀌면 여기도 고친다.
"""
from __future__ import annotations

import datetime as dt
import json
import re
import subprocess
import sys
from pathlib import Path

PROJECTS = Path.home() / ".claude" / "projects"

# (단계, 할 일, 찾을 것). 찾을 것: "run:<정규식>" 은 셸 명령, "write:<정규식>" 은 쓰거나 고친 파일(프로젝트 기준 경로)
STEPS = [
    ("brief", "맥락 정리(사이트 꼴 포함)", "write:^concept-brief\\.md$"),
    ("board", "공용 틀 보기 화면", "run:make_live_board\\.py|live_proxy\\.mjs"),
    ("base", "바탕 확정 기록", "run:stage\\.py\\b.*--decide base|file:formats/decision\\.json"),
    ("material", "바탕 자료 틀", "run:base_material\\.py"),
    ("material", "바탕 통째 저장", "run:snapshot\\.mjs"),
    ("material", "바탕 움직임", "run:motion\\.mjs"),
    ("material", "바탕 캡처", "run:capture\\.mjs.*base"),
    ("material", "바탕 글자·색 재기", "run:extract_styles\\.mjs"),
    ("material", "바탕 구성 표", "write:^formats/바탕-구성\\.md$"),
    ("palette", "글꼴은 표에서", "run:fonts\\.py\\b.*\\bpick"),
    ("palette", "색상은 공개 팔레트에서", "run:palettes\\.py\\b.*\\bpick"),
    ("palette", "색·글꼴 확정 기록", "run:stage\\.py\\b.*--decide palette|file:palette/decision\\.json"),
    ("design", "바꿀 곳 재기(n/N)", "run:skeleton\\.mjs.*--base"),
    ("design", "DESIGN.md", "write:^DESIGN\\.md$"),
    ("main", "부품마다 지식 묻기", "run:knowledge\\.py\\b.*\\bask"),
    ("main", "견본 사진 찾기", "run:sample_photos\\.py"),
    ("main", "메인 시안", "write:^mockups/index\\.html$"),
    ("check", "사이트 점검", "run:check_site\\.py"),
    ("check", "우리 캡처", "run:capture\\.mjs.*mockups"),
    ("check", "바탕과 나란히", "run:side_by_side\\.py"),
    ("check", "보내기 전 점검", "run:preflight\\.py"),
    ("after", "시안 승인 기록", "run:stage\\.py\\b.*--decide main"),
    ("after", "사본 지우기(도구로)", "run:clear_copies\\.py"),
]
# 순서를 볼 대표 결과물 — 앞 단계 확정 없이 다음 단계를 만들면 순서 어김
GATES = ["맥락 정리(사이트 꼴 포함)", "공용 틀 보기 화면", "바탕 확정 기록", "바탕 구성 표", "색·글꼴 확정 기록", "DESIGN.md", "메인 시안"]
# 메인 시안을 만든 뒤 한 번 이상 돌아야 하는 점검
AFTER_PAGE = [("check_site.py", r"check_site\.py"), ("우리 캡처", r"capture\.mjs.*mockups"), ("side_by_side.py", r"side_by_side\.py"),
              ("preflight.py", r"preflight\.py")]
# 하면 안 되는 일: (이름, 정규식, 대상)
DONT = [
    ("남의 사이트 사본을 손으로 지움", r"\brm\b[^|;&]*formats/(snapshot|base-cap|pal-cap)|Remove-Item[^|;&]*formats[\\/](snapshot|base-cap)", "run"),
    ("보기 화면을 손으로 씀(make_live_board.py 가 만든다)", r"^formats/[^/]*\.html$", "write"),
]
SCRIPT = re.compile(r"[\w-]+\.(?:py|mjs)\b")


def utf8() -> None:
    for s in (sys.stdout, sys.stderr):
        s.reconfigure(encoding="utf-8", errors="replace")


def find_session(folder: Path) -> Path | None:
    """이 폴더 이름이 앞쪽 기록에 나오는 가장 최근 대화."""
    name = folder.name
    files = sorted(PROJECTS.glob("*/*.jsonl"), key=lambda p: p.stat().st_mtime, reverse=True)
    for f in files[:60]:
        with f.open(encoding="utf-8", errors="replace") as fh:
            head = "".join(line for _, line in zip(range(40), fh))
        if name in head and "ui-design-director" in head:
            return f
    return None


def events(main: Path, folder: Path):
    """(시각, 하위 여부, 종류, 내용) — 종류: run·write·read·ask·agent·error·client."""
    files = [main, *sorted((main.parent / main.stem / "subagents").glob("*.jsonl"))]
    root = folder.resolve().as_posix().lower()
    for f in files:
        sub = "subagents" in f.parts
        for line in f.open(encoding="utf-8", errors="replace"):
            try:
                o = json.loads(line)
            except json.JSONDecodeError:
                continue
            t = o.get("timestamp")
            m = o.get("message") or {}
            if not t or not isinstance(m.get("content"), (list, str)):
                continue
            when = dt.datetime.fromisoformat(t.replace("Z", "+00:00"))
            if o.get("type") == "user" and isinstance(m["content"], str) and not sub:
                yield when, sub, "client", m["content"]
                continue
            for c in m["content"] if isinstance(m["content"], list) else []:
                if c.get("type") == "tool_use":
                    name, inp = c["name"], c.get("input", {})
                    if name in ("Bash", "PowerShell"):
                        yield when, sub, "run", inp.get("command", "")
                    elif name in ("Write", "Edit", "NotebookEdit"):
                        p = str(inp.get("file_path", "")).replace("\\", "/")
                        low = p.lower()
                        yield when, sub, "write", p[len(root) + 1:] if low.startswith(root) else p
                    elif name == "Read":
                        yield when, sub, "read", str(inp.get("file_path", ""))
                    elif name == "AskUserQuestion":
                        yield when, sub, "ask", json.dumps(inp, ensure_ascii=False)[:200]
                    elif name == "Agent":
                        yield when, sub, "agent", inp.get("description", "")
                elif c.get("type") == "tool_result" and c.get("is_error"):
                    body = c.get("content")
                    text = body if isinstance(body, str) else json.dumps(body, ensure_ascii=False)
                    yield when, sub, "error", text
                elif c.get("type") == "text" and o.get("type") == "user" and not sub:
                    yield when, sub, "client", c.get("text", "")


def first(evs, spec: str, folder: Path):
    kind, pat = spec.split(":", 1)
    for alt in pat.split("|"):
        if alt.startswith("file:"):
            p = folder / alt[5:]
            if p.is_file():
                return dt.datetime.fromtimestamp(p.stat().st_mtime, dt.timezone.utc), False, "파일 " + alt[5:]
    rx = re.compile("|".join(a for a in pat.split("|") if not a.startswith("file:")) or "$^")
    for when, sub, k, body in evs:
        if k == kind and rx.search(body.replace("\\", "/")):
            return when, sub, body
        # 셸로 쓴 파일(heredoc·Out-File)도 쓴 것으로 — 치과 17차는 맥락 정리를 셸로 썼다
        if kind == "write" and k == "run" and shell_wrote(body, pat):
            return when, sub, body
    return None


def shell_wrote(cmd: str, pat: str) -> bool:
    """셸 명령이 그 파일에 썼나 — 「> 파일」「Out-File 파일」「Path('파일').write_text」. 글 속에 이름만 나온 것(체크리스트 줄)은 아니다."""
    core = pat.strip("^$")
    cmd = cmd.replace("\\", "/")
    target = r"""(?:>>?|Out-File|Set-Content|Add-Content)\s*(?:-(?:File)?Path\s*)?["']?[^"'\s|;<>]*?""" + core + r"""["']?(?:\s|$|;|\|)"""
    return re.search(target, cmd) is not None or re.search(core + r"""["']\)?\s*\.write_text""", cmd) is not None


def memo_values(memo: str) -> list[str]:
    """메모의 사실 값 — 「」 이름과 단위 붙은 숫자. 싫은 것·「그 밖에」 줄은 빼고."""
    facts = "\n".join(line for line in memo.splitlines() if not re.match(r"\s*-\s*(싫은 것|그 밖에)", line))
    names = re.findall(r"「([^」]{1,20})」", facts)
    nums = re.findall(r"\d+\s*(?:만\s*원|원|개|마리|시(?!간)|명|팀|주)", facts)  # 「1시간」은 시각이 아니다
    return list(dict.fromkeys(names + [re.sub(r"\s+", "", n) for n in nums]))


def in_page(value: str, flat: str) -> bool:
    """값이 시안 글에 있나 — 「9시」는 09:00·9:00 도, 「40개」는 40 이 다른 단위로 붙어도(40자리·40팀) 있는 것으로."""
    if re.sub(r"\s+", "", value) in flat:  # 시안 글은 띄어쓰기를 지우고 견준다 — 「털손질 소소」를 못 찾았다
        return True
    m = re.fullmatch(r"(\d+)(만원|원|개|마리|시|명|팀|주)", value)
    if not m:
        return False
    n, unit = m.groups()
    if unit == "시":
        return re.search(rf"(?<!\d)(0?{n}|{int(n) + 12}):00", flat) is not None
    if unit == "만원":
        return f"{n}0,000" in flat or f"{n}만" in flat
    return re.search(rf"(?<!\d){n}(?!\d)", flat) is not None


def report(folder: Path, main: Path, memo: Path | None) -> int:
    evs = sorted(events(main, folder), key=lambda e: e[0])
    if not evs:
        print(f"기록 없음: {main}")
        return 1
    t0 = evs[0][0]
    mins = lambda t: f"{(t - t0).total_seconds() / 60:5.0f}분"  # noqa: E731
    print(f"세션 {main.stem} · 프로젝트 {folder.name} · 하위 에이전트 기록 포함\n")
    print("단계별 할 일 (✓ 처음 한 때 · 하위=하위 에이전트가 함 · ✗ 안 함)")
    done: dict[str, dt.datetime] = {}
    missing, order = [], []
    for stage, label, spec in STEPS:
        hit = first(evs, spec, folder)
        if hit:
            when, sub, body = hit
            done.setdefault(stage, when)
            want = SCRIPT.findall(spec.replace("\\.", "."))
            kind, pat = spec.split(":", 1)
            times = sum(1 for _, _, k, b in evs if k == kind and re.search(pat.split("|file:")[0], b.replace("\\", "/")))
            shown = want[0] if want and kind == "run" else (body if kind == "write" and len(body) < 60 else "셸로 씀")
            print(f"  ✓ {mins(when)} {stage:<8} {label}{' (하위)' if sub else ''}  {shown}{f' ×{times}' if times > 1 else ''}")
        else:
            missing.append(f"{stage} {label}")
            print(f"  ✗        {stage:<8} {label}")
    spec_of = {label: spec for _, label, spec in STEPS}
    gates = [(label, first(evs, spec_of[label], folder)) for label in GATES]
    gates = [(label, hit[0]) for label, hit in gates if hit]
    for (a, ta), (b, tb) in zip(gates, gates[1:]):
        if tb < ta:
            order.append(f"「{b}」이(가) 「{a}」보다 먼저")
    page_at = next((w for w, _, k, b in evs if k == "write" and b == "mockups/index.html"), None)
    for label, spec in AFTER_PAGE:
        rx = re.compile(spec)
        if page_at and not any(k == "run" and w >= page_at and rx.search(b) for w, _, k, b in evs):
            order.append(f"시안을 만든 뒤 「{label}」을(를) 안 돌림")
    last_page = max((w for w, _, k, b in evs if k == "write" and b.startswith("mockups/")), default=None)
    last_check = max((w for w, _, k, b in evs if k == "run" and "preflight.py" in b), default=None)
    print("\n하면 안 되는 일")
    bad = 0
    for label, pat, kind in DONT:
        hits = [(w, b) for w, _, k, b in evs if k == kind and re.search(pat, b.replace("\\", "/"))]
        bad += bool(hits)
        print(f"  {'✗ ' + str(len(hits)) + '번' if hits else '✓ 없음'}  {label}" + (f" — {hits[0][1][:80]}" if hits else ""))
    if last_page and (not last_check or last_check < last_page):
        bad += 1
        print("  ✗ 마지막 시안 고침 뒤 preflight.py 를 다시 안 돌림")
    else:
        print("  ✓ 마지막 시안 고침 뒤 preflight.py 돌림" if last_page else "  - 시안 없음")
    for o_ in order:
        print(f"  ✗ 순서: {o_}")
    errors = [b for _, _, k, b in evs if k == "error"]
    blocks = [b for b in errors if "hook" in b.lower() or "훅" in b or "guard" in b.lower()]
    print("\n수치")
    print(f"  의뢰인에게 질문 상자 {sum(k == 'ask' for _, _, k, _ in evs)}개 · 의뢰인 답 {sum(k == 'client' for _, _, k, _ in evs)}개")
    board_at = first(evs, spec_of["공용 틀 보기 화면"], folder)
    if board_at:  # 맥락 질문을 건너뛰고 후보부터 내밀었는지(guided-conversation.md: 손님·목적·싫은 것·사진을 먼저)
        print(f"  보기 화면 전에 받은 의뢰인 답 {sum(k == 'client' and w < board_at[0] for w, _, k, _ in evs) - 1}개(첫 요청 뺌)")
    print(f"  하위 에이전트 {sum(k == 'agent' for _, _, k, _ in evs)}번 · 그림 읽기 {sum(k == 'read' and re.search(r'\.(png|jpe?g|webp)$', b, re.I) is not None for _, _, k, b in evs)}번")
    print(f"  도구 오류 {len(errors)}번(그중 훅이 막음 {len(blocks)}번) · 걸린 시간 {mins(evs[-1][0]).strip()}")
    for b in blocks[:3]:
        print(f"    막힘: {' '.join(b.split())[:120]}")
    if memo:
        page = (folder / "mockups" / "index.html")
        text = page.read_text(encoding="utf-8", errors="replace") if page.is_file() else ""
        flat = re.sub(r"\s+", "", re.sub(r"<[^>]+>", " ", text))
        vals = memo_values(memo.read_text(encoding="utf-8"))
        lost = [v for v in vals if not in_page(v, flat)]
        bad += bool(lost)  # 의뢰인이 준 사실이 시안에 없으면 어긴 일 — 이름·가격을 묻지 않고 빈칸 말을 넣었다(애견미용 21차)
        print(f"\n의뢰인 메모 값이 시안에 있나: {len(vals) - len(lost)}/{len(vals)}" + (f" — 없음: {', '.join(lost)}" if lost else ""))
    spec = folder / "formats" / "board-spec.json"
    if spec.is_file():  # 바탕 후보가 이름난 사이트였나(애견미용 18차: 일본 동네 미용실이 바탕이 됨)
        sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "skills" / "ui-design-director" / "scripts"))
        import make_live_board
        try:
            issues = make_live_board.candidate_issues(json.loads(spec.read_text(encoding="utf-8")))
        except ValueError:
            issues = ["board-spec.json 을 읽을 수 없음"]
        bad += bool(issues)
        print(f"\n바탕 후보 점검 {len(issues)}개" + "".join(f"\n  {line[:150]}" for line in issues))
    if last_page:  # 넘길 때 남은 걸림 — 디자이너가 걸린 채로 넘겼는지(애견미용 18차: 미달 뒤 비교 사이트를 바꿈)
        pre = Path(__file__).resolve().parent.parent / "skills" / "ui-design-director" / "scripts" / "preflight.py"
        r = subprocess.run([sys.executable, "-X", "utf8", str(pre), str(folder)], capture_output=True, text=True, encoding="utf-8", errors="replace")
        left = [line for line in r.stdout.splitlines() if line.startswith("- ")]
        bad += bool(left)
        print(f"\n지금 preflight 에 남은 걸림 {len(left)}개" + "".join(f"\n  {line[:150]}" for line in left[:5]))
    print(f"\n빠진 일 {len(missing)} · 어긴 일 {bad}")
    return 1 if missing or bad else 0


def main(argv: list[str]) -> int:
    utf8()
    args = [a for a in argv if not a.startswith("--")]
    if not args:
        print(__doc__.strip(), file=sys.stderr)
        return 2
    # Git Bash 꼴(/c/Users/…)을 윈도 경로로 — 그대로 두면 C:/c/Users 가 되어 기록의 C:\Users\… 쓰기를 하나도 못 맞췄다(애견미용 18차)
    folder = Path(re.sub(r"^/([a-zA-Z])/", r"\1:/", args[0]))
    opt = lambda k: argv[argv.index(k) + 1] if k in argv and argv.index(k) + 1 < len(argv) else None  # noqa: E731
    sid, memo = opt("--session"), opt("--memo")
    memo = re.sub(r"^/([a-zA-Z])/", r"\1:/", memo) if memo else None
    main_file = next(PROJECTS.glob(f"*/{sid}.jsonl"), None) if sid else find_session(folder)
    if not main_file:
        print(f"이 폴더의 대화 기록을 못 찾음: {folder.name} — --session <ID> 로 주세요", file=sys.stderr)
        return 2
    return report(folder, main_file, Path(memo) if memo else None)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
