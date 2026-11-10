# Finding sample photos

Use this when the client's own photos are missing. Placement rules (no empty photo boxes, the one 「견본」 line, drop a part rather than leave a slot): [build-rules.md](build-rules.md) § Content and samples.

## Ask once, then use the defaults

The brief asks one yes/no question: 「사진이 있으세요?」. Never a multiple choice about an image strategy (「사진 없이 약칭·팀색만 / 데이터 업체 계약 / 아직 모름」) and never a follow-up about it. If the answer is no, or the client does not know, use these defaults without asking more:

| Missing | Default |
|---|---|
| Text (intro, prices, hours) | Short neutral sample text of the right length ([build-rules.md](build-rules.md) § Content and samples) |
| Photos | Licence-checked searched photos from `sample_photos.py`, marked 견본, credited in the footer line |
| Logos, team marks, brand art | Letter marks: initials (or the short name) on the brand colour, in our type — drawn in CSS, never downloaded |

Use real logos or team marks only when the client explicitly asks for them, and then only as 견본 with the rights notice in [build-rules.md](build-rules.md) § Content and samples. Never fetch them on your own from a team, league or sports-site CDN.

## What to look for

- Match the product and the client's customers' setting (a Korean apartment, not a Western bathroom).
- **A local client gets local photos.** When the client is a local Korean business or event (「망원동 골목」 flea market, a 동네 dentist), pass `--place "<place words in English and Korean>"` (e.g. `--place "Seoul Korea 서울 망원동"`). On the contact sheet drop every photo whose signs, buildings or setting read as another country — a Berlin street market with a 「KÜCHE」 sign became a Seoul flea market's hero (flea market 14th). If nothing local is found, use a close-up without signs or buildings, or drop the part, and say so in the 「견본」 line (「동네 사진은 못 찾아 다른 곳 사진이에요」).
- Before/after samples show the same room from the same angle; otherwise drop the pair and ask the client.
- Prefer everyday, unstaged photos (people, places, mess) over evenly graded stock, which a blind judge read as AI.
- Judge candidates from a contact sheet, not their titles; check the subject matches what the client has and that every photo loaded.
- Credit author and licence for each photo; list them in the 「견본」 line.

## Where to search, in this order

1. `python ${CLAUDE_SKILL_DIR}/scripts/sample_photos.py "<subject in English>" --n 8 --out <project>/mockups/img/sample [--orient landscape|portrait|square] [--no-people] [--place "Seoul Korea 서울 망원동"]`. It searches the Wikimedia Commons and Openverse APIs, keeps CC0, public domain, CC BY and CC BY-SA only, skips svg files and titles naming a logo, emblem, crest or wordmark, and writes `sample-01.jpg …`, `credits.json` and `contact.jpg`. Open only `contact.jpg` to choose; paste the 「견본 줄」 it prints into the footer. `--no-people` only drops titles and descriptions that say portrait, headshot or selfie — it cannot see faces or names, so check the contact sheet and crop faces the client has not cleared. `--place` searches the subject with the place words first (all English words, then the first one, then the Korean words), then the plain subject, puts photos whose title, description or page name mention the place (and Korea, Seoul, 한국, 서울 for a Korean place) first, and prints 「장소 맞음(seoul)」 or 「장소 표시 없음」 per photo — a match in the title is not proof, so still check the contact sheet. If it finds nothing, retry once with a broader English subject (「basketball」 rather than 「KBL 3점슛」), then fall back below.
2. hallmark's library, when installed: `node <hallmark>/scripts/theme.mjs photos "<subject>" --json`.
3. The Wikimedia Commons API by hand (`commons.wikimedia.org/w/api.php`, `generator=search`, `filetype:bitmap`, `prop=imageinfo` with `extmetadata`, a descriptive User-Agent). Keep CC0, public domain, CC BY or CC BY-SA; use the sized thumbnail URL (960 and 1280 work).
4. The WordPress Photo Directory via Openverse (`api.openverse.org/v1/images/?q=<subject>&source=wordpress`, CC0); download the files into the mockup folder.
5. The Unsplash API with the client's own key (kept in their secrets folder, never in the page). Never drive a browser or script over Unsplash's site — its Terms §8 forbid automated access except through the API.
6. Otherwise drop the part and ask the client for the photo, or ask them to pick photos in their browser and paste the photo pages.
