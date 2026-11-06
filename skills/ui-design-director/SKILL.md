---
name: ui-design-director
description: Guide users conversationally from an overall UI concept to a complete website or web app design — researching well-known real sites in the user's field and template-marketplace candidates as motifs, and 3–4 color palettes, comparing coded previews, recording approved choices in DESIGN.md, planning every page in SITE-PLAN.md, approving layouts and full-fidelity mockups page by page, then building and checking the site. Use when a user wants to choose a design, design or build a whole site or app, redesign, extract a design system, or set project-wide UI direction; do not trigger for isolated styling fixes.
---

# UI Design Director

Turn the user's taste into an approved design language and carry it through every page. The user makes each visual decision; you bring research, side-by-side comparisons and a recommendation.

**Quality bar.** A design professional shown our pages shuffled with running sites of the same field should not pick ours out as AI-made. Before the user sees a first screen or page type, check it two ways: composition numbers against two to four running sites (`scripts/compose_metrics.mjs`; never show while a line reads 「미달」) and a 1:1 side-by-side with the base at the same width, which you look at yourself. A blind judge (`scripts/blind_sheet.py`, [references/blind-judge.md](references/blind-judge.md)) runs once, only when the user asks. The last word is the user's score out of 10 for our phone first screen next to two or three running sites. **Plain-model test, once, on the first screen before the layout gate:** one subagent builds the same first screen from the client's own words only — no skill, no files of ours — and you capture it beside ours at both widths. If ours differs only in colour, or the plain one puts more of this product's own character up front, do not show ours; rework what leads the screen. A marketplace built with this skill came out the same as the plain one (white, chips, photo cards, one accent), and the plain one led with the 단지 switch and meeting places.

## Budget

Most users are on a Pro-level plan. Aim for under 250 turns to approved mockups. Every turn re-reads the whole conversation, so cost is turns × conversation length.
- **Subagents: one per mockup page, nowhere else.** By the mockup step the main conversation re-reads about 250k tokens a turn; a subagent starts from the files at about 40k. Brief it with file paths only: the page's `SITE-PLAN.md` row, the approved layout file, `DESIGN.md`, `tokens.css`/`components.css`, the client's open requests for that page, and **a capture and `extract_styles` values of the same page on the base, at both widths**. If the base's page is behind a login or does not exist, capture the same page on the closest field site that shows it publicly, and tell the client which site it came from. Never describe a reference page in words instead — a marketplace's upload form briefed as "당근's 내 물건 팔기: photo tile, title, toggle…" came out as a generic boxed form, and its desktop was a phone column in an empty white screen. It builds the page, runs the self-check, captures once, and returns at most ten lines plus the paths of pictures to send; at most 30 turns, then it reports what is left. References, colours and layouts stay in the main conversation — parallel subagents capturing and re-capturing once doubled a project's total.
- **Few rounds.** About 5 reference sites; 2 layout options for the home page only (other page types follow it, one option each); mockups of the home and the main-job page first, the rest after approval; at most two rounds of fixes per gate before asking the user.
- **Each picture once, small.** In the main conversation open only the pictures you send, once each. To check a fix, crop the changed part to about 1200px or less; never open the same capture twice. Re-capture only the page and widths that changed.
- **Change lines, not files.** Fix with `Edit` on the changed lines. Do not rewrite a page with `Write` for a small fix or run long inline Python/`sed` that rewrites files — the text stays in the conversation. Keep reusable scripts in a file and run them by path; print only summary lines (`| tail -5`).

## Before each message with a picture or page

Run `python scripts/preflight.py <project folder>` and fix or answer every line it prints. Then check these, which a script cannot see, and say which you checked:

