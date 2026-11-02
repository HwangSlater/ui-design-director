# Companion skills and tools

Other open-source design skills cover parts of this workflow well. Use them as **evidence and checks inside this skill's gates**, never as a second workflow. This skill keeps ownership of every user decision and of `DESIGN.md` and `SITE-PLAN.md`.

## Start-of-project check

Run this in the context gate, before any candidates are researched, so the companions shape the work from the start instead of being remembered at the end.

1. Look for each companion: a `SKILL.md` for `ui-ux-pro-max`, `hallmark`, `animate`/`review-animations` (emilkowalski) and `web-design-guidelines` in the user's skill folders (`~/.claude/skills`, `~/.agents/skills`, the project's `.claude/skills`) or in the available skills list; for impeccable run `npx --no-install impeccable --version` (prints a version only when it is already on the machine).
2. Show the user one short table: companion · installed or not · what it adds at which step (widen candidates / name layout shapes / motion / automatic quality checks) · what installing downloads.
3. Ask once whether to install the missing ones. Install only what the user approves, and say which steps will run without the others.
4. Record the result in the concept brief. At every later gate, say which companion ran, which was skipped, and why.

## Rules for every companion

- **Optional, never silent.** Each step below works without the companion, but whether it runs is decided with the user at the start, and every skip is reported. Use one only when it is installed (it appears in the available skills list, or its `SKILL.md` exists in a skill directory) or when it runs without installation and the user approved the network access it needs.
- **Never install or download without asking.** `npx` and remote rule fetches download code or content; name what will be fetched and ask once per session. If the user declines, continue with this skill's own steps and say which check was skipped.
- **Inputs, not decisions.** A companion's suggestion is a candidate for the user to choose, with its source named. Do not let a companion pick the theme, palette, or layout, or roll dice on the user's behalf.
- **Our files only.** Do not let a companion create or overwrite `DESIGN.md`, `PRODUCT.md`, design-system folders, theme scaffolds, or logs. Use read-only modes; when a mode writes files, skip it.
- **Verify before reporting.** Re-check every companion finding against the current files and map it to this skill's tiers (`ui-review.md` § Site check): a confirmed accessibility failure is `FLOOR`; a value bypassing an approved token is `DRIFT`; a taste rule that `DESIGN.md` does not adopt is `NOTE`. A companion's house style does not outrank the user's approved concept.
- **Credit the source.** When a candidate or rule came from a companion, say so next to it. Do not copy a companion's text into project files; link or name it instead.

## By stage

### Format, palette, and type candidates — ui-ux-pro-max

`nextlevelbuilder/ui-ux-pro-max-skill` (MIT) holds searchable style, colour, typography, and product-pattern data. Use its search script in read-only domain mode to widen a shortlist:

```bash
python <skill-dir>/scripts/search.py "<2–5 terms: product, industry, mood>" --domain style|color|typography|product -n 5
```

- Treat results as **ideas, not inspected candidates.** They are database entries, not live templates; a format candidate still needs a real template or showcase that was opened and verified (`design-selection.md`).
- Palette results enter the palette shortlist labelled with their source and go through the same contrast calculation as any other palette (`color-selection.md`).
- Do not use `--persist` or `--output-dir`: they write a design system into the project and would compete with `DESIGN.md`.

### Layout options — hallmark (vocabulary only)

`Nutlope/hallmark` (MIT) names landing-page shapes in `references/macrostructures.md`. When it is installed, read that index to name and contrast the 2–3 layout options of a read-surface page type (`page-design.md` § 1). Derive the options from the page's job first; use the names to make them clearly different and easy to talk about.

Do not run its theme deal, scaffold, photo draw, or build flow; they decide the visual world, which this skill has already settled with the user. Its own description says not to run it on an existing design unless the user names it.

### Motion in mockups and code — emilkowalski/skills

`emilkowalski/skills` (MIT) sets the bar for animation choices: whether to animate, which property, curve, duration, interruption, and exit.

- When adding motion that `DESIGN.md` approved, use `animate` to build it.
- To check motion, read the installed `review-animations/SKILL.md` and apply its rules to the motion code. That skill is marked as user-invoked only, so it cannot be called automatically; the user may also run it themselves.
- Motion values that pass review become tokens in `DESIGN.md` (durations, curves), not per-component numbers.

### Site check — impeccable detector and Vercel guidelines

Run these after `check_site.py` passes, as the fourth pass of `ui-review.md` § Site check.

- **impeccable detector** (`pbakaus/impeccable`, Apache-2.0): deterministic rules for generic-looking UI and quality problems. Runs without installing the skill, but `npx` downloads the package:

  ```bash
  npx impeccable detect --json <mockup-or-build-dir>
  npx impeccable detect --json <local-url>     # rendered page, uses installed Chrome or Edge
  ```

  Exit code 0 means no findings and 2 means findings were reported; treat any other code or empty output as a failed run. Use only the detector. The skill's `critique` and `audit` commands run their own context setup around `PRODUCT.md` and save snapshots; use them only when the user asks for an impeccable review by name.

- **Web Interface Guidelines** (`vercel-labs/web-interface-guidelines`, MIT): the rule list behind Vercel's `web-design-guidelines` skill. Invoke that skill when installed; otherwise fetch `https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md` with the user's approval and apply its rules to the page files. Report in `file:line` form.

### Not used inside this workflow

These have their own end-to-end flow that would take decisions away from the user or write competing design files. Mention them only if the user asks:

- hallmark build, redesign, and theme flows;
- taste-skill (`Leonxlnx/taste-skill`) art-direction flow;
- impeccable `init`, `document`, `extract`, `shape`, and the refine/enhance commands that edit code.

## Reporting

In the site-check report, list each companion as `ran`, `skipped (not installed)`, `skipped (user declined download)`, or `failed (reason)`, with its finding counts after mapping to this skill's tiers.
