#!/usr/bin/env node
// 화면 「구성」을 숫자로 잰다 — 첫 화면에서 사진·색 판·빈 바탕이 차지하는 비율, 가장 큰 글자, 진한 색 덩어리 수, 내용 폭.
// 둥글기·여백 같은 작은 값(extract_styles.mjs)이 같아도 구성이 다르면 실제 사이트처럼 보이지 않는다. 그래서 따로 잰다.
// 사용: node compose_metrics.mjs <out.md> --width 1280 이름=주소 이름=주소 ... [--ours 이름]
//   --ours 로 우리 화면을 지정하면 나머지(기준 사이트)의 가운데 값과 비교해 미달 항목을 표시한다.
// 외부 패키지 없음. Edge/Chrome DevTools 프로토콜만 쓴다.
import { writeFileSync } from "node:fs";
import { launch } from "./browser.mjs";

const SETTLE_MS = 3000;
const SCROLL_STEP_MS = 150;
const PHONE_MAX = 600;
const PHONE_H = 844, DESKTOP_H = 800;
const CELL = 8; // 넓이를 셀 때 칸 크기(px)
const MAX_PAGE = 12000; // 너무 긴 페이지는 앞부분만
// 미달 판정: 기준 사이트 가운데 값 대비 이 비율 아래면 「미달」
const SHORT_RATIO = 0.7;
// 첫 화면이 이만큼 넘게 비어 있으면 그 기준 사이트는 덜 불러온 것으로 보고 가운데 값에서 뺀다.
// 빵집 비교에서 Tatte·태극당이 한 번은 88%·60%, 다음 번엔 1% 로 재져 기준이 흔들렸다.
const BLANK_REF = 0.9;
const MIN_REFS = 2;
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

const args = process.argv.slice(2);
const out = args[0];
const width = Number(args[args.indexOf("--width") + 1]) || 1280;
const ours = args.includes("--ours") ? args[args.indexOf("--ours") + 1] : null;
const targets = args.slice(1).filter((a) => a.includes("=") && !a.startsWith("--")).map((a) => { const i = a.indexOf("="); return [a.slice(0, i), a.slice(i + 1)]; });
if (!out || !targets.length) { console.error("사용: node compose_metrics.mjs <out.md> --width 1280 이름=주소 ... [--ours 이름]"); process.exit(1); }

