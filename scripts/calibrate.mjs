#!/usr/bin/env node
// 세 쪽 비교 맞춤 — docs/세-쪽-정답.json 의 회차를 다시 재서 기대(통과·실패)와 다른 것을 알린다.
// 판정 도구를 고칠 때마다 한 번 돌린다: 하나를 고치면 다른 회차 판정이 바뀌는지 몰랐다(21~40차에 도구 고침 9번).
// 사용: node scripts/calibrate.mjs <시안 폴더>   (회차마다 바탕 사이트를 띄워 2~4분)
import { mkdtempSync, readFileSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { dirname, join } from "node:path";
import { spawnSync } from "node:child_process";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const root = process.argv[2];
if (!root) { console.error("사용: node scripts/calibrate.mjs <시안 폴더>"); process.exit(2); }
const { cases } = JSON.parse(readFileSync(join(here, "..", "docs", "세-쪽-정답.json"), "utf8"));
const tmp = mkdtempSync(join(tmpdir(), "calib-"));
let wrong = 0;
try {
  for (const c of cases) {
    const r = spawnSync(process.execPath, [join(here, "triad.mjs"), join(tmp, "t.md"), `base=${c.base}`, `ours=${join(root, c.ours)}`, `ai=${join(root, c.ai)}`],
      { encoding: "utf8", timeout: 600000 });
    const rows = (r.stdout || "").split(/\r?\n/).filter((l) => /^\d+px — /.test(l));
    if (rows.length < 2) { console.log(`?? ${c.label}: 재지 못함 ${(r.stderr || "").split(/\r?\n/)[0]}`); wrong++; continue; }
    const pass = rows.every((l) => { const m = l.match(/오답지 쪽 (\d+)개.*우리만 다름 (\d+)개/); return m && Number(m[1]) <= 1 && Number(m[2]) === 0; });
    const got = pass ? "통과" : "실패";
    if (got !== c.expect) wrong++;
    console.log(`${got === c.expect ? "맞음" : "틀림"}  ${c.label}: 기대 ${c.expect}, 판정 ${got} — ${rows.map((l) => l.replace(/ · /g, " ")).join(" / ")}`);
  }
} finally { rmSync(tmp, { recursive: true, force: true }); }
console.log(`정답표 ${cases.length}건 중 틀림 ${wrong}건`);
process.exit(wrong ? 1 : 0);
