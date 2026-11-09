#!/usr/bin/env node
// 바탕 사이트의 「움직임」을 글과 전후 그림으로 남긴다 — AI 는 영상을 못 보니, 따라 만들 수 있는 숫자로.
// 사용: node motion.mjs <주소> <out.md> [--width 1280]
// 남기는 것: ① 전환(transition)·애니메이션 길이·곡선 묶음 ② 마우스 올림 전후 바뀌는 값(+ 전후 그림)
//   ③ 스크롤하면 바뀌는 머리(붙는지, 높이·바탕색) ④ 스크롤로 나타나는 요소 ⑤ 저절로 넘어가는 사진(몇 초마다)
// 그림은 <out.md> 옆 <이름>-움직임/ 에. 결과는 짐작이 아니라 브라우저가 계산한 값이다.
import { mkdirSync, writeFileSync } from "node:fs";
import { basename, dirname, join } from "node:path";
import { evaluate, goto, launch, openPage, scrollWakeExpr, sleep, HIDE_OVERLAYS } from "./browser.mjs";
import { requireStage } from "./stage_guard.mjs";

const SETTLE_MS = 2500, SCROLL_STEP_MS = 400, MAX_SCROLL = 12000;
const HOVER_MAX = 14;          // 마우스 올림을 볼 단추·링크 수(첫 화면에서)
const HOVER_SHOTS = 4;         // 그 가운데 전후 그림을 남길 수
const CAROUSEL_WAIT_MS = 4000; // 넘기는 사진을 이 간격으로 세 번 본다
const HEADER_AT = [0, 400, 1200]; // 머리를 볼 스크롤 위치(px)
const REVEAL_MAX = 600;        // 스크롤로 나타나는지 볼 아래쪽 요소 수
const PROPS = ["color", "background-color", "border-color", "box-shadow", "transform", "opacity", "text-decoration-line", "filter", "outline-color", "scale", "translate"];

// ── 페이지 안에서 도는 식 ──
// 첫 화면에 보이는 큰 그림·제목의 서명 — 몇 초 뒤 달라지면 저절로 넘어가는 것
const HERO_SIGNATURE = `(() => [...document.querySelectorAll("img, [style*='background-image'], h1, h2")]
  .filter((n) => {
    const r = n.getBoundingClientRect();
    return r.top < innerHeight && r.bottom > 0 && r.left < innerWidth && r.right > 0 && r.width * r.height > 20000;
  })
  .map((n) => (n.currentSrc || n.style.backgroundImage || n.textContent).slice(0, 80) + "@" + Math.round(n.getBoundingClientRect().left))
  .join("|"))()`;

// 전환·애니메이션을 「종류 | 무엇이 | 길이 | 곡선」 묶음으로 세어 많은 순 15개
const TRANSITION_GROUPS = `(() => {
  const m = new Map();
  const count = (k) => m.set(k, (m.get(k) || 0) + 1);
  for (const n of document.querySelectorAll("body *")) {
    const cs = getComputedStyle(n);
    const d = cs.transitionDuration;
    if (d && d !== "0s") count("전환 | " + cs.transitionProperty.slice(0, 60) + " | " + d + " | " + cs.transitionTimingFunction);
    if (cs.animationName && cs.animationName !== "none") {
      count("애니메이션 | " + cs.animationName.slice(0, 40) + " | " + cs.animationDuration + " | " + cs.animationTimingFunction + " | 반복 " + cs.animationIterationCount);
    }
  }
  return [...m].sort((a, b) => b[1] - a[1]).slice(0, 15);
})()`;

// 첫 화면의 단추·링크에 data-mo 번호를 붙이고 수를 돌려준다
const MARK_HOVER_TARGETS = `(() => {
  let i = 0;
  for (const el of document.querySelectorAll("a, button, [role=button], input[type=submit]")) {
    const r = el.getBoundingClientRect();
    if (r.top < 0 || r.bottom > innerHeight || r.width < 24 || r.height < 16) continue;
    el.setAttribute("data-mo", String(i));
    if (++i >= ${HOVER_MAX}) break;
  }
  return i;
})()`;