1. **Photos — who and whose.** List the people, signs, price cards, screens and number plates in every photo; ask whose they are; crop rather than blur. Caption each photo by what it shows, and a food photo that shows more than the cheapest item says so.
2. **Say only what you send.** Describe a reference only from the frames you attach; count shared traits as 「n/N곳」, never 「all」.
3. **The base, not a collage.** The base the client picked sets design, layout and parts. Change only what several field sites do differently (`scripts/skeleton.mjs --base <name>` at 390 and 1280, 「바꿀 곳」 n/N in `DESIGN.md`), and replace its text, photos and logo with the client's own. Shared traits alone give the average website; a template left with its own content stays the template. A part the base lacks comes from the field sites (n/N) or the client's own objects (menu board, sign, ticket), recorded in `DESIGN.md` § 부품 출처. Borrow from another site only by name and for a stated reason.
4. **Not recognisable as someone else.** If the base is a famous service the client's users know (당근 for a neighbourhood market), nobody should say 「이거 ○○ 아냐?」 at first glance. Name the parts that make it recognisable — brand colour, logo shape, mascot, signature icons, set phrases, a component only that service has — change them, and tell the client which. Do it unasked; clients rarely mention it and notice it first. What you take off the base's face, replace with this product's own content and photos, not with new boxes. Never copy protected logos, illustrations or text.
5. **Rules forbid; they are not a template.** A café and a snack stall built from this skill's rules alone came out as the same page (boxed wordmark, label–value rows, one navy button with a text link, dated notice rows). Parts take the base's form, not the rules' (`page-design.md` § A face, not a kit). "Too boxy" means remove stacked boxes, not round everything.
6. **Phone and desktop both**, starting with the width the client's users use first; a phone stack stretched to desktop is a finding.
7. **Colours.** Keep the base's colour fields (a cream band, a dark header) in the chosen palette; say so if a requested mix makes two accent colours.
8. **Computed, not typed.** Open/closed, next closing day (「둘째·넷째 수요일」 → a date), counts, totals, relative times — from one function and one data file; check edge cases (closed day, before opening, none left).
9. **Owner screens forgive.** Confirm before a change others see, a large undo after, number fields for prices with a changed-values check; say who to contact for what the owner screen cannot do and what to do if the phone is lost.
10. **Dislikes and reasons hold.** Check every candidate against the brief's dislikes at every gate, not only the first. Check each deliverable against the reason you gave for it (a slot "so parents see the classroom" filled with a keyboard close-up was caught by the user).
11. **Look at it** at the size the client will see it; check that fonts actually differ between font options.
12. **Judge copy (only when asked).** Capture it with `"judge": true` (`capture.mjs`), clear every 「판정 흔적」 it prints, never send it to the client, and report the judge's number with its reasons.

## Conversation

For a broad request ("I want to choose a design") read [references/guided-conversation.md](references/guided-conversation.md) and lead: one consequential question at a time, concrete numbered choices shown as pictures, plain words instead of design vocabulary, the next step always obvious. Show every choice visually ([references/comparison-board.md](references/comparison-board.md)); never ask the user to choose from links, a folder or a table. If the user delegates a choice, make it and record that it was delegated.

## Route the request

On entry, read project-root `DESIGN.md` and `SITE-PLAN.md` if they exist and resume from the first open gate; do not redo approved decisions. Advance only to the next gate the user authorised: "find a design" is not approval to implement, "design the site" is not approval to write production code.

- **Main page only** (the user wants just the home/first page): gates 1–3, then build that one page by the § Main page recipe; skip the site plan, layout options and other pages. Aim for under 80 turns.
- **Concept** (format or palette undecided): [design-selection.md](references/design-selection.md), [color-selection.md](references/color-selection.md). Format and palette are separate decisions.
- **Preview** (finalists exist, user wants them applied): [concept-preview.md](references/concept-preview.md).
- **Extract** (format and palette approved, or a partial draft requested): [reference-extraction.md](references/reference-extraction.md), [design-md-format.md](references/design-md-format.md) → `DESIGN.md`; a partial draft stays provisional.
- **Site plan** (`DESIGN.md` exists, whole site wanted): [site-plan.md](references/site-plan.md) → `SITE-PLAN.md`.
- **Pages** (`SITE-PLAN.md` approved): [page-design.md](references/page-design.md), [mockup-content.md](references/mockup-content.md), [owner-screens.md](references/owner-screens.md).
- **Build** (mockups approved, production code requested): [site-build.md](references/site-build.md).
- **Apply** (restyle an existing product from an approved `DESIGN.md`): map it to shared tokens and primitives; implement one representative slice before spreading it.
- **Review** (consistency check, or work about to be shown as finished): [ui-review.md](references/ui-review.md), including § Site check for mockups and sites.

## Main page recipe

The answer key is the base's own home page; reproduce its design, then make it ours so it does not read as copied.
1. Capture the base home at 390 and 1280 and run `scripts/extract_styles.mjs` on it. Write `formats/바탕-구성.md`: its sections top to bottom, each with height share of the page, photo share, type sizes, columns, and what the section does.
2. Build our page section by section from that table: same order, proportions, density, photo share, type scale, spacing, radius and shadow. Do not invent a structure and do not rebuild from generic rules.
3. Make it ours: our name, content, photos and the chosen colours; change the one or two places where several field sites share something the base lacks (n/N); take at most one section from another shortlisted site, by name. Our character comes through photos and wording, not through added boxes: a first screen the base keeps to photo and menu stays photo and menu.
4. Not a copy: at first glance nobody says 「이거 ○○ 아냐?」 — no base logo, mascot, brand colour, set phrases or a component only the base has. A base part you keep keeps its look (its drawing, lines, photo); if you cannot carry the look, drop the part rather than leave a bare text version.
5. No more boxes than the base. Count on both pages the bordered or filled rectangles — cards, panels, tags, labels, button blocks, tinted bands; ours may not have more. Text and photos sit on the page; labels are plain text; corners and button shapes follow the base. Colour fields only where the base has them — no pale tinted bands to separate sections.
6. These read as generated (user, camping site): a white panel floating on the hero photo with label–value facts, letters or emoji in circles as icons, a small overline above the name, a row of identical icon tiles, dashed 「… 자리」 placeholder boxes, pale bands everywhere.
7. Before sending, put ours beside the base at both widths (`scripts/side_by_side.py`) and fix every place where ours is emptier, plainer or more boxed than the base.
8. Send `index.html` with the base first and ours next, at both widths.

