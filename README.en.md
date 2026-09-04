# UI Design Director

[한국어](README.md)

`ui-design-director` is a Codex skill for establishing the overall UI concept of a project. It researches real templates and 3–4 color palettes, helps the user choose the visual format and color direction independently, compares finalists through small coded previews, and turns approved decisions into a reusable `DESIGN.md`.

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

## Workflow

```text
Understand the product context
→ Research design-format candidates
→ Research 3–4 color palette candidates
→ Let the user choose format and color independently
→ Compare finalist combinations in coded UI previews
→ Document the approved decisions in DESIGN.md
→ Implement and review a representative screen
→ Propagate approved rules across the project
```

The skill does not finalize the design system or production UI before the user makes a choice. It favors one primary reference and only borrows narrowly defined traits—such as typography hierarchy or dashboard density—from secondary references.

## Installation

### Easiest method: install from a GitHub URL

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

In the current development environment, it is linked at:

```text
~/.codex/skills/ui-design-director
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
        └── references/
            ├── design-selection.md
            ├── guided-conversation.md
            ├── color-selection.md
            ├── concept-preview.md
            ├── reference-extraction.md
            ├── design-md-format.md
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
- `ui-review.md`: rendered consistency and accessibility review

## Context footprint

The complete skill instructions are approximately 35.4KB, but they are not loaded all at once. Codex reads the base `SKILL.md` and only the references needed for the active mode.

| Mode | Approximate load | Assessment |
|---|---:|---|
| Base entry point | 7.4KB | Light to moderate |
| Full guided selection | 21.3KB | Moderate |
| Concept and color selection | 17.0KB | Moderate |
| Coded preview | 10.8KB | Light to moderate |
| DESIGN.md extraction | 16.4KB | Moderate |
| UI review | 9.2KB | Light |

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
