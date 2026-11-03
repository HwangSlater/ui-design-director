# Extracting and adapting a selected reference

The goal is a coherent product design language, not a pixel-for-pixel clone.

## Evidence coverage

Inspect multiple representative pages and relevant viewport sizes where available. Combine rendered evidence with DOM/computed-style inspection when tools permit:

- color-role and contrast relationships from the format reference only when useful; if the user selected a separate palette, preserve that palette and borrow roles rather than literal reference colors;
- type family, hierarchy, scale, weight, leading, tracking, and measure;
- spacing rhythm, containers, grids, alignment, density, and section cadence;
- shape, borders, elevation, iconography, imagery, and motion;
- navigation, buttons, inputs, cards, lists/tables, overlays, and feedback;
- default, hover, focus, active, selected, disabled, loading, empty, success, and error states;
- responsive changes in hierarchy, navigation, columns, density, and information priority.

DOM/CSS reveals values but not necessarily intent. Screenshots reveal appearance but not exact values or hidden states. Record which evidence exists.

## Visual layers — what makes the reference look made

Structure is the easy part to borrow; finish is what gets lost. A futsal-league site took FotMob's table layout and dropped everything else — league crest, team crests, coloured form chips, the second column at desktop width — and the owner's verdict was "compared with sites that actually run, it has no design and is too simple." Before writing tokens, list the reference's visual layers from its captures at 1:1 (the list lives in `scripts/side_by_side.py`): identity (logo, wordmark, header band), the face of each item (team crests, product photos, avatars), icons, colour blocks beyond buttons, data marks (chips, bars, badges), imagery or what stands in for it, depth (shadows, one dark panel), wide-screen columns, type contrast, and trust (reviews, ratings, certificates). Trust is the layer most often missing because the brief never mentions it: Stayfolio shows reviews, the mockup had none, and the owner noticed. Never invent reviews; leave a labelled slot for ones the owner can bring ("에어비앤비 후기 몇 개를 옮겨 올 자리") and ask.

For each layer record **adopt**, **replace with …**, or **drop because …**. A dislike removes a form, not the layer: "no big player photos" becomes team crests or monogram badges, "no black background with neon" becomes one dark scoreboard panel on a light page. Two or more layers dropped without a replacement means the result will look generated; take it back to the user before building. Missing assets get a designed stand-in (a wordmark and simple mark for a league without a logo, monogram badges for teams without crests), labelled as such, not an empty space.

### Borrow the grammar, not the face

Measuring and following a leading site in the same field is how a page gets its finish, but when that site shares the user's audience, looking like it is a real cost: a shelter owner whose donors also give to the large welfare groups did not want to be mistaken for them. Take the reference's interaction patterns, proportions and numbers (card ratio, filter style, form steps, type scale, radii); keep the identity layers the user's own — palette, wordmark, photo treatment, signature element. Before showing, put the first screens side by side and ask whether a regular visitor of the reference could mistake one for the other; if so, change the identity layers, not the patterns.

## Classify every important rule

- **Observed:** directly verified in the reference.
- **Inferred:** a likely system rule derived from repeated evidence.
- **Adapted:** intentionally changed to fit this product, its content, brand, implementation, or accessibility.
- **Provisional:** a reversible default pending user confirmation.

Include confidence for consequential inferred rules. Do not invent false precision: consolidate noisy, near-duplicate values into a purposeful scale.

## Extract relationships before numbers

Determine the design grammar first: hierarchy, density, contrast strategy, emphasis, repetition, and component character. Then encode values. Preserve relationships such as “section gap is roughly twice card padding” when they matter more than an isolated pixel measurement.

Convert approved palette colors to semantic roles. The format reference may inform color distribution and emphasis, but its literal colors must not override a separately approved palette. Build a coherent typography and spacing scale rather than listing every computed value. Identify exceptions and decide whether they are intentional or extraction noise.

## Adapt deliberately

Check the selected reference against the concept brief and real project content. Common reasons to depart include:

- the product has denser data or longer localized text;
- reference body text, contrast, targets, or focus behavior is insufficient;
- brand assets or existing component conventions must remain;
- the reference lacks product UI, forms, destructive actions, or responsive states;
- implementation constraints require a simpler motion or layout system.

Document each high-impact departure and rationale. The reference is evidence, while approved `DESIGN.md` is the authority for implementation.

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

Do not mark `DESIGN.md` approved until the user has confirmed the format reference, palette and derived accessibility adjustments, high-impact adaptations, and any preview feedback they requested.
