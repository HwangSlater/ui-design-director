// page_probe.mjs 판정 시험 — 바탕보다 넘치는 상자·띠, 바탕의 85% 아래 사진, 흰 바탕에 크림(빵집 32~36차).
import { test } from "node:test";
import assert from "node:assert/strict";
import { driftLines } from "../skills/ui-design-director/scripts/page_probe.mjs";

const base = { 제목수: 5, 회색한줄: 0, 제목위윗줄: 0, 옅은띠: 0, 진한띠: 0, 끝단추띠: 0, 큰숫자칸: 0, 둥근카드: 2, 펼침질문: 3, 단추: 3, 같은짜임잇달음: 1, 사진비율: 0.8, 바탕색: [255, 255, 255] };

test("바탕과 같으면 걸리지 않는다", () => {
  assert.deepEqual(driftLines(1280, base, { ...base }), []);
});

test("회색 한 줄·옅은 띠·사진 부족·크림 바탕", () => {
  const ours = { ...base, 회색한줄: 4, 옅은띠: 1, 단추: 4, 사진비율: 0.5, 바탕색: [255, 240, 220] };
  const lines = driftLines(390, base, ours).join("\n");
  assert.match(lines, /회색한줄/);
  assert.match(lines, /옅은띠/);
  assert.match(lines, /사진비율/);
  assert.match(lines, /바탕색/);
  assert.doesNotMatch(lines, /단추 —/);  // 단추는 하나 차이까지 봐준다
});

test("바탕에 제목 태그가 없으면 제목 항목은 견주지 않는다(자전거 38차)", () => {
  const b = { ...base, 제목수: 0 };
  assert.doesNotMatch(driftLines(390, b, { ...b, 회색한줄: 3, 제목위윗줄: 1 }).join(" "), /회색한줄|제목위윗줄/);
});

test("어두운 바탕에 밝은 페이지는 걸린다(맥주집 41차)", () => {
  const dark = { ...base, 바탕색: [24, 28, 28] };
  assert.match(driftLines(1280, dark, { ...dark, 바탕색: [255, 255, 255] }).join(" "), /바탕밝기/);
  assert.equal(driftLines(1280, dark, { ...dark, 바탕색: [30, 30, 32] }).length, 0);
});

test("AI 티 꼴은 바탕에 있어도 걸린다(사용자 2026-11-11)", () => {
  const kit = { ...base, 큰숫자칸: 3, 끝단추띠: 1 };
  const lines = driftLines(1280, kit, { ...kit }).join(" ");
  assert.match(lines, /큰숫자칸/);
  assert.match(lines, /끝단추띠/);
});
