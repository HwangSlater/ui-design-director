# Finding sample photos

Use this when the client's own photos are missing. Placement rules (no empty photo boxes, the one 「견본」 line, drop a part rather than leave a slot): [build-rules.md](build-rules.md) § Content and samples.

## What to look for

- Match the product and the client's customers' setting (a Korean apartment, not a Western bathroom).
- Before/after samples show the same room from the same angle; otherwise drop the pair and ask the client.
- Prefer everyday, unstaged photos (people, places, mess) over evenly graded stock, which a blind judge read as AI.
- Judge candidates from a contact sheet, not their titles; check the subject matches what the client has and that every photo loaded.
- Credit author and licence for each photo; list them in the 「견본」 line.

## Where to search, in this order

1. hallmark's library, when installed: `node <hallmark>/scripts/theme.mjs photos "<subject>" --json`.
2. The Wikimedia Commons API (`commons.wikimedia.org/w/api.php`, `generator=search`, `filetype:bitmap`, `prop=imageinfo` with `extmetadata`, a descriptive User-Agent). Keep CC0, public domain or CC BY; use the sized thumbnail URL (960 and 1280 work).
3. The WordPress Photo Directory via Openverse (`api.openverse.org/v1/images/?q=<subject>&source=wordpress`, CC0); download the files into the mockup folder.
4. The Unsplash API with the client's own key (kept in their secrets folder, never in the page). Never drive a browser or script over Unsplash's site — its Terms §8 forbid automated access except through the API.
5. Otherwise ask the client to pick photos in their browser and paste the photo pages.
