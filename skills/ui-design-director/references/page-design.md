# Designing every page

Use this after `SITE-PLAN.md` is approved. Each page type passes two decisions before any production code: a **layout** choice from options that differ in structure, then a **mockup** approval at full fidelity. Work core page types first, then secondary ones. Keep `SITE-PLAN.md` status columns current as each decision lands.

## 1. Layout options

For each page type, produce 2–3 numbered layout options that differ in **structure**, not styling: what leads, how content is ordered, how the primary action is reached, how the page reflows on a phone.

- Render them with the approved `DESIGN.md` tokens — palette, fonts, spacing, components — and a licence-checked sample photo in every photo slot (see `comparison-board.md` § Sample photos). Keep colour, type and photos identical across options so only the structure differs. Users judged greyscale boxes as unable to show the real mood, and asked for photos always.
- Use the real or planned content from `SITE-PLAN.md` at real length.
- Capture each option at one wide and one real phone width (`scripts/capture.mjs`) and show the options in the viewer from `comparison-board.md`.
- Under each option state in one line what it prioritises and what it gives up.
- At least one option changes the **first screen** itself, not only the order of sections below it: full-width photo, type only, the timetable or price list first, a single strong object drawing. Three options that all open with text on the left and a photo on the right are one option.

Before drawing options, write down what makes the chosen reference good on this page type, from captures viewed at 1:1: image size relative to the screen, white space between sections, type hierarchy (how many sizes, how much contrast between them), density, and its signature components. Every option keeps those traits; options differ in structure, not in quality.

Derive options from the page's job and content. Do not pick a fashionable shape and fill it. When hallmark is installed, its named landing-page shapes can label read-surface options so they are clearly distinct (`companion-skills.md`); name the shape after deriving it, not before. Useful questions per surface:

- **Read surface:** What must the visitor believe before acting, and what proves it? Does the proof lead (product capture, figure, quote) or does the claim lead? Where does the primary action repeat? How long can the page be before the action is lost?
- **Work surface:** What does the user look at most often, and what do they change most often? Is the layout list → detail, master–detail split, canvas with panels, or stepwise? What stays fixed when content scrolls? What happens at 0, 1, and 1,000 items?

Set times and prices in the body face with tabular figures; a monospace face for `14:00 ~ 19:00` read as generated to the user. Recommend one option with the reason tied to the job, then let the user choose by number, combine by named part ("2's header with 1's list"), or reject. Mark the page type's `Layout` column `approved` only on the user's choice or explicit delegation.

When many page types share a frame (navigation, footer, sidebar, page header), settle that shared frame first on the most important page type and reuse it; do not re-offer it on every page.

## 2. Mockups (full fidelity)

Once a layout is approved, build the page as a full-fidelity mockup using only `DESIGN.md` tokens and components.

### Where mockups live

Keep mockups outside production routes, in one directory the user can open directly (default `mockups/` at the project root unless the user names another place), with an `index.html` that links every page and state. Build them as static HTML/CSS that load one shared `tokens.css` and one `components.css`; pages contain layout only. This makes the later code step a transfer of approved parts rather than a rewrite, and lets one token change restyle every mockup.

If the project already has a component library or framework that runs locally, build mockups with it on a non-production route instead, so the approved mockup is already close to code.

### What a mockup must show

