---
name: ui-design-director
description: Guides a client from an overall UI concept to a finished website or web app design, one decision at a time — puts well-known real sites of the client's field side by side in a shared viewer so the client picks one as the base, then palette and fonts, then rebuilds the base's structure and finish as the client's own page (main page only, or the whole site with DESIGN.md and SITE-PLAN.md), and checks it against the base. Use when someone wants to choose or set a design, design or redesign a site, home page or app, or extract a design system — also when asked in Korean, e.g. 홈페이지 디자인, 메인 페이지 시안, 사이트 디자인 골라 줘, 디자인 시안 만들어 줘. Not for isolated styling fixes.
allowed-tools: Bash(python *scripts/stage.py*)
---

# UI Design Director

The client makes each visual decision; you bring real reference sites, side-by-side comparisons and a recommendation, then rebuild the chosen base as the client's own page. Terms: **client** — the person commissioning the design; **base** — the one site or template the client picked; **owner screen** — the site's own admin pages; **machine owner** — whoever approves installs on this computer.

**Needs:** Node 18+, Python 3.10+ with Pillow, Edge or Chrome. `${CLAUDE_SKILL_DIR}` is this skill's folder (outside Claude Code: the folder holding this file). **Run the bundled scripts; never read them** — only their output enters the conversation. Print summary lines only (`| tail -5`). When a hook blocks you, run the command it names.

## Where you are

!`python "${CLAUDE_SKILL_DIR}/scripts/stage.py" .`

If the line above still shows a command (another tool, or the table was not filled in), run it in the project folder. Run it again after every client decision.

## Workflow — follow in order, never skip

Copy this checklist into your reply when you start and tick it as you go. Before you build a step's screen, `python ${CLAUDE_SKILL_DIR}/scripts/stage.py <project> --require <step>` MUST exit 0; if it fails, finish the step it names first. Every client-facing screen comes from the bundled templates — never a viewer, palette page or sheet of your own.

```
- [ ] brief     concept-brief.md: main job, customers, dislikes, 「사진이 있으세요?」 (yes/no; if no, sample_photos.py
                and letter marks — sample-photos.md), one question at a time; 「사이트 꼴: 여러 쪽」 or
                「사이트 꼴: 한 쪽 홍보·모집」 inferred and read back (guided-conversation.md § Site type);
                companion-skills.md § Start-of-project check, once, with the machine owner
- [ ] board     candidates by design-selection.md §§ 2–3 → formats/board-spec.json →
                node ${CLAUDE_SKILL_DIR}/scripts/live_proxy.mjs formats/board-spec.json   (background)
                if it warns about a broken candidate, replace that candidate before giving the address;
                give the client its one OPEN address; 확정 arrives as a DECISION line + formats/decision.json
- [ ] material  python ${CLAUDE_SKILL_DIR}/scripts/base_material.py . <base url>
                run the snapshot/motion/capture/extract_styles commands it prints; fill formats/바탕-구성.md
- [ ] palette   palette/index.html on the palette-switcher template (comparison-board.md § Palettes and fonts); fonts from
                python ${CLAUDE_SKILL_DIR}/scripts/fonts.py pick --style <…> (fonts.md); colours keep the base's relationships
                in our own hues — never a 「바탕 그대로」 candidate (color-selection.md); wait_choice.mjs for 확정
- [ ] design    node ${CLAUDE_SKILL_DIR}/scripts/skeleton.mjs … --base <base> (page-design.md § Skeleton from the base)
                → 「바꿀 곳 n/N」; DESIGN.md (design-md-format.md, § 바탕에서 바꾼 곳 and § 부품 출처)
- [ ] main      before each part: knowledge.py ask --part <part> (you and each mockup subagent; Korean names work)
                mockups/ by build-rules.md → compose_metrics.mjs → side_by_side.py → plain-model test (once)
                → preflight.py (includes check_site) after the LAST edit → send; never send an edit without it
```

