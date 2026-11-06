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
const LONG = "책방 오후는 전주 한옥마을 뒷골목의 작은 책방이에요. ".repeat(10);
const LAZY_PAGE = `<!doctype html><html><head><style>@font-face{font-family:x;src:url(/f.woff2)}</style></head><body><p>${LONG}</p>
<img data-src="/a.jpg" src="data:image/gif;base64,R0lGODlhAQABAAAAACw=" loading="lazy"><img data-srcset="/b.jpg 1x"><div data-bg="/c.jpg">배경</div>
<noscript><img src="/n.jpg"></noscript><script>1</script></body></html>`;
const APP_PAGE = `<!doctype html><html><head></head><body><div id="root"></div><script src="/app.js"></script></body></html>`;
let site, proc, base, origin, lastHeaders = {};

before(async () => {
  site = createServer((req, res) => {
    lastHeaders = req.headers;
    if (req.url === "/lazy") { res.writeHead(200, { "content-type": "text/html" }); res.end(LAZY_PAGE); return; }
    if (req.url === "/check") { res.writeHead(200, { "content-type": "text/html" }); res.end(`<html><body><h1>Checking your browser...</h1><p>${LONG}</p><script>1</script></body></html>`); return; }
    if (req.url === "/app") { res.writeHead(200, { "content-type": "text/html" }); res.end(APP_PAGE); return; }
    if (req.url === "/s2.css") { res.writeHead(200, { "content-type": "text/css" }); res.end("@font-face{src:url(/f.woff2) format('woff2')}h1{background:url(/bg.png)}"); return; }
    if (req.url === "/s.css") { res.writeHead(200, { "content-type": "text/css", "cross-origin-resource-policy": "same-origin" }); res.end("body{background:url(/bg.png)}"); return; }
    res.writeHead(200, { "content-type": "text/html", "x-frame-options": "DENY", "content-security-policy": "frame-ancestors 'none'", "set-cookie": "s=1" });
    res.end(PAGE);
  });
  await new Promise((r) => site.listen(0, "127.0.0.1", r));
  origin = `http://127.0.0.1:${site.address().port}`;
  const dir = mkdtempSync(join(tmpdir(), "live-proxy-"));
  writeFileSync(join(dir, "board.html"), '<script type="application/json" id="board-data">{}</script><script src="board.js"></script>'); // 공용 틀 표시가 있어야 연다
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

test("브라우저 같은 머리를 보낸다(머리가 빈 요청은 보안 장치가 막는다)", async () => {
  await via(`${origin}/lazy`);
  assert.match(lastHeaders["user-agent"], /iPhone/);
  assert.match(lastHeaders["accept"], /text\/html/);
  assert.equal(lastHeaders["sec-fetch-dest"], "document");
  assert.ok(lastHeaders["accept-language"].startsWith("ko-KR"));
});

test("스크립트 없이 띄울 때 늦게 불러오는 사진을 바로 보이게, noscript 를 꺼낸다", async () => {
  const body = await (await via(`${origin}/lazy`)).text();
  assert.ok(/<img src="\/a\.jpg"/.test(body) || body.includes(' src="/a.jpg"'), "data-src 가 src 로 안 바뀜");
  assert.ok(!/loading="lazy"/.test(body), "loading=lazy 가 남음");
  assert.ok(body.includes('srcset="/b.jpg 1x"'), "data-srcset 이 srcset 으로 안 바뀜");
  assert.ok(body.includes("background-image:url('/c.jpg')"), "data-bg 가 배경으로 안 바뀜");
  assert.ok(body.includes('<img src="/n.jpg">') && !body.includes("<noscript>"), "noscript 안 사진이 안 나옴");
});

test("같은 사이트 글꼴은 프록시로(스타일시트·페이지 안 style 둘 다), 그림은 원래 주소로", async () => {
  const css = await (await via(`${origin}/s2.css`)).text();
  assert.ok(css.includes(`url("${base}${encodeURIComponent(`${origin}/f.woff2`)}?ua=phone")`), "스타일시트 글꼴이 프록시로 안 감");
  assert.ok(css.includes(`url("${origin}/bg.png")`), "그림이 원래 주소가 아님");
  const page = await (await via(`${origin}/lazy`)).text();
  assert.ok(page.includes(`${base}${encodeURIComponent(`${origin}/f.woff2`)}`), "페이지 안 style 글꼴이 프록시로 안 감");
});

test("묻기(probe): 스크립트로 그리는 빈 화면만 js 가 필요하다고 답한다", async () => {
  const app = await (await via(`${origin}/app`, "?ua=pc&probe=1")).json();
  assert.equal(app.js, true);
  const lazy = await (await via(`${origin}/lazy`, "?ua=pc&probe=1")).json();
  assert.equal(lazy.js, false);
});

test("묻기(probe): 사이트 대신 「브라우저 확인 중」 화면이 오면 스크립트가 필요하다고 답한다", async () => {
  const j = await (await via(`${origin}/check`, "?ua=pc&probe=1")).json();
  assert.equal(j.js, true);
});

test("공용 틀이 아닌 보기 화면은 열지 않는다", async () => {
  const dir = mkdtempSync(join(tmpdir(), "live-proxy-own-"));
  writeFileSync(join(dir, "own.html"), "<p>직접 짠 보기 화면</p><iframe src=x></iframe>");
  writeFileSync(join(dir, "spec.json"), JSON.stringify({ candidates: [{ n: "1", name: "가짜", pages: { 홈: `${origin}/` } }] }));
  const p = spawn(process.execPath, [PROXY, join(dir, "own.html"), join(dir, "spec.json")]);
  const code = await new Promise((r) => p.on("exit", r));
  assert.equal(code, 3);
});
