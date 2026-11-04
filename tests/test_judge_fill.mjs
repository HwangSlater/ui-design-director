// judge_fill.mjs 시험 — 브라우저 없이 식이 만들어지는지와 남은 흔적 규칙만 본다(채우기 자체는 capture.mjs 로 페이지를 찍어 확인).
// 실행: node --test tests/test_judge_fill.mjs
import { test } from "node:test";
import assert from "node:assert/strict";
import { judgeFillExpr, JUDGE_HIDE, LEFT_MARKS } from "../skills/ui-design-director/scripts/judge_fill.mjs";

test("식이 자바스크립트로 읽힌다", () => {
  assert.doesNotThrow(() => new Function(`return ${judgeFillExpr()}`));
});

test("견본 표시와 빗금 자리를 숨긴다", () => {
  for (const sel of [".sample", ".proto", "slot", "hatch"]) assert.ok(JUDGE_HIDE.includes(sel), sel);
});

test("남은 흔적: 0000·○○·견본은 잡고 값은 잡지 않는다", () => {
  const marks = (s) => s.match(new RegExp(LEFT_MARKS.source, "g")) || [];
  assert.deepEqual(marks("○○동 123"), ["○○"]);
  assert.deepEqual(marks("가게 앞 사진 자리"), ["사진 자리"]);
  assert.deepEqual(marks("값 100,000원"), []);
});