// data-mo 번호 i 인 요소의 볼 값·글·자리·전환 길이
const readHoverTarget = (i) => `(() => {
  const el = document.querySelector('[data-mo="${i}"]');
  const cs = getComputedStyle(el);
  const r = el.getBoundingClientRect();
  return {
    v: ${JSON.stringify(PROPS)}.map((p) => cs.getPropertyValue(p)),
    t: (el.innerText || el.getAttribute("aria-label") || el.tagName).trim().slice(0, 24),
    r: [r.left, r.top, r.width, r.height],
    dur: cs.transitionDuration,
  };
})()`;

// 맨 위에 붙은 머리 막대의 위치·높이·바탕(없으면 null)
const HEADER_STATE = `(() => {
  const els = [...document.querySelectorAll("header, nav, [class*=header i], [id*=header i]")].filter((e) => {
    const r = e.getBoundingClientRect();
    return r.top <= 4 && r.height > 20 && r.height < innerHeight / 2 && r.width > innerWidth * 0.6;
  });
  const e = els[0];
  if (!e) return null;
  const cs = getComputedStyle(e);
  const r = e.getBoundingClientRect();
  return { pos: cs.position, top: Math.round(r.top), h: Math.round(r.height), bg: cs.backgroundColor, shadow: cs.boxShadow !== "none", backdrop: cs.backdropFilter };
})()`;

// 첫 화면 아래쪽 요소에 data-mr 번호를 붙인다
const MARK_BELOW_FOLD = `(() => {
  let i = 0;
  for (const el of document.querySelectorAll("body *")) {
    const r = el.getBoundingClientRect();
    if (r.top < innerHeight * 1.2 || r.width * r.height < 6000) continue;
    el.setAttribute("data-mr", String(i));
    if (++i >= ${REVEAL_MAX}) break;
  }
  return i;
})()`;

// 번호 붙인 요소들의 투명도·이동·보임·전환
const BELOW_FOLD_STATE = `[...document.querySelectorAll("[data-mr]")].map((e) => {
  const cs = getComputedStyle(e);
  return [cs.opacity, cs.transform, cs.translate, cs.visibility, cs.transitionDuration, cs.transitionTimingFunction];
})`;

const args = process.argv.slice(2);
const wi = args.indexOf("--width"); const width = wi >= 0 ? Number(args.splice(wi, 2)[1]) : 1280;
const [url, outMd] = args;
if (!url || !outMd) { console.error("사용: node motion.mjs <주소> <out.md> [--width 1280]"); process.exit(2); }
requireStage(outMd); // 스킬 프로젝트 formats/ 안이면 바탕 확정 뒤에만(바탕 자료) — 밖이면 그대로
const shotDir = join(dirname(outMd), basename(outMd, ".md") + "-움직임");

const ev = (cdp, expression, awaitPromise = false) => evaluate(cdp, expression, { awaitPromise });
const secs = (ms) => ms / 1000;

// ⑤ 저절로 넘어가는 사진: 첫 화면을 몇 초 간격으로 세 번 보고 바뀐 큰 그림·글을 센다
async function carousel(cdp, md) {
  const sigs = [];
  for (let i = 0; i < 3; i++) { sigs.push(await ev(cdp, HERO_SIGNATURE)); if (i < 2) await sleep(CAROUSEL_WAIT_MS); }
  const changes = sigs.slice(1).filter((s, i) => s !== sigs[i]).length;
  const said = changes
    ? `첫 화면의 큰 그림·글이 ${secs(CAROUSEL_WAIT_MS)}초 간격 두 번 중 ${changes}번 바뀜 — 약 ${secs(CAROUSEL_WAIT_MS)}초 안팎으로 넘어가는 사진·배너가 있다.`
    : `${secs(CAROUSEL_WAIT_MS * 2)}초 동안 바뀌지 않음 — 저절로 넘기는 사진은 없거나 그보다 느리다.`;
  md.push("## 저절로 넘어가는 것(첫 화면)", "", said, "");
  return changes;
}

