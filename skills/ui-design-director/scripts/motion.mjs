#!/usr/bin/env node
// 바탕 사이트의 「움직임」을 글과 전후 그림으로 남긴다 — AI 는 영상을 못 보니, 따라 만들 수 있는 숫자로.
// 사용: node motion.mjs <주소> <out.md> [--width 1280]
// 남기는 것: ① 전환(transition)·애니메이션 길이·곡선 묶음 ② 마우스 올림 전후 바뀌는 값(+ 전후 그림)
//   ③ 스크롤하면 바뀌는 머리(붙는지, 높이·바탕색) ④ 스크롤로 나타나는 요소 ⑤ 저절로 넘어가는 사진(몇 초마다)
// 그림은 <out.md> 옆 <이름>-움직임/ 에. 결과는 짐작이 아니라 브라우저가 계산한 값이다.
import { mkdirSync, writeFileSync } from "node:fs";
import { basename, dirname, join } from "node:path";
import { Cdp, launch, sleep, HIDE_OVERLAYS } from "./browser.mjs";

const DESKTOP_UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36 Edg/142.0.0.0";
const PHONE_UA = "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1";
const NAV_TIMEOUT_MS = 45000, SETTLE_MS = 2500, SCROLL_STEP_MS = 400, MAX_SCROLL = 12000;
const HOVER_MAX = 14;          // 마우스 올림을 볼 단추·링크 수(첫 화면에서)
const HOVER_SHOTS = 4;         // 그 가운데 전후 그림을 남길 수
const CAROUSEL_WAIT_MS = 4000; // 넘기는 사진을 이 간격으로 세 번 본다
const HEADER_AT = [0, 400, 1200]; // 머리를 볼 스크롤 위치(px)
const PROPS = ["color", "background-color", "border-color", "box-shadow", "transform", "opacity", "text-decoration-line", "filter", "outline-color", "scale", "translate"];

const args = process.argv.slice(2);
const wi = args.indexOf("--width"); const width = wi >= 0 ? Number(args.splice(wi, 2)[1]) : 1280;
const [url, outMd] = args;
if (!url || !outMd) { console.error("사용: node motion.mjs <주소> <out.md> [--width 1280]"); process.exit(2); }
const shotDir = join(dirname(outMd), basename(outMd, ".md") + "-움직임"); mkdirSync(shotDir, { recursive: true });
const phone = width <= 600;

const ev = async (cdp, expression, awaitPromise = false) => (await cdp.send("Runtime.evaluate", { expression, returnByValue: true, awaitPromise })).result.value;

