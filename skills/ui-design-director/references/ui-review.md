# Rendered UI review

Review the rendered product, not code alone. Compare it with approved `DESIGN.md`, the concept brief, and actual content/interaction needs.

## Severity

1. **Blocking:** unusable interaction, broken hierarchy/task flow, inaccessible keyboard path, severe contrast/reflow issue, broken responsive layout, or missing critical state.
2. **System drift:** hard-coded repeated values, inconsistent variants, reference traits applied outside their approved scope, or typography/spacing/component behavior contradicting `DESIGN.md`.
3. **Polish:** alignment, rhythm, optical balance, wrapping/truncation, icon sizing, image treatment, and motion timing.

For each finding identify the screen/component, observed behavior, violated rule or user impact, evidence, and concrete correction. Mark subjective alternatives as decisions for the user rather than defects.

## Coverage

- representative narrow, medium, and wide widths plus stress points between them;
- realistic content density, long labels, empty/dense data, localization expansion, and zoom/reflow;
- hover, keyboard focus, active, selected, disabled, loading, empty, success, and error states as applicable;
- reduced motion, keyboard order, target sizes, semantics, and non-color feedback;
- consistency across repeated components and absence of unexplained one-off values;
- visual continuity between marketing pages and product UI without forcing them to identical density.

## Site check

Use this before showing a set of mockups and before reporting a built site as done. It adds seven passes to the review above.

**1. Static check.** Run `python scripts/check_site.py <dir>` from the skill directory against the mockup or build output (HTML and CSS). Findings carry a tier:

- `FLOOR` — never ships: missing `lang`, viewport, image `alt`, form labels, accessible names on icon-only controls, duplicate IDs, in-page links (`href="#…"`) whose target is missing or has no visible heading, focus outlines removed with no `:focus-visible` replacement, motion with no reduced-motion alternative. Fix all of them.
  - `title-option-label` — a `<title>` that names a layout option, not the page (「목록 2 거르기 칩 고정」, 「2 아이들 먼저」, 시안, option/layout): number then space, a word followed by a lone digit, 「N안」.
  - `date-weekday` — a date written with its weekday that does not match (「11월 19일 수요일」 when the 19th is a Thursday): checked against a 「20XX년」 on the page, otherwise this year and next. A client-supplied sample notice had this; compute weekdays from the date in the build script instead of typing them.
  - `repeated-heading` — the same h1–h3 text twice on a page, or an h2/h3 sharing six or more leading Hangul characters with the h1 (「가족을 기다리는 아이 52마리」 / 「가족을 기다리는 아이들」); 견본 marks are ignored.
- `DRIFT` — values that bypass tokens: raw colours or font sizes outside the token file, `!important`, `transition: all`, and `photo-reused-across-pages` — one image file on three or more pages with at least one use outside a card, thumbnail or the item's own gallery (class names pet/card/thumb/mini/row/media/gallery/th), or twice outside cards on one page; a sample photo appears once in the flow. Fix, or keep with a one-line reason recorded in `DESIGN.md` § Implementation mapping as an approved exception. Layout options (`today-1/2/3.html`) and judge copies (`-clean`) count as one page.
- `NOTE` — patterns that often signal generic output (gradient text, more than two font families), a page with no logo, mark, icon or image at all (`no-visual-layer` — text and boxes only usually reads as unfinished next to a running site), and an in-page link whose words share nothing with the heading it lands on (「수업 시간 보기」 landing on 「초등학생」 — the reader clicked one name and got another; rename the link or give the section the heading the link promises). Also `one-colour-blocks` — one strong colour (dark, or highly saturated) fills five or more block roles (button, band, panel, toast…, `var()` resolved from `:root`) and no second strong block colour exists; keep the accent for the main button and status and let bands and panels go white with lines, rather than adding a second accent (`color-selection.md`). And `unsourced-rule` — shop-rule wording (안 돼요, 못 해요, 불가, 금지); confirm the user gave each rule, and delete invented ones rather than marking them 견본 — a bakery mockup said 「영어·이모티콘은 안 돼요」 when the shop writes HAPPY BIRTHDAY and piped hearts, and 「딸기 철이 아닐 땐 냉동 딸기」, a line that would stop customers buying. And `unsourced-duration` — copy with a time or frequency guess (보통, N분쯤, N주쯤, N일 안에) not inside or beside a `class="sample"` mark; keep only what the user gave. Review against `DESIGN.md`; keep when the approved concept calls for it.