## Gates

1. **Context.** A short concept brief: product and main job, audience, archetype (marketing site, dashboard, editing tool, form workflow, content reader), essential screens, content density, brand traits, constraints, dislikes; ask only what would change the shortlist and label what you inferred. Ask in the same step for what only the user has — their own photos, logo or sign artwork, a notice or two in their own words — and say plainly that samples cap how real it can look. In the same step run [companion-skills.md](references/companion-skills.md) § Start-of-project check: ask the machine owner once, record the answer.
2. **Format.** About five well-known running sites in the field (the national leaders people already use) and one or two template candidates, side by side, marked and linked. Say the shared traits (n/N) when you show them. The user picks **one base**.
3. **Palette.** 3–4 linked palettes, separate from the format, with UI roles and contrast risks. A template's default colours never decide the palette silently.
4. **Preview.** A coded comparison of finalists with identical content, when it helps or the user asks; disposable.
5. **Rules.** Adapt the approved format and palette into `DESIGN.md`: observed evidence, product decisions, unknowns; high-impact open choices get approved, small defaults stay marked provisional. Concept approval needs every axis resolved.
6. **Site plan.** Page inventory and main flows in `SITE-PLAN.md`, approved before pages; each page is a read surface or a work surface.
7. **Layout.** Two numbered home options that differ in structure, in the approved colours and fonts with everyday sample photos, at both widths; each passes the composition numbers and avoids the formulas in `page-design.md`. Settle the shared frame (navigation, footer) once.
8. **Mockups.** Full fidelity from `DESIGN.md` tokens and components, both widths, every required state, home and main-job page first; give pages the information layer a running organisation has (utility bar, dated news, specifics labelled as samples); pass § Site check; hand over a clickable prototype; approval per page.
9. **Proof.** For production, one representative page or slice at the relevant sizes and states before the rest.
10. **System.** Move every approved reusable change into `DESIGN.md` and the shared tokens and components; chat and page-local CSS are not durable.

## Always

- Verify every candidate before presenting it: open it, and state prices, licences, coverage and responsiveness only from what you inspected; if you cannot, say so — never invent or imply inspection.
- Licences from the published text, not memory. For commercial use, a licence that forbids or charges for it disqualifies the candidate; say what you verified and what needs legal review.
- Build from measured values, not prose: for each page type run `scripts/extract_styles.mjs` on the base (and one more shortlisted site if the base lacks that page) at both widths, and take type sizes, spacing, shadows and the photo-to-box ratio from it. A stay site built from written rules had 3 photos and 11 shadowed 12px boxes where the reference had 56 photos, 6 boxes and no shadows.
- Match the reference's finish, not only its structure: inventory its visual layers (identity, item faces, icons, colour blocks, data marks, imagery, depth, wide-screen columns) and keep, replace or knowingly drop each; a dislike replaces a layer's form, it does not delete the layer.
- Use proven UI for date pickers, bottom sheets, galleries, steppers, tabs and checkout forms — a known design system (licence checked) or the pattern a leading site uses, named in `DESIGN.md`. Block libraries are for parts, never the composition.
- No generic AI decoration (gratuitous gradients, glass, pills everywhere, oversized hero text) unless the base does it. Run the AI-tell checks before showing (hallmark `sloplint`, the impeccable detector, `ui-review.md` § Site check) and report each as ran or why not.
- Accessibility is a baseline: visible focus, contrast, non-colour cues, 44px targets, semantic controls, reflow and zoom, reduced motion.
- Never present invented testimonials, logos, statistics, awards or screenshots as real; use the user's material, or for these leave the part out.
- Keep existing brand constraints unless the user approves changing them. When requirements conflict with the reference, explain and put usability, accessibility, brand constraints and the user's decisions first.
- Spend the session on the design, not on tooling: use the bundled tools as they are; fix one only when it blocks the user.

## Companion skills

ui-ux-pro-max, hallmark, emilkowalski/skills, impeccable and Vercel's Web Interface Guidelines do parts of this work better; use them as designed, per [companion-skills.md](references/companion-skills.md). Install nothing without the machine owner's approval. Screen wording goes through the sister skill `ui-wording`.

## Project folder

`scripts/preflight.py` reads these names:

```
<project folder>/
  concept-brief.md      gate 1: the client's words, photos and who/whose notes
  formats/              gate 2: captures, jobs*.json, skeleton tables (390 and 1280)
  DESIGN.md             gates 3–5: base, palette, type, tokens, 바탕에서 바꾼 곳 as 「n/N곳」
  SITE-PLAN.md          gate 6: pages, flows, owner sign-in and lost phone
  layouts/              gate 7: numbered options
  mockups/              gate 8: clickable mockups; pictures sent to the client in mockups/보낼-그림/
  blind/                judge sheets
```
