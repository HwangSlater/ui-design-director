# Building the site from approved mockups

The job is transfer, not redesign: approved structure, tokens, and components move into the codebase intact. Any visual change discovered during build returns to the mockup or `DESIGN.md` first.

## 1. Choose the target

- **Existing project:** build in its framework, styling approach, and component conventions. Map `DESIGN.md` tokens onto the existing token or theme file; do not create a parallel one.
- **No project yet:** default to plain static HTML/CSS with the mockups' `tokens.css` and `components.css`. Propose a framework only when the site needs one (accounts, server data, many pages from data, client-side state), state why, and get approval before adding it.

Record the target in `SITE-PLAN.md` front matter (`build_target`).

## 2. Order of work

1. **Tokens:** semantic tokens from `DESIGN.md` into the project's token layer. Nothing below may use a raw colour, font size, spacing, radius, shadow, or duration value that is not a token.
2. **Shared components:** buttons, inputs, navigation, footer, cards, tables, dialogs, feedback — each with all states the mockups showed.
3. **Shared frame:** page shell, navigation, footer or sidebar, page header.
4. **One representative page**, end to end, at all widths and states. Show it and get confirmation that code matches the mockup before propagating.
5. **Remaining pages** by priority, reusing components. Mark each page's `Code` column `done` as it lands, so an interrupted build resumes from the next pending page.

When a page needs something no component covers, add it to the shared layer and to `DESIGN.md` § Components; do not style it inline on the page.

## 3. What production code must add beyond the mockup

- Semantic structure, unique `title` and description per page, Open Graph image and title for shareable pages, favicon, `aria-current` on the current page, a skip link, external links identified.
- **Forms:** real validation messages tied to fields, a submitting state, a success state, and a failure message that tells the user what to do. A form that shows success without sending anything is a defect.
- **Images:** explicit width and height or aspect ratio, modern formats, lazy loading below the first screen; no layout shift when fonts or images load (`font-display`, reserved space); no animation library for effects CSS can do.
- **Motion:** only what `DESIGN.md` defines, reduced under `prefers-reduced-motion`.

Do not add analytics, tracking, third-party embeds, or external font/CDN requests the user has not approved; each one is a privacy and performance decision.

## 4. Content in code

Use the approved copy. Sample content from the mockups stays visibly marked as sample (or in a clearly named data file) until the user supplies the real text. Follow `DESIGN.md` § Voice and terminology for every label, message, and button.

## 5. Finishing the build

Run `ui-review.md` § Site check across every page before reporting the site as done. Report what was built, which pages remain pending, which sample content still needs replacing, and how to run or open the site.
