# Rendered UI review

Review the rendered product, not code alone. Compare it with approved `DESIGN.md`, the concept brief, and actual content/interaction needs.

## Severity

1. **Blocking:** unusable interaction, broken hierarchy/task flow, inaccessible keyboard path, severe contrast/reflow issue, broken responsive layout, or missing critical state.
2. **System drift:** hard-coded repeated values, inconsistent variants, reference traits applied outside their approved scope, or typography/spacing/component behavior contradicting `DESIGN.md`.
3. **Polish:** alignment, rhythm, optical balance, wrapping/truncation, icon sizing, image treatment, and motion timing.

For each finding identify the screen/component, observed behavior, violated rule or user impact, evidence, and concrete correction. Mark subjective alternatives as decisions for the user rather than defects.

## Coverage

Stress points between widths, long labels and localization expansion, empty and dense data, every state the page claims, keyboard order and focus, 200% zoom, reduced motion, and one-off values that repeated components should share. Marketing pages and product UI should feel related without sharing one density.

## Site check

Use this before showing a set of mockups and before reporting a built site as done. On a later round, re-run only on the pages that changed.

**1. Static check.** Run `python scripts/check_site.py <dir>` from the skill directory against the mockup or build output (HTML and CSS). Each finding names its rule and line; page-level rules are described at the top of `page_rules.py`, `anchor_check.py` and `block_colours.py`.

- `FLOOR` — never ships; fix all of them. For `date-weekday`, compute weekdays from the date in the build script instead of typing them.
- `DRIFT` — values that bypass tokens, and a sample photo reused across pages. Fix, or keep with a one-line reason in `DESIGN.md` § Implementation mapping as an approved exception. Layout options (`today-1/2/3.html`) and judge copies (`-clean`) count as one page.
- `NOTE` — patterns that often signal generic output; review against `DESIGN.md` and keep when the approved concept calls for it. `one-colour-blocks`: keep the accent for the main button and status and let bands and panels go white with lines, rather than adding a second accent (`color-selection.md`). `unsourced-rule` and `unsourced-duration`: keep only what the user gave and delete the rest rather than marking it 견본. `anchor-label`: rename the link or give the section the heading the link promises.

The script reads markup and stylesheets only. It cannot see contrast on rendered colours, layout, or overflow; the next pass covers those.

**2. Render pass.** Capture the changed pages at ≈390 and ≈1280px (≈768 for work surfaces) with `scripts/capture.mjs`; a headless window resized below about 500px still lays out wider, so window-size screenshots of phone widths are not evidence. Fix every 「넘침」 capture prints (element and px). Check the longest label at the narrowest width, the first screen fitting the viewport, sticky regions, a visible focus ring on every control, and each state listed for the page in `SITE-PLAN.md`. Compute contrast for each text/background pair actually used from token values, not by eye. Without a renderer, say the check was structural only.

**2b. Skeleton pass.** Run `page-design.md` § Skeleton from the base step 6 at 390 and 1280. Also treat 「참고 한 곳과 거의 같은 뼈대」 (a site other than the base) as a finding; redraw, or record in `DESIGN.md` § 바탕에서 바꾼 곳 why this project departs.

**3. Fresh reviewer (only when the user asks; it costs a session's worth of tokens).** Give it the screenshots, `DESIGN.md`, and `SITE-PLAN.md` only — not your reasoning — and ask where the site breaks its own rules, where pages disagree, and what looks unfinished. Verify each finding against the current files before acting on it. Otherwise state that this pass was skipped.

**4. Companion checks.** Run hallmark's `sloplint`, the impeccable detector and the Web Interface Guidelines review described in `companion-skills.md` whenever they were installed or approved at the start-of-project check; they are not optional once agreed. Map their findings to the tiers above and report each as ran, skipped (with the reason agreed with the user), or failed.

**4b. Wording.** Run `ui-wording` over the pages and show the user its term table before applying it.

**5. Reference critique.** Open each page beside the base at the same width at 1:1 with `scripts/side_by_side.py`, and fill in its layer table (identity, item faces, icons, colour blocks, data marks, imagery, depth, wide-screen columns, type contrast). More than two layers missing without a recorded replacement means the set is not ready, however clean it is. Name where the page is flatter, denser, more generic or less finished than the reference — image scale, white space, type contrast, component detail, copy — and fix those before calling the set ready.

**5b. Numbers against the reference.** Compare `scripts/extract_styles.mjs` on our first screen and densest page with the base's numbers from `page-design.md` § Measure the reference pages: corner radius, shadows, number of boxes, number of photos, type sizes, button size. The generated look has larger radii, more shadows, more boxes and fewer photos than the reference, every section in the same container. Bring each number to the reference's range or record why not.

**6. Trade test.** For every page type, including forms, confirmations and admin screens, cover the name and logo. If it could belong to a different trade, strengthen the element only this business has (`design-selection.md` § 1) or change the composition. Carry the signature (photo band, heading face, signature figures) into the plain screens too.

Report the result as counts per tier plus the findings that remain, each with the page, the evidence, and the fix or the recorded reason for keeping it. Do not call the site done while a `FLOOR` finding remains.

## Correction protocol

Fixes require user authorization when the request was review-only. When fixing, update the highest reusable layer first: `DESIGN.md` decision → semantic token → shared component → page exception. If a finding exposes a concept-level conflict, stop broad propagation and return the decision to the user.
