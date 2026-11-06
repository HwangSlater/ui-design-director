// raw.jsonl → fonts.json(글꼴별 쓰는 사이트·역할) + dropped.json(뺀 이름) + summary.json
// 사이트가 「쓴다」고 세는 기준: (1) 역할별 CSS font-family 맨 앞의 이름(일반·시스템 글꼴은 건너뛰고 그다음),
// (2) 실제로 그린 웹폰트(CSS.getPlatformFontsForNode 의 isCustomFont), (3) document.fonts 에서 loaded 인 @font-face 이름
import { readFileSync, writeFileSync } from "node:fs";

const RAW = "raw.jsonl";
const rows = readFileSync(RAW, "utf8").split("\n").filter(Boolean).map((l) => JSON.parse(l));
// 같은 사이트를 다시 잰 줄이 있으면 마지막 것만
const bySite = new Map(rows.map((r) => [r.name, r]));
const all = [...bySite.values()];

// 일반 글꼴·운영체제 기본 글꼴(뺄 것). 키는 normKey 결과
const GENERIC = ["sans-serif", "serif", "monospace", "cursive", "fantasy", "system-ui", "-apple-system", "blinkmacsystemfont", "ui-sans-serif", "ui-serif", "ui-monospace", "emoji", "math", "inherit", "initial", "sans"];
const SYSTEM = ["apple sd gothic neo", "applesdgothicneo", "applegothic", "malgun gothic", "맑은 고딕", "malgungothic", "dotum", "돋움", "dotumche", "돋움체", "gulim", "굴림", "gulimche", "굴림체", "batang", "바탕", "gungsuh", "궁서", "arial", "helvetica", "helvetica neue", "helveticaneue", "segoe ui", "tahoma", "verdana", "times new roman", "times", "georgia", "courier new", "courier", "apple color emoji", "segoe ui emoji", "segoe ui symbol", "noto color emoji", "lucida grande", "lucida sans unicode", "arial unicode ms", "consolas", "menlo", "monaco", "sf pro", "sf pro text", "sf pro display", "sfprodisplay", "sfprotext", ".sf ns", "trebuchet ms", "microsoft yahei", "meiryo", "ms pgothic", "hiragino sans", "hiragino kaku gothic pro", "pingfang sc", "yu gothic", "simsun", "sans-serif-kr", "arial black", "impact", "liberation sans", "droid sans", "ubuntu", "cantarell", "oxygen", "fira sans", "nimbus sans", "segoe ui historic", "segoe ui variable", "apple sd gothic", "malgun_gothic", "sans serif", "-apple-system-body", "miui", "mi sans", "pingfang", "noto sans tc", "noto sans sc", "noto sans jp", "microsoft jhenghei"];
// 측정 도구가 만든 이름·임시 이름·크기 맞춤용 대체 글꼴(진짜 글꼴이 아님)
const JUNK = (k) => k.length < 3 || /^ots derived/.test(k) || /fallback|probe|adjusted|size-adjust/.test(k) || (/^[a-z0-9]{16,}$/i.test(k.replace(/[\s_-]/g, "")) && /\d/.test(k));
const ICON = /icon|awesome|glyph|symbol|xeicon|fontello|swiper|slick|remix|material|bootstrap-icons|feather/i;
// 같은 글꼴의 다른 표기 → 대표 이름
const ALIAS = {
  "nanumgothic": "Nanum Gothic", "나눔고딕": "Nanum Gothic", "nanum gothic": "Nanum Gothic",
  "nanumsquare": "NanumSquare", "나눔스퀘어": "NanumSquare", "nanumsquareneo": "NanumSquare Neo", "nanumsquareround": "NanumSquareRound",
  "nanummyeongjo": "Nanum Myeongjo", "나눔명조": "Nanum Myeongjo", "nanumbarungothic": "NanumBarunGothic", "나눔바른고딕": "NanumBarunGothic",
  "notosanskr": "Noto Sans KR", "notosanscjkkr": "Noto Sans KR", "notosans kr": "Noto Sans KR", "notosans": "Noto Sans", "notoserifkr": "Noto Serif KR",
  "pretendard": "Pretendard", "notokr": "Noto Sans KR", "cafe24ohsquareon": "Cafe24 Ohsquare", "cafe24ohsquare": "Cafe24 Ohsquare", "맑은고딕": "Malgun Gothic", "pretendardjp": "Pretendard", "pretendardstd": "Pretendard", "pretendardgov": "Pretendard GOV",
  "spoqahansans": "Spoqa Han Sans", "spoqahansansneo": "Spoqa Han Sans Neo", "spoqa han sans neo": "Spoqa Han Sans Neo",
  "roboto": "Roboto", "inter": "Inter", "suit": "SUIT", "wantedsans": "Wanted Sans",
};
const normKey = (s) => s.trim().replace(/^["']|["']$/g, "").trim().toLowerCase();
const WEIGHT = /[\s_-]*(thin|hairline|extralight|ultralight|light|regular|normal|book|medium|semibold|demibold|bold|extrabold|ultrabold|black|heavy|semi|text|display|beta[\s\d-]*|\d00|\d{2,3}|italic|oblique)$/i;
const SUFFIX = /[\s_-]*(variable|vf|var|otf|ttf|woff2?|web|webfont|subset|dynamic[\s_-]*subset|proto|_proto|kr[\s_-]*subset|ko|local|fallback|fix|font|regular)$/i;
function canon(raw) {
  let s = raw.trim().replace(/^["']|["']$/g, "").trim();
  if (!s) return null;
  for (let i = 0; i < 6; i++) { const t = s.replace(SUFFIX, "").replace(WEIGHT, "").trim(); if (t === s) break; s = t; }
  const k = s.toLowerCase(), kc = k.replace(/[\s_-]/g, "");
  if (ALIAS[k]) return ALIAS[k];
  if (ALIAS[kc]) return ALIAS[kc];
  for (const [re, name] of FAMILY_RULES) if (re.test(kc)) return name;
  return s;
}
// 사이트가 같은 글꼴에 붙인 별명·굵기별 이름을 한 가족으로(이름 꼴로 판단 — fonts-all.md 에 적어 둔다)
const FAMILY_RULES = [
  [/^(noto(sans)?(kr|korean|cjkkr)|notokr|noto(r|m|b|t|l|dl|krb|krl|krm|krr)$|notosanskr|notosans(header|l|r|kr_en)$)/, "Noto Sans KR"],
  [/^notoserif(kr|cjkkr)/, "Noto Serif KR"],
  [/^pretendard(gov)/, "Pretendard GOV"],
  [/^pretendard/, "Pretendard"],
  [/^spoqa(hansans)?(neo)?$/, "Spoqa Han Sans Neo"],
  [/^cjonlyone/, "CJ ONLYONE NEW"],
  [/^ibkidream/, "IBK iDream"],
  [/^(lgsmart|lgsmha)/, "LG Smart UI"],
  [/^rixsgo/, "Rix신고딕(RixSGo)"],
  [/^modetour/, "Modetour"],
  [/^adineue/, "adineue PRO"],
  [/^(abc)?ginto/, "ABC Ginto"],
  [/^riotsans/, "Riot Sans"],
  [/^spotifymix/, "Spotify Mix"],
  [/^pinsans/, "Pin Sans"],
  [/^inspire/, "Inspire"],
  
  [/^samsungone/, "SamsungOne"],
  [/^nanumsquare(r|b|eb|l)?$/, "NanumSquare"],
  [/^(onesinhandigital|oneshinhan|digitaloneshinhan)/, "One Shinhan"],
  [/^kakaobig/, "KakaoBig"], [/^kakaosmall/, "KakaoSmall"],
  [/^suite$/, "SUITE"],
  [/^(segoe|sfpro|sfui|applegothic|applesdgothic|hiragino|メイリオ|avenirnext|myriadset|doutm)/, "__SYSTEM__"],
  [/^(lang(arabic|global|jp|kr|sc|tc|thai)|icomo|videojs|fontbranded|fontuniversal|hoteldesktop|hy$)/, "__JUNK__"],
  [/^(ｍｓ|ms(p)?gothic|stxihei|applelegacy)/, "__SYSTEM__"],
  [/^bmwtypenext/, "BMW Type Next"], [/^mgkfcc/, "MG KFCC"], [/^flightsans/, "Flight Sans"], [/^hyundaisans/, "Hyundai Sans"], [/^speedee/, "Speedee"],
  [/^notosans(b|m)$/, "Noto Sans KR"], [/^montserrat/, "Montserrat"], [/^robotoheader$/, "Roboto"], [/^youandi/, "Youandi"], [/^canvasans/, "Canva Sans"], [/^figma(sans)?$/, "Figma Sans"], [/^notioninter$/, "Inter"], [/^latonew$/, "Lato"],
  [/^notosansbacktick$/, "__JUNK__"], [/^wenquanyi/, "__SYSTEM__"],
];
const dropped = new Map(); // 이름 → 이유
function classify(raw, site, loadedNames) {
  const k = normKey(raw);
  if (!k) return null;
  if (JUNK(k)) { dropped.set(k, "측정 부산물·크기 맞춤 대체 글꼴·임시 이름"); return null; }
  if (GENERIC.includes(k)) { dropped.set(k, "일반 글꼴군"); return null; }
  if (ICON.test(k)) { dropped.set(k, "아이콘 글꼴"); return null; }
  const c = canon(raw);
  const ck = c.toLowerCase();
  if (c === "__JUNK__" || /[�]|占|留|怨/.test(raw) || /^(base|pass|hnt|nsn|pre)$/.test(ck)) { dropped.set(raw.trim(), "아이콘·언어별 별명·깨진 이름·뜻 모를 짧은 별명"); return null; }
  if (c === "__SYSTEM__") { dropped.set(raw.trim(), "운영체제 기본 글꼴"); return null; }
  if (SYSTEM.includes(k) || SYSTEM.includes(ck)) { dropped.set(c, "운영체제 기본 글꼴"); return null; }
  // Roboto 는 웹폰트로 받은 경우만 센다(안드로이드 시스템 대체 글꼴로 적힌 경우가 많다)
  if (c === "Roboto" && !loadedNames.has("Roboto")) { dropped.set("Roboto(웹폰트로 받지 않은 경우)", "시스템 대체 글꼴"); return null; }
  return c;
}
const splitStack = (ff) => (ff || "").split(",").map((s) => s.trim()).filter(Boolean);

const fonts = new Map();
const display = new Map(); // 비교 키 → 처음 본 표기
const keyOf = (c) => c.toLowerCase().replace(/[\s_-]/g, "");
const add = (font0, site, role, how) => {
  const kk = keyOf(font0); if (!display.has(kk)) display.set(kk, font0); const font = display.get(kk);
  if (!fonts.has(font)) fonts.set(font, { font, sites: new Set(), roles: { heading: new Set(), body: new Set(), nav: new Set(), button: new Set(), loadedOnly: new Set() }, how: new Set() });
  const f = fonts.get(font);
  f.sites.add(site); f.roles[role].add(site); f.how.add(how);
};
const perSite = [];
for (const r of all) {
  if (r.error) continue;
  const loadedNames = new Set((r.loadedFonts || []).map((x) => canon(x.replace(/\s+\d+(\s+\d+)?\s+(normal|italic|oblique).*$/i, ""))));
  const used = new Set();
  for (const role of ["heading", "body", "nav", "button"]) {
    for (const el of r.roles?.[role] || []) {
      for (const name of splitStack(el.ff)) { const c = classify(name, r.name, loadedNames); if (c) { add(c, r.name, role, "CSS 첫 글꼴"); used.add(c); break; } }
    }
    for (const pf of r.platform?.[role] || []) {
      if (!pf.custom) continue;
      const c = classify(pf.family, r.name, loadedNames); if (c) { add(c, r.name, role, "실제로 그린 웹폰트"); used.add(c); }
    }
  }
  for (const c of loadedNames) {
    const cc = c && classify(c, r.name, loadedNames);
    if (cc && !used.has(cc)) { add(cc, r.name, "loadedOnly", "불러오기만 함(document.fonts loaded)"); used.add(cc); }
  }
  perSite.push({ site: r.name, fonts: [...used] });
}
const out = [...fonts.values()].map((f) => ({
  font: f.font, count: f.sites.size, sites: [...f.sites],
  roles: Object.fromEntries(Object.entries(f.roles).map(([k, v]) => [k, v.size])), how: [...f.how],
})).sort((a, b) => b.count - a.count || a.font.localeCompare(b.font));
writeFileSync("fonts.json", JSON.stringify(out, null, 1));
writeFileSync("dropped.json", JSON.stringify(Object.fromEntries([...dropped.entries()].sort()), null, 1));
const failed = all.filter((r) => r.error);
const summary = { tried: all.length, measured: all.length - failed.length, failed: failed.length, failures: failed.map((r) => `${r.name}: ${r.error}`), unique: out.length, sitesWithNoNamedFont: perSite.filter((p) => !p.fonts.length).map((p) => p.site) };
writeFileSync("summary.json", JSON.stringify(summary, null, 1));
console.log(`시도 ${summary.tried} / 잰 것 ${summary.measured} / 실패 ${summary.failed} / 고유 글꼴 ${summary.unique} / 이름 있는 글꼴 없음 ${summary.sitesWithNoNamedFont.length}`);
