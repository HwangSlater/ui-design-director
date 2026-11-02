# Showing candidates

Every choice the user makes — format reference, palette, layout option — is shown visually, in the browser, before it is asked about in chat. A table of links or a folder of screenshots is not a presentation: the user has to open tabs, compare from memory, and judge from one image. Use the tools below so every project looks and behaves the same.

## Rules

- **Pictures first, words last.** Open the viewer in the user's browser, then ask a short question. Keep chat to what the screen cannot say (licence, what was not verified).
- **Several screens per candidate.** One screenshot is not enough to judge a site. Capture the pages that matter for the product (for a shop: first screen, list, detail, cart or checkout) at a desktop width and a real phone width.
- **Same frame for every candidate.** The viewer shows one candidate at a time, full screen, in an identical frame, scrolled inside the frame. Never mix image sizes or crops between candidates.
- **No commentary on the board.** Do not put pros/cons chips, badges, or paragraphs on the viewer. The user judges from the screens; your recommendation and reasoning go in chat, briefly.
- **Ask with clickable options** when the client offers a structured question tool: one option per candidate (number + name + one-line consequence), recommendation first and labelled. Otherwise ask for a number in one sentence.
- **Palettes are tried, not listed.** Show palettes as switchable colours on a live preview built in the chosen format (§ Palettes), never as a static swatch table.
- **Korean text** uses `word-break: keep-all` everywhere (viewer, previews, mockups) so words never split mid-word.

## Capturing sites — `scripts/capture.mjs`

Drives the installed Edge or Chrome through the DevTools protocol; no packages. Emulates real device widths (a headless window cannot go below about 500 px, so window-size screenshots of "phone" layouts are wrong), scrolls to wake lazy images, captures the full page, and refuses to save 4xx/5xx responses.

```bash
python scripts/make_board.py <spec.json> --jobs <jobs.json>   # job list from the spec's urls
node scripts/capture.mjs <jobs.json> <captures-dir> [--widths 1280,390]
```

A job may carry `steps` run in the same window before the capture — `{"goto": url}`, `{"click": "css"}`, `{"wait": ms}` — so state-dependent pages are captured in a comparable state (e.g. add a product, then capture the cart; an empty cart compares nothing). Set the job's url to `@current` to capture the page the steps ended on when its address is unknown. In the spec these live under each candidate's `steps` keyed by page.

Files already captured are skipped, so a rerun resumes an interrupted batch. Open a few captures before building the viewer: a 200 response can still be the wrong page. Note capture limits honestly (e.g. sections that fade in on scroll may appear faded).

## The viewer — `scripts/make_board.py`

```bash
python scripts/make_board.py <spec.json> <out-dir>/index.html
```

Spec fields: `project`, `step`, `dock` (2 two-tier bar is the standard; 1 one-row and 3 three groups exist for comparison only), `pages_mode` (`tabs`, the standard: one page at a time, ↑ ↓ switch pages; `stack` exists for comparison only: all pages joined top to bottom so scrolling alone walks through them, with each page's name pinned at its top and the tabs jumping and following), `captures`, `widths` (default 1440 and 390), `pages` (key + label), and `candidates` (`id`, `slug`, `title`, `meta`, `recommended`, `demo`, `urls`, `steps`). Use the name the visitor sees on the site as `title` and put the template's name in `meta`. Captures are read from `<captures>/<slug>-<page>-<width>.jpg`.

The viewer fills the window with the selected page. A floating two-tier bar at the bottom shows the step title ("뼈대 고르기 · 5개 중 하나를 골라 주세요"), the current candidate, and the controls: thumbnails, previous/next, page tabs, PC/phone, demo link, hide. Keys: ← → candidates, ↑ ↓ pages, M phone, H hide. Behaviour the usability test required:

- the chosen page tab stays chosen across candidates; a candidate without that page shows "this candidate has no … page" in the frame and its tab is marked 없음 — never silently switch tabs;
- one tooltip above the whole bar, describing the action first and the key second, shown on hover and keyboard focus only;
- keyboard focus is drawn in a different colour from the selected state, and shortcuts move focus to the newly selected item;
- the wheel scrolls the visible page from anywhere, including over the bar and beside the phone frame;
- a missing page is marked without changing the tab's width (faint text and a corner dot), so the bar never resizes between candidates;
- page jumps are instant — pages are thousands of pixels apart and a smooth scroll makes the next key press start from the wrong place;
- hiding the bar collapses it into a pill in the bottom-right corner that still says which candidate, page and view are showing ("2 Field · 상품 목록 · 휴대폰") and reopens on click or H;
- long text never leaves the bar: names, notes and page tabs truncate with an ellipsis (shrinking the note first, the candidate name last) and show in full in the tooltip; the name row never widens the bar; on narrow screens the "n개 중 하나" hint is dropped and the thumbnail row scrolls sideways.

The bar itself lives in `assets/dock.css` and `assets/dock.js` (tokens, tooltip, hide/pill, shortcuts) and is shared with the palette preview, so both choices look and behave the same. Fix bar problems there, not in a copy.

The address keeps the position (`#c=1&p=home&v=pc`) so you can open the user straight to a specific view.

Use the same viewer for layout options (`page-design.md`): render each option, capture it with `capture.mjs`, and list options as candidates.

## Palettes — `assets/palette-switcher.js` and `.css`

After the format is chosen, build a small preview page in that format's structure with realistic content (for a shop: header, first screen, categories, product grid, product detail). Style it only with six role colours — `--c-bg`, `--c-surface`, `--c-text`, `--c-action`, `--c-on-action`, `--c-accent` — plus values mixed from them. Wrap the content in `.page` and use container queries so the phone view reflows it.

Put the candidates in `<script type="application/json" id="palettes" data-step="팔레트 고르기">` with their source link, original swatches, role mapping, and a one-line note on derived colours. The switcher adds the same two-tier bar as the candidate viewer: step title, palette name and note, colour-strip thumbnails, the three contrast checks (text/background, button text/button, accent/background, computed from the hex values, with the verdict in words as well as colour) where the page tabs would be, PC/phone, source link and hide. Keys: ← → palettes, M phone (the page narrows to 390 px inside a device frame on the dark stage), H hide. The address keeps the choice (`#p=A&v=phone`). Link `dock.css` and `palette-switcher.css`, load `dock.js` then `palette-switcher.js`, and copy all four files next to the page.

## Before showing

Run `scripts/check_site.py` on the folder (boards carry `<meta name="check-site" content="comparison-board">`, so raw swatch colours are not reported as drift) and look at the viewer yourself at 1440×900 and 1280×720: nothing clipped, bar not covering the end of the page, same frame for every candidate. Screenshots taken with the browser's `--screenshot` flag can catch the page before scripted scrolling settles; verify interactive states through the DevTools protocol (as `capture.mjs` does) before trusting them. Then open it for the user.
