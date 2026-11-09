# Web typography rules for a design agent (Korean + English pages)

Researched 2026-11-09 from free material by practising designers, research groups and design-system teams; each rule links its source, rewritten in our own words. Rules here are background: `build-rules.md` and the chosen base win when they disagree. Read only the section you need.

## Contents
- 1. Sources
- 2. Rules by sub-topic
- 3. Korean (한글) specifics
- 4. Common generated-looking mistakes the sources warn about

Distilled from free, publicly readable material by working typographers, designers and official design-system teams. All rules are paraphrased. Every rule has the form **rule — why — source**. Where a rule is my own inference rather than a source statement, it is marked *(inference)*. Read on 2026-11-09.

---

## 1. Sources

| # | Title | Author | Credentials (why credible) | URL | Read |
|---|---|---|---|---|---|
| S1 | Practical Typography: Summary of key rules, plus the chapters on line length, line spacing, letterspacing, headings, all caps, bold or italic, centered text, mixing fonts, system fonts, alternate figures | Matthew Butterick | Typographer and type designer (Equity, Concourse, Triplicate), lawyer, author of *Practical Typography* and *Typography for Lawyers* | https://practicaltypography.com/summary-of-key-rules.html (chapter pages under the same domain) | 2026-11-09 |
| S2 | Learn Design: Typography | web.dev (Google), course by Jeremy Keith *(the fetched page shows no byline; the course is credited to him)* | Co-founder of Clearleft, long-time web standards writer | https://web.dev/learn/design/typography | 2026-11-09 |
| S3 | 7 Practical Tips for Cheating at Design (read through the readmedium.com mirror, since Medium returned 403) | Adam Wathan & Steve Schoger | Authors of *Refactoring UI*; creators of Tailwind CSS / Tailwind UI | https://medium.com/refactoring-ui/7-practical-tips-for-cheating-at-design-40c736799886 | 2026-11-09 |
| S4 | The Step-by-Step Guide for Pairing Fonts | Erik D. Kennedy | Independent UI/UX designer; runs Learn UI Design | https://learnui.design/blog/guide-pairing-fonts.html | 2026-11-09 |
| S5 | 7 Rules for Creating Gorgeous UI, Part 2 | Erik D. Kennedy | as above | https://www.learnui.design/blog/7-rules-for-creating-gorgeous-ui-part-2.html | 2026-11-09 |
| S6 | Font Size Guidelines for Responsive Websites | Erik D. Kennedy | as above | https://www.learnui.design/blog/mobile-desktop-website-font-size-guidelines.html | 2026-11-09 |
| S7 | The ideal line length & line height in web design | Oliver Schöndorfer | Typography consultant and speaker (Pimp my Type); UI designer for about 15 years | https://pimpmytype.com/line-length-line-height/ | 2026-11-09 |
| S8 | Material 3 type scale (Android docs + material-web token file) | Google Material Design team | Official design system | https://raw.githubusercontent.com/material-components/material-components-android/master/docs/theming/Typography.md ; https://raw.githubusercontent.com/material-components/material-web/main/tokens/versions/v0_192/_md-sys-typescale.scss ; https://raw.githubusercontent.com/material-components/material-web/main/docs/theming/typography.md | 2026-11-09 |
| S9 | Human Interface Guidelines: Typography (read via the HIG JSON data endpoint) | Apple design team | Official platform guidelines | https://developer.apple.com/design/human-interface-guidelines/typography | 2026-11-09 |
| S10 | GOV.UK Design System: Type scale; Paragraphs | Government Digital Service (UK) | Official, heavily user-tested public-sector design system | https://design-system.service.gov.uk/styles/type-scale/ ; https://design-system.service.gov.uk/styles/paragraphs/ | 2026-11-09 |
| S11 | U.S. Web Design System: Typography | USWDS team, GSA Technology Transformation Services | Official US federal design system | https://designsystem.digital.gov/components/typography/ | 2026-11-09 |
| S12 | Carbon: Typography overview; Style strategies | IBM Carbon Design System team | Official design system (IBM Plex) | https://carbondesignsystem.com/elements/typography/overview/ ; https://carbondesignsystem.com/elements/typography/style-strategies/ | 2026-11-09 |
| S13 | Designing with fluid type scales (Utopia) | James Gilyead (designer), Trys Mudford (developer) | Clearleft; creators of Utopia fluid type method | https://utopia.fyi/blog/designing-with-fluid-type-scales/ | 2026-11-09 |
| S14 | CSS text-wrap: balance | Adam Argyle | Chrome Developer Relations (CSS), Google | https://developer.chrome.com/docs/css-ui/css-text-wrap-balance | 2026-11-09 |
| S15 | Understanding WCAG 2.2 SC 1.4.12 Text Spacing | W3C WAI | Web accessibility standard | https://www.w3.org/WAI/WCAG22/Understanding/text-spacing.html | 2026-11-09 |
| S16 | Requirements for Hangul Text Layout and Typography (KLREQ) | Editor Richard Ishida (W3C); authors Soon-Bum Lim, Wu-Jin Sim, Yong-Je Lee, Dongsun Nam, HyunYoung Kim, YongHo Lim | W3C internationalization note written by Korean typesetting experts | https://www.w3.org/TR/klreq/ | 2026-11-09 |
| S17 | Korean Layout Gap Analysis | W3C Internationalization | Lists where browsers fail Korean layout | https://www.w3.org/TR/kore-gap/ | 2026-11-09 |
| S18 | Mailing-list reply on `word-break: keep-all` (4 Mar 2015) | Jungshik Shin (신정식) | Google engineer on Chrome internationalization / CJK text handling | https://lists.w3.org/Archives/Public/www-international/2015JanMar/0112.html | 2026-11-09 |
| S19 | KRDS (한국 디자인 시스템) 스타일: 타이포그래피 | Ministry of the Interior and Safety (행정안전부) | Official Korean government design system | https://www.krds.go.kr/html/site/style/style_03.html | 2026-11-09 |
| S20 | TDS Mobile Foundation: Typography; Paragraph component | Toss design system team | Official docs of Toss Design System | https://tossmini-docs.toss.im/tds-mobile/foundation/typography/ ; https://tossmini-docs.toss.im/tds-mobile/components/paragraph/ | 2026-11-09 |
| S21 | 서체 고민 없이 본질에만 집중할 수 있도록 (Toss Product Sans) | 김지윤 (Kim Ji-yoon) | Toss brand designer; font built with Sandoll and Leedotype | https://toss.im/tossfeed/article/beginning-of-tps | 2026-11-09 |
| S22 | Pretendard README and design notes (cactus.tistory.com/306) | 길형진 (Gil Hyeong-jin) | Type designer/author of Pretendard (and Pretendard GOV used by KRDS) | https://github.com/orioncactus/pretendard ; https://cactus.tistory.com/306 | 2026-11-09 |
| S23 | Technical Problems in Multilingual Typography (Journal of the Korean Society of Typography, 2016; free PDF) | 김병조 (Kim Byungjo) | Graphic designer; peer-reviewed in the Korean Society of Typography journal | http://koreantypography.org/wp-content/uploads/2016/08/kst_13_8_1_03.pdf.pdf | 2026-11-09 |
| S24 | 한글 맞춤법 부록: 문장 부호 (2014 revision), and 『문장 부호 해설』 index page | National Institute of Korean Language (국립국어원) | Official authority on Korean orthography and punctuation | https://korean.go.kr/kornorms/regltn/regltnView.do?regltn_code=0001&regltn_no=287 ; https://www.korean.go.kr/front/etcData/etcDataView.do?mn_id=46&etc_seq=431 | 2026-11-09 |

