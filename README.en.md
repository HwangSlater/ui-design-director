# UI Design Director

[한국어](README.md)

`ui-design-director` is a skill for establishing the overall UI concept of a project and carrying it through a complete website or web app, working in both Codex and Claude Code. It researches real templates and 3–4 color palettes, helps the user choose the visual format and color direction independently, compares finalists through small coded previews, and turns approved decisions into a reusable `DESIGN.md`. It then plans the pages, gets a layout and a full-fidelity mockup approved for each page type, and only then moves them into production code.

The user does not need to know design terminology or provide a complete brief. Starting with “I want to choose a design” makes the skill ask one consequential question at a time, offer concrete choices and recommendations, and guide the user to the next decision.

Its purpose is to replace vague requests such as “make it feel like Linear” with explicit rules for color, typography, spacing, layout, components, interaction states, and accessibility.

## Features

- Research real template and design-system candidates from sources matched to the product archetype: marketing site, dashboard, editing tool, form workflow, or content reader
- Establish each candidate and recommended dependency's licence from its published text, and rule out commercially unusable options before taste enters
- Select the overall design format and color palette independently
- Compare 3–4 color combinations from sources such as Coolors, Color Hunt, Adobe Color, and Huemint
- Explain semantic UI roles and distribution for each palette, with contrast ratios computed from hex values rather than eyeballed
- Compare 2–3 finalists using the same content in small coded UI previews, self-checked for overflow, wrapping, and states before they are shown
- Convert the approved design language into project-root `DESIGN.md`
- Fix on-screen wording and terminology as rules pitched at the audience's expertise
- Guide later implementation toward shared tokens and components
- Accumulate feedback as durable design rules instead of one-off CSS
- Review responsive behavior, focus, error, loading, empty states, and accessibility
- Guide vague requests through a step-by-step design conversation
- Plan the whole site in `SITE-PLAN.md`: page inventory, main flows, navigation, and per-page status
- Treat read surfaces (marketing, docs) and work surfaces (dashboards, forms) by their own rules
- Offer 2–3 numbered greyscale layout options per page type, then build full-fidelity mockups from the chosen one
- Share one token and component stylesheet across mockups so approved pages transfer into code intact
- Run a dependency-free static check (`check_site.py`) that reports accessibility floor, token drift, and common generic patterns in three tiers
- Check rendering at three widths and get a review from a reviewer that never saw the builder's reasoning
- Compare candidates in a full-screen browser viewer, not a table of links: key pages captured at desktop and real phone width (`capture.mjs`) shown in identical frames (`make_board.py`)
- Choose palettes by clicking them on a live preview of the chosen format (`palette-switcher.js`), with contrast computed automatically

## Workflow

```text
Understand the product context
→ Research design-format candidates
→ Research 3–4 color palette candidates
→ Let the user choose format and color independently
→ Compare finalist combinations in coded UI previews
→ Document the approved decisions in DESIGN.md
→ Plan pages and flows in SITE-PLAN.md
→ Choose a layout option per page type
→ Approve full-fidelity mockups per page (three widths, every state)
→ Build one representative page in code, then the rest
→ Static check, render pass, and fresh reviewer
```

The skill does not finalize the design system or production UI before the user makes a choice. It favors one primary reference and only borrows narrowly defined traits—such as typography hierarchy or dashboard density—from secondary references.

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

### Claude Code: link it into the personal skills directory

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
- Invented testimonials, customer logos, or figures are never presented as real; missing material stays a labelled empty slot.

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
        │   ├── board.css · board.js
        │   └── palette-switcher.css · palette-switcher.js
        ├── scripts/
        │   ├── check_site.py
        │   ├── capture.mjs
        │   └── make_board.py
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
- `design-selection.md`: template research and overall format selection
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
- `ui-review.md`: rendered consistency and accessibility review, plus the whole-site check
- `check_site.py`: static HTML/CSS check with no dependencies (`python scripts/check_site.py <dir>`)

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
