#!/usr/bin/env node
/*
 * 비교 화면의 「이걸로 확정」 단추를 기다린다. 외부 패키지 없음.
 *
 *   node wait_choice.mjs <page.html> <decision.json> [--hash "p=A&v=pc"] [--minutes 120]
 *
 * - 127.0.0.1 의 빈 포트에서 기다린다(내 컴퓨터 밖에서는 닿지 않음).
 * - 한 번만 쓰는 열쇠를 만들어, 열쇠가 맞는 확정만 받는다.
 * - 비교 화면이 있는 폴더를 같은 주소(http://127.0.0.1:<포트>/)로 함께 내준다. 화면과 받는 곳이 같은 주소라
 *   브라우저가 「로컬 네트워크 접근」을 막거나 묻지 않는다(file:// 로 열면 Chrome 이 막을 수 있다).
 * - 시작하면 사용자에게 줄 주소를 한 줄로 찍는다:  OPEN http://127.0.0.1:<포트>/page.html#…&wait=<포트>-<열쇠>
 * - 확정이 오면 decision.json 에 쓰고 CHOSEN 줄을 찍고 끝난다(종료 코드 0).
 *   시간이 다 되면 3, 잘못 부르면 2.
 * 에이전트는 이것을 백그라운드로 돌리고, 끝나면 decision.json 을 읽어 다음 단계로 간다.
 * 후보 보기 화면은 live_proxy.mjs 가 이 파일의 choiceHandler 로 같은 주소에서 확정을 받는다 — 이것은 팔레트 화면용.
 */
import { createServer } from "node:http";
import { randomBytes } from "node:crypto";
import { writeFileSync, existsSync, readFile, statSync, realpathSync } from "node:fs";
import { resolve, dirname, basename, extname, sep } from "node:path";
import { fileURLToPath } from "node:url";

const DEFAULT_MINUTES = 120;
const MAX_BODY = 8 * 1024; // 확정 한 건은 몇백 바이트면 충분하다
export const HOST = "127.0.0.1";
// dock.js 가 읽는 주소 꼴 wait=<포트>-<열쇠>: 열쇠는 16바이트(16진수 32자)여야 한다
export const newChoiceToken = () => randomBytes(16).toString("hex");
export const waitHash = (port, token) => `wait=${port}-${token}`;

const CORS = {
  // 비교 화면은 file:// 에서 열리므로 출처가 "null" 이다. 열쇠로 거른다.
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Methods": "POST, OPTIONS",
  "Access-Control-Allow-Headers": "Content-Type",
  "Access-Control-Allow-Private-Network": "true",
};

export function reply(res, status, body) {
  res.writeHead(status, { ...CORS, "Content-Type": "application/json; charset=utf-8" });
  res.end(JSON.stringify(body));
}

/*
 * 「확정」 받는 곳(POST /choice) — wait_choice.mjs 와 live_proxy.mjs 가 함께 쓴다.
 * token: 한 번 쓰는 열쇠 · out: 확정을 쓸 파일 · once: 첫 확정 뒤에는 409 로 거절(false 면 다시 확정하면 덮어쓴다)
 * onChosen(decision): 파일을 쓴 뒤 부른다.
 * 돌려주는 함수 handle(req, res) 는 확정 요청(OPTIONS·POST /choice)이면 처리하고 true, 아니면 false.
 */
export function choiceHandler({ token, out, once = true, onChosen = () => {} }) {
  let done = false;
  const isValid = (d) => d && typeof d === "object" && d.token === token
    && typeof d.label === "string" && d.label.length > 0 && d.label.length <= 300
    && (d.choice === undefined || (typeof d.choice === "object" && d.choice !== null));
  return function handle(req, res) {
    if (req.method === "OPTIONS") { reply(res, 204, {}); return true; }
    if (req.method !== "POST") return false;
    if (req.url !== "/choice") { reply(res, 404, { ok: false }); return true; }
    let size = 0;
    const chunks = [];
    req.on("data", (c) => {
      size += c.length;
      if (size > MAX_BODY) { reply(res, 413, { ok: false }); req.destroy(); return; }
      chunks.push(c);
    });
    req.on("end", () => {
      if (res.writableEnded) return; // 너무 커서 이미 거절함
      if (once && done) return reply(res, 409, { ok: false, reason: "already-chosen" });
      let data;
      try { data = JSON.parse(Buffer.concat(chunks).toString("utf8")); } catch { return reply(res, 400, { ok: false }); }
      if (!isValid(data)) return reply(res, 403, { ok: false });
      done = true;
      const { token: _drop, ...decision } = data; // 열쇠는 기록에 남기지 않는다
      decision.received_at = new Date().toISOString();
      try {
        writeFileSync(out, JSON.stringify(decision, null, 1), "utf8");
      } catch (err) {
        done = false;
        console.error(`ERROR: could not write ${out}: ${err.message}`);
        return reply(res, 500, { ok: false });
      }
      reply(res, 200, { ok: true });
      onChosen(decision);
    });
    return true;
  };
}

