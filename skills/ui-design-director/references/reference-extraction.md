# Extracting and adapting a selected reference

## Evidence coverage

Inspect representative pages at phone and desktop width with rendered captures and computed styles (`scripts/extract_styles.mjs` and the snapshot, build-rules.md § Follow the base), covering type, spacing and grid, shape and elevation, imagery, components, and their states and responsive changes. DOM/CSS reveals values but not intent; screenshots reveal appearance but not exact values or hidden states. Record which evidence exists.

## Visual layers — what makes the reference look made

Structure is the easy part to borrow; finish is what gets lost. Before writing tokens, list the reference's visual layers from its captures at 1:1 (the list lives in `scripts/side_by_side.py`): identity (logo, wordmark, header band), the face of each item (team crests, product photos, avatars), icons, colour blocks beyond buttons, data marks (chips, bars, badges), imagery or what stands in for it, depth (shadows, one dark panel), wide-screen columns, type contrast, and trust (reviews, ratings, certificates). Trust is the layer most often missing because the brief never mentions it; leave a labelled slot for reviews the owner can bring ("에어비앤비 후기 몇 개를 옮겨 올 자리") and ask.

For each layer record **adopt**, **replace with …**, or **drop because …**. A dislike removes a form, not the layer: "no big player photos" becomes team crests or monogram badges, "no black background with neon" becomes one dark scoreboard panel on a light page. Two or more layers dropped without a replacement means the result will look generated; take it back to the user before building. Missing assets get a designed stand-in (a wordmark and simple mark for a league without a logo, monogram badges for teams without crests), labelled as such, not an empty space.

When the reference shares the user's audience (donors who also give to the large groups), keep its patterns and numbers but make the identity layers the user's own — palette, wordmark, photo treatment, signature element (build-rules.md § Make it ours, not a copy).

## Classify every important rule

- **Observed:** directly verified in the reference.
- **Inferred:** a likely system rule derived from repeated evidence.
- **Adapted:** intentionally changed to fit this product, its content, brand, implementation, or accessibility.
- **Provisional:** a reversible default pending user confirmation.

Include confidence for consequential inferred rules. Consolidate noisy, near-duplicate values into a purposeful scale.

## Extract relationships before numbers

Determine the design grammar first — hierarchy, density, contrast strategy, emphasis, repetition, component character — then encode values. Preserve relationships such as “section gap is roughly twice card padding” when they matter more than an isolated measurement.

Convert approved palette colors to semantic roles. The format reference may inform color distribution and emphasis, but its literal colors never override a separately approved palette. Identify exceptions and decide whether they are intentional or extraction noise.

## Adapt deliberately

Document each high-impact departure from the reference (denser data, longer text, weak contrast or targets, brand assets to keep, missing product UI or states) and its rationale. The reference is evidence; approved `DESIGN.md` is the authority for implementation.

## Extraction completeness gate

Before marking the document ready for approval, verify it defines:

- semantic colors and interaction/accessibility states;
- type hierarchy and content measure;
- spacing/grid/container system;
- component patterns relevant to the actual product;
- product vocabulary and message patterns pitched at the audience's expertise;
- responsive behavior and density rules;
- focus, loading, empty, error, disabled, and reduced-motion behavior;
- implementation mapping or clearly listed open questions.
