# Composition numbers and the blind judge

Composition numbers run on every first screen and page type before the client sees it. The blind judge runs once, only when the user asks for it; it is an AI agent, not people — say so whenever you report its number.

## Composition numbers

1. List each shortlisted home's sections top to bottom with their fill (photo, card grid, text, band, footer) at 390 and 1280.
2. Build from the order and fill they share (`skeleton.mjs` 「위에서부터 배치」), customers' width first.
3. Run `node ${CLAUDE_SKILL_DIR}/scripts/compose_metrics.mjs <out.md> --width 1280 --ours ours ours=<file url> ref1=<url> ref2=<url> …` and rework until no line reads 「미달」. Record the table next to the mockup.
4. Check list and menu pages against the references' page of the same type; text-first menu options measured 2–36% photo against 55–78%.
5. Re-measure after adding any band or strip.

## Blind sheet (only when the user asks)

1. Build it with `python ${CLAUDE_SKILL_DIR}/scripts/blind_sheet.py <dir> 우리=<ours.jpg> ref=<ref.jpg> …` (same crop, logos greyed, shuffled, answer key kept apart) and give its `prompt.txt` to one fresh agent, once (SKILL.md § Budget exception).
2. Give every image its own logo box (`이름=<path>@x,y,w,h`), sized to the logo only; an oversized box that hides a menu is a tell.
3. Put exactly one of our screens in a sheet; two variants of one client give each other away.
4. Controls: same country and language, lesser-known running sites mixed with famous ones, none whose device you borrowed.
5. When the field's businesses rarely run their own site, use the platform pages they do run (for small Korean shops, the Naver Place listing and Instagram profile) as the running reference for operating traces (map, hours, notice, business info).

## Fair sheet (judge's copy only)

Only when the blind judge runs. Capture the judge's copy with `"judge": true` on the `capture.mjs` job; it prints 「판정 흔적」 for anything that still gives the page away (○○, 견본). Clear every one by hand before the sheet is built:

1. Replace leftover 「○○○」 and invented street names with plausible sample values.
2. Any empty box or 「… 자리」 slot left on the page breaks build-rules.md § Content and samples: fix it in the mockup itself (sample photo, or drop the part), not only in the judge's copy.
3. Never send this copy to the client.

## Reading the verdict

1. Read our score against the real controls in the same sheet, not against zero; one run is noisy, so treat it as a list of tells, not a grade.
2. The judge reads operating residue as real: the client's own photos (sign, street, price cards), owner-made banners, platform parts (Cafe24 login, Kakao chat button), leftover template text.
3. It reads completeness as AI: live status as app UI (dots, badges), every line in one warm voice, a key-value rules table, warm brown with one orange button, every card filled to one template, one mark before every heading and an arrow after every link, the accent on every highlight.
4. Above 70% 「AI-made」 on ours is a fail: fix the fixable design tells it names, then report the number with its reasons. Do not run it again unless the user asks. Never imitate mess to win the judge.
5. Content you cannot design away sets a floor (sample photos, a concept no small business runs, one tidy voice, cover images the client banned). Record such a gap instead of faking it.
