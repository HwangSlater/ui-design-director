#!/usr/bin/env node
// 화면의 「뼈대」를 숫자로 잰다 — 칸이 세로로만 쌓이는지(한 단 비율), 몇 단으로 나뉘는지, 옆에 붙어 있는 안내판, 둥근 모양, 옆으로 넘기는 띠, 사진 위 글.
// 사용자 지적(2026-11-04): 시안 셋이 업종과 참고 사이트가 달라도 「머리 → 전폭 칸 세로 나열 · 직사각형」 한 틀로 나왔다. 참고한 실제 사이트들은 다 달랐다.
// 사용: node skeleton.mjs <out.md> [--width 1280] 이름=주소 ... [--base 이름] [--ours 이름] [--prev 이름,이름]
//   --base: 의뢰인이 고른 템플릿·대표 사이트. 짜임은 이것을 따르고, 관련 사이트 여럿이 함께 다르게 하는 곳만 「바꿀 곳」으로 뽑는다(skeleton_base.mjs).
//   --ours: 우리 시안. --base 가 있으면 바탕과 다른 곳(바꿀 곳 말고)을 알린다. 없으면 참고들의 공통 범위와 견준다.
//   --prev: 이전 프로젝트 시안. 우리 시안과 뼈대가 거의 같으면 「이전 시안과 같은 틀」.
//   바탕이 아닌 참고 한 곳과 거의 같으면 「참고 한 곳과 거의 같은 뼈대」.
// 외부 패키지 없음. Edge/Chrome DevTools 프로토콜만 쓴다.
import { writeFileSync } from "node:fs";
import { evaluate, goto, launch, openPage, scrollWakeExpr, sleep, VIEWPORT } from "./browser.mjs";
import { baseDiff } from "./skeleton_base.mjs";

const SETTLE_MS = 3000;
const SCROLL_STEP_MS = 150;
const BAND = 160;          // 세로로 이만큼씩 잘라 단 수를 센다(px)
const MAX_PAGE = 8000;     // 앞부분만
const GAP = 24;            // 이보다 가까운 글·사진 덩어리는 한 단으로 본다(px)
const MIN_COL = 64;        // 이보다 좁은 것(아이콘·색 점·작은 링크)은 단으로 세지 않는다 — 폰에서 아이콘 줄을 「7단」으로 세던 것
const MIN_BOX = 20000;     // 모양을 볼 상자 최소 넓이(px²)
const ROUND_PX = 20;       // 이 이상 둥글면 「둥근 모양」
const MIN_PHOTO = 10000;   // 모서리를 볼 사진 최소 넓이(px²)
const PHOTO_ROUND = 4;     // 사진 모서리가 이 이상이면 둥근 사진
const BOX_OVER = 0.15;     // 바탕·테두리 상자 넓이가 참고 가장 많은 곳보다 이만큼 넘으면 「상자 위에 상자」
const SAME_STACK = 0.12;   // 한 단 비율 차이가 이 안이면 같은 틀로 본다
const DIFF_STACK = 0.2;    // 참고들의 한 단 비율 범위에서 이만큼 넘게 벗어나면 「공통 범위 밖」
const CLONE = 0.05;        // 참고 한 곳과 비율 차이가 모두 이 안이고 단·띠·안내판이 같으면 「참고 한 곳과 거의 같음」(베낀 짜임)
// 브라우저 이름은 openPage 가 건다 — 머리 없는 브라우저 이름(HeadlessChrome)으로 가면 네이버 지도가 빈 화면을 줘서 사진이 「없음」으로 나왔다

