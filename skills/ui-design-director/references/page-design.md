# Designing every page

> SKILL.md § Before you send anything to the client lists the checks sessions skip most. This file covers layout options and mockup gates. Content rules: [mockup-content.md](mockup-content.md). Owner screens: [owner-screens.md](owner-screens.md). Composition numbers and blind judge: [blind-judge.md](blind-judge.md).

Use this after `SITE-PLAN.md` is approved. Each page type passes a **layout** choice, then a **mockup** approval, before production code. Core page types first; keep the `SITE-PLAN.md` status columns current.

## 1. Layout options

For each page type, offer 2–3 numbered options that differ in **structure**, not styling: what leads, content order, how the main action is reached, how the page reflows on a phone.

### Skeleton from the base

The base the client picked (`design-selection.md` § 4) gives the look — type contrast, colour fields, photo placement, part shapes — and the starting layout. The layout follows the field where the field agrees: where several field sites share a trait the base does not (or lack one it has), take theirs; everywhere else keep the base's section order and column split. Commonality alone gives the average website: a café, a snack stall and a vintage shop built from shared traits all came out as white page, hairlines, square boxes and one accent.

1. Run `scripts/skeleton.mjs out.md --base <name> name=url …` on the base and the field sites, separately at `--width 390` and `--width 1280`. Its 「바탕과 다르게 할 곳」 lists only what two or more sites, more than half, do differently from the base (「옆으로 넘기는 띠: 바탕은 없음, 3/5곳은 있음」).
2. Take each listed change or leave it, and record both in `DESIGN.md` § 바탕에서 바꾼 곳 with the count. Everything else follows the base.
3. Replace the base's text, photos, logo and illustrations with this shop's; a template's own content left in place is what made a pottery site look like its template.
4. Add content patterns the tool cannot see (hours, last drop-off and phone number in one block), and check the base answers each of the owner's top questions (「출퇴근용으로 뭐 사요?」); a missing answer is a change, taken from the field sites.
5. Options (2–3) are variations within the base: what leads, which listed change is taken, how the main action is reached.
6. Before showing, rerun with `--ours <option>`. 「바탕과 다름」, 「바탕의 짜임을 버림」, 「상자 위에 상자」 or 「칸 속 칸」 means redraw, or say in one line why. (`--prev` compares with earlier projects; the client never sees those, so it is only for testing the skill.)
7. Compose phone and desktop both, starting with the customers' device, from the base's own phone and desktop pages. A phone stack stretched to desktop is a finding.

One platform's pages (Naver Place, Instagram) count as one reference.

### Measure the reference pages

1. Run `node scripts/extract_styles.mjs <url> <out.json> --width 390`, then at 1280, on the base's page doing the same job, and on two or more field sites. `DESIGN.md` tokens (type scale, radius, shadow, button and input size, section spacing, photos against boxes) take the base's values; move one only where the field sites agree against it, citing them. Keep the base's screenshots open while building.
2. Take components (calendar, sheet, gallery, form, tabs) from a known design system or the reference's pattern, and name the source.
3. Borrow a pattern whole: list its parts and check them off. A donation form lost the 「다른 금액」 field its pattern had.
4. Carry the `DESIGN.md` visual layers (identity, item faces, icons, colour blocks, data marks, wide-screen columns) into every option; text on grey with white cards is a wireframe.
5. Note from 1:1 captures what the shortlisted sites do well in common (image size, white space, type hierarchy, density); every option keeps it. One site's signature component stays theirs.

### Checks for each option

1. Approved tokens and a licence-checked sample photo in every slot (`comparison-board.md` § Sample photos); colour, type and photos identical across options.
2. Real or planned `SITE-PLAN.md` content at real length.
3. Capture wide and phone with `scripts/capture.mjs`; show options in the `comparison-board.md` viewer.
4. One line per option: what it prioritises and what it gives up.
5. At least one option changes the **first screen** itself (full-width photo, type only, price list first, one strong object). Three options opening text-left, photo-right are one option.
6. Options differ on the first phone screen, or the name says where they start to differ (「2 — 사진 바로 밑에 객실」).
7. No more than two sections in a row share a container; photos keep appearing down the page (one per section when the reference does so).
8. Work screens (date pickers, checkout, account) keep a photo band of what is booked, the heading face and one signature element, or they read as a hospital booking app.
9. When the home leads with the same list as a section page, give the home its own first line (name and one sentence).
10. Judge the first screen and sticky parts with one-screen captures at several scroll positions (`capture.mjs` job with `"scrollY"`), not a full-length capture.
11. Times and prices in the body face with tabular figures; a monospace `14:00 ~ 19:00` read as generated.

### Parts from the base

