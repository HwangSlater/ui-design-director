# Designing every page

> Checks before each message: SKILL.md § Before each message with a picture or page. Building rules: [build-rules.md](build-rules.md). Content rules: [mockup-content.md](mockup-content.md). Owner screens: [owner-screens.md](owner-screens.md). Composition numbers: [blind-judge.md](blind-judge.md) § Composition numbers.

Keep the `SITE-PLAN.md` status columns current.

## Contents
- 1. Layout options
- 2. Mockups
- 3. Consistency across pages
- 4. Mockup approval gate

## 1. Layout options

Options differ in **structure**, not styling: what leads, content order, how the main action is reached, how the page reflows on a phone.

### Skeleton from the base

The base the client picked (`design-selection.md` § 4) gives the look — type contrast, colour fields, photo placement, part shapes — and the starting layout. Where several field sites share a trait the base does not (or lack one it has), take theirs; everywhere else keep the base's section order and column split.

1. Run `node ${CLAUDE_SKILL_DIR}/scripts/skeleton.mjs formats/뼈대-390.md --width 390 --base <name> <name>=<url> …` on the base and the field sites, and again with `--width 1280`. Its 「바탕과 다르게 할 곳」 (the 「바꿀 곳」) lists only what two or more sites, more than half, do differently from the base (「옆으로 넘기는 띠: 바탕은 없음, 3/5곳은 있음」).
2. Take each listed change or leave it, and record both in `DESIGN.md` § 바탕에서 바꾼 곳 with the count. Everything else follows the base.
3. Replace the base's text, photos, logo and illustrations with the client's own.
4. Add content patterns the tool cannot see (hours, last drop-off and phone number in one block), and check the base answers each of the client's top customer questions (「출퇴근용으로 뭐 사요?」); a missing answer is a change, taken from the field sites.
5. Options are variations within the base: what leads, which listed change is taken, how the main action is reached.
6. Before showing, rerun with `--ours <option>`. 「바탕과 다름」, 「바탕의 짜임을 버림」, 「상자 위에 상자」 or 「칸 속 칸」 means redraw, or say in one line why.
7. Compose each width from the base's own phone and desktop pages (build-rules.md § Follow the base 5).

Platform pages (Naver Place, Instagram) are never references (design-selection.md § 3).

### Measure the reference pages

1. Run `node ${CLAUDE_SKILL_DIR}/scripts/extract_styles.mjs <url> <out.json> --width 390`, then at 1280, on the base's page doing the same job (one shortlisted site's if the base lacks it). `DESIGN.md` tokens (type scale, radius, shadow, button and input size, section spacing, photos against boxes) take the base's values; move one only where the skeleton tables show the field sites agree against it, citing them.
2. Take components (calendar, sheet, gallery, form, tabs) from a known design system or the reference's pattern, and name the source.
3. Borrow a pattern whole: list its parts and check them off (a donation form lost its 「다른 금액」 field).
4. Carry the `DESIGN.md` visual layers into every option (build-rules.md § Follow the base 6).
5. Note what the shortlisted sites do well in common (image size, white space, type hierarchy, density); every option keeps it. Follow the base's composition and rhythm closely; only a component that identifies one site (its mascot, a trademark widget) stays theirs.

### Checks for each option

1. Approved tokens and a sample photo in every photo place (build-rules.md § Content and samples); colour, type and photos identical across options.
2. Real or planned `SITE-PLAN.md` content at real length.
3. Capture wide and phone with `${CLAUDE_SKILL_DIR}/scripts/capture.mjs`; show options in the `comparison-board.md` viewer.
4. One line per option: what it prioritises and what it gives up.
5. At least one option changes the **first screen** itself (full-width photo, type only, price list first, one strong object); two options that both open text-left, photo-right are one option.
6. Options differ on the first phone screen, or the name says where they start to differ (「2 — 사진 바로 밑에 객실」).
7. No more than two sections in a row share a container; photos keep appearing down the page (one per section when the reference does so).
8. Work screens (date pickers, checkout, account) keep a photo band of what is booked or bought, the heading face and one signature element, or they read as a generic booking app.
9. When the home leads with the same list as a section page, give the home its own first line (name and one sentence).
10. When the page has sticky parts, check them with one one-screen capture at a scrolled position (`capture.mjs` job with `"scrollY"`), not a full-length capture.
11. Times and prices in the body face with tabular figures.

### Parts from the base

