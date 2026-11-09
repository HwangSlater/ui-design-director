#!/usr/bin/env node
// 다른 페이지 안에 띄우는 걸 막는 참고 사이트(X-Frame-Options, CSP frame-ancestors)도 실시간 보기 화면에 띄운다.
// 사용: node live_proxy.mjs <spec.json> [--decision <decision.json>]  — 공용 틀 보기 화면(보기.html)을 만들어 연다.
//   이미 만든 화면이면 <보기.html> <spec.json>. --decision 을 안 주면 보기 화면 옆 decision.json.
//   → 「OPEN http://127.0.0.1:<보드 포트>/<보드>?proxy=…#wait=…」 한 줄을 찍는다. 그 주소 하나만 사용자에게 준다.
//   의뢰인이 「확정」을 누르면 decision.json 을 쓰고 「DECISION <고른 것>」을 찍은 뒤 계속 띄운다(다시 확정하면 덮어쓴다). Ctrl+C 로 끈다.
// 방법은 willyogo/iframe-proxy(MIT)의 생각을 빌려 외부 패키지 없이 다시 썼다:
//   막는 응답 머리를 지우고, <base> 로 그림·글꼴은 원래 사이트에서 바로 받게 하고, 페이지 안 링크·fetch·XHR 을 이 프록시로 돌린다.
// 안전: 127.0.0.1 에만 열고, 주소마다 한 번 쓰는 열쇠(프록시·확정 따로), 넘겨주기(redirect)도 후보 사이트로만 최대 5번, spec 의 후보 사이트(와 그 하위 도메인)만, 읽기(GET·HEAD)만,
//   쿠키는 보내지도 받지도 않는다. 보드와 프록시는 포트를 달리해 서로 다른 출처 — 샌드박스 안 페이지가 보드를 건드리지 못한다.
// 더한 것: 브라우저 같은 요청 머리(보안 장치 통과), 같은 사이트 글꼴은 프록시로(출처가 달라 글꼴이 막힘), 스크립트 없이 띄울 때 늦게 불러오는 사진·noscript 를 보이게,
//   ?probe=1 로 「스크립트 없이는 빈 화면인가」를 보드에 알려 준다(보드가 스크립트를 켤지 정한다).
// 한계: 로그인·웹소켓·자기 서버에 쓰기(POST)가 필요한 화면, 스크립트가 화면을 숨겨 버리는 곳은 그대로 안 보인다 → 그런 후보는 capture.mjs 그림으로.
import { createServer } from "node:http";
import { readFileSync, existsSync, statSync } from "node:fs";
import { dirname, join, resolve, extname, basename, sep } from "node:path";
import { randomBytes } from "node:crypto";
import { spawnSync } from "node:child_process";
import { fileURLToPath } from "node:url";
import { choiceHandler, newChoiceToken, waitHash, HOST } from "./wait_choice.mjs";

