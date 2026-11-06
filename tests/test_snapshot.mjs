// snapshot.mjs 의 거르기 시험 — 남의 HTML 을 내 컴퓨터에서 열기 전에 실행될 것을 다 지우는지(바깥 접속 없음)
// 실행: node --test tests/test_snapshot.mjs
import { test } from "node:test";
import assert from "node:assert/strict";
import { join, dirname } from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";

const MOD = join(dirname(fileURLToPath(import.meta.url)), "..", "skills", "ui-design-director", "scripts", "snapshot.mjs");
const { sanitize } = await import(pathToFileURL(MOD).href);

test("스크립트·페이지 속 페이지·자동 이동·base 를 지운다", () => {
  const out = sanitize(`<head><base href="https://x/"><meta http-equiv="refresh" content="0;url=https://evil/"></head>
<body><script>alert(1)</script><script src="a.js"></script><noscript>켜 주세요</noscript><iframe src="https://ad/"></iframe><object data="x"></object><embed src="y"><p>본문</p></body>`);
  for (const bad of ["<script", "<iframe", "<object", "<embed", "<base", "refresh", "<noscript", "alert(1)"]) assert.ok(!out.toLowerCase().includes(bad), bad);
  assert.ok(out.includes("<p>본문</p>"));
});

test("on…= 속성과 javascript:·data:text/html 주소를 지운다", () => {
  const out = sanitize(`<img src="a.jpg" onerror="alert(1)"><a href="javascript:alert(2)" onclick='x()'>가</a><a href=" data:text/html,<b>">나</a><div onmouseover=y()>다</div>`);
  assert.ok(!/onerror|onclick|onmouseover|javascript:|data:text\/html/i.test(out), out);
  assert.ok(out.includes('src="a.jpg"') && out.includes(">가</a>") && out.includes(">다</div>"));
});