Before the first layout, list the parts the page needs (name, today's status and hours, the contact action, notices, menu and prices, photos, directions, the owner's story). Each takes the base's form for it. For a part the base lacks, look at how the field sites show it and count (「시간을 첫 화면 큰 글씨로 3/6곳」), or at the shop's own objects (the menu board, the sign, the order slip). Write `DESIGN.md` § 부품 출처: part → form → source (base, n/N, or the shop's object). Two projects whose references differ should not end with the same parts; if a part is drawn the way this file's examples are, check it came from this project's references and not from the skill. The rules below say what not to do — they are not a template.

### A face, not a kit

A gate before the first layout is shown; judges named these in every round.

1. **A face.** The name, colour and one motif come from the shop (its sign, its trade's objects), set in the base's type and colour fields (a second accent only when the client picks it), icons in one style.
2. **No repeated section formula.** Three sections in a row with the same make-up (「heading → list → small grey note」, 「label – value rows」) read as generated; change two, using the base's forms (§ Parts from the base).
3. **No kit parts.** No left-border callouts, equal filled-and-outlined button pair as the main action, status dot before every state, same 6–8px radius on every box, tilted name tag, oversized corner on every photo, pills everywhere, or headline line in a second colour.
4. **"Too boxy" means stacked boxes.** Remove tinted panels and boxes inside boxes. Do not round everything or copy another site's shapes; a café that did heard 「네이버랑 똑같다」.
5. **The owner's voice, shorter.** Keep computed, kind lines (「지금 맡기시면 내일(목) 저녁」) once each; drop the grey footnote under every block, which reads as 「모범답안」.
6. **One photo grade.** Same crop logic, white balance and contrast; fewer, larger photos.
7. **Not the generated formula.** No stock photo with a floating box, headline and two buttons; no four icon cards over the photo edge; no display face on every title (one or two levels); no thin generic line icons.
8. **What reads as running.** The store's main job as a real input on the first screen (a search box, not a 「책 찾기」 button); the shop's own rooms and goods in the photos; no borrowed chain-store hero.
9. **Filled like a running organisation.** Keep what the base has and add what the field sites share — utility bar (hours, phone, messenger), quick links as plain text (not a row of identical icon tiles), dated news, an Instagram strip, a multi-column footer — labelled 「견본」 for the client. No features a small organisation would not have (a filter bar for 50 animals).

### Questions per surface

Derive options from the page's job, not a fashionable shape; name hallmark shapes only afterwards (`companion-skills.md`).

- **Read surface:** What must the visitor believe, and what proves it? Proof or claim first? Where does the action repeat, and when is it lost?
- **Work surface:** What is looked at and changed most? List → detail, split, canvas, or steps? What stays fixed? What at 0, 1 and 1,000 items?

### Choosing

Recommend one option with a reason tied to the job; the user picks a number, combines named parts or rejects. Mark `Layout` approved only on the user's choice or explicit delegation. Settle a shared frame (navigation, footer) once on the main page type.

## 2. Mockups

Build the approved layout with only `DESIGN.md` tokens and components.

### Where mockups live

Outside production routes in one folder (default `mockups/`) with an `index.html` linking every page and state; static HTML/CSS loading one `tokens.css` and one `components.css`, pages holding layout only. If a local component library exists, use it on a non-production route instead.

### Composition first

Every first screen and page type passes the composition numbers and blind judge before the client sees it: [blind-judge.md](blind-judge.md).

### Self-check before showing

1. Sort every name, number and date as **given**, **derived** or **invented**; invented items a reader could take as real get 「견본」.
2. Mark once per block at most, never on a photo or the first screen; write one line under it instead (「사진은 모두 견본이에요」).
3. Diff the mockup text against the chosen option and report every lost line.
4. Run `scripts/check_site.py` and fix every `FLOOR`; run the agreed companion checks.
5. Build `python scripts/side_by_side.py <out.html> <ours.jpg> <reference.jpg> …` for the first screen and densest page at both widths; fix every layer the reference has and ours lacks without a recorded reason.
6. Name and fix three places flatter, denser, more generic or less finished than the reference.
7. Fix everything you notice in your own screenshots, however small.
8. Check narrow overflow, the longest label, sticky regions and claimed states at three widths; without a renderer, say the check was structural only.
9. Capture again right before sending and send only those paths.

### Handing over

1. A **clickable prototype**, not screenshots: main flows linked, and a collapsed 「상태」 switcher per page, clear of toasts, bars and dialogs.
2. Read-only site for a non-developer owner: no switcher; describe fallbacks in one sentence (「인터넷이 느리면 사진 대신 빈칸이 보여요」).
3. Prototype notes go after the footer under 「시안 안내 — 손님에게는 안 보여요」; prototype script and styles stay in separate files.
4. Click the flows in a real browser at both widths; give the entry page's full path and what to look at.
5. Name photos by what they show (「밭 사진」), not the slot.
6. Use the screenshot viewer only for choosing layouts.
7. Ask approval per page type. Sort feedback with `design-md-format.md` § Feedback protocol; site-wide changes go into `DESIGN.md`, `tokens.css` and `components.css`.

## 3. Consistency across pages

Render approved core pages side by side; check navigation, footer, heading scale, spacing, button hierarchy, and empty and error states. Fix drift at the shared layer. Record one-page components in `DESIGN.md` § Components when approved.

## 4. Mockup approval gate

Approved when every core page type has `Mockup: approved` in `SITE-PLAN.md`; list pending secondary types as remaining work. No production code for an unapproved page unless the user explicitly asks.
