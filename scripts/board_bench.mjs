// 보기 화면 속도·메모리 재기(개발용) — 후보를 차례로 넘기며 화면이 다 뜰 때까지 걸린 시간과, 끝난 뒤 브라우저 메모리
// 사용: node scripts/board_bench.mjs <board-spec.json> [--settle 1500]
// spec 옆에 보기 화면을 만들고(live_proxy.mjs), 머리 없는 브라우저로 열어 → 키로 넘긴다. 남의 사이트를 실제로 불러온다.
import { spawn, spawnSync } from "node:child_process";
import { dirname, join } from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";

const SKILL = join(dirname(fileURLToPath(import.meta.url)), "..", "skills", "ui-design-director", "scripts");
const { launch, openPage, sleep } = await import(pathToFileURL(join(SKILL, "browser.mjs")).href);
const specPath = process.argv[2];
const SETTLE_MS = Number(process.argv[process.argv.indexOf("--settle") + 1]) || 1500;
const LOAD_TIMEOUT_MS = 30000;
if (!specPath) { console.error("사용: node scripts/board_bench.mjs <board-spec.json>"); process.exit(2); }

// 1. 프록시를 띄우고 OPEN 주소를 받는다
const proxy = spawn(process.execPath, [join(SKILL, "live_proxy.mjs"), specPath], { stdio: ["ignore", "pipe", "inherit"] });
const open = await new Promise((resolve, reject) => {
  let buf = "";
  proxy.stdout.on("data", (d) => { buf += d; const m = buf.match(/OPEN (\S+)/); if (m) resolve(m[1]); });
  proxy.on("exit", () => reject(new Error("프록시가 OPEN 주소 없이 끝남")));
});

// 화면 속 틀(iframe)이 모두 load 될 때까지 — 보드가 틀을 만들 때마다 load 를 세는 표시를 단다
// 페이지 스크립트보다 먼저 심는다(늦게 붙이면 첫 후보의 load 를 놓쳤다). 틀마다 만들어진 차례 번호를 단다
const WATCH = `(() => { let seq = 0; window.__errs = []; addEventListener("error", (e) => __errs.push(String(e.message)));
  const mark = () => document.querySelectorAll("iframe:not([data-w])").forEach((f) => { f.dataset.w = String(++seq); f.dataset.t0 = String(Math.round(performance.now())); f.addEventListener("load", () => { f.dataset.loaded = "1"; f.dataset.t1 = f.dataset.t1 || String(Math.round(performance.now())); }); });
  document.addEventListener("DOMContentLoaded", () => { mark(); new MutationObserver(mark).observe(document.body, { childList: true, subtree: true, attributes: true, attributeFilter: ["style", "hidden", "class"] }); }); })()`;
// 보이는 틀이 모두 load 됐는가 — 보이는 틀의 src 목록도 돌려준다(넘긴 뒤 새 후보의 틀인지 가르기)
const VISIBLE = `(() => { const fs = [...document.querySelectorAll("iframe")].filter((f) => f.offsetParent !== null && getComputedStyle(f).visibility !== "hidden");
  return { ok: fs.length > 0 && fs.every((f) => f.dataset.loaded === "1"), srcs: fs.map((f) => f.src).sort().join(" ") }; })()`;

const { port, close, profile } = await launch("capture-");
const page = await openPage(port, { width: 1440, phone: false });
const ev = async (expr) => (await page.cdp.send("Runtime.evaluate", { expression: expr, returnByValue: true })).result.value;
let lastSrcs = "";
const waitShown = async (t0 = Date.now()) => {
  while (Date.now() - t0 < LOAD_TIMEOUT_MS) {
    const v = await ev(VISIBLE);
    if (process.env.BENCH_DEBUG && v && JSON.stringify(v) !== waitShown.prev) { waitShown.prev = JSON.stringify(v); console.log(`  ${Date.now() - t0}ms ok=${v.ok} ${v.srcs.slice(0, 120)}`); }
    if (v && v.ok && v.srcs !== lastSrcs) { lastSrcs = v.srcs; return Date.now() - t0; }
    await sleep(50);
  }
  if (process.env.BENCH_DEBUG) console.log("오류·위치:", JSON.stringify(await ev("({ e: window.__errs, h: location.hash })")), "틀:", JSON.stringify(await ev(`[...document.querySelectorAll("iframe")].map((f) => ({ v: f.offsetParent !== null && getComputedStyle(f).visibility !== "hidden", l: f.dataset.loaded || "", w: f.dataset.w, src: f.src.slice(0, 90) }))`)));
  return null;
};
// 키를 보내기 전에 초점을 보기 화면으로 — 띄운 사이트가 초점을 가져가면 키가 그쪽으로 갔다
const key = async (k) => { await ev("document.activeElement && document.activeElement.blur(), window.focus()"); return page.cdp.send("Input.dispatchKeyEvent", { type: "keyDown", key: k, code: k, windowsVirtualKeyCode: k === "ArrowRight" ? 39 : 37 }); };

try {
  await page.cdp.send("Page.addScriptToEvaluateOnNewDocument", { source: WATCH });
  const start = Date.now();
  // 보기 화면의 load 를 기다리지 않는다 — 부모 페이지의 load 는 안의 틀(미리 띄운 다음 후보까지)이 다 떠야 와서, 첫 화면을 늦게 쟀다
  await page.cdp.send("Page.navigate", { url: open });
  const n = await ev("document.querySelectorAll('.v-thumb, [data-cand]').length") || 7;
  const times = [];
  times.push(await waitShown(start));
  if (process.argv.includes("--first-only")) { console.log(`첫 후보: ${(times[0] / 1000).toFixed(1)}초`, JSON.stringify(await ev(`[...document.querySelectorAll("iframe")].map((f) => [f.dataset.w, f.dataset.t0, f.dataset.t1 || "-", Math.round(f.getBoundingClientRect().width), f.src.slice(8, 30)])`))); process.exitCode = 0; throw new Error("first-only"); }
  for (let i = 1; i < n; i++) { await sleep(SETTLE_MS); const t = Date.now(); await key("ArrowRight"); times.push(await waitShown(t)); }
  await sleep(SETTLE_MS);
  const tb = Date.now();
  for (let i = 1; i < n; i++) await key("ArrowLeft"); // 처음 후보로 돌아오기
  const back = await waitShown(tb);
  // 메모리: 이 프로필로 뜬 Edge 프로세스 전부의 작업 집합 합계
  const ps = spawnSync("powershell", ["-NoProfile", "-Command",
    `(Get-CimInstance Win32_Process -Filter "Name='msedge.exe'" | Where-Object { $_.CommandLine -like '*${profile.replace(/'/g, "''")}*' } | Measure-Object WorkingSetSize -Sum).Sum`], { encoding: "utf8" });
  const mb = Math.round(Number(ps.stdout.trim()) / 1048576);
  const fmt = (t) => (t === null ? "시간 초과" : `${(t / 1000).toFixed(1)}초`);
  console.log(`후보별 다 뜨기까지: ${times.map(fmt).join(" · ")}`);
  console.log(`처음 후보로 돌아오기: ${fmt(back)}`);
  console.log(`브라우저 메모리(작업 집합 합계): ${mb}MB`);
} catch (e) { if (e.message !== "first-only") throw e; } finally {
  await page.close().catch(() => {});
  await close();
  proxy.kill();
}
