// 캡처·스냅샷이 함께 쓰는 브라우저 띄우기와 DevTools 프로토콜 연결(외부 패키지 없음)
import { spawn, spawnSync } from "node:child_process";
import { existsSync, mkdtempSync, readdirSync, readFileSync, realpathSync, rmSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";
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

// 브라우저 이름은 assets/browser.json 한 곳에 둔다(frame_check.py 도 같은 파일을 읽는다)
const NAMES = JSON.parse(readFileSync(join(dirname(fileURLToPath(import.meta.url)), "..", "assets", "browser.json"), "utf8"));
const PHONE_UA = NAMES.phoneUA;
const DESKTOP_UA = NAMES.desktopUA;
const ACCEPT_LANGUAGE = NAMES.acceptLanguage;
export const PHONE_MAX_WIDTH = 600; // 이 폭 이하는 폰으로 연다(폰 이름·터치 화면)
// 한 화면 높이. measure: 구성·뼈대 측정(compose_metrics·skeleton)은 처음부터 800 으로 재 와서 기준값이 이 높이에서 나왔다
export const VIEWPORT = { phone: 844, desktop: 900, measure: 800 };
const NAV_TIMEOUT_MS = 45000;
const HIDE_WEBDRIVER = "Object.defineProperty(navigator, 'webdriver', { get: () => undefined })";

export const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

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

export class Cdp {
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
    // 탭이 닫히거나 브라우저가 죽으면 기다리던 요청이 영영 안 끝났다 — 오류로 끝낸다
    ws.addEventListener("close", () => {
      for (const { reject } of this.pending.values()) reject(new Error("브라우저 연결이 끊겼습니다."));
      this.pending.clear();
    });
  }
  static async open(url) {
    const ws = new WebSocket(url);
    await new Promise((res, rej) => {
      ws.addEventListener("open", res, { once: true });
      ws.addEventListener("error", () => rej(new Error(`브라우저에 연결하지 못했습니다: ${url}`)), { once: true });
    });
    return new Cdp(ws);
  }
  send(method, params = {}) {
    if (this.ws.readyState !== WebSocket.OPEN) return Promise.reject(new Error("브라우저 연결이 끊겼습니다."));
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

// 브라우저 끄기 — 윈도우에서 proc.kill() 은 처음 띄운 프로세스만 끄고 화면을 그리는 Edge 본체는 남았다
// (하루 역할극에 headless Edge 75벌, 프로세스 700여 개가 쌓임). 본체 번호를 DevTools 로 받아 그 나무째 끈다.
const PROFILE_PREFIXES = ["capture-", "styles-", "compose-", "snap-", "motion-", "skeleton-"];
const OWNER_FILE = "owner.json"; // 이 브라우저를 띄운 node 번호와 본체 번호 — 주인이 죽고 남은 브라우저를 다음 실행이 찾아 끈다
const live = new Set();

function killTree(pid) {
  if (!pid) return;
  try {
    if (process.platform === "win32") spawnSync("taskkill", ["/PID", String(pid), "/T", "/F"], { stdio: "ignore" });
    else process.kill(pid, "SIGKILL");
  } catch { /* 이미 꺼짐 */ }
}

// 꺼진 Edge 가 잠깐 파일을 쥐고 있어 한 번에 안 지워졌다(남은 프로필 255벌, 51GB) — 3초까지 다시 시도, 그래도 안 되면 다음 정리 때
const pause = (ms) => Atomics.wait(new Int32Array(new SharedArrayBuffer(4)), 0, 0, ms);
function removeDirSync(dir) {
  for (let i = 0; i < 15 && existsSync(dir); i++) {
    try { rmSync(dir, { recursive: true, force: true }); } catch { pause(200); }
  }
}

const alive = (pid) => { try { process.kill(pid, 0); return true; } catch (e) { return e.code === "EPERM"; } };

// 주인(node)이 시간 초과 등으로 강제로 끝나 끄는 코드가 돌지 못한 브라우저를 끈다
export function sweepOrphans() {
  let n = 0;
  for (const name of readdirSync(tmpdir())) {
    if (!PROFILE_PREFIXES.some((p) => name.startsWith(p))) continue;
    const dir = join(tmpdir(), name);
    let owner;
    try { owner = JSON.parse(readFileSync(join(dir, OWNER_FILE), "utf8")); } catch { continue; } // 표시가 없으면 누구 것인지 몰라 둔다
    if (alive(owner.owner)) continue;
    killTree(owner.browser);
    removeDirSync(dir);
    n++;
  }
  return n;
}

function closeAllSync() {
  for (const b of live) { killTree(b.browser); killTree(b.proc.pid); removeDirSync(b.profile); }
  live.clear();
}
let hooked = false;
function hookExit() {
  if (hooked) return;
  hooked = true;
  process.on("exit", closeAllSync);
  for (const sig of ["SIGINT", "SIGTERM", "SIGHUP"]) process.on(sig, () => { closeAllSync(); process.exit(130); });
}

export async function launch(prefix = "capture-") {
  const exe = BROWSERS.find((p) => existsSync(p));
  if (!exe) throw new Error("Edge 또는 Chrome을 찾지 못했습니다. CAPTURE_BROWSER 로 경로를 지정하세요.");
  sweepOrphans();
  const port = await freePort();
  const profile = mkdtempSync(join(tmpdir(), prefix));
  const proc = spawn(exe, [
    "--headless=new", "--disable-gpu", "--hide-scrollbars", "--no-first-run", "--mute-audio",
    "--disable-blink-features=AutomationControlled",
    `--remote-debugging-port=${port}`, `--user-data-dir=${profile}`, "about:blank",
  ], { stdio: "ignore" });
  const entry = { proc, profile, browser: 0 };
  live.add(entry);
  hookExit();
  for (let i = 0; i < 50; i++) {
    try {
      const res = await fetch(`http://127.0.0.1:${port}/json/version`);
      if (res.ok) {
        const { webSocketDebuggerUrl } = await res.json();
        try {
          const b = await Cdp.open(webSocketDebuggerUrl);
          const info = await b.send("SystemInfo.getProcessInfo");
          entry.browser = info.processInfo.find((p) => p.type === "browser")?.id || 0;
          b.close();
        } catch { /* 본체 번호를 못 받으면 proc 나무로만 끈다 */ }
        writeFileSync(join(profile, OWNER_FILE), JSON.stringify({ owner: process.pid, browser: entry.browser }));
        const close = async () => {
          try {
            const b = await Cdp.open(webSocketDebuggerUrl);
            await Promise.race([b.send("Browser.close"), sleep(1500)]);
          } catch { /* 이미 닫힘 */ }
          await sleep(300);
          killTree(entry.browser);
          killTree(proc.pid);
          removeDirSync(profile);
          live.delete(entry);
        };
        return { proc, port, profile, close };
      }
    } catch { /* 아직 뜨는 중 */ }
    await sleep(200);
  }
  killTree(proc.pid);
  live.delete(entry);
  throw new Error("브라우저 디버깅 포트가 열리지 않았습니다.");
}

// 새 탭을 열어 폭·폰 여부에 맞춘 화면 크기, 실제 브라우저 이름, webdriver 숨김을 걸어 돌려준다.
// height 를 주면 컴퓨터 폭의 화면 높이를 그것으로(폰은 늘 VIEWPORT.phone). close() 는 몇 번 불러도 된다.
export async function openPage(port, { width, phone = width <= PHONE_MAX_WIDTH, height, scale = 1 } = {}) {
  const res = await fetch(`http://127.0.0.1:${port}/json/new?about:blank`, { method: "PUT" });
  if (!res.ok) throw new Error(`새 탭을 열지 못했습니다(응답 ${res.status}).`);
  const target = await res.json();
  let cdp = null, closed = false;
  const close = async () => {
    if (closed) return;
    closed = true;
    cdp?.close();
    await fetch(`http://127.0.0.1:${port}/json/close/${target.id}`).catch(() => {});
  };
  const viewH = phone ? VIEWPORT.phone : height ?? VIEWPORT.desktop;
  try {
    cdp = await Cdp.open(target.webSocketDebuggerUrl);
    await cdp.send("Page.enable");
    await cdp.send("Network.enable");
    await cdp.send("Emulation.setDeviceMetricsOverride", { width, height: viewH, deviceScaleFactor: scale, mobile: phone });
    await cdp.send("Emulation.setUserAgentOverride", { userAgent: phone ? PHONE_UA : DESKTOP_UA, acceptLanguage: ACCEPT_LANGUAGE });
    await cdp.send("Page.addScriptToEvaluateOnNewDocument", { source: HIDE_WEBDRIVER });
  } catch (err) {
    await close();
    throw err;
  }
  return { cdp, close, phone, height: viewH };
}

// 주소로 가서 load 까지 기다린다. 문서 응답 번호를 돌려준다(0 = 못 받음). 못 열면 한 줄 오류.
export async function goto(cdp, url, { timeout = NAV_TIMEOUT_MS } = {}) {
  let status = 0, timer, onEvent;
  const loaded = new Promise((resolve, reject) => {
    timer = setTimeout(() => reject(new Error(`${Math.round(timeout / 1000)}초 안에 다 열리지 않았습니다: ${url}`)), timeout);
    onEvent = (msg) => {
      if (msg.method === "Network.responseReceived" && msg.params.type === "Document" && !status) status = msg.params.response.status;
      else if (msg.method === "Page.loadEventFired") resolve();
    };
    cdp.listeners.push(onEvent);
  });
  try {
    const { errorText } = await cdp.send("Page.navigate", { url });
    if (errorText) throw new Error(`페이지를 열지 못했습니다(${errorText}): ${url}`);
    await loaded;
    return status;
  } finally {
    clearTimeout(timer);
    cdp.listeners = cdp.listeners.filter((f) => f !== onEvent);
  }
}

// 페이지 안에서 식을 돌려 값을 받는다. 페이지 쪽에서 오류가 나면 undefined 대신 그 오류 첫 줄로 끝낸다
export async function evaluate(cdp, expression, { awaitPromise = false } = {}) {
  const r = await cdp.send("Runtime.evaluate", { expression, returnByValue: true, awaitPromise });
  if (r.exceptionDetails) {
    const d = r.exceptionDetails;
    throw new Error(`페이지 안 코드 오류: ${String(d.exception?.description || d.text || "").split(/\r?\n/)[0]}`);
  }
  return r.result?.value;
}

// 늦게 불러오는 사진을 깨우려고 maxHeight 까지 한 화면(stride 배)씩 내린다. toTop 이면 끝나고 맨 위로
export const scrollWakeExpr = (maxHeight, stepMs, { stride = 1, toTop = true } = {}) => `(async () => {
  for (let y = 0; y < Math.min(document.body.scrollHeight, ${maxHeight}); y += innerHeight * ${stride}) {
    scrollTo(0, y);
    await new Promise((r) => setTimeout(r, ${stepMs}));
  }
  ${toTop ? "scrollTo(0, 0);" : ""}
})()`;

// 쿠키·동의·알림·앱 설치 창 걷어 내기 — 캡처와 스냅샷이 같이 쓴다
// 이름으로 못 찾는 덮개: 화면에 붙어 있고(fixed/sticky) 「쿠키」 문구가 있으며 화면 절반보다 작은 것. Flour 메뉴의 아래 쿠키 띠가 이름으로는 안 잡혔다
// 빵집 메뉴의 「쿠키」처럼 상품 이름과 겹치지 않게 문장 꼴로만 찾고, 머리·메뉴(header·nav)는 건드리지 않는다
// 한국 사이트의 광고·공지 팝업은 「오늘 하루 그만 보기」「오늘 하루 보지 않기」로 닫는다(집닥 시공사례에 이사 광고 팝업)
const OVERLAY_WORDS = /use (of )?cookies|cookies help|cookie (policy|settings|preferences)|accept (all )?cookies|쿠키(를| 사용| 정책| 설정)|개인정보 수집|오늘(은)? (하루 ?)?(그만 ?보기|보지 않기|열지 않기)|하루 동안 보지 않기|앱(으로|에서) ?(보기|열기|이용하기)|APP ?(열기|설치)|앱 ?설치|모바일 ?웹으로 (볼래요|보기)/i; // 앱 설치 권유 창(오늘의집)
const hideOverlaysExpr = (sel, words) => `(() => {
  const off = (n) => n.style.setProperty("display", "none", "important");
  document.querySelectorAll(${JSON.stringify(sel)}).forEach(off);
  for (const n of document.querySelectorAll("body *")) {
    const cs = getComputedStyle(n), pos = cs.position;
    const floating = pos === "fixed" || pos === "sticky" || (pos === "absolute" && Number(cs.zIndex) >= 1); // 한국 사이트 팝업은 absolute + z-index가 많다
    if (!floating) continue;
    if (n.matches("header, nav") || n.querySelector("nav")) continue;
    const r = n.getBoundingClientRect();
    if (r.height > innerHeight / 2 || !${words}.test(n.textContent || "")) continue;
    off(n);
  }
  // 흐름 안에 박힌 광고 상자(집닥: 「오늘 하루 그만 보기 · 닫기」가 달린 오른쪽 광고): 그 글자에서 위로 올라가며
  // 화면보다 작은 가장 큰 상자를 가린다 — 머리·메뉴·본문 전체는 크기 제한에 걸려 남는다
  const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  for (let t = walker.nextNode(); t; t = walker.nextNode()) {
    if (!/오늘(은)? (하루 ?)?(그만 ?보기|보지 않기|열지 않기)|하루 동안 보지 않기/.test(t.textContent)) continue;
    let box = null;
    for (let el = t.parentElement; el && el !== document.body; el = el.parentElement) {
      const r = el.getBoundingClientRect();
      if (r.width > innerWidth * 0.6 || r.height > innerHeight * 0.85 || el.matches("header, nav, main")) break;
      box = el;
    }
    if (box) off(box);
    // 화면 전체를 덮는 광고 창(교보·예스24 「오늘은 그만보기」): 위로 올라가며 떠 있는(fixed) 가장 바깥 상자를 가린다
    let fixed = null;
    for (let el = t.parentElement; el && el !== document.body; el = el.parentElement) {
      if (el.matches("header, nav, main")) break;
      if (getComputedStyle(el).position === "fixed") fixed = el;
    }
    if (fixed) off(fixed);
  }
  // 글자 없이 화면을 어둡게 덮는 판(광고 창 뒤 그늘)
  for (const n of document.querySelectorAll("body *")) {
    const cs = getComputedStyle(n);
    if (cs.position !== "fixed" || (n.textContent || "").trim()) continue;
    const r = n.getBoundingClientRect();
    if (r.width >= innerWidth * 0.9 && r.height >= innerHeight * 0.8) off(n);
  }
})()`;
const OVERLAY_SELECTORS = '[id*="cookie" i],[class*="cookie" i],[id*="consent" i],[class*="consent" i],[id*="onetrust" i],[class*="onetrust" i],[id*="termly" i],[id*="klaviyo" i],[class*="klaviyo" i],[id*="onesignal" i],[class*="newsletter-popup" i],[aria-modal="true"]';
export const HIDE_OVERLAYS = hideOverlaysExpr(OVERLAY_SELECTORS, OVERLAY_WORDS);

// 플러그인 훅이 답이 끝날 때·세션을 닫을 때 부른다: node browser.mjs --sweep
// 주인 도구가 끝났는데 남은 headless 브라우저와 임시 프로필을 치운다(남은 것이 있을 때만 한 줄 알림)
/** 이 파일을 직접 실행했는지. 정션·심볼릭 링크(~/.claude/skills/… → 저장소)로 불러도 맞게 실제 경로로 견준다 — 주소 문자열로 견주면 아무 일 없이 exit 0 으로 끝났다(치과 17차). */
export function isMain(metaUrl) {
  if (!process.argv[1]) return false;
  const real = (p) => { try { return realpathSync(p); } catch { return resolve(p); } };
  return real(process.argv[1]) === real(fileURLToPath(metaUrl));
}

if (process.argv[2] === "--sweep" && isMain(import.meta.url)) {
  const n = sweepOrphans();
  if (n) console.log(JSON.stringify({ systemMessage: `남아 있던 측정용 브라우저 ${n}벌을 끄고 임시 폴더를 지웠습니다(ui-design-director).` }));
}
