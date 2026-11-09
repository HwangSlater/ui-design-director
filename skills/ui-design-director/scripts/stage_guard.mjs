// 바탕 자료를 만드는 스크립트(snapshot·motion·capture)가 프로젝트 formats/ 에 쓰기 전에 단계를 본다.
// 훅(hooks/guard.py)은 Write·Edit 만 보고 Bash 로 돌린 스크립트 출력은 못 본다 — 바탕을 확정하기 전에 바탕 자료를 세 번 모았다.
// 판단은 stage.py --guard 하나로(프로젝트 표시·앞 단계는 파이썬 한 곳). 프로젝트 밖이면 그대로 지나간다.
// 파이썬 찾기는 hooks/python.mjs 와 같은 차례(윈도: python → py -3 → python3, 그 밖: python3 → python). PYTHON 환경 변수가 있으면 그것.
import { spawnSync } from "node:child_process";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const STAGE = join(dirname(fileURLToPath(import.meta.url)), "stage.py");
const PROBE_MS = 5000;
const CANDIDATES = process.platform === "win32" ? [["python"], ["py", "-3"], ["python3"]] : [["python3"], ["python"]];

let found;
export function findPython() {
  if (found !== undefined) return found;
  if (process.env.PYTHON) return (found = [process.env.PYTHON]);
  const works = ([cmd, ...pre]) => spawnSync(cmd, [...pre, "--version"], { stdio: "ignore", timeout: PROBE_MS }).status === 0;
  return (found = CANDIDATES.find(works) || null);
}

// 쓸 곳(out)이 프로젝트 formats/ 안이고 stage 의 앞 단계가 안 됐으면 막을 이유(글), 아니면 "".
// 파이썬을 못 찾으면 막지 않는다(hooks/python.mjs 와 같은 원칙 — 검사가 고장 나도 작업은 이어진다).
export function stageBlock(out, stage = "material") {
  const py = findPython();
  if (!py) return "";
  const [cmd, ...pre] = py;
  const r = spawnSync(cmd, [...pre, "-X", "utf8", STAGE, "--guard", stage, out], { encoding: "utf8" });
  return r.status === 1 ? (r.stderr || "").trim() || "앞 단계가 안 됨" : "";
}

// 막을 이유가 있으면 찍고 끝낸다(종료 코드 3 — 사용법 오류 1·2 와 구별).
export function requireStage(out, stage = "material") {
  const why = stageBlock(out, stage);
  if (!why) return;
  console.error(`멈춤: ${why}`);
  process.exit(3);
}
