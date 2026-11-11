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
import { isMain, launch } from "../skills/ui-design-director/scripts/browser.mjs";
import { BAD_IF_LESS, BAD_IF_MORE, EXACT, INFO_ONLY, TELLS, measure, side } from "../skills/ui-design-director/scripts/page_probe.mjs";
export { side };



const args = process.argv.slice(2);
const out = args[0];
const opt = (k, d) => (args.includes(k) ? args[args.indexOf(k) + 1] : d);
const widths = opt("--width", "390,1280").split(",").map(Number);
const label = opt("--label", "");
const pages = Object.fromEntries(args.filter((a) => /^(base|ours|ai)=/.test(a)).map((a) => {
  const i = a.indexOf("="), v = a.slice(i + 1);
  return [a.slice(0, i), /^https?:|^file:/.test(v) ? v : pathToFileURL(resolve(v)).href];
}));



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
        // AI 티로 판별한 꼴은 바탕에 있어도 문제 — 우리 값이 있으면 「우리만 다름」(사용자 2026-11-11)
        if (TELLS.has(key) && v.ours[key] > 0 && !(["회색한줄", "제목위윗줄"].includes(key) && !v.base.제목수)) {
          lines.push(`| ${key} | ${v.base[key]} | ${v.ours[key]} | ${v.ai[key]} | 우리만 다름 |`); rows.push({ key, verdict: "우리만 다름" }); continue;
        }
        let verdict = ["제목가운데", "회색한줄", "제목위윗줄"].includes(key) && !v.base.제목수 ? "가르지 못함" : side(v.base[key], v.ours[key], v.ai[key], !EXACT.has(key));
        if ((BAD_IF_MORE.has(key) && v.ours[key] <= v.base[key]) || (BAD_IF_LESS.has(key) && v.ours[key] >= v.base[key])) verdict = "정답지 쪽";
        // 사진은 바탕의 85% 아래면 바탕보다 오답지(사진 0)에 가깝지 않아도 모자람 — compose_metrics 와 같은 잣대(빵집 31차 0.41 대 0.78)
        if (BAD_IF_LESS.has(key) && v.ours[key] < v.base[key] * 0.85 && verdict !== "가르지 못함") verdict = "오답지 쪽";
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
