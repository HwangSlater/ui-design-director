# Guided design conversation

Use this when the user wants help choosing a design but has not given a complete brief.

## Conversation contract

- Begin by confirming the outcome in one sentence and state the immediate next step.
- Inspect the repository and conversation before asking for information already available; never ask the user to repeat it.
- Ask one primary, high-impact question per turn; add closely related factual subquestions only when separating them would cause needless delay.
- Offer 2–4 concrete options with a short consequence for each, plus permission to answer freely or say “not sure.” Give a recommendation when evidence supports one, labelled as such.
- Use plain language before design terminology (“more information visible at once” before “high density”).
- Assume the user is not a developer. Keep tool names, file names, ports, shortcuts, measuring jargon and terms like token or component out of anything the client reads — messages, the brief, table headers in `SITE-PLAN.md`. Give the one address or file the tool prints without explaining it; say what a check found in the client's words (「실제 빵집 메뉴 페이지만큼 사진이 들어가 있어요」) and keep the numbers in your notes; summarise `DESIGN.md` or `SITE-PLAN.md` in a few plain lines, with the path only as a reference. Answers in chat are always enough — the 확정 button is an extra.
- When the user gives schedules, prices, capacities or rules, check them against each other at once (overlapping times for a one-person business, totals that do not add up, rules that contradict) and ask before drawing them.
- Every preview that carries content (palette preview, layout options, mockups) uses only facts the user gave; anything filled in is marked unconfirmed and listed in the message ("제가 채워 넣은 것: …"). A reference site's claims are not the client's facts: borrow its order and kinds of content, never its sentences.
- Welcome real content whenever the user offers it (prices, hours, rules, answers to common questions), even before it is asked for, and record it in the brief under the facts that will appear on the pages.

Do not dump the entire workflow, a large questionnaire, or all unresolved choices into one message.

## At each gate

Follow SKILL § Gates and skip resolved ones. What to ask the user:

- **Format:** name sites the way the user knows them ("the K League site", "PLAB"); ask for favourites and definite rejections, not an immediate final answer if the user is uncertain.
- **Palette:** let the user lock, reject or combine colours by role.
- **Pages:** propose the page inventory and 2–5 main flows from `site-plan.md`; ask what to cut or add, not to invent the list.
- **Layouts:** the user answers with a number or a combination of named parts.
- **Mockups:** ask for approval or one concrete change per page.

## Help an uncertain user

“I don't know” is useful feedback. Show two contrasting examples and ask which is closer, ask what feels wrong rather than what is perfect, or offer “neither” and use that reaction to narrow the next set. Never treat silence, confusion or “anything is fine” as a preference.

## Maintain selection state

After a meaningful decision, give a compact recap in the client's words only when it helps orientation:

```text
진행: 방향 정리 ✓ → 뼈대 고르는 중 → 색 · 미리 보기 · 디자인 규칙 · 쪽 목록 · 배치 · 완성 시안 · 만들기
정한 것: 차분한 말투, 컴퓨터 화면 먼저, 정보 많이 보이게
빼기로 한 것: 유리 효과, 너무 큰 첫 화면 글자
다음: 뼈대 후보 두 개로 줄이기
```

Keep three categories distinct: **locked** (approved or delegated), **provisional** (inferred, easy to revise), **rejected** (a negative preference that shapes later research). Only a locked or delegated choice goes into approved `DESIGN.md`; a 확정 or a clear chat answer locks it — restate it in one line and continue without asking again.

Allow the user to revisit any prior choice. When a decision changes, say which later candidates, previews or rules are affected instead of silently carrying stale assumptions forward.

## Candidate conversations

- Recommend what to inspect instead of asking “Which looks best?”
- Accept a candidate number, URL, screenshot, or natural-language reaction.
- Ask for one reason when it will improve the next shortlist, but do not interrogate the user; use rejected candidates to sharpen future results.
