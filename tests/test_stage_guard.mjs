// 바탕 자료 스크립트의 단계 확인 시험 — 스킬 프로젝트 formats/ 에는 바탕 확정 뒤에만 쓴다(훅은 Bash 출력을 못 본다).
// 실행: node --test tests/test_stage_guard.mjs  (브라우저를 띄우기 전에 멈추는지만 본다 — 바깥 접속 없음)
import { test } from "node:test";
import assert from "node:assert/strict";
import { spawnSync } from "node:child_process";
import { mkdtempSync, mkdirSync, writeFileSync, existsSync } from "node:fs";
import { tmpdir } from "node:os";
import { join, dirname } from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";

const SCRIPTS = join(dirname(fileURLToPath(import.meta.url)), "..", "skills", "ui-design-director", "scripts");
const { stageBlock } = await import(pathToFileURL(join(SCRIPTS, "stage_guard.mjs")).href);

const project = () => {
  const root = mkdtempSync(join(tmpdir(), "stage-guard-"));
  writeFileSync(join(root, "concept-brief.md"), "주 업무");
  mkdirSync(join(root, "formats"));
  writeFileSync(join(root, "formats", "보기.html"), '<script id="board-data">{}</script>');
  writeFileSync(join(root, "formats", "jobs-base.json"), "[]");
  return root;
};
const run = (script, ...args) => spawnSync(process.execPath, [join(SCRIPTS, script), ...args], { encoding: "utf8" });

test("바탕 확정 전에는 막고, 확정 뒤·프로젝트 밖은 지나간다", () => {
  const root = project();
  assert.match(stageBlock(join(root, "formats", "snapshot")), /바탕 확정/);
  assert.equal(stageBlock(join(mkdtempSync(join(tmpdir(), "no-project-")), "formats", "snapshot")), "");
  writeFileSync(join(root, "decisions.json"), JSON.stringify({ base: "1 가" }));
  assert.equal(stageBlock(join(root, "formats", "snapshot")), "");
});

test("snapshot·motion·capture(jobs-base) 는 바탕 확정 전 프로젝트 formats/ 에 쓰지 않고 3 으로 끝난다", () => {
  const root = project();
  const fm = join(root, "formats");
  for (const [script, args] of [
    ["snapshot.mjs", [join(fm, "jobs-base.json"), join(fm, "snapshot")]],
    ["motion.mjs", ["https://example.com/", join(fm, "바탕-움직임.md")]], // lint:allow url 시험용 가짜 주소(멈추므로 접속하지 않음)
    ["capture.mjs", [join(fm, "jobs-base.json"), join(fm, "base-cap")]],
  ]) {
    const r = run(script, ...args);
    assert.equal(r.status, 3, `${script}: ${r.stderr}`);
    assert.match(r.stderr, /멈춤: .*바탕 확정/);
  }
  assert.ok(!existsSync(join(fm, "snapshot")) && !existsSync(join(fm, "base-cap")));
});

test("capture 의 후보 캡처(바탕 고르기 전)는 막지 않는다", () => {
  const root = project();
  writeFileSync(join(root, "formats", "jobs.json"), "[]"); // 일이 없으니 브라우저 없이 끝난다
  const r = run("capture.mjs", join(root, "formats", "jobs.json"), join(root, "formats", "cap"));
  assert.notEqual(r.status, 3, r.stderr);
  assert.ok(!/멈춤:/.test(r.stderr));
});
