#!/usr/bin/env node
// 실제 기기 폭으로 웹 페이지 전체를 찍는다. 외부 패키지 없이 Edge/Chrome DevTools 프로토콜만 쓴다.
// 사용: node capture.mjs <jobs.json> <out-dir> [--widths 1280,390]
// jobs.json: [{ "id": "1-craft-home", "url": "https://…", "steps": [ … ] }, …]
//   steps(선택): 찍기 전에 같은 창에서 할 일. { "goto": url } · { "click": "css 선택자" } · { "wait": ms }
//   예) 장바구니를 상품이 담긴 상태로 찍기: 상품 페이지로 가서 담기 단추를 누른 뒤 url(장바구니)을 찍는다.
//   url 을 "@current" 로 주면 steps 를 마친 화면 그대로 찍는다(주소를 모르는 상품 상세 등).
//   쿠키·동의·알림 창은 기본으로 걷어 낸다. 창 자체를 보여 줘야 하면 "keepOverlays": true.
//   "judge": true — 블라인드 판정용 사본만: 견본 표시·빗금 자리를 숨기고 0000 번호를 그럴듯한 번호로(judge_fill.mjs). 남은 흔적은 「판정 흔적」으로 알린다.
//   "scrollY": 숫자 를 주면 전체 길이 대신 그 위치의 한 화면만 찍는다 — 아래에 붙는 단추·위에 붙는 칩처럼
//   스크롤해도 따라오는 것은 전체 길이 캡처에선 페이지 중간에 박혀 글을 가린 것처럼 보이므로 이렇게 확인한다.
// 배율: 기본 2배(--scale 1~3, job 마다 "scale"). 그림 크기는 폭×배율 — 그림을 재는 도구는 폭으로 나눠 본다.
// 결과: <out-dir>/<id>-<width>.jpg. 이미 있는 파일은 건너뛰므로 중간에 끊겨도 다시 돌리면 이어서 찍는다.
//   단 file:// 로 찍은 우리 시안은 그 html 이나 같은 폴더의 파일(css·사진)이 그림보다 새로우면 다시 찍는다 —
//   고친 시안을 옛 그림으로 비교했다. 원격 주소는 그대로 건너뛴다. --force 는 늘 다시 찍는다.
// 문서 응답이 400 이상이면 저장하지 않고 실패로 보고한다.

import { existsSync, mkdirSync, readdirSync, readFileSync, statSync, writeFileSync } from "node:fs";
import { basename, dirname, join, resolve, sep } from "node:path";
import { fileURLToPath } from "node:url";
import { judgeFillExpr } from "./judge_fill.mjs";
import { goto, launch, openPage, scrollWakeExpr, sleep, HIDE_OVERLAYS, isMain } from "./browser.mjs";
import { requireStage } from "./stage_guard.mjs";

const SCREEN_SLICES = 16; // 맨 위부터 한 화면씩 잘라 따로 저장할 최대 수(screens/ 폴더). 4장만 자르면 페이지 아래쪽(시간표·질문·오시는 길)을 못 봤다
const MAX_PAGE_HEIGHT = 16000; // 8000 에서 잘려 긴 페이지(나이키 12,857px)의 아래쪽을 못 봤다
const SETTLE_MS = 2500;
const SCROLL_STEP_MS = 300; // 120ms 로 휙 내리면 늦게 불러오는 사진이 빈칸으로 남았다
const CURRENT_PAGE = "@current"; // url 에 이 값을 주면 steps 를 마친 그 화면을 찍는다
// 화면 크기·실제 브라우저 이름(「HeadlessChrome」을 보고 거절하는 사이트가 있다)·webdriver 숨김은 browser.mjs 의 openPage 가 건다
// 2배로 찍는다: 1배 JPEG 82는 작은 글자·가는 선·단추 테두리가 뭉개져 바탕의 마감을 사람도 AI도 못 읽었다
const DEFAULT_SCALE = 2;
const JPEG_QUALITY = 92;
const JPEG_MAX_PX = 65000; // JPEG 한 장의 최대 높이(픽셀) — 넘으면 배율을 낮춰 찍는다
const SOURCE_DEPTH = 2; // 시안 폴더에서 새로 고친 파일을 찾을 깊이(css/·img/ 정도) — 프로젝트 전체를 훑지 않게
const SKIP_DIRS = new Set(["node_modules", ".git", "__pycache__"]);



