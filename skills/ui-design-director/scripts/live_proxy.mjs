#!/usr/bin/env node
// 다른 페이지 안에 띄우는 걸 막는 참고 사이트(X-Frame-Options, CSP frame-ancestors)도 실시간 보기 화면에 띄운다.
// 사용: node live_proxy.mjs <make_live_board.py 로 만든 보드.html> <spec.json>
//   → 「OPEN http://127.0.0.1:<보드 포트>/<보드>?proxy=…」 를 찍는다. 그 주소를 사용자에게 준다. Ctrl+C 로 끈다.
// 방법은 willyogo/iframe-proxy(MIT)의 생각을 빌려 외부 패키지 없이 다시 썼다:
//   막는 응답 머리를 지우고, <base> 로 그림·글꼴은 원래 사이트에서 바로 받게 하고, 페이지 안 링크·fetch·XHR 을 이 프록시로 돌린다.
// 안전: 127.0.0.1 에만 열고, 주소마다 한 번 쓰는 열쇠, spec 의 후보 사이트(와 그 하위 도메인)만, 읽기(GET·HEAD)만,
//   쿠키는 보내지도 받지도 않는다. 보드와 프록시는 포트를 달리해 서로 다른 출처 — 샌드박스 안 페이지가 보드를 건드리지 못한다.
// 한계: 로그인·웹소켓·자기 서버에 쓰기(POST)가 필요한 화면, 스크립트가 화면을 숨겨 버리는 곳은 그대로 안 보인다 → 그런 후보는 capture.mjs 그림으로.
import { createServer } from "node:http";
import { readFileSync, existsSync, statSync } from "node:fs";
import { dirname, join, resolve, extname, basename, sep } from "node:path";
import { randomBytes } from "node:crypto";

const PHONE_UA = "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1";
const DESKTOP_UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36";
const TIMEOUT_MS = 20000;
const PARSE_BASE = "http://local.invalid"; // lint:allow url 요청 경로만 읽으려고 붙이는 가짜 바탕 주소(어디에도 접속하지 않음)
const DROP_HEADERS = ["x-frame-options", "content-security-policy", "content-security-policy-report-only", "set-cookie", "content-length", "content-encoding", "transfer-encoding", "strict-transport-security", "cross-origin-opener-policy", "cross-origin-embedder-policy", "cross-origin-resource-policy"];
const TYPES = { ".html": "text/html; charset=utf-8", ".css": "text/css", ".js": "text/javascript", ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".png": "image/png", ".webp": "image/webp", ".svg": "image/svg+xml", ".json": "application/json" };

const [boardPath, specPath] = process.argv.slice(2);
if (!boardPath || !specPath || !existsSync(boardPath) || !existsSync(specPath)) {
  console.error("사용: node live_proxy.mjs <보드.html> <spec.json>");
  process.exit(2);
}
const spec = JSON.parse(readFileSync(specPath, "utf8"));
const allowed = new Set((spec.candidates || []).flatMap((c) => Object.values(c.pages || {})).map((u) => new URL(u).hostname.replace(/^www\./, "")));
const okHost = (h) => [...allowed].some((a) => h === a || h.endsWith("." + a));
const key = randomBytes(12).toString("hex");
const boardDir = resolve(dirname(boardPath));

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

// 보드 쪽: 보드 폴더 안의 파일만 읽기 전용으로
const boardServer = createServer((req, res) => {
  const path = decodeURIComponent(new URL(req.url, PARSE_BASE).pathname).replace(/^\/+/, "");
  const file = resolve(boardDir, path || basename(boardPath));
  if (req.method !== "GET" || !file.startsWith(boardDir + sep) || !existsSync(file) || !statSync(file).isFile()) {
    res.writeHead(404); res.end(); return;
  }
  sendFile(res, file);
});

