# Planning the whole site

The output is project-root `SITE-PLAN.md`: the page inventory, flows, and per-page status that every later step reads and updates.

## Contents
- Gates (whole site)
- 1. Decide the scope of each surface
- 2. Build the page inventory
- 3. Map the flows
- 4. Check content reality
- 5. Write SITE-PLAN.md
- 6. Approval

## Gates (whole site)

Gates 1–5 are the SKILL.md workflow (brief to design); a whole site continues with 6–10.

1. **Context.** Concept brief: product and main job, audience, archetype, essential screens, density, brand traits, constraints, dislikes; label what you inferred. Ask in the same step for what only the client has — photos, logo or sign artwork, a notice in their own words — and say samples cap how real it can look.
2. **Format.** About five well-known running sites of the field and one or two templates, in the shared live viewer; say the shared traits (n/N). The client picks **one base**.
3. **Palette.** 3–4 palettes on the palette-switcher template, each built from the base's 4–6 tones; fonts on the same page.
4. **Preview.** Only when it helps or the client asks; disposable.
5. **Rules.** `DESIGN.md`: observed evidence, product decisions, unknowns; small defaults stay marked provisional.
6. **Site plan.** Page inventory and flows in `SITE-PLAN.md` (this file's §§ 1–6), approved before pages.
7. **Layout.** Two numbered home options differing in structure, in the approved colours and fonts, at both widths; settle the shared frame once.
8. **Mockups.** Full fidelity from `DESIGN.md` tokens, both widths, every required state, home and main-job page first; a clickable prototype; approval per page.
9. **Proof.** For production, one representative page before the rest.
10. **System.** Move every approved reusable change into `DESIGN.md` and the shared tokens and components.

## 1. Decide the scope of each surface

Classify every page before planning it:

- **Read surfaces** — marketing, landing, pricing, about, blog, docs, legal. The visitor scans and decides. Hierarchy, a single primary action per page, and section rhythm govern them.
- **Work surfaces** — dashboard, list/detail, settings, editor, multi-step form, account. The user repeats a task. Density, navigation stability, keyboard paths, and every data state govern them. Hero sections, section rhythm, decorative imagery, and load-in reveals do not apply.

When one product has both, keep one `DESIGN.md` and let density and component sizes differ by surface; do not force the dashboard to look like the landing page or the reverse.

## 2. Build the page inventory

Derive pages from the product's jobs, not from a template's page list. Start from repository evidence (routes, existing pages, README, data models) and the concept brief, then confirm only what is missing.

For each page record:

| Field | Meaning |
|---|---|
| Name | The page's name in the client's language (「첫 화면」, 「사례 모음」) — the client reads this table; keep the file slug (`home`, `cases`) in a separate designer line below it. |
| Surface | read or work |
| Page type | Shared layout it belongs to; pages of one type share one design |
| Job | The one thing the visitor or user comes to do here |
| Primary action | The single action the page exists to produce |
| Entry points | Where users arrive from |
| Content source | Supplied by user / exists in repo / needs writing / sample data |
| Required states | Empty, loading, error, no-permission, long content, success, as applicable |
| Kept up to date by | For content that changes (dates, seats, prices, menus, hours, staff, listings): who updates it, where, how often |
| Priority | Core / secondary / later |

Group pages by **page type** (ten blog posts are one type). Design every page type, and only the pages whose content changes the layout.

Always include the pages users meet when something goes wrong or is missing: 404, error, empty first-run, signed-out, and no-permission where the product has accounts.

**When the owner or staff update anything, plan their screens now, not at the mockup step.** List in `SITE-PLAN.md` how they sign in, what to do when the phone is lost, the few jobs they actually do (often two, e.g. today closed, change a price), and who to contact for what is not on their screen; rules in `owner-screens.md`. `${CLAUDE_SKILL_DIR}/scripts/preflight.py` reports a plan with owner screens but no sign-in or lost-phone line.

**Every field a page shows needs an input someone fills.** Trace each label on a public page back to the form that feeds it and design both together; show nothing the upload form does not collect. Prefer taps over typing (yes / no / don't know, hidden when unknown: 「개와 지내요: 예」). Never pre-fill a free-amount or free-text field with a sample value — a grey "5,000" reads as already entered. Every field a customer fills shows on the staff screen that handles it. When a status change hands work to someone else (「방문 약속」 sends the owner to measure), draw the fields that change needs (date, time) and an alert to that person that is always on, not a tick box.

**Design out content nobody will maintain.** For every piece of changing content, ask who updates it and where; a small team rarely keeps a second copy in sync. When the data already lives in another system (a booking platform, Instagram, a menu tool, a marketplace listing), link to it for the live part and design a version that cannot go stale on the site: a recurring timetable instead of dated slots, "see live availability" instead of seat counts, prices that change rarely. Use a live embed only when that system offers one and its terms allow it. Record the decision in the page inventory. Mark payment methods 견본 until the payment provider is chosen. Prefer timeless phrasing ("every weekend") over words that go false the first week nobody updates them ("this weekend", "seats left", "new this month") unless the text comes live from the source.

**Orders and bookings.** For pickup or made-to-order work, ask for a per-hour limit as well as the per-day one. Ask who the order belongs to: label the form 「주문하시는 분」 (「받는 분」 is misread), add a gift checkbox for a different person picking up, and send messages only to the orderer.

## 3. Map the flows

List the 2–5 journeys that matter most, each as an ordered chain of page IDs with the action that moves between them:

```text
Sign-up: home —[Start free]→ sign-up —[Submit]→ verify-email —[Link]→ onboarding-1 → onboarding-2 → dashboard (empty)
```

For each flow name the point where users most often abandon and what the design must do there. A flow that ends on a page with no next action is a gap; record it.

Navigation follows from the inventory: global navigation holds only core pages; secondary pages live in the footer, a settings area, or contextual links. State the mobile navigation pattern explicitly.

## 4. Check content reality

For each core page note what real content exists. Where it does not, plan sample content of the real length and shape (a real-length product name, a realistic price table, a 40-row list), marked as sample. Keep a list of the practical facts the user has confirmed (address, directions, hours, policies); everything else stays unconfirmed (`mockup-content.md` § Facts and wording).

## 5. Write SITE-PLAN.md

```markdown
---
status: draft | approved
updated: YYYY-MM-DD
design_md_version: 0.1
build_target: static-html | <framework found in repo>
---

# Pages
| ID | Surface | Page type | Job | Primary action | Content | States | Priority | Layout | Mockup | Code |
|---|---|---|---|---|---|---|---|---|---|---|
| home | read | landing | Decide whether to try | Start free | needs writing | — | core | pending | pending | pending |

# Flows
1. Sign-up: home —[Start free]→ sign-up → …  Drop-off risk: …

# Navigation
Global: … · Footer: … · Mobile: …

# Decision log
- YYYY-MM-DD — approved — page inventory — rationale
```

The `Layout`, `Mockup`, and `Code` columns track progress per page: `pending` → `options-shown` → `approved` (or `done` for code). Update the row the moment a state changes.

## 6. Approval

Present the inventory table and the flows, recommend what to cut or defer, and ask the user to approve the list. Do not start page layouts until the inventory is approved or the user explicitly delegates it.
