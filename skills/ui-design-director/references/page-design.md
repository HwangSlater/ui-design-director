# Designing every page

Use this after `SITE-PLAN.md` is approved. Each page type passes two decisions before any production code: a **layout** choice from low-fidelity options, then a **mockup** approval at full fidelity. Work core page types first, then secondary ones. Keep `SITE-PLAN.md` status columns current as each decision lands.

## 1. Layout options (low fidelity)

For each page type, produce 2–3 numbered layout options that differ in **structure**, not styling: what leads, how content is ordered, how the primary action is reached, how the page reflows on a phone.

- Render them in greyscale with `DESIGN.md` spacing and type scale only — no palette, imagery, or decoration — so the user judges structure rather than colour.
- Use the real or planned content from `SITE-PLAN.md` at real length.
- Capture each option at one wide and one real phone width (`scripts/capture.mjs`) and show the options in the viewer from `comparison-board.md`.
- Under each option state in one line what it prioritises and what it gives up.

Derive options from the page's job and content. Do not pick a fashionable shape and fill it. When hallmark is installed, its named landing-page shapes can label read-surface options so they are clearly distinct (`companion-skills.md`); name the shape after deriving it, not before. Useful questions per surface:

- **Read surface:** What must the visitor believe before acting, and what proves it? Does the proof lead (product capture, figure, quote) or does the claim lead? Where does the primary action repeat? How long can the page be before the action is lost?
- **Work surface:** What does the user look at most often, and what do they change most often? Is the layout list → detail, master–detail split, canvas with panels, or stepwise? What stays fixed when content scrolls? What happens at 0, 1, and 1,000 items?

Recommend one option with the reason tied to the job, then let the user choose by number, combine by named part ("2's header with 1's list"), or reject. Mark the page type's `Layout` column `approved` only on the user's choice or explicit delegation.

When many page types share a frame (navigation, footer, sidebar, page header), settle that shared frame first on the most important page type and reuse it; do not re-offer it on every page.

## 2. Mockups (full fidelity)

Once a layout is approved, build the page as a full-fidelity mockup using only `DESIGN.md` tokens and components.

### Where mockups live

Keep mockups outside production routes, in one directory the user can open directly (default `mockups/` at the project root unless the user names another place), with an `index.html` that links every page and state. Build them as static HTML/CSS that load one shared `tokens.css` and one `components.css`; pages contain layout only. This makes the later code step a transfer of approved parts rather than a rewrite, and lets one token change restyle every mockup.

If the project already has a component library or framework that runs locally, build mockups with it on a non-production route instead, so the approved mockup is already close to code.

### What a mockup must show

- every section or region at real content length, including the longest realistic title, name, and label;
- the page at narrow (≈375px), medium (≈768px), and wide (≈1280px+) widths;
- for work surfaces, each required state from `SITE-PLAN.md` as its own labelled frame: empty, loading, error, no-permission, dense data;
- interactive components in default, hover, keyboard focus, active, disabled, and error/invalid states where they appear;
- only the motion `DESIGN.md` approved, built and checked against emilkowalski/skills when installed (`companion-skills.md`);
- real imagery only when it is supplied or its licence is verified; otherwise a labelled empty frame of the correct aspect ratio. Do not use generated or stock imagery as if it were the product.

### Self-check before showing

Run `scripts/check_site.py` on the mockup directory and fix every `FLOOR` finding. Then render the pages and check the places mockups break: overflow at the narrow width, the longest label, sticky or scrolling regions, and the states you claimed. Screenshot each page at the three widths. If no renderer is available, say the check was structural only.

Show the mockups in the viewer first, then a short list of what to look at. Ask for approval per page type, or for specific changes. Classify feedback with `design-md-format.md` § Feedback protocol: a change that should apply everywhere goes into `DESIGN.md` and `tokens.css`/`components.css`, not into one page.

## 3. Consistency across pages

After the core page types are approved, render them side by side and check that they read as one site: same navigation and footer, same heading scale for the same level, same spacing rhythm, same button hierarchy, same treatment of empty and error states. Fix drift at the shared layer.

A new component that appears on only one page is allowed; record it in `DESIGN.md` § Components when it is approved so the next page reuses it instead of inventing a variant.

## 4. Mockup approval gate

The site's mockups are approved when every core page type has `Mockup: approved` in `SITE-PLAN.md`. Secondary page types may stay pending if the user wants to start code; list them as remaining work. Do not begin production code for a page whose mockup is not approved unless the user explicitly asks.
