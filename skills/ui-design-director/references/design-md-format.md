# DESIGN.md specification

Create `DESIGN.md` at the project root unless the repository has another canonical location.

## Contents
- Required structure
- Source and adaptation record
- 바탕에서 바꾼 곳
- 부품 출처
- Principles
- Voice and terminology
- Tokens
- Components
- Page and interaction patterns
- Accessibility requirements
- Implementation mapping
- Decision log
- Open questions
- Writing rules
- Feedback protocol
- Agent handoff contract

## Required structure

```markdown
---
name: Product design language
status: draft | approved
version: 0.1
updated: YYYY-MM-DD
primary_reference: URL | local screenshot/path | user-defined concept
secondary_references:
  - source: URL | local screenshot/path
    borrowed_trait: Exact trait and scope
palette_sources:
  - source: URL | generated | user-provided
    colors: ["#000000", "#FFFFFF", "#3366FF"]
    borrowed_role: Full palette | background | surface | action | accent
preview_selection: stable-preview-id | not-created
selection_status:
  format: provisional | approved-user | approved-delegated
  palette: provisional | approved-user | approved-delegated
  preview: not-requested | provisional | approved
---

# Design intent
Product, audience, desired impression, content reality, and selected concept.

## Source and adaptation record
What was inspected; observed/inferred/adapted/provisional distinctions; known
license/reuse constraints; chosen format and palette; deliberate departures
from the reference; preview combination approved by the user.

## 바탕에서 바꾼 곳
Each change from the base that `skeleton.mjs --base` listed, taken or left,
with its count (「옆으로 넘기는 띠: 넣음 — 3/5곳」), and any other departure
with its reason.

End it with a short list 「우리 것(마감)」 naming at least two of 색 계열,
이름 처리, 칸 마감, 대표 요소, each with what ours is (「- 칸 마감: 둥근 흰 칸,
선 없음」). `copy_check.py` (also run by `preflight.py`) reports 「우리 것 마감이
둘 미만」 when fewer than two of those words appear in this section. When the
client asked for real logos or photos (DESIGN.md says 실제 로고 or 견본 로고),
이름 처리 does not count as ours; pick two others.

## 부품 출처
One line per part: part → form → source (the base, a field trait as n/N, or
the client's own object such as the menu board or sign).

## Principles
Three to five testable rules with “do” and “avoid” guidance.

## Voice and terminology
The audience expertise these choices assume, product vocabulary as banned/
preferred term pairs, fixed status labels, and message patterns for validation,
error, empty, confirmation, and undo states.

## Tokens
### Color
Original 3–4 color selection, derived ramps/neutrals, semantic roles,
foreground/background contrast results, interaction states, modes, and rationale.

### Typography
Families/fallbacks, role-based scale, weights, line heights, tracking, measure,
numeric behavior, and responsive adjustments.

### Spacing and layout
Base rhythm, scale, containers, grids, gutters, density, section cadence, and
content-driven breakpoints.

### Visual layers
The reference's layer inventory (`build-rules.md` § Follow the base 6) with adopt / replace / drop for each, the stand-ins used for missing assets (wordmark, monogram badges), and the icon set with its licence.

### Shape, border, elevation, iconography, imagery, and motion
Purposeful scales and usage rules, including reduced-motion behavior.

## Components
Relevant primitive anatomy, variants, sizes, content rules, and default/hover/
focus/active/selected/disabled/loading/error behavior.

## Page and interaction patterns
Hierarchy, navigation, forms, validation, loading, empty/error states,
destructive actions, responsive transformations, and information density.

## Accessibility requirements
Keyboard/focus, contrast, target size, semantics, zoom/reflow, non-color cues,
and motion alternatives.

## Implementation mapping
Map semantic tokens to existing CSS variables/theme keys and rules to shared
components. List approved exceptions; do not duplicate an existing canonical token file.

## Decision log
- YYYY-MM-DD — proposed/approved/superseded — decision — rationale

## Open questions
Only unresolved decisions that materially affect implementation, with provisional defaults.
```

## Writing rules

- Prefer semantic component-facing names such as `color.action.primary` over visual names such as `blue.500`; a primitive palette may sit underneath.
- Pair unusual values and exceptions with rationale or evidence.
- Record on-screen wording as rules — a term table and message patterns — not samples.
- Keep product requirements distinct from reference observations.
- Preserve the original selected palette separately from derived accessible UI tokens, so later agents do not confuse inspiration swatches with usable semantic colors.
- `approved` needs explicit user approval of format, palette, derived accessibility adjustments, high-impact adaptations, and requested preview feedback; otherwise keep `status: draft` and name the unresolved items. Use `approved-delegated` only when the user explicitly delegated that choice, with the rationale in the decision log.
- When an approved rule changes, increment the version, mark the earlier decision superseded, and update shared implementation mapping.

## Feedback protocol

Interpret feedback at the correct level:

- one-off content/layout adjustment → page pattern or documented exception;
- repeated visual change → token or shared component rule;
- change in product character → principle/concept decision requiring explicit approval.

Propose the rule-level change, name affected components/pages, obtain approval for high-impact changes, then update `DESIGN.md` before or with code. Do not leave a reusable decision only in chat.

## Agent handoff contract

For the subagents SKILL.md § Budget allows, use a short prompt of file paths; do not paste the design system:

> Read project-root `DESIGN.md` before UI work. Treat approved rules as constraints. Reuse mapped tokens and shared components. If a requirement conflicts or a needed rule is absent, report it and propose a `DESIGN.md` update rather than inventing a page-local convention. Verify the rendered result at relevant sizes and states.