**Could not read (skipped):** Google Fonts Knowledge lessons (pages render client-side; only the title came back), m3.material.io pages (client-side; used the official GitHub token files instead), Medium directly (403; used mirror), GOV.UK `/styles/typography/` and Carbon `/type-basics/` (404 at the tried URLs), toss.tech (no typography article found), Sandoll / Yoon Design / Woowahan / Daangn SEED / Kakao design blogs (searches found no readable typography guidance with rules), theteams.kr post (403). A "Naver mobile research: 155% line height" claim appeared only in second-hand blogs and was not verified, so it is not used.

---

## 2. Rules by sub-topic

### 2.1 Choosing typefaces

1. Pick the body face first, before the display face. — Body text has the tightest constraints; choose a plain, legible face with a tall x-height and open counters. — S4
2. For most product and business UI, use clean, neutral faces; save distinctive faces for brands with strong personalities. — Neutral faces keep content in front. — S5, S21 (Toss removed "excess character" so content stands out)
3. Do not use novelty fonts or faces that act out the theme (e.g. a "spooky" font for Halloween). — They over-dramatise and look amateur. — S4
4. Start from 3–5 brand adjectives and choose faces that *subtly* match them. — Gives a checkable reason for every font choice. — S4
5. Default/overused system faces (Times New Roman, Arial) make a page look undesigned; prefer a professionally made face. — Upgrading the font is the single most visible improvement. — S1 (key rules, system fonts)
6. A system UI stack (`system-ui`, `-apple-system`) is an acceptable "plain" token for product UI. — Native rendering, zero download, variable weights on some OSes. — S8 (plain typeface token = `system-ui`), S2, S22
7. Choose the typeface before setting measure and line height. — Metrics and widths differ by face, so spacing values depend on it. — S7
8. For data-heavy or financial UI, prefer a face that ships tabular figures. — Live numbers must not jitter. — S21, S11 (Public Sans has tabular numerals)

