// live_proxy.mjs 시험 — 내 컴퓨터에 「띄우기를 막는 가짜 사이트」를 열고 프록시를 거쳐 본다(바깥 접속 없음).
// 실행: node --test tests/test_live_proxy.mjs
import { test, before, after } from "node:test";
import assert from "node:assert/strict";
import { createServer } from "node:http";
import { spawn } from "node:child_process";
import { mkdtempSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";

const PROXY = join(dirname(fileURLToPath(import.meta.url)), "..", "skills", "ui-design-director", "scripts", "live_proxy.mjs");
const PAGE = `<!doctype html><html><head><link rel="stylesheet" href="/s.css" integrity="sha-x" crossorigin></head>
<body><script>document.body.innerHTML = "지워짐"</script><a href="/menu">메뉴</a><a href="https://other.example/">남의 곳</a></body></html>`;
let site, proc, base, origin;

before(async () => {
  site = createServer((req, res) => {
    if (req.url === "/s.css") { res.writeHead(200, { "content-type": "text/css", "cross-origin-resource-policy": "same-origin" }); res.end("body{background:url(/bg.png)}"); return; }
    res.writeHead(200, { "content-type": "text/html", "x-frame-options": "DENY", "content-security-policy": "frame-ancestors 'none'", "set-cookie": "s=1" });
    res.end(PAGE);
  });
  await new Promise((r) => site.listen(0, "127.0.0.1", r));
  origin = `http://127.0.0.1:${site.address().port}`;
  const dir = mkdtempSync(join(tmpdir(), "live-proxy-"));
  writeFileSync(join(dir, "board.html"), "<p>보드</p>");
  writeFileSync(join(dir, "spec.json"), JSON.stringify({ candidates: [{ n: "1", name: "가짜", pages: { 홈: `${origin}/` } }] }));
  proc = spawn(process.execPath, [PROXY, join(dir, "board.html"), join(dir, "spec.json")]);
  const line = await new Promise((r) => proc.stdout.on("data", (d) => { const m = String(d).match(/OPEN (\S+)/); if (m) r(m[1]); }));
  base = decodeURIComponent(line.split("proxy=")[1]);
});
after(() => { proc.kill(); site.close(); });

const via = (url, q = "?ua=phone") => fetch(base + encodeURIComponent(url) + q);

test("막는 머리와 쿠키를 지우고 사이트 스크립트를 뺀다", async () => {
  const r = await via(`${origin}/`);
  assert.equal(r.status, 200);
  for (const h of ["x-frame-options", "content-security-policy", "set-cookie"]) assert.equal(r.headers.get(h), null, h);
  const body = await r.text();
  assert.ok(body.includes(`<base href="${origin}/">`));
  assert.ok(!body.includes("지워짐"), "사이트 스크립트가 남음");
  assert.ok(!/integrity|crossorigin/.test(body), "스타일시트 무결성 속성이 남음");
  assert.ok(body.includes(base + encodeURIComponent(`${origin}/menu`)), "같은 사이트 링크가 프록시로 안 바뀜");
  assert.ok(body.includes('target="_blank"'), "남의 사이트 링크가 새 창이 아님");
});

test("스타일시트: 막는 머리를 지우고 url() 을 원래 주소로", async () => {
  const r = await via(`${origin}/s.css`);
  assert.equal(r.headers.get("cross-origin-resource-policy"), null);
  assert.ok((await r.text()).includes(`url("${origin}/bg.png")`));
});

test("후보가 아닌 곳·틀린 열쇠·쓰기는 막는다", async () => {
  assert.equal((await via("https://other.example/")).status, 403);
  assert.equal((await fetch(base.replace(/[0-9a-f]{24}\/$/, "0".repeat(24) + "/") + encodeURIComponent(`${origin}/`))).status, 403);
  assert.equal((await fetch(base + encodeURIComponent(`${origin}/`), { method: "POST" })).status, 403);
});