- every section or region at real content length, including the longest realistic title, name, and label;
- each piece of information once per screen: a hero visual that repeats the table below it ("why does the timetable appear twice?") is decoration pretending to be content;
- one consistent moment in time. When a sample screen is set on a day ("today = 27 October"), every number on it must be true as of that day: a pre-match card next to standings taken after that match showed eight games played when only seven had been, and the client caught it. Pick the day the supplied data describes (the day after the round it covers) and fill only what lies after it as samples;
- sample data that agrees with itself. Totals must add up (a 4 : 1 score lists four goals), the same team or roster has the same members on every page, and one snapshot date governs every count (places left, confirmed, waiting). Never give a real name the user supplied a role they did not state: the client's top scorers turned into invented team captains read as fact. Write counts with their unit (「이준석 2골」, not 「이준석 2」) or readers count names. A fresh reviewer given only the screenshots and the plan caught most of these;
- only facts the user gave. Anything you had to fill in — directions, walking times, opening days, policies, prices, staff names — is marked on the page as unconfirmed (for example a small "확인 필요" tag) and listed when you hand the mockup over. Plausible guesses read as facts: a client found an invented subway exit, walking time and closing day only because they happened to read every line;
- the page at narrow (≈375px), medium (≈768px), and wide (≈1280px+) widths;
- for work surfaces, each required state from `SITE-PLAN.md` as its own labelled frame: empty, loading, error, no-permission, dense data;
- interactive components in default, hover, keyboard focus, active, disabled, and error/invalid states where they appear;
- only the motion `DESIGN.md` approved, built and checked against emilkowalski/skills when installed (`companion-skills.md`);
- real imagery when supplied; otherwise licence-checked sample photos of the right subject and aspect ratio, credited and labelled on the page as samples to be replaced, with a hatched frame as the offline fallback. Do not use generated imagery, and do not present sample photos as the product.

### Self-check before showing

First hold every name, number and date on the page against the brief: list each one as **given** (the user said it), **derived** (computed from what they gave — a weekday, a deadline three days later, standings maths) or **invented**. Invented items that a reader could take as real — people's names, scores, prices, dates, counts — get a 「견본」 mark; filler that cannot be mistaken (an empty-state line, a placeholder in an input) does not. Mark at the smallest unit that carries the risk and at most once per block: a client stopped reading marks that appeared four times a screen, and still had to catch an invented player name, a captain's role given to a real scorer, a score whose scorers did not add up and a word left from another project — each one a check against this list would have caught.

Run `scripts/check_site.py` on the mockup directory and fix every `FLOOR` finding. Run the companion checks agreed at the start (impeccable detector, Web Interface Guidelines) and fix what they confirm. Then put each page next to the reference at the same width at 1:1 and name at least three places where the mockup is flatter, denser, more generic or less finished than the reference; fix them before showing. Anything you notice in your own screenshots is fixed before the user sees it, however small — a label that wraps one word onto its own line was spotted in review, sent anyway, and was the first thing the user pointed out. Then render the pages and check the places mockups break: overflow at the narrow width, the longest label, sticky or scrolling regions, and the states you claimed. Screenshot each page at the three widths. If no renderer is available, say the check was structural only.

Hand the mockups over as a **clickable prototype**, not as screenshots: link the pages so the main flows can be clicked through (logo, navigation, card → detail → add to cart → cart → checkout → order complete, account links), and give every page a small collapsed "상태" switcher on the edge of the screen that jumps between that page's states (empty, invalid, failure, notice/confirm, busy). Keep the switcher clear of toasts, fixed bars, dialogs and content at every width you hand over. For a read-only site handed to an owner who is not a developer (a local shop or school), leave the switcher out: describe the fallback states in one plain sentence ("인터넷이 느리면 사진 대신 빈칸이 보여요") and keep only prototype notices that answer a real question, such as what a not-yet-connected button will do; an owner found a 「시안 상태」 tab meaningless and it covered a caption at tablet width. Prototype-only script and styles stay in separate files that never move into production code. Click the flows through in a real browser at phone and desktop width before handing over, then give the full path of the entry page and a short list of what to look at. Users found a screenshot viewer tedious once there were many pages and states. Use the screenshot viewer (`comparison-board.md`) for choosing between layout options, where side-by-side comparison matters. Ask for approval per page type, or for specific changes. Classify feedback with `design-md-format.md` § Feedback protocol: a change that should apply everywhere goes into `DESIGN.md` and `tokens.css`/`components.css`, not into one page.

## 3. Consistency across pages

After the core page types are approved, render them side by side and check that they read as one site: same navigation and footer, same heading scale for the same level, same spacing rhythm, same button hierarchy, same treatment of empty and error states. Fix drift at the shared layer.

A new component that appears on only one page is allowed; record it in `DESIGN.md` § Components when it is approved so the next page reuses it instead of inventing a variant.

## 4. Mockup approval gate

The site's mockups are approved when every core page type has `Mockup: approved` in `SITE-PLAN.md`. Secondary page types may stay pending if the user wants to start code; list them as remaining work. Do not begin production code for a page whose mockup is not approved unless the user explicitly asks.