### 2.2 Pairing and number of families

9. One family is enough for most pages; two is fine; a third is rarely justified; four or more almost never. — Size, weight and style already give enough variety. — S1 (mixing fonts), S9 (minimise typefaces), S5
10. Give each family one fixed job (e.g. A = headings, B = body; or A = content, B = numbers/labels). — Fixed roles keep hierarchy readable. — S1, S4 (write usage rules per element: headers, body, menus, labels, forms, footers)
11. Switch fonts only at paragraph boundaries, never mid-paragraph. — Mid-paragraph switches look like errors. — S1
12. If you add a second family, it must contrast clearly with the first; two near-identical faces is the classic mistake. — Readers see a near-miss as a mismatch. — S4, S1
13. **Disagreement:** Kennedy says ~95% of good pairings are serif + sans (S4); Butterick says serif/sans is not required and similar faces often pair better than very different ones (S1). Practical rule: pick obvious contrast (serif + sans) when unsure; pair two sans faces only if they differ clearly in width or structure.
14. In Material-style token systems, define two typeface tokens (brand, plain) and map every role to one of them. — Changing fonts later becomes a two-token edit. — S8

### 2.3 Body size

15. Web body text: 15–25 px (Butterick); never below 16 px for running text (USWDS, KRDS, Schöndorfer). — Smaller sizes are for captions/footnotes only. — S1, S11, S19, S7
16. Mobile body: 16–20 px on text-heavy pages, 16–18 px on interaction-heavy pages; start at 17 px. — S6
17. Desktop body: 18–24 px for reading pages, 14–20 px for dense app UI. — S6
18. Form inputs: at least 16 px. — iOS Safari zooms the page into smaller inputs. — S6
19. Reference defaults: Material body-large 16 px; Apple iOS body 17 pt (min 11 pt); GOV.UK body 19 px; KRDS body 17 px; Toss TDS regular body 17 px. — Use these as sanity anchors. — S8, S9, S10, S19, S20
20. Secondary text: about 2 px smaller than body (e.g. 13–15 px) and lighter in colour (~70% strength). — S6
21. Use about four sizes in a simple page: title, default, secondary, optional caption. — More sizes blur hierarchy. — S6
22. If a mobile line holds fewer than ~30 characters, the body size is too large. — S6
23. Light/thin custom faces need sizes above the platform recommendations. — S9

### 2.4 Type scale

