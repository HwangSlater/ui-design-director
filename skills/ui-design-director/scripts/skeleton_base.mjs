// 바탕(의뢰인이 고른 템플릿·대표 사이트)과 관련 사이트들을 견줘 「바꿀 곳」을 뽑는다 — skeleton.mjs --base 가 쓴다.
// 사용자(2026-11-05): 「템플릿을 정했으면 해당 템플릿의 디자인과 유사하게 가져가야 하는 거야. 레이아웃도 그렇고.
// 완전히 베낄 수는 없으니 여러 관련 사이트들을 참조해서 공통점이 있는 것만 다르게 해 보는 거야.」
// 공통점만으로 짜면 어느 업종이든 같은 평균 웹사이트가 나왔다(카페·분식집·구제 가게 역할극).

const PHOTO_ROUND = 4; // skeleton.mjs 와 같은 값 — 사진 모서리가 이 이상이면 둥근 사진
const STACK_OFF = 0.2; // 우리 한 단 비율이 바탕과 이만큼 넘게 다르면 바탕의 짜임을 버린 것

export const TRAITS = [
  ["navTop", "맨 위 메뉴 줄", (r) => !!r.navTop],
  ["heroPhoto", "첫 화면이 큰 사진", (r) => !!r.heroPhoto],
  ["searchFirst", "첫 화면에 검색창", (r) => !!r.searchFirst],
  ["callEnd", "끝에 전화·연락", (r) => !!r.callEnd],
  ["side", "옆에 붙은 안내판", (r) => !!r.side],
  ["hscroll", "옆으로 넘기는 띠", (r) => r.hscroll > 0],
  ["cols3", "3단 이상 칸", (r) => r.maxCols >= 3],
  ["roundBox", "둥근 큰 상자", (r) => r.roundShare > 0.1],
  ["roundPhoto", "둥근 사진 모서리", (r) => r.photoRad != null && r.photoRad >= PHOTO_ROUND],
];

const yn = (v) => (v ? "있음" : "없음");
const shape = (r) => (r.btnShape && r.btnShape !== "—" ? r.btnShape : null); // skeleton.mjs 는 단추가 없으면 「—」

// base: 바탕 한 곳의 잰 값. others: 관련 사이트들(같은 주소의 여러 쪽은 한 곳). me: 우리 시안(없으면 null).
// 관련 사이트 두 곳 이상이 절반 넘게 바탕과 다르게 하는 것만 「바꿀 곳」. 나머지는 바탕을 따른다.
export function baseDiff(base, others, me = null) {
  const hosts = [...new Set(others.map((r) => r.host))];
  const has = (h, f) => { const pg = others.filter((r) => r.host === h); return pg.filter(f).length * 2 >= pg.length; };
  const N = hosts.length;
  const changes = [], keep = [], notes = [];
  for (const [key, label, f] of TRAITS) {
    const n = hosts.filter((h) => has(h, f)).length;
    const b = f(base);
    const against = b ? N - n : n; // 바탕과 다르게 하는 곳 수
    if (against >= 2 && against * 2 > N) changes.push({ key, label, to: !b, text: `${label}: 바탕은 ${yn(b)}, 관련 사이트 ${against}/${N}곳은 ${yn(!b)}` });
    else keep.push(label);
  }
  const shapes = {};
  for (const h of hosts) { const s = shape(others.find((r) => r.host === h) || {}); if (s) shapes[s] = (shapes[s] || 0) + 1; }
  const [topShape, topN] = Object.entries(shapes).sort((a, c) => c[1] - a[1])[0] || [];
  if (topShape && shape(base) && topShape !== shape(base) && topN >= 2 && topN * 2 > N)
    changes.push({ key: "btnShape", label: "단추 모양", to: topShape, text: `단추 모양: 바탕은 ${base.btnShape}, 관련 사이트 ${topN}/${N}곳은 ${topShape}` });
  else keep.push("단추 모양");
  if (me) {
    for (const [key, label, f] of TRAITS) {
      if (f(me) !== f(base) && !changes.some((c) => c.key === key)) notes.push(`바탕과 다름: ${label}(바탕 ${yn(f(base))}, 우리 ${yn(f(me))}) — 바탕을 따르거나, 바꾼 이유를 DESIGN.md § 바탕에서 바꾼 곳에`);
    }
    if (shape(me) && shape(base) && shape(me) !== shape(base) && !changes.some((c) => c.key === "btnShape"))
      notes.push(`바탕과 다름: 단추 모양(바탕 ${base.btnShape}, 우리 ${me.btnShape})`);
    if (Math.abs(me.stack - base.stack) > STACK_OFF)
      notes.push(`바탕의 짜임을 버림: 한 단 비율 바탕 ${Math.round(base.stack * 100)}%, 우리 ${Math.round(me.stack * 100)}% — 바탕의 칸 나눔을 따를 것`);
  }
  return { changes, keep, notes };
}
