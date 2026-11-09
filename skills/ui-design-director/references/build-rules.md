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
3. **Motion only from the base.** Reproduce the motion in `바탕-움직임.md` with those durations and curves — hover changes, sticky header, reveal on scroll, auto-advancing slides. Add no motion the base does not have.
4. Change only what several field sites do differently (「바꿀 곳」 n/N in `DESIGN.md`). A part the base lacks comes from the field sites (n/N) or the client's own objects (menu board, sign, ticket), recorded in `DESIGN.md` § 부품 출처.
5. **Desktop is not a centred phone column.** Each width takes the base's own composition for that width (a side column, a live preview, help next to the fields); a phone column centred in empty space is a finding.
6. **Visual layers.** Keep the base's finish, not only its structure. Its layers — identity (logo, wordmark, header band), item faces (crests, product photos, avatars), icons, colour blocks beyond buttons, data marks (chips, bars, badges), imagery, depth (shadows, one dark panel), wide-screen columns, type contrast, trust (real reviews, ratings, certificates) — are each kept, replaced or knowingly dropped and recorded in `DESIGN.md` § Visual layers. A dislike replaces a layer's form, it does not delete the layer; two or more layers dropped without a replacement goes back to the client before building.

## Make it ours, not a copy

- Our name, content, photos and the chosen colours. Character comes through photos and wording, not added boxes: a first screen the base keeps to photo and menu stays photo and menu.
- Nobody should say 「이거 ○○ 아냐?」 at first glance: no base logo, mascot, brand colour, set phrases or a component only the base has. Tell the client which recognisable parts you changed.
- Follow the base's structure, never its finish as well. At least two of these must be ours, and `DESIGN.md` § 바탕에서 바꾼 곳 names them: the colour family (never the base's exact palette), the name/wordmark treatment, the finish of the repeated item (card, row, tile: border, fill, corner, divider), and one signature element that comes from this client's job (for Korean NBA fans: today's games on Korean time, the broadcast channel). When `skeleton.mjs --base` finds 0 「바꿀 곳」 the structure stays — these finish changes are still required. `python ${CLAUDE_SKILL_DIR}/scripts/copy_check.py <project>` (also run by `preflight.py`) refuses a first screen whose colours equal the base's.
- A base part you keep keeps its look (drawing, lines, photo); if you cannot carry the look, drop it rather than leave a bare text version.
- At most one section from another shortlisted site, by name and for a stated reason. Never copy protected logos, illustrations or text.

## Colour, type and identity parts

- Colours: the base's combination of 4–6 tones and their relationships (from `DESIGN.md`), never a white page with one accent. Colour fields only where the base has them — no pale tinted bands between sections.
- Knowledge: before building each part, run `python ${CLAUDE_SKILL_DIR}/scripts/knowledge.py ask --part <part> --stage main` with the part's real id — `first-screen`, `header`, `nav`, `button`, `card`, `form`, `input`, `footer`, `numbers`, `korean-text`, `body-text`, `heading`, `image`, `list`, `table`, `error-state`, `empty-state`, `loading`, `booking`, `shop` (all ids: `knowledge.py parts`); Korean names also work (`--part "첫 화면,단추,입력 양식"`), and an unknown name prints the nearest ids. Then follow those rules where the base does not decide; cite the rule id when the client asks why. The base still wins ([design-knowledge.md](design-knowledge.md)).
- Fonts: only the faces approved in `DESIGN.md`, chosen by [fonts.md](fonts.md) (`fonts.py pick`, never from memory).
- Identity parts take the base's measured finish: the wordmark (typeface, size, weight, tracking, colour, placement — a designed name, never body text in a bar), the navigation, the buttons (fill or outline, border, height, padding, type). A default black pill or a plain text name is a finding.
- No more boxes than the base: count bordered or filled rectangles (cards, panels, tags, labels, button blocks, tinted bands) on both pages; ours may not have more. Text and photos sit on the page; labels are plain text.

## What reads as generated

The single list of generated-look tells; other files point here. Never: a white panel floating on the hero photo with label–value facts; a stock photo with a floating box, headline and two buttons; letters or emoji in circles as icons; thin generic line icons; a small overline above the name; a row of identical icon tiles or icon cards over the photo edge; empty photo boxes or 「… 자리」 slots; pale bands everywhere; one accent on white; a half-and-half colour panel; a symmetrical two-card split; left-border callouts; a status dot before every state; the same 6–8px radius on every box; boxes inside boxes; three sections in a row with the same make-up; a grey footnote under every block; a display face on every title; a monospace for times and prices. Gradients, glass, pills everywhere and oversized hero text only when the base has them.

Also generated unless the base has them (from unslop's signs list, Damir Sokolovsky, CC BY 4.0, github.com/heydamir/unslop): uppercase or headings with wide letter spacing; emoji as icons, labels or status; glowing shadows and coloured glows; cards and buttons that grow on hover, `transition: all`; everything flying in on load; numbers in mixed formats on one screen (`48,210` beside `124,860.40`) — one format, tabular figures; a small chart or sparkline on every stat; several near-identical tints of one hue for text; a headline that would fit any business if the name were swapped; exclamation marks and hype words (최고, 완벽한, 특별한 경험) on labels and buttons. `check_site.py` flags wide tracking, emoji, glow, hover growth and `transition: all` as DRIFT.

## Content and samples

- Only facts the client gave; anything filled in is listed at handover. Where the client's words are missing (an intro, a price, an address) write short neutral sample text of the right length.
- **One 「견본」 line.** Everything that is sample — text and photos — is listed in one 「견본」 line at the page foot (「사진과 소개 글은 견본이에요」), never marked on the page itself.
- **No empty boxes.** Never a hatched box, dashed slot or 「… 자리」 label: every photo slot gets a licence-checked sample photo of the right subject ([sample-photos.md](sample-photos.md)). When no fitting sample exists (before/after of the same room, a staff photo), drop the part and ask the client for the photo.
- Never invented testimonials, reviews, logos, statistics or awards; leave those parts out until the client supplies real ones.
- Real logos, team marks or photos found by search (the client may ask for them as samples): use them only marked 견본, tell the client in the same message that a live site needs the owners' permission (league, team, photographer), and list them in the 「견본」 footer line. Never present them as approved for launch.
- Times, open/closed, counts and totals come from one function and one data file; check the edge cases.
- Photos: credited, licence checked; crop people, signs and number plates the client has not cleared. No generated imagery.

## Check before handing back

Run, do not read, the bundled scripts; print only their summary lines.
1. `python ${CLAUDE_SKILL_DIR}/scripts/check_site.py <mockups dir>` — fix every `FLOOR`.
2. One `capture.mjs` jobs file for the changed pages at 390 and 1280; open only cropped parts to check a fix.
3. `python ${CLAUDE_SKILL_DIR}/scripts/side_by_side.py <out.html> <ours.jpg> <base.jpg>` at both widths; fix every place ours is emptier, plainer or more boxed than the base.
4. Hand back at most ten lines: what you built, what is sample, what is left, and the paths of the pictures to send.