24. Build sizes from a defined scale and expose them as tokens; never hard-code px per element. — Tokens let text scale with user settings. — S20 (do not hard-code; system text size support), S8, S12
25. Example scales to copy: Material (rem at 16 px root) display 57/45/36, headline 32/28/24, title 22/16/14, body 16/14/12, label 14/12/11 px. — S8
26. Carbon scale steps: 12, 14, 16, 18, 20, 24, 28, 32, 36, 42, 48, 54, 60, 68, 76, 84, 92 px. — S12
27. Fluid scale: define a small-screen scale (e.g. ratio 1.2 at 320 px) and a large-screen scale (e.g. 1.333 at 1500 px) and interpolate; check at ~1024 px. — Removes breakpoint jumps. — S13
28. Implement fluid sizes with `clamp(min-rem, rem + vw, max-rem)`; never `vw` alone. — Pure `vw` blocks user zoom/resizing. — S2
29. Page title: 28–40 px mobile, 35–50 px desktop. — S6
30. Heading-to-body ratio about 1.25–1.5×; headings never the same size as body unless differentiated by weight. — S19
31. GOV.UK pairs: heading-xl 48 px (32 on small screens), heading-l 36 (27), heading-m 24 (21), body 19, body-s 16; 80 px only exceptionally. — Shows how much headings shrink on mobile (~0.65–0.9×). — S10
32. **Disagreement:** For *documents*, Butterick wants headings only slightly bigger than body (e.g. 12 → 12.5–13 pt) and emphasised mainly by space (S1 headings). Web systems use bigger steps (S6, S8, S19). Rule: long-form article sub-heads can be small and bold; landing-page and app titles follow the scale.
33. Use no more than three heading levels in running content; two is better. — S1
34. Carbon: use compact "productive" styles for forms, tables, filters; "expressive" (fluid, larger) styles only for full-width page headers, banners, home pages — never inside cards or tables. Do not mix type sets inside one component. — S12

### 2.5 Line length (measure)

35. Body lines: 45–90 characters including spaces (Butterick, USWDS); ~66 is the classic ideal (web.dev, USWDS). — Long lines make the return sweep to the next line hard. — S1, S2, S11
36. Set the measure with `max-inline-size: 66ch` (or ~30–40 rem); not a fixed px width. — S2, S7
37. **Ranges differ:** 45–75 (S2), 50–75 desktop (S6), 60–80 desktop (S7), 45–90 (S1, S11). Safe target: 60–75 characters on desktop.
38. Mobile: text column ~20–25 rem; ~40–50 characters is normal. — S7
39. Multi-column text: 40–50 characters. — S2
40. Quick check when you cannot count: two to three lowercase alphabets should fit on one line. — S1

### 2.6 Line height (leading)

41. Always use unitless `line-height` (e.g. `1.5`), never px. — Unitless values scale with font size. — S1, S2; KRDS says relative units (% / em), not px — S19
42. Long Latin body text: 1.5–1.6 on desktop (S7); web.dev uses 1.5 general / 1.65 for articles (S2); USWDS ≥ 1.5 (S11). — Browser default ~1.2 is too tight for body. — S7
43. **Disagreement:** Butterick's print-based range is 1.2–1.45 (S1). Web sources sit higher (1.5+). Use ≥ 1.5 for web body; this also matches the WCAG tolerance value (S15).
44. Longer lines need more leading, shorter lines less (~1.3 at 30 characters, ≥ 1.5 at 60–80). — S7, S11
45. Mobile body: 1.3–1.45 for Latin (S7). (Korean needs more — see §3.)
46. Headings and 1–2-line text: 1.0–1.35 (S11); about 1.1 for large headings (S7). Test multi-line headings for colliding ascenders/descenders. — S7
47. UI text, nav, notifications: 1.2–1.3; buttons can be 1.0. — S7
48. Do not go loose (e.g. 2.0) on body: lines lose cohesion. — S7 (slides), S1 (170% looked too loose)
49. Faces that look large at a given size need more leading; small-looking faces need less. — S1
50. Material line heights (px at 16 px root): display-l 57/64, headline-l 32/40, title-l 22/28, body-l 16/24, body-m 14/20, label-l 14/20. — S8
51. Apple: avoid tight leading for three or more lines; loose leading for long passages, tight only in constrained rows. — S9
52. Keep line heights on a grid where practical (GOV.UK uses multiples of 5 px). — S10

