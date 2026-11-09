// wait_choice.mjs 시험 — 팔레트 화면처럼 따로 돌릴 때 확정 한 번을 받고 끝나는지(바깥 접속 없음).
// 실행: node --test tests/test_wait_choice.mjs
import { test } from "node:test";
import assert from "node:assert/strict";
import { spawn } from "node:child_process";
import { mkdtempSync, writeFileSync, readFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";

const WAIT = join(dirname(fileURLToPath(import.meta.url)), "..", "skills", "ui-design-director", "scripts", "wait_choice.mjs");

test("확정 하나를 받아 쓰고 CHOSEN 을 찍은 뒤 끝난다(종료 코드 0)", async () => {
  const dir = mkdtempSync(join(tmpdir(), "wait-choice-"));
  writeFileSync(join(dir, "index.html"), "<p>팔레트</p>");
  const out = join(dir, "decision.json");
  const p = spawn(process.execPath, [WAIT, join(dir, "index.html"), out, "--minutes", "1"]);
  let log = "";
  const open = new URL(await new Promise((r) => p.stdout.on("data", (d) => { log += d; const m = String(d).match(/OPEN (\S+)/); if (m) r(m[1]); })));
  const [, token] = new URLSearchParams(open.hash.slice(1)).get("wait").split("-");
  assert.equal((await fetch(open.href)).status, 200);
  const exited = new Promise((r) => p.on("exit", r));
  const r = await fetch(`${open.origin}/choice`, { method: "POST", body: JSON.stringify({ token, label: "B 숲" }) });
  assert.equal(r.status, 200);
  assert.equal(await exited, 0);
  assert.equal(JSON.parse(readFileSync(out, "utf8")).label, "B 숲");
  assert.match(log, /CHOSEN B 숲/);
});
