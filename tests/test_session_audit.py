"""session_audit.py 시험 — 대화 기록에서 단계별 도구 사용·순서·하면 안 되는 일·메모 값을 맞게 읽는지."""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import session_audit as sa  # noqa: E402


def transcript(path: Path, folder: Path, calls: list[tuple[str, dict]]) -> Path:
    """분마다 도구 호출 하나씩인 가짜 대화 기록."""
    lines = [{"type": "user", "timestamp": "2026-11-10T10:00:00Z", "message": {"content": f"/ui-design-director {folder}"}}]
    for i, (name, inp) in enumerate(calls, 1):
        lines.append({"type": "assistant", "timestamp": f"2026-11-10T10:{i:02d}:00Z",
                      "message": {"content": [{"type": "tool_use", "name": name, "input": inp}]}})
    path.write_text("\n".join(json.dumps(x, ensure_ascii=False) for x in lines), encoding="utf-8")
    return path


def test_steps_order_and_donts(tmp_path: Path, capsys) -> None:
    folder = tmp_path / "치과"
    (folder / "mockups").mkdir(parents=True)
    (folder / "mockups" / "index.html").write_text("<p>바른이치과 평일 09:00–18:00 주차 1시간</p>", encoding="utf-8")
    f = folder.as_posix()
    calls = [
        ("Bash", {"command": f"cat > '{f}/concept-brief.md' <<'EOF'\n사이트 꼴: 여러 쪽\nEOF"}),
        ("Bash", {"command": "node live_proxy.mjs formats/board-spec.json"}),
        ("Bash", {"command": 'python stage.py . --decide base "1 세종"'}),
        ("Write", {"file_path": f"{f}/mockups/index.html"}),  # DESIGN.md 없이 시안
        ("Write", {"file_path": f"{f}/DESIGN.md"}),
        ("Bash", {"command": "rm -rf formats/snapshot formats/base-cap"}),
    ]
    main = transcript(tmp_path / "s.jsonl", folder, calls)
    memo = tmp_path / "memo.md"
    memo.write_text("- 이름: 「바른이치과」\n- 시간: 평일 9시~6시\n- 싫은 것: 「최고」\n- 주차 1시간 무료, 6마리", encoding="utf-8")
    assert sa.report(folder, main, memo) == 1
    out = capsys.readouterr().out
    assert "✓     1분 brief" in out  # 셸 heredoc 으로 쓴 맥락 정리도 셈
    assert "✗        material 바탕 통째 저장" in out
    assert "「메인 시안」이(가) 「DESIGN.md」보다 먼저" in out
    assert "✗ 1번  남의 사이트 사본을 손으로 지움" in out
    assert "✗ 마지막 시안 고침 뒤 preflight.py 를 다시 안 돌림" in out
    assert "메모 값이 시안에 있나: 3/4 — 없음: 6마리" in out  # 9시·6시는 09:00·18:00 으로, 「최고」는 싫은 것이라 빼고


def test_checklist_line_is_not_a_write() -> None:
    """체크리스트에 파일 이름만 적은 셸 명령은 그 파일을 쓴 것이 아니다(치과 17차)."""
    assert not sa.shell_wrote("cat >> checklist.md <<'EOF'\n- [ ] 맥락 정리(concept-brief.md)\nEOF", "^concept-brief\\.md$")
    assert sa.shell_wrote("cat > 'C:/x/concept-brief.md' <<'EOF'", "^concept-brief\\.md$")
