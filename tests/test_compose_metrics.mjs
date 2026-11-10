// compose_metrics.mjs 의 비교 사이트 고정 시험 — 첫 기록과 다른 사이트로 돌리면 까닭(--why) 없이는 멈춘다(브라우저 없음)
// 실행: node --test tests/test_compose_metrics.mjs
import { test } from "node:test";
import assert from "node:assert/strict";
import { spawnSync } from "node:child_process";
import { mkdtempSync, rmSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join, dirname } from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";

const MOD = join(dirname(fileURLToPath(import.meta.url)), "..", "skills", "ui-design-director", "scripts", "compose_metrics.mjs");
const { parseArgs, siteChange, trimHistory } = await import(pathToFileURL(MOD).href);
const U = (n) => `https://example.com/${n}`; // lint:allow url 시험용 가짜 주소(접속하지 않음)

test("--why 의 값은 사이트로 읽지 않는다", () => {
  const a = parseArgs(["out.md", "--width", "390", "가=" + U("a"), "--why", "점수 페이지끼리=같은 일", "--ours", "우리"]);
  assert.equal(a.width, 390);
  assert.equal(a.why, "점수 페이지끼리=같은 일");
  assert.deepEqual(a.targets.map(([n]) => n), ["가"]);
});

test("같은 폭 첫 기록과 사이트가 다를 때만 바뀐 것으로 본다", () => {
  const hist = [{ width: 1280, sites: [{ name: "가", url: U("a") }, { name: "나", url: U("b") }] }, { width: 390, sites: [{ name: "다", url: U("c") }] }];
  assert.equal(siteChange(hist, 1280, [{ url: U("b") + "/" }, { url: U("a") }]), null);
  assert.ok(siteChange(hist, 1280, [{ url: U("a") }, { url: U("z") }]));
  assert.equal(siteChange(hist, 768, [{ url: U("z") }]), null);
  assert.equal(siteChange([], 1280, [{ url: U("z") }]), null);
});

test("기록을 줄여도 폭마다 첫 기록은 남는다", () => {
  const list = [{ width: 1280, n: 0 }, { width: 390, n: 1 }, ...Array.from({ length: 10 }, (_, i) => ({ width: 1280, n: i + 2 }))];
  const kept = trimHistory(list, 5);
  assert.equal(kept.length, 5);
  assert.deepEqual(kept.slice(0, 2).map((r) => r.n), [0, 1]);
  assert.equal(kept.at(-1).n, 11);
});

test("까닭 없이 사이트를 바꾸면 재기 전에 멈춘다", () => {
  const dir = mkdtempSync(join(tmpdir(), "compose-test-"));
  try {
    writeFileSync(join(dir, "구성-기록.json"), JSON.stringify([{ at: "t", width: 1280, sites: [{ name: "가", url: U("a") }], short: 2 }]));
    const r = spawnSync(process.execPath, [MOD, join(dir, "구성.md"), "--width", "1280", "나=" + U("b"), "우리=" + U("o"), "--ours", "우리"], { encoding: "utf8" });
    assert.equal(r.status, 1);
    assert.match(r.stderr, /미달이 나온 뒤라/);  // 미달(short 2) 뒤에는 까닭이 있어도 못 바꾼다(빵집 31차)
    assert.match(r.stderr, /가/);
    const w = spawnSync(process.execPath, [MOD, join(dir, "구성.md"), "--width", "1280", "나=" + U("b"), "우리=" + U("o"), "--ours", "우리", "--why", "까닭"], { encoding: "utf8" });
    assert.equal(w.status, 1);
  } finally { rmSync(dir, { recursive: true }); }
});

test("미달 없이 바꿀 때는 까닭을 요구한다", () => {
  const dir = mkdtempSync(join(tmpdir(), "compose-test-"));
  try {
    writeFileSync(join(dir, "구성-기록.json"), JSON.stringify([{ at: "t", width: 1280, sites: [{ name: "가", url: U("a") }], short: 0 }]));
    const r = spawnSync(process.execPath, [MOD, join(dir, "구성.md"), "--width", "1280", "나=" + U("b"), "우리=" + U("o"), "--ours", "우리"], { encoding: "utf8" });
    assert.equal(r.status, 1);
    assert.match(r.stderr, /--why/);
  } finally { rmSync(dir, { recursive: true }); }
});
