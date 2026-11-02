#!/usr/bin/env node
// 실제 기기 폭으로 웹 페이지 전체를 찍는다. 외부 패키지 없이 Edge/Chrome DevTools 프로토콜만 쓴다.
// 사용: node capture.mjs <jobs.json> <out-dir> [--widths 1280,390]
// jobs.json: [{ "id": "1-craft-home", "url": "https://…", "steps": [ … ] }, …]
//   steps(선택): 찍기 전에 같은 창에서 할 일. { "goto": url } · { "click": "css 선택자" } · { "wait": ms }
//   예) 장바구니를 상품이 담긴 상태로 찍기: 상품 페이지로 가서 담기 단추를 누른 뒤 url(장바구니)을 찍는다.
//   url 을 "@current" 로 주면 steps 를 마친 화면 그대로 찍는다(주소를 모르는 상품 상세 등).
// 결과: <out-dir>/<id>-<width>.jpg. 이미 있는 파일은 건너뛰므로 중간에 끊겨도 다시 돌리면 이어서 찍는다.
// 문서 응답이 400 이상이면 저장하지 않고 실패로 보고한다.

import { spawn } from "node:child_process";
import { existsSync, mkdirSync, readFileSync, writeFileSync, mkdtempSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { createServer } from "node:net";

// 설치 위치는 운영체제가 알려 주는 폴더에서 찾는다
const WIN_DIRS = [process.env["ProgramFiles(x86)"], process.env.ProgramFiles, process.env.LOCALAPPDATA].filter(Boolean);
const BROWSERS = [
  process.env.CAPTURE_BROWSER,
  ...WIN_DIRS.map((d) => join(d, "Microsoft", "Edge", "Application", "msedge.exe")),
  ...WIN_DIRS.map((d) => join(d, "Google", "Chrome", "Application", "chrome.exe")),
  "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
  "/usr/bin/google-chrome",
  "/usr/bin/chromium",
].filter(Boolean);
const PHONE_MAX = 600;
const PHONE_HEIGHT = 844;
const DESKTOP_HEIGHT = 900;
const MAX_PAGE_HEIGHT = 8000;
const SETTLE_MS = 2500;
const SCROLL_STEP_MS = 120;
const CURRENT_PAGE = "@current"; // url 에 이 값을 주면 steps 를 마친 그 화면을 찍는다
const NAV_TIMEOUT_MS = 45000;
const PHONE_UA =
  "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1";

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

function freePort() {
  return new Promise((resolve, reject) => {
    const srv = createServer();
    srv.once("error", reject);
    srv.listen(0, "127.0.0.1", () => {
      const { port } = srv.address();
      srv.close(() => resolve(port));
    });
  });
}

function parseArgs(argv) {
  const args = { widths: [1280, 390], rest: [] };
  for (let i = 0; i < argv.length; i++) {
    if (argv[i] === "--widths") args.widths = argv[++i].split(",").map(Number);
    else args.rest.push(argv[i]);
  }
  if (args.rest.length !== 2 || args.widths.some((w) => !Number.isFinite(w) || w < 200)) {
    console.error("사용: node capture.mjs <jobs.json> <out-dir> [--widths 1280,390]");
    process.exit(2);
  }
  return args;
}

class Cdp {
  constructor(ws) {
    this.ws = ws;
    this.id = 0;
    this.pending = new Map();
    this.listeners = [];
    ws.addEventListener("message", (ev) => {
      const msg = JSON.parse(ev.data);
      if (msg.id && this.pending.has(msg.id)) {
        const { resolve, reject } = this.pending.get(msg.id);
        this.pending.delete(msg.id);
        msg.error ? reject(new Error(msg.error.message)) : resolve(msg.result);
      } else if (msg.method) {
        this.listeners.forEach((fn) => fn(msg));
      }
    });
  }
  static async open(url) {
    const ws = new WebSocket(url);
    await new Promise((res, rej) => {
      ws.addEventListener("open", res, { once: true });
      ws.addEventListener("error", rej, { once: true });
    });
    return new Cdp(ws);
  }
  send(method, params = {}) {
    const id = ++this.id;
    this.ws.send(JSON.stringify({ id, method, params }));
    return new Promise((resolve, reject) => this.pending.set(id, { resolve, reject }));
  }
  waitFor(method, timeout) {
    return new Promise((resolve, reject) => {
      const timer = setTimeout(() => reject(new Error(`${method} 대기 시간 초과`)), timeout);
      const fn = (msg) => {
        if (msg.method === method) {
          clearTimeout(timer);
          this.listeners = this.listeners.filter((f) => f !== fn);
          resolve(msg.params);
        }
      };
      this.listeners.push(fn);
    });
  }
  close() {
    this.ws.close();
  }
}

async function launch() {
  const exe = BROWSERS.find((p) => existsSync(p));
  if (!exe) throw new Error("Edge 또는 Chrome을 찾지 못했습니다. CAPTURE_BROWSER 로 경로를 지정하세요.");
  const port = await freePort();
  const profile = mkdtempSync(join(tmpdir(), "capture-"));
  const proc = spawn(exe, [
    "--headless=new", "--disable-gpu", "--hide-scrollbars", "--no-first-run", "--mute-audio",
    `--remote-debugging-port=${port}`, `--user-data-dir=${profile}`, "about:blank",
  ], { stdio: "ignore" });
  for (let i = 0; i < 50; i++) {
    try {
      const res = await fetch(`http://127.0.0.1:${port}/json/version`);
      if (res.ok) return { proc, port, profile };
    } catch { /* 아직 뜨는 중 */ }
    await sleep(200);
  }
  proc.kill();
  throw new Error("브라우저 디버깅 포트가 열리지 않았습니다.");
}

async function shoot(port, url, width, steps = []) {
  const target = await (await fetch(`http://127.0.0.1:${port}/json/new?about:blank`, { method: "PUT" })).json();
  const cdp = await Cdp.open(target.webSocketDebuggerUrl);
  try {
    const phone = width <= PHONE_MAX;
    await cdp.send("Page.enable");
    await cdp.send("Network.enable");
    await cdp.send("Emulation.setDeviceMetricsOverride", {
      width, height: phone ? PHONE_HEIGHT : DESKTOP_HEIGHT, deviceScaleFactor: 1, mobile: phone,
    });
    if (phone) await cdp.send("Emulation.setUserAgentOverride", { userAgent: PHONE_UA });

    let status = 0;
    cdp.listeners.push((msg) => {
      if (msg.method === "Network.responseReceived" && msg.params.type === "Document" && !status) {
        status = msg.params.response.status;
      }
    });
    const go = async (to) => {
      status = 0;
      const loaded = cdp.waitFor("Page.loadEventFired", NAV_TIMEOUT_MS);
      await cdp.send("Page.navigate", { url: to });
      await loaded;
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
      } else if (step.wait) await sleep(step.wait);
    }
    if (url !== CURRENT_PAGE) await go(url);

    // 늦게 불러오는 사진을 깨우려고 끝까지 내렸다가 올린다
    await cdp.send("Runtime.evaluate", {
      expression: `(async () => { for (let y = 0; y < document.body.scrollHeight; y += innerHeight) { scrollTo(0, y); await new Promise(r => setTimeout(r, ${SCROLL_STEP_MS})); } scrollTo(0, 0); })()`,
      awaitPromise: true,
    });
    await sleep(SETTLE_MS);
    const { cssContentSize } = await cdp.send("Page.getLayoutMetrics");
    const height = Math.min(Math.ceil(cssContentSize.height), MAX_PAGE_HEIGHT);
    const shot = await cdp.send("Page.captureScreenshot", {
      format: "jpeg", quality: 82, captureBeyondViewport: true,
      clip: { x: 0, y: 0, width, height, scale: 1 },
    });
    return { data: Buffer.from(shot.data, "base64"), height, status };
  } finally {
    cdp.close();
    await fetch(`http://127.0.0.1:${port}/json/close/${target.id}`).catch(() => {});
  }
}

