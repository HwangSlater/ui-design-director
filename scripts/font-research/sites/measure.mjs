// 사이트 첫 화면에서 실제로 그려진 글꼴을 잰다. 결과는 raw.jsonl 에 한 줄씩 바로 덧붙인다(중단돼도 이어 하기)
// 사용: node measure.mjs [--limit N] [--retry-errors]  · 동시에 띄우는 브라우저는 WORKERS(기본·최대 4)
import { readFileSync, writeFileSync, appendFileSync, existsSync } from "node:fs";
import { launch, Cdp, sleep } from "../../../skills/ui-design-director/scripts/browser.mjs"; // 스킬과 같은 브라우저 띄우기·끄기

const SITE_TIMEOUT = Number(process.env.SITE_TIMEOUT_MS || 25000);
const WORKERS = Math.min(4, Number(process.env.WORKERS || 4));
const RAW = "raw.jsonl";
const args = process.argv.slice(2);
const limit = args.includes("--limit") ? Number(args[args.indexOf("--limit") + 1]) : Infinity;
const withWww = (url) => { const u = new URL(url); u.hostname = "www." + u.hostname; return u.href; }; // 맨 도메인이 안 열릴 때 www 로 다시
const UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0";

// sites.csv: 모든 칸이 큰따옴표로 감싸여 있다
const parseRow = (l) => [...l.matchAll(/"((?:[^"]|"")*)"/g)].map((m) => m[1].replace(/""/g, '"'));
const sites = readFileSync("sites.csv", "utf8").replace(/^﻿/, "").split(/\r?\n/).slice(1).filter(Boolean)
  .map(parseRow).map(([url, name]) => ({ url, name }));

// 이어 하기: 이미 잰 사이트는 건너뛴다. --retry-errors 면 실패 줄을 지우고 다시 잰다
let done = new Set();
if (existsSync(RAW)) {
  let lines = readFileSync(RAW, "utf8").split("\n").filter(Boolean).map((l) => JSON.parse(l));
  if (args.includes("--retry-errors")) {
    lines = lines.filter((r) => !r.error);
    writeFileSync(RAW, lines.map((r) => JSON.stringify(r)).join("\n") + (lines.length ? "\n" : ""));
  }
  done = new Set(lines.map((r) => r.name));
}
const queue = sites.filter((s) => !done.has(s.name)).slice(0, limit);
console.log(`대상 ${sites.length}, 남은 것 ${queue.length}`);

// 페이지 안에서: 역할별 대표 요소에 표시를 달고 계산된 font-family 를 모은다
const PROBE = `(() => {
  const vis = (el) => { const r = el.getBoundingClientRect(); const cs = getComputedStyle(el);
    return r.width > 0 && r.height > 0 && cs.visibility !== "hidden" && cs.display !== "none" && (el.innerText || el.value || "").trim().length > 0; };
  const out = { title: document.title, lang: document.documentElement.lang, roles: {} };
  const mark = (role, els) => {
    const picked = [...els].filter(vis).slice(0, 3);
    picked.forEach((el, i) => el.setAttribute("data-fr", role + i));
    out.roles[role] = picked.map((el) => ({ tag: el.tagName.toLowerCase(), ff: getComputedStyle(el).fontFamily, w: getComputedStyle(el).fontWeight, text: (el.innerText || el.value || "").trim().slice(0, 20) }));
  };
  mark("heading", document.querySelectorAll("h1, h2, h3"));
  mark("nav", document.querySelectorAll("nav a, header a, [role=navigation] a, [class*=gnb] a, [id*=gnb] a, [class*=menu] a"));
  mark("button", document.querySelectorAll("button, [role=button], input[type=submit], a[class*=btn], a[class*=button]"));
  // 본문: 글자가 직접 들어 있는 요소들 가운데 글자 수가 가장 많은 font-family
  const tally = new Map(), sample = new Map();
  for (const el of document.querySelectorAll("body *")) {
    if (/^(SCRIPT|STYLE|NOSCRIPT|SVG|H1|H2|H3|BUTTON)$/i.test(el.tagName)) continue;
    let n = 0; for (const c of el.childNodes) if (c.nodeType === 3) n += c.textContent.trim().length;
    if (n < 2 || !vis(el)) continue;
    const ff = getComputedStyle(el).fontFamily;
    tally.set(ff, (tally.get(ff) || 0) + n); if (!sample.has(ff)) sample.set(ff, el);
  }
  const top = [...tally.entries()].sort((a, b) => b[1] - a[1]).slice(0, 3);
  out.bodyStacks = top.map(([ff, n]) => ({ ff, chars: n }));
  top.forEach(([ff], i) => sample.get(ff).setAttribute("data-fr", "body" + i));
  out.roles.body = top.map(([ff]) => ({ tag: sample.get(ff).tagName.toLowerCase(), ff }));
  const ld = []; document.fonts.forEach((f) => { if (f.status === "loaded") ld.push(f.family.replace(/^["']|["']$/g, "") + " " + f.weight + " " + f.style); });
  out.loadedFonts = [...new Set(ld)];
  out.declaredFontFaces = document.fonts.size;
  return out;
})()`;