### 2.7 Letter spacing (tracking)

53. Lowercase body text: leave tracking at 0. — Fonts are spaced for text sizes already; Apple says do not add tracking to body text. — S1, S9, S19 (KRDS 0 for body)
54. All caps and small caps: add 5–12% (`letter-spacing: 0.05em–0.12em`). — Caps are designed to sit next to lowercase, so caps-on-caps look cramped. — S1; USWDS also loosens uppercase — S11
55. Very small text may be loosened slightly. — S1, S11
56. Large headlines may be tightened: USWDS −1/−2/−3 tokens at larger sizes; Kennedy ~−1% for Source Sans headers; Material display-large −0.25 px. — Big type looks over-spaced at default tracking. — S11, S5, S8
57. **Disagreement:** KRDS uses +1 px on display and heading-xl/large (S19), opposite to the Latin tightening habit. Apple: system fonts track automatically per size; do not override in code (S9). Rule: tighten Latin display slightly (−0.5% to −2%); for Korean display, follow the font's defaults or KRDS (§3).
58. Never track so wide that another letter would fit in the gap. — S1
59. Put the letter-spacing inside the caps/label style itself, so it travels with the style. — S1
60. Letter-spacing adds trailing space after the last character; avoid it on right-aligned/justified line ends and check backgrounds/outlines. — S17
61. Keep kerning on everywhere. — S1

### 2.8 Weights and emphasis

62. Use two weights for most UI: regular (~400–500) and a heavier one (~600–700). — S3; Carbon uses 300/400/600 — S12; KRDS 400/500/700, max ~4 weights — S19
63. Avoid weights below 400 for UI text and body. — Hard to read at small sizes; de-emphasise with colour or size instead. — S3, S9 (avoid Ultralight/Thin/Light), S19 (avoid light, thin, extra bold)
64. Black/Heavy weights are for large display sizes only. — S1, S9
65. Semibold suits section headers, not long passages. — S12
66. Emphasis: bold *or* italic, never both; never underline bold; never whole paragraphs in bold. — S1, S11
67. In sans-serif text, emphasise with bold, not italic (sans italics barely stand out). — S1
68. Underline only links. — S1, S19, S5
69. Avoid text-background highlight (except hover) and strikethrough as emphasis. — S5
70. Hierarchy comes from weight, size **and colour** together, not size alone; a much larger light-weight line can outrank a smaller bold one. — S3, S9, S12
71. Use 2–3 text colours: near-black primary, mid grey secondary, lighter grey tertiary. — S3
72. Running text stays neutral in colour; coloured text is for links, actions, code, warnings. — S12
73. On coloured backgrounds, never use grey text: use white at reduced opacity, or a tint of the background hue. — Grey reads as dirty on colour. — S3
74. Hover/selected states must not change size, case or weight (layout shift); change colour, background, underline or shadow. — S5
75. Only the page title should "pop" by increasing emphasis alone; other emphasised elements combine one up-pop with one down-pop (e.g. bold but smaller, caps but grey). — S5

### 2.9 Case, alignment, paragraphs

76. All caps only for less than one line (labels, short headers, captions); never paragraphs. — Caps are slower to read and get skipped. — S1
77. Headings in sentence case; avoid all-caps and title-case headings. — S1
78. Uppercase labels/buttons may be set slightly smaller than lowercase text, since caps look heavier. — S6
79. Left-align (flush left) running text; do not justify on the web. — Browser justification makes rivers; Butterick requires hyphenation if justifying. — S11, S1
80. Centre only short lines (titles, one-line headings); never centre text blocks; break centred multi-line titles at natural phrase points. — S1
81. Paragraph separation: either first-line indent or space between, never both; on the web use unindented paragraphs with 0.5–1.5 em between. — S1, S11
82. Space above a heading ≥ 1.5× the space below it. — Ties the heading to its own section. — S11
83. List items: ≥ 0.5 em apart. — S11
84. One lead paragraph per page at most (GOV.UK 24 px). — S10
85. Use `text-wrap: balance` on headings, short quotes (≤ 6 lines) and give them a max width; never on body or on `*`. — Prevents a one-word last line; it is costly on long text. — S14