Before the first layout, list the parts the page needs (name, today's status and hours, the contact action, notices, main items and prices, photos, directions, the client's story). Each takes the base's form for it. For a part the base lacks, look at how the field sites show it and count (「시간을 첫 화면 큰 글씨로 3/6곳」), or at the client's own objects (the menu board, the sign, the order slip). Write `DESIGN.md` § 부품 출처: part → form → source (base, n/N, or the client's object). Two projects whose references differ should not end with the same parts; if a part is drawn the way this file's examples are, check it came from this project's references, not from the skill.

### A face, not a kit

A gate before the first layout is shown.

1. **A face.** The name, colour and one motif come from the client (its sign, its trade's objects), set in the base's type and colour fields (a second accent only when the client picks it), icons in one style.
2. **Not the generated look.** Check every option against build-rules.md § What reads as generated. Three sections in a row with the same make-up (「heading → list → small grey note」) get two changed, using the base's forms (§ Parts from the base). "Too boxy" means stacked boxes: remove tinted panels and boxes inside boxes; do not round everything or copy another site's shapes.
3. **The client's voice, shorter.** Keep computed, kind lines (「지금 맡기시면 내일(목) 저녁」) once each.
4. **One photo grade.** Same crop logic, white balance and contrast; fewer, larger photos.
5. **What reads as running.** The main job as a real input on the first screen (a search box, not a 「책 찾기」 button); the client's own rooms and goods in the photos; no borrowed chain-store hero.
6. **Filled like a running organisation.** Keep what the base has and add what the field sites share — utility bar (hours, phone, messenger), quick links as plain text, dated news, an Instagram strip, a multi-column footer — listed in the 「견본」 line. No features a small organisation would not have (a filter bar for 50 items).

### Questions per surface

Derive options from the page's job, not a fashionable shape; name hallmark shapes only afterwards (`companion-skills.md`).

- **Read surface:** What must the visitor believe, and what proves it? Proof or claim first? Where does the action repeat, and when is it lost?
- **Work surface:** What is looked at and changed most? List → detail, split, canvas, or steps? What stays fixed? What at 0, 1 and 1,000 items?

### Choosing

Recommend one option with a reason tied to the job; the user picks a number, combines named parts or rejects. Mark `Layout` approved only on the user's choice or explicit delegation.

## 2. Mockups

Build the approved layout with only `DESIGN.md` tokens and components. Each page is built by its own subagent with a brief of file paths (SKILL.md § Budget).

### Where mockups live

Outside production routes in one folder (default `mockups/`) with an `index.html` linking every page and state; static HTML/CSS loading one `tokens.css` and one `components.css`, pages holding layout only. If a local component library exists, use it on a non-production route instead.

### Self-check before showing

1. Sort every name, number and date as **given**, **derived** or **invented**; invented items a reader could take as real get 「견본」.
2. List sample items in the one 「견본」 line at the page foot (build-rules.md § Content and samples).
3. Diff the mockup text against the chosen option and report every lost line.
4. Run `ui-review.md` § Site check passes 1, 2, 2b and 5 on this page (fix every `FLOOR`; side-by-side for the first screen and densest page). Name and fix three places flatter, denser, more generic or less finished than the reference.
5. Capture once, after the fixes, and send only those paths; on a later fix re-capture only the changed page and widths.

### Handing over

1. A collapsed 「상태」 switcher per page, clear of toasts, bars and dialogs, with the main flows linked.
2. Read-only site for a non-developer client: no switcher; describe fallbacks in one sentence (「인터넷이 느리면 사진 대신 빈칸이 보여요」).
3. Prototype notes go after the footer under 「시안 안내 — 손님에게는 안 보여요」; prototype script and styles stay in separate files.
4. Click the flows in a real browser at both widths; give the entry page's full path and what to look at.
5. Name photos by what they show (「밭 사진」), not the slot.
6. Use the screenshot viewer only for choosing layouts.
7. Ask approval per page type. Sort feedback with `design-md-format.md` § Feedback protocol; site-wide changes go into `DESIGN.md`, `tokens.css` and `components.css`.

## 3. Consistency across pages

Render approved core pages side by side; check navigation, footer, heading scale, spacing, button hierarchy, and empty and error states. Fix drift at the shared layer. Record one-page components in `DESIGN.md` § Components when approved.

## 4. Mockup approval gate

Approved when every core page type has `Mockup: approved` in `SITE-PLAN.md`; list pending secondary types as remaining work.
