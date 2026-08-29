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
- responsive behavior and density rules;
- focus, loading, empty, error, disabled, and reduced-motion behavior;
- implementation mapping or clearly listed open questions.

Do not mark `DESIGN.md` approved until the user has confirmed the format reference, palette and derived accessibility adjustments, high-impact adaptations, and any preview feedback they requested.