// ① 전환·애니메이션 묶음
async function transitions(cdp, md) {
  const tr = await ev(cdp, TRANSITION_GROUPS);
  const row = ([k, n]) => { const [kind, what, dur, ease, rep] = k.split(" | "); return `| ${kind} | ${what} | ${dur} | ${ease}${rep ? " · " + rep : ""} | ${n} |`; };
  md.push("## 전환·애니메이션(많이 쓴 순)", "", "| 종류 | 무엇이 | 길이 | 곡선 | 요소 수 |", "|---|---|---|---|---|", ...tr.map(row), "");
}

// ② 마우스 올림: 첫 화면 단추·링크에 :hover 를 걸어 바뀌는 값을 본다
async function hovers(cdp, md) {
  const n = await ev(cdp, MARK_HOVER_TARGETS);
  const { root } = await cdp.send("DOM.getDocument", { depth: 0 });
  const rows = []; let shots = 0;
  for (let i = 0; i < n; i++) {
    const { nodeId } = await cdp.send("DOM.querySelector", { nodeId: root.nodeId, selector: `[data-mo="${i}"]` });
    if (!nodeId) continue;
    const before = await ev(cdp, readHoverTarget(i));
    const [cx, cy] = [before.r[0] + before.r[2] / 2, before.r[1] + before.r[3] / 2];
    const hoverOn = async () => { await cdp.send("CSS.forcePseudoState", { nodeId, forcedPseudoClasses: ["hover"] }); await cdp.send("Input.dispatchMouseEvent", { type: "mouseMoved", x: cx, y: cy }); };
    const hoverOff = async () => { await cdp.send("CSS.forcePseudoState", { nodeId, forcedPseudoClasses: [] }); await cdp.send("Input.dispatchMouseEvent", { type: "mouseMoved", x: 1, y: 1 }); };
    await hoverOn();
    await sleep(Math.min(1500, 400 + 1000 * Math.max(...before.dur.split(",").map((d) => parseFloat(d) * (d.includes("ms") ? 0.001 : 1) || 0))));
    const after = await ev(cdp, readHoverTarget(i));
    const diff = PROPS.map((p, k) => (before.v[k] !== after.v[k] ? `${p}: ${before.v[k]} → ${after.v[k]}` : null)).filter(Boolean);
    if (diff.length) {
      let pic = "";
      if (shots < HOVER_SHOTS) {
        const [x, y, w, h] = before.r, pad = 24, clip = { x: Math.max(0, x - pad), y: Math.max(0, y - pad), width: w + pad * 2, height: h + pad * 2, scale: 1 };
        await hoverOff(); await sleep(600);
        const a = await cdp.send("Page.captureScreenshot", { format: "png", clip });
        await hoverOn(); await sleep(600);
        const b = await cdp.send("Page.captureScreenshot", { format: "png", clip });
        writeFileSync(join(shotDir, `올림-${i}-전.png`), Buffer.from(a.data, "base64")); writeFileSync(join(shotDir, `올림-${i}-후.png`), Buffer.from(b.data, "base64"));
        pic = ` (그림: 올림-${i}-전/후.png)`; shots++;
      }
      rows.push(`| ${before.t.replace(/\|/g, "/")} | ${diff.join("<br>")} | ${before.dur} |${pic ? " " + pic.trim() : ""}`);
    }
    await hoverOff(); await sleep(200);
  }
  const table = rows.length ? ["|---|---|---|---|", ...rows.map((r) => (r.split("|").length < 6 ? r + " |" : r))] : [];
  md.push("## 마우스 올림(첫 화면 단추·링크)", "", rows.length ? "| 무엇 | 바뀌는 값 | 전환 길이 | 그림 |" : `첫 화면 단추·링크 ${n}개 가운데 마우스를 올려 바뀌는 것이 없음.`, ...table, "");
  return shots;
}