function parseArgs(argv) {
  const args = { widths: [1280, 390], scale: DEFAULT_SCALE, force: false, rest: [] };
  for (let i = 0; i < argv.length; i++) {
    if (argv[i] === "--force") args.force = true;
    else if (argv[i] === "--widths") args.widths = argv[++i].split(",").map(Number);
    else if (argv[i] === "--scale") args.scale = Math.min(3, Math.max(1, Number(argv[++i]) || DEFAULT_SCALE));
    else args.rest.push(argv[i]);
  }
  if (args.rest.length !== 2 || args.widths.some((w) => !Number.isFinite(w) || w < 200)) {
    console.error("사용: node capture.mjs <jobs.json> <out-dir> [--widths 1280,390] [--scale 2] [--force]");
    process.exit(2);
  }
  return args;
}


// 폴더 안 가장 늦게 고친 시각(ms). 캡처를 담는 폴더(skip)는 뺀다 — 시안 옆 formats/ 에 찍으면 새 그림이 늘 「더 새로움」이 된다
function newestIn(dir, skip, depth = SOURCE_DEPTH) {
  let newest = 0;
  let names = [];
  try { names = readdirSync(dir, { withFileTypes: true }); } catch { return 0; }
  for (const d of names) {
    const p = join(dir, d.name);
    if (d.isDirectory()) {
      if (depth > 0 && !SKIP_DIRS.has(d.name) && !(resolve(p) + sep).startsWith(skip)) newest = Math.max(newest, newestIn(p, skip, depth - 1));
    } else if (d.isFile() && !(resolve(dir) + sep).startsWith(skip)) { // 시안과 같은 폴더에 찍어도 그림끼리 비교하지 않게
      try { newest = Math.max(newest, statSync(p).mtimeMs); } catch { /* 읽는 사이 지워진 파일 */ }
    }
  }
  return newest;
}

