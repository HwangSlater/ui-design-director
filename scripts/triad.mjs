#!/usr/bin/env node
// 오답지·정답지·우리 것 — 세 페이지를 같은 잣대로 재서 「우리 것이 바탕보다 AI 시안을 닮은 곳」을 찾는다.
//   오답지: 스킬 없이 AI 가 만든 시안, 정답지: 바탕 실제 사이트, 우리 것: 스킬로 만든 시안.
//   사용자 제안(2026-11-10): 「오답지, 정답지, 우리가 구현해야 할 것 세 종류로 계속 배우면서 고치자」.
// 사용: node scripts/triad.mjs <out.md> base=<주소> ours=<주소|파일> ai=<주소|파일> [--width 390,1280] [--label <회차>]
//   결과 표를 out.md 에 쓰고, 같은 폴더의 「세-쪽-기록.json」에 회차마다 한 줄씩 쌓는다(어느 항목이 자주 오답지 쪽인지 보려고).
// 외부 패키지 없음 — 스킬의 browser.mjs(Edge/Chrome DevTools 프로토콜)를 쓴다.
import { existsSync, readFileSync, writeFileSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { pathToFileURL } from "node:url";
import { evaluate, goto, isMain, launch, openPage, scrollWakeExpr, sleep, HIDE_OVERLAYS } from "../skills/ui-design-director/scripts/browser.mjs";

const SETTLE_MS = 3000;
const MAX_PAGE = 12000;
const LEAD_MAX = 45;      // 제목 바로 밑 이 글자 수 이하의 한 줄 = 「회색 한 줄 설명」
const CARD_RADIUS = 12;   // 이 이상 둥근 채운·테두리 상자 = 둥근 카드
const CARD_AREA = 20000;
const BAND_MIN_H = 200;   // 진한 띠로 셀 최소 높이(px)
const NEAR = 0.15;
const INFO_ONLY = new Set(["제목글꼴수", "제목본문같은글꼴", "제목수"]);
const EXACT = new Set(["옅은띠", "진한띠", "제목위윗줄", "첫화면가운데사진위", "큰숫자칸", "끝단추띠"]);
// 방향: 상자·띠·되풀이는 바탕보다 많을 때만, 사진은 바탕보다 적을 때만 문제 — 23차에 바탕보다 적은 카드·질문을 「오답지 쪽」으로 셌다
const BAD_IF_MORE = new Set(["둥근카드", "펼침질문", "단추", "진한띠", "옅은띠", "회색한줄", "제목위윗줄", "같은짜임잇달음", "큰숫자칸", "끝단추띠"]);
const BAD_IF_LESS = new Set(["사진비율"]);  // 잡음 거르기 없이 견준다  // 표에는 싣되 통과 판정에는 넣지 않는다        // 세 값의 차가 이보다 작으면(상대) 「비슷」

// 페이지 안에서 도는 측정 — 짜임 특징
const PROBE = `(() => {
  const W = innerWidth, H = innerHeight, PH = Math.min(document.documentElement.scrollHeight, ${MAX_PAGE});
  const rgb = (s) => { const m = (s || "").match(/[\\d.]+/g); return m ? m.map(Number) : null; };
  const lum = (c) => (0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]) / 255;
  const vis = (el) => { const cs = getComputedStyle(el); return cs.display !== "none" && cs.visibility !== "hidden" && Number(cs.opacity) > 0; };
  const pageBg = (() => { for (const el of [document.body, document.documentElement]) { const c = rgb(getComputedStyle(el).backgroundColor); if (c && (c[3] ?? 1) > 0.5) return c; } return [255, 255, 255]; })();
  const heads = [...document.querySelectorAll("h1,h2,h3")].filter(vis).filter((h) => h.getBoundingClientRect().top + scrollY < PH);
  const h2 = heads.filter((h) => h.tagName !== "H3");
  const centred = h2.filter((h) => getComputedStyle(h).textAlign === "center").length;
  let lead = 0;
  // 링크 칸(a) 안의 제목·설명은 구역 머리가 아니다(22차의 「네이버로 예약하기 →」 칸)
  for (const h of h2) { if (h.closest("a")) continue; let n = h.nextElementSibling; if (n && n.tagName === "P" && vis(n) && n.textContent.trim().length <= ${LEAD_MAX}) lead++; }
  const fonts = new Set(heads.map((h) => getComputedStyle(h).fontFamily.split(",")[0].replace(/["']/g, "").trim()));
  const bodyFont = getComputedStyle(document.body).fontFamily.split(",")[0].replace(/["']/g, "").trim();
  // 펼침 질문: details·aria-expanded 말고도 「?」로 끝나는 짧은 글을 누르게 한 줄(바탕 Barkbus 는 div 로 만들어 놓쳤다)
  // details 하나를 summary 와 둘로 세지 않는다(21차에서 6개를 11개로 셌다)
  const qs = new Set([...document.querySelectorAll("details, [aria-expanded]")].filter((e) => !e.closest("details") || e.tagName === "DETAILS"));
  for (const el of document.querySelectorAll("button, [role=button], div, li, h3, h4, p")) {
    const t = el.textContent.trim(); if (t.length < 4 || t.length > 80 || !/[?？]$/.test(t) || el.children.length > 3) continue;
    if (el.closest("details")) continue;
    if (getComputedStyle(el).cursor === "pointer" || el.closest("button,[role=button],[aria-expanded]")) qs.add(el.closest("button,[role=button],[aria-expanded]") || el);
  }
  const acc = qs.size;
  // 제목 위 작은 윗줄(「소소는 이렇게 해요」 같은 색 글자) — 오답지에 구역마다 있었다
  let eyebrow = 0;
  for (const h of h2) { const pr = h.previousElementSibling; if (pr && pr.textContent.trim().length <= 24 && parseFloat(getComputedStyle(pr).fontSize) < parseFloat(getComputedStyle(h).fontSize) * 0.6) eyebrow++; }
  let cards = 0, bands = 0, pale = 0, ctas = 0, photo = 0; const btnCols = {};
  for (const el of document.querySelectorAll("body *")) {
    if (!vis(el)) continue;
    const r = el.getBoundingClientRect(), top = r.top + scrollY; if (top > PH || !r.width) continue;
    const cs = getComputedStyle(el), bg = rgb(cs.backgroundColor), filled = bg && (bg[3] ?? 1) > 0.5;
    if (["IMG", "VIDEO", "PICTURE"].includes(el.tagName) || /url\\(/.test(cs.backgroundImage)) { photo += r.width * r.height; continue; }
    const radius = parseFloat(cs.borderTopLeftRadius) || 0, framed = parseFloat(cs.borderTopWidth) > 0;
    if ((filled || framed) && radius >= ${CARD_RADIUS} && r.width * r.height >= ${CARD_AREA} && r.width < W * 0.95) cards++;
    if (filled && lum(bg) < 0.32 && r.width >= W * 0.95 && r.height >= ${BAND_MIN_H}) bands++;
    // 옅은 띠: 폭 가득, 밝지만 페이지 바탕과 다른 색 판(22차 가격 구역 뒤 민트)
    if (filled && lum(bg) > 0.85 && Math.hypot(...bg.slice(0, 3).map((v, i) => v - pageBg[i])) > 12 && r.width >= W * 0.95 && r.height >= ${BAND_MIN_H}) pale++;
    if ((el.tagName === "A" || el.tagName === "BUTTON") && filled && Math.hypot(...bg.slice(0, 3).map((v, i) => v - pageBg[i])) > 40 && r.height >= 32 && r.height <= 80) { ctas++; const k = bg.slice(0, 3).map((v) => Math.round(v / 8) * 8).join(","); btnCols[k] = (btnCols[k] || 0) + 1; }
  }
  // 큰 숫자 칸: 형제 3개 이상이 각각 큰 숫자(본문의 2배 넘는 짧은 글)로 시작 — 「8명 · 주 3회 · 3명 · 6년」(수학학원 26차)
  const bodyPx = parseFloat(getComputedStyle(document.body).fontSize) || 16;
  let stats = 0;
  for (const par of document.querySelectorAll("body *")) {
    const kids = [...par.children].filter(vis); if (kids.length < 3 || kids.length > 6) continue;
    const big = kids.filter((k) => [...k.querySelectorAll("*")].concat(k).some((e) => { const t = e.childElementCount ? "" : e.textContent.trim();
      return t && t.length <= 8 && /[0-9]/.test(t) && parseFloat(getComputedStyle(e).fontSize) >= bodyPx * 2; }));
    if (big.length >= 3 && big.length >= kids.length - 1) { stats = Math.max(stats, big.length); }
  }
  // 끝 단추 띠: 바닥글(없으면 페이지 끝) 바로 위 400px 안에서 끝나는, 폭 절반 넘는 색 칸에 글과 단추 — 오답지의 마무리 꼴.
  // DOM 형제로 찾으면 바탕 RSM 의 안쪽으로 들인 초록 띠를 놓쳤다(수학학원 29차) — 화면 위치로 찾는다
  let closing = 0;
  const footEl = [...document.querySelectorAll("footer")].filter(vis).pop();
  const footTop = footEl ? footEl.getBoundingClientRect().top + scrollY : document.documentElement.scrollHeight;
  for (const e of document.querySelectorAll("section, div, aside")) {
    // 바닥글 안 맨 위에 둔 띠(RSM 「Learn more about our program.」)도 센다 — 링크 목록 덩어리(바닥 메뉴)는 아니다
    if (!vis(e) || e === footEl || e.querySelectorAll("a").length > 4) continue;
    const r = e.getBoundingClientRect(), bottom = r.bottom + scrollY, c = rgb(getComputedStyle(e).backgroundColor);
    if (!c || (c[3] ?? 1) <= 0.5 || Math.hypot(...c.slice(0, 3).map((v, i) => v - pageBg[i])) <= 30 || r.width < W * 0.5 || r.height > 500) continue;
    // 바닥글 태그가 없는 사이트(RSM)도 있어 「페이지 아래 30% 안, 바닥글보다 위」로 본다
    const fullH = document.documentElement.scrollHeight;
    if (r.top + scrollY < fullH * 0.7) continue;
    // 제목 태그 없이 div 글만 둔 띠도(RSM 의 evaluationCTA) — 단추를 뺀 글이 8자 넘으면 글이 있는 칸
    const btn = e.querySelector("a,button");
    if (btn && e.textContent.replace(btn.textContent, "").trim().length > 8) { closing = 1; break; }
  }
  // 첫 화면: 가장 큰 글이 가운데 정렬이고 사진 위에 있나
  let big = null; for (const h of heads) { const r = h.getBoundingClientRect(); if (r.top < H && (!big || parseFloat(getComputedStyle(h).fontSize) > parseFloat(getComputedStyle(big).fontSize))) big = h; }
  let heroCentredOnPhoto = false;
  if (big) {
    const br = big.getBoundingClientRect(), cx = br.left + br.width / 2, cy = br.top + br.height / 2;
    const under = document.elementsFromPoint(cx, cy).some((e) => ["IMG", "VIDEO", "PICTURE"].includes(e.tagName) || /url\\(/.test(getComputedStyle(e).backgroundImage));
    heroCentredOnPhoto = under && getComputedStyle(big).textAlign === "center";
  }
  // 구역 짜임 되풀이: 큰 덩어리마다 [제목 정렬, 회색 한 줄, 단추] 서명 — 같은 서명이 몇 번 잇달아 나오나
  const blocks = [...document.querySelectorAll("main > *, body > section, main section")].filter((b) => vis(b) && b.getBoundingClientRect().height > 200);
  const sig = blocks.map((b) => { const h = b.querySelector("h2,h3"); if (!h) return "-"; const n = h.nextElementSibling;
    // 제목 다음 첫 내용의 꼴(표·목록·사진·펼침·글)과 사진 수까지 넣는다 — 정렬·한 줄·단추만 보면 다른 구역도 같다고 셌다(애견미용 21차)
    const body = [...b.querySelectorAll("table, ul, ol, dl, img, picture, details, figure, p")].find((e) => e !== n && h.compareDocumentPosition(e) & 4);
    const imgs = b.querySelectorAll("img, picture").length;
    return [getComputedStyle(h).textAlign === "center" ? "가운데" : "왼쪽", n && n.tagName === "P" && n.textContent.trim().length <= ${LEAD_MAX} ? "한줄" : "",
      b.querySelector("a[class*=btn],button") ? "단추" : "", body ? body.tagName : "", imgs > 2 ? "사진여럿" : imgs ? "사진" : ""].join("·"); });
  let run = 1, best = 1; for (let i = 1; i < sig.length; i++) { if (sig[i] !== "-" && sig[i] === sig[i - 1]) { run++; best = Math.max(best, run); } else run = 1; }
  return { 제목수: h2.length, 제목가운데: h2.length ? centred / h2.length : 0, 회색한줄: lead, 제목글꼴수: fonts.size, 제목본문같은글꼴: fonts.size === 1 && fonts.has(bodyFont) ? 1 : 0,
    펼침질문: acc, 둥근카드: cards, 진한띠: bands, 단추: ctas, 사진비율: photo / (W * PH), 첫화면가운데사진위: heroCentredOnPhoto ? 1 : 0,
    같은짜임잇달음: best, 제목위윗줄: eyebrow, 옅은띠: pale, 큰숫자칸: stats, 끝단추띠: closing,
    바탕색: pageBg.slice(0, 3), 단추색: (Object.entries(btnCols).sort((a, b) => b[1] - a[1])[0]?.[0] || "255,255,255").split(",").map(Number) };
})()`;

const args = process.argv.slice(2);
const out = args[0];
const opt = (k, d) => (args.includes(k) ? args[args.indexOf(k) + 1] : d);
const widths = opt("--width", "390,1280").split(",").map(Number);
const label = opt("--label", "");
const pages = Object.fromEntries(args.filter((a) => /^(base|ours|ai)=/.test(a)).map((a) => {
  const i = a.indexOf("="), v = a.slice(i + 1);
  return [a.slice(0, i), /^https?:|^file:/.test(v) ? v : pathToFileURL(resolve(v)).href];
}));

async function measure(port, width, url) {
  const page = await openPage(port, { width, height: 900 });
  try {
    await goto(page.cdp, url);
    await sleep(SETTLE_MS);
    await evaluate(page.cdp, scrollWakeExpr(MAX_PAGE, 120), { awaitPromise: true });
    await sleep(SETTLE_MS / 2);
    await evaluate(page.cdp, HIDE_OVERLAYS);
    return await evaluate(page.cdp, PROBE);
  } finally { await page.close(); }
}

// 우리 값이 바탕(정답지)보다 오답지에 가까우면 「오답지 쪽」. 바탕과 오답지가 비슷하면 판단하지 않는다(가르는 잣대가 아님)
export function side(base, ours, ai, noisy = true) {
  if (Array.isArray(base)) {  // 색: RGB 거리 — 우리 색이 오답지 색에 더 가까우면 오답지 쪽
    const d = (a, b) => Math.hypot(...a.map((v, i) => v - b[i]));
    if (d(base, ai) < 30) return "가르지 못함";
    return d(ours, ai) < d(ours, base) ? "오답지 쪽" : "정답지 쪽";
  }
  const span = Math.max(Math.abs(base), Math.abs(ai), 1e-9);
  const all = Math.max(span, Math.abs(ours));
  // 잡음 거르기: 세 값이 모두 이 폭 안이면 다르다고 보지 않는다 — 단추 3·2·2, 제목 가운데 0.14·0·0 을 판정에 넣었다(애견미용 21차)
  // 띠·윗줄처럼 하나만 있어도 티가 나는 것은 거르지 않는다(22차 옅은 띠 0·1·1 을 놓쳤다)
  const tiny = !noisy ? 0 : Number.isInteger(base) && Number.isInteger(ours) && Number.isInteger(ai) ? 1 : 0.15;
  if (tiny && Math.max(base, ours, ai) - Math.min(base, ours, ai) <= tiny) return "가르지 못함";
  // 바탕·오답지 둘 다 없는데 우리만 많은 것 — 스킬 규칙이 덧붙인 것(애견미용 19차의 「회색 한 줄」 4번)
  if (Math.abs(base - ai) / all < NEAR) return Math.abs(ours - base) / all >= 0.5 ? "우리만 다름" : "가르지 못함";
  return Math.abs(ours - ai) < Math.abs(ours - base) ? "오답지 쪽" : "정답지 쪽";
}

async function main() {
  if (!out || !pages.base || !pages.ours || !pages.ai) {
    console.error("사용: node scripts/triad.mjs <out.md> base=<주소> ours=<주소|파일> ai=<주소|파일> [--width 390,1280] [--label 회차]");
    process.exit(2);
  }
  const { port, close } = await launch("triad-");
  const lines = [`# 세 쪽 비교${label ? ` — ${label}` : ""}`, "", `정답지(바탕): ${pages.base}`, `우리 것: ${pages.ours}`, `오답지(스킬 없는 AI): ${pages.ai}`, ""];
  const record = { at: new Date().toISOString(), label, widths: {} };
  try {
    for (const w of widths) {
      const v = {};
      for (const k of ["base", "ours", "ai"]) v[k] = await measure(port, w, pages[k]);
      lines.push(`## ${w}px`, "", "| 항목 | 정답지 | 우리 것 | 오답지 | 판정 |", "|---|---|---|---|---|");
      const rows = [];
      for (const key of Object.keys(v.base)) {
        // 바탕에 채운 단추가 없으면 단추색은 견줄 것이 없다(22차 준오헤어)
        if (key === "단추색" && !v.base.단추) { lines.push(`| ${key} | 없음 | - | - | 가르지 못함 |`); rows.push({ key, verdict: "가르지 못함" }); continue; }
        const f = (x) => (Array.isArray(x) ? "#" + x.map((n) => Math.min(255, n).toString(16).padStart(2, "0")).join("") : Number.isInteger(x) ? String(x) : x.toFixed(2));
        // 바탕에 제목(h2)이 없으면 제목 정렬은 견줄 것이 없다(22차 준오헤어)
        let verdict = key === "제목가운데" && !v.base.제목수 ? "가르지 못함" : side(v.base[key], v.ours[key], v.ai[key], !EXACT.has(key));
        if ((BAD_IF_MORE.has(key) && v.ours[key] <= v.base[key]) || (BAD_IF_LESS.has(key) && v.ours[key] >= v.base[key])) verdict = "정답지 쪽";
        rows.push({ key, verdict });
        lines.push(`| ${key} | ${f(v.base[key])} | ${f(v.ours[key])} | ${f(v.ai[key])} | ${verdict} |`);
      }
      // 글꼴 수는 참고만 — 한국 사이트는 한 글꼴로 다 쓰는 일이 흔해 AI 티를 가르지 못한다(애견미용 21차)
      const judged = rows.filter((r) => !INFO_ONLY.has(r.key));
      const wrong = judged.filter((r) => r.verdict === "오답지 쪽").map((r) => r.key);
      const odd = judged.filter((r) => r.verdict === "우리만 다름").map((r) => r.key);
      lines.push("", `오답지 쪽 ${wrong.length}개${wrong.length ? ": " + wrong.join(", ") : ""} · 우리만 다름 ${odd.length}개${odd.length ? ": " + odd.join(", ") : ""}`, "");
      record.widths[w] = { values: v, wrong, odd };
      console.log(`${w}px — 오답지 쪽 ${wrong.length}개${wrong.length ? ": " + wrong.join(", ") : ""} · 우리만 다름 ${odd.length}개${odd.length ? ": " + odd.join(", ") : ""}`);
    }
  } finally { await close(); }
  writeFileSync(out, lines.join("\n") + "\n", "utf8");
  const hist = join(dirname(resolve(out)), "세-쪽-기록.json");
  let list = []; try { list = existsSync(hist) ? JSON.parse(readFileSync(hist, "utf8")) : []; } catch { list = []; }
  list.push(record); writeFileSync(hist, JSON.stringify(list, null, 1), "utf8");
  console.log(`→ ${out}`);
}

if (isMain(import.meta.url)) main().catch((e) => { console.error(`ERROR: ${e.message}`); process.exit(1); });