function usage(msg) {
  if (msg) console.error(`ERROR: ${msg}`);
  console.error('usage: node wait_choice.mjs <page.html> <decision.json> [--hash "p=A&v=pc"] [--minutes 120]');
  process.exit(2);
}

const TYPES = {
  ".html": "text/html; charset=utf-8", ".css": "text/css; charset=utf-8", ".js": "text/javascript; charset=utf-8",
  ".json": "application/json; charset=utf-8", ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".png": "image/png",
  ".webp": "image/webp", ".svg": "image/svg+xml", ".woff": "font/woff", ".woff2": "font/woff2",
};

// 비교 화면 폴더 안의 파일만 읽기 전용으로 내준다. 폴더 밖·목록 보기·모르는 형식은 거절.
function serveFile(root, req, res) {
  let rel;
  try { rel = decodeURIComponent(new URL(req.url, "http://x").pathname); } catch { return reply(res, 400, { ok: false }); } // lint:allow url 요청 경로만 읽는 가짜 바탕 주소
  const file = resolve(root, "." + rel);
  const type = TYPES[extname(file).toLowerCase()];
  if (!(file === root || file.startsWith(root + sep)) || !type) return reply(res, 404, { ok: false });
  let st;
  try { st = statSync(file); } catch { return reply(res, 404, { ok: false }); }
  if (!st.isFile()) return reply(res, 404, { ok: false });
  readFile(file, (err, data) => {
    if (err) return reply(res, 500, { ok: false });
    res.writeHead(200, { "Content-Type": type, "Cache-Control": "no-store", "X-Content-Type-Options": "nosniff" });
    res.end(data);
  });
}

function main(args) {
  const opts = { hash: "", minutes: DEFAULT_MINUTES };
  const pos = [];
  for (let i = 0; i < args.length; i++) {
    if (args[i] === "--hash") opts.hash = (args[++i] || "").replace(/^#/, "");
    else if (args[i] === "--minutes") opts.minutes = Number(args[++i]);
    else pos.push(args[i]);
  }
  if (pos.length !== 2) usage();
  const [page, out] = pos.map((p) => resolve(p));
  if (!existsSync(page)) usage(`page not found: ${page}`);
  if (!(opts.minutes > 0)) usage("--minutes must be a positive number");

  const token = newChoiceToken();
  const root = dirname(page);
  const onChoice = choiceHandler({
    token, out,
    onChosen: (decision) => {
      console.log(`CHOSEN ${decision.label}`);
      console.log(`WROTE ${out}`);
      server.close(() => process.exit(0));
    },
  });
  const server = createServer((req, res) => {
    if (onChoice(req, res)) return;
    if (req.method === "GET") return serveFile(root, req, res);
    reply(res, 404, { ok: false });
  });

  server.listen(0, HOST, () => {
    const { port } = server.address();
    const url = `http://${HOST}:${port}/${encodeURIComponent(basename(page))}#` + [opts.hash, waitHash(port, token)].filter(Boolean).join("&"); // lint:allow url 내 컴퓨터 안(127.0.0.1)에서 연 기다리기 주소
    console.log(`OPEN ${url}`);
    console.log(`WAITING up to ${opts.minutes} min on ${HOST}:${port}`);
  });

  setTimeout(() => {
    console.log("TIMEOUT no choice received");
    server.close(() => process.exit(3));
  }, opts.minutes * 60 * 1000).unref();
}

// live_proxy.mjs 가 choiceHandler 만 가져다 쓸 때는 기다리기를 시작하지 않는다
const self = (p) => { try { return realpathSync(p); } catch { return resolve(p); } };
if (process.argv[1] && self(process.argv[1]) === self(fileURLToPath(import.meta.url))) main(process.argv.slice(2));
