# Showing candidates

## Contents
- Rules
- The board — live sites in the shared viewer
- Palettes and fonts
- Before showing
- Only when the client can only look at images, or a page is behind a login

## Rules

- **Pictures first, words last.** Give the client the one address the tool prints and let them open it (open a window yourself only when they ask), then ask a short question. Keep chat to what the screen cannot say (licence, what was not verified).
- **Same frame for every candidate.** Never mix image sizes or crops between candidates.
- **No commentary on the board.** No pros/cons chips, badges or paragraphs on the viewer; your recommendation goes in chat, briefly.
- **Ask with clickable options** when the client offers a structured question tool: one option per candidate (number + name + one-line consequence), recommendation first and labelled. Otherwise ask for a number in one sentence.
- **Palettes are tried, not listed** (§ Palettes and fonts), never a static swatch table.

## The board — live sites in the shared viewer

Every candidate screen uses the one shared viewer; never write another viewer page. Candidates come from `design-selection.md` §§ 2–3.

1. Write `formats/board-spec.json`: `project`, `step`, `captures`, `widths` (default 1440 and 390), `pages` (key + label), and `candidates` (`id`, `slug`, `title`, `meta`, `recommended`, `demo`, `urls`, `steps`); leave `dock` and `pages_mode` at their defaults. Use the name the visitor sees on the site as `title` and put a template's name in `meta`.
2. Run `node ${CLAUDE_SKILL_DIR}/scripts/live_proxy.mjs formats/board-spec.json` in the background (Claude Code: `run_in_background`). Give the client the one `OPEN` address it prints, never a `file://` path.
3. When the client presses 확정 it prints a `DECISION` line and writes `formats/decision.json`: record the base and continue to the material step without asking again. If the client answers in chat instead, record it with `stage.py --decide`. Stop the proxy once the choice is made.

**Sites that refuse a frame**, in this order:
1. **The proxy view in the same board** — the default; if a candidate shows a block page, nothing, or text without its photos, use the board's 「우회로 보기」 or 「스크립트 켜기」.
2. **「실제 창으로 보기」** — the real site in a sized window of the client's own browser. This is where motion and feel are judged.
3. **A snapshot** (`base_material.py` at the material step) — only for exact structure, fonts and colours; it is frozen, so never the view for motion.

Login-walled apps (Instagram) show only a splash screen: capture those (last section).

**Snapshots and captures** of other sites stay in the project folder's `formats/`, are never committed, and are deleted once the mockup is approved.

After the client chooses, show the revision on its own: only the chosen option as revised, earlier options removed or moved to an `earlier/` folder. Use the same viewer for layout options (`page-design.md`): list each option as a candidate.

## Palettes and fonts

After the base is chosen, build a small preview page in the base's structure with realistic content for the main-job screens. Style it only with six role colours — `--c-bg`, `--c-surface`, `--c-text`, `--c-action`, `--c-on-action`, `--c-accent` — plus values mixed from them. Wrap the content in `.page` and use container queries so the phone view reflows it. Each candidate is built from the base's 4–6 tones (`color-selection.md`).

Put the candidates in `<script type="application/json" id="palettes" data-step="팔레트 고르기">` with their source, original swatches, role mapping, and a one-line note on derived colours; the switcher builds the bar. Link `assets/dock.css` and `assets/palette-switcher.css`, load `dock.js` then `palette-switcher.js`, and copy all four files next to the page.

**Fonts on the same page.** The switcher also takes font candidates from `<script type="application/json" id="fonts">` (`id`, `name`, `heading`, `body` font stacks, `css` stylesheet URLs and/or `faces` — `{family, src, weight}` for fonts published only as files — plus `maker`, `license`, `source`, `note`). The candidates come from [fonts.md](fonts.md) (`fonts.py pick`), never from memory; put each font's origin in `source` and its licence conditions in `license`. Run `python ${CLAUDE_SKILL_DIR}/scripts/fonts.py check palette` before sending; when a font loads from a mirror for the preview, note that the real site should self-host the official files. The page uses `--f-heading` and `--f-body`. Set `data-sample` on the fonts script to a line from this project (`"19:30 영통 A코트 · 승점 19"`), never one left from another project.

**Complete example — copy and fill; do not read the switcher script.** Angle-bracket values come from the tools named; everything else is the exact field set the switcher reads. A palette needs `id` and all six `roles` (one missing and the switcher drops that candidate); a font needs `id`, `heading` and `body`. `colors` are the swatches on the chip, `source` opens from the bar, `note` shows under the name. For a font, take the webfont line `fonts.py pick` prints: a stylesheet goes in `css`; for a font published only as files run `python ${CLAUDE_SKILL_DIR}/scripts/fonts.py face "<name>"` and copy each printed `@font-face` rule's `font-family`, `src` url and `font-weight` into one `faces` item (`style` is optional, default `normal`).

