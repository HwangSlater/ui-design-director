#!/usr/bin/env node
// 화면을 띄워 짜임 특징(회색 한 줄·윗줄·띠·카드·펼침 질문·단추·사진 비율·끝 띠·큰 숫자 칸·바탕색)을 잰다.
// 세 쪽 비교(저장소 scripts/triad.mjs)와 보내기 전 점검(preflight.py)이 같은 잣대를 쓰게 한 곳에 둔다 —
// 판정 도구와 점검이 따로 재서 점검은 통과하고 판정에서 떨어지는 일이 되풀이됐다(빵집 32~36차).
//   node page_probe.mjs --check <project folder>   # 바탕(바탕-구성.md 「주소:」)과 우리 시안을 390·1280 에서 재서 바탕보다 넘치거나 모자란 것만 DRIFT 로
// 바탕 값은 formats/바탕-표지.json 의 "probe" 에 남겨 두고 다시 쓴다(사본을 지운 뒤에도, 다시 재지 않게).
import { existsSync, readFileSync, writeFileSync } from "node:fs";
import { join, resolve } from "node:path";
import { pathToFileURL } from "node:url";
import { evaluate, goto, isMain, launch, openPage, scrollWakeExpr, sleep, HIDE_OVERLAYS } from "./browser.mjs";

export const SETTLE_MS = 3000;
const MAX_PAGE = 12000;
const LEAD_MAX = 45;      // 제목 바로 밑 이 글자 수 이하의 한 줄 = 「회색 한 줄 설명」
const CARD_RADIUS = 12;   // 이 이상 둥근 채운·테두리 상자 = 둥근 카드
const CARD_AREA = 20000;
const BAND_MIN_H = 200;   // 진한 띠로 셀 최소 높이(px)
export const NEAR = 0.15;
export const INFO_ONLY = new Set(["제목글꼴수", "제목본문같은글꼴", "제목수"]);
export const EXACT = new Set(["옅은띠", "진한띠", "제목위윗줄", "첫화면가운데사진위", "큰숫자칸", "끝단추띠"]);
// 방향: 상자·띠·되풀이는 바탕보다 많을 때만, 사진은 바탕보다 적을 때만 문제 — 23차에 바탕보다 적은 카드·질문을 「오답지 쪽」으로 셌다
export const BAD_IF_MORE = new Set(["첫화면가운데사진위", "둥근카드", "펼침질문", "단추", "진한띠", "옅은띠", "회색한줄", "제목위윗줄", "같은짜임잇달음", "큰숫자칸", "끝단추띠"]);
export const BAD_IF_LESS = new Set(["사진비율"]);  // 잡음 거르기 없이 견준다  // 표에는 싣되 통과 판정에는 넣지 않는다        // 세 값의 차가 이보다 작으면(상대) 「비슷」