### 2.10 Numerals and symbols

86. Tabular (fixed-width) figures for tables, prices, live values, timers, stacked numbers; proportional figures in running text. CSS: `font-variant-numeric: tabular-nums` (or `tnum`). — Aligned digits do not jitter. — S1 (alternate figures), S21, S22
87. Lining figures with caps and in UI; oldstyle only in lowercase prose, never beside capitals. — S1
88. Test for tabular figures: set "0000" above "1111"; equal widths mean tabular. — S1
89. Use `case` feature (case-sensitive punctuation) for all-caps labels where the font has it. — S22, S1
90. Typographic marks: curly quotes, real ellipsis (…), real ©/™, proper dashes (not double hyphens), one space after full stops. — S1
91. Large UI symbols (%, +/−, arrows) may need to be larger and more spaced than text defaults; Toss redrew them almost as icons. — S21

### 2.11 Accessibility and font loading

92. Layout must survive user overrides of line-height 1.5×, paragraph spacing 2×, letter-spacing 0.12×, word-spacing 0.16× font size without clipping or overlap. — WCAG 1.4.12. — S15
93. Support OS/browser text scaling: allow multi-line labels, avoid forced one-line truncation, prioritise main content as text grows. — Toss found one-line ellipsis hid information at large text sizes; Apple says minimise truncation. — S20, S9
94. Contrast: 4.5:1 normal text, 3:1 large (≥ 24 px, or ≥ 18.66 px bold); AAA 7:1 / 4.5:1. — S19
95. Fonts: WOFF2; preload critical font files (`rel=preload as=font type=font/woff2 crossorigin`); limit the number of files; consider one variable font instead of many weights. — Each file costs load time. — S2
96. Use `font-display` with a short block and `size-adjust` on the fallback `@font-face` to reduce layout shift. — S2
97. Load each typeface in every weight its tokens reference (e.g. 400/500/700) — missing weights get faked. — S8

---

## 3. Korean (한글) specifics

### 3.1 Fonts and Korean/Latin mixing

K1. Body and UI: use a gothic (sans) Korean face. KRDS standard is Pretendard GOV; alternatives Noto Sans KR, Nanum Gothic, Spoqa Han Sans. Non-gothic display faces only in banners/displays. — S19
K2. Pretendard (Inter Latin + Source Han Sans Korean, tuned toward SF / Apple SD Gothic Neo) is a cross-platform `system-ui` substitute; its vertical metrics match SF, so layouts built on `-apple-system` behave the same. — S22
K3. Ship Korean webfonts as subsets or dynamic subsets (only glyphs on the page). — Full Hangul is 11,172 syllables; Toss added a subset file for faster loading. — S22, S21
K4. Korean and Latin in one line must match in **overall weight (grey value) and contrast**, not in a single stroke measure. — S23
K5. In ordinary Korean fonts, Latin and digits often look smaller than Hangul; good Korean UI faces enlarge and slightly embolden Latin/digits so they do not look thin. Check a mixed sample like "2026년 3월 Pro 요금제 9,900원" at body size. — S21, S23
K6. When pairing a separate Latin face with a Korean face, prefer a Latin face with a large x-height; it reduces the size gap. Uppercase words will still look larger than Hangul and lowercase smaller. — S23
K7. Latin's visual centre sits lower than Hangul's; shifting the Latin baseline is only a partial fix. Prefer a Korean font whose bundled Latin is already harmonised (Pretendard, Spoqa Han Sans, Toss Product Sans) over browser fallback mixing. — S23, S22, S21
K8. If Japanese kana/kanji also appear, use a CJK face reduced for mixing (Pretendard JP reduces kana/kanji ~6.25%). — S22
K9. Korean fonts often have wider word spaces than Latin; spacing should be tuned per script so readers do not notice the difference. — S23
K10. Korean text tends to sit off-centre vertically in buttons with some fonts; check vertical centring in buttons and chips on Windows, Android, iOS, Chrome and Safari. — Toss had to retune vertical metrics. — S21

