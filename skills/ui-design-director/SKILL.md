---
name: ui-design-director
description: Guide users conversationally from an overall UI concept to a complete website or web app design — researching well-known real sites in the user's field and template-marketplace candidates as motifs, and 3–4 color palettes, comparing coded previews, recording approved choices in DESIGN.md, planning every page in SITE-PLAN.md, approving layouts and full-fidelity mockups page by page, then building and checking the site. Use when a user wants to choose a design, design or build a whole site or app, redesign, extract a design system, or set project-wide UI direction; do not trigger for isolated styling fixes.
---

# UI Design Director

Turn subjective taste into an explicit, user-approved design language, then carry that language through every page of the site. The user owns each visual decision; provide strong research, comparisons, and a recommendation so that choice is informed rather than arbitrary.

## The quality bar

The result is judged against running sites, not against the brief. A beginner or a prototype maker must get pages that a design professional, shown them shuffled with real sites of the same field and country, cannot pick out as AI-made. Passing lint checks is not the bar: four projects that passed every check still looked like documents next to running sites. Every first screen and every page type goes through three gates before the user sees it — composition numbers against running sites (`scripts/compose_metrics.mjs`), a blind judge (`scripts/blind_sheet.py`, fresh agent, same-country controls), and a 1:1 side-by-side you look at yourself — and loops while the judge still names fixable tells (layout faults, invented copy, mismatched photos, generic formula). The judge is an AI agent, not people; say so whenever you report its numbers. Its AI-made percentage has a floor set by content you cannot design away (sample photos, a concept no small shop runs, every line in one tidy voice): in a bakery project seven surface variants — chalkboard, display face, the owner's own sentences, one photographer, a real shop's photos, a photo-only first screen — all stayed at 80–85% while a real site in the same run scored 10–15%. When two rounds of fixes no longer move it and the named tells are content-level, stop looping, report the number with its reasons, and gate on the design score instead (at or above the controls' median). The last word belongs to people: put the user's phone first screen next to two or three running sites of the same field and country and ask them for a score out of 10 for each; a bakery owner scored the finished mockup 6.5 against 5–8 for four real bakeries and named what would lift it (their own photos and sign lettering). See [references/page-design.md](references/page-design.md) § Composition first.

## Before you send anything to the client

These are the misses that recur even though each has a rule further down; fresh sessions followed them only after the client pointed them out. Before each message that carries a picture or a page, run `python scripts/preflight.py <project folder>` and fix or answer every line it prints — client-named channels missing from the references or the mockup, shared traits not counted (skeleton tables at 390 and 1280, 「n/N곳」 in `DESIGN.md`), owner sign-in and lost-phone screens, an equal pair of buttons as the main action. Then check the items below that a script cannot see, and say which you checked.

Keep the main conversation short: hand capture runs, re-renders and judge-sheet builds to a subagent and take back only paths and findings. In a measured café run the mockup phase was 55% of all tokens, mostly because every reply re-read the long conversation.

1. **Photos — who and whose.** List the people, signs, price cards, screens and number plates in every photo; ask the owner whose they are (a neighbour's staff, another stall's price card); crop rather than blur. Caption a food photo that shows a richer set than the cheapest menu.
2. **What you say matches what you send.** Describe a reference only from the frames you attach; count traits as 「n/N곳」, never 「all」; caption each photo by what it shows.
3. **Layout from what the references share.** Run `scripts/skeleton.mjs` on the shortlist at 390 and 1280 separately; build from the shared traits that suit this client; say which and why. Not one site's copy, not the last project's skeleton (`--prev`).
4. **Phone and desktop both.** Every layout and mockup message shows both widths; a phone-only stack stretched to desktop is a finding.
5. **Common colours first.** Start from the field's measured colours (usually white, near-black, one accent); say so if a requested mix makes two accent colours.
6. **A face and no kit.** A wordmark set like a sign plus one motif from the trade's own objects; no repeated heading-table-grey-note formula, no left-border callout, no equal filled-and-outline button pair as the main action. Shape is not the fix: when the client says "too boxy", take away the stacked boxes (tinted panels, a white box inside a tinted one) and divide with lines and space; do not round everything or borrow the round-photo strip and pill buttons of a platform page — a café that did both was told "it looks just like my Naver page". `skeleton.mjs` flags 「상자 위에 상자」, 「칸 속 칸」 and 「참고 한 곳과 같은 생김새」.
7. **Computed, not typed.** Open/closed, last order, next closing day (「둘째·넷째 수요일」 → a date), pickup day, totals for 2/3/4 people, weekdays — from one function and one data file; check the edge days (closed day, after last order, before opening).
8. **Owner screens forgive.** Confirm before a change customers see, a large undo after, prices as number fields with a changed-values check; say who to contact for what is not on the owner screen and what to do if the phone is lost.
9. **Fair blind sheet.** For the judge only: plausible values for 「0000」 numbers and 「○○○」, hatched photo or map slots filled or removed, `.sample` and prototype notes hidden. Report the judge's number with its reasons.
10. **Look at it.** Open every picture you send at the size the client will see it, and check fonts actually changed between font options.

## Guide the conversation

When the user gives a broad request such as “I want to choose a design,” read [references/guided-conversation.md](references/guided-conversation.md) and lead the process proactively. Do not wait for the user to know which design questions to ask. Ask one consequential question at a time, provide concrete choices and plain-language examples, remember previous answers, and always make the next step obvious.

## Route the request

- **Concept:** The format or palette is undecided. Read [references/design-selection.md](references/design-selection.md) and [references/color-selection.md](references/color-selection.md). Let the user select the overall format and base palette as separate decisions.
- **Preview:** Format and palette finalists exist but the user wants to see them applied. Read [references/concept-preview.md](references/concept-preview.md) and create small, comparable coded UI previews outside production surfaces.
- **Extract:** The format reference and palette are approved, or the user explicitly wants a partial draft. Read [references/reference-extraction.md](references/reference-extraction.md) and [references/design-md-format.md](references/design-md-format.md), then create or revise project-root `DESIGN.md`. A partial draft must keep unresolved selections provisional and cannot be marked approved.
- **Site plan:** `DESIGN.md` exists and the user wants the whole site or app designed. Read [references/site-plan.md](references/site-plan.md) and produce project-root `SITE-PLAN.md`: page inventory, flows, navigation, and per-page status.
- **Pages:** `SITE-PLAN.md` is approved. Read [references/page-design.md](references/page-design.md); for each page type offer numbered layout options in the approved tokens with sample photos, then build full-fidelity mockups from the chosen layout.
- **Build:** Mockups are approved and the user asked for production code. Read [references/site-build.md](references/site-build.md); move tokens, then shared components, then one representative page, then the rest.
- **Apply:** `DESIGN.md` is approved and the user asked to restyle an existing product without a page-by-page redesign. Read it first, map it to shared tokens and primitives, and implement a representative slice before broad propagation when practical.
- **Review:** The user wants consistency or quality review, or a set of mockups or a built site is about to be shown as finished. Read [references/ui-review.md](references/ui-review.md) and inspect rendered UI against `DESIGN.md`; for mockups and sites also run its § Site check.

On entry, read project-root `DESIGN.md` and `SITE-PLAN.md` if they exist and resume from the first gate they leave open; do not redo approved decisions.

If a request spans modes, advance only to the next decision gate that is authorized. Do not interpret “find a design” as approval to implement it, or “design the site” as approval to write production code.

## Required gates

1. **Context gate:** Establish a compact concept brief from repository evidence and user input: product/job, audience, interaction archetype, essential screens, content density, brand traits, constraints, and anti-preferences. Name the archetype explicitly: marketing site, dashboard, editing tool, form workflow, or content reader. Ask only for missing information that would materially change the shortlist; label inferred items. Ask in the same step for the material only the user has, because it decides how real the result looks more than any layout: five photos (the front with its sign, the counter or workspace, hands at work, the products as they are sold, the room), the sign or logo artwork, and lines in their own words for a notice or two. Until they arrive, use samples and say plainly that samples cap how real it can look — a finished bakery mockup scored 6.5 and the owner named their photos and sign lettering as the missing 1–2 points. In the same step run the companion check in [references/companion-skills.md](references/companion-skills.md) § Start-of-project check: tell the user in one short table which companions are installed, what each would add, and ask once whether to install the missing ones. Record the answer in the brief; a companion is never skipped silently.
2. **Format gate:** Present running sites in the user's field — well-known ones and smaller ones of the same country and size as the client — and template-marketplace candidates side by side. A template chosen as the primary reference produces a template (the pottery-class site built on a Framer template looked exactly like one); prefer a running site as primary and use templates for parts, both found from the brief's field, main job, concept and audience; mark which is which and give direct links. Let the user pick the sites whose tone they like and reject the rest. The pick sets tone; the page structure comes later from what the shortlisted sites share (count each trait as 「n/N곳」 with `scripts/skeleton.mjs` at 390 and 1280 now, and say the shared traits when you show the shortlist — not only when asked). No site is traced section by section.
3. **Palette gate:** Present linked 3–4 color palette candidates independently from the format. Explain intended UI roles and contrast risks. Let the user select, modify, or reject them; a palette's original swatches are inspiration, not yet complete semantic UI tokens.
4. **Preview gate:** Offer a coded comparison when visual judgment would benefit; create it when the user requests or accepts. Combine only finalists using identical content and component coverage. Preview code is disposable evidence, not approval or production implementation.
5. **Rules gate:** Extract and adapt the approved format and palette into `DESIGN.md`. Separate observed evidence, product-specific decisions, and unknowns. Ask for approval of unresolved high-impact choices; minor safe defaults may remain clearly marked as provisional.
6. **Site plan gate:** For a whole-site request, get the page inventory and main flows in `SITE-PLAN.md` approved before designing pages. Classify each page as a read surface or a work surface; they follow different rules.
7. **Layout gate:** For each page type, show 2–3 numbered layout options that differ only in structure, drawn in the approved colours and fonts with everyday sample photos, at phone and desktop width — the width the client's customers use first (phone for most local shops) — and let the user choose. Each option must already pass the composition numbers; avoid the generated formulas listed in page-design.md (floating box on a stock photo, half-and-half colour panel, row of identical icon tiles, symmetrical two-card split, display face on every heading). Settle the shared frame (navigation, footer, sidebar) once.
8. **Mockup gate:** Build full-fidelity mockups of each page type from `DESIGN.md` tokens and components, at three widths and in every required state, pass the § Site check — including the companion checks, the composition numbers and the blind judge (two shuffles, dummies such as 「0000」 and hatched slots replaced with plausible sample values in the judge's copy only; below 70% "AI-made", or the floor reached as described in "The quality bar" above with no fixable tell left) — and get per-page approval. Give the page the information layer a running organisation has (utility bar, dated news, real-looking specifics labelled as samples) rather than only what the brief lists. Hand them over as a clickable prototype.
9. **Proof gate:** When production implementation is requested, build or adapt one representative page/slice and show it at relevant viewport sizes and states. Propagate only after approval when the scope is broad.
10. **System gate:** Move every approved reusable feedback item into `DESIGN.md` and the shared token/component layer. Chat instructions and page-local CSS are not durable design decisions.

## Non-negotiable behavior

- Verify every candidate before presenting it: open the link, and state prices, licences, page coverage, and responsiveness only from what you actually inspected. If something is inaccessible, unverifiable, or live research is unavailable, say so and ask for user-provided references — never fabricate a candidate or imply you inspected one.
- Keep format, palette, and typography identifiable as separate choices. Do not let a template's default colors silently decide the user's palette.
- Do not mark the concept approved until format, palette, any high-impact adaptation, and requested preview feedback are resolved. Approval of one axis does not imply approval of another.
- Build the page structure from what the shortlisted references have in common, choosing among those shared traits the ones that suit this project (`scripts/skeleton.mjs` lists them) — not by ranking the sites and copying the winner, and not by reusing the last project's skeleton. The client's pick sets tone and direction; borrow a trait only one site has only by name and for a stated reason; do not create a collage of unrelated trends.
- Extract relationships and intent—not merely frequent CSS values. Adapt the reference to the product's content, interaction model, brand, and accessibility needs.
- Preserve existing brand and product constraints unless the user explicitly approves changing them.
- Treat accessibility as a baseline across every candidate: visible focus, sufficient contrast, non-color cues, usable targets, semantic controls, reflow/zoom, and reduced motion.
- Avoid generic AI decoration such as gratuitous gradients, glass effects, excessive pills, and oversized hero text unless the chosen reference and product rationale support them.
- Compose both widths, starting with the one the client's customers use, from the traits the references share — never by tracing one site section by section (a café told to stop looking boxy copied Naver Place's photo strip and pill buttons and heard "it looks just like my Naver page"). Small values (radius, shadow, body size) are not the look; composition is. Gate every first screen with `scripts/compose_metrics.mjs` against two to four running sites in the field (photo share, colour-panel share, empty share, largest type, strong block colours, text span) and do not show it while any line reads 「미달」. Then run a blind check: a fresh agent sees our screen shuffled with the real ones, logos covered, and must not pick ours as the AI-made one with high confidence. Four mockup projects that passed every lint check still looked like documents next to running sites at 1280 (4% photo and colour area against 23%, 63% empty first screen against 20%).
- Templates and block libraries alone do not fix this: free Tailwind block sets carry their own recognisable template look. Use them for parts (forms, footers), never as the composition.
- Build from the reference's screens and measured values, not from prose. For every page type, open the matching page on two or more shortlisted sites, run `scripts/extract_styles.mjs` on each at phone and desktop width, and take type sizes, shadows, spacing and the ratio of photos to boxes from the range they share. A stay site built from written rules came out with 3 photos, 11 rounded 12px boxes and shadows where Stayfolio had 56 photos, 6 boxes, 4px corners and no shadows, and the owner called it AI-looking and simple.
- Use proven UI rather than inventing components. Date-range calendars, bottom sheets, galleries, steppers, tabs and checkout forms come from a well-known design system or library (licence checked) or follow the pattern a leading site in the field uses, named in `DESIGN.md`; hand-rolled versions of these are where the generated look comes from.
- Run the AI-tell checks every time before showing: hallmark's `sloplint`, the impeccable detector, and the number comparison with the reference (`ui-review.md` § Site check). Report each as ran or why not.
- Match the reference's finish, not only its structure. Inventory its visual layers (identity, item faces, icons, colour blocks, data marks, imagery, depth, wide-screen columns) and keep, replace or consciously drop each one; a dislike replaces a layer's form, it does not delete the layer. A futsal site that kept FotMob's table and dropped its crests, chips and columns was judged "no design, too simple" next to running sites.
- Carry the brief's dislikes through every gate, not only the first. Before showing any comparison, check each candidate against the dislikes list and drop or fix what breaks it; a "no rainbow colours" said in the first message and ignored at the palette step was what disappointed the user most.
- Check each deliverable against the reason you gave for it. A photo slot recommended "so parents see the classroom at once" was filled with a keyboard close-up and the user caught it.
- Never present invented testimonials, customer logos, statistics, awards, or product screenshots as real. Use the user's material or a labelled empty slot.
- Do not copy protected logos, illustrations, text, or a distinctive composition verbatim.
- Establish the licence of every candidate and recommended dependency from its published licence text, not from memory. When the product will be operated commercially, a licence that forbids or charges for commercial use is a disqualifier, not a footnote — filter on it before taste, name what you verified, and flag what still needs legal review.
- The user may explicitly delegate a design choice. Treat that as authorization to select, but record the delegated decision and rationale rather than presenting it as the user's personal preference.
- Show every choice visually before asking about it: candidates in the full-screen viewer, palettes as a live switchable preview, per [references/comparison-board.md](references/comparison-board.md). Never ask the user to choose from a table of links, a folder of images, or one screenshot per candidate.
- Spend the session on the design, not on tooling. Use the bundled capture, viewer, confirm and check tools as they are; fix a tool only when it blocks the user, minimally, then return to the design work.
- Judge design quality at real size. Compare each page with the chosen reference at the same width and 1:1 scale before showing it; shrunken contact sheets are only for spotting breakage.
- Do not turn concept discovery into a long questionnaire or require design vocabulary. Translate abstract choices into visible product consequences and let the user answer with a candidate number, a reaction, or plain language.

## Companion skills

Open-source design skills — ui-ux-pro-max, hallmark, emilkowalski/skills, impeccable, Vercel's Web Interface Guidelines — do parts of this work better than this skill alone. Use them as they were designed rather than copying their rules in here; read [references/companion-skills.md](references/companion-skills.md) for where each fits. This skill keeps the conversation and the record of the user's choices (`DESIGN.md`/`SITE-PLAN.md`), and nothing is installed without the machine owner's approval. Screen wording is checked with the sister skill `ui-wording` (same repository, `/ui-wording`): terms matched to similar services and unified across every page.

## Durable outputs

Keep every project in one folder with this layout — `scripts/preflight.py` reads these names and says so when it finds none of them:

```
<project folder>/
  concept-brief.md      gate 1: the owner's words, photos and who/whose notes
  formats/              gate 2: captures, jobs*.json, skeleton tables (skeleton.mjs at 390 and 1280)
  DESIGN.md             gates 3–5: palette, type, tokens, shared traits as 「n/N곳」
  SITE-PLAN.md          gate 6: pages, flows, owner sign-in and lost phone
  layouts/              gate 7: numbered options
  mockups/              gate 8: clickable mockups; pictures sent to the client in mockups/보낼-그림/
  blind/                judge sheets
```

Depending on the active mode, produce only the necessary artifact:

- a compact concept brief plus a candidate viewer (captured pages at desktop and phone width);
- a live palette preview on the chosen format with semantic roles and computed contrast;
- isolated coded previews comparing finalist format/palette combinations;
- an approved-reference record;
- project-root `DESIGN.md` with tokens, rationale, provenance, decisions, and open questions;
- project-root `SITE-PLAN.md` with page inventory, flows, navigation, and per-page layout/mockup/code status;
- numbered layout options and full-fidelity mockups per page type, sharing one token and component stylesheet;
- shared token/component implementation and a representative UI proof, then the remaining pages;
- a rendered-UI review or site check with findings by tier and concrete corrections.

When product requirements conflict with the reference, explain the conflict and prioritize usability, accessibility, existing brand constraints, and the user's explicit decisions.
