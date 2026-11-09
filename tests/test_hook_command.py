"""hooks.json 의 guard 명령을 Claude Code 처럼 셸로 돌려, 막을 때 종료 코드 2와 이유(표준 오류)가 그대로 오는지 본다."""
from __future__ import annotations

import json
import os
import shlex
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def guard_command() -> str:
    hooks = json.loads((ROOT / "hooks" / "hooks.json").read_text(encoding="utf-8"))["hooks"]
    return hooks["PreToolUse"][0]["hooks"][0]["command"]


def run_hook(payload: dict) -> subprocess.CompletedProcess:
    cmd = guard_command()
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    env = {**os.environ, "CLAUDE_PLUGIN_ROOT": ROOT.as_posix()}
    bash = shutil.which("bash")
    if bash:  # Claude Code 는 훅 명령을 셸로 돌린다
        return subprocess.run([bash, "-c", cmd], input=data, capture_output=True, env=env)
    return subprocess.run(shlex.split(cmd.replace("${CLAUDE_PLUGIN_ROOT}", ROOT.as_posix())), input=data, capture_output=True, env=env)


def test_block_passes_exit_2_and_reason(tmp_path: Path) -> None:
    (tmp_path / "concept-brief.md").write_text("주 업무", encoding="utf-8")
    r = run_hook({"tool_name": "Write", "tool_input": {"file_path": str(tmp_path / "mockups" / "index.html"), "content": "<p>시안</p>"}})
    assert r.returncode == 2
    assert "먼저" in r.stderr.decode("utf-8")


def test_allowed_write_passes_0(tmp_path: Path) -> None:
    r = run_hook({"tool_name": "Write", "tool_input": {"file_path": str(tmp_path / "note.txt"), "content": "x"}})
    assert r.returncode == 0, r.stderr.decode("utf-8", "replace")
