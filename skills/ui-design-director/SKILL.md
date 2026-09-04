---
name: ui-design-director
description: Guide users conversationally through an overall UI concept by researching live templates and 3–4 color palettes, comparing coded previews, and converting approved choices into a durable DESIGN.md. Use when a user says they want to choose a design, for new products, redesigns, design-system extraction, or project-wide UI direction; do not trigger for isolated styling fixes.
---

# UI Design Director

Turn subjective taste into an explicit, user-approved design language. The user owns the visual decision; provide strong research, comparisons, and a recommendation so that choice is informed rather than arbitrary.

## Guide the conversation

When the user gives a broad request such as “I want to choose a design,” read [references/guided-conversation.md](references/guided-conversation.md) and lead the process proactively. Do not wait for the user to know which design questions to ask. Ask one consequential question at a time, provide concrete choices and plain-language examples, remember previous answers, and always make the next step obvious.

## Route the request

- **Concept:** The format or palette is undecided. Read [references/design-selection.md](references/design-selection.md) and [references/color-selection.md](references/color-selection.md). Let the user select the overall format and base palette as separate decisions.
- **Preview:** Format and palette finalists exist but the user wants to see them applied. Read [references/concept-preview.md](references/concept-preview.md) and create small, comparable coded UI previews outside production surfaces.
- **Extract:** The format reference and palette are approved, or the user explicitly wants a partial draft. Read [references/reference-extraction.md](references/reference-extraction.md) and [references/design-md-format.md](references/design-md-format.md), then create or revise project-root `DESIGN.md`. A partial draft must keep unresolved selections provisional and cannot be marked approved.
- **Apply:** `DESIGN.md` is approved and the user asked for implementation. Read it first, map it to shared tokens and primitives, and implement a representative slice before broad propagation when practical.
- **Review:** The user wants consistency or quality review. Read [references/ui-review.md](references/ui-review.md) and inspect rendered UI against `DESIGN.md`.

If a request spans modes, advance only to the next decision gate that is authorized. Do not interpret “find a design” as approval to implement it.

## Required gates

1. **Context gate:** Establish a compact concept brief from repository evidence and user input: product/job, audience, interaction archetype, essential screens, content density, brand traits, constraints, and anti-preferences. Name the archetype explicitly — marketing site, dashboard, editing tool, form workflow, or content reader — because it decides which sources are worth searching, and getting it wrong wastes the entire shortlist rather than one candidate. Ask only for missing information that would materially change the shortlist; label inferred items.
2. **Format gate:** Present direct links to individual live template/showcase candidates. Let the user choose a primary structural/visual reference, reject candidates, and optionally select exact secondary traits.
3. **Palette gate:** Present linked 3–4 color palette candidates independently from the format. Explain intended UI roles and contrast risks. Let the user select, modify, or reject them; a palette's original swatches are inspiration, not yet complete semantic UI tokens.
4. **Preview gate:** Offer a coded comparison when visual judgment would benefit; create it when the user requests or accepts. Combine only finalists using identical content and component coverage. Preview code is disposable evidence, not approval or production implementation.
5. **Rules gate:** Extract and adapt the approved format and palette into `DESIGN.md`. Separate observed evidence, product-specific decisions, and unknowns. Ask for approval of unresolved high-impact choices; minor safe defaults may remain clearly marked as provisional.
6. **Proof gate:** When production implementation is requested, build or adapt one representative page/slice and show it at relevant viewport sizes and states. Propagate only after approval when the scope is broad.
7. **System gate:** Move every approved reusable feedback item into `DESIGN.md` and the shared token/component layer. Chat instructions and page-local CSS are not durable design decisions.

## Non-negotiable behavior

- Verify every candidate before presenting it: open the link, and state prices, licences, page coverage, and responsiveness only from what you actually inspected. If something is inaccessible, unverifiable, or live research is unavailable, say so and ask for user-provided references — never fabricate a candidate or imply you inspected one.
- Keep format, palette, and typography identifiable as separate choices. Do not let a template's default colors silently decide the user's palette.
- Do not mark the concept approved until format, palette, any high-impact adaptation, and requested preview feedback are resolved. Approval of one axis does not imply approval of another.
- Prefer one coherent primary reference. Borrow from secondary references only by named trait; do not create a collage of unrelated trends.
- Extract relationships and intent—not merely frequent CSS values. Adapt the reference to the product's content, interaction model, brand, and accessibility needs.
- Preserve existing brand and product constraints unless the user explicitly approves changing them.
- Treat accessibility as a baseline across every candidate: visible focus, sufficient contrast, non-color cues, usable targets, semantic controls, reflow/zoom, and reduced motion.
- Avoid generic AI decoration such as gratuitous gradients, glass effects, excessive pills, and oversized hero text unless the chosen reference and product rationale support them.
- Do not copy protected logos, illustrations, text, or a distinctive composition verbatim.
- Establish the licence of every candidate and recommended dependency from its published licence text, not from memory. When the product will be operated commercially, a licence that forbids or charges for commercial use is a disqualifier, not a footnote — filter on it before taste, name what you verified, and flag what still needs legal review.
- The user may explicitly delegate a design choice. Treat that as authorization to select, but record the delegated decision and rationale rather than presenting it as the user's personal preference.
- Do not turn concept discovery into a long questionnaire or require design vocabulary. Translate abstract choices into visible product consequences and let the user answer with a candidate number, a reaction, or plain language.

## Durable outputs

Depending on the active mode, produce only the necessary artifact:

- a compact concept brief plus linked candidate shortlist;
- a linked palette shortlist with swatches, semantic-role proposal, and contrast notes;
- isolated coded previews comparing finalist format/palette combinations;
- an approved-reference record;
- project-root `DESIGN.md` with tokens, rationale, provenance, decisions, and open questions;
- shared token/component implementation and a representative UI proof;
- a rendered-UI review with concrete deviations and corrections.

When product requirements conflict with the reference, explain the conflict and prioritize usability, accessibility, existing brand constraints, and the user's explicit decisions.
