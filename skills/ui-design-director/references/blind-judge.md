# Composition numbers and the blind judge

Every first screen and page type passes both gates before the client sees it, after the layout rules in [page-design.md](page-design.md). The judge is an AI agent, not people; say so whenever you report its numbers.

## Composition numbers

1. List each shortlisted home's sections top to bottom with their fill (photo, card grid, text, band, footer) at 390 and 1280.
2. Build from the order and fill they share (`skeleton.mjs` 「위에서부터 배치」), customers' width first. Never trace one site.
3. Run `node scripts/compose_metrics.mjs <out.md> --width 1280 --ours ours ours=<file url> ref1=<url> ref2=<url> …` and rework until no line reads 「미달」. Record the table next to the mockup.
4. Check list and menu pages against the references' page of the same type; text-first menu options measured 2–36% photo against 55–78%.
5. Re-measure after adding any band or strip.

## Blind sheet

1. Build it with `python scripts/blind_sheet.py <dir> 우리=<ours.jpg> ref=<ref.jpg> …` (same crop, logos greyed, shuffled, answer key kept apart) and give its `prompt.txt` to a fresh agent.
2. Give every image its own logo box (`이름=<path>@x,y,w,h`), sized to the logo only; oversized boxes hid a menu and judges named it.
3. Put exactly one of our screens in a sheet; two variants of one client give each other away.
4. Controls: same country and language, lesser-known running sites mixed with famous ones, none whose device you borrowed.
5. For small Korean shops, which rarely run a homepage, the running reference for operating traces (map, hours, notice, Instagram, business info) is the Naver Place listing and Instagram profile.
6. Above 70% 「AI-made」 on ours sends it back while the judge still names fixable tells.

## Fair sheet (judge's copy only)

1. Hide 「견본」 marks, `.sample` and prototype notes (`capture.mjs` step `{"hide": ".sample, .proto"}`, or a `clean` body class).
2. Replace 「0000」 numbers (「02-336-0000」) and 「○○○」 with plausible sample values, and invented street names likewise.
3. Fill or remove hatched photo and map slots (「가게 앞 사진 자리」, 「네이버 지도 자리」); a photo grid gets a sample in each slot. Left in, they were the judge's decisive tell.
4. Never hand this copy to the client.

## Calibrating

1. Each time you change the controls or masks, put one real site of the field in a sheet as 「우리」 with its name masked. Above 30% means the controls or masks are wrong, not your page.
2. Read our score against the real controls in the same sheet, not against zero. When ours is level with a real site, put further work into the client's score, not the judge's.
3. Run two judges on different shuffles and average. One round is noise (an unchanged page scored 80, 70, 80), so change one thing per round and read a trend over two or three rounds.

## Reading the verdict

1. The judge reads operating residue as real: the shop's own photos (sign, street, price cards), owner-made banners, platform parts (Cafe24 login, Kakao chat button), leftover template text.
2. It reads completeness as AI: live status as app UI (dots, badges), every line in one warm voice, a key-value rules table, warm brown with one orange button, every card filled to one template, one mark before every heading and an arrow after every link, the accent on every highlight.
3. Fix what is wrong, then stop and report. Never imitate mess to win the judge.
4. Real material moves the client more than the judge.

## The floor

1. Content you cannot design away sets a floor: sample photos, a concept no small shop runs, one tidy voice, publishers' book covers the owner banned. Record such a gap instead of faking it.
2. Ask for the owner's photos at the brief (storefront with sign, counter, hands at work, the day's shelf, interior) and say early that sample photos cap the score.
3. When two rounds no longer move it and the named tells are content-level, stop looping, report the number with reasons, and gate on the design score (at or above the controls' median).
4. People have the last word: show the client their phone first screen beside two or three running sites of the same field and country and ask for a score out of 10 each.
