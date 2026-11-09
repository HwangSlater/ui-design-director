# Selecting a color direction

## Start from the field's measured colours

Measure the base's colours by area (computed styles plus the capture): background, second surface, text, muted text, accent, any dark field — usually 4–6 tones. A palette is that combination and the relationships between the tones (warm or cool, value steps, which tone carries which part), not a white page with one accent: a Pilates studio built on white, ink and a touch of green read as 「단색」 next to its base's dark brown, oat, taupe and sand. Candidate A is the base's own combination adapted to the client; the others keep the same number of tones and the same relationships while shifting hue or temperature toward the client's identity. When the client asks to mix two candidates, say what the mix changes before building it.

## Curate for the product

Present 3–4 palettes, each with the base's 4–6 tones; no near-duplicates. Candidates must differ in the colours that carry the page — the base's own colour fields and the accent — not only in the button; never add pale tinted bands or surfaces the base does not have. When the brief says “warm”, offer more than one reading of warmth (cream and brown; pale sky and tangerine; off-white and deep green; butter and brick) (`design-selection.md` § 3).

Check selected and active states in every candidate: mark selection by fill plus a check mark or weight, never by an accent outline alone (a pale outline vanishes in some palettes), and keep the primary button high-contrast in every palette.

For each candidate show hex values with its source (the base, or a fallback palette link), proposed roles (canvas/surface, text, primary action, accent) with rough distribution, and contrast, colour-blindness and saturation risks; note any existing brand colour preserved or adjusted.

Let the user try the palettes on the chosen format in the live palette preview (`comparison-board.md` § Palettes and fonts). The preview is disposable; do not apply palettes to production UI at this stage.

Derive neutral ramps and state colours faithful to the tones; do not pretend every tone can serve as accessible text or button colour.

## Fallback: the base has no usable palette

Only when the base's colours cannot be used (a monochrome template, a brand colour the client rejects): take palettes from Coolors, Color Hunt, Adobe Color, Huemint or the ui-ux-pro-max colour database when installed (labelled as a database suggestion), and extend each to 4–6 tones in the base's relationships. Link individual palettes, verify links and exact hex values, and never cite a generated combination as a published palette.

## Let the user choose freely

Label palettes A/B/C rather than ranking by taste; recommend one or two. The user may lock individual colours, combine colours by named role (“A background + C accent”), reject a mood, or ask for lighter, darker, warmer, cooler, quieter or more vivid variants. After combining, verify harmony and role contrast instead of concatenating swatches.

## Accessibility gate

Before approval, test intended foreground/background pairs. Compute each ratio from the hex values rather than recalling or eyeballing it; a pair can miss AA by hundredths. If computation is unavailable, mark the pair unverified. Report pass/fail for normal text, large text and essential controls. When a chosen raw colour fails, adjust the role mapping or derive an accessible shade; keep the user's colour as an accent if appropriate.

Record the selected source URL, original colors, derived colors, semantic roles, distribution, user modifications, and accessibility adjustments in the pending selection record. Add it to `DESIGN.md` together with the approved format record.