A chat answer instead of 확정: `python ${CLAUDE_SKILL_DIR}/scripts/stage.py <project> --decide <step> "<choice>"`. Whole site: after **design**, follow [site-plan.md](references/site-plan.md) § Gates (whole site) 6–10.

## Budget

Most clients are on a Pro-level plan: main page in under 80 turns, approved mockups for a whole site in under 250. Every turn re-reads the whole conversation, so cost is turns × conversation length.
- **Subagents: one per mockup page, plus three named exceptions** — the plain-model test (once), the fresh reviewer (`ui-review.md` § Site check 3, only when asked) and the blind judge (`blind-judge.md`, only when asked). Nowhere else. A subagent does not see this skill. Brief a mockup subagent with file paths only: `${CLAUDE_SKILL_DIR}/references/build-rules.md` (read first) and the `knowledge.py ask --part <part>` command for each part it builds, the page's `SITE-PLAN.md` row or the main-page brief, `DESIGN.md`, `tokens.css`/`components.css`, the base material in `formats/` (snapshot, 2× section captures, `바탕-구성.md`, `바탕-움직임.md`) and the client's open requests. If the base lacks that page or it is behind a login, use the closest field site that shows it publicly and say which. Never describe a reference page in words instead. It returns at most ten lines plus picture paths; at most 30 turns.
- **Few rounds.** About 5 reference sites; 2 home layout options for a whole site (main page only: none); at most two rounds of fixes per step before asking the client.
- **Each picture once, small.** In the main conversation open only the pictures you send, once each; to check a fix, crop the changed part to about 1200px. One `capture.mjs` jobs file per round, only for the pages and widths that changed.
- **Change lines, not files.** Fix with `Edit` on the changed lines; no long inline Python or `sed` that rewrites files; read several files in one command.

## Before each message with a picture or page

Run `python ${CLAUDE_SKILL_DIR}/scripts/preflight.py <project>` and fix or answer every line it prints. Then check these, which a script cannot see, and say which you checked:

1. **Photos — who and whose.** List the people, signs, price cards, screens and number plates in every photo; ask whose they are; crop rather than blur. Caption each photo by what it shows.
2. **Say only what you send.** Describe a reference only from the frames you attach; count shared traits as 「n/N곳」, never 「all」.
3. **Built by the rules.** Every page follows `references/build-rules.md`.
4. **Phone and desktop both**, starting with the width the client's customers use first.
5. **Owner screens forgive.** Confirm before a change others see, a large undo after; say who to contact for what the owner screen cannot do and what to do if the phone is lost.
6. **Dislikes and reasons hold** at every step, and each deliverable matches the reason you gave for it.
7. **Look at it** at the size the client will see it; check that fonts actually differ between font options.

**Quality bar.** A design professional shown our page shuffled with running sites of the field should not pick ours out as AI-made. Before the client sees a first screen, in this order: composition numbers against two to four running sites (`compose_metrics.mjs`, `blind-judge.md` § Composition numbers; never show while a line reads 「미달」; if you change the comparison sites after a 미달, tell the client which and why), a 1:1 side-by-side with the base (`side_by_side.py`), and once a **plain-model test** — one subagent builds the same first screen from the client's words only, with no skill; if ours differs only in colour or the plain one shows more of the product's own character, rework ours. A blind judge runs once, only when the client asks.

## Conversation

