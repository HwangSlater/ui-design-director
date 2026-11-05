# Coded concept previews

Skip this gate when the live palette preview (`comparison-board.md` § Palettes) already settled format and palette together.

## Control the comparison

Do not render every template × palette permutation. After the user narrows the choices, preview 2–3 combinations at a time, holding content, viewport, component coverage and effort constant. Name each combination: format reference, palette ID and source, any secondary trait, and the provisional typography.

## Preview content

Use realistic product content: navigation, title and body hierarchy, primary and secondary actions, a card or list/table, an input with focus and error, a status element, at narrow and wide widths. For a marketing-only product use a hero, trust section, content block, conversion action and footer; for an application prioritise navigation, density, controls and states.

## Implementation isolation

Prefer the project's existing framework and primitives when they can be used without altering production behavior; otherwise a minimal standalone HTML/CSS preview in an isolated temporary workspace. Keep previews in the project only when the user asks, in a clearly labeled non-production route or directory.

Do not connect previews to production navigation, data, analytics, authentication, or deployment without explicit permission, and do not overwrite existing routes or components. Reuse identical markup across variants and vary only tokens and layout rules.

## Presentation

Before showing, check the three places previews break: every scroll container has a constrained height, the longest realistic label wraps or truncates deliberately, and the states you claimed are present. Render it if a renderer is available; if not, say the check was structural rather than visual. Hand it over through the viewer (`comparison-board.md`), labelled A/B/C, listing only the intentional differences.

Ask one question: which is closer, and the one change needed before approval.

A preview may use provisional tokens solely to render the comparison. After the user chooses, record the approved combination and feedback in `DESIGN.md`; do not silently propagate rejected preview code.
