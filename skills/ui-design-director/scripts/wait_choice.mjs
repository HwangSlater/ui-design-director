#!/usr/bin/env node
/*
 * 비교 화면의 「이걸로 확정」 단추를 기다린다. 외부 패키지 없음.
 *
 *   node wait_choice.mjs <page.html> <decision.json> [--hash "p=A&v=pc"] [--minutes 120]
 *
 * - 127.0.0.1 의 빈 포트에서 기다린다(내 컴퓨터 밖에서는 닿지 않음).
 * - 한 번만 쓰는 열쇠를 만들어, 열쇠가 맞는 확정만 받는다.
 * - 시작하면 사용자에게 줄 주소를 한 줄로 찍는다:  OPEN file:///…/page.html#…&wait=<포트>-<열쇠>
 * - 확정이 오면 decision.json 에 쓰고 CHOSEN 줄을 찍고 끝난다(종료 코드 0).
 *   시간이 다 되면 3, 잘못 부르면 2.
 * 에이전트는 이것을 백그라운드로 돌리고, 끝나면 decision.json 을 읽어 다음 단계로 간다.
 */
import { createServer } from "node:http";
import { randomBytes } from "node:crypto";
import { writeFileSync, existsSync } from "node:fs";
import { resolve } from "node:path";
import { pathToFileURL } from "node:url";

const DEFAULT_MINUTES = 120;
const MAX_BODY = 8 * 1024; // 확정 한 건은 몇백 바이트면 충분하다
const HOST = "127.0.0.1";

function usage(msg) {
  if (msg) console.error(`ERROR: ${msg}`);
  console.error('usage: node wait_choice.mjs <page.html> <decision.json> [--hash "p=A&v=pc"] [--minutes 120]');
  process.exit(2);
}

const args = process.argv.slice(2);
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

const token = randomBytes(16).toString("hex");
const CORS = {
  // 비교 화면은 file:// 에서 열리므로 출처가 "null" 이다. 열쇠로 거른다.
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Methods": "POST, OPTIONS",
  "Access-Control-Allow-Headers": "Content-Type",
  "Access-Control-Allow-Private-Network": "true",
};

function reply(res, status, body) {
  res.writeHead(status, { ...CORS, "Content-Type": "application/json; charset=utf-8" });
  res.end(JSON.stringify(body));
}

function isValid(d) {
  return d && typeof d === "object" && d.token === token
    && typeof d.label === "string" && d.label.length > 0 && d.label.length <= 300
    && (d.choice === undefined || (typeof d.choice === "object" && d.choice !== null));
}

let done = false;
const server = createServer((req, res) => {
  if (req.method === "OPTIONS") return reply(res, 204, {});
  if (req.method !== "POST" || req.url !== "/choice") return reply(res, 404, { ok: false });
  let size = 0;
  const chunks = [];
  req.on("data", (c) => {
    size += c.length;
    if (size > MAX_BODY) { reply(res, 413, { ok: false }); req.destroy(); return; }
    chunks.push(c);
  });
  req.on("end", () => {
    if (res.writableEnded) return; // 너무 커서 이미 거절함
    if (done) return reply(res, 409, { ok: false, reason: "already-chosen" });
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
    console.log(`CHOSEN ${decision.label}`);
    console.log(`WROTE ${out}`);
    server.close(() => process.exit(0));
  });
});

server.listen(0, HOST, () => {
  const { port } = server.address();
  const url = pathToFileURL(page).href + "#" + [opts.hash, `wait=${port}-${token}`].filter(Boolean).join("&");
  console.log(`OPEN ${url}`);
  console.log(`WAITING up to ${opts.minutes} min on ${HOST}:${port}`);
});

setTimeout(() => {
  console.log("TIMEOUT no choice received");
  server.close(() => process.exit(3));
}, opts.minutes * 60 * 1000).unref();
