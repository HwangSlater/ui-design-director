# Rendered UI review

Review the rendered product, not code alone. Compare it with approved `DESIGN.md`, the concept brief, and actual content/interaction needs.

## Severity

1. **Blocking:** unusable interaction, broken hierarchy/task flow, inaccessible keyboard path, severe contrast/reflow issue, broken responsive layout, or missing critical state.
2. **System drift:** hard-coded repeated values, inconsistent variants, reference traits applied outside their approved scope, or typography/spacing/component behavior contradicting `DESIGN.md`.
3. **Polish:** alignment, rhythm, optical balance, wrapping/truncation, icon sizing, image treatment, and motion timing.

For each finding identify the screen/component, observed behavior, violated rule or user impact, evidence, and concrete correction. Mark subjective alternatives as decisions for the user rather than defects.

## Coverage

- representative narrow, medium, and wide widths plus stress points between them;
- realistic content density, long labels, empty/dense data, localization expansion, and zoom/reflow;
- hover, keyboard focus, active, selected, disabled, loading, empty, success, and error states as applicable;
- reduced motion, keyboard order, target sizes, semantics, and non-color feedback;
- consistency across repeated components and absence of unexplained one-off values;
- visual continuity between marketing pages and product UI without forcing them to identical density.

## Correction protocol

Fixes require user authorization when the request was review-only. When fixing, update the highest reusable layer first: `DESIGN.md` decision → semantic token → shared component → page exception. If a finding exposes a concept-level conflict, stop broad propagation and return the decision to the user.
