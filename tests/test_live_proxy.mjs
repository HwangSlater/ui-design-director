// live_proxy.mjs 시험 — 내 컴퓨터에 「띄우기를 막는 가짜 사이트」를 열고 프록시를 거쳐 본다(바깥 접속 없음).
// 실행: node --test tests/test_live_proxy.mjs
import { test, before, after } from "node:test";
import assert from "node:assert/strict";
import { createServer } from "node:http";
import { spawn } from "node:child_process";
import { mkdtempSync, writeFileSync, readFileSync, existsSync } from "node:fs";
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
let site, proc, base, origin, open, dir, out = "", lastHeaders = {}, hits = {};

before(async () => {
  site = createServer((req, res) => {
    lastHeaders = req.headers;
    hits[req.url] = (hits[req.url] || 0) + 1;
    if (req.url === "/gone") { res.writeHead(403, { "content-type": "text/html" }); res.end("<p>forbidden</p>"); return; }
    if (req.url === "/hop") { res.writeHead(302, { location: "/lazy" }); res.end(); return; }
    if (req.url === "/away") { res.writeHead(302, { location: `http://localhost:${site.address().port}/` }); res.end(); return; }
    if (req.url === "/loop") { res.writeHead(301, { location: "/loop" }); res.end(); return; }
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
  dir = mkdtempSync(join(tmpdir(), "live-proxy-"));
  writeFileSync(join(dir, "board.html"), '<script type="application/json" id="board-data">{}</script><script src="board.js"></script>'); // 공용 틀 표시가 있어야 연다
  writeFileSync(join(dir, "spec.json"), JSON.stringify({ candidates: [{ n: "1", name: "가짜", pages: { 홈: `${origin}/` } }] }));
  proc = spawn(process.execPath, [PROXY, join(dir, "board.html"), join(dir, "spec.json")]);
  const line = await new Promise((r) => proc.stdout.on("data", (d) => { out += d; const m = String(d).match(/OPEN (\S+)/); if (m) r(m[1]); }));
  open = new URL(line);
  base = open.searchParams.get("proxy");
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
  const p = spawn(process.execPath, [PROXY, join(dir, "own.html"), join(dir, "spec.json"), "--no-thumbs"]);
  const code = await new Promise((r) => p.on("exit", r));
  assert.equal(code, 3);
});

test("주소 하나로 확정까지: 같은 주소의 /choice 가 decision.json 을 쓰고 DECISION 을 찍는다", async () => {
  const m = new URLSearchParams(open.hash.slice(1)).get("wait").match(/^(\d+)-([0-9a-f]{32})$/);
  assert.ok(m, "OPEN 주소에 wait=<포트>-<열쇠> 가 없음");
  assert.equal(m[1], open.port, "확정 받는 곳이 보기 화면과 다른 포트");
  const post = (body) => fetch(`${open.origin}/choice`, { method: "POST", headers: { "content-type": "text/plain" }, body: JSON.stringify(body) });
  assert.equal((await post({ token: "0".repeat(32), label: "1 가짜" })).status, 403);
  assert.equal((await post({ token: m[2], label: "x".repeat(9000) })).status, 413);
  assert.equal((await post({ token: m[2], step: "바탕", label: "1 가짜", choice: { candidate: "1" } })).status, 200);
  const d = JSON.parse(readFileSync(join(dir, "decision.json"), "utf8"));
  assert.equal(d.label, "1 가짜");
  assert.equal(d.token, undefined, "열쇠가 기록에 남음");
  await new Promise((r) => setTimeout(r, 100));
  assert.match(out, /DECISION 1 가짜/);
  assert.equal((await fetch(open.href)).status, 200, "확정 뒤에도 계속 띄워야 함");
});

test("넘겨주기: 같은 사이트는 따라가고, 후보가 아닌 곳·끝없는 넘기기는 막는다", async () => {
  const hop = await via(`${origin}/hop`);
  assert.equal(hop.status, 200);
  assert.ok((await hop.text()).includes(`<base href="${origin}/lazy">`), "넘겨받은 마지막 주소가 base 가 아님");
  assert.equal((await via(`${origin}/away`)).status, 403);
  assert.equal((await via(`${origin}/loop`)).status, 403);
});

test("잘못된 퍼센트 인코딩은 400, 서버는 계속 돈다", async () => {
  assert.equal((await fetch(`${open.origin}/%E0%A4%A`)).status, 400);
  assert.equal((await fetch(`${base}%E0%A4%A`)).status, 400);
  assert.equal(proc.exitCode, null, "프록시가 꺼짐");
  assert.equal((await via(`${origin}/`)).status, 200);
});

test("--decision 으로 확정 파일 자리를 바꾼다", async () => {
  const d2 = mkdtempSync(join(tmpdir(), "live-proxy-dec-"));
  writeFileSync(join(d2, "board.html"), '<script type="application/json" id="board-data">{}</script><script src="board.js"></script>');
  writeFileSync(join(d2, "spec.json"), JSON.stringify({ candidates: [{ n: "1", name: "가짜", pages: { 홈: `${origin}/` } }] }));
  const target = join(d2, "고름.json");
  const p = spawn(process.execPath, [PROXY, join(d2, "board.html"), join(d2, "spec.json"), "--decision", target, "--no-thumbs"]);
  try {
    const u = new URL(await new Promise((r) => p.stdout.on("data", (d) => { const m = String(d).match(/OPEN (\S+)/); if (m) r(m[1]); })));
    const token = new URLSearchParams(u.hash.slice(1)).get("wait").split("-")[1];
    const r = await fetch(`${u.origin}/choice`, { method: "POST", body: JSON.stringify({ token, label: "1 가짜" }) });
    assert.equal(r.status, 200);
    assert.ok(existsSync(target) && !existsSync(join(d2, "decision.json")));
  } finally { p.kill(); }
});

test("같은 페이지는 한 번만 받는다: 묻기(probe) 뒤 화면 요청은 기억해 둔 것을 쓴다", async () => {
  const url = `${origin}/app?once=1`;
  const before = hits["/app?once=1"] || 0;
  await (await via(url, "?ua=pc&probe=1")).json();
  const page = await via(url, "?ua=pc&js=1");
  assert.equal(page.status, 200);
  assert.equal((hits["/app?once=1"] || 0) - before, 1);
});

test("띄우기 전에 후보 첫 페이지를 확인해 고장 난 후보를 알린다(그래도 OPEN 은 찍는다)", async () => {
  const d3 = mkdtempSync(join(tmpdir(), "live-proxy-chk-"));
  writeFileSync(join(d3, "board.html"), '<script type="application/json" id="board-data">{}</script><script src="board.js"></script>');
  writeFileSync(join(d3, "spec.json"), JSON.stringify({ candidates: [
    { n: "1", name: "멀쩡", pages: { 홈: `${origin}/` } }, { n: "2", name: "막힘", pages: { 홈: `${origin}/gone` } }] }));
  const p = spawn(process.execPath, [PROXY, join(d3, "board.html"), join(d3, "spec.json"), "--no-thumbs"]);
  let text = "";
  try {
    await new Promise((r) => p.stdout.on("data", (d) => { text += d; if (/OPEN /.test(text)) r(); }));
    assert.match(text, /후보 2 막힘: 403 — 바꾸거나 빼고 다시 띄우세요/);
    assert.ok(!/후보 1 멀쩡:/.test(text), "멀쩡한 후보가 찍힘");
    assert.ok(text.indexOf("403") < text.indexOf("OPEN "), "경고가 OPEN 보다 늦게 나옴");
  } finally { p.kill(); }
});

// 이 시험은 브라우저(Edge·Chrome)로 가짜 사이트 첫 화면을 찍는다 — 맨 처음 띄운 프록시가 OPEN 뒤에 뒤에서 찍은 것
test("OPEN 뒤에 후보 첫 화면 썸네일을 thumbs/<id>.jpg 로 찍고 한 줄 알린다, 보드 서버가 내준다", async () => {
  const deadline = Date.now() + 90000;
  while (!/썸네일 \d+장 저장/.test(out) && Date.now() < deadline) await new Promise((r) => setTimeout(r, 300));
  assert.match(out, /썸네일 1장 저장/);
  const jpg = readFileSync(join(dir, "thumbs", "1.jpg"));
  assert.equal(jpg[0], 0xff); assert.equal(jpg[1], 0xd8); // JPEG
  assert.ok(jpg.length < 60000, `썸네일이 너무 큼: ${jpg.length}`);
  const r = await fetch(`${open.origin}/thumbs/1.jpg`);
  assert.equal(r.status, 200);
  assert.equal(r.headers.get("content-type"), "image/jpeg");
});
