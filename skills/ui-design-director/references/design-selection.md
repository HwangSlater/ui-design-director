# Selecting the overall design concept

This phase helps the user select the overall visual structure and component character before rules or production code are produced. Palette selection is separate; read `color-selection.md` after or alongside this phase.

## 1. Create the concept brief

Derive what is safe from the repository and conversation, then confirm only consequential unknowns:

- product type, primary user, main job, and interaction archetype: marketing site, dashboard, editing tool, form workflow, or content reader;
- essential page types and the most information-dense screen;
- desired brand traits and emotions;
- trust, familiarity, distinctiveness, and conversion needs;
- mobile/desktop priority and accessibility constraints;
- existing logo, palette, typeface, component library, or technical constraints;
- explicit dislikes and examples the user considers “too much” or “too plain”;
- **what only this business has**: two or three materials, objects, places or habits of this trade (a pottery studio: clay texture, the wheel, glaze drips; a piano school: the black-and-white rhythm of keys, staff lines, the apartment-block shop sign). At least one candidate direction is built around one of them, so the site could not be mistaken for another trade;
- whether paid templates are acceptable and whether the goal is inspiration or licensed reuse.

Summarize these as **confirmed**, **inferred**, and **open**. Do not force a lengthy questionnaire when repository evidence is sufficient.

## 2. Search the right libraries

Use live web research because catalogs and links change. Search multiple relevant sources rather than one marketplace only:

- Framer Marketplace for polished marketing, startup, portfolio, editorial, and commerce templates;
- Webflow Templates and Made in Webflow for responsive multi-page structures and cloneable community work;
- Landbook for curated websites and landing-page directions;
- SaaSFrame for SaaS marketing pages, product UI, onboarding, pricing, and dashboard flows;
- published design-system documentation and its component gallery when the archetype is a tool or application rather than a site;
- a better current domain-specific marketplace/gallery when the product warrants it.

When ui-ux-pro-max is installed, its style and product-pattern search can suggest directions to look for (`companion-skills.md`). A suggestion becomes a candidate only after a real template or showcase in that direction has been opened and inspected.

Let the archetype pick the sources. Template marketplaces overwhelmingly sell marketing pages; for a tool or a dense workflow, design-system documentation is where component, density, and state coverage is actually visible.

Use template sources when adopting page structure is plausible. Use showcases when only visual language or interaction patterns are needed. Never imply that an inspiration item can be copied or purchased.

## 3. Curate candidates

A user without design vocabulary cannot read "just look at the mood" off a site whose content is unrelated: a piano-school owner shown a pharmacy app, a tool-rental shop and a children's English game could not picture her own page. Prefer candidates from the same or a neighbouring trade, and when the direction is still hard to read, render two or three directions with the user's own content in their language (as the layout step does) before asking them to choose; the layout step with real content was the one the user found most useful.

**Do not converge on your last project.** Brief words such as “warm”, “clean” or “calm” have many readings, but they drift to one default: a pottery studio and a piano school, briefed a day apart, both came out as cream paper, a brown button, the same heading face and a text-left/photo-right first screen, and the user said they looked like one company's sites. Before presenting, look at the other `*-시안` folders beside this project and name what they settled on (background, action colour, heading face, first-screen composition). Keep at most one of those in any candidate unless the user asked for it, and say which one you kept and why.

Present 5–8 individual candidates with working detail or preview links, not gallery homepages. The set should cover 2–4 relevant concept territories while remaining plausible for the product. Avoid near-duplicates, trend-only picks, and deliberately weak decoys.

Inspect enough of each candidate to evaluate it. Prefer candidates with multiple relevant pages, responsive previews, and visible component/state coverage. A beautiful hero with no evidence for the product's core screens is a secondary visual reference, not a whole-system candidate.

For every candidate include:

- name, direct link, source, and free/paid/inspiration-only status when known;
- screenshot/thumbnail when tools allow;
- concept territory and brand impression;
- why it fits the brief;
- relevant pages/components actually observed;
- one strong transferable trait;
- mismatch, risk, and expected adaptation cost;
- **whole-system**, **marketing-only**, **product-UI-only**, or **trait-only** scope.

Do not state unverified prices, licenses, responsiveness, or page coverage as fact.

## 4. Make comparison easy

Show the candidates in the full-screen viewer described in `comparison-board.md`: capture the product's key pages at desktop and phone width, build the viewer, check it, and open it in the user's browser. Do not present a table of links or a folder of screenshots as the comparison.

In chat, keep to what the screens cannot show: licence and reuse status, what could not be verified, and a recommendation of one or two finalists tied to the brief. Explain why the recommendation fits the real content and user task, not merely why it looks fashionable.

Ask the user for a simple decision:

1. primary reference;
2. definite rejections and why;
3. optionally one named trait from a secondary reference.

Examples of valid secondary traits: “B's type hierarchy,” “C's dashboard density,” or “D's restrained motion.” “Mix B and C” is too vague; resolve which traits govern which layer.

If no candidate fits, use the user's reactions as new constraints and return a narrower second shortlist. Do not pressure the user into choosing.

If the user explicitly delegates the choice, select the strongest candidate using the concept brief, state that the choice was delegated, and continue only through the scope they authorized.

## 5. Record the choice

Before extraction, state the proposed selection record and obtain confirmation:

- primary reference and direct URL;
- selected secondary trait(s) and their scope;
- rejected directions and the reason;
- known licensing/reuse status;
- confirmed product-specific departures from the reference;
- whether the template's original palette is rejected, retained as a finalist, or undecided.

Hold this format-selection record until the palette decision is also recorded. Together they become the first entries in `DESIGN.md`'s decision log. A requested coded preview may be created before final approval, but it is not the design system or production UI.

For a single component or minor page, two or three targeted references may replace the full shortlist. Do not use that exception for an overall product concept.
