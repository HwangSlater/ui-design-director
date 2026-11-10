# Selecting a color direction

## Start from the field's measured colours

Measure the base's colours by area (computed styles plus the capture): background, second surface, text, muted text, accent, any dark field — usually 4–6 tones. A palette is that combination and the relationships between the tones (warm or cool, value steps, which tone carries which part), not a white page with one accent: a Pilates studio built on white, ink and a touch of green read as 「단색」 next to its base's dark brown, oat, taupe and sand. Every candidate keeps the base's number of tones and their relationships (value steps, warm or cool, which tone carries which part) but moves the hues to the client's own: never offer the base's exact colours as a candidate (「바탕 그대로」) — the client picked it every time and the page then read as the base's own site (NBA round: theScore in Korean). The only exception is a client whose existing brand colours already match the base; record that in `concept-brief.md`. `copy_check.py` flags a palette candidate or a mockup whose colours equal the base's.

**Hues come from a published palette, never from memory.** Run `python ${CLAUDE_SKILL_DIR}/scripts/palettes.py pick --tags <tags> --project .` (tags: warm, cold, earth, nature, pastel, vintage, retro, cream, coffee, dark, light, sea, sky, spring, summer, fall, winter, food, kids, wedding, night, sunset, skin, gold, happy) and build each candidate from one printed palette: its colours take the base's roles (lightest → background and surface, darkest → text or dark field, the strongest → action or accent); white, near-black and pale grey may be added, and a palette colour may be darkened or lightened in the same hue for contrast. Put the printed `colorhunt.co/palette/…` address in `source`. Models picked cream with forest green, brick and butter yellow again and again (62 earlier candidates: forest green 12, brick 12, butter 10; dog groomer 19th), so `pick` leaves those families out and the hook refuses a palette page whose candidates have no published source. Colours the client already uses (sign, logo) go in with `source` 「의뢰인 색 …」.

## Curate for the product

Present 3–4 palettes, each with the base's 4–6 tones; no near-duplicates. Candidates must differ in the colours that carry the page — the base's own colour fields and the accent — not only in the button; never add pale tinted bands or surfaces the base does not have. When the brief says “warm”, offer more than one reading of warmth (cream and brown; pale sky and tangerine; off-white and deep green; butter and brick) (`design-selection.md` § 3).

Check selected and active states in every candidate: mark selection by fill plus a check mark or weight, never by an accent outline alone (a pale outline vanishes in some palettes), and keep the primary button high-contrast in every palette.

For each candidate show hex values with its source (the base, or a fallback palette link), proposed roles (canvas/surface, text, primary action, accent) with rough distribution, and contrast, colour-blindness and saturation risks; note any existing brand colour preserved or adjusted.

Let the user try the palettes on the chosen format in the live palette preview (`comparison-board.md` § Palettes and fonts). The preview is disposable; do not apply palettes to production UI at this stage.

Derive neutral ramps and state colours faithful to the tones; do not pretend every tone can serve as accessible text or button colour.

## Fallback: the base has no usable palette

Only when the base's colours cannot be used (a monochrome template, a brand colour the client rejects): take the tone relationships from the other well-known candidates instead, and the hues still from `palettes.py pick`. Never Huemint or other generated palettes.

## Let the user choose freely

Label palettes A/B/C rather than ranking by taste; recommend one or two. The user may lock individual colours, combine colours by named role (“A background + C accent”), reject a mood, or ask for lighter, darker, warmer, cooler, quieter or more vivid variants. After combining, verify harmony and role contrast instead of concatenating swatches.

## Accessibility gate

Before approval, test intended foreground/background pairs. Compute each ratio from the hex values rather than recalling or eyeballing it; a pair can miss AA by hundredths. If computation is unavailable, mark the pair unverified. Report pass/fail for normal text, large text and essential controls. When a chosen raw colour fails, adjust the role mapping or derive an accessible shade; keep the user's colour as an accent if appropriate.

Record the selected source URL, original colors, derived colors, semantic roles, distribution, user modifications, and accessibility adjustments in the pending selection record. Add it to `DESIGN.md` together with the approved format record.