// 프록시 쪽: /<열쇠>/<인코딩한 주소>?ua=phone|pc
let proxyBase = "";
const proxyServer = createServer(async (req, res) => {
  const u = new URL(req.url, PARSE_BASE);
  const [, k, enc] = u.pathname.split("/");
  if (k !== key || !enc || !["GET", "HEAD"].includes(req.method)) { res.writeHead(403); res.end(); return; }
  let target;
  try { target = new URL(decodeURIComponent(enc)); } catch { res.writeHead(400); res.end(); return; }
  if (!/^https?:$/.test(target.protocol) || !okHost(target.hostname)) { res.writeHead(403); res.end("후보 사이트가 아님"); return; }
  const ua = u.searchParams.get("ua") === "phone" ? "phone" : "pc";
  const js = u.searchParams.get("js") === "1";
  try {
    const up = await fetch(target, { method: req.method, redirect: "follow", headers: { "user-agent": ua === "phone" ? PHONE_UA : DESKTOP_UA, "accept-language": "ko-KR,ko;q=0.9" }, signal: AbortSignal.timeout(TIMEOUT_MS) });
    const headers = {};
    up.headers.forEach((v, h) => { if (!DROP_HEADERS.includes(h)) headers[h] = v; });
    headers["access-control-allow-origin"] = "*";
    const type = up.headers.get("content-type") || "";
    if (type.includes("text/css")) {
      // 스타일시트 안의 url()·@import 는 프록시 주소 기준으로 풀리면 깨진다 — 원래 주소로 바꿔 둔다
      const css = (await up.text()).replace(/url\(\s*(['"]?)([^'")]+)\1\s*\)/g, (m, q, ref) => (/^(data:|#)/.test(ref) ? m : `url("${new URL(ref, up.url).href}")`));
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
    // 같은 사이트의 스타일시트도 프록시로 — 남의 사이트에서 파일을 못 쓰게 하는 머리(Cross-Origin-Resource-Policy) 때문에 당근이 글자만 나왔다
    body = body.replace(/<link\b[^>]*>/gi, (tag) => {
      if (!/rel=["']?stylesheet/i.test(tag)) return tag;
      return tag.replace(/\s(integrity|crossorigin)(=("[^"]*"|'[^']*'|[^\s>]*))?/gi, "").replace(/href=(["'])([^"']+)\1/i, (m, q, ref) => {
        const abs = new URL(ref, up.url);
        return okHost(abs.hostname) ? `href=${q}${proxyBase}${encodeURIComponent(abs.href)}?ua=${ua}${q}` : m;
      });
    });
    if (!js) {
      // 기본은 사이트 스크립트 없이 — 남의 주소에서 돌면 머리를 다시 짜며 스타일을 지워 당근이 글자만 나왔다. 네이버 지도는 없어도 같았다.
      // 링크는 여기서 바꿔 둔다: 같은 사이트는 프록시로, 다른 사이트는 새 창으로
      body = body.replace(/<script\b(?![^>]*application\/ld\+json)[^>]*>[\s\S]*?<\/script>/gi, "");
      body = body.replace(/<a\b[^>]*>/gi, (tag) => tag.replace(/href=(["'])([^"']*)\1/i, (m, q, ref) => {
        let abs; try { abs = new URL(ref, up.url); } catch { return m; }
        if (!/^https?:$/.test(abs.protocol)) return m;
        return okHost(abs.hostname) ? `href=${q}${proxyBase}${encodeURIComponent(abs.href)}?ua=${ua}${q}` : `href=${q}${abs.href}${q} target=${q}_blank${q} rel=${q}noopener${q}`;
      }));
    }
    const head = `<base href="${up.url.replace(/"/g, "&quot;")}">${js ? inject(proxyBase, ua) : ""}`;
    body = /<head[^>]*>/i.test(body) ? body.replace(/<head[^>]*>/i, (m) => m + head) : head + body;
    headers["content-type"] = "text/html; charset=utf-8";
    res.writeHead(up.status, headers);
    res.end(body);
  } catch (err) {
    res.writeHead(502, { "content-type": "text/plain; charset=utf-8" });
    res.end(`가져오지 못함: ${err.message}`);
  }
});

const listen = (srv) => new Promise((r) => srv.listen(0, "127.0.0.1", () => r(srv.address().port)));
const pPort = await listen(proxyServer);
proxyBase = `http://127.0.0.1:${pPort}/${key}/`;
const bPort = await listen(boardServer);
console.log(`허용 사이트: ${[...allowed].join(", ")}`);
console.log(`OPEN http://127.0.0.1:${bPort}/${encodeURIComponent(basename(boardPath))}?proxy=${encodeURIComponent(proxyBase)}`);
console.log("끄려면 Ctrl+C");
