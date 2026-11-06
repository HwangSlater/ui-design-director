# Rules for building a page

Read this file before building or changing any layout option or mockup page. The main conversation and every mockup subagent read the same file — a subagent does not see SKILL.md, so these rules travel by this path, never by memory.

## Contents
- Follow the base
- Make it ours, not a copy
- Colour, type and identity parts
- What reads as generated
- Content and samples
- Check before handing back

## Follow the base

The answer key is the base's own page; reproduce its design, then make it ours.
1. Work from the base material in `formats/`: the snapshot (`snapshot/…/index.html`, read it for exact structure, fonts and colours), the 2× section captures (open only the section you are building), `바탕-구성.md` (sections top to bottom with height share, photo share, type sizes, columns, job) and `바탕-움직임.md` (motion values).
2. Build section by section from `바탕-구성.md`: same order, proportions, density, photo share, type scale, spacing, radius and shadow. Do not invent a structure or rebuild from generic rules. A page built from written rules had 3 photos and 11 shadowed boxes where its reference had 56 photos, 6 boxes and no shadows.
3. Reproduce the motion in `바탕-움직임.md` with those durations and curves — hover changes, sticky header, reveal on scroll, auto-advancing slides. Add no motion the base does not have.
4. Change only what several field sites do differently (「바꿀 곳」 n/N in `DESIGN.md`). A part the base lacks comes from the field sites (n/N) or the client's own objects (menu board, sign, ticket), recorded in `DESIGN.md` § 부품 출처.
5. Desktop takes the base's desktop composition; a phone column centred in empty space is a finding.
6. Keep the base's finish, not only its structure: its visual layers (identity, item faces, icons, colour blocks, data marks, imagery, depth, wide-screen columns) are kept, replaced or knowingly dropped one by one; a dislike replaces a layer's form, it does not delete the layer.

## Make it ours, not a copy

- Our name, content, photos and the chosen colours. Character comes through photos and wording, not added boxes: a first screen the base keeps to photo and menu stays photo and menu.
- Nobody should say 「이거 ○○ 아냐?」 at first glance: no base logo, mascot, brand colour, set phrases or a component only the base has. Tell the client which recognisable parts you changed.
- A base part you keep keeps its look (drawing, lines, photo); if you cannot carry the look, drop it rather than leave a bare text version.
- At most one section from another shortlisted site, by name and for a stated reason. Never copy protected logos, illustrations or text.

## Colour, type and identity parts

- Colours: the base's combination of 4–6 tones and their relationships (from `DESIGN.md`), never a white page with one accent. Colour fields only where the base has them — no pale tinted bands between sections.
- Fonts: only the faces approved in `DESIGN.md`, chosen by [fonts.md](fonts.md) (`fonts.py pick`, never from memory). The faces in `assets/fonts/ai-fonts.json` are refused — `fonts.py check` and the plugin hook block them.
- Identity parts take the base's measured finish: the wordmark (typeface, size, weight, tracking, colour, placement — a designed name, never body text in a bar), the navigation, the buttons (fill or outline, border, height, padding, type). A default black pill or a plain text name is a finding.
- No more boxes than the base: count bordered or filled rectangles (cards, panels, tags, labels, button blocks, tinted bands) on both pages; ours may not have more. Text and photos sit on the page; labels are plain text.

## What reads as generated

Each of these was called out by the client: a white panel floating on the hero photo with label–value facts; letters or emoji in circles as icons; a small overline above the name; a row of identical icon tiles; dashed 「… 자리」 boxes; pale bands everywhere; one accent on white; the default fonts above; gratuitous gradients, glass, pills everywhere, oversized hero text unless the base has them.

## Content and samples

- Only facts the client gave; anything filled in is listed at handover. Where the client's words are missing (an intro, a price, an address) write short neutral sample text of the right length and list it in one 「견본」 line at the page foot — never a dashed slot on the page.
- Never invented testimonials, logos, statistics or awards; leave those parts out.
- Times, open/closed, counts and totals come from one function and one data file; check the edge cases.
- Photos: credited, licence checked; crop people, signs and number plates the client has not cleared.

## Check before handing back

Run, do not read, the bundled scripts; print only their summary lines.
1. `python ${CLAUDE_SKILL_DIR}/scripts/check_site.py <mockups dir>` — fix every `FLOOR`.
2. One `capture.mjs` jobs file for the changed pages at 390 and 1280; open only cropped parts to check a fix.
3. `python ${CLAUDE_SKILL_DIR}/scripts/side_by_side.py <out.html> <ours.jpg> <base.jpg>` at both widths; fix every place ours is emptier, plainer or more boxed than the base.
4. Hand back at most ten lines: what you built, what is sample, what is left, and the paths of the pictures to send.