### 3.2 Size and line height

K11. Korean body minimum 16 px; with Pretendard GOV use 17 px as the default, because it looks smaller than other faces at the same size. — S19
K12. KRDS sizes (PC / mobile, px): display 60/44, 44/32, 36/28; heading xl 40/28, l 32/24, m 24/22, s 19, xs 17, xxs 15; body 19 / 17 / 15 / 13; label 19 / 17 / 15 / 13. Body 400, headings 700. — S19
K13. Korean line height: minimum 150% for all KRDS styles. — Hangul fills a square body with dense strokes and no ascender/descender gaps, so it needs more leading than Latin. *(reason is inference; the 150% is S19)* — S19
K14. Toss TDS uses 1.5 for body (17/25.5, 15/22.5, 13/19.5) and ~1.33–1.45 for headings (30/40, 22/31, 20/29). — S20
K15. KLREQ gives 160% of character size as its example leading for Korean text. — S16
K16. Practical Korean ranges *(synthesis)*: body 1.5–1.7; headings 1.3–1.4; one-line UI labels 1.2–1.4. Do not apply the Latin print range (1.2–1.45) to Korean body. — S19, S20, S16, S1
K17. Heading-to-body ratio about 1.25–1.5×. — S19
K18. In-app web pages must follow the app's text-size scaling (TDS maps OS percentages to web tokens), or body text looks relatively small. — S20

### 3.3 Letter spacing

K19. Korean body tracking: 0 (KRDS 0 px for body, headings below xl). — S19
K20. **Disagreement / unverified:** many Korean sites tighten Hangul (−0.01 to −0.03 em, or "−0.3" at 16–17 px); this appears only in blogs, not in any official or practitioner source read here. Pretendard's author deliberately avoided size-specific tracking adjustments and tuned default spacing to Helvetica Neue / SF at body size (S22). Toss button CSS seen second-hand uses −0.01em (unverified). Rule: start at 0; tighten display Korean only after a visual check, never below −0.02 em on body. *(the −0.02 em cap is inference)*
K21. KRDS uses +1 px on display and heading-xl/l. Follow it on government-style pages. — S19

### 3.4 Line breaking

K22. Korean may break between any two syllables by default; KLREQ allows breaking by character or by eojeol (word), chosen per paragraph or document. — S16
K23. `word-break: keep-all` (break only at spaces) is right for **short** text: titles, headings, buttons, labels, ad copy, UI. — Words split mid-syllable look broken in big type. — S18
K24. For long Korean body text (articles, comments), syllable breaking is the traditional norm (books, newspapers); Jungshik Shin argues against keep-all on body. **Disagreement:** many Korean product sites apply keep-all to body anyway. Rule: keep-all on headings/UI always; on body only with short-to-medium lines and `overflow-wrap: anywhere` (or `break-word`) as a safety net. *(safety net is inference)* — S18
K25. With keep-all on narrow elements (buttons, mobile cards), check for overflow from long words or URLs. *(inference)*
K26. Combine `text-wrap: balance` with keep-all on Korean headings for even lines. — S14 (balance), S18 (keep-all)
K27. Line-start prohibited: closing brackets, `?` `!`, middle dot, period, comma, hyphen. Line-end prohibited: opening brackets. Never split: repeated dashes/ellipses, consecutive digits, a number and its unit or %/℃, prefix symbol and number. Use `&nbsp;` / `white-space: nowrap` for number+unit pairs if the browser breaks them. — S16
K28. Korean justification needs adjusted inter-character spacing; browsers do it poorly, so left-align web body. — S16, S11
K29. Paragraphs: one-character first-line indent is the print default, but no indent is appropriate for short horizontal lines (web). — S16

### 3.5 Punctuation and marks (Korean orthography)