Lead: one consequential question at a time, numbered choices shown as pictures, plain words instead of design vocabulary, the next step always obvious ([references/guided-conversation.md](references/guided-conversation.md)). **Candidates are live sites in the shared viewer**, never captures or a viewer of your own ([references/comparison-board.md](references/comparison-board.md)). A site that refuses a frame: first its proxy view in the same board; 「실제 창으로」 (the real site in a sized window of the client's browser) to judge motion and feel; a snapshot only for exact material. Captures (2×) only for login-walled pages or a client who can only look at images. If the client delegates a choice, make it and record that it was delegated.

**Every line the client sees is Korean** — questions, answers and progress notes alike, including the one-line progress notes between tool calls (「바탕 재는 중이에요」, never 「Capturing the base…」).

## Route the request

On entry, the stage table above shows the first open step; resume there and do not redo approved decisions. Advance only as far as the client authorised: "find a design" is not approval to implement, "design the site" is not approval to write production code.

- **Main page only:** the workflow above, ending at **main**.
- **Concept** (format or palette undecided): [design-selection.md](references/design-selection.md), [color-selection.md](references/color-selection.md), [fonts.md](references/fonts.md).
- **Preview** (finalists exist, client wants them applied): [concept-preview.md](references/concept-preview.md).
- **Extract** (format and palette approved): [reference-extraction.md](references/reference-extraction.md), [design-md-format.md](references/design-md-format.md) → `DESIGN.md`.
- **Site plan** (`DESIGN.md` exists, whole site wanted): [site-plan.md](references/site-plan.md) → `SITE-PLAN.md`.
- **Pages** (`SITE-PLAN.md` approved): [build-rules.md](references/build-rules.md), [page-design.md](references/page-design.md), [mockup-content.md](references/mockup-content.md), [owner-screens.md](references/owner-screens.md).
- **Build** (mockups approved, production code requested): [site-build.md](references/site-build.md).
- **Apply** (restyle an existing product from an approved `DESIGN.md`): map it to shared tokens; one representative slice before spreading it.
- **Review** (consistency check, or work about to be shown as finished): [ui-review.md](references/ui-review.md) § Site check.
- **Design knowledge** (any step, when a decision needs a reason): `python ${CLAUDE_SKILL_DIR}/scripts/knowledge.py ask --part <part>` — 700+ sourced rules from practising designers; the stage table already lists the few that matter for the next step ([design-knowledge.md](references/design-knowledge.md)). Never read the long knowledge files.

## Always

- Verify every candidate before presenting it: state prices, licences, coverage and responsiveness only from what you inspected; never invent or imply inspection.
- Licences from the published text. For commercial use, a licence that forbids or charges for it disqualifies the candidate.
- Use proven UI for date pickers, bottom sheets, galleries, steppers, tabs and checkout forms — a known design system or the pattern a leading site uses, named in `DESIGN.md`.
- Before showing, run the AI-tell checks when installed (hallmark `sloplint`, the impeccable detector) and always `ui-review.md` § Site check; report each as ran or why not.
- Accessibility is a baseline: visible focus, contrast, non-colour cues, 44px targets, semantic controls, reflow and zoom, reduced motion.
- Keep existing brand constraints unless the client approves changing them.
- Snapshots and captures of other sites are copies of other people's work: keep them in the project folder's `formats/`, never commit them, and delete them once the mockup is approved.
- Spend the session on the design, not on tooling: use the bundled tools as they are; fix one only when it blocks the client.
- **Companion skills** (ui-ux-pro-max, hallmark, emilkowalski/skills, impeccable, Vercel's Web Interface Guidelines) do parts of this work better; use them as designed, per [companion-skills.md](references/companion-skills.md). Install nothing without the machine owner's approval. Screen wording goes through the sister skill `ui-wording`.

## Project folder

`stage.py` and `preflight.py` read these names:

```
<project folder>/
  concept-brief.md      brief: the client's words, photos and who/whose notes
  decisions.json        decisions given in chat (stage.py --decide)
  formats/              board: board-spec.json, decision.json; material: jobs-base.json, snapshot/, base-cap/,
                        바탕-구성.md, 바탕-움직임.md (snapshot/ and base-cap/ never committed)
  palette/              palette-switcher page, decision.json
  DESIGN.md             base, palette, type, tokens, 바탕에서 바꾼 곳 (n/N), 부품 출처
  SITE-PLAN.md          whole site: pages, flows, owner sign-in and lost phone
  layouts/              whole site: numbered options
  mockups/              clickable mockups; pictures sent to the client in mockups/보낼-그림/
  blind/                judge sheets
```
