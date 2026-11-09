#!/usr/bin/env node
// 훅 명령에서 파이썬 스크립트를 돌린다 — python3 만 있는 곳(맥·리눅스)과 python 만 있는 곳(윈도) 둘 다.
// 사용(hooks.json): node "${CLAUDE_PLUGIN_ROOT}/hooks/python.mjs" "${CLAUDE_PLUGIN_ROOT}/hooks/guard.py"
// 셸의 「python3 … || python …」은 쓰지 않는다: 막을 때의 종료 코드 2도 실패로 보고 python 으로 한 번 더 돌린다.
// 표준 입력을 그대로 넘기고, 표준 출력·오류와 종료 코드도 그대로 돌려준다(2 = 막음, 이유는 표준 오류로 Claude 에게).
// 윈도의 python3 은 「스토어에서 받으세요」 가짜 실행 파일일 수 있어, 먼저 --version 으로 진짜인지 본다.
// 파이썬을 못 찾으면 막지 않고 0(훅이 고장 나도 작업은 이어진다 — guard.py 와 같은 원칙).
import { spawnSync } from "node:child_process";
import { readFileSync } from "node:fs";

const PROBE_MS = 5000;
const CANDIDATES = process.platform === "win32" ? [["python"], ["py", "-3"], ["python3"]] : [["python3"], ["python"]];

const [script, ...rest] = process.argv.slice(2);
if (!script) { console.error("사용: node python.mjs <script.py> [인자…]"); process.exit(0); }
let input = Buffer.alloc(0);
try { input = readFileSync(0); } catch { /* 표준 입력이 없음 */ }

const works = ([cmd, ...pre]) => spawnSync(cmd, [...pre, "--version"], { stdio: "ignore", timeout: PROBE_MS }).status === 0;
const found = CANDIDATES.find(works);
if (!found) { console.error("파이썬을 찾지 못해 검사를 건너뜁니다(python3·python)"); process.exit(0); }
const [cmd, ...pre] = found;
const r = spawnSync(cmd, [...pre, script, ...rest], { input, stdio: ["pipe", "inherit", "inherit"] });
process.exit(r.status ?? 0);
