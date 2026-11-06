// 캡처·스냅샷이 함께 쓰는 브라우저 띄우기와 DevTools 프로토콜 연결(외부 패키지 없음)
import { spawn } from "node:child_process";
import { existsSync, mkdtempSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { createServer } from "node:net";

// 설치 위치는 운영체제가 알려 주는 폴더에서 찾는다
export const WIN_DIRS = [process.env["ProgramFiles(x86)"], process.env.ProgramFiles, process.env.LOCALAPPDATA].filter(Boolean);
export const BROWSERS = [
  process.env.CAPTURE_BROWSER,
  ...WIN_DIRS.map((d) => join(d, "Microsoft", "Edge", "Application", "msedge.exe")),
  ...WIN_DIRS.map((d) => join(d, "Google", "Chrome", "Application", "chrome.exe")),
  "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
  "/usr/bin/google-chrome",
  "/usr/bin/chromium",
].filter(Boolean);

export const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

export function freePort() {
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

export async function launch() {
  const exe = BROWSERS.find((p) => existsSync(p));
  if (!exe) throw new Error("Edge 또는 Chrome을 찾지 못했습니다. CAPTURE_BROWSER 로 경로를 지정하세요.");
  const port = await freePort();
  const profile = mkdtempSync(join(tmpdir(), "capture-"));
  const proc = spawn(exe, [
    "--headless=new", "--disable-gpu", "--hide-scrollbars", "--no-first-run", "--mute-audio",
    "--disable-blink-features=AutomationControlled",
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
