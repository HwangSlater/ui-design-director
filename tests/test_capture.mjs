// capture.mjs 의 다시 찍기 판단 시험 — 고친 시안을 옛 그림으로 비교하지 않게(브라우저 없음)
// 실행: node --test tests/test_capture.mjs
import { test } from "node:test";
import assert from "node:assert/strict";
import { mkdtempSync, mkdirSync, rmSync, utimesSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join, dirname } from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";

const MOD = join(dirname(fileURLToPath(import.meta.url)), "..", "skills", "ui-design-director", "scripts", "capture.mjs");
const { recaptureReason } = await import(pathToFileURL(MOD).href);

function project() {
  const dir = mkdtempSync(join(tmpdir(), "capture-test-"));
  const html = join(dir, "ours.html");
  writeFileSync(html, "<p>시안</p>");
  mkdirSync(join(dir, "cap"));
  const shot = join(dir, "cap", "ours-1280.jpg");
  writeFileSync(shot, "jpg");
  const old = new Date(Date.now() - 60_000), now = new Date();
  utimesSync(html, old, old);
  utimesSync(shot, now, now);
  return { dir, html, shot, url: pathToFileURL(html).href, outDir: join(dir, "cap") };
}

test("그림이 없으면 찍는다", () => {
  const p = project();
  try { assert.equal(recaptureReason(join(p.outDir, "none.jpg"), p.url, { outDir: p.outDir }), "없음"); } finally { rmSync(p.dir, { recursive: true }); }
});

test("시안이 그림보다 오래되면 건너뛴다", () => {
  const p = project();
  try { assert.equal(recaptureReason(p.shot, p.url, { outDir: p.outDir }), null); } finally { rmSync(p.dir, { recursive: true }); }
});

test("시안 html 을 고치면 다시 찍는다", () => {
  const p = project();
  try {
    const later = new Date(Date.now() + 60_000);
    utimesSync(p.html, later, later);
    assert.ok(recaptureReason(p.shot, p.url, { outDir: p.outDir }));
  } finally { rmSync(p.dir, { recursive: true }); }
});

test("같은 폴더의 css 를 고쳐도 다시 찍는다", () => {
  const p = project();
  try {
    mkdirSync(join(p.dir, "css"));
    const css = join(p.dir, "css", "site.css");
    writeFileSync(css, "p{}");
    const later = new Date(Date.now() + 60_000);
    utimesSync(css, later, later);
    assert.ok(recaptureReason(p.shot, p.url, { outDir: p.outDir }));
  } finally { rmSync(p.dir, { recursive: true }); }
});

test("캡처 폴더 안의 새 그림은 고친 것으로 치지 않는다", () => {
  const p = project();
  try {
    const later = new Date(Date.now() + 60_000);
    writeFileSync(join(p.outDir, "ours-390.jpg"), "jpg");
    utimesSync(join(p.outDir, "ours-390.jpg"), later, later);
    assert.equal(recaptureReason(p.shot, p.url, { outDir: p.outDir }), null);
  } finally { rmSync(p.dir, { recursive: true }); }
});

test("원격 주소는 그림이 있으면 건너뛰고, --force 면 늘 찍는다", () => {
  const p = project();
  try {
    assert.equal(recaptureReason(p.shot, "https://example.com/", { outDir: p.outDir }), null); // lint:allow url 시험용 가짜 주소
    assert.equal(recaptureReason(p.shot, "https://example.com/", { outDir: p.outDir, force: true }), "--force"); // lint:allow url 시험용 가짜 주소
  } finally { rmSync(p.dir, { recursive: true }); }
});
