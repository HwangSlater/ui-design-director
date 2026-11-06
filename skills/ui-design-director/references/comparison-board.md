# Showing candidates

## Rules

- **Pictures first, words last.** Give the user the viewer's full address and let them open it (open a window yourself only when they ask), then ask a short question. Keep chat to what the screen cannot say (licence, what was not verified).
- **Same frame for every candidate.** Never mix image sizes or crops between candidates.
- **No commentary on the board.** No pros/cons chips, badges or paragraphs on the viewer; your recommendation goes in chat, briefly.
- **Ask with clickable options** when the client offers a structured question tool: one option per candidate (number + name + one-line consequence), recommendation first and labelled. Otherwise ask for a number in one sentence.
- **Palettes are tried, not listed** (§ Palettes), never a static swatch table.
- **Three or four phone screens per image** when the user can only see images; label each screen by what it shows, not by its file name.
- **Korean text** in previews and mockups uses `word-break: keep-all` (the viewer's CSS already does).

## Live sites first — the shared viewer in live mode

Every candidate screen uses the one shared viewer (bottom bar, thumbnails, 확정, keys): never write another viewer page. For a user who can open web pages, build it in live mode — `python scripts/make_live_board.py <spec.json> <out.html>` (or `"live": true` in a `make_board.py` spec): the centre shows the real page in a phone or desktop frame, captures in the spec's captures folder become the thumbnails, and sites that refuse framing are marked for the proxy.

Capture the part being compared (the grid, not the banner above it) and name each image by what it shows.

**Blocked sites: real window first, snapshot to compare, proxy last.** 「실제 창으로 보기」 opens the candidate in a sized window of the client's own browser and follows the board (no install, full motion; sites that answer automated browsers with 403 open normally there). `node scripts/snapshot.mjs <jobs.json> <dir>` saves each blocked candidate as a sanitised local HTML (no scripts, fonts and photos kept, animations frozen at their end state) — sharp and scrollable to the end, but frozen, so never the only view for motion. Snapshots are copies of other people's pages: keep them outside the project and delete them after the choice.

**Blocked sites through the local proxy.** When the board reports blocked or failing candidates (Naver Place, Daangn, most platform pages, sites whose firewall refuses bare requests), run `node scripts/live_proxy.mjs <board.html> <spec.json>` in the background and give the user the `OPEN` address it prints instead of the file. It sends browser-like headers, proxies the site's own fonts so the base's type shows, and loads pages without their scripts (lazy `data-src` photos and `<noscript>` content are made visible). Before showing a candidate the board asks the proxy whether the page is empty without scripts and turns them on if so — no `"js": true` by hand. On the board, 「우회로 보기」 sends a directly framed site that shows a block page or nothing through the proxy, and 「스크립트 켜기」 fixes a wrong guess (text present but photos or backgrounds come from scripts). The address keeps the view (`#c=2&p=0&v=pc&x=1`). Login-walled apps (Instagram) still show a splash screen — capture those. Stop the proxy when the choice is made.

Capture with `capture.mjs` only what the live page cannot show: login-walled sites, a user who can only look at images — one first-screen image per candidate, not a full set — and the side-by-side critique in `ui-review.md`.

## Capturing sites — `scripts/capture.mjs`

Phone captures need `capture.mjs` (it emulates the device width); a narrowed headless window is not a phone layout.

```bash
python scripts/make_board.py <spec.json> --jobs <jobs.json>   # job list from the spec's urls
node scripts/capture.mjs <jobs.json> <captures-dir> [--widths 1280,390]
```

A job may carry `steps` run in the same window before the capture — `{"goto": url}`, `{"click": "css"}`, `{"hide": "css"}` (removes overlays such as the bottom bar), `{"wait": ms}` — so state-dependent pages are captured in a comparable state (add a product, then capture the cart). Set the job's url to `@current` to capture the page the steps ended on. In the spec these live under each candidate's `steps` keyed by page.

It also saves screen-height slices to `<captures-dir>/screens/` (`<id>-<width>-1.jpg` …). Point image-only users to the slices from the first set, not the full-page capture; open only the slice you send. For pages with the bottom bar (palette preview), capture with `steps` that `hide` `.v-nav, .v-tip` and `url: "@current"`.

Files already captured are skipped, so a rerun resumes an interrupted batch. Run `scripts/check_shots.py` (§ Before showing) before building the viewer: a 200 response can still be the wrong page. Note capture limits honestly (sections that fade in on scroll may appear faded).

## The viewer — `scripts/make_board.py`

```bash
python scripts/make_board.py <spec.json> <out-dir>/index.html
```

Spec fields: `project`, `step`, `captures`, `widths` (default 1440 and 390), `pages` (key + label), and `candidates` (`id`, `slug`, `title`, `meta`, `recommended`, `demo`, `urls`, `steps`); leave `dock` and `pages_mode` at their defaults. Use the name the visitor sees on the site as `title` and put the template's name in `meta`. Captures are read from `<captures>/<slug>-<page>-<width>.jpg`.

The bottom bar shows the step title ("뼈대 고르기 · 5개 중 하나를 골라 주세요"). Keys: ← → candidates, ↑ ↓ pages, M phone, H hide. The bar lives in `assets/dock.css` and `assets/dock.js`, shared with the palette preview; fix bar problems there, not in a copy (the behaviour it must keep is listed at the top of `dock.js`).

After the user chooses, show the revision on its own: only the chosen option as revised, with earlier options removed or moved to an `earlier/` folder.

The address keeps the position (`#c=1&p=home&v=pc`), so you can open the user straight to a view.

Use the same viewer for layout options (`page-design.md`): render each option, capture it, and list options as candidates.

## Palettes — `assets/palette-switcher.js` and `.css`

After the format is chosen, build a small preview page in that format's structure with realistic content for the main-job screens. Style it only with six role colours — `--c-bg`, `--c-surface`, `--c-text`, `--c-action`, `--c-on-action`, `--c-accent` — plus values mixed from them. Wrap the content in `.page` and use container queries so the phone view reflows it. Candidates differ as `color-selection.md` § Curate for the product says.

Put the candidates in `<script type="application/json" id="palettes" data-step="팔레트 고르기">` with their source link, original swatches, role mapping, and a one-line note on derived colours; the switcher builds the bar (contrast goes in the thumbnail tooltip, not the bar). Keys: ← → palettes, M phone, H hide; the address keeps the choice (`#p=A&v=phone`). Link `dock.css` and `palette-switcher.css`, load `dock.js` then `palette-switcher.js`, and copy all four files next to the page.

**For a user who can only look at images**, a live switcher shows one palette. Capture every palette and every font with the bar hidden and send side-by-side sheets — all palettes on one or two images at the first screen and the densest section, all fonts likewise — named by candidate, after `check_shots.py`.

**Fonts on the same page.** The switcher also takes font candidates from `<script type="application/json" id="fonts">` (`id`, `name`, `heading`, `body` font stacks, `css` stylesheet URLs and/or `faces` — `{family, src, weight}` for fonts published only as files — plus `maker`, `license`, `source`, `note`). Offer well-known free fonts, including those released by companies (RIDIBatang, Wanted Sans, Spoqa Han Sans Neo, LINE Seed, Gmarket Sans), not only Google Fonts. Check commercial web embedding in each licence (KoPub needs separate approval for web embedding) and say what it allows in `license`; when a font loads from a mirror for the preview, note that the real site should self-host the official files. The page uses `--f-heading` and `--f-body`. Set `data-sample` on the fonts script to a line from this project (`"19:30 영통 A코트 · 승점 19"`), never one left from another project. The address keeps `&f=1`.

**Sample photos.** Fill photo slots with sample photos rather than empty hatched boxes, matched to the product and to the client's customers' setting (a Korean apartment, not a Western bathroom); before/after samples must show the same room, otherwise leave labelled 「전 사진 자리 / 후 사진 자리」 slots. List each photo's page in the footer and say on the page that they are samples to be replaced. Keep the hatched slot underneath and remove an image that fails to load, so offline the slots show instead of broken icons.
- Never collect photos by driving a browser or script over Unsplash's site (Terms §8 forbid automated access except through the API).
- Search in this order, crediting author and licence: hallmark's library (`node <hallmark>/scripts/theme.mjs photos "<subject>" --json`); the Wikimedia Commons API (`commons.wikimedia.org/w/api.php`, `generator=search`, `filetype:bitmap`, `prop=imageinfo` with `extmetadata`, a descriptive User-Agent; keep CC0, public domain or CC BY; use the sized thumbnail URL — only some widths work, 960 and 1280 did); the WordPress Photo Directory via Openverse (`api.openverse.org/v1/images/?q=<subject>&source=wordpress`, CC0; download the files into the mockup folder). Otherwise use the Unsplash API with the user's own key (kept in their secrets folder, never in the page), or ask the user to pick photos in their browser and paste the photo pages.
- Prefer everyday, unstaged photos (people, places, mess) over evenly graded stock, which a blind judge read as AI. Judge candidates from a contact sheet, not their titles, check the subject matches what the user has, and check every photo loaded.

## Before showing

Run `scripts/check_site.py` on the folder (boards carry `<meta name="check-site" content="comparison-board">`, so raw swatch colours are not reported as drift).

Before any image goes to the user, run `python scripts/check_shots.py <folder>`: it flags captures that are blank or one colour at the top (spinner, logo-only entrance, black intro). `capture.mjs` hides cookie, consent and newsletter overlays by default (`"keepOverlays": true` keeps them).

## The confirm button — `scripts/wait_choice.mjs`

Both bars carry a 확정 button so the user can decide on the screen. Start the waiter before giving out the address:

```bash
node scripts/wait_choice.mjs <page.html> <decision.json> [--hash "p=A&f=1&v=pc"] [--minutes 120]
```

- It prints `OPEN http://127.0.0.1:<port>/<page>#…&wait=<port>-<key>`; give the user that address, not a `file://` one (Chrome blocks a file page calling 127.0.0.1, and the button falls back to copying).
- Run it in the background so its exit wakes you (Claude Code: `run_in_background`). On exit 0 it has written `decision.json` (`step`, `label`, `choice`, `received_at`): record the decision in the brief or `DESIGN.md` and continue to the next gate without asking again. Exit 3 means it timed out.
- If the user answers in chat instead, stop the waiter. Never leave one running after the step.
- Without a waiter the button copies "<step>: <label> 확정" to paste into chat, so a decision is never lost.
