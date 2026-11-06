// browser.mjs 시험 — 띄운 headless 브라우저를 끝에 확실히 끄는지, 주인이 죽고 남은 브라우저를 다음 실행이 치우는지
// 실행: node --test tests/test_browser.mjs  (Edge 또는 Chrome 필요)
import { test } from "node:test";
import assert from "node:assert/strict";
import { spawn } from "node:child_process";
import { existsSync, mkdtempSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join, dirname } from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";

const MOD = join(dirname(fileURLToPath(import.meta.url)), "..", "skills", "ui-design-director", "scripts", "browser.mjs");
const { launch, sweepOrphans } = await import(pathToFileURL(MOD).href);
const alive = (pid) => { try { process.kill(pid, 0); return true; } catch (e) { return e.code === "EPERM"; } };
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

test("close() 뒤에는 브라우저 본체와 프로필이 남지 않는다", async () => {
  const { port, profile, close } = await launch("capture-");
  const owner = JSON.parse((await import("node:fs")).readFileSync(join(profile, "owner.json"), "utf8"));
  assert.ok(owner.browser > 0, "본체 번호를 받아야 한다");
  await close();
  await sleep(500);
  assert.equal(alive(owner.browser), false, "본체가 살아 있음");
  assert.equal(existsSync(profile), false, "프로필 폴더가 남음");
  await assert.rejects(fetch(`http://127.0.0.1:${port}/json/version`));
});

test("주인 node 가 없는 프로필은 다음 실행이 치운다", async () => {
  const dir = mkdtempSync(join(tmpdir(), "capture-"));
  const dead = spawn(process.execPath, ["-e", "0"]); // 바로 끝나는 프로세스 번호 = 죽은 주인
  await new Promise((r) => dead.on("exit", r));
  writeFileSync(join(dir, "owner.json"), JSON.stringify({ owner: dead.pid, browser: 0 }));
  sweepOrphans();
  assert.equal(existsSync(dir), false);
});

test("도구가 강제로 죽어 남은 브라우저를 --sweep 이 끈다(훅이 부르는 명령)", async () => {
  const child = spawn(process.execPath, ["--input-type=module", "-e",
    `const m = await import(${JSON.stringify(pathToFileURL(MOD).href)}); const b = await m.launch("capture-");
     const o = JSON.parse((await import("node:fs")).readFileSync(b.profile + "/owner.json", "utf8"));
     console.log(JSON.stringify({ browser: o.browser, profile: b.profile })); setInterval(() => {}, 1000);`]);
  const line = await new Promise((r) => child.stdout.once("data", (d) => r(String(d))));
  const { browser, profile } = JSON.parse(line);
  // 시간 초과로 죽는 것처럼 끄는 코드가 돌 틈 없이 죽인다
  if (process.platform === "win32") spawn("taskkill", ["/PID", String(child.pid), "/F"]); else child.kill("SIGKILL");
  await new Promise((r) => child.on("exit", r));
  assert.equal(alive(browser), true, "주인이 죽어도 브라우저는 남는다(고치기 전 증상)");
  const out = await new Promise((r) => { const s = spawn(process.execPath, [MOD, "--sweep"]); let t = ""; s.stdout.on("data", (d) => (t += d)); s.on("exit", () => r(t)); });
  await sleep(500);
  assert.match(out, /systemMessage/);
  assert.equal(alive(browser), false, "--sweep 뒤에도 브라우저가 살아 있음");
  assert.equal(existsSync(profile), false);
});