// 페이지 안에서 도는 측정. 문서 순서대로 칠해서(나중 요소가 위) 칸마다 사진/색 판/바탕을 정한다
const PROBE = `(() => {
  const CELL = ${CELL}, W = innerWidth, H = innerHeight;
  // 쿠키·동의 창은 실제 구성이 아니므로 뺀다
  document.querySelectorAll('[id*="cookie" i],[class*="cookie" i],[id*="consent" i],[class*="consent" i],[id*="onetrust" i],[class*="onetrust" i]').forEach((n) => n.style.setProperty("display", "none", "important"));
  const PH = Math.min(document.documentElement.scrollHeight, ${MAX_PAGE});
  const cols = Math.ceil(W / CELL), rows = Math.ceil(PH / CELL);
  const kind = new Uint8Array(cols * rows); // 0 바탕, 1 색 판, 2 사진
  const col = new Int32Array(cols * rows).fill(-1);
  const rgb = (s) => { const m = (s || "").match(/[\\d.]+/g); return m ? m.map(Number) : null; };
  const pageBg = (() => { for (const el of [document.body, document.documentElement]) { const c = rgb(getComputedStyle(el).backgroundColor); if (c && (c[3] ?? 1) > 0.5) return c; } return [255, 255, 255]; })();
  const dist = (a, b) => Math.hypot(a[0] - b[0], a[1] - b[1], a[2] - b[2]);
  const palette = [];
  const colourId = (c) => { const q = c.slice(0, 3).map((v) => Math.round(v / 16) * 16); const k = q.join(","); let i = palette.findIndex((p) => p.k === k); if (i < 0) { palette.push({ k, c: q }); i = palette.length - 1; } return i; };
  const paint = (r, v, cid) => {
    const x0 = Math.max(0, Math.floor(r.left / CELL)), x1 = Math.min(cols, Math.ceil(r.right / CELL));
    const y0 = Math.max(0, Math.floor((r.top + scrollY) / CELL)), y1 = Math.min(rows, Math.ceil((r.bottom + scrollY) / CELL));
    for (let y = y0; y < y1; y++) for (let x = x0; x < x1; x++) { kind[y * cols + x] = v; col[y * cols + x] = cid; }
  };
  let maxFirst = 0, textL = W, textR = 0;
  for (const el of document.querySelectorAll("body *")) {
    const cs = getComputedStyle(el);
    if (cs.display === "none" || cs.visibility === "hidden" || Number(cs.opacity) === 0) continue;
    const r = el.getBoundingClientRect();
    if (r.width * r.height < CELL * CELL * 4) continue;
    const tag = el.tagName;
    if (tag === "IMG" && !(el.complete && el.naturalWidth > 0)) continue; // 깨진 사진은 사진이 아니다
    const isImg = ["IMG", "VIDEO", "PICTURE", "CANVAS", "IFRAME"].includes(tag) || (tag === "svg" && r.width > 120 && r.height > 120) || /url\\(/.test(cs.backgroundImage) || el.classList.contains("slot") || el.hasAttribute("data-photo"); // 시안의 「사진 자리」는 사진 자리로 센다(빗금 바탕을 색 판으로 세면 사진이 들어갈 짜임을 깎아 먹음)
    if (isImg) { paint(r, 2, -1); continue; }
    const bg = rgb(cs.backgroundColor);
    if (bg && (bg[3] ?? 1) > 0.5 && dist(bg, pageBg) > 24) paint(r, 1, colourId(bg));
    else if (bg && (bg[3] ?? 1) > 0.5 && dist(bg, pageBg) <= 24 && r.width > W * 0.9) paint(r, 0, -1); // 바탕색 판은 아래 칠을 덮는다
  }
  // 글자: 첫 화면의 가장 큰 글자, 넓은 화면에서 글이 차지하는 폭
  const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  for (let n = walker.nextNode(); n; n = walker.nextNode()) {
    if (!n.textContent.trim()) continue;
    const el = n.parentElement; const cs = getComputedStyle(el);
    if (cs.display === "none" || cs.visibility === "hidden") continue;
    const range = document.createRange(); range.selectNodeContents(n);
    const r = range.getBoundingClientRect(); if (!r.width) continue;
    const top = r.top + scrollY;
    if (top < H) maxFirst = Math.max(maxFirst, parseFloat(cs.fontSize));
    // 옆으로 넘기는 칸의 화면 밖 글은 세지 않는다
    if (n.textContent.trim().length > 12 && r.right > 0 && r.left < W) { textL = Math.min(textL, Math.max(0, r.left)); textR = Math.max(textR, Math.min(W, r.right)); }
  }
  const share = (y0, y1) => { let img = 0, blk = 0, n = 0; const counts = {}; for (let y = y0; y < y1; y++) for (let x = 0; x < cols; x++) { const i = y * cols + x; n++; if (kind[i] === 2) img++; else if (kind[i] === 1) { blk++; counts[col[i]] = (counts[col[i]] || 0) + 1; } } return { img: img / n, block: blk / n, counts, n }; };
  const first = share(0, Math.min(rows, Math.ceil(H / CELL)));
  const page = share(0, rows);
  const lum = (c) => { const f = (v) => { v /= 255; return v <= 0.03928 ? v / 12.92 : ((v + 0.055) / 1.055) ** 2.4; }; return 0.2126 * f(c[0]) + 0.7152 * f(c[1]) + 0.0722 * f(c[2]); };
  const sat = (c) => { const mx = Math.max(...c), mn = Math.min(...c); return mx ? (mx - mn) / mx : 0; };
  const blocks = Object.entries(page.counts).map(([i, k]) => ({ hex: "#" + palette[i].c.map((v) => Math.min(255, v).toString(16).padStart(2, "0")).join(""), pct: k / page.n, strong: lum(palette[i].c) < 0.35 || sat(palette[i].c) > 0.45 })).sort((a, b) => b.pct - a.pct);
  return { title: document.title, height: document.documentElement.scrollHeight,
    firstImg: first.img, firstBlock: first.block, firstEmpty: 1 - first.img - first.block, maxFirstPx: maxFirst,
    pageImg: page.img, pageBlock: page.block,
    strongColours: blocks.filter((b) => b.strong && b.pct >= 0.01).length,
    blocks: blocks.slice(0, 6), textSpan: textR > textL ? (textR - textL) / W : 0 };
})()`;