async function measure(port, site) {
  const t = await (await fetch(`http://127.0.0.1:${port}/json/new?about:blank`, { method: "PUT" })).json();
  const cdp = await Cdp.open(t.webSocketDebuggerUrl);
  try {
    await cdp.send("Page.enable"); await cdp.send("DOM.enable"); await cdp.send("CSS.enable");
    cdp.listeners.push((m) => { if (m.method === "Page.javascriptDialogOpening") cdp.send("Page.handleJavaScriptDialog", { accept: false }).catch(() => {}); });
    await cdp.send("Network.setUserAgentOverride", { userAgent: UA, acceptLanguage: "ko-KR,ko;q=0.9", platform: "Windows" });
    await cdp.send("Emulation.setDeviceMetricsOverride", { width: 1440, height: 900, deviceScaleFactor: 1, mobile: false });
    const nav = async (url) => {
      const load = cdp.waitFor("Page.loadEventFired", 14000).catch(() => "noload");
      const r = await cdp.send("Page.navigate", { url });
      if (r.errorText) throw new Error(r.errorText);
      return load;
    };
    let loadState;
    try { loadState = await nav(site.url); }
    catch { loadState = await nav(withWww(site.url)); } // 맨 도메인이 안 열리면 www 로
    await sleep(2500);
    await cdp.send("Runtime.evaluate", { expression: "document.fonts.ready.then(()=>1)", awaitPromise: true, timeout: 3000 }).catch(() => {});
    const { result, exceptionDetails } = await cdp.send("Runtime.evaluate", { expression: PROBE, returnByValue: true });
    if (exceptionDetails) throw new Error("probe: " + exceptionDetails.text);
    const out = result.value;
    const loc = await cdp.send("Runtime.evaluate", { expression: "location.href", returnByValue: true });
    // 실제로 그린 글꼴(대체 글꼴까지): CSS.getPlatformFontsForNode
    // 재는 사이에 페이지가 바뀌면(리디렉트·새로 그리기) 노드가 사라진다 — 그때는 계산된 font-family 만 남기고 표시한다
    const platform = {};
    const { root } = await cdp.send("DOM.getDocument", { depth: 0 });
    const { nodeIds } = await cdp.send("DOM.querySelectorAll", { nodeId: root.nodeId, selector: "[data-fr]" }).catch(() => ({ nodeIds: [] }));
    if (!nodeIds.length) platform.note = "노드를 다시 찾지 못해 실제 그린 글꼴은 못 잼";
    for (const id of nodeIds) {
      const attrs = (await cdp.send("DOM.getAttributes", { nodeId: id }).catch(() => null))?.attributes;
      if (!attrs) continue;
      const role = attrs[attrs.indexOf("data-fr") + 1].replace(/\d+$/, "");
      const pf = await cdp.send("CSS.getPlatformFontsForNode", { nodeId: id }).catch(() => ({ fonts: [] }));
      (platform[role] ||= []).push(...pf.fonts.map((f) => ({ family: f.familyName, custom: f.isCustomFont, glyphs: f.glyphCount })));
    }
    return { ...out, platform, finalUrl: loc.result.value, loadState: loadState === "noload" ? "load 이벤트 없음(14초)" : "ok" };
  } finally {
    cdp.close();
    await fetch(`http://127.0.0.1:${port}/json/close/${t.id}`).catch(() => {});
  }
}

// 띄우기·끄기·남은 브라우저 치우기는 스킬의 browser.mjs 가 맡는다(끝날 때·Ctrl+C·강제 종료 뒤 다음 실행)
async function worker(wid) {
  let b = null;
  const start = async () => { b = await launch("capture-"); };
  const stop = async () => { if (b) { const c = b.close; b = null; await c(); } };
  while (queue.length) {
    const site = queue.shift();
    if (!b) await start();
    const t0 = Date.now();
    let rec, timer;
    try {
      const to = new Promise((_, rej) => { timer = setTimeout(() => rej(new Error(`시간 초과 ${SITE_TIMEOUT / 1000}초`)), SITE_TIMEOUT); });
      rec = { name: site.name, url: site.url, ...(await Promise.race([measure(b.port, site), to])) };
    } catch (e) {
      rec = { name: site.name, url: site.url, error: String(e.message || e).slice(0, 200) };
      await stop(); // 멈춘 탭이 남지 않게 브라우저째 새로 띄운다
    } finally { clearTimeout(timer); }
    rec.ms = Date.now() - t0; rec.measuredAt = new Date().toISOString();
    appendFileSync(RAW, JSON.stringify(rec) + "\n");
    console.log(`[w${wid}] ${rec.error ? "실패" : "완료"} ${site.name} ${rec.ms}ms${rec.error ? " " + rec.error : ""}`);
  }
  await stop();
}
await Promise.all(Array.from({ length: WORKERS }, (_, i) => worker(i + 1)));
cleanup();
await sleep(2000);
console.log("끝");
