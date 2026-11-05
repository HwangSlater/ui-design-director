// skeleton_base.mjs 시험 — 바탕(고른 템플릿)을 따르고, 관련 사이트 여럿이 함께 다르게 하는 곳만 바꾼다.
// 실행: node --test tests/test_skeleton_base.mjs
import { test } from "node:test";
import assert from "node:assert/strict";
import { join, dirname } from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";

const MOD = join(dirname(fileURLToPath(import.meta.url)), "..", "skills", "ui-design-director", "scripts", "skeleton_base.mjs");
const { baseDiff } = await import(pathToFileURL(MOD).href);

const site = (host, o = {}) => ({ host, stack: 0.6, maxCols: 3, navTop: true, heroPhoto: true, callEnd: true, hscroll: 0, roundShare: 0, photoRad: 0, btnShape: "각진", ...o });

test("여럿이 함께 다르게 하는 것만 바꿀 곳", () => {
  const base = site("tmpl", { hscroll: 0, callEnd: false });
  const others = [site("a", { hscroll: 2 }), site("b", { hscroll: 1 }), site("c")];
  const d = baseDiff(base, others);
  const keys = d.changes.map((c) => c.key);
  assert.ok(keys.includes("hscroll"), "옆 띠 2/3곳");
  assert.ok(keys.includes("callEnd"), "끝 전화 3/3곳");
  assert.ok(!keys.includes("cols3"), "바탕과 같은 것은 그대로");
});

test("한 곳만 다르면 바꾸지 않는다", () => {
  const d = baseDiff(site("tmpl"), [site("a", { roundShare: 0.5 }), site("b"), site("c")]);
  assert.equal(d.changes.length, 0);
});

test("같은 주소의 여러 쪽은 한 곳으로 센다", () => {
  const naver = [site("map.naver.com", { hscroll: 3 }), site("map.naver.com", { hscroll: 2 }), site("map.naver.com", { hscroll: 1 })];
  const d = baseDiff(site("tmpl"), [...naver, site("b")]);
  assert.ok(!d.changes.some((c) => c.key === "hscroll"), "네이버 세 쪽이 한 곳 — 2곳 중 1곳");
});

test("우리 시안이 바꿀 곳 말고 바탕과 다르면 알린다", () => {
  const base = site("tmpl", { stack: 0.5, hscroll: 0 });
  const others = [site("a", { hscroll: 2 }), site("b", { hscroll: 1 })];
  const me = site("ours", { stack: 0.95, hscroll: 1, heroPhoto: false });
  const d = baseDiff(base, others, me);
  assert.ok(d.notes.some((n) => n.includes("첫 화면이 큰 사진")), "바탕엔 있는 큰 사진을 뺌");
  assert.ok(!d.notes.some((n) => n.includes("옆으로 넘기는 띠")), "옆 띠는 바꿀 곳이라 괜찮음");
  assert.ok(d.notes.some((n) => n.includes("짜임을 버림")), "한 단 50% → 95%");
});

test("바탕에 단추가 없으면(「—」) 단추 모양은 바꿀 곳이 아니다", () => {
  const d = baseDiff(site("tmpl", { btnShape: "—" }), [site("a"), site("b"), site("c")]);
  assert.ok(!d.changes.some((c) => c.key === "btnShape"));
});