const { port, close } = await launch("compose-"); // 끄기·남은 브라우저 치우기는 browser.mjs 한 곳에서
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
  const phone = width <= PHONE_MAX;
  await cdp("Emulation.setDeviceMetricsOverride", { width, height: phone ? PHONE_H : DESKTOP_H, deviceScaleFactor: 1, mobile: phone });
  for (const [name, url] of targets) {
    await cdp("Page.navigate", { url });
    await sleep(SETTLE_MS);
    // 늦게 불러오는 사진을 깨운 뒤 맨 위로
    await cdp("Runtime.evaluate", { expression: `(async () => { for (let y = 0; y < Math.min(document.body.scrollHeight, ${MAX_PAGE}); y += innerHeight) { scrollTo(0, y); await new Promise(r => setTimeout(r, ${SCROLL_STEP_MS})); } scrollTo(0, 0); })()`, awaitPromise: true });
    await sleep(SETTLE_MS / 2);
    const r = await cdp("Runtime.evaluate", { expression: PROBE, returnByValue: true });
    const v = r.result?.result?.value;
    if (!v) { console.log(`실패  ${name}  (값을 읽지 못함 — 봇 막힘일 수 있음)`); continue; }
    rows.push({ name, url, ...v });
    console.log(`잼  ${name}`);
  }
} finally {
  ws.close(); await close();
}

// 표와 판정
const METRICS = [
  ["firstImg", "첫 화면 사진 비율", (x) => `${Math.round(x * 100)}%`],
  ["firstBlock", "첫 화면 색 판 비율", (x) => `${Math.round(x * 100)}%`],
  ["firstEmpty", "첫 화면 빈 바탕", (x) => `${Math.round(x * 100)}%`],
  ["maxFirstPx", "첫 화면 가장 큰 글자", (x) => `${Math.round(x)}px`],
  ["pageImg", "전체 사진 비율", (x) => `${Math.round(x * 100)}%`],
  ["pageBlock", "전체 색 판 비율", (x) => `${Math.round(x * 100)}%`],
  ["strongColours", "진한 색 덩어리 수", (x) => `${x}`],
  ["textSpan", "글이 차지하는 폭", (x) => `${Math.round(x * 100)}%`],
];
const LOWER_IS_BETTER = new Set(["firstEmpty"]);
const median = (a) => { const s = [...a].sort((x, y) => x - y); const m = Math.floor(s.length / 2); return s.length % 2 ? s[m] : (s[m - 1] + s[m]) / 2; };
const blankRefs = rows.filter((r) => r.name !== ours && r.firstEmpty > BLANK_REF);
const refs = rows.filter((r) => r.name !== ours && !blankRefs.includes(r));
const tooFew = Boolean(ours) && refs.length < MIN_REFS;
const me = rows.find((r) => r.name === ours);
const lines = [`# 구성 비교 — ${width}px`, "", `| 항목 | ${rows.map((r) => r.name).join(" | ")} |${me ? " 판정 |" : ""}`, `|---|${rows.map(() => "---").join("|")}|${me ? "---|" : ""}`];
let short = 0;
for (const [k, label, fmt] of METRICS) {
  let verdict = "";
  if (me && !tooFew) {
    const m = median(refs.map((r) => r[k]));
    const bad = LOWER_IS_BETTER.has(k) ? me[k] > m / SHORT_RATIO && me[k] - m > 0.1 : me[k] < m * SHORT_RATIO;
    if (bad) short++;
    verdict = ` ${bad ? "미달" : "통과"} (기준 가운데 ${fmt(m)}) |`;
  }
  lines.push(`| ${label} | ${rows.map((r) => fmt(r[k])).join(" | ")} |${verdict}`);
}
lines.push("", "## 색 판(넓은 순)", ...rows.map((r) => `- ${r.name}: ${r.blocks.map((b) => `${b.hex}${b.strong ? "(진함)" : ""} ${Math.round(b.pct * 100)}%`).join(", ") || "없음"}`));
if (blankRefs.length) lines.push("", `덜 불러온 기준(첫 화면 ${Math.round(BLANK_REF * 100)}% 넘게 빔, 가운데 값에서 뺌): ${blankRefs.map((r) => r.name).join(", ")} — 다시 돌리거나 캡처를 열어 본다.`);
if (tooFew) lines.push("", `판정 못 함 — 제대로 잰 기준 사이트가 ${refs.length}곳뿐이다(${MIN_REFS}곳 이상 필요). 다시 돌린다.`);
else if (me) lines.push("", `미달 ${short}개 — 미달이 있으면 보여 주지 않고 구성을 다시 짠다(references/blind-judge.md § Composition numbers).`);
writeFileSync(out, lines.join("\n") + "\n");
console.log(lines.join("\n"));
