#!/usr/bin/env node
// 기준 사이트 화면에서 실제로 쓰인 값을 뽑는다 — 글자 크기·굵기·줄 간격, 여백, 둥글기, 그림자, 단추·입력칸·카드 모양.
// 규칙 글을 읽고 짐작으로 짜지 않고, 기준 화면의 숫자를 보고 짜기 위해서다(외부 패키지 없음).
// 사용: node extract_styles.mjs <주소> <out.json> [--width 390]
// 결과: <out.json>(원자료)과 같은 이름의 .md(요약표: 글자 단계, 단추·입력칸·카드 견본, 자주 쓴 여백·둥글기·그림자).

import { writeFileSync } from "node:fs";
import { launch } from "./browser.mjs";

const SETTLE_MS = 3000;
const PHONE_MAX = 600;
const TOP_N = 8;
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

const [url, out, ...rest] = process.argv.slice(2);
const width = Number(rest[rest.indexOf("--width") + 1]) || 390;
if (!url || !out) { console.error("사용: node extract_styles.mjs <주소> <out.json> [--width 390]"); process.exit(2); }


// 페이지 안에서 돈다: 보이는 요소를 역할별로 모아 계산된 값을 돌려준다
const PROBE = `(() => {
  const alpha = (v) => { const m = String(v).match(/[\\d.]+/g); return m && m.length === 4 ? +m[3] : (v === "transparent" ? 0 : 1); };
  const vis = (e) => { const r = e.getBoundingClientRect(); const c = getComputedStyle(e); return r.width > 4 && r.height > 4 && c.visibility !== "hidden" && c.display !== "none"; };
  const pick = (c) => ({ font: c.fontFamily.split(",")[0].replace(/["']/g, "").trim(), size: c.fontSize, weight: c.fontWeight, line: c.lineHeight,
    track: c.letterSpacing, color: c.color, bg: c.backgroundColor, pad: c.padding, radius: c.borderRadius, border: c.border, shadow: c.boxShadow, gap: c.gap });
  const text = (e) => (e.innerText || e.value || e.getAttribute("aria-label") || "").trim().replace(/\\s+/g, " ").slice(0, 40);
  const roles = {
    heading: [...document.querySelectorAll("h1,h2,h3,h4")],
    body: [...document.querySelectorAll("p,li")].filter((e) => e.innerText && e.innerText.trim().length > 20),
    button: [...document.querySelectorAll("button,a,[role=button]")].filter((e) => { const c = getComputedStyle(e); return alpha(c.backgroundColor) > 0 || parseFloat(c.borderWidth) > 0; }),
    input: [...document.querySelectorAll("input,select,textarea")],
    card: [...document.querySelectorAll("div,article,section,li,a")].filter((e) => { const c = getComputedStyle(e); const r = e.getBoundingClientRect();
      return r.width > 120 && r.height > 80 && (parseFloat(c.borderRadius) > 0 || c.boxShadow !== "none") && (alpha(c.backgroundColor) > 0 || c.boxShadow !== "none" || parseFloat(c.borderWidth) > 0); }),
    image: [...document.querySelectorAll("img,picture,video")],
  };
  const res = {};
  for (const [k, list] of Object.entries(roles)) res[k] = list.filter(vis).slice(0, 60).map((e) => ({ tag: e.tagName.toLowerCase(), text: text(e),
    w: Math.round(e.getBoundingClientRect().width), h: Math.round(e.getBoundingClientRect().height), ...pick(getComputedStyle(e)) }));
  const sections = [...document.querySelectorAll("section,main > div,header,footer")].filter(vis).slice(0, 40).map((e) => { const c = getComputedStyle(e); return { pad: c.padding, margin: c.margin, bg: c.backgroundColor }; });
  return { title: document.title, viewport: innerWidth, pageHeight: document.documentElement.scrollHeight, maxContent: Math.max(...[...document.querySelectorAll("main,section,div")].filter(vis).map((e) => e.getBoundingClientRect().width).filter((w) => w < innerWidth)), roles: res, sections };
})()`;

function tally(list, key) {
  const m = new Map();
  for (const x of list) { const v = x[key]; if (v && v !== "none" && v !== "0px" && v !== "normal") m.set(v, (m.get(v) || 0) + 1); }
  return [...m.entries()].sort((a, b) => b[1] - a[1]).slice(0, TOP_N);
}

