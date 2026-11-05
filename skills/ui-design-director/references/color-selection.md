# Selecting a color direction

## Start from the field's measured colours

Before looking at palette libraries, measure the background, text and button colours of the reference sites (computed styles, weighted by area). Running sites in Korea and abroad are mostly white background, light-grey panels, near-black text (#000–#1A1C20) and one strong accent or none; show at least one candidate built that way. Treat a warm beige background with a brown or olive button as a known generated look, not a neutral default (a blind judge called it 「개성 없는 베이지 톤」).

Start from one accent besides black: an open/closed green plus a red or blue button reads as 「강조색이 두 개, 근거 없음」, and one dark accent painted on the header, every button and every panel reads as AI-made. Offer a second block colour only when the client asks for more colour or the shortlisted sites share one, and spread the one accent over fewer places instead of painting every panel. When the client asks to mix two candidates, say before building it that this makes two accent colours. Colour alone is a small lever; it does not fix a page with no brand mark, uniform section rhythm or mismatched photos.

## Find real palette candidates

Use Coolors, Color Hunt, Adobe Color, Huemint, another reputable library that fits the brand, or the ui-ux-pro-max colour database when installed (labelled as a database suggestion, `companion-skills.md`). Link to individual palettes, verify links and exact hex values, and do not cite a generated combination as a published palette.

## Curate for the product

Present 3–4 palettes covering a few mood territories from the concept brief (calm/trustworthy, warm/human, technical/precise, bold/creative); no near-duplicates.

Candidates must differ in their large areas — background, surfaces, bands — not only in the button. When the brief says “warm”, offer more than one reading of warmth (cream and brown; pale sky and tangerine; off-white and deep green; butter and brick) (`design-selection.md` § 3).

Check selected and active states in every candidate: mark selection by fill plus a check mark or weight, never by an accent outline alone (a pale outline vanishes in some palettes), and keep the primary button high-contrast in every palette.

For each candidate show hex values with a source link, proposed roles (canvas/surface, text, primary action, accent) with rough distribution, and contrast, colour-blindness and saturation risks; note any existing brand colour preserved or adjusted.

Let the user try the palettes on the chosen format in the live palette preview (`comparison-board.md` § Palettes). The preview is disposable; do not apply palettes to production UI at this stage.

A 3–4 swatch palette needs derived neutral ramps and state colours; keep them faithful to the palette, but do not pretend every swatch can serve as accessible text or button colour.

## Let the user choose freely

Label palettes A/B/C rather than ranking by taste; recommend one or two. The user may lock individual colours, combine colours by named role (“A background + C accent”), reject a mood, or ask for lighter, darker, warmer, cooler, quieter or more vivid variants. After combining, verify harmony and role contrast instead of concatenating swatches.

## Accessibility gate

Before approval, test intended foreground/background pairs. Compute each ratio from the hex values rather than recalling or eyeballing it; a pair can miss AA by hundredths. If computation is unavailable, mark the pair unverified. Report pass/fail for normal text, large text and essential controls. When a chosen raw colour fails, adjust the role mapping or derive an accessible shade; keep the user's colour as an accent if appropriate.

Record the selected source URL, original colors, derived colors, semantic roles, distribution, user modifications, and accessibility adjustments in the pending selection record. Add it to `DESIGN.md` together with the approved format record.