K30. Horizontal Korean uses half-width `,` and `.`; quotations use curly quotes `“ ”` `‘ ’`. (「」『』 are traditional for vertical text.) — S16
K31. No full stop at the end of headings, titles or slogans (allowed only exceptionally). — S24
K32. Middle dot `·` joins items in a set (e.g. 서정시·서사시), no spaces around it; a comma or nothing is also allowed. — S24
K33. Colon: attach to the preceding word, space after (e.g. `문의: 02-…`); no spaces in times, chapter:verse or scores (10:20, 65:60). — S24
K34. Ranges (periods, distances): tilde `~` with no spaces (e.g. `9:00~18:00`, `3~5일`); hyphen allowed instead. — S24
K35. Slash: no spaces by default (`100미터/초`); spaces allowed when the paired phrases are multi-word. — S24
K36. Titles: books/newspapers in 『 』 or ≪ ≫ (or “ ”); chapters, artworks, laws, company names in 「 」 or < > (or ‘ ’). — S24
K37. Opening quote attaches to the following word, closing quote to the preceding word. — S24
K38. Ellipsis: the standard is `……`; if a sentence ends with an ellipsis, a full stop/question/exclamation mark follows. (Secondary sources say `…` and `...` are also accepted since 2015; not verified in the read portion.) Pretendard `ss05` gives a Korean-matched ellipsis. — S24, S22
K39. Emphasis in Korean prose: 국립국어원 lists emphasis dots (드러냄표) and underline, and allows ‘ ’ for emphasis. For web UI use bold; avoid italic on Hangul because Korean fonts have no true italic and the browser fakes an oblique. *(italic part is inference)* — S24
K40. Space a symbol or math sign from adjacent Hangul by about 1/8 em; no extra space next to digits or Latin. — S16

---

## 4. Common generated-looking mistakes the sources warn about

Each line is something to check for on a finished page.

1. Arial / Times New Roman or an unconsidered default face carrying the brand. — S1
2. A novelty or theme-acting font (handwriting, "techy", "spooky") for body or nav. — S4
3. Two near-identical families paired (e.g. two geometric sans), or three or more families on one page. — S4, S1, S9
4. Thin/Light (≤ 300) weights for body or small UI text, especially light grey on white. — S3, S9, S19
5. Hierarchy made by size alone, so every heading is huge; no use of weight and colour. — S3, S12
6. Grey text on a coloured or photo background. — S3
7. Pure black text with no secondary/tertiary text colours, or decorative coloured body text. — S3, S12
8. All-caps paragraphs or long all-caps buttons, and all-caps without added tracking (or wide-tracked lowercase body). — S1, S11
9. Centred multi-line paragraphs (hero subtitle blocks, feature descriptions). — S1
10. Justified web text with rivers. — S11, S1
11. Body lines running full container width (100+ characters) on desktop. — S1, S2
12. `line-height` in px, or the browser default ~1.2 on body; or Korean body at Latin print leading (< 1.5). — S2, S7, S19
13. Bold + italic together, underlined non-links, bold whole paragraphs, italic emphasis in sans text. — S1, S5
14. Hover states that change weight or size and make text jump. — S5
15. Straight quotes, `...` from three periods, `--` for dashes, `(c)` for ©. — S1
16. Proportional digits in price tables, timers or stats that wiggle. — S1, S21
17. Plain text dropped on a busy photo with no overlay/scrim (Kennedy: dark overlay ~35%, floor fade, blur, or scrim). — S5
18. Headings with a one-word last line (no `text-wrap: balance`); Korean headings split mid-word (no `keep-all`). — S14, S18
19. Text sizes in fixed px only, so OS/browser text scaling breaks or truncates labels with ellipses. — S20, S9, S2
20. Too many sizes (7+ distinct sizes on a simple landing page) instead of a defined scale of ~4 roles. — S6, S12
21. Expressive display type inside cards, tables or form panels. — S12
22. Korean pages: Latin/digits visibly smaller or thinner than surrounding Hangul (fallback-font mixing); text off-centre in buttons. — S21, S23
23. Korean headings ending with a full stop; spaced-out ranges like `3 ~ 5일`; colon with a space before it. — S24