// 다시 찍을 이유. 없으면 null(건너뜀). 원격 주소는 바뀌었는지 알 수 없으니 그림이 있으면 건너뛴다
export function recaptureReason(file, url, { force = false, outDir = dirname(file) } = {}) {
  if (!existsSync(file)) return "없음";
  if (force) return "--force";
  if (typeof url !== "string" || !url.startsWith("file:")) return null;
  let src;
  try { src = fileURLToPath(url.split(/[?#]/)[0]); } catch { return null; }
  const shot = statSync(file).mtimeMs;
  const skip = resolve(outDir) + sep;
  if (existsSync(src) && statSync(src).mtimeMs > shot) return "시안이 그림보다 새로움";
  return newestIn(dirname(src), skip) > shot ? "시안 폴더의 파일이 그림보다 새로움" : null;
}

// 글·입력·사진 중 오른쪽 끝이 화면 너비를 넘는 것(가로로 미는 목록 안은 뺌)
const OVERFLOW_PROBE = `(() => {
  const W = document.documentElement.clientWidth, out = [];
  for (const el of document.querySelectorAll("input, textarea, select, button, img, p, h1, h2, h3, li, dd, a, label")) {
    const r = el.getBoundingClientRect();
    if (!r.width || r.right <= W + 1) continue;
    let n = el.parentElement, scroller = false;
    while (n && n !== document.body) { const o = getComputedStyle(n).overflowX; if (o === "auto" || o === "scroll" || o === "hidden") { scroller = true; break; } n = n.parentElement; }
    if (!scroller) out.push(el.tagName.toLowerCase() + (el.className && typeof el.className === "string" ? "." + el.className.split(" ")[0] : "") + " +" + Math.round(r.right - W) + "px");
  }
  return out;
})()`;

// 한 주소를 한 폭으로 찍는다. 옵션: url · width · steps · scrollY(한 화면만) · keepOverlays · judge · scale
async function shoot(port, { url, width, steps = [], scrollY = null, keepOverlays = false, judge = false, scale = DEFAULT_SCALE }) {
  const page = await openPage(port, { width, scale });
  const { cdp } = page;
  try {
    let status = 0;
    const go = async (to) => {
      status = await goto(cdp, to);
      if (status >= 400) throw new Error(`응답 ${status} (${to})`);
    };
    for (const step of steps) {
      if (step.goto) await go(step.goto);
      else if (step.click) {
        const { result } = await cdp.send("Runtime.evaluate", {
          expression: `(() => { const n = document.querySelector(${JSON.stringify(step.click)}); if (!n) return false; n.scrollIntoView({ block: "center" }); n.click(); return true; })()`,
          returnByValue: true,
        });
        if (!result.value) throw new Error(`누를 것을 찾지 못함: ${step.click}`);
        await sleep(SETTLE_MS);
      } else if (step.hide) {
        // 캡처를 가리는 떠 있는 막대 같은 것을 아예 숨긴다. 스크롤한 뒤에 다시 생기는 채팅 단추(채널톡·카카오)도 있어 규칙으로도 남긴다
        await cdp.send("Runtime.evaluate", {
          expression: `(() => { const sel = ${JSON.stringify(step.hide)}; document.querySelectorAll(sel).forEach((n) => { n.style.setProperty("display", "none", "important"); }); const st = document.createElement("style"); st.textContent = sel + "{display:none !important}"; document.head.appendChild(st); })()`,
        });
      } else if (step.wait) await sleep(step.wait);
    }
    if (url !== CURRENT_PAGE) await go(url);

    // 쿠키·동의·알림 창은 사이트의 구성이 아니다 — 기본으로 걷어 낸다(빵집 후보 셋이 창에 덮여 의뢰인이 볼 수 없었다)
    let marks = [];
    if (judge) marks = (await cdp.send("Runtime.evaluate", { expression: judgeFillExpr(), returnByValue: true })).result.value || [];
    if (!keepOverlays) {
      await cdp.send("Runtime.evaluate", { expression: HIDE_OVERLAYS });
    }

    // 늦게 불러오는 사진을 깨우려고 끝까지 내렸다가 올린다
    await cdp.send("Runtime.evaluate", { expression: scrollWakeExpr(Infinity, SCROLL_STEP_MS), awaitPromise: true });
    await sleep(SETTLE_MS);
    if (!keepOverlays) await cdp.send("Runtime.evaluate", { expression: HIDE_OVERLAYS }); // 내리는 동안 늦게 뜬 띠
    if (scrollY !== null) {
      // 실제 폰처럼 한 화면만: 붙어 다니는 막대가 제자리에 보인다
      await cdp.send("Runtime.evaluate", { expression: `scrollTo(0, ${Number(scrollY)})` });
      await sleep(SETTLE_MS);
      const view = await cdp.send("Page.captureScreenshot", { format: "jpeg", quality: JPEG_QUALITY });
      return { data: Buffer.from(view.data, "base64"), height: page.height, status, screens: [], marks };
    }
    // 화면 오른쪽 밖으로 삐져나간 칸 — 폰에서 두 칸 입력이 잘린 것을 의뢰인이 먼저 잡았다(집수리 사장님 화면)
    const spill = (await cdp.send("Runtime.evaluate", { returnByValue: true, expression: OVERFLOW_PROBE })).result.value || [];
    const { cssContentSize } = await cdp.send("Page.getLayoutMetrics");
    const height = Math.min(Math.ceil(cssContentSize.height), MAX_PAGE_HEIGHT);
    // 전체 한 장은 JPEG 최대 높이를 넘지 않게 배율을 낮춘다(조각은 늘 원래 배율)
    const fullScale = Math.min(1, JPEG_MAX_PX / (height * scale));
    const shot = await cdp.send("Page.captureScreenshot", {
      format: "jpeg", quality: JPEG_QUALITY, captureBeyondViewport: true,
      clip: { x: 0, y: 0, width, height, scale: fullScale },
    });
    // 한 화면 크기 조각 — 긴 전체 캡처는 파일로 열면 글씨가 너무 작아 안 읽힌다
    const viewH = page.height;
    const screens = [];
    for (let i = 0; i < SCREEN_SLICES && i * viewH < height; i++) {
      const part = await cdp.send("Page.captureScreenshot", {
        format: "jpeg", quality: JPEG_QUALITY, captureBeyondViewport: true,
        clip: { x: 0, y: i * viewH, width, height: Math.min(viewH, height - i * viewH), scale: 1 },
      });
      screens.push(Buffer.from(part.data, "base64"));
    }
    return { data: Buffer.from(shot.data, "base64"), height, status, screens, spill, marks };
  } finally {
    await page.close();
  }
}

async function main() {
  const { widths, scale, force, rest } = parseArgs(process.argv.slice(2));
  const [jobsPath, outDir] = rest;
  // 바탕 자료(base_material.py 가 만든 jobs-base.json)를 찍을 때만 바탕 확정을 본다 — 후보 캡처(바탕 고르기 전)는 그대로
  if (/^jobs-base/i.test(basename(jobsPath || ""))) requireStage(outDir);
  const jobs = JSON.parse(readFileSync(jobsPath, "utf8"));
  mkdirSync(outDir, { recursive: true });
  const { port, close } = await launch("capture-");
  const failed = [];
  let done = 0;
  const total = jobs.length * widths.length;
  try {
    for (const job of jobs) {
      for (const width of widths) {
        const file = join(outDir, `${job.id}-${width}.jpg`);
        done++;
        const why = recaptureReason(file, job.url, { force, outDir });
        if (!why) {
          console.log(`[${done}/${total}] 있음, 건너뜀  ${job.id}-${width}`);
          continue;
        }
        if (why !== "없음") console.log(`[${done}/${total}] 다시 찍음  ${job.id}-${width}  (${why})`);
        try {
          const { data, height, screens, spill = [], marks = [] } = await shoot(port, {
            url: job.url, width, steps: job.steps || [], scrollY: job.scrollY ?? null,
            keepOverlays: Boolean(job.keepOverlays), judge: Boolean(job.judge), scale: job.scale ?? scale,
          });
          writeFileSync(file, data);
          const sliceDir = join(outDir, "screens");
          mkdirSync(sliceDir, { recursive: true });
          screens.forEach((buf, i) => writeFileSync(join(sliceDir, `${job.id}-${width}-${i + 1}.jpg`), buf));
          console.log(`[${done}/${total}] 저장  ${job.id}-${width}  ${width}x${height}`);
          if (marks.length) console.log(`        판정 흔적  아직 보이는 견본 흔적: ${marks.join(", ")} — 판정용 사본에서 지우거나 채울 것`);
          if (spill.length) console.log(`        넘침  화면 밖으로 나간 칸 ${spill.length}개: ${spill.slice(0, 3).join(" | ")}`);
        } catch (err) {
          failed.push(`${job.id}-${width}: ${err.message}`);
          console.log(`[${done}/${total}] 실패  ${job.id}-${width}  ${err.message}`);
        }
      }
    }
  } finally {
    await close();
  }
  console.log(`끝: 성공 ${total - failed.length} / 실패 ${failed.length}`);
  if (failed.length) {
    failed.forEach((f) => console.log(`  - ${f}`));
    process.exit(1);
  }
}

if (isMain(import.meta.url)) {
  main().catch((err) => {
    console.error(`ERROR: ${err.message}`);
    process.exit(1);
  });
}