async function main() {
  const { widths, rest } = parseArgs(process.argv.slice(2));
  const [jobsPath, outDir] = rest;
  const jobs = JSON.parse(readFileSync(jobsPath, "utf8"));
  mkdirSync(outDir, { recursive: true });
  const { proc, port, profile } = await launch();
  const failed = [];
  let done = 0;
  const total = jobs.length * widths.length;
  try {
    for (const job of jobs) {
      for (const width of widths) {
        const file = join(outDir, `${job.id}-${width}.jpg`);
        done++;
        if (existsSync(file)) {
          console.log(`[${done}/${total}] 있음, 건너뜀  ${job.id}-${width}`);
          continue;
        }
        try {
          const { data, height } = await shoot(port, job.url, width, job.steps || []);
          writeFileSync(file, data);
          console.log(`[${done}/${total}] 저장  ${job.id}-${width}  ${width}x${height}`);
        } catch (err) {
          failed.push(`${job.id}-${width}: ${err.message}`);
          console.log(`[${done}/${total}] 실패  ${job.id}-${width}  ${err.message}`);
        }
      }
    }
  } finally {
    proc.kill();
    await sleep(500);
    try { rmSync(profile, { recursive: true, force: true }); } catch { /* 브라우저가 늦게 닫히면 남을 수 있음 */ }
  }
  console.log(`끝: 성공 ${total - failed.length} / 실패 ${failed.length}`);
  if (failed.length) {
    failed.forEach((f) => console.log(`  - ${f}`));
    process.exit(1);
  }
}

main().catch((err) => {
  console.error(`ERROR: ${err.message}`);
  process.exit(1);
});
