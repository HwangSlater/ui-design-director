# Selecting a color direction

Choose the palette independently from the template's default colors so the user can retain a layout they like without inheriting an unsuitable brand mood.

## Start from the field's measured colours

Before looking at palette libraries, measure the background, text and button colours of the reference sites (computed styles, weighted by area). Running local-shop sites in Korea and abroad are almost all white background, light-grey panels, near-black text (#000–#1A1C20) and one strong accent or none: six bike shops measured white/#F2–#F7/#111 with red, pink or black buttons. Show at least one candidate built that way, and treat a warm beige background with a brown or olive button as a known generated look, not a neutral default — five projects in a row drifted there from 「차분한」 Color Hunt palettes, and a blind judge called it 「개성 없는 베이지 톤」. Keep to one colour besides black: an open/closed green plus a red or blue button read as 「강조색이 두 개, 근거 없음」. When the client asks to mix two candidates (a red button from one, a yellow panel from another), say before building it that this makes two accent colours and what it costs; a fresh session built the mix without a word. Colour alone is a small lever (white+black moved a blind judge from 85% to 80% AI and from 6 to 7 for finish, within the judge's noise); do not expect it to fix a page with no brand mark, uniform section rhythm or mismatched photos.

## Find real palette candidates

Use current palette libraries and link to individual palettes or reproducible combinations. Suitable sources include:

- Coolors for browsable and shareable multi-color palettes;
- Color Hunt for curated four-color combinations;
- Adobe Color for harmony-based palettes, image extraction, and accessibility exploration;
- Huemint when contextual previews help explain foreground/background/accent use;
- another reputable palette library that better fits the product or existing brand color;
- the ui-ux-pro-max colour database when installed, labelled as a database suggestion (`companion-skills.md`).

Verify links and exact hex values. Do not cite a generated combination as a community-curated palette unless it is actually published there.

## Curate for the product

Present 6–10 relevant 3–4 color combinations. Cover a small number of meaningful mood territories—such as calm/trustworthy, warm/human, technical/precise, or bold/creative—derived from the concept brief. Avoid random rainbow variety and near-duplicates.

Check selected and active states in every candidate, not only the default one: a selected tab and a selected amount that read clearly in one palette (yellow outline) vanished in another (a near-white mint outline), and the owner could not tell what was chosen. Mark selection by fill plus a check mark or weight, never by an accent outline alone, and keep the primary button high-contrast in every palette.

Candidates must differ in their large areas — background, surfaces, bands — not only in the button: five palettes on the same paper colour gave a piano-school owner nothing to choose between. When the brief says “warm”, offer more than one reading of warmth (cream and brown; pale sky and tangerine; off-white and deep green; butter and brick) instead of three shades of cream and brown (`design-selection.md` § 3).

Count the strong colours a palette gives you. A palette with one dark accent and three pale tints ends up painting the header, every button, the status bands, the donation panel, the contact buttons and the confirmation panel the same colour; a shelter owner called the result "green boxes all the way down", the one AI-looking thing left, next to a reference that rotates purple, orange and sky blue. When a candidate has a single strong colour, propose a second block colour (from the same source or a sibling palette) for information or celebration panels at this gate, and let the user choose it.

For each candidate show:

- a clear swatch strip with exact hex values and a direct source link;
- mood and brand signal;
- proposed roles for each color, such as canvas/surface, text, primary action, and accent;
- approximate distribution and emphasis, avoiding equal use of every swatch unless the concept intentionally calls for it;
- whether neutral text/surface shades must be derived separately;
- likely strengths on the selected design format;
- contrast, color-blindness, saturation, and dark-mode risks;
- any existing brand color preserved or adjusted.

Let the user try the palettes on the chosen format rather than read about them: build the live palette preview in `comparison-board.md` § Palettes, where each palette is a clickable chip that recolours a realistic page and shows its computed contrast. Record mood, roles, and risks in that page's data and in chat only as briefly as needed. The preview is disposable; do not apply palettes to production UI at this stage.

A 3–4 swatch palette is not a complete UI system. Most palettes need derived neutral ramps and state colors. Keep these derivations visually faithful to the selected palette, but do not pretend every original swatch can serve as accessible text or button color.

## Let the user choose freely

Keep palette labels neutral as A/B/C rather than ranking by taste. Recommend one or two based on audience, content, and accessibility, then let the user:

1. select one palette;
2. lock individual colors and ask for alternatives around them;
3. combine colors from candidates by named role, such as “A background + C accent”;
4. reject a mood territory entirely;
5. request lighter, darker, warmer, cooler, quieter, or more vivid variants.

When combining, verify the resulting harmony and UI role contrast instead of mechanically concatenating swatches.

If the user delegates the palette choice, select using product fit and accessible role pairs, show the chosen swatches and rationale, and record that the decision was delegated.

## Accessibility gate

Before approval, test intended foreground/background pairs rather than judging swatches in isolation. Compute each ratio from the hex values rather than recalling or eyeballing it; a pair can miss AA by hundredths. If computation is unavailable, mark the pair unverified instead of asserting a result. Report pass/fail for normal text, large text, and essential controls as relevant. Adjust the role mapping or derive an accessible shade when the chosen raw color fails; preserve the user's selected color as an accent if appropriate.

Record the selected source URL, original colors, derived colors, semantic roles, distribution, user modifications, and accessibility adjustments in the pending selection record. Add it to `DESIGN.md` together with the approved format record.
