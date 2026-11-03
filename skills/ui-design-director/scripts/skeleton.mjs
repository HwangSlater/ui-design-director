#!/usr/bin/env node
// 화면의 「뼈대」를 숫자로 잰다 — 칸이 세로로만 쌓이는지(한 단 비율), 몇 단으로 나뉘는지, 옆에 붙어 있는 안내판, 둥근 모양, 옆으로 넘기는 띠, 사진 위 글.
// 사용자 지적(2026-11-04): 시안 셋이 업종과 참고 사이트가 달라도 「머리 → 전폭 칸 세로 나열 · 직사각형」 한 틀로 나왔다. 참고한 실제 사이트들은 다 달랐다.
// 사용: node skeleton.mjs <out.md> [--width 1280] 이름=주소 ... [--ours 이름] [--prev 이름,이름]
//   --ours: 우리 시안. 기준(--ours·--prev 아닌 것)과 뼈대가 다르면 「참고와 다름」.
//   --prev: 이전 프로젝트 시안. 우리 시안과 뼈대가 거의 같으면 「이전 시안과 같은 틀」.
// 외부 패키지 없음. Edge/Chrome DevTools 프로토콜만 쓴다.
import { spawn } from "node:child_process";
import { existsSync, mkdtempSync, rmSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { createServer } from "node:net";

const SETTLE_MS = 3000;
const SCROLL_STEP_MS = 150;
const DESKTOP_H = 800;
const BAND = 160;          // 세로로 이만큼씩 잘라 단 수를 센다(px)
const MAX_PAGE = 8000;     // 앞부분만
const GAP = 24;            // 이보다 가까운 글·사진 덩어리는 한 단으로 본다(px)
const MIN_BOX = 20000;     // 모양을 볼 상자 최소 넓이(px²)
const ROUND_PX = 20;       // 이 이상 둥글면 「둥근 모양」
const SAME_STACK = 0.12;   // 한 단 비율 차이가 이 안이면 같은 틀로 본다
const DIFF_STACK = 0.2;    // 기준과 이만큼 넘게 다르면 「참고와 다름」
const WIN_DIRS = [process.env["ProgramFiles(x86)"], process.env.ProgramFiles, process.env.LOCALAPPDATA].filter(Boolean);
const BROWSERS = [process.env.CAPTURE_BROWSER,
  ...WIN_DIRS.flatMap((d) => [join(d, "Microsoft/Edge/Application/msedge.exe"), join(d, "Google/Chrome/Application/chrome.exe")]),
  "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome", "/usr/bin/google-chrome", "/usr/bin/chromium"].filter(Boolean);
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const freePort = () => new Promise((res, rej) => { const s = createServer(); s.once("error", rej); s.listen(0, "127.0.0.1", () => { const { port } = s.address(); s.close(() => res(port)); }); });

const args = process.argv.slice(2);
const out = args[0];
const width = args.includes("--width") ? Number(args[args.indexOf("--width") + 1]) : 1280;
const ours = args.includes("--ours") ? args[args.indexOf("--ours") + 1] : null;
const prev = args.includes("--prev") ? args[args.indexOf("--prev") + 1].split(",") : [];
const targets = args.slice(1).filter((a) => a.includes("=") && !a.startsWith("--")).map((a) => { const i = a.indexOf("="); return [a.slice(0, i), a.slice(i + 1)]; });
if (!out || !targets.length) { console.error("사용: node skeleton.mjs <out.md> [--width 1280] 이름=주소 ... [--ours 이름] [--prev 이름,이름]"); process.exit(1); }

const PROBE = `(() => {
  const H = Math.min(document.documentElement.scrollHeight, ${MAX_PAGE}), W = innerWidth, VH = innerHeight;
  const leaves = [];
  for (const el of document.querySelectorAll("img,video,picture,svg,h1,h2,h3,h4,p,li,a,button,input,blockquote,dt,dd,figcaption,td")) {
    const cs = getComputedStyle(el); if (cs.visibility === "hidden" || cs.display === "none" || +cs.opacity === 0) continue;
    const r = el.getBoundingClientRect(); if (r.width < 8 || r.height < 8) continue;
    const isMedia = /^(IMG|VIDEO|PICTURE|svg)$/i.test(el.tagName);
    if (!isMedia && !(el.innerText || el.value || "").trim()) continue;
    if (!isMedia && el.querySelector("p,li,h1,h2,h3,img")) continue; // 안쪽 칸만
    leaves.push({ x: r.left, w: r.width, y: r.top + scrollY, h: r.height, media: isMedia });
  }
  const bands = [];
  for (let y = 0; y < H; y += ${BAND}) {
    const iv = leaves.filter((b) => b.y < y + ${BAND} && b.y + b.h > y && b.w < W * 0.98 || (b.y < y + ${BAND} && b.y + b.h > y && b.media)).map((b) => [Math.max(0, b.x), Math.min(W, b.x + b.w)]).sort((a, b) => a[0] - b[0]);
    if (!iv.length) continue;
    const cols = [];
    for (const [a, b] of iv) { const c = cols[cols.length - 1]; if (c && a <= c[1] + ${GAP}) c[1] = Math.max(c[1], b); else cols.push([a, b]); }
    bands.push(cols.length);
  }
  const stack = bands.length ? bands.filter((n) => n <= 1).length / bands.length : 1;
  let changes = 0; for (let i = 1; i < bands.length; i++) if (Math.min(bands[i], 3) !== Math.min(bands[i - 1], 3)) changes++;
  let side = false, hscroll = 0, overText = 0;
  const radii = []; let shapes = 0;
  for (const el of document.querySelectorAll("body *")) {
    const cs = getComputedStyle(el), r = el.getBoundingClientRect();
    if ((cs.position === "sticky" || cs.position === "fixed") && r.height > VH * 0.5 && r.width < W * 0.45 && r.width > 120) side = true;
    if (/(auto|scroll)/.test(cs.overflowX) && el.scrollWidth > el.clientWidth + 20 && r.height > 80) hscroll++;
    const area = r.width * r.height;
    if (area > ${MIN_BOX}) {
      const visible = /^(IMG|VIDEO)$/.test(el.tagName) || cs.backgroundImage !== "none" || (cs.backgroundColor !== "rgba(0, 0, 0, 0)" && cs.backgroundColor !== "transparent") || parseFloat(cs.borderTopWidth) > 0; // lint:allow color 계산된 스타일의 투명 값과 비교하는 것(색을 쓰는 곳 아님)
      if (visible) {
        const rad = Math.max(...[cs.borderTopLeftRadius, cs.borderTopRightRadius, cs.borderBottomLeftRadius, cs.borderBottomRightRadius].map((v) => v.endsWith("%") ? parseFloat(v) / 100 * Math.min(r.width, r.height) : parseFloat(v) || 0));
        radii.push(rad);
        if (cs.clipPath !== "none" || rad >= Math.min(r.width, r.height) / 3) shapes++;
      }
    }
  }
  const imgs = [...document.querySelectorAll("img")].map((i) => i.getBoundingClientRect()).filter((r) => r.width * r.height > 40000);
  for (const t of document.querySelectorAll("h1,h2,p")) { const r = t.getBoundingClientRect(); if ((t.innerText || "").trim() && imgs.some((m) => r.left >= m.left && r.right <= m.right && r.top >= m.top && r.bottom <= m.bottom)) overText++; }
  radii.sort((a, b) => a - b);
  return { stack, maxCols: Math.max(1, ...bands), changes, side, hscroll, roundShare: radii.length ? radii.filter((v) => v >= ${ROUND_PX}).length / radii.length : 0, radMed: radii.length ? radii[Math.floor(radii.length / 2)] : 0, shapes, overText, bands: bands.length };
})()`;

const exe = BROWSERS.find((p) => existsSync(p));
if (!exe) { console.error("Edge 또는 Chrome을 찾지 못했습니다(CAPTURE_BROWSER 로 지정)."); process.exit(1); }
const port = await freePort();
const profile = mkdtempSync(join(tmpdir(), "skeleton-"));
const proc = spawn(exe, ["--headless=new", "--disable-gpu", "--hide-scrollbars", "--no-first-run", `--remote-debugging-port=${port}`, `--user-data-dir=${profile}`, "about:blank"], { stdio: "ignore" });
let list;
for (let i = 0; i < 50 && !list; i++) { try { list = await (await fetch(`http://127.0.0.1:${port}/json/list`)).json(); } catch { await sleep(200); } }
const ws = new WebSocket(list.find((t) => t.type === "page").webSocketDebuggerUrl);
await new Promise((r) => ws.addEventListener("open", r, { once: true }));
let id = 0; const wait = new Map();
ws.addEventListener("message", (m) => { const d = JSON.parse(m.data); if (wait.has(d.id)) { wait.get(d.id)(d); wait.delete(d.id); } });
const cdp = (method, params = {}) => new Promise((r) => { const n = ++id; wait.set(n, r); ws.send(JSON.stringify({ id: n, method, params })); });

const rows = [];
try {
  await cdp("Page.enable");
  await cdp("Emulation.setDeviceMetricsOverride", { width, height: DESKTOP_H, deviceScaleFactor: 1, mobile: false });
  for (const [name, url] of targets) {
    await cdp("Page.navigate", { url });
    await sleep(SETTLE_MS);
    await cdp("Runtime.evaluate", { expression: `(async () => { for (let y = 0; y < Math.min(document.body.scrollHeight, ${MAX_PAGE}); y += innerHeight) { scrollTo(0, y); await new Promise(r => setTimeout(r, ${SCROLL_STEP_MS})); } scrollTo(0, 0); })()`, awaitPromise: true });
    await sleep(SETTLE_MS / 2);
    const r = await cdp("Runtime.evaluate", { expression: PROBE, returnByValue: true });
    const v = r.result?.result?.value;
    if (!v) { console.log(`실패  ${name}`); continue; }
    rows.push({ name, ...v });
    console.log(`잼  ${name}`);
  }
} finally {
  ws.close(); proc.kill(); await sleep(300);
  try { rmSync(profile, { recursive: true, force: true }); } catch { /* 브라우저가 늦게 놓음 */ }
}

const pct = (x) => `${Math.round(x * 100)}%`;
const COLS = [["stack", "한 단으로만 쌓인 비율", pct], ["maxCols", "가장 많은 단", String], ["changes", "단 수가 바뀐 횟수", String], ["side", "옆에 붙은 안내판", (x) => (x ? "있음" : "—")],
  ["hscroll", "옆으로 넘기는 띠", String], ["roundShare", "둥근 상자 비율", pct], ["radMed", "모서리 가운데 값", (x) => `${Math.round(x)}px`], ["shapes", "원·아치·자른 모양", String], ["overText", "사진 위 글", String]];
const lines = [`# 뼈대 비교 — ${width}px`, "", `| 항목 | ${rows.map((r) => r.name).join(" | ")} |`, `|---|${rows.map(() => "---").join("|")}|`];
for (const [k, label, f] of COLS) lines.push(`| ${label} | ${rows.map((r) => f(r[k])).join(" | ")} |`);
const me = rows.find((r) => r.name === ours);
const refs = rows.filter((r) => r.name !== ours && !prev.includes(r.name));
const notes = [];
if (me && refs.length) {
  const med = (k) => { const s = refs.map((r) => +r[k]).sort((a, b) => a - b); return s[Math.floor(s.length / 2)]; };
  if (Math.abs(me.stack - med("stack")) > DIFF_STACK) notes.push(`참고와 다름: 한 단 비율 ${pct(me.stack)} ↔ 참고 가운데 ${pct(med("stack"))}`);
  if (refs.some((r) => r.side) && !me.side) notes.push("참고에 옆 안내판이 있는데 우리는 없음");
  if (refs.some((r) => r.hscroll) && !me.hscroll) notes.push("참고에 옆으로 넘기는 띠가 있는데 우리는 없음");
  if (Math.abs(me.roundShare - med("roundShare")) > DIFF_STACK) notes.push(`참고와 다름: 둥근 상자 ${pct(me.roundShare)} ↔ 참고 가운데 ${pct(med("roundShare"))}`);
}
for (const p of rows.filter((r) => me && prev.includes(r.name))) {
  if (Math.abs(p.stack - me.stack) <= SAME_STACK && p.side === me.side && !!p.hscroll === !!me.hscroll && Math.abs(p.roundShare - me.roundShare) <= SAME_STACK)
    notes.push(`이전 시안과 같은 틀: ${p.name}(한 단 ${pct(p.stack)}, 둥근 ${pct(p.roundShare)}) — 컨셉·참고에서 뼈대를 다시 잡을 것`);
}
lines.push("", notes.length ? notes.map((n) => `- ${n}`).join("\n") : "- 걸린 것 없음");
writeFileSync(out, lines.join("\n") + "\n", "utf8");
console.log(lines.slice(-Math.max(1, notes.length)).join("\n"));
