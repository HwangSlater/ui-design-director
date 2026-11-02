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

A job may carry `steps` run in the same window before the capture — `{"goto": url}`, `{"click": "css"}`, `{"hide": "css"}` (removes overlays such as the bottom bar), `{"wait": ms}` — so state-dependent pages are captured in a comparable state (e.g. add a product, then capture the cart; an empty cart compares nothing). Set the job's url to `@current` to capture the page the steps ended on when its address is unknown. In the spec these live under each candidate's `steps` keyed by page.

It also saves screen-height slices of each capture down to the end of the page (up to 16) to `<captures-dir>/screens/` (`<id>-<width>-1.jpg` …). A full-page phone capture is thousands of pixels tall and unreadable when opened as a file — users who look at files instead of the viewer could not read any text — so point them at the slices from the very first set of candidates, not after they complain. For pages that carry the bottom bar (palette preview), capture with `steps` that `hide` `.v-nav, .v-tip` and `url: "@current"` so neither the bar nor its collapsed pill covers the slices.

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
- long text never leaves the bar: names and notes truncate with an ellipsis (shrinking the note first, the candidate name last) and show in full in the tooltip; the name row never widens the bar; on narrow screens the "n개 중 하나" hint is dropped;
- many candidates or tabs never squeeze the rest of the bar: the thumbnail row has a capped width (`--v-cands-max`) and scrolls sideways, page tabs keep their full label and scroll sideways when they do not fit, and the selected thumbnail and tab are scrolled into view. Check a viewer with 15+ candidates and 6 tabs at 1280 and 390 before showing it.

The bar itself lives in `assets/dock.css` and `assets/dock.js` (tokens, tooltip, hide/pill, shortcuts) and is shared with the palette preview, so both choices look and behave the same. Fix bar problems there, not in a copy.

The address keeps the position (`#c=1&p=home&v=pc`) so you can open the user straight to a specific view.

Use the same viewer for layout options (`page-design.md`): render each option, capture it with `capture.mjs`, and list options as candidates.

## Palettes — `assets/palette-switcher.js` and `.css`

After the format is chosen, build a small preview page in that format's structure with realistic content (for a shop: header, first screen, categories, product grid, product detail). Style it only with six role colours — `--c-bg`, `--c-surface`, `--c-text`, `--c-action`, `--c-on-action`, `--c-accent` — plus values mixed from them. Wrap the content in `.page` and use container queries so the phone view reflows it.

Make the candidates differ in more than the button: background, surfaces, text and accent together, so the page changes character at a glance. A set that only swaps the action colour gives the user nothing to choose between ("they were all the same except the button").

Put the candidates in `<script type="application/json" id="palettes" data-step="팔레트 고르기">` with their source link, original swatches, role mapping, and a one-line note on derived colours. The switcher adds the same two-tier bar as the candidate viewer: step title, palette name and note, colour-strip thumbnails (their tooltip gives the computed contrast for text/background, button text/button and accent/background), the font button where the page tabs would be, PC/phone, source link, 확정 and hide. Keep contrast out of the bar itself: users found the three readouts noise; the numbers belong in the tooltip, in chat when they matter, and in `DESIGN.md`. Keys: ← → palettes, M phone (the page narrows to 390 px inside a device frame on the dark stage), H hide. The address keeps the choice (`#p=A&v=phone`). Link `dock.css` and `palette-switcher.css`, load `dock.js` then `palette-switcher.js`, and copy all four files next to the page.

**Fonts on the same page.** Typography is its own choice, but it is judged together with colour, so the switcher also takes font candidates from `<script type="application/json" id="fonts">` (`id`, `name`, `heading`, `body` font stacks, `css` stylesheet URLs and/or `faces` — `{family, src, weight}` for fonts published only as font files — plus `maker`, `license`, `source`, `note`). Offer well-known free fonts, including those released by known companies (e.g. RIDIBatang, Wanted Sans, Spoqa Han Sans Neo, LINE Seed, Gmarket Sans), not only Google Fonts. Check each licence from its published text for commercial web embedding before listing it (KoPub, for example, needs separate approval for web embedding) and say what it allows in `license`; when a font is loaded from a mirror for the preview, note that the real site should self-host the official files. The page uses `--f-heading` and `--f-body`; the bar's centre 글꼴 button (showing the current font name) opens a scrollable list above it, each entry drawn in its own font with a sample line, and F cycles fonts. Stylesheets load on first use. The address keeps `&f=1`.

**Sample photos.** Empty hatched boxes make every palette look flat. Fill photo slots with sample photos hotlinked from a free-licence library (Unsplash: free for commercial use, hotlinking its image URLs is expected) that match the product, list each photo's page in the footer, and say plainly on the page that they are samples to be replaced with the user's own. Keep the hatched slot underneath and remove an image that fails to load, so offline the page falls back to the slots instead of broken-image icons. Unsplash blocks plain HTTP clients; collect URLs through a real browser (DevTools protocol, as `capture.mjs` does) and judge candidates from a contact sheet of the images, not from their auto-translated titles.

## Before showing

Run `scripts/check_site.py` on the folder (boards carry `<meta name="check-site" content="comparison-board">`, so raw swatch colours are not reported as drift) and look at the viewer yourself at 1440×900 and 1280×720: nothing clipped, bar not covering the end of the page, same frame for every candidate. Screenshots taken with the browser's `--screenshot` flag can catch the page before scripted scrolling settles; verify interactive states through the DevTools protocol (as `capture.mjs` does) before trusting them. Then give the user the full address to open; do not open browser windows on their screen unless asked.

## The confirm button — `scripts/wait_choice.mjs`

Both bars carry a 확정 button so the user can decide on the screen instead of typing in chat. Start the waiter before giving out the address:

```bash
node scripts/wait_choice.mjs <page.html> <decision.json> [--hash "p=A&f=1&v=pc"] [--minutes 120]
```

- It listens on a free port on 127.0.0.1 only, with a one-time key, and also serves the page's folder read-only on the same address, so it prints `OPEN http://127.0.0.1:<port>/<page>#…&wait=<port>-<key>`. Give the user that address; it is the only one whose button reaches you, and the viewers keep `wait` in the address while the user moves around. Do not hand out a `file://` address for confirming: Chrome (Local Network Access) blocks or prompts when a file page calls 127.0.0.1, and the button then falls back to copying. Only files inside the page folder with known web types are served; anything else, folder listings and paths outside it get 404.
- Run it in the background in a way that wakes you when it exits (in Claude Code: `run_in_background`). On exit code 0 it has written `decision.json` (`step`, `label`, `choice`, `received_at`; the key is not stored): record the decision in the brief or `DESIGN.md` and continue to the next gate without asking again. Exit 3 means it timed out.
- If the user answers in chat instead, stop the waiter. Never leave one running after the step.
- Without a waiter (another client, a closed session, an expired wait) the button says it is not connected, copies "<step>: <label> 확정" to the clipboard and shows it to paste into chat, so a decision is never lost.
- The button's label keeps its width (확정 / 보내는 중 / 확정됨) and the result stays on screen until closed.
