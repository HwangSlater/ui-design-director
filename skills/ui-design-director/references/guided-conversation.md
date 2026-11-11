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
- **Ask for the page's facts before the main page.** Once, after the palette and before building, ask in one message for what the main page will show: the name (a working name is fine), prices, hours and days off, where people book or call, and the area. Fill only what the client could not give with sample values, list them at handover. Every fact the client gave goes on the page as given; if two facts look inconsistent, ask, but keep both on the page until the client changes them — a daily limit of seven was dropped while a question about it went unanswered (nail salon 43rd). A mockup titled 「가게 이름」 with a sample bath price that contradicted the client's real one (dog groomer 21st) came from never asking; `preflight.py` flags `placeholder-name`.
- Welcome real content whenever the user offers it (prices, hours, rules, answers to common questions), even before it is asked for, and record it in the brief under the facts that will appear on the pages.
- **Photos are one yes/no question:** 「사진이 있으세요?」. If yes, ask for them and whose they are. If no (or 「아직 몰라요」), do not ask more and offer no image-strategy options: sample text, searched sample photos (`sample_photos.py`) and letter marks for logos and team marks apply as defaults ([sample-photos.md](sample-photos.md) § Ask once). Logos stay letter marks unless the client asks for real ones.

Do not dump the entire workflow, a large questionnaire, or all unresolved choices into one message.

**Read the dislikes back.** After writing `concept-brief.md`, repeat the client's likes and dislikes in one line each and ask them to correct it ("싫은 것: 큰 서점 느낌, 꾸민 감성 카페 — 맞나요?").

## Site type

`concept-brief.md` carries one line `사이트 꼴: 여러 쪽` or `사이트 꼴: 한 쪽 홍보·모집`; `stage.py` does not count the brief as done without it. Infer it from the main job, do not ask a separate question: a shop, service, business, studio, records or information site is 여러 쪽 (each menu item is its own page; the main page only previews, like the base's main page); one event, one recruitment drive or one campaign is 한 쪽 홍보·모집 (one long page, menu links jump down the page). Say it in the same read-back as the dislikes, in the client's words (「메뉴마다 따로 페이지가 있는 가게 홈페이지로 만들어요 — 맞나요?」). Ask outright only when the main job fits both (a shop that mainly wants to advertise one opening event).

## At each gate

Follow the SKILL.md workflow and `site-plan.md` § Gates (whole site); skip resolved ones. What to ask the user:

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