// 브라우저 이름은 측정 도구와 같은 한 곳(assets/browser.json) — 버전이 도구마다 달랐다
const BROWSER = JSON.parse(readFileSync(join(dirname(fileURLToPath(import.meta.url)), "..", "assets", "browser.json"), "utf8"));
const PHONE_UA = BROWSER.phoneUA;
const DESKTOP_UA = BROWSER.desktopUA;
const TIMEOUT_MS = 20000;
const MAX_HOPS = 5; // 넘겨주기를 따라가는 최대 횟수 — 매번 후보 사이트인지 다시 본다
const REDIRECTS = new Set([301, 302, 303, 307, 308]);
// 브라우저가 보내는 머리를 갖춘다 — 머리가 빈 요청은 보안 장치가 막았다(건축사무소 OBBA: 「request blocked」)
const browserHeaders = (ua, target, kind) => ({
  "user-agent": ua === "phone" ? PHONE_UA : DESKTOP_UA,
  "accept": kind === "doc" ? "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8" : "*/*",
  "accept-language": BROWSER.acceptLanguage,
  "upgrade-insecure-requests": "1",
  "sec-fetch-dest": kind === "doc" ? "document" : "empty",
  "sec-fetch-mode": kind === "doc" ? "navigate" : "cors",
  "sec-fetch-site": "none",
  "referer": target.origin + "/",
});
const FONT_RE = /\.(woff2?|ttf|otf|eot)(\?|#|$)/i;
const ASSET_RE = /\.(css|js|mjs|json|woff2?|ttf|otf|eot|png|jpe?g|gif|webp|avif|svg)(\?|#|$)/i;
const TEXT_MIN = 200; // 스크립트를 빼고 남은 글이 이보다 적으면 스크립트로 그리는 사이트로 보고 스크립트를 살린다
const PARSE_BASE = "http://local.invalid"; // lint:allow url 요청 경로만 읽으려고 붙이는 가짜 바탕 주소(어디에도 접속하지 않음)
const DROP_HEADERS = ["x-frame-options", "content-security-policy", "content-security-policy-report-only", "set-cookie", "content-length", "content-encoding", "transfer-encoding", "strict-transport-security", "cross-origin-opener-policy", "cross-origin-embedder-policy", "cross-origin-resource-policy"];
const TYPES = { ".html": "text/html; charset=utf-8", ".css": "text/css", ".js": "text/javascript", ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".png": "image/png", ".webp": "image/webp", ".svg": "image/svg+xml", ".json": "application/json" };

// 보기 화면은 늘 공용 틀(make_board.py 의 아래 막대·썸네일·확정)이다 — 따로 짠 화면은 열지 않는다(사용자가 「우리 템플릿을 안 따랐다」고 짚었다).
// 인자가 spec 하나면 그 옆에 「보기.html」을 공용 틀로 직접 만든 뒤 연다.
const SHARED_MARK = /id=["']board-data["'][\s\S]*board\.js|board\.js[\s\S]*id=["']board-data["']/;
const argv = process.argv.slice(2);
const di = argv.indexOf("--decision");
let decisionPath = di >= 0 ? argv.splice(di, 2)[1] : "";
let [boardPath, specPath] = argv;
if (boardPath && !specPath && boardPath.endsWith(".json")) {
  specPath = boardPath;
  boardPath = join(dirname(resolve(specPath)), "보기.html");
  const py = process.env.PYTHON || (process.platform === "win32" ? "python" : "python3");
  const r = spawnSync(py, ["-X", "utf8", join(dirname(fileURLToPath(import.meta.url)), "make_live_board.py"), specPath, boardPath], { stdio: "inherit", env: { ...process.env, UIDD_FROM_PROXY: "1" } }); // 안에서 부를 때는 「프록시로 띄우라」 안내를 다시 찍지 않게
  if (r.status !== 0) { console.error("공용 틀 보기 화면을 만들지 못했어요(make_live_board.py)"); process.exit(1); }
  const live = join(dirname(resolve(specPath)), basename(specPath, ".json") + "-live.json");
  if (existsSync(live)) specPath = live;
}
if (!boardPath || !specPath || !existsSync(boardPath) || !existsSync(specPath) || (di >= 0 && !decisionPath)) {
  console.error("사용: node live_proxy.mjs <spec.json> [--decision <decision.json>]   (공용 틀 보기 화면을 만들어 연다)\n      node live_proxy.mjs <make_board·make_live_board 로 만든 보기.html> <spec.json> [--decision <decision.json>]");
  process.exit(2);
}
if (!SHARED_MARK.test(readFileSync(boardPath, "utf8"))) {
  console.error(`공용 틀이 아닌 보기 화면이에요: ${boardPath}\n→ python scripts/make_live_board.py <spec.json> <out.html> 로 만들거나 node live_proxy.mjs <spec.json> 로 여세요. 보기 화면을 직접 짜지 않습니다.`);
  process.exit(3);
}
const spec = JSON.parse(readFileSync(specPath, "utf8"));
const allowed = new Set((spec.candidates || []).flatMap((c) => Object.values(c.pages || c.urls || {})).map((u) => new URL(u).hostname.replace(/^www\./, "")));
const okHost = (h) => [...allowed].some((a) => h === a || h.endsWith("." + a));
const key = randomBytes(12).toString("hex");
const boardDir = resolve(dirname(boardPath));
decisionPath = resolve(decisionPath || join(boardDir, "decision.json"));
const choiceToken = newChoiceToken();

// 페이지 안에 넣는 스크립트: 같은 사이트로 가는 링크·fetch·XHR 을 프록시로, 다른 사이트 링크는 새 창으로
const inject = (proxyBase, ua) => `<script>(()=>{const P=${JSON.stringify(proxyBase)},U=${JSON.stringify(ua)},A=${JSON.stringify([...allowed])};
const ok=(h)=>A.some((a)=>h===a||h.endsWith("."+a)||h==="www."+a);
const wrap=(u)=>{try{const x=new URL(u,document.baseURI);return ok(x.hostname)&&/^https?:$/.test(x.protocol)?P+encodeURIComponent(x.href)+"?ua="+U+"&js=1":null}catch(e){return null}};
document.addEventListener("click",(e)=>{const a=e.target.closest&&e.target.closest("a[href]");if(!a)return;const w=wrap(a.getAttribute("href"));e.preventDefault();if(w)location.href=w;else window.open(new URL(a.getAttribute("href"),document.baseURI).href,"_blank","noopener")},true);
const f=window.fetch;window.fetch=(i,o)=>{const u=typeof i==="string"?i:i&&i.url;const w=u&&wrap(u);return f(w||i,o)};
const op=XMLHttpRequest.prototype.open;XMLHttpRequest.prototype.open=function(m,u,...r){return op.call(this,m,wrap(u)||u,...r)};
})();</script>`;

const sendFile = (res, file) => {
  res.writeHead(200, { "content-type": TYPES[extname(file).toLowerCase()] || "application/octet-stream", "cache-control": "no-store" });
  res.end(readFileSync(file));
};

// 스타일 안의 url(): 프록시 주소 기준으로 풀리면 깨지므로 원래 주소로. 같은 사이트 글꼴만 프록시로 —
// 우회 페이지와 출처가 달라 브라우저가 글꼴을 막고 기본 글꼴로 그렸다(접근 허용 머리는 프록시가 붙인다)
const fixCssUrls = (css, baseUrl, ua) => css.replace(/url\(\s*(['"]?)([^'")]+)\1\s*\)/g, (m, q, ref) => {
  if (/^(data:|#)/.test(ref)) return m;
  let abs; try { abs = new URL(ref, baseUrl); } catch { return m; }
  if (FONT_RE.test(abs.pathname) && okHost(abs.hostname)) return `url("${proxyBase}${encodeURIComponent(abs.href)}?ua=${ua}")`;
  return `url("${abs.href}")`;
});
// 스크립트 없이 띄울 때: 늦게 불러오는 사진(data-src 등)을 바로 보이게, <noscript> 안의 대체 내용을 꺼낸다
const LAZY_SRC = /\sdata-(?:lazy-)?(?:src|original|url)=(["'])([^"']+)\1/i;
const LAZY_SET = /\sdata-(?:lazy-)?srcset=(["'])([^"']+)\1/i;
const setAttr = (tag, name, value) => (new RegExp(`\\s${name}=(["'])[^"']*\\1`, "i").test(tag)
  ? tag.replace(new RegExp(`\\s${name}=(["'])[^"']*\\1`, "i"), ` ${name}="${value}"`)
  : tag.replace(/^<(\w+)/, `<$1 ${name}="${value}"`));
const unlazy = (html) => html
  .replace(/<noscript>([\s\S]*?)<\/noscript>/gi, "$1")
  .replace(/<(img|source|iframe)\b[^>]*>/gi, (tag) => {
    let t = tag;
    const s = t.match(LAZY_SRC); if (s) t = setAttr(t, "src", s[2]);
    const ss = t.match(LAZY_SET); if (ss) t = setAttr(t, "srcset", ss[2]);
    return t.replace(/\sloading=(["'])lazy\1/i, "");
  })
  .replace(/<(\w+)\b([^>]*?)\sdata-bg(?:-src)?=(["'])([^"']+)\3([^>]*)>/gi, (m, n, a, q, u, b) => `<${n}${a} data-bg="${u}"${b} style="background-image:url('${u}')">`);
const REVEAL_CSS = "[data-aos],[data-sal],[data-scroll],.et_animated,.et_pb_animation_off,.wow,.reveal,.js-reveal,.fade-in,.fadeIn,.animate__animated,.lazyload,.lazyloaded,.lazyloading{opacity:1!important;visibility:visible!important;transform:none!important;animation:none!important}"
  + ".et_pb_slider .et_pb_slide:first-child{display:block!important;opacity:1!important;z-index:1}.et_pb_section,.et_pb_row,.et_pb_module{opacity:1!important}"
  + ".et_pb_preload,.et_pb_preload *{visibility:visible!important;opacity:1!important}.et_pb_preload:before,.et_pb_preload:after{display:none!important}";
const CHALLENGE_RE = /checking your browser|just a moment\.\.\.|verifying you are human|automatic security check|enable javascript and cookies to continue/i;
// 스크립트를 빼고 남는 글의 양 — 적으면 스크립트로 화면을 그리는 사이트
const visibleText = (html) => html.replace(/<(script|style|noscript|template)\b[\s\S]*?<\/\1>/gi, "").replace(/<[^>]+>/g, " ").replace(/&[a-z#0-9]+;/gi, " ").replace(/\s+/g, " ").trim().length;

// 넘겨주기(redirect)를 손으로 따라간다 — 자동으로 따라가면 후보 사이트가 아닌 곳(내부망 주소 등)으로도 갔다.
// 매번 후보 사이트인지 다시 보고, MAX_HOPS 를 넘거나 다른 곳으로 가면 null. 돌려주는 응답의 finalUrl 이 마지막 주소.
const fetchAllowed = async (start, method, ua) => {
  let target = start;
  for (let hop = 0; hop <= MAX_HOPS; hop++) {
    const up = await fetch(target, { method, redirect: "manual", headers: browserHeaders(ua, target, ASSET_RE.test(target.pathname) ? "asset" : "doc"), signal: AbortSignal.timeout(TIMEOUT_MS) });
    const loc = up.headers.get("location");
    if (!REDIRECTS.has(up.status) || !loc) { up.finalUrl = target.href; return up; }
    await up.body?.cancel(); // 넘겨주기 응답의 본문은 버린다(연결을 붙잡지 않게)
    try { target = new URL(loc, target); } catch { return null; }
    if (!/^https?:$/.test(target.protocol) || !okHost(target.hostname)) return null;
  }
  return null;
};

// 보드 쪽: 보드 폴더 안의 파일만 읽기 전용으로 + 「확정」 받는 곳(POST /choice, wait_choice.mjs 와 같은 처리)
const onChoice = choiceHandler({
  token: choiceToken, out: decisionPath, once: false,
  onChosen: (d) => { console.log(`DECISION ${d.label}`); console.log(`WROTE ${decisionPath}`); },
});
const boardServer = createServer((req, res) => {
  if (onChoice(req, res)) return;
  let path;
  try { path = decodeURIComponent(new URL(req.url, PARSE_BASE).pathname).replace(/^\/+/, ""); } catch { res.writeHead(400); res.end(); return; }
  const file = resolve(boardDir, path || basename(boardPath));
  if (req.method !== "GET" || !file.startsWith(boardDir + sep) || !existsSync(file) || !statSync(file).isFile()) {
    res.writeHead(404); res.end(); return;
  }
  sendFile(res, file);
});

// 프록시 쪽: /<열쇠>/<인코딩한 주소>?ua=phone|pc
let proxyBase = "";
const proxyServer = createServer(async (req, res) => {
  let u;
  try { u = new URL(req.url, PARSE_BASE); } catch { res.writeHead(400); res.end(); return; }
  const [, k, enc] = u.pathname.split("/");
  if (k !== key || !enc || !["GET", "HEAD"].includes(req.method)) { res.writeHead(403); res.end(); return; }
  let target;
  try { target = new URL(decodeURIComponent(enc)); } catch { res.writeHead(400); res.end(); return; }
  if (!/^https?:$/.test(target.protocol) || !okHost(target.hostname)) { res.writeHead(403); res.end("후보 사이트가 아님"); return; }
  const ua = u.searchParams.get("ua") === "phone" ? "phone" : "pc";
  const js = u.searchParams.get("js") === "1";
  try {
    const up = await fetchAllowed(target, req.method, ua);
    if (!up) { res.writeHead(403, { "content-type": "text/plain; charset=utf-8" }); res.end("후보 사이트가 아닌 곳으로 넘기거나 넘기기가 너무 많음"); return; }
    const headers = {};
    up.headers.forEach((v, h) => { if (!DROP_HEADERS.includes(h)) headers[h] = v; });
    headers["access-control-allow-origin"] = "*";
    const type = up.headers.get("content-type") || "";
    if (type.includes("text/css")) {
      const css = fixCssUrls(await up.text(), up.finalUrl, ua);
      res.writeHead(up.status, { ...headers, "content-type": "text/css; charset=utf-8" });
      res.end(css);
      return;
    }
    if (!type.includes("text/html")) {
      res.writeHead(up.status, headers);
      res.end(Buffer.from(await up.arrayBuffer()));
      return;
    }
    let body = await up.text();
    body = body.replace(/<meta[^>]+http-equiv=["']?(content-security-policy|x-frame-options)[^>]*>/gi, "");
    body = body.replace(/<style\b([^>]*)>([\s\S]*?)<\/style>/gi, (m, a, css) => `<style${a}>${fixCssUrls(css, up.finalUrl, ua)}</style>`);
    // 보드가 띄우기 전에 묻는다(?probe=1): 스크립트를 빼면 거의 빈 화면인 사이트(스크립트로 그리는 곳)인가.
    // 그렇다면 보드가 스크립트를 허락한 틀로 띄운다 — spec 에 "js": true 를 손으로 붙이지 않아도 된다
    if (u.searchParams.get("probe") === "1") {
      // 글이 거의 없거나, 사이트 대신 「브라우저 확인 중」 화면이 왔을 때(스크립트가 돌아야 통과해 원래 페이지로 넘어간다 —
      // Norm Architects 가 이 화면이라 스크립트 없이 빈 미색으로 보였다)
      const needJs = /<script\b/i.test(body) && (visibleText(body) < TEXT_MIN || CHALLENGE_RE.test(body.slice(0, 20000)));
      res.writeHead(200, { "content-type": "application/json", "access-control-allow-origin": "*", "cache-control": "no-store" });
      res.end(JSON.stringify({ js: needJs, status: up.status }));
      return;
    }
    // 같은 사이트의 스타일시트도 프록시로 — 남의 사이트에서 파일을 못 쓰게 하는 머리(Cross-Origin-Resource-Policy) 때문에 당근이 글자만 나왔다
    body = body.replace(/<link\b[^>]*>/gi, (tag) => {
      if (!/rel=["']?stylesheet/i.test(tag)) return tag;
      return tag.replace(/\s(integrity|crossorigin)(=("[^"]*"|'[^']*'|[^\s>]*))?/gi, "").replace(/href=(["'])([^"']+)\1/i, (m, q, ref) => {
        let abs; try { abs = new URL(ref, up.finalUrl); } catch { return m; }
        return okHost(abs.hostname) ? `href=${q}${proxyBase}${encodeURIComponent(abs.href)}?ua=${ua}${q}` : m;
      });
    });
    if (!js) {
      // 기본은 사이트 스크립트 없이 — 남의 주소에서 돌면 머리를 다시 짜며 스타일을 지워 당근이 글자만 나왔다. 네이버 지도는 없어도 같았다.
      // 링크는 여기서 바꿔 둔다: 같은 사이트는 프록시로, 다른 사이트는 새 창으로
      body = body.replace(/<script\b(?![^>]*application\/ld\+json)[^>]*>[\s\S]*?<\/script>/gi, "");
      body = unlazy(body);
      // 스크립트가 보이게 해 주던 「나타나기」 요소를 처음부터 보이게 — Divi(Norm Architects)·AOS·WOW·늦게 불러오기 표시가 투명한 채 남았다
      body = body.replace(/<\/head>/i, `<style>${REVEAL_CSS}</style></head>`);
      body = body.replace(/<a\b[^>]*>/gi, (tag) => tag.replace(/href=(["'])([^"']*)\1/i, (m, q, ref) => {
        let abs; try { abs = new URL(ref, up.finalUrl); } catch { return m; }
        if (!/^https?:$/.test(abs.protocol)) return m;
        return okHost(abs.hostname) ? `href=${q}${proxyBase}${encodeURIComponent(abs.href)}?ua=${ua}${q}` : `href=${q}${abs.href}${q} target=${q}_blank${q} rel=${q}noopener${q}`;
      }));
    }
    const head = `<base href="${up.finalUrl.replace(/"/g, "&quot;")}">${js ? inject(proxyBase, ua) : ""}`;
    body = /<head[^>]*>/i.test(body) ? body.replace(/<head[^>]*>/i, (m) => m + head) : head + body;
    headers["content-type"] = "text/html; charset=utf-8";
    res.writeHead(up.status, headers);
    res.end(body);
  } catch (err) {
    res.writeHead(502, { "content-type": "text/plain; charset=utf-8" });
    res.end(`가져오지 못함: ${err.message}`);
  }
});

const listen = (srv) => new Promise((r) => srv.listen(0, HOST, () => r(srv.address().port)));
const pPort = await listen(proxyServer);
proxyBase = `http://${HOST}:${pPort}/${key}/`; // lint:allow url 내 컴퓨터 안에서 연 프록시 주소
const bPort = await listen(boardServer);
console.log(`허용 사이트: ${[...allowed].join(", ")}`);
console.log(`OPEN http://${HOST}:${bPort}/${encodeURIComponent(basename(boardPath))}?proxy=${encodeURIComponent(proxyBase)}#${waitHash(bPort, choiceToken)}`); // lint:allow url 내 컴퓨터 안에서 연 보기 화면 주소
console.log(`확정이 오면 ${decisionPath} 에 쓰고 DECISION 줄을 찍는다`);
console.log("끄려면 Ctrl+C");
