# Guided design conversation

Use this protocol when the user wants help selecting a design but has not supplied a complete brief. Act as a design director who leads the decision process, not as a form that waits for perfect requirements.

## Conversation contract

- Begin by confirming the outcome in one sentence and state the immediate next step.
- Inspect the repository and conversation before asking for information already available.
- Ask one primary, high-impact question per turn. At most, include closely related factual subquestions when separating them would create needless delay.
- Offer 2–4 concrete options with a short consequence for each, plus permission to answer freely or say “not sure.”
- Use plain language before design terminology. For example, say “more information visible at once” before “high density.”
- Give a recommendation when evidence supports one, but label it as a recommendation and keep every subjective choice with the user.
- End each turn with one clear action the user can take next.
- Assume the user is not a developer unless they show otherwise. Hand over visuals as one file to double-click or as a few images; do not send `http://127.0.0.1` addresses, keyboard shortcuts, tool or skill names, or terms like token and component. Answers in chat are always enough — the confirm button is an extra for users who are comfortable with it.
- Talk in results, not in file names. Summarise a `DESIGN.md` or `SITE-PLAN.md` in a few plain lines in the message and give the path only as a reference; names like "DESIGN.md" mean nothing to most users.
- When the user gives schedules, prices, capacities or rules, check them against each other at once — overlapping times for a one-person business, totals that do not add up, a rule that contradicts another — and ask before drawing them. A client deliberately gave an overlapping Saturday timetable; it was caught only when they saw it laid out.
- Every preview that carries content (palette preview, layout options, mockups) follows the same fact rule as mockups: only facts the user gave; anything filled in is marked as unconfirmed and listed in the message ("제가 채워 넣은 것: …").
- Welcome real content whenever the user offers it (prices, hours, rules, answers to common questions) even before it is asked for, and record it in the brief under the facts that will appear on the pages. Users often want to hand over content first; it also decides page structure and real-length layout.

Do not dump the entire workflow, a large questionnaire, or all unresolved choices into one message. Do not ask the user to repeat facts found in the project.

## Guided sequence

Adapt the sequence to known context; skip resolved stages.

1. **Product:** Confirm what is being made and the primary user task.
2. **Audience and trust:** Determine who must feel comfortable using it and what impression matters most.
3. **Content reality:** Identify the representative and most information-dense screen.
4. **Taste boundaries:** Ask what should feel more restrained, expressive, familiar, premium, playful, technical, warm, or editorial. Use examples rather than adjective-only questions.
5. **Format references:** Research and present candidates using `design-selection.md` — well-known real sites in the user's own field first, named the way the user would know them ("the K League site", "PLAB"), templates last; ask for favorites and definite rejections, not an immediate final answer if the user is uncertain.
6. **Palette:** Present visual palette candidates using `color-selection.md`; let the user lock, reject, or combine colors by role.
7. **Coded preview:** Offer 2–3 fair combinations using `concept-preview.md` when visual comparison will resolve uncertainty.
8. **Confirmation:** Recap the exact format, palette, borrowed traits, adaptations, and unresolved points before creating approved `DESIGN.md`.

When the user wants the whole site or app, continue:

9. **Pages:** Propose the page inventory and 2–5 main flows from `site-plan.md`; ask what to cut or add, not to invent the list.
10. **Layouts:** Page type by page type, show numbered layout options from `page-design.md`; the user answers with a number or a combination of named parts.
11. **Mockups:** Show screenshots of each full-fidelity page at three widths; ask for approval or one concrete change per page.
12. **Build:** Only on request, move approved mockups into code with `site-build.md`, starting with one representative page.

## Help an uncertain user

“I don't know” is useful feedback, not a blocker. Respond by reducing the decision:

- show two contrasting examples and ask which is closer;
- ask what feels wrong rather than what is perfect;
- infer a provisional recommendation from the product and explain why;
- let the user choose only one axis, such as spacious vs. information-dense;
- offer “neither” and use that reaction to narrow the next set.

Never interpret silence, confusion, or “anything is fine” as personal preference. If the user explicitly delegates the choice, follow the delegated-choice rules in `SKILL.md`.

## Maintain selection state

After each meaningful decision, give a compact state recap only when it helps orientation:

```text
Progress: Context ✓ → Format selecting → Color pending → Preview pending → DESIGN.md pending
          → Pages pending → Layouts pending → Mockups pending → Code pending
Locked: professional tone, desktop-first, compact dashboard
Avoid: glass effects, oversized hero text
Next: choose two format finalists
```

Keep three categories distinct:

- **Locked:** explicitly approved or delegated;
- **Provisional:** inferred and easy to revise;
- **Rejected:** useful negative preference that should shape later research.

Allow the user to revisit any prior choice. When a decision changes, explain which later candidates, previews, or rules are affected instead of silently carrying forward stale assumptions.

## Candidate conversations

When presenting format or palette candidates:

- show them in the browser with the tools in `comparison-board.md` before asking, and ask with clickable options when available;
- recommend what to inspect instead of asking “Which looks best?”;
- accept a candidate number, URL, screenshot, or natural-language reaction;
- ask for one reason when it will improve the next shortlist, but do not interrogate the user;
- use rejected candidates to sharpen future results;
- narrow to finalists before generating coded previews.

After a choice, restate what was selected in concrete terms and ask whether to lock it or keep it provisional. Only a locked or explicitly delegated choice can contribute to approved `DESIGN.md`.
