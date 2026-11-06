<div align="center">

# UI Design Director

### You know which sites you like. You don't know how to make yours.

A design skill that puts well-known real sites from your field side by side, lets you pick one,<br>
then measures its structure and finish and rebuilds that first page for your own shop or service.

[![Claude Code](https://img.shields.io/badge/Claude%20Code-skill-d97757.svg)](#installation)
[![Codex](https://img.shields.io/badge/Codex-skill-555.svg)](#installation)
![Tested](https://img.shields.io/badge/roleplay%20tests-10-6b8f71.svg)

[한국어](README.md) · **English**

<img src="docs/images/bookshop-hero.jpg" alt="Home page mockup for the independent bookshop 「책방 오후」 on desktop and phone: handwritten name in the centre, a pencil-line hanok-roof background and a 'book of the month, November' card" width="820">

<sub>Home page mockup for 「책방 오후」, an independent bookshop in Jeonju's hanok village. It follows the structure of Title, the Tokyo bookshop chosen as the base; the name, drawing, colours and text are the shop's own.</sub>

</div>

---

## So nobody says "this looks AI-made"

Ask an AI for a bookshop home page and you usually get the same screen: white background, one accent colour, rounded chips, photo cards, the usual fonts. There are plenty of good sites to learn from, but the model redraws the average it remembers instead of looking at them.

**ui-design-director** changes the order.

- It shows about five real sites people in your field already know, plus one or two templates, **side by side at the same size**, and asks you to pick one as the **base**.
- It measures the base's first page section by section: heights, photo share, type sizes, how the name and buttons are drawn, the colour combination. It rebuilds that, then swaps in your name, photos, colours and words.
- It leaves out what identifies the base (its logo, mascot, signature parts), so nobody looking at yours thinks "isn't this ○○?".
- Every choice is shown as a picture and answered with a number. No design vocabulary needed.

## What it makes

Both mockups below were made with this skill. A person played the client; the photos are credited free samples.

### Independent bookshop 「책방 오후」 — home page only

<table>
<tr>
<td width="46%" valign="top"><img src="docs/images/bookshop-phone-full.jpg" alt="The whole 책방 오후 phone page split into three columns: book of the month, shop photo, November calendar, news, meetup sign-up, coffee, directions" width="100%"></td>
<td valign="top">

**Client** a bookseller who runs a small shop alone in a back alley of Jeonju's hanok village<br>
**Wants** book-talk and copying-circle sign-ups and the monthly picks to stand out<br>
**Dislikes** big-chain bookstore feel, over-styled "aesthetic café" looks

1. Five bookshop sites (Thanks Books, Daunt Books, Books Are Magic, Title, one template) side by side; **Title** chosen as the base, because its "book of the day" card matches the monthly picks.
2. Title's structure measured and rebuilt: centred name over a pencil drawing, a framed book card with the month on its border, a large shop photo, a calendar tab, news divided by rules.
3. Title's own sky-blue square logo and street drawing left out; replaced with the shop's sign lettering and hanok-roof lines.
4. Colours from late-afternoon ochre and pine green; fonts other than the ones models always reach for.
5. "Open now · until 8 pm" updates itself from the Monday closing day and opening hours.

</td>
</tr>
</table>

### Jinju Namgang Lantern Festival — a first screen that changes with the date

<table>
<tr>
<td valign="top"><img src="docs/images/festival-states.jpg" alt="Festival first screen on phone in four states: 3 October 4 pm as planned, the same day cancelled by rain, before the festival, after the festival" width="100%"></td>
<td width="30%" valign="top"><img src="docs/images/festival-desktop.jpg" alt="Festival first screen on desktop: lantern gate photo on black with a pink 'today at the festival' panel" width="100%"></td>
</tr>
</table>

**Client** the city tourism office's festival officer · **Base** Amsterdam Light Festival (light installations on black) · **Colours** the base site's own combination

The five questions callers ask most (parking, tonight's fireworks, rain, floating a lantern, toilets and pushchairs) become first-screen shortcuts, and the "today at the festival" panel follows the date and the 3 pm go/no-go the officer enters: as planned, cancelled by rain, before the festival and after it each read differently.

<sub>Photos: festival by hyolee2 (CC BY-SA 3.0); bookshop by Ahmed, Sashimi-b (CC BY 4.0), Mobius6, Sathya Madhu (CC BY-SA 4.0), lumoplank, Tookapic (CC0) — all Wikimedia Commons.</sub>

## Quick start

Install it ([Installation](#installation)) and say:

```text
/ui-design-director A home page for our neighbourhood Pilates studio, just the home page
```

From there the skill asks one thing at a time.

```text
About the shop or service    who, what, which customers · what you dislike
→ Pick a base                ~5 real sites in the field + templates, same size, side by side
→ Pick colours and fonts     3–4 options starting from the base's colours, on the same page
→ Home page mockup           next to the base, phone and desktop, a clickable HTML page
```

A single home page ends there. For the whole site it continues the same way: a page list (`SITE-PLAN.md`), page-by-page mockups, then code.

## Rules are fixed by testing

These rules weren't written at a desk. A fresh session plays the designer and another session or a person plays the client — a café, a snack bar, a vintage shop, a festival, a second-hand market, a campsite, a Pilates studio, a bookshop. Each result is put next to one made without the skill, the "AI tells" are pointed out, and the rule that caused them is changed.

Some of what changed:

| What was pointed out | Rule that caused it | Now |
| --- | --- | --- |
| A white info panel floating on the hero photo | "Put the product's character up front" | First screen stays like the base; character comes through photos and words |
| One colour (white + a single accent) | "One accent besides black" | Carry over the base's 4–6 tones and how they relate |
| Dashed 「… 자리」 empty boxes | "Leave missing content as labelled slots" | Short sample text, flagged in one line at the foot |
| The same fonts every time | No font rule | Model-default fonts banned; pick from free font libraries to match the base |

Each roleplay — what was checked and what changed — is logged in [docs/역할극-기록.md](docs/역할극-기록.md) (Korean). Tokens are measured too, aiming for one home page within an ordinary plan's limits.

## Installation

### Codex: install from a GitHub URL

After publishing this repository to GitHub, ask Codex:

```text
Use $skill-installer to install this skill:
https://github.com/HwangSlater/ui-design-director/tree/main/skills/ui-design-director
```

The user does not need to clone the repository or run a separate shell command. Public repositories are downloaded from the URL; private repositories can use the user's existing Git credentials or token. `$ui-design-director` becomes available on the next turn after installation.

For a copied installation, the complete repository should appear as:

```text
repository/skills/ui-design-director/
├── SKILL.md
├── agents/
└── references/
```

Do not overwrite an existing directory with the same name without inspecting it first. If the skill does not appear after installation, restart Codex or open a new session.

In Codex, the stage-table line at the top of SKILL.md (`!`python …stage.py``) shows as plain text; run that command in the project folder to get the same table. `${CLAUDE_SKILL_DIR}` is the skill folder (`~/.codex/skills/ui-design-director`).

### Claude Code: install as a plugin (recommended)

```text
/plugin marketplace add HwangSlater/ui-design-director
/plugin install ui-design-director@ui-design-director
```

The plugin carries both skills (`ui-design-director`, `ui-wording`) and a hook. The hook acts only inside a skill project (a folder with `concept-brief.md`, `decisions.json` or `formats/board-spec.json`) and refuses:

- a viewer HTML in `formats/` that is not the shared template (it points to `make_live_board.py`)
- a page in `palette/` not built on the palette-switcher template
- base material, palette, `DESIGN.md`, `layouts/` or `mockups/` written before the earlier stages are decided

The hook is not in SKILL.md because claude.ai accepts only a fixed set of frontmatter keys and rejects an upload containing `hooks`. SKILL.md stays portable; enforcement lives in the Claude Code plugin. If you linked the skill folder as below, remove that link when you install the plugin, or the skill is listed twice.

### Claude Code: link it into the personal skills directory (no hook)

Place the `skills/ui-design-director` directory under `~/.claude/skills/`. The `SKILL.md` frontmatter is already compatible, so no file needs editing, and the accompanying `agents/openai.yaml` is harmless.

If you intend to keep editing the skill in this repository, link rather than copy so repository edits apply to the installation immediately.

```bash
# macOS and Linux
ln -s "$PWD/skills/ui-design-director" ~/.claude/skills/ui-design-director
```

```powershell
# Windows (a junction works without administrator rights)
New-Item -ItemType Junction `
  -Path  "$env:USERPROFILE\.claude\skills\ui-design-director" `
  -Target "$PWD\skills\ui-design-director"
```

The link is picked up within the same session; `$ui-design-director` or `/ui-design-director` works from the next turn. Copying also works, but then every repository edit has to be copied again.

The installation paths for the two environments are:

```text
~/.codex/skills/ui-design-director
~/.claude/skills/ui-design-director
```

## Usage

For the simplest guided start:

```text
Use $ui-design-director. I want to choose a design.
Guide me one step at a time even if I do not know design terminology.
```

The skill begins with the product and its users, then leads the conversation through format references, color palettes, coded previews, and final approval. It asks one major question at a time and responds to “I don't know” with contrasting examples or a provisional recommendation.

To establish a concept from scratch:

```text
Use $ui-design-director to understand this product and its users.
Research suitable live templates and 3–4 color palettes,
then let me choose the visual format and palette independently.
```

To compare coded previews:

```text
Use $ui-design-director to create 2–3 small UI previews from my finalist
format and palette combinations. Use identical content for each candidate,
and do not apply anything to production before I approve it.
```

To create the design contract:

```text
Use $ui-design-director to turn my approved format and palette into
project-root DESIGN.md. Separate observed, inferred, and adapted rules.
```

To design the whole site:

```text
Use $ui-design-director to list the pages and main flows this site needs,
based on DESIGN.md. Once I approve, show me layout options per page type.
```

To move approved mockups into code:

```text
Use $ui-design-director to build the approved mockups. Show me one
representative page first, then extend to the rest once I confirm.
```

To review an existing implementation:

```text
Use $ui-design-director to review the rendered UI against DESIGN.md.
Do not modify files; report findings with severity and evidence.
```

## Selection and approval rules

- Format, palette, and typography remain identifiable decisions.
- Selecting a format does not silently approve its default colors.
- Original 3–4 color swatches remain distinct from accessible semantic UI tokens.
- For commercially operated products, licence precedes taste. A candidate that forbids or charges for commercial use is a disqualification, not a footnote.
- Delegated choices are recorded as delegated, with the selection rationale.
- `DESIGN.md` is approved only after format, palette, high-impact adaptations, and requested preview feedback are resolved.
- Coded previews are comparison artifacts, not production implementation or an approved design system.
- “Design the site” authorizes mockups only. Production code is written only on request and for pages whose mockups are approved.
- Invented testimonials, customer logos, or figures are never presented as real; those parts are left out, and other missing copy becomes short sample text flagged in one line at the page foot.

## Companion skills

The open-source skills and tools below assist specific stages only when installed or when the user approves the download. This skill keeps every decision and the `DESIGN.md`/`SITE-PLAN.md` files, and does not copy their text. Rules live in `references/companion-skills.md`.

| Stage | Skill or tool | Licence | Part used |
|---|---|---|---|
| Format, palette, type candidates | [ui-ux-pro-max](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) | MIT | read-only search |
| Layout options | [hallmark](https://github.com/Nutlope/hallmark) | MIT | names of page shapes |
| Motion | [emilkowalski/skills](https://github.com/emilkowalski/skills) | MIT | `animate`, `review-animations` rules |
| Site check | [impeccable](https://github.com/pbakaus/impeccable) | Apache-2.0 | `npx impeccable detect` only |
| Site check | [Web Interface Guidelines](https://github.com/vercel-labs/web-interface-guidelines) | MIT | rule list |

## Repository structure

```text
.
├── README.md
├── README.en.md
├── scripts/
│   └── validate_skill.py
└── skills/
    └── ui-design-director/
        ├── SKILL.md
        ├── agents/
        │   └── openai.yaml
        ├── assets/
        │   ├── dock.css · dock.js
        │   ├── board.css · board.js
        │   └── palette-switcher.css · palette-switcher.js
        ├── scripts/
        │   ├── check_site.py
        │   ├── anchor_check.py
        │   ├── page_rules.py
        │   ├── block_colours.py
        │   ├── side_by_side.py
        │   ├── make_live_board.py
        │   ├── check_shots.py
        │   ├── blind_sheet.py
        │   ├── compose_metrics.mjs
        │   ├── extract_styles.mjs
        │   ├── capture.mjs
        │   ├── make_board.py
        │   └── wait_choice.mjs
        └── references/
            ├── design-selection.md
            ├── guided-conversation.md
            ├── color-selection.md
            ├── concept-preview.md
            ├── reference-extraction.md
            ├── design-md-format.md
            ├── site-plan.md
            ├── page-design.md
            ├── site-build.md
            ├── companion-skills.md
            ├── comparison-board.md
            └── ui-review.md
```

- `SKILL.md`: mode routing, approval gates, and shared constraints
- `validate_skill.py`: dependency-free structure and documentation checks
- `guided-conversation.md`: step-by-step conversational guidance
- `design-selection.md`: real-site motifs, template research and overall format selection
- `color-selection.md`: palette research and accessibility review
- `concept-preview.md`: comparable coded UI previews
- `reference-extraction.md`: extracting and adapting reference rules
- `design-md-format.md`: the `DESIGN.md` contract and feedback protocol
- `site-plan.md`: page inventory, flows, and `SITE-PLAN.md`
- `page-design.md`: layout options and full-fidelity mockups per page type
- `site-build.md`: order and standards for moving approved mockups into code
- `companion-skills.md`: rules for using other open-source design skills as stage helpers
- `comparison-board.md`: how candidates are shown (capture, full-screen viewer, palette switcher)
- `capture.mjs`: dependency-free real-device-width full-page capture via Edge/Chrome, with pre-capture steps and resume
- `make_board.py`: builds the candidate viewer from captures and writes capture job lists
- `wait_choice.mjs`: waits for the viewers' confirm button and hands the decision over as a file (loopback only, one-time key); without it the button copies the decision text to paste into chat
- `ui-review.md`: rendered consistency and accessibility review, plus the whole-site check
- `check_site.py`: static HTML/CSS check with no dependencies (`python scripts/check_site.py <dir>`)
- `check_shots.py`: checks captures before they are sent (blank or one-colour first screens: spinners, entrance pages, black intros)
- `blind_sheet.py`: shuffles our screen with running sites, logos greyed, and writes the prompt asking a fresh agent which one an AI made
- `compose_metrics.mjs`: measures the desktop first screen's composition (photo, colour-panel and empty shares, largest type, strong block colours, text span) against several running sites and marks what falls short
- `extract_styles.mjs`: pulls the type sizes, radii, shadows, spacing and photo/box counts a reference actually uses
- `make_live_board.py`: a board that loads candidate sites live instead of capturing them, marking sites that refuse framing
- `side_by_side.py`: our page beside the reference at the same width, with a visual-layer checklist

## Context footprint

The complete skill instructions are approximately 53KB, but they are not loaded all at once. The agent reads the base `SKILL.md` and only the references needed for the active mode.

| Mode | Approximate load | Assessment |
|---|---:|---|
| Base entry point | 9.6KB | Light to moderate |
| Full guided selection | 24.0KB | Moderate |
| Concept and color selection | 19.0KB | Moderate |
| Coded preview | 12.8KB | Light to moderate |
| DESIGN.md extraction | 18.5KB | Moderate |
| Site plan | 14.2KB | Light to moderate |
| Page mockups | 18.4KB | Moderate |
| Build | 17.1KB | Moderate |
| UI review | 13.5KB | Light to moderate |

Progressive disclosure keeps the skill from consuming unnecessary project context.

## Development and validation

Check the skill name, frontmatter, required files, Codex metadata, unfinished markers, and Markdown links with:

```bash
python3 scripts/validate_skill.py
```

In development environments that include the official `skill-creator` validator, validate the skill directory directly with:

```bash
python3 /path/to/skill-creator/scripts/quick_validate.py skills/ui-design-director
```

These commands catch structural issues; behavioral testing should still cover the complete conversational flow: template research, palette selection, coded preview, and `DESIGN.md` generation.

## Wording review — `/ui-wording`

The second skill in this repository. It aligns screen copy with the words similar services already use and unifies it across every page (cart vs basket, mixed politeness levels, "Book" vs "Book now"). It extracts all visible text (`extract_ui_text.py`), finds the inconsistencies (`term_check.py`), and applies an approved term table in one pass. Install by linking `skills/ui-wording` to `~/.claude/skills/ui-wording`.