const { port, close } = await launch("styles-"); // 끄기·남은 브라우저 치우기는 browser.mjs 한 곳에서
let list;
for (let i = 0; i < 50 && !list; i++) { try { list = await (await fetch(`http://127.0.0.1:${port}/json/list`)).json(); } catch { await sleep(200); } }
const ws = new WebSocket(list.find((t) => t.type === "page").webSocketDebuggerUrl);
await new Promise((r) => ws.addEventListener("open", r, { once: true }));
let id = 0; const wait = new Map();
ws.addEventListener("message", (m) => { const d = JSON.parse(m.data); if (wait.has(d.id)) { wait.get(d.id)(d); wait.delete(d.id); } });
const cdp = (method, params = {}) => new Promise((r) => { const n = ++id; wait.set(n, r); ws.send(JSON.stringify({ id: n, method, params })); });
try {
  await cdp("Page.enable");
  await cdp("Emulation.setDeviceMetricsOverride", { width, height: width <= PHONE_MAX ? 844 : 900, deviceScaleFactor: 1, mobile: width <= PHONE_MAX });
  await cdp("Page.navigate", { url });
  await sleep(SETTLE_MS);
  const r = await cdp("Runtime.evaluate", { expression: PROBE, returnByValue: true });
  const data = r.result?.result?.value;
  if (!data) throw new Error("페이지에서 값을 읽지 못했습니다(로그인·봇 막힘일 수 있음).");
  writeFileSync(out, JSON.stringify({ url, width, ...data }, null, 1));
  const R = data.roles;
  const all = Object.values(R).flat();
  const row = (x) => `| ${x.tag} | ${x.text || "—"} | ${x.font} | ${x.size} / ${x.weight} / ${x.line} | ${x.pad} | ${x.radius} | ${x.shadow === "none" ? "—" : "있음"} |`;
  const md = [`# ${data.title || url} — ${width}px에서 쓰인 값`, "", `주소: ${url} · 페이지 높이 ${data.pageHeight}px · 가장 넓은 내용 폭 ${data.maxContent}px`, "",
    "## 글자 단계(제목)", "| 태그 | 글 | 글꼴 | 크기/굵기/줄 | 여백 | 둥글기 | 그림자 |", "|---|---|---|---|---|---|---|", ...R.heading.slice(0, 10).map(row), "",
    "## 본문", "| 태그 | 글 | 글꼴 | 크기/굵기/줄 | 여백 | 둥글기 | 그림자 |", "|---|---|---|---|---|---|---|", ...R.body.slice(0, 5).map(row), "",
    "## 단추", "| 태그 | 글 | 글꼴 | 크기/굵기/줄 | 여백 | 둥글기 | 그림자 |", "|---|---|---|---|---|---|---|", ...R.button.slice(0, 10).map(row), "",
    "## 입력칸", "| 태그 | 글 | 글꼴 | 크기/굵기/줄 | 여백 | 둥글기 | 그림자 |", "|---|---|---|---|---|---|---|", ...R.input.slice(0, 6).map(row), "",
    "## 카드·상자", "| 태그 | 글 | 글꼴 | 크기/굵기/줄 | 여백 | 둥글기 | 그림자 |", "|---|---|---|---|---|---|---|", ...R.card.slice(0, 8).map(row), "",
    `## 자주 쓴 값`, `- 글자 크기: ${tally(all, "size").map(([v, n]) => `${v}×${n}`).join(", ")}`,
    `- 둥글기: ${tally(all, "radius").map(([v, n]) => `${v}×${n}`).join(", ")}`,
    `- 여백: ${tally(all, "pad").map(([v, n]) => `${v}×${n}`).join(", ")}`,
    `- 그림자: ${tally(all, "shadow").map(([v, n]) => `${v}×${n}`).join(" / ") || "없음"}`,
    `- 구획 여백: ${tally(data.sections, "pad").map(([v, n]) => `${v}×${n}`).join(", ")}`,
    `- 사진·영상 수: ${R.image.length} · 카드·상자 수: ${R.card.length} · 단추 수: ${R.button.length}`, ""].join("\n");
  writeFileSync(out.replace(/\.json$/i, "") + ".md", md);
  console.log(`wrote ${out} (+ .md)`);
} finally {
  ws.close(); await close();
}
