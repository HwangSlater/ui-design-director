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

Use this before showing a set of mockups and before reporting a built site as done. It adds three passes to the review above.

**1. Static check.** Run `python scripts/check_site.py <dir>` from the skill directory against the mockup or build output (HTML and CSS). Findings carry a tier:

- `FLOOR` — never ships: missing `lang`, viewport, image `alt`, form labels, accessible names on icon-only controls, duplicate IDs, focus outlines removed with no `:focus-visible` replacement, motion with no reduced-motion alternative. Fix all of them.
- `DRIFT` — values that bypass tokens: raw colours or font sizes outside the token file, `!important`, `transition: all`. Fix, or keep with a one-line reason recorded in `DESIGN.md` § Implementation mapping as an approved exception.
- `NOTE` — patterns that often signal generic output (gradient text, more than two font families). Review against `DESIGN.md`; keep when the approved concept calls for it.

The script reads markup and stylesheets only. It cannot see contrast on rendered colours, layout, or overflow; the next pass covers those.

**2. Render pass.** Open every page at ≈375, ≈768, and ≈1280px and capture screenshots with `scripts/capture.mjs`; a headless window resized below about 500px still lays out wider, so window-size screenshots of phone widths are not evidence. Check horizontal overflow, the longest label at the narrowest width, the hero or first screen fitting the viewport, sticky regions, keyboard order with a visible focus ring on every control, 200% zoom, and each state listed for the page in `SITE-PLAN.md`. Compute contrast for each text/background pair actually used from token values, not by eye.

**3. Fresh reviewer.** When a subagent is available, give it the screenshots, `DESIGN.md`, and `SITE-PLAN.md` only — not your reasoning — and ask it to find where the site breaks its own rules, where pages disagree with each other, and what looks unfinished. Verify each finding against the current files before acting on it. Without a subagent, state that this pass was skipped.

**4. Companion checks.** When available and approved, run the impeccable detector and the Web Interface Guidelines review described in `companion-skills.md`, map their findings to the tiers above, and report each as ran, skipped, or failed.

Report the result as counts per tier plus the findings that remain, each with the page, the evidence, and the fix or the recorded reason for keeping it. Do not call the site done while a `FLOOR` finding remains.

## Correction protocol

Fixes require user authorization when the request was review-only. When fixing, update the highest reusable layer first: `DESIGN.md` decision → semantic token → shared component → page exception. If a finding exposes a concept-level conflict, stop broad propagation and return the decision to the user.