const { proc, port } = await launch();
const target = await (await fetch(`http://127.0.0.1:${port}/json/new?about:blank`, { method: "PUT" })).json();
const cdp = await Cdp.open(target.webSocketDebuggerUrl);
const md = [];
try {
  await cdp.send("Page.enable"); await cdp.send("DOM.enable"); await cdp.send("CSS.enable");
  await cdp.send("Emulation.setDeviceMetricsOverride", { width, height: phone ? 844 : 900, deviceScaleFactor: 2, mobile: phone });
  await cdp.send("Emulation.setUserAgentOverride", { userAgent: phone ? PHONE_UA : DESKTOP_UA, acceptLanguage: "ko-KR,ko;q=0.9" });
  const loaded = cdp.waitFor("Page.loadEventFired", NAV_TIMEOUT_MS);
  await cdp.send("Page.navigate", { url }); await loaded; await sleep(SETTLE_MS);
  await ev(cdp, HIDE_OVERLAYS);
  md.push(`# 움직임 — ${url} (${width}px)`, "", "브라우저가 계산한 값. 시안은 이 값을 그대로 쓰고, 없는 움직임을 지어 넣지 않는다.", "");

  // ⑤ 저절로 넘어가는 사진: 첫 화면을 몇 초 간격으로 세 번 보고 바뀐 큰 그림·글을 센다
  const heroSig = `(() => [...document.querySelectorAll("img, [style*='background-image'], h1, h2")].filter((n) => { const r = n.getBoundingClientRect(); return r.top < innerHeight && r.bottom > 0 && r.left < innerWidth && r.right > 0 && r.width * r.height > 20000; }).map((n) => (n.currentSrc || n.style.backgroundImage || n.textContent).slice(0, 80) + "@" + Math.round(n.getBoundingClientRect().left)).join("|"))()`;
  const sigs = [];
  for (let i = 0; i < 3; i++) { sigs.push(await ev(cdp, heroSig)); if (i < 2) await sleep(CAROUSEL_WAIT_MS); }
  const changes = sigs.slice(1).filter((s, i) => s !== sigs[i]).length;
  md.push("## 저절로 넘어가는 것(첫 화면)", "", changes ? `첫 화면의 큰 그림·글이 ${CAROUSEL_WAIT_MS / 1000}초 간격 두 번 중 ${changes}번 바뀜 — 약 ${CAROUSEL_WAIT_MS / 1000}초 안팎으로 넘어가는 사진·배너가 있다.` : `${(CAROUSEL_WAIT_MS * 2) / 1000}초 동안 바뀌지 않음 — 저절로 넘기는 사진은 없거나 그보다 느리다.`, "");

  // ① 전환·애니메이션 묶음
  const tr = await ev(cdp, `(() => { const m = new Map(); for (const n of document.querySelectorAll("body *")) { const cs = getComputedStyle(n); const d = cs.transitionDuration; if (d && d !== "0s") { const k = "전환 | " + cs.transitionProperty.slice(0, 60) + " | " + d + " | " + cs.transitionTimingFunction; m.set(k, (m.get(k) || 0) + 1); } if (cs.animationName && cs.animationName !== "none") { const k = "애니메이션 | " + cs.animationName.slice(0, 40) + " | " + cs.animationDuration + " | " + cs.animationTimingFunction + " | 반복 " + cs.animationIterationCount; m.set(k, (m.get(k) || 0) + 1); } } return [...m].sort((a, b) => b[1] - a[1]).slice(0, 15); })()`);
  md.push("## 전환·애니메이션(많이 쓴 순)", "", "| 종류 | 무엇이 | 길이 | 곡선 | 요소 수 |", "|---|---|---|---|---|", ...tr.map(([k, n]) => { const [kind, what, dur, ease, rep] = k.split(" | "); return `| ${kind} | ${what} | ${dur} | ${ease}${rep ? " · " + rep : ""} | ${n} |`; }), "");

  // ② 마우스 올림: 첫 화면 단추·링크에 :hover 를 걸어 바뀌는 값을 본다
  const n = await ev(cdp, `(() => { let i = 0; for (const el of document.querySelectorAll("a, button, [role=button], input[type=submit]")) { const r = el.getBoundingClientRect(); if (r.top < 0 || r.bottom > innerHeight || r.width < 24 || r.height < 16) continue; el.setAttribute("data-mo", String(i)); if (++i >= ${HOVER_MAX}) break; } return i; })()`);
  const { root } = await cdp.send("DOM.getDocument", { depth: 0 });
  const rows = []; let shots = 0;
  for (let i = 0; i < n; i++) {
    const { nodeId } = await cdp.send("DOM.querySelector", { nodeId: root.nodeId, selector: `[data-mo="${i}"]` });
    if (!nodeId) continue;
    const read = `(() => { const el = document.querySelector('[data-mo="${i}"]'); const cs = getComputedStyle(el); const r = el.getBoundingClientRect(); return { v: ${JSON.stringify(PROPS)}.map((p) => cs.getPropertyValue(p)), t: (el.innerText || el.getAttribute("aria-label") || el.tagName).trim().slice(0, 24), r: [r.left, r.top, r.width, r.height], dur: cs.transitionDuration }; })()`;
    const before = await ev(cdp, read);
    const [cx, cy] = [before.r[0] + before.r[2] / 2, before.r[1] + before.r[3] / 2];
    const hoverOn = async () => { await cdp.send("CSS.forcePseudoState", { nodeId, forcedPseudoClasses: ["hover"] }); await cdp.send("Input.dispatchMouseEvent", { type: "mouseMoved", x: cx, y: cy }); };
    const hoverOff = async () => { await cdp.send("CSS.forcePseudoState", { nodeId, forcedPseudoClasses: [] }); await cdp.send("Input.dispatchMouseEvent", { type: "mouseMoved", x: 1, y: 1 }); };
    await hoverOn();
    await sleep(Math.min(1500, 400 + 1000 * Math.max(...before.dur.split(",").map((d) => parseFloat(d) * (d.includes("ms") ? 0.001 : 1) || 0))));
    const after = await ev(cdp, read);
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
  md.push("## 마우스 올림(첫 화면 단추·링크)", "", rows.length ? "| 무엇 | 바뀌는 값 | 전환 길이 | 그림 |" : `첫 화면 단추·링크 ${n}개 가운데 마우스를 올려 바뀌는 것이 없음.`, ...(rows.length ? ["|---|---|---|---|", ...rows.map((r) => (r.split("|").length < 6 ? r + " |" : r))] : []), "");

  // ③ 머리: 스크롤 위치마다 맨 위 막대의 위치·높이·바탕
  const head = `(() => { const els = [...document.querySelectorAll("header, nav, [class*=header i], [id*=header i]")].filter((e) => { const r = e.getBoundingClientRect(); return r.top <= 4 && r.height > 20 && r.height < innerHeight / 2 && r.width > innerWidth * 0.6; }); const e = els[0]; if (!e) return null; const cs = getComputedStyle(e); const r = e.getBoundingClientRect(); return { pos: cs.position, top: Math.round(r.top), h: Math.round(r.height), bg: cs.backgroundColor, shadow: cs.boxShadow !== "none", backdrop: cs.backdropFilter }; })()`;
  const hs = [];
  for (const y of HEADER_AT) { await ev(cdp, `scrollTo(0, ${y})`); await sleep(900); hs.push([y, await ev(cdp, head)]); }
  md.push("## 머리(스크롤 위치마다)", "", "| 스크롤 | 보임 | 붙는 방식 | 높이 | 바탕 | 그림자 | 흐림 |", "|---|---|---|---|---|---|---|", ...hs.map(([y, h]) => (h ? `| ${y}px | 맨 위 ${h.top}px | ${h.pos} | ${h.h}px | ${h.bg} | ${h.shadow ? "있음" : "없음"} | ${h.backdrop} |` : `| ${y}px | 맨 위에 머리 없음 | | | | | |`)), "");
  await ev(cdp, "scrollTo(0, 0)"); await sleep(500);

  // ④ 스크롤로 나타나는 것: 아래쪽 요소의 투명도·위치를 내리기 전과 후에 비교
  const mark = `(() => { let i = 0; for (const el of document.querySelectorAll("body *")) { const r = el.getBoundingClientRect(); if (r.top < innerHeight * 1.2 || r.width * r.height < 6000) continue; el.setAttribute("data-mr", String(i)); if (++i >= 600) break; } return i; })()`;
  const snap = `[...document.querySelectorAll("[data-mr]")].map((e) => { const cs = getComputedStyle(e); return [cs.opacity, cs.transform, cs.translate, cs.visibility, cs.transitionDuration, cs.transitionTimingFunction]; })`;
  await ev(cdp, mark); const pre = await ev(cdp, snap);
  await ev(cdp, `(async () => { for (let y = 0; y < Math.min(document.body.scrollHeight, ${MAX_SCROLL}); y += innerHeight / 2) { scrollTo(0, y); await new Promise((r) => setTimeout(r, ${SCROLL_STEP_MS})); } })()`, true);
  await sleep(1200); const post = await ev(cdp, snap);
  const revealed = pre.map((p, i) => [p, post[i]]).filter(([a, b]) => b && (a[0] !== b[0] || a[1] !== b[1] || a[2] !== b[2] || a[3] !== b[3]));
  const kinds = new Map(); for (const [a, b] of revealed) { const k = `투명도 ${a[0]}→${b[0]} · 이동 ${a[1] === b[1] ? "없음" : a[1].slice(0, 40) + "→" + b[1].slice(0, 20)} · ${b[4]} ${b[5]}`; kinds.set(k, (kinds.get(k) || 0) + 1); }
  md.push("## 스크롤로 나타나는 것", "", revealed.length ? `첫 화면 아래 요소 ${pre.length}개 가운데 ${revealed.length}개가 내리면서 바뀜:` : `첫 화면 아래 요소 ${pre.length}개 가운데 내리면서 바뀌는 것이 없음 — 나타나는 효과 없이 그대로 놓인다.`, "", ...[...kinds].sort((a, b) => b[1] - a[1]).slice(0, 8).map(([k, c]) => `- ${k} — ${c}개`), "");
  writeFileSync(outMd, md.join("\n") + "\n");
  console.log(`wrote ${outMd} · 올림 전후 그림 ${shots}쌍 · 나타남 ${revealed.length}개 · 넘김 ${changes ? "있음" : "없음"}`);
} finally {
  cdp.close(); proc.kill();
}