The script reads markup and stylesheets only. It cannot see contrast on rendered colours, layout, or overflow; the next pass covers those.

**2. Render pass.** Open every page at ≈375, ≈768, and ≈1280px and capture screenshots with `scripts/capture.mjs`; a headless window resized below about 500px still lays out wider, so window-size screenshots of phone widths are not evidence. Check horizontal overflow (capture prints 「넘침」 with the element and how many px it sticks out — fix every one), the longest label at the narrowest width, the hero or first screen fitting the viewport, sticky regions, keyboard order with a visible focus ring on every control, 200% zoom, and each state listed for the page in `SITE-PLAN.md`. Compute contrast for each text/background pair actually used from token values, not by eye.

**2b. Skeleton pass.** Run `node scripts/skeleton.mjs <out.md> <ours>=<home> <ref>=<url> … --ours <ours>` at 1280 (`--prev <earlier homes>` only when testing the skill — the client never sees other projects). It reports how much of the page is one stacked column, the most columns, column changes, side panels, sideways strips, round boxes and shapes, and at 390 also photo corners, button shape, how much of the page sits in tinted or framed boxes and boxes inside boxes. Run it at 390 as well as 1280. Treat 「공통 범위 밖」, 「참고 한 곳과 거의 같은 뼈대」, 「참고 한 곳과 같은 생김새(폰)」, 「상자 위에 상자」 and 「칸 속 칸」 as findings; photo corners and button shape are information, never a target: redraw from the references' shared traits and the concept, or record in `DESIGN.md` why this project departs from them.

**3. Fresh reviewer.** When a subagent is available, give it the screenshots, `DESIGN.md`, and `SITE-PLAN.md` only — not your reasoning — and ask it to find where the site breaks its own rules, where pages disagree with each other, and what looks unfinished. Verify each finding against the current files before acting on it. Without a subagent, state that this pass was skipped.

**4. Companion checks.** Run hallmark's `sloplint`, the impeccable detector and the Web Interface Guidelines review described in `companion-skills.md` whenever they were installed or approved at the start-of-project check; they are not optional extras once agreed. Map their findings to the tiers above and report each as ran, skipped (with the reason agreed with the user), or failed.

**4b. Wording.** Run the `ui-wording` skill (bundled in this repository) over the pages: one name per thing, the words similar services already use, one tone, one button form. Show the user its term table before applying it.

**5. Reference critique.** Open each page beside the primary reference at the same width at 1:1 with `scripts/side_by_side.py`, and fill in its layer table (identity, item faces, icons, colour blocks, data marks, imagery, depth, wide-screen columns, type contrast). More than two layers missing without a recorded replacement means the set is not ready, however clean it is; `check_site.py` reports a page with no logo, mark, icon or image at all as `no-visual-layer`. Name where the page is flatter, denser, more generic or less finished than the reference — image scale, white space, type contrast, component detail, copy — and fix those before calling the set ready. Passing passes 1–4 only proves nothing is broken; this pass is about whether it is good.

**5b. Numbers against the reference.** Run `scripts/extract_styles.mjs` on our first screen and densest page and on the reference's matching pages at the same width, and compare the summaries: corner radius, shadows, number of boxes, number of photos, type sizes, button size. The generated look has a profile — larger radii, more shadows, more boxes and fewer photos than the reference, every section in the same container. Bring each number to the reference's range or record why not.

**6. Trade test.** Do this for every page type, not only the first screen; forms, confirmations and admin screens are where sites fall back to the generic booking-app look (white rounded cards, one filled button). Cover the name and logo on each. If it could belong to a different trade — a pottery studio's page passing for a piano school's — strengthen the element only this business has (`design-selection.md` § 1) or change the composition before showing it. Booking, checkout and account screens are the usual offenders: a stay site's date picker and checkout read as a hospital booking app until a photo band of the room and the heading face came back. Carry the signature into the plain screens too: the league's scoreboard figures belonged on the sign-up page's seats-left number as well, and the client noticed they were missing.

Report the result as counts per tier plus the findings that remain, each with the page, the evidence, and the fix or the recorded reason for keeping it. Do not call the site done while a `FLOOR` finding remains.

## Correction protocol

Fixes require user authorization when the request was review-only. When fixing, update the highest reusable layer first: `DESIGN.md` decision → semantic token → shared component → page exception. If a finding exposes a concept-level conflict, stop broad propagation and return the decision to the user.
