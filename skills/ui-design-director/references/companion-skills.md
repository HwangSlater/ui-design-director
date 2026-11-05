# Companion skills and tools

Use other open-source design skills as they were designed — their own flows, rules and checkers — instead of re-implementing a weaker copy here. This skill keeps the conversation and the record (`DESIGN.md`, `SITE-PLAN.md`); a companion may produce candidates, build pages and run checks, but the user makes each choice and approved choices in `DESIGN.md` bind every companion.

## Start-of-project check

Run this in the context gate, before any candidates are researched.

1. Look for each companion: a `SKILL.md` for `ui-ux-pro-max`, `hallmark`, `animate`/`review-animations` (emilkowalski) and `web-design-guidelines` in the user's skill folders (`~/.claude/skills`, `~/.agents/skills`, the project's `.claude/skills`) or in the available skills list; for impeccable run `npx --no-install impeccable --version` (prints a version only when it is already on the machine).
2. Ask the machine owner once, in one short table: companion · installed or not · what it adds at which step (widen candidates / name layout shapes / motion / automatic quality checks) · what installing downloads — with one plain sentence per companion on what changes in the result ("more template and colour ideas to choose from") and your recommendation. Installing changes the machine, so consent comes only from its owner: when you are designing with someone else (a client, a colleague, another session acting as the user), do not show them this table, never treat their "sure" as permission, proceed with what is installed and ask the owner separately.
3. Install only what is approved, say which steps will run without the others, and record the result in the concept brief.

## Rules for every companion

- **Optional, never silent.** Each step works without the companion; use one only when installed, or when it runs without installation and the owner approved the network access. Report every skip (§ Reporting).
- **Never install or download without asking.** `npx` and remote rule fetches download code or content; name what will be fetched and ask once per session. If declined, continue with this skill's own steps and say which check was skipped.
- **One record of decisions.** A companion may write its own working files (logs, `tokens.css`, its stamp, snapshots). It must not overwrite `DESIGN.md` or `SITE-PLAN.md`; when it produces a design system, fold the user-approved parts into `DESIGN.md` instead of keeping two competing ones.
- **Verify before reporting.** Re-check every companion finding against the current files and map it to this skill's tiers (`ui-review.md` § Site check): a confirmed accessibility failure is `FLOOR`; a value bypassing an approved token is `DRIFT`; a taste rule that `DESIGN.md` does not adopt is `NOTE`. A companion's house style does not outrank the user's approved concept.
- **Credit the source.** When a candidate or rule came from a companion, say so next to it. Do not copy a companion's text into project files; link or name it instead.

## By stage

### Concept: directions, palettes, type — ui-ux-pro-max

`nextlevelbuilder/ui-ux-pro-max-skill` (MIT). Run its design-system reasoning for the product and show the result as one of the candidate directions; use its domain searches to widen styles, palettes, font pairings and UX rules:

```bash
python -I <skill-dir>/scripts/search.py "<product, industry, mood>" --design-system -p "<project>"
python -I <skill-dir>/scripts/search.py "<terms>" --domain style|color|typography|product|ux -n 5
```

Database entries are ideas: a format candidate still needs a live template or site that was opened and verified (`design-selection.md`), and every palette goes through the contrast calculation (`color-selection.md`). Its typography data is mostly Latin; for Korean pages pair its mood with Korean fonts. Skip `--persist` unless the user wants its design-system folder; `DESIGN.md` stays the record.

### Layout, pages and craft — hallmark

`Nutlope/hallmark` (MIT) exists to make generated pages look made, not generated. Use it when building layout options and mockups:

- Once per project, before drawing options, read its `SKILL.md` Floor and its layout and macrostructures references; name read-surface options with its macrostructures.
- With an approved `DESIGN.md` at the root, hallmark treats it as a locked system, so its build flow can run without overriding the user's choices. Only when the user cannot pick a direction from the shortlisted sites, its theme deal is a candidate source: each theme in `references/themes/` has a preview image, which makes a quick "which feeling?" page (3–4 themes whose keywords match the product). Check each of a theme's signature devices against the brief's dislikes before borrowing it.
- Run its linter on every layout option and mockup before showing them, and fix every `FAIL`; fix or record a reason for every `REFLEX`. The stamp rule applies only to hallmark-built pages.

  ```bash
  node <skill-dir>/scripts/sloplint.mjs <page.html> [--render]
  ```

### Motion — emilkowalski/skills

`emilkowalski/skills` (MIT). Build approved motion with `animate`; check it against `review-animations` (user-invoked only: read its `SKILL.md` and apply it, or ask the user to run it). Values that pass become tokens in `DESIGN.md`.

### Site check — impeccable and Vercel guidelines

Run after `check_site.py`, as pass 4 of `ui-review.md` § Site check, together with hallmark's linter. When impeccable is installed it runs on every layout option set and every mockup set, not only at the end.

- **impeccable** (`pbakaus/impeccable`, Apache-2.0): `npx impeccable detect --json <dir-or-url>` (exit 0 clean, 2 findings, anything else failed). Run its `critique` and `audit` only when the user asks.
- **Web Interface Guidelines** (`vercel-labs/web-interface-guidelines`, MIT): invoke the `web-design-guidelines` skill when installed, otherwise (after asking, as a remote fetch) apply `https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md` to the page files and report in `file:line` form.

## Reporting

In the site-check report (not at every gate), list each companion as `ran`, `skipped (not installed)`, `skipped (user declined download)`, or `failed (reason)`, with its finding counts after mapping to this skill's tiers.
