# Coded concept previews

Use small coded UI previews to let the user judge how a selected design format and palette behave together before production implementation.

## Control the comparison

Do not render every template × palette permutation. After the user narrows the choices, preview 2–3 combinations at a time. Hold content, viewport, component coverage, and implementation effort constant so the comparison is fair.

Name each combination explicitly:

- format reference;
- palette ID and source;
- any secondary trait;
- provisional typography choice if typography is not yet approved.

## Preview content

Use realistic product content when available. Include enough UI to expose the system rather than making a decorative hero only:

- navigation/header;
- page title and body hierarchy;
- primary and secondary actions;
- card or list/table appropriate to the product;
- input/control with focus and error treatment;
- status/feedback element;
- representative narrow and wide layouts.

For a marketing-only product, use a hero, trust/evidence section, feature/content block, conversion action, and footer. For an application, prioritize navigation, data density, controls, and states.

## Implementation isolation

Prefer the project's existing framework and primitives when they can be used without altering production behavior. Otherwise create a minimal standalone HTML/CSS preview. By default, use an isolated temporary workspace so concept experiments do not dirty the product repository. Keep previews in the project only when the user asks to retain them or project-local execution materially improves the comparison; then use a clearly labeled non-production route or directory.

Do not connect previews to production navigation, data, analytics, authentication, or deployment without explicit permission. Do not overwrite existing routes or components to create a comparison.

Avoid adding a new framework or heavyweight dependency solely for the preview. Reuse identical markup across variants and vary tokens/layout rules; this makes visual differences attributable to the concept rather than different content.

## Presentation

Run or render the preview when tools permit. Provide clickable local files/routes and screenshots at comparable dimensions; raw source code alone is not an adequate visual comparison. Label A/B/C neutrally and list only the intentional differences.

Ask the user to judge:

1. overall product fit and first impression;
2. hierarchy and clarity of the primary task;
3. density and reading comfort;
4. palette mood and emphasis;
5. one specific change needed before approval.

Treat the preview as disposable evidence, not the production implementation or an approved design system. A preview may use provisional tokens solely to render the comparison. After the user chooses, record the approved format/palette combination and feedback in `DESIGN.md`; do not silently propagate rejected preview code.
