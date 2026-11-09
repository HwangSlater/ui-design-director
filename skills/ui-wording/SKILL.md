---
name: ui-wording
description: Aligns screen copy and terms with the words similar services already use and makes them one across the whole site or app — finds things called by several names (카트/장바구니, 체험 수업/무료 체험), mixed tone (해요체/합니다체), inconsistent button forms and coined words the trade does not use, builds a term table, and after approval applies it everywhere at once. Use when the user says 「/ui-wording」, 「문구 검토」, 「용어 통일」, 「말 맞춰 줘」 or 「업계 용어로」, or as the last check before showing a mockup, site or app.
---

# UI Wording

Build a term table from the words similar services already use, then apply it everywhere. Never coin new words. `${CLAUDE_SKILL_DIR}` is this skill's folder (outside Claude Code: the folder holding this file); Python 3.10+.

## Steps

1. **Service type.** Read it from the repository and brief (shopping, booking, academy or lessons, workshop or class, marketplace, app settings …); list all that apply. If unknown, ask once.
2. **Extract every string.**
   ```bash
   python "${CLAUDE_SKILL_DIR}/scripts/extract_ui_text.py" <folder> --out ui-text.json
   ```
   Pass the mockup folder and the code folder together to see whether both use the same words.
3. **Find the drift.**
   ```bash
   python "${CLAUDE_SKILL_DIR}/scripts/term_check.py" ui-text.json --suggest
   ```
4. **Term table.** Start from that service type's conventions in [references/conventions-ko.md](references/conventions-ko.md). For any word you are unsure of — or a service type the file has no table for (e.g. marketplace) — **open 2–3 real services of the same type** and write which ones in 「why」. Words the user already chose (`DESIGN.md` voice and terms, the user's own phrasing) override convention. Save the table as `wording.json` (format in the header of `term_check.py`).
5. **Show the user.** A table of 「쓰인 말 → 바꿀 말 → 이유 → 몇 곳」 plus the tone and button-form decisions, briefly. For a non-developer, describe on-screen words, not file names. Change nothing before approval.
6. **Apply all at once.**
   ```bash
   python "${CLAUDE_SKILL_DIR}/scripts/term_check.py" ui-text.json --glossary wording.json --apply
   ```
   Then rerun steps 2 and 3 to confirm nothing is left. Fix by hand what the script cannot (tone, button form).
7. **Record.** Copy the approved table into the project's design rules (`DESIGN.md` § Voice and terminology if it exists, otherwise `WORDING.md`) so the next screen uses the same words.

## Rules

- The standard is the words customers of that trade already know, not the words we like.
- One name per thing — in intro text, buttons, questions, notification messages and error messages alike.
- One tone across the product (see conventions-ko.md § Tone for which).
- One button form; the same action has the same label on every screen.
- One way to write numbers, times and amounts (do not mix 「14만 원」 and 「140,000원」, or 「오후 2시」 and 「14:00」).
- Do not say "unified" until a fresh extraction shows zero remaining.
