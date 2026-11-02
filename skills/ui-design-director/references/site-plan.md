# Planning the whole site

Use this after `DESIGN.md` exists (draft or approved) and the user wants the full website or app designed, not only its visual language. The output is project-root `SITE-PLAN.md`: the page inventory, flows, and per-page status that every later step reads and updates.

## 1. Decide the scope of each surface

A site usually mixes two kinds of surface. Classify every page before planning it, because the rules differ:

- **Read surfaces** — marketing, landing, pricing, about, blog, docs, legal. The visitor scans and decides. Hierarchy, a single primary action per page, and section rhythm govern them.
- **Work surfaces** — dashboard, list/detail, settings, editor, multi-step form, account. The user repeats a task. Density, navigation stability, keyboard paths, and every data state govern them. Hero sections, section rhythm, decorative imagery, and load-in reveals do not apply.

When one product has both, keep one `DESIGN.md` and let density and component sizes differ by surface; do not force the dashboard to look like the landing page or the reverse.

## 2. Build the page inventory

Derive pages from the product's jobs, not from a template's page list. Start from repository evidence (routes, existing pages, README, data models) and the concept brief, then confirm only what is missing.

For each page record:

| Field | Meaning |
|---|---|
| ID | Stable short slug, such as `home`, `pricing`, `project-detail` |
| Surface | read or work |
| Page type | Shared layout it belongs to; pages of one type share one design |
| Job | The one thing the visitor or user comes to do here |
| Primary action | The single action the page exists to produce |
| Entry points | Where users arrive from |
| Content source | Supplied by user / exists in repo / needs writing / sample data |
| Required states | Empty, loading, error, no-permission, long content, success, as applicable |
| Priority | Core / secondary / later |

Group pages by **page type**. Ten blog posts are one page type; designing the type once is what keeps the site consistent and the work finite. Design every page type, and only the pages whose content changes the layout.

Always include the pages users meet when something goes wrong or is missing: 404, error, empty first-run, signed-out, and no-permission where the product has accounts. These are routinely forgotten and the first to look unfinished.

## 3. Map the flows

List the 2–5 journeys that matter most, each as an ordered chain of page IDs with the action that moves between them:

```text
Sign-up: home —[Start free]→ sign-up —[Submit]→ verify-email —[Link]→ onboarding-1 → onboarding-2 → dashboard (empty)
```

For each flow name the point where users most often abandon and what the design must do there. A flow that ends on a page with no next action is a gap; record it.

Navigation follows from the inventory: global navigation holds only core pages; secondary pages live in the footer, a settings area, or contextual links. State the mobile navigation pattern explicitly.

## 4. Check content reality

Design fails quietly when it is drawn around invented copy. For each core page note what real content exists. Where it does not, plan sample content that matches the real length and shape (a real-length product name, a realistic price table, a 40-row list), and mark it as sample. Never present invented testimonials, customer logos, statistics, or awards as if they were real; leave a labelled slot instead.

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

The `Layout`, `Mockup`, and `Code` columns track progress per page: `pending` → `options-shown` → `approved` (or `done` for code). Update the row the moment a state changes. This file is how a later session resumes multi-page work without redoing approved pages.

## 6. Approval

Present the inventory table and the flows, recommend what to cut or defer, and ask the user to approve the list. Adding a page later is cheap; designing a page nobody needs is not. Do not start page layouts until the inventory is approved or the user explicitly delegates it.
