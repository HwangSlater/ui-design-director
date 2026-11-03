# Companion skills and tools

Other open-source design skills cover parts of this workflow well. **Use them as they were designed** — their own flows, rules and checkers — instead of re-implementing a weaker copy inside this skill. This skill's job is the conversation and the record: which candidate the user chose, written in `DESIGN.md` and `SITE-PLAN.md`. A companion may produce candidates, build pages and run its checks; the user still makes each choice, and approved choices in `DESIGN.md` bind every companion (hallmark, for one, treats a root `DESIGN.md` as a locked system).

## Start-of-project check

Run this in the context gate, before any candidates are researched, so the companions shape the work from the start instead of being remembered at the end.

1. Look for each companion: a `SKILL.md` for `ui-ux-pro-max`, `hallmark`, `animate`/`review-animations` (emilkowalski) and `web-design-guidelines` in the user's skill folders (`~/.claude/skills`, `~/.agents/skills`, the project's `.claude/skills`) or in the available skills list; for impeccable run `npx --no-install impeccable --version` (prints a version only when it is already on the machine).
2. Tell the machine owner in one short table: companion · installed or not · what it adds at which step (widen candidates / name layout shapes / motion / automatic quality checks) · what installing downloads. Do not put this in front of a client or non-technical user you are designing with — tool names and "it gets better if you install" only worry them. Ask the owner directly, or proceed with what is installed and note it in the brief.
3. Ask once whether to install the missing ones, in plain words: one sentence per companion on what changes in the result ("more template and colour ideas to choose from", "smoother, checked animation"), plus your recommendation. Most users do not know these tools; a bare "install X?" gets "I don't know, skip it". Install only what is approved, and say which steps will run without the others.
   - Installing changes the machine, so consent must come from whoever owns it. When the person you are designing with is not that owner (a client, a colleague, another session acting as the user), proceed with what is installed and ask the owner separately; never treat the client's "sure" as permission to install.
4. Record the result in the concept brief. At every later gate, say which companion ran, which was skipped, and why.

## Rules for every companion

- **Optional, never silent.** Each step below works without the companion, but whether it runs is decided with the user at the start, and every skip is reported. Use one only when it is installed (it appears in the available skills list, or its `SKILL.md` exists in a skill directory) or when it runs without installation and the user approved the network access it needs.
- **Never install or download without asking.** `npx` and remote rule fetches download code or content; name what will be fetched and ask once per session. If the user declines, continue with this skill's own steps and say which check was skipped.
- **Candidates go to the user.** When a companion proposes or deals a direction, theme, palette or layout, show it as a candidate with its source; the user picks. Once picked, record it in `DESIGN.md`.
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

`Nutlope/hallmark` (MIT) exists to make generated pages look made, not generated. Use it when building layout options and mockups, not only for its vocabulary:

- Read its `SKILL.md` Floor and `references/` (layout, craft, imagery, macrostructures, gates) before drawing options; name read-surface options with its macrostructures.
- With an approved `DESIGN.md` at the root, hallmark treats it as a locked system, so its build flow can run without overriding the user's choices. Its theme deal is a candidate source when the user has not chosen a direction yet: each theme in `references/themes/` has a preview image, which makes a quick, non-technical "which feeling?" page (pick 3–4 themes whose keywords match the product). A theme chosen this way is the direction reference, alongside or instead of a live template. Before borrowing any of a theme's signature devices, check each one against the brief's dislikes and the user's reactions: a theme's per-weekday tints went straight into a page whose user had said "no rainbow colours".
- Run its linter on every layout option and mockup before showing them, and fix every `FAIL`; fix or record a reason for every `REFLEX`:

  ```bash
  node <skill-dir>/scripts/sloplint.mjs <page.html> [--render]
  ```

  It catches the generated look that the other checks miss: eyebrow labels over every heading, tracked small-caps labels, middle-dot meta strings, arrows glued to link text, dashes in copy, bare `1fr` image tracks, missing `overflow-x: clip`, stock photos. The stamp rule applies to hallmark-built pages; elsewhere note it as not applicable.

### Motion — emilkowalski/skills

`emilkowalski/skills` (MIT). Build approved motion with `animate`; check it against `review-animations` (user-invoked only: read its `SKILL.md` and apply it, or ask the user to run it). Values that pass become tokens in `DESIGN.md`.

### Site check — impeccable and Vercel guidelines

Run after `check_site.py`, as pass 4 of `ui-review.md` § Site check, together with hallmark's linter. When impeccable is installed it runs on every layout option set and every mockup set, not only at the end; a stay project that skipped it shipped exactly the look it detects.

- **impeccable** (`pbakaus/impeccable`, Apache-2.0): `npx impeccable detect --json <dir-or-url>` (exit 0 clean, 2 findings, anything else failed). Its `critique` and `audit` commands are also useful for a second opinion on a finished page.
- **Web Interface Guidelines** (`vercel-labs/web-interface-guidelines`, MIT): invoke the `web-design-guidelines` skill when installed, otherwise apply `https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md` to the page files and report in `file:line` form.

## Reporting

In the site-check report, list each companion as `ran`, `skipped (not installed)`, `skipped (user declined download)`, or `failed (reason)`, with its finding counts after mapping to this skill's tiers.
