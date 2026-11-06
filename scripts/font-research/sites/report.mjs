// fonts.json + licenses.json + summary.json + dropped.json → fonts-candidates.md, fonts-all.md
import { readFileSync, writeFileSync } from "node:fs";

const fonts = JSON.parse(readFileSync("fonts.json", "utf8"));
// licenses.json = 아래 파일을 순서대로 덮어 합친 것(뒤 파일이 이김). 없는 파일은 건너뜀
const LIC_FILES = ["licenses-base.json", "licenses-agent.json", "licenses-extra.json", "recheck-open.json", "recheck-korean.json", "recheck-global.json"];
const lic = {};
for (const file of LIC_FILES) { try { for (const [k, v] of Object.entries(JSON.parse(readFileSync(file, "utf8")))) lic[k] = { ...lic[k], ...v }; } catch (e) { if (e.code !== "ENOENT") throw e; } }
writeFileSync("licenses.json", JSON.stringify(lic, null, 1));
const sum = JSON.parse(readFileSync("summary.json", "utf8"));
const dropped = JSON.parse(readFileSync("dropped.json", "utf8"));
const raw = readFileSync("raw.jsonl", "utf8").split("\n").filter(Boolean).map((l) => JSON.parse(l));
const measuredDate = [...new Set(raw.map((r) => (r.measuredAt || "").slice(0, 10)).filter(Boolean))].sort().join(" ~ ");
// AI 모델이 기본으로 고르는 글꼴(다음 단계에서 뺄 후보) — 표에서는 표시만 한다
const AI_DEFAULT = ["Pretendard", "Noto Sans KR", "Noto Serif KR", "Inter", "Spoqa Han Sans", "Spoqa Han Sans Neo", "Nanum Gothic", "Nanum Myeongjo", "MaruBuri", "Gowun Dodum", "Gowun Batang", "SUIT", "Wanted Sans"];
const isAi = (f) => AI_DEFAULT.some((a) => f.toLowerCase() === a.toLowerCase() || f.toLowerCase().startsWith(a.toLowerCase() + " ")); // SUITE 는 SUIT 와 다른 글꼴
const ROLE_KO = { heading: "제목", body: "본문", nav: "메뉴", button: "버튼", loadedOnly: "불러오기만" };
const roles = (r) => Object.entries(r).filter(([, n]) => n).map(([k, n]) => `${ROLE_KO[k]} ${n}`).join(", ");
const esc = (s) => String(s ?? "").replace(/\|/g, "\\|");

const rowsAll = fonts.map((f) => ({ ...f, l: lic[f.font] || { free: "확인 못 함" } }));
const free = rowsAll.filter((f) => f.l.free === "무료");
const cand = free.filter((f) => f.l.korean === "있음" && !f.l.approvalNeeded);
const needApproval = rowsAll.filter((f) => f.l.korean === "있음" && f.l.approvalNeeded && f.l.free === "무료");

const head = [
  `- 측정한 날: ${measuredDate} (Windows 10, 헤드리스 Edge, 1440×900, 한국어 Accept-Language)`,
  `- 사이트: 시도 ${sum.tried} / 측정 ${sum.measured} / 실패 ${sum.failed}`,
  `- 고유 글꼴: ${fonts.length}개 (일반·시스템·아이콘 글꼴 ${Object.keys(dropped).length}개 이름은 뺌 — fonts-all.md 아래쪽)`,
  `- 상업 웹 사용 무료: ${free.length}개, 그 가운데 한글 글자 있음: ${cand.length}개 / 무료 아님 ${rowsAll.filter((f) => f.l.free === "무료 아님").length}개 / 확인 못 함 ${rowsAll.filter((f) => f.l.free === "확인 못 함").length}개`,
  `- 「쓰는 곳」 기준: 제목·본문·메뉴·버튼 요소의 CSS font-family 맨 앞 이름(일반·시스템 글꼴은 건너뜀), 실제로 그린 웹폰트, document.fonts 에서 loaded 인 @font-face 이름 가운데 하나라도 해당하면 1곳`,
  `- 「AI 기본 의심」: ${AI_DEFAULT.join(", ")} — 아직 빼지 않고 표시만 함`,
];

const md1 = ["# 한국 사이트 실측 무료 한글 글꼴 후보", "", ...head, "",
  "| 글꼴 | 성격 | 쓰는 곳 수 | 쓰는 사이트(최대 5) | 라이선스(출처) | 출처 구분 | 조건 | 받는 곳 | AI 기본 의심 |",
  "|---|---|---:|---|---|---|---|---|---|",
  ...cand.map((f) => `| ${esc(f.font)} | ${esc(f.l.character)} | ${f.count} | ${esc(f.sites.slice(0, 5).join(", "))} | ${esc(f.l.license)} (${esc(f.l.source)}${f.l.readDate ? ", " + f.l.readDate + " 읽음" : ""}) | ${esc(f.l.sourceType || "")} | ${esc(f.l.conditions || "")} | ${esc(f.l.download)} | ${isAi(f.font) ? "의심" : ""} |`),
  "", "## 따로 승인을 받아야 웹에 쓸 수 있는 글꼴(위 표에서 뺌)", "", ...(needApproval.length ? needApproval.map((f) => `- ${esc(f.font)} (${f.count}곳: ${esc(f.sites.slice(0, 5).join(", "))}) — ${esc(f.l.conditions || f.l.license || "")} (${esc(f.l.source || "")})`) : ["- 없음"]),
  "", "역할별 쓰임(제목·본문·메뉴·버튼·불러오기만)은 fonts-all.md 에 있다.", ""];
writeFileSync("fonts-candidates.md", md1.join("\n"));

const md2 = ["# 실측 고유 글꼴 전체", "", ...head, "",
  "| 글꼴 | 쓰는 곳 수 | 역할 | 쓰는 사이트 | 상업 무료 | 한글 | 라이선스·판단 근거 | 출처 |",
  "|---|---:|---|---|---|---|---|---|",
  ...rowsAll.map((f) => `| ${esc(f.font)} | ${f.count} | ${roles(f.roles)} | ${esc(f.sites.join(", "))} | ${f.l.free} | ${esc(f.l.korean || "")} | ${esc([f.l.license, f.l.note].filter(Boolean).join(" — "))} | ${esc(f.l.source || (f.l.free === "무료 아님" ? "공개 배포처 없음(그 회사 사이트 서버에서만 제공)" : ""))} |`),
  "", "## 뺀 이름", "", "| 이름 | 이유 |", "|---|---|",
  ...Object.entries(dropped).map(([k, v]) => `| ${esc(k)} | ${v} |`),
  "", "## 실패한 사이트", "", ...sum.failures.map((s) => `- ${esc(s)}`),
  "", "## 이름 있는 글꼴이 하나도 안 잡힌 사이트(시스템 글꼴만 씀)", "", sum.sitesWithNoNamedFont.join(", "), ""];
writeFileSync("fonts-all.md", md2.join("\n"));
const missing = fonts.filter((f) => !lic[f.font]).map((f) => f.font);
console.log(`후보 ${cand.length} / 무료 ${free.length} / 라이선스 표 없음 ${missing.length}${missing.length ? ": " + missing.join(", ") : ""}`);