// ③ 머리: 스크롤 위치마다 맨 위 막대의 위치·높이·바탕
async function header(cdp, md) {
  const hs = [];
  for (const y of HEADER_AT) { await ev(cdp, `scrollTo(0, ${y})`); await sleep(900); hs.push([y, await ev(cdp, HEADER_STATE)]); }
  const row = ([y, h]) => (h ? `| ${y}px | 맨 위 ${h.top}px | ${h.pos} | ${h.h}px | ${h.bg} | ${h.shadow ? "있음" : "없음"} | ${h.backdrop} |` : `| ${y}px | 맨 위에 머리 없음 | | | | | |`);
  md.push("## 머리(스크롤 위치마다)", "", "| 스크롤 | 보임 | 붙는 방식 | 높이 | 바탕 | 그림자 | 흐림 |", "|---|---|---|---|---|---|---|", ...hs.map(row), "");
  await ev(cdp, "scrollTo(0, 0)"); await sleep(500);
}

// ④ 스크롤로 나타나는 것: 아래쪽 요소의 투명도·위치를 내리기 전과 후에 비교
async function reveals(cdp, md) {
  await ev(cdp, MARK_BELOW_FOLD); const pre = await ev(cdp, BELOW_FOLD_STATE);
  await ev(cdp, scrollWakeExpr(MAX_SCROLL, SCROLL_STEP_MS, { stride: 0.5, toTop: false }), true);
  await sleep(1200); const post = await ev(cdp, BELOW_FOLD_STATE);
  const revealed = pre.map((p, i) => [p, post[i]]).filter(([a, b]) => b && (a[0] !== b[0] || a[1] !== b[1] || a[2] !== b[2] || a[3] !== b[3]));
  const kinds = new Map();
  for (const [a, b] of revealed) {
    const k = `투명도 ${a[0]}→${b[0]} · 이동 ${a[1] === b[1] ? "없음" : a[1].slice(0, 40) + "→" + b[1].slice(0, 20)} · ${b[4]} ${b[5]}`;
    kinds.set(k, (kinds.get(k) || 0) + 1);
  }
  const said = revealed.length
    ? `첫 화면 아래 요소 ${pre.length}개 가운데 ${revealed.length}개가 내리면서 바뀜:`
    : `첫 화면 아래 요소 ${pre.length}개 가운데 내리면서 바뀌는 것이 없음 — 나타나는 효과 없이 그대로 놓인다.`;
  md.push("## 스크롤로 나타나는 것", "", said, "", ...[...kinds].sort((a, b) => b[1] - a[1]).slice(0, 8).map(([k, c]) => `- ${k} — ${c}개`), "");
  return revealed.length;
}

async function main() {
  mkdirSync(shotDir, { recursive: true });
  const { port, close } = await launch("motion-");
  let page = null;
  try {
    page = await openPage(port, { width, scale: 2 });
    const { cdp } = page;
    await cdp.send("DOM.enable"); await cdp.send("CSS.enable");
    await goto(cdp, url); await sleep(SETTLE_MS);
    await ev(cdp, HIDE_OVERLAYS);
    const md = [`# 움직임 — ${url} (${width}px)`, "", "브라우저가 계산한 값. 시안은 이 값을 그대로 쓰고, 없는 움직임을 지어 넣지 않는다.", ""];
    const changes = await carousel(cdp, md);
    await transitions(cdp, md);
    const shots = await hovers(cdp, md);
    await header(cdp, md);
    const revealed = await reveals(cdp, md);
    writeFileSync(outMd, md.join("\n") + "\n");
    console.log(`wrote ${outMd} · 올림 전후 그림 ${shots}쌍 · 나타남 ${revealed}개 · 넘김 ${changes ? "있음" : "없음"}`);
  } finally {
    await page?.close();
    await close();
  }
}

main().catch((err) => {
  console.error(`오류: ${err.message}`);
  process.exit(1);
});