// 페이지 안에서 도는 측정 — 짜임 특징
export const PROBE = `(() => {
  const W = innerWidth, H = innerHeight, PH = Math.min(document.documentElement.scrollHeight, ${MAX_PAGE});
  const rgb = (s) => { const m = (s || "").match(/[\\d.]+/g); return m ? m.map(Number) : null; };
  const lum = (c) => (0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]) / 255;
  const vis = (el) => { const cs = getComputedStyle(el); return cs.display !== "none" && cs.visibility !== "hidden" && Number(cs.opacity) > 0; };
  // 페이지 바탕색: 페이지를 내려가며 화면 여러 점에 실제로 보이는 바탕 — body 값이나 폭 가득 칸만 보면
  // 성심당(크라프트 종이 무늬·크림 칸, body 는 흰색)을 흰 바탕으로 쟀다(빵집 36차). 사진·무늬 그림 위 점은 그 칸의 바탕색으로
  const pageBg = (() => {
    const area = {}, y0 = scrollY, total = Math.min(document.documentElement.scrollHeight, ${MAX_PAGE});
    for (let y = 0; y < total; y += 300) {
      scrollTo(0, y);
      for (const fx of [0.04, 0.5, 0.96]) {
        let e = document.elementFromPoint(W * fx, Math.min(H - 2, 150));
        while (e && e !== document.documentElement) {
          const cs = getComputedStyle(e), c = rgb(cs.backgroundColor);
          if (["IMG", "VIDEO", "PICTURE", "CANVAS"].includes(e.tagName)) { e = null; break; }
          if (c && (c[3] ?? 1) > 0.5) break;
          if (cs.backgroundImage !== "none" && e.getBoundingClientRect().width >= W * 0.9) break;  // 종이 무늬 같은 바탕 그림
          e = e.parentElement;
        }
        if (!e) continue;
        const cs = e === document.documentElement ? getComputedStyle(document.body) : getComputedStyle(e);
        let c = rgb(cs.backgroundColor);
        if ((!c || (c[3] ?? 1) <= 0.5) && cs.backgroundImage !== "none") c = [240, 230, 210];  // 무늬 바탕은 밝은 종이색으로 셈
        if (!c || (c[3] ?? 1) <= 0.5) c = [255, 255, 255];
        const k = c.slice(0, 3).map((v) => Math.round(v / 4) * 4).join(","); area[k] = (area[k] || 0) + 1;
      }
    }
    scrollTo(0, y0);
    const top = Object.entries(area).sort((a, b) => b[1] - a[1])[0];
    return top ? top[0].split(",").map(Number) : [255, 255, 255];
  })();
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
  let cards = 0, bands = 0, pale = 0, ctas = 0; const btnCols = {};
  const GRID = 16, gw = Math.ceil(W / GRID), gh = Math.ceil(PH / GRID), cover = new Uint8Array(gw * gh);
  for (const el of document.querySelectorAll("body *")) {
    if (!vis(el)) continue;
    const r = el.getBoundingClientRect(), top = r.top + scrollY; if (top > PH || !r.width) continue;
    const cs = getComputedStyle(el), bg = rgb(cs.backgroundColor), filled = bg && (bg[3] ?? 1) > 0.5;
    // 사진은 칸 격자에 칠해 겹친 곳은 한 번만, 화면 밖(넘기는 띠의 숨은 장)은 빼고 센다 — 넓이를 더하니 맥파이가 3.75 로 나왔다(맥주집 40차)
    if (["IMG", "VIDEO", "PICTURE"].includes(el.tagName) || /url\\(/.test(cs.backgroundImage)) {
      const x0 = Math.max(0, Math.floor(r.left / GRID)), x1 = Math.min(gw, Math.ceil(r.right / GRID));
      const y0 = Math.max(0, Math.floor(top / GRID)), y1 = Math.min(gh, Math.ceil((top + r.height) / GRID));
      for (let y = y0; y < y1; y++) for (let x = x0; x < x1; x++) cover[y * gw + x] = 1;
      continue;
    }
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
    펼침질문: acc, 둥근카드: cards, 진한띠: bands, 단추: ctas, 사진비율: cover.reduce((a, v) => a + v, 0) / cover.length, 첫화면가운데사진위: heroCentredOnPhoto ? 1 : 0,
    같은짜임잇달음: best, 제목위윗줄: eyebrow, 옅은띠: pale, 큰숫자칸: stats, 끝단추띠: closing,
    바탕색: pageBg.slice(0, 3), 단추색: (Object.entries(btnCols).sort((a, b) => b[1] - a[1])[0]?.[0] || "255,255,255").split(",").map(Number) };
})()`;

