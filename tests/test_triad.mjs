// triad.mjs 판정 시험 — 우리 값이 바탕보다 오답지에 가까우면 「오답지 쪽」, 둘 다 없는데 우리만 많으면 「우리만 다름」.
import { test } from "node:test";
import assert from "node:assert/strict";
import { side } from "../scripts/triad.mjs";

test("오답지 쪽·정답지 쪽·우리만 다름", () => {
  assert.equal(side(10, 3, 5), "오답지 쪽");
  assert.equal(side(10, 9, 5), "정답지 쪽");
  assert.equal(side(0, 4, 0), "우리만 다름");          // 19차 회색 한 줄
  assert.equal(side(1, 1, 1), "가르지 못함");
  assert.equal(side([32, 48, 96], [32, 72, 64], [48, 72, 56]), "오답지 쪽"); // 단추색: 남색 바탕, 숲초록 우리·오답지
});
