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

Use this before showing a set of mockups and before reporting a built site as done. It adds six passes to the review above.

**1. Static check.** Run `python scripts/check_site.py <dir>` from the skill directory against the mockup or build output (HTML and CSS). Findings carry a tier:

- `FLOOR` — never ships: missing `lang`, viewport, image `alt`, form labels, accessible names on icon-only controls, duplicate IDs, in-page links (`href="#…"`) whose target is missing or has no visible heading, focus outlines removed with no `:focus-visible` replacement, motion with no reduced-motion alternative. Fix all of them.
- `DRIFT` — values that bypass tokens: raw colours or font sizes outside the token file, `!important`, `transition: all`. Fix, or keep with a one-line reason recorded in `DESIGN.md` § Implementation mapping as an approved exception.
- `NOTE` — patterns that often signal generic output (gradient text, more than two font families), and an in-page link whose words share nothing with the heading it lands on (「수업 시간 보기」 landing on 「초등학생」 — the reader clicked one name and got another; rename the link or give the section the heading the link promises). Review against `DESIGN.md`; keep when the approved concept calls for it.

The script reads markup and stylesheets only. It cannot see contrast on rendered colours, layout, or overflow; the next pass covers those.

**2. Render pass.** Open every page at ≈375, ≈768, and ≈1280px and capture screenshots with `scripts/capture.mjs`; a headless window resized below about 500px still lays out wider, so window-size screenshots of phone widths are not evidence. Check horizontal overflow, the longest label at the narrowest width, the hero or first screen fitting the viewport, sticky regions, keyboard order with a visible focus ring on every control, 200% zoom, and each state listed for the page in `SITE-PLAN.md`. Compute contrast for each text/background pair actually used from token values, not by eye.

**3. Fresh reviewer.** When a subagent is available, give it the screenshots, `DESIGN.md`, and `SITE-PLAN.md` only — not your reasoning — and ask it to find where the site breaks its own rules, where pages disagree with each other, and what looks unfinished. Verify each finding against the current files before acting on it. Without a subagent, state that this pass was skipped.

**4. Companion checks.** Run hallmark's `sloplint`, the impeccable detector and the Web Interface Guidelines review described in `companion-skills.md` whenever they were installed or approved at the start-of-project check; they are not optional extras once agreed. Map their findings to the tiers above and report each as ran, skipped (with the reason agreed with the user), or failed.

**4b. Wording.** Run the `ui-wording` skill (bundled in this repository) over the pages: one name per thing, the words similar services already use, one tone, one button form. Show the user its term table before applying it.

**5. Reference critique.** Open each page beside the primary reference at the same width at 1:1. Name where the page is flatter, denser, more generic or less finished than the reference — image scale, white space, type contrast, component detail, copy — and fix those before calling the set ready. Passing passes 1–4 only proves nothing is broken; this pass is about whether it is good.

**6. Trade test.** Do this for every page type, not only the first screen; forms, confirmations and admin screens are where sites fall back to the generic booking-app look (white rounded cards, one filled button). Cover the name and logo on each. If it could belong to a different trade — a pottery studio's page passing for a piano school's — strengthen the element only this business has (`design-selection.md` § 1) or change the composition before showing it. Carry the signature into the plain screens too: the league's scoreboard figures belonged on the sign-up page's seats-left number as well, and the client noticed they were missing.

Report the result as counts per tier plus the findings that remain, each with the page, the evidence, and the fix or the recorded reason for keeping it. Do not call the site done while a `FLOOR` finding remains.

## Correction protocol

Fixes require user authorization when the request was review-only. When fixing, update the highest reusable layer first: `DESIGN.md` decision → semantic token → shared component → page exception. If a finding exposes a concept-level conflict, stop broad propagation and return the decision to the user.
