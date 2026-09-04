# Selecting a color direction

Choose the palette independently from the template's default colors so the user can retain a layout they like without inheriting an unsuitable brand mood.

## Find real palette candidates

Use current palette libraries and link to individual palettes or reproducible combinations. Suitable sources include:

- Coolors for browsable and shareable multi-color palettes;
- Color Hunt for curated four-color combinations;
- Adobe Color for harmony-based palettes, image extraction, and accessibility exploration;
- Huemint when contextual previews help explain foreground/background/accent use;
- another reputable palette library that better fits the product or existing brand color.

Verify links and exact hex values. Do not cite a generated combination as a community-curated palette unless it is actually published there.

## Curate for the product

Present 6–10 relevant 3–4 color combinations. Cover a small number of meaningful mood territories—such as calm/trustworthy, warm/human, technical/precise, or bold/creative—derived from the concept brief. Avoid random rainbow variety and near-duplicates.

For each candidate show:

- a clear swatch strip with exact hex values and a direct source link;
- mood and brand signal;
- proposed roles for each color, such as canvas/surface, text, primary action, and accent;
- approximate distribution and emphasis, avoiding equal use of every swatch unless the concept intentionally calls for it;
- whether neutral text/surface shades must be derived separately;
- likely strengths on the selected design format;
- contrast, color-blindness, saturation, and dark-mode risks;
- any existing brand color preserved or adjusted.

Use a compact comparison table for meaning and risks, but do not rely on hex strings alone to communicate appearance:

| Palette | Visual swatches | Mood | Proposed roles | Product fit | Contrast/risk |
|---|---|---|---|---|---|

If the response surface cannot render faithful color swatches, create a lightweight isolated HTML palette board or comparable visual artifact. Use equal-size swatches, readable labels, exact hex values, source links, and sample foreground/background pairs. Do not apply the palettes to production UI at this stage.

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
