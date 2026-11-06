#!/usr/bin/env node
// 참고 사이트를 「그려진 그대로」 저장한다 — 틀 안 띄우기를 막아 보기 화면에 못 띄우는 후보를 선명하게, 끝까지 보여 주려고.
// 브라우저가 원래 주소에서 끝까지 그린 페이지를 MHTML 로 받아, 사진·글꼴·스타일을 파일로 풀고 HTML 하나로 묶는다.
// 사용: node snapshot.mjs <jobs.json> <out-dir> [--widths 1280,390]
//   jobs.json: capture.mjs 와 같은 꼴 [{ "id": "1-title-home", "url": "https://…" }, …]
// 결과: <out-dir>/<id>-<width>/index.html (+ res/ 에 사진·글꼴). 이미 있으면 건너뛴다(끊겨도 이어서).
// 안전: 남의 HTML 을 내 컴퓨터에서 여니 스크립트·on…= 속성·javascript: 주소·자동 이동·페이지 속 페이지를 모두 지운다.
//   보기 화면은 스크립트를 막은 틀(sandbox)로 연다. 남의 사진·글꼴 사본이므로 고르는 동안만 쓰고 지운다 — 저장소에 넣지 않는다.
// 한계: 움직임(넘기는 사진·메뉴·마우스 올림)은 멈춘 채다 — 그건 실제 사이트로 본다. 로그인·확인 화면은 걸러 실패로 알린다.
import { createHash } from "node:crypto";
import { existsSync, mkdirSync, readFileSync, writeFileSync, rmSync } from "node:fs";
import { join, resolve } from "node:path";
import { pathToFileURL } from "node:url";
import { Cdp, launch, sleep, HIDE_OVERLAYS } from "./browser.mjs";

const PHONE_MAX = 600, PHONE_H = 844, DESKTOP_H = 900;
const PHONE_UA = "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1";
const DESKTOP_UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36 Edg/142.0.0.0";
const NAV_TIMEOUT_MS = 45000, SETTLE_MS = 2500, SCROLL_STEP_MS = 300, MAX_SCROLL = 16000;
// 사이트 대신 확인·차단 화면이 왔는지 — 그대로 저장하면 그 화면이 후보처럼 보인다
const CHALLENGE = /access denied|just a moment|verify you are human|are you a robot|captcha|request (was )?blocked|보안 확인|접근이 (거부|차단)|자동 ?입력 ?방지/i;
// 저장 직전에 애니메이션을 끝 상태로 보내고 그 값을 요소에 적는다 — 저장본에서는 애니메이션 정의가 비어
// 「투명하게 시작해 나타나는」 사진·글자가 투명한 채 남았다(스포티파이 앨범 사진, 나이키 큰 사진 위 글자)
const FREEZE_ANIMATIONS = `(() => {
  for (const a of document.getAnimations()) {
    try { a.finish(); } catch { /* 끝이 없는 반복 애니메이션 */ }
    const el = a.effect && a.effect.target;
    if (!el || !el.style) continue;
    const cs = getComputedStyle(el);
    for (const p of ["opacity", "transform", "visibility", "filter", "clip-path", "translate", "scale", "rotate"]) el.style.setProperty(p, cs.getPropertyValue(p), "important");
    el.style.setProperty("animation", "none", "important");
    el.style.setProperty("transition", "none", "important");
  }
})()`;
const EXT = { "image/jpeg": "jpg", "image/png": "png", "image/webp": "webp", "image/gif": "gif", "image/svg+xml": "svg", "image/avif": "avif", "font/woff2": "woff2", "font/woff": "woff", "font/ttf": "ttf", "font/otf": "otf", "application/font-woff": "woff", "application/font-woff2": "woff2", "text/css": "css" };

function parseArgs(argv) {
  const a = { widths: [1280, 390], rest: [] };
  for (let i = 0; i < argv.length; i++) argv[i] === "--widths" ? (a.widths = argv[++i].split(",").map(Number)) : a.rest.push(argv[i]);
  if (a.rest.length !== 2) { console.error("사용: node snapshot.mjs <jobs.json> <out-dir> [--widths 1280,390]"); process.exit(2); }
  return a;
}