const args = process.argv.slice(2);
const out = args[0];
const width = args.includes("--width") ? Number(args[args.indexOf("--width") + 1]) : 1280;
const ours = args.includes("--ours") ? args[args.indexOf("--ours") + 1] : null;
const base = args.includes("--base") ? args[args.indexOf("--base") + 1] : null;
const prev = args.includes("--prev") ? args[args.indexOf("--prev") + 1].split(",") : [];
const targets = args.slice(1).filter((a) => a.includes("=") && !a.startsWith("--")).map((a) => { const i = a.indexOf("="); return [a.slice(0, i), a.slice(i + 1)]; });
if (!out || !targets.length) { console.error("사용: node skeleton.mjs <out.md> [--width 1280] 이름=주소 ... [--base 이름] [--ours 이름] [--prev 이름,이름]"); process.exit(1); }

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
  const bands = [], kinds = [];
  for (let y = 0; y < H; y += ${BAND}) {
    const inBand = leaves.filter((b) => b.y < y + ${BAND} && b.y + b.h > y && b.w >= ${MIN_COL} && (b.w < W * 0.98 || b.media));
    const iv = inBand.map((b) => [Math.max(0, b.x), Math.min(W, b.x + b.w)]).sort((a, b) => a[0] - b[0]);
    if (!iv.length) continue;
    const cols = [];
    for (const [a, b] of iv) { const c = cols[cols.length - 1]; if (c && a <= c[1] + ${GAP}) c[1] = Math.max(c[1], b); else cols.push([a, b]); }
    bands.push(cols.length);
    // 배치 순서: 사진이 차지하는 띠(사진) / 3칸 이상(여러 칸) / 그 밖(글)
    const mediaW = inBand.filter((b) => b.media).reduce((s, b) => s + Math.min(b.w, W), 0);
    kinds.push(mediaW > W * 0.45 ? (cols.length >= 3 ? "사진 여러 칸" : "큰 사진") : cols.length >= 3 ? "여러 칸" : "글");
  }
  const order = kinds.filter((k, i) => i === 0 || k !== kinds[i - 1]).slice(0, 6);
  const firstImg = leaves.filter((b) => b.media && b.y < VH).reduce((s, b) => s + Math.min(b.w, W) * Math.min(b.h, VH - b.y), 0) / (W * VH);
  const searchFirst = [...document.querySelectorAll("input")].some((i) => {
    const r = i.getBoundingClientRect();
    const words = i.placeholder + (i.getAttribute("aria-label") || "") + (i.closest("form")?.getAttribute("role") || "");
    return r.top + scrollY < VH && r.width > 120 && (i.type === "search" || /검색|찾|search/i.test(words));
  });
  const navTop = [...document.querySelectorAll("header a, nav a")].filter((a) => { const r = a.getBoundingClientRect(); return r.top + scrollY < 140 && r.width > 0; }).length >= 3;
  const callEnd = [...document.querySelectorAll('a[href^="tel:"], a[href*="kakao"], a[href^="mailto:"]')].some((a) => a.getBoundingClientRect().top + scrollY > document.documentElement.scrollHeight - 1200);
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
      const filled = cs.backgroundColor !== "rgba(0, 0, 0, 0)" && cs.backgroundColor !== "transparent"; // lint:allow color 계산된 스타일의 투명 값과 비교하는 것(색을 쓰는 곳 아님)
      const visible = /^(IMG|VIDEO)$/.test(el.tagName) || cs.backgroundImage !== "none" || filled || parseFloat(cs.borderTopWidth) > 0;
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
  // 모양은 큰 상자 하나로 말하지 않는다(사용자 2026-11-04: 「직사각형을 너무 의식해서 오히려 AI 티」) —
  // 참고에 큰 둥근 상자가 없던 것을 「모서리 0」으로 읽어 사진·단추·칸까지 전부 네모로 만들었다. 실제로는 큰 상자 자체가 적고 사진·단추는 둥글었다.
  const rad = (cs, w, h) => Math.max(...[cs.borderTopLeftRadius, cs.borderBottomRightRadius].map((v) => v.endsWith("%") ? parseFloat(v) / 100 * Math.min(w, h) : parseFloat(v) || 0));
  const photoR = [];
  for (const im of document.querySelectorAll("img,video")) {
    const r = im.getBoundingClientRect(); if (r.width * r.height < ${MIN_PHOTO}) continue;
    let best = rad(getComputedStyle(im), r.width, r.height), el = im.parentElement;
    for (let i = 0; i < 3 && el && !best; i++, el = el.parentElement) { const c = getComputedStyle(el); if (c.overflow !== "visible") best = rad(c, r.width, r.height); }
    photoR.push(best);
  }
  photoR.sort((a, b) => a - b);
  const btn = { 알약: 0, 둥근: 0, 각진: 0 }; let wideBtn = 0;
  for (const b of document.querySelectorAll("a,button")) {
    const cs = getComputedStyle(b), r = b.getBoundingClientRect();
    if (r.height < 24 || r.height > 90 || r.width < 40 || r.top + scrollY > H) continue;
    if (!((cs.backgroundColor !== "rgba(0, 0, 0, 0)" && cs.backgroundColor !== "transparent") || parseFloat(cs.borderTopWidth) > 0)) continue; // lint:allow color 계산된 투명 값과 비교
    const k = rad(cs, r.width, r.height); btn[k >= r.height / 2 - 1 ? "알약" : k >= 4 ? "둥근" : "각진"]++;
    if (r.width > W * 0.8) wideBtn++;
  }
  // 바탕 넓이: 격자 점마다 가장 안쪽 바탕을 찾아, 가장 넓은 바탕(그 페이지의 「종이」)이 아닌 곳의 비율과 상자 속 상자 비율을 잰다.
  // 네이버처럼 회색 몸통 위에 흰 띠를 깐 곳은 흰 띠가 종이가 된다(몸통 색과 비교하면 100% 상자로 잘못 나옴).
  const TRANSPARENT = ["rgba(0, 0, 0, 0)", "transparent"]; // lint:allow color 계산된 투명 값과 비교
  const fills = [];
  for (const el of document.querySelectorAll("body, body *")) {
    if (/^(IMG|VIDEO|PICTURE|svg)$/i.test(el.tagName)) continue;
    const cs = getComputedStyle(el); const r = el.getBoundingClientRect(); if (r.width < ${MIN_COL} || r.height < 24) continue;
    const framed = ["Top", "Right", "Bottom", "Left"].filter((x) => parseFloat(cs["border" + x + "Width"]) > 0).length >= 3;
    const bg = cs.backgroundImage !== "none" ? "img" : TRANSPARENT.includes(cs.backgroundColor) ? null : cs.backgroundColor;
    if (!bg && !framed) continue;
    fills.push({ x: r.left, y: r.top + scrollY, w: r.width, h: r.height, bg: bg || "frame", img: bg === "img" });
  }
  const STEP = 24, hits = {}; let pts = 0; const deep = [];
  for (let y = 0; y < H; y += STEP) for (let x = STEP / 2; x < W; x += STEP) {
    const on = fills.filter((f) => x >= f.x && x < f.x + f.w && y >= f.y && y < f.y + f.h);
    pts++; const top = on[on.length - 1]; const k = top ? top.bg : "none"; hits[k] = (hits[k] || 0) + 1; deep.push(on);
  }
  const paper = Object.entries(hits).filter(([k]) => k !== "img").sort((a, b) => b[1] - a[1])[0]?.[0] || "none";
  let boxed = 0, nested = 0;
  for (const on of deep) {
    if (on.some((f) => f.img)) continue;
    const paperAt = on.map((f) => f.bg).lastIndexOf(paper);
    const above = on.slice(paperAt + 1).filter((f) => f.bg !== paper); // 종이 위에 올린 바탕·테두리
    if (above.length) boxed++; if (above.length >= 2) nested++;
  }
  const boxShare = boxed / pts, nestShare = nested / pts;
  for (const el of document.querySelectorAll("body *")) {
    const cs = getComputedStyle(el); if (cs.backgroundImage === "none" || !cs.backgroundImage.includes("url(")) continue;
    const r = el.getBoundingClientRect(); if (r.width * r.height < ${MIN_PHOTO} || r.top + scrollY > H) continue;
    let best = rad(cs, r.width, r.height), p = el.parentElement;
    for (let i = 0; i < 3 && p && !best; i++, p = p.parentElement) { const c = getComputedStyle(p); if (c.overflow !== "visible") best = rad(c, r.width, r.height); }
    photoR.push(best);
  }
  photoR.sort((a, b) => a - b);
  const btnTop = Object.entries(btn).sort((a, b) => b[1] - a[1])[0];
  const mid = (a) => a[Math.floor(a.length / 2)];
  return {
    photoRad: photoR.length ? mid(photoR) : null, photoN: photoR.length,
    btnShape: btnTop[1] ? btnTop[0] : "—", btnN: btn.알약 + btn.둥근 + btn.각진, wideBtn,
    boxShare, nestShare, stack, maxCols: Math.max(1, ...bands), changes, side, hscroll,
    roundShare: radii.length ? radii.filter((v) => v >= ${ROUND_PX}).length / radii.length : 0,
    radMed: radii.length ? mid(radii) : 0,
    shapes, overText, bands: bands.length, order, heroPhoto: firstImg > 0.4, searchFirst, navTop, callEnd,
  };
})()`;

async function measureOne(cdp, url) {
  await goto(cdp, url);
  await sleep(SETTLE_MS);
  await evaluate(cdp, scrollWakeExpr(MAX_PAGE, SCROLL_STEP_MS), { awaitPromise: true });
  await sleep(SETTLE_MS / 2);
  return evaluate(cdp, PROBE);
}

async function measureAll(port) {
  const rows = [];
  // 폰 너비는 따로 잰다 — 넓은 화면의 칸 나눔을 폰 공통점으로 말하면 안 됨(의뢰인 지적). 컴퓨터 폭은 800 높이로 재 왔다
  const page = await openPage(port, { width, height: VIEWPORT.measure });
  try {
    for (const [name, url] of targets) {
      let v;
      try { v = await measureOne(page.cdp, url); } catch (err) { console.log(`실패  ${name}  (${err.message})`); continue; }
      if (!v) { console.log(`실패  ${name}`); continue; }
      rows.push({ name, host: url.startsWith("file:") ? `file:${name}` : new URL(url).host, ...v });
      console.log(`잼  ${name}`);
    }
  } finally {
    await page.close();
  }
  return rows;
}

async function main() {
  const { port, close } = await launch("skeleton-"); // 끄기·남은 브라우저 치우기는 browser.mjs 한 곳에서
  try {
    report(await measureAll(port));
  } finally {
    await close();
  }
}

const pct = (x) => `${Math.round(x * 100)}%`;
const COLS = [["stack", "한 단으로만 쌓인 비율", pct], ["maxCols", "가장 많은 단", String], ["changes", "단 수가 바뀐 횟수", String], ["side", "옆에 붙은 안내판", (x) => (x ? "있음" : "—")],
  ["hscroll", "옆으로 넘기는 띠", String], ["roundShare", "둥근 큰 상자 비율", pct], ["radMed", "큰 상자 모서리 가운데 값", (x) => `${Math.round(x)}px`],
  ["photoRad", "사진 모서리 가운데 값", (x) => (x == null ? "사진 없음" : `${Math.round(x)}px`)], ["btnShape", "단추 모양(가장 많은 것)", String], ["btnN", "단추 수", String], ["wideBtn", "폭 가득 단추", String], ["boxShare", "종이 위 바탕·테두리 칸 넓이", pct], ["nestShare", "칸 속 칸 넓이", pct], ["shapes", "원·아치·자른 모양", String], ["overText", "사진 위 글", String]];
function report(rows) {
  const lines = [`# 뼈대 비교 — ${width}px`, "", `| 항목 | ${rows.map((r) => r.name).join(" | ")} |`, `|---|${rows.map(() => "---").join("|")}|`];
  for (const [k, label, f] of COLS) lines.push(`| ${label} | ${rows.map((r) => f(r[k])).join(" | ")} |`);
  const me = rows.find((r) => r.name === ours);
  const refs = rows.filter((r) => r.name !== ours && !prev.includes(r.name));
  const notes = [];
  const baseRow = rows.find((r) => r.name === base);
  if (base && !baseRow) notes.push(`바탕 ${base} 을(를) 못 잼 — 이름=주소 목록에 넣을 것`);
  const others = refs.filter((r) => r !== baseRow);
  // 너무 같아도 문제(사용자): 참고 한 곳의 뼈대를 그대로 옮긴 것은 베낀 짜임 — 분야의 범위 안에서 컨셉으로 바꿔야 함
  for (const r of others.filter(() => me && me.stack < 0.9)) { // 둘 다 거의 한 줄로만 쌓인 폰 화면은 뼈대가 같아도 베낀 게 아님(폰의 기본) — 비교하지 않음
    if (Math.abs(r.stack - me.stack) <= CLONE && r.maxCols === me.maxCols && Math.abs(r.changes - me.changes) <= 1 && r.side === me.side && !!r.hscroll === !!me.hscroll && Math.abs(r.roundShare - me.roundShare) <= CLONE)
      notes.push(`참고 한 곳과 거의 같은 뼈대: ${r.name} — 그 사이트를 옮겨 그린 것인지 확인하고 컨셉으로 바꿀 것`);
  }
  // 폰은 다 한 줄로 쌓여 뼈대로는 못 가른다 — 생김새(옆으로 넘기는 사진·단추 모양·사진 모서리·칸 넓이)가 참고 한 곳과 같으면 그 화면을 옮긴 것
  // (마당집 카페: 네모를 풀라는 말에 네이버 지도 화면의 둥근 사진 띠 + 알약 단추를 그대로 옮겨 「네이버랑 똑같다」)
  const roundPhoto = (r) => r.photoRad != null && r.photoRad >= PHOTO_ROUND;
  const lookSeen = new Set();
  for (const r of others.filter(() => me && me.stack >= 0.9))
    if (!lookSeen.has(r.host) && lookSeen.add(r.host) && !!r.hscroll === !!me.hscroll && r.btnShape === me.btnShape && roundPhoto(r) === roundPhoto(me) && r.hscroll > 0)
      notes.push(`참고 한 곳과 같은 생김새(폰): ${r.name} — 모양을 피하려고 다른 곳을 옮겨 오지 말고, 이 가게의 얼굴(사진·이름·자랑거리)에서 다시 잡을 것`);
  for (const p of rows.filter((r) => me && prev.includes(r.name) && !(me.stack >= 0.9 && r.stack >= 0.9))) { // 둘 다 한 줄로 쌓인 폰 화면은 늘 같아서 경고가 늘 떴다 — 폰은 생김새 비교로
    if (Math.abs(p.stack - me.stack) <= SAME_STACK && p.side === me.side && !!p.hscroll === !!me.hscroll && Math.abs(p.roundShare - me.roundShare) <= SAME_STACK)
      notes.push(`이전 시안과 같은 틀: ${p.name}(한 단 ${pct(p.stack)}, 둥근 ${pct(p.roundShare)}) — 컨셉·참고에서 뼈대를 다시 잡을 것`);
  }
  // 참고 공통점 — 바탕(의뢰인이 고른 템플릿)을 어디서 바꿀지 정하는 근거. 공통점만으로 짜면 어느 업종이든 같은 평균 웹사이트가 나왔다(사용자 2026-11-05).
  if (refs.length >= 2) {
    // 한 사이트(같은 주소)의 여러 쪽은 한 곳으로 센다 — 네이버 지도 가게 셋이 한 틀이라 「4/7곳」으로 공통점을 끌고 갔다
    const hosts = [...new Set(refs.map((r) => r.host))];
    const hostHas = (f) => hosts.filter((h) => { const pg = refs.filter((r) => r.host === h); return pg.filter(f).length * 2 >= pg.length; }).length;
    const half = (f) => hostHas(f) >= Math.ceil(hosts.length / 2);
    const cnt = (f) => `${hostHas(f)}/${hosts.length}곳`; // 몇 곳 중 몇 곳인지 함께 — 「일곱 곳 공통」처럼 넉넉하게 말하지 않게
    const st = refs.map((r) => r.stack).sort((a, b) => a - b), mc = refs.map((r) => r.maxCols).sort((a, b) => a - b);
    const common = [`한 단 세로 나열 ${pct(st[0])}~${pct(st[st.length - 1])}(가운데 ${pct(st[Math.floor(st.length / 2)])})`, `가장 많은 단 가운데 ${mc[Math.floor(mc.length / 2)]}`];
    const traits = [["navTop", "맨 위 메뉴 줄"], ["heroPhoto", "첫 화면이 큰 사진"], ["searchFirst", "첫 화면에 검색창"], ["callEnd", "끝에 전화·연락"], ["side", "옆에 붙은 안내판"], ["hscroll", "옆으로 넘기는 띠"]];
    for (const [k, label] of traits) if (half((r) => r[k])) common.push(`${label} (${cnt((r) => r[k])})`);
    if (half((r) => r.maxCols >= 3)) common.push(`3단 이상 칸이 있음 (${cnt((r) => r.maxCols >= 3)})`);
    if (half((r) => r.changes >= 4)) common.push(`내려가며 단 수가 자주 바뀜 (${cnt((r) => r.changes >= 4)})`);
    // 모양은 부품마다 따로 — 「큰 상자가 각지다」를 「전부 모서리 0」으로 읽지 않게
    const bs = refs.map((r) => r.boxShare).sort((a, b) => a - b);
    common.push(`종이 위 바탕·테두리 칸 넓이 ${pct(bs[0])}~${pct(bs[bs.length - 1])}(가운데 ${pct(bs[Math.floor(bs.length / 2)])}) — 적으면 「큰 상자 없이 흰 바탕에 글·사진·줄」이라는 뜻이지, 상자를 네모로 그리라는 뜻이 아님`);
    if (half((r) => r.roundShare > 0.1)) common.push(`둥근 큰 상자 (${cnt((r) => r.roundShare > 0.1)})`);
    const withPhoto = refs.filter((r) => r.photoRad != null);
    if (withPhoto.length) common.push(`사진 모서리: 둥긂 ${cnt((r) => r.photoRad != null && r.photoRad >= PHOTO_ROUND)}, 각짐 ${cnt((r) => r.photoRad != null && r.photoRad < PHOTO_ROUND)}`);
    const shapeCnt = {}; for (const k of ["알약", "둥근", "각진"]) { const n = hostHas((r) => r.btnShape === k); if (n) shapeCnt[k] = n; }
    common.push(`단추 모양: ${Object.entries(shapeCnt).map(([k, n]) => `${k} ${n}곳`).join(", ") || "단추 없음"} (/${hosts.length}) · 폭 가득 단추 있는 곳 ${cnt((r) => r.wideBtn > 0)}`);
    // 사진 모서리·단추 모양은 판정하지 않는다(사용자 2026-11-04 「직사각형을 너무 의식해서 오히려 AI 티」): 네모를 피하라는 말에 둥글게 바꾸면 그게 또 만든 티이고,
    // 다수 쪽 모양으로 맞추면 그 사이트를 옮긴 것이 된다. 모양은 가게 얼굴(사진·이름·자랑거리)에 맞춰 고르고, 걸러 낼 것은 칸이 쌓이는 것뿐.
    if (me && me.boxShare > bs[bs.length - 1] + BOX_OVER) notes.push(`상자 위에 상자: 우리 종이 위 칸 넓이 ${pct(me.boxShare)} — 참고는 ${pct(bs[0])}~${pct(bs[bs.length - 1])}. 칸 바탕·테두리를 걷어 흰 바탕에 줄·여백으로 나눌 것`);
    const ns = refs.map((r) => r.nestShare).sort((a, b) => a - b);
    if (me && me.nestShare > ns[ns.length - 1] + BOX_OVER / 3) notes.push(`칸 속 칸: 우리 ${pct(me.nestShare)} — 참고 가장 많은 곳 ${pct(ns[ns.length - 1])}. 바탕 칸 안에 또 흰 칸을 넣지 말 것`);
    // 배치 순서 공통점: 자리마다 절반 넘게 같은 것
    const seq = [];
    for (let i = 0; i < 6; i++) {
      const cnt = {}; for (const r of refs) if (r.order[i]) cnt[r.order[i]] = (cnt[r.order[i]] || 0) + 1;
      const top = Object.entries(cnt).sort((a, b) => b[1] - a[1])[0];
      if (!top || top[1] < Math.ceil(refs.length / 2)) break;
      seq.push(top[0]);
    }
    if (seq.length) common.push(`위에서부터 배치: ${seq.join(" → ")} (자리마다 절반 넘게 같은 것만 — 모든 곳 공통이 아님)`);
    const only = [...new Set(refs.flatMap((r) => traits.filter(([k]) => r[k] && !half((x) => x[k])).map(([, l]) => `${r.name}의 ${l}`)))];
    lines.push("", baseRow ? "## 참고 공통점 — 바탕을 바꿀 곳은 아래 「바탕과 다르게 할 곳」만" : "## 참고 공통점 — 바탕(--base)을 아직 안 골랐다면 의뢰인이 고르게 하고 다시 잴 것", "(짜임만 잰다. 영업시간·접수 마감·전화를 한 덩어리로 두는 것 같은 내용 짜임은 화면을 보고 따로 적는다)", ...common.map((c) => `- ${c}`));
    if (only.length) lines.push("", `절반이 안 되는 곳에만 있는 것(공통이 아님 — 쓰려면 이유를 대고 이름으로): ${only.join(", ")}`);
    if (me && !baseRow && (me.stack < st[0] - DIFF_STACK || me.stack > st[st.length - 1] + DIFF_STACK)) notes.push(`공통 범위 밖: 우리 한 단 ${pct(me.stack)} — 참고 ${pct(st[0])}~${pct(st[st.length - 1])}`);
  }
  if (baseRow && others.length) {
    const d = baseDiff(baseRow, others, me);
    lines.push("", `## 바탕(${base})과 다르게 할 곳 — 관련 사이트 여럿이 함께 다르게 하는 것만`, ...(d.changes.length ? d.changes.map((c) => `- ${c.text}`) : ["- 없음 — 바탕을 그대로 따른다"]),
      `(나머지는 바탕을 따른다: ${d.keep.join(", ")}. 글·사진·로고는 우리 것으로)`);
    notes.push(...d.notes);
  }
  lines.push("", "## 판정", notes.length ? notes.map((n) => `- ${n}`).join("\n") : "- 걸린 것 없음");
  writeFileSync(out, lines.join("\n") + "\n", "utf8");
  console.log(lines.slice(-Math.max(1, notes.length)).join("\n"));
}

main().catch((err) => {
  console.error(`오류: ${err.message}`);
  process.exit(1);
});