```html
<link rel="stylesheet" href="dock.css"><link rel="stylesheet" href="palette-switcher.css">
<script type="application/json" id="palettes" data-step="팔레트 고르기">
[{"id": "A", "name": "바탕 그대로", "source": "<base url>",
  "colors": ["#f6f1e9", "#ffffff", "#2b2622", "#8a4b2a", "#d9a441"],
  "roles": {"bg": "#f6f1e9", "surface": "#ffffff", "text": "#2b2622", "action": "#8a4b2a", "on-action": "#ffffff", "accent": "#d9a441"},
  "note": "면 색은 배경에 흰색 6%를 섞음"}]
</script>
<script type="application/json" id="fonts" data-sample="<a line from this project>">
[{"id": "1", "name": "<pick name>", "heading": "\"<family>\", serif", "body": "\"<family>\", sans-serif",
  "css": ["<stylesheet url from fonts.py pick>"],
  "maker": "<maker>", "license": "<licence conditions>", "source": "<official page>", "note": "제목·본문 같은 글꼴"},
 {"id": "2", "name": "<pick name>", "heading": "\"<family>\", serif", "body": "\"<family>\", serif",
  "faces": [{"family": "<font-family from fonts.py face>", "src": "<src url from fonts.py face>", "weight": "400"},
            {"family": "<font-family from fonts.py face>", "src": "<src url of the bold file>", "weight": "700"}],
  "maker": "<maker>", "license": "<licence conditions>", "source": "<official page>", "note": "미리 보기는 사본, 실제 사이트는 공식 파일을 직접 올림"}]
</script>
<script src="dock.js"></script><script src="palette-switcher.js"></script>
```

**The 확정 button on the palette page.** Start the waiter before giving out the address:

```bash
node ${CLAUDE_SKILL_DIR}/scripts/wait_choice.mjs palette/index.html palette/decision.json [--hash "p=A&f=1&v=pc"] [--minutes 120]
```

- Give the client the `OPEN http://127.0.0.1:<port>/…` address it prints, never a `file://` one.
- Run it in the background so its exit wakes you. On exit 0 it has written `decision.json` (`step`, `label`, `choice`, `received_at`): record the decision in `DESIGN.md` and continue without asking again. Exit 3 means it timed out.
- If the client answers in chat instead, stop the waiter. Never leave one running after the step.

## Before showing

- `python ${CLAUDE_SKILL_DIR}/scripts/check_site.py <folder>` (boards and palette pages are exempt from swatch drift).
- Before any image goes to the client, `python ${CLAUDE_SKILL_DIR}/scripts/check_shots.py <folder>`: it flags captures that are blank or one colour at the top (spinner, logo-only entrance, black intro). A 200 response can still be the wrong page.

## Only when the client can only look at images, or a page is behind a login

Use captures only for login-walled pages, a client who cannot open web pages (one first-screen image per candidate, not a full set), and the side-by-side critique in `ui-review.md`. Phone captures need `capture.mjs` (it emulates the device width); a narrowed headless window is not a phone layout.

```bash
python ${CLAUDE_SKILL_DIR}/scripts/make_board.py formats/board-spec.json --jobs <jobs.json>   # job list from the spec's urls
node ${CLAUDE_SKILL_DIR}/scripts/capture.mjs <jobs.json> <captures-dir> [--widths 1280,390]
python ${CLAUDE_SKILL_DIR}/scripts/make_board.py formats/board-spec.json <out-dir>/index.html  # capture board
```

- Capture the part being compared (the grid, not the banner above it) and name each image by what it shows.
- A job may carry `steps` run before the capture — `{"goto": url}`, `{"click": "css"}`, `{"hide": "css"}`, `{"wait": ms}` — so state-dependent pages are captured in a comparable state (add a product, then capture the cart); set its url to `@current` to capture the page the steps ended on. In the spec these live under each candidate's `steps` keyed by page.
- Screen-height slices land in `<captures-dir>/screens/` (`<id>-<width>-1.jpg` …). Send three or four phone screens per image, labelled by what each shows, from the slices; open only the slice you send.
- Palettes and fonts: a live switcher shows one palette at a time, so capture every palette and every font with the bar hidden (`steps` that `hide` `.v-nav, .v-tip`, `url: "@current"`) and send side-by-side sheets — all palettes on one or two images at the first screen and the densest section, all fonts likewise — named by candidate.
- Note capture limits honestly (sections that fade in on scroll may appear faded).