// MHTML 부품 나누기
function parseMhtml(text) {
  const boundary = text.match(/boundary="?([^";\r\n]+)"?/i)[1];
  return text.split("--" + boundary).slice(1, -1).map((raw) => {
    const cut = raw.indexOf("\r\n\r\n"), head = raw.slice(0, cut), body = raw.slice(cut + 4);
    const h = (k) => (head.match(new RegExp(`^${k}:\\s*(.+)$`, "im")) || [])[1]?.trim();
    const enc = (h("Content-Transfer-Encoding") || "").toLowerCase();
    const buf = enc === "base64" ? Buffer.from(body.replace(/\s+/g, ""), "base64")
      : enc === "quoted-printable" ? Buffer.from(body.replace(/=\r?\n/g, "").replace(/=([0-9A-F]{2})/gi, (m, x) => String.fromCharCode(parseInt(x, 16))), "latin1")
      : Buffer.from(body, "latin1");
    return { type: (h("Content-Type") || "").split(";")[0].toLowerCase(), loc: h("Content-Location") || h("Content-ID"), buf };
  });
}

// 남의 HTML 에서 실행될 수 있는 것을 모두 지운다
export function sanitize(html) {
  return html
    .replace(/<(script|noscript|iframe|frame|frameset|object|embed|applet|portal)\b[\s\S]*?<\/\1\s*>/gi, "")
    .replace(/<(script|iframe|frame|object|embed|applet|portal|base)\b[^>]*\/?>/gi, "")
    .replace(/<meta\b[^>]*http-equiv=["']?refresh[^>]*>/gi, "")
    .replace(/\son[a-z]+\s*=\s*("[^"]*"|'[^']*'|[^\s>]+)/gi, "")
    .replace(/(href|src|action|formaction|xlink:href)\s*=\s*(["'])\s*(javascript|vbscript|data:text\/html)[^"']*\2/gi, '$1="#"');
}

// 부품을 res/ 에 파일로(같은 내용은 한 번만) 풀고 HTML·CSS 안 주소를 그 파일로 바꾼다
function unpack(parts, dir, pageUrl) {
  const res = join(dir, "res"); mkdirSync(res, { recursive: true });
  const byLoc = new Map(parts.map((p) => [p.loc, p]));
  const saved = new Map();
  const file = (p) => {
    if (saved.has(p)) return saved.get(p);
    const name = createHash("sha1").update(p.buf).digest("hex").slice(0, 16) + "." + (EXT[p.type] || "bin");
    if (!existsSync(join(res, name))) writeFileSync(join(res, name), p.buf);
    saved.set(p, "res/" + name); return "res/" + name;
  };
  const look = (u) => { const k = u.replace(/&amp;/g, "&"); return byLoc.get(k) || (() => { try { return byLoc.get(new URL(k, pageUrl).href); } catch { return null; } })(); };
  const fixCss = (css, up = "") => css.replace(/url\(\s*(['"]?)([^'")]+)\1\s*\)/g, (m, q, u) => { const p = look(u); return p && !/html/.test(p.type) ? `url("${up}${file(p)}")` : m; });
  const main = parts.find((p) => p.type === "text/html");
  let html = sanitize(main.buf.toString("utf8"));
  html = html.replace(/<link\b[^>]*>/gi, (tag) => {
    if (!/rel=["']?stylesheet/i.test(tag)) return /rel=["']?(preload|prefetch|modulepreload|preconnect|dns-prefetch)/i.test(tag) ? "" : tag;
    const p = look((tag.match(/href=["']([^"']+)["']/i) || [])[1] || "");
    return p ? `<style>${fixCss(p.buf.toString("utf8"))}</style>` : tag;
  });
  html = html.replace(/<style\b([^>]*)>([\s\S]*?)<\/style>/gi, (m, a, css) => `<style${a}>${fixCss(css)}</style>`);
  html = html.replace(/\s(src|poster)=(["'])([^"']+)\2/gi, (m, a, q, u) => { const p = look(u); return p && !/html/.test(p.type) ? ` ${a}="${file(p)}"` : m; });
  html = html.replace(/\ssrcset=(["'])([^"']+)\1/gi, (m, q, v) => ` srcset="${v.split(",").map((s) => { const [u, d] = s.trim().split(/\s+/); const p = u && look(u); return (p ? file(p) : u) + (d ? " " + d : ""); }).join(", ")}"`);
  html = html.replace(/\sstyle=(["'])([^"']*url\([^"']*)\1/gi, (m, q, st) => ` style=${q}${fixCss(st.replace(/&quot;/g, '"')).replace(/"/g, "&quot;")}${q}`);
  // 링크는 원래 사이트로 새 창에 — 저장한 사본 안에서 길을 잃지 않게
  html = html.replace(/<a\b([^>]*?)\shref=(["'])([^"']+)\2/gi, (m, pre, q, u) => { let abs; try { abs = new URL(u.replace(/&amp;/g, "&"), pageUrl).href; } catch { return m; } return /^https?:/.test(abs) ? `<a${pre} href="${abs}" target="_blank" rel="noopener noreferrer"` : m; });
  html = html.replace(/<head\b[^>]*>/i, (h) => `${h}<meta name="robots" content="noindex"><meta name="referrer" content="no-referrer">`);
  writeFileSync(join(dir, "index.html"), html);
  return saved.size;
}

async function snap(port, url, width, dir) {
  const target = await (await fetch(`http://127.0.0.1:${port}/json/new?about:blank`, { method: "PUT" })).json();
  const cdp = await Cdp.open(target.webSocketDebuggerUrl);
  try {
    const phone = width <= PHONE_MAX;
    await cdp.send("Page.enable"); await cdp.send("Network.enable");
    await cdp.send("Emulation.setDeviceMetricsOverride", { width, height: phone ? PHONE_H : DESKTOP_H, deviceScaleFactor: 1, mobile: phone });
    await cdp.send("Emulation.setUserAgentOverride", { userAgent: phone ? PHONE_UA : DESKTOP_UA, acceptLanguage: "ko-KR,ko;q=0.9,en;q=0.8" });
    await cdp.send("Page.addScriptToEvaluateOnNewDocument", { source: "Object.defineProperty(navigator, 'webdriver', { get: () => undefined })" });
    let status = 0;
    cdp.listeners.push((m) => { if (m.method === "Network.responseReceived" && m.params.type === "Document" && !status) status = m.params.response.status; });
    const loaded = cdp.waitFor("Page.loadEventFired", NAV_TIMEOUT_MS);
    await cdp.send("Page.navigate", { url }); await loaded; await sleep(SETTLE_MS);
    if (status >= 400) throw new Error(`응답 ${status}`);
    await cdp.send("Runtime.evaluate", { expression: HIDE_OVERLAYS });
    await cdp.send("Runtime.evaluate", { awaitPromise: true, expression: `(async () => { for (let y = 0; y < Math.min(document.body.scrollHeight, ${MAX_SCROLL}); y += innerHeight) { scrollTo(0, y); await new Promise((r) => setTimeout(r, ${SCROLL_STEP_MS})); } scrollTo(0, 0); })()` });
    await sleep(SETTLE_MS);
    await cdp.send("Runtime.evaluate", { expression: HIDE_OVERLAYS }); // 내리는 동안 늦게 뜬 띠
    const text = (await cdp.send("Runtime.evaluate", { returnByValue: true, expression: "document.body.innerText.slice(0, 3000)" })).result.value || "";
    if (CHALLENGE.test(text) && text.length < 1500) throw new Error("사이트 대신 확인·차단 화면이 옴");
    await cdp.send("Runtime.evaluate", { expression: FREEZE_ANIMATIONS });
    const { data } = await cdp.send("Page.captureSnapshot", { format: "mhtml" });
    rmSync(dir, { recursive: true, force: true }); mkdirSync(dir, { recursive: true });
    return { files: unpack(parseMhtml(data), dir, url), status };
  } finally {
    cdp.close();
    await fetch(`http://127.0.0.1:${port}/json/close/${target.id}`).catch(() => {});
  }
}

async function main() {
  const { widths, rest: [jobsPath, outDir] } = parseArgs(process.argv.slice(2));
  const jobs = JSON.parse(readFileSync(jobsPath, "utf8"));
  mkdirSync(outDir, { recursive: true });
  const { proc, port, profile } = await launch();
  const failed = []; let done = 0; const total = jobs.length * widths.length;
  try {
    for (const job of jobs) for (const width of widths) {
      const dir = join(outDir, `${job.id}-${width}`); done++;
      if (existsSync(join(dir, "index.html"))) { console.log(`[${done}/${total}] 있음, 건너뜀  ${job.id}-${width}`); continue; }
      try { const r = await snap(port, job.url, width, dir); console.log(`[${done}/${total}] 저장  ${job.id}-${width}  부품 ${r.files}개`); }
      catch (e) { failed.push(`${job.id}-${width}: ${e.message}`); console.log(`[${done}/${total}] 실패  ${job.id}-${width}  ${e.message}`); }
    }
  } finally { proc.kill(); await sleep(500); try { rmSync(profile, { recursive: true, force: true }); } catch { /* 늦게 닫히면 남음 */ } }
  console.log(`끝: 성공 ${total - failed.length} / 실패 ${failed.length}`);
  if (failed.length) { failed.forEach((f) => console.log(`  - ${f}`)); process.exit(1); }
}

// 직접 실행할 때만 돈다(시험이 sanitize 만 불러 쓸 수 있게) — 이름 끝만 보면 test_snapshot.mjs 도 걸렸다
if (process.argv[1] && import.meta.url === pathToFileURL(resolve(process.argv[1])).href) main().catch((e) => { console.error(`ERROR: ${e.message}`); process.exit(1); });