export async function measure(port, width, url) {
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

const HEADING_KEYS = new Set(["회색한줄", "제목위윗줄"]);
const MARKS = join("formats", "바탕-표지.json");
const PHOTO_RATIO = 0.85;
const LABEL = { 회색한줄: "제목 밑 회색 한 줄", 제목위윗줄: "제목 위 작은 윗줄", 옅은띠: "옅은 띠", 진한띠: "진한 띠", 끝단추띠: "끝 단추 띠",
  큰숫자칸: "큰 숫자 칸", 둥근카드: "둥근 카드", 펼침질문: "펼침 질문", 단추: "채운 단추", 같은짜임잇달음: "같은 짜임 잇달음" };

function readJson(p) { try { return JSON.parse(readFileSync(p, "utf8")); } catch { return {}; } }

/** 바탕 값과 우리 값을 견줘 걸리는 줄 — 바탕보다 넘치는 것(상자·띠·되풀이), 사진은 바탕의 85% 아래, 흰 바탕에 크림 */
export function driftLines(width, base, ours) {
  const out = [];
  for (const key of BAD_IF_MORE) {
    // 바탕이 제목 태그(h1·h2)를 안 쓰면 제목에 붙는 항목은 견줄 것이 없다 — 세탁특공대가 0개라 「바탕 0개」로 잘못 걸었다(자전거 38차)
    if (HEADING_KEYS.has(key) && !base.제목수) continue;
    const tol = EXACT.has(key) || key === "회색한줄" ? 0 : 1;
    if (ours[key] > base[key] + tol) out.push(`DRIFT ${width}px ${key} — ${LABEL[key] || key} ${ours[key]}개(바탕 ${base[key]}개) — 바탕에 없는 만큼 걷어 낸다(build-rules.md § What reads as generated)`);
  }
  if (base.사진비율 > 0.05 && ours.사진비율 < base.사진비율 * PHOTO_RATIO) out.push(`DRIFT ${width}px 사진비율 — 사진 ${ours.사진비율.toFixed(2)}(바탕 ${base.사진비율.toFixed(2)}) — 바탕의 85% 넘게 사진으로`);
  const white = (c) => c.every((v) => v >= 248), cream = (c) => !white(c) && c[0] >= 235 && c[0] - c[2] >= 12;
  // 어두운 바탕(먹색 페이지)인데 우리는 밝은 바탕 — 또는 그 반대(맥주집 41차: Other Half #181c1c 에 흰 바탕)
  const lum = (c) => (0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]) / 255;
  if ((lum(base.바탕색) < 0.25) !== (lum(ours.바탕색) < 0.25)) out.push(`DRIFT ${width}px 바탕밝기 — 바탕 페이지는 ${lum(base.바탕색) < 0.25 ? "어두운" : "밝은"} 바탕(rgb(${base.바탕색.join(",")}))인데 우리는 ${lum(ours.바탕색) < 0.25 ? "어두운" : "밝은"} 바탕 — 페이지 바탕의 밝기는 바탕을 따른다`);
    if (white(base.바탕색) && cream(ours.바탕색)) out.push(`DRIFT ${width}px 바탕색 — 바탕은 흰 바탕인데 우리는 크림 rgb(${ours.바탕색.join(",")}) — 페이지 바탕은 흰색으로`);
  return out;
}

async function check(root) {
  const plan = existsSync(join(root, "formats", "바탕-구성.md")) ? readFileSync(join(root, "formats", "바탕-구성.md"), "utf8") : "";
  const url = (plan.match(/주소\s*[:：]\s*(https?:\/\/\S+)/) || [])[1];
  const page = join(root, "mockups", "index.html");
  if (!url || !existsSync(page)) { console.log("짜임 재기 못 함: 바탕 주소(formats/바탕-구성.md 「주소:」) 또는 mockups/index.html 없음"); return 0; }
  const marks = readJson(join(root, MARKS));
  const cached = marks.probe && marks.probe.url === url ? marks.probe : { url, widths: {} };
  const { port, close } = await launch("probe-");
  const lines = [];
  try {
    for (const w of [390, 1280]) {
      const base = cached.widths[w] || (cached.widths[w] = await measure(port, w, url));
      const ours = await measure(port, w, pathToFileURL(resolve(page)).href);
      lines.push(...driftLines(w, base, ours));
    }
  } finally { await close(); }
  if (existsSync(join(root, "formats"))) writeFileSync(join(root, MARKS), JSON.stringify({ ...marks, probe: cached }, null, 1), "utf8");
  for (const l of lines) console.log(l);
  if (lines.length) console.log("고칠 곳: 위 줄은 바탕과 같은 화면을 같은 브라우저로 잰 값이에요. 넘겨 달라고 묻지 말고 페이지를 고친 뒤 preflight.py 를 다시 돌려요.");
  return lines.length ? 1 : 0;
}

if (isMain(import.meta.url)) {
  const i = process.argv.indexOf("--check");
  if (i < 0 || !process.argv[i + 1]) { console.error("사용: node page_probe.mjs --check <project folder>"); process.exit(2); }
  check(resolve(process.argv[i + 1])).then((c) => process.exit(c)).catch((e) => { console.error(`ERROR: ${e.message}`); process.exit(1); });
}
