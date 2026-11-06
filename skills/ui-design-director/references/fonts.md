# Fonts

Font candidates come from evidence, never from memory: from memory a model offers the same defaults every time (Pretendard, Noto Sans KR, Wanted Sans, SUIT — rounds 10 and its replay both did). Read this before the palette step and before any page.

## Contents
- The data
- Choosing candidates
- Never these
- Checks

## The data

`assets/fonts/fonts.json` holds 835 free Korean fonts a website may embed, measured 2026-11-06:
- the free fonts the 186 most-visited Korean sites actually render (headless measurement of headings, body, menus, buttons and loaded `@font-face`), with how many sites use each;
- every font a company, brand or public body published on 눈누 whose licence allows commercial use and web embedding, with its conditions (no modification, no resale, no BI·CI·logo use, credit, banned trades) and licence source.

Fonts that need separate approval for web use (KoPub, some city fonts) are not in it. Never read the file; query it with `fonts.py`.

## Choosing candidates

1. Measure the base's type character from `formats/추출-1280.json` and the snapshot: gothic or serif or hand, width, stroke contrast, heading and body weights.
2. `python ${CLAUDE_SKILL_DIR}/scripts/fonts.py pick --style <고딕|명조|바탕|손글씨|제목용|장식체> --top 8` — candidates matching that character, ordered by sites that use them, then 눈누 views. Ask for heading and body separately when the base pairs two faces.
3. Offer 3–4 pairs on the palette page. For each say where it comes from (「상위 사이트 3곳이 씀」, 「롯데마트 공개」) and its conditions in the font's `license` and `note` fields. A condition that clashes with the project (a game company and 쿠키런, a logo set in a no-BI·CI font) disqualifies the font.
4. When the base itself uses a font on the list below, replace it with the closest-character font from step 2 and say so; 「바탕 그대로」 is not a reason to keep it.
5. A font the client already uses stays: record it in `concept-brief.md` as `의뢰인 글꼴: <name>`.

## Never these

`assets/fonts/ai-fonts.json` lists the faces models choose unprompted (the nine long-banned ones plus every face that appeared in earlier mockups). `fonts.py pick` leaves them out; `fonts.py check`, `preflight.py` and the plugin hook refuse them. Add a face there when a mockup shows a new default.

## Checks

- `python ${CLAUDE_SKILL_DIR}/scripts/fonts.py check palette mockups` before sending a palette page or a page; exit 1 lists each file and face.
- Rebuild the data: `scripts/font-research/how-to-rerun.md` in the repository (measurement, 눈누 collection, `merge.py`).
