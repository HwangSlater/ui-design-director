---
name: ui-design-director
description: Guide users conversationally from an overall UI concept to a complete website or web app design — researching live templates and 3–4 color palettes, comparing coded previews, recording approved choices in DESIGN.md, planning every page in SITE-PLAN.md, approving layouts and full-fidelity mockups page by page, then building and checking the site. Use when a user wants to choose a design, design or build a whole site or app, redesign, extract a design system, or set project-wide UI direction; do not trigger for isolated styling fixes.
---

# UI Design Director

Turn subjective taste into an explicit, user-approved design language, then carry that language through every page of the site. The user owns each visual decision; provide strong research, comparisons, and a recommendation so that choice is informed rather than arbitrary.

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

1. **Context gate:** Establish a compact concept brief from repository evidence and user input: product/job, audience, interaction archetype, essential screens, content density, brand traits, constraints, and anti-preferences. Name the archetype explicitly: marketing site, dashboard, editing tool, form workflow, or content reader. Ask only for missing information that would materially change the shortlist; label inferred items. In the same step run the companion check in [references/companion-skills.md](references/companion-skills.md) § Start-of-project check: tell the user in one short table which companions are installed, what each would add, and ask once whether to install the missing ones. Record the answer in the brief; a companion is never skipped silently.
2. **Format gate:** Present direct links to individual live template/showcase candidates. Let the user choose a primary structural/visual reference, reject candidates, and optionally select exact secondary traits.
3. **Palette gate:** Present linked 3–4 color palette candidates independently from the format. Explain intended UI roles and contrast risks. Let the user select, modify, or reject them; a palette's original swatches are inspiration, not yet complete semantic UI tokens.
4. **Preview gate:** Offer a coded comparison when visual judgment would benefit; create it when the user requests or accepts. Combine only finalists using identical content and component coverage. Preview code is disposable evidence, not approval or production implementation.
5. **Rules gate:** Extract and adapt the approved format and palette into `DESIGN.md`. Separate observed evidence, product-specific decisions, and unknowns. Ask for approval of unresolved high-impact choices; minor safe defaults may remain clearly marked as provisional.
6. **Site plan gate:** For a whole-site request, get the page inventory and main flows in `SITE-PLAN.md` approved before designing pages. Classify each page as a read surface or a work surface; they follow different rules.
7. **Layout gate:** For each page type, show 2–3 numbered layout options that differ only in structure, drawn in the approved colours and fonts with sample photos, and let the user choose. Settle the shared frame (navigation, footer, sidebar) once.
8. **Mockup gate:** Build full-fidelity mockups of each page type from `DESIGN.md` tokens and components, at three widths and in every required state, pass the § Site check — including the companion checks and the reference critique at full size — and get per-page approval. Hand them over as a clickable prototype.
9. **Proof gate:** When production implementation is requested, build or adapt one representative page/slice and show it at relevant viewport sizes and states. Propagate only after approval when the scope is broad.
10. **System gate:** Move every approved reusable feedback item into `DESIGN.md` and the shared token/component layer. Chat instructions and page-local CSS are not durable design decisions.

## Non-negotiable behavior

- Verify every candidate before presenting it: open the link, and state prices, licences, page coverage, and responsiveness only from what you actually inspected. If something is inaccessible, unverifiable, or live research is unavailable, say so and ask for user-provided references — never fabricate a candidate or imply you inspected one.
- Keep format, palette, and typography identifiable as separate choices. Do not let a template's default colors silently decide the user's palette.
- Do not mark the concept approved until format, palette, any high-impact adaptation, and requested preview feedback are resolved. Approval of one axis does not imply approval of another.
- Prefer one coherent primary reference. Borrow from secondary references only by named trait; do not create a collage of unrelated trends.
- Extract relationships and intent—not merely frequent CSS values. Adapt the reference to the product's content, interaction model, brand, and accessibility needs.
- Preserve existing brand and product constraints unless the user explicitly approves changing them.
- Treat accessibility as a baseline across every candidate: visible focus, sufficient contrast, non-color cues, usable targets, semantic controls, reflow/zoom, and reduced motion.
- Avoid generic AI decoration such as gratuitous gradients, glass effects, excessive pills, and oversized hero text unless the chosen reference and product rationale support them.
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
