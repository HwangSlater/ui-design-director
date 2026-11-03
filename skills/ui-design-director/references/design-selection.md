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

## 2. Find well-known real sites first

The strongest motif is a site that already runs in the same field and that people recognise. Owners judge the result against the sites they use ("compared with sites that actually run, it looks too simple"), and a famous site in their own field is something they can read without design vocabulary; a template or an unrelated showcase is not ("a German train site — I'd have asked why"). Templates come second.

Derive the search from the brief, not from a gallery: the **field** (futsal league, piano school, pottery shop), the **job** of the main screen (find my next match, book a trial lesson, buy a mug), the **concept words** (scoreboard, warm and calm, editorial) and the **audience** (office workers on phones, parents, gift buyers). Then look in this order and stop when you have 5–8 strong candidates:

1. **Leaders in the same field** — the sites that define it, domestic and international: for a futsal league the national league and federation sites, the big league and score services (K League, Premier League, LaLiga, FotMob, ESPN), and the leading local amateur-sport service (PLAB); for a ceramics shop the well-known studios and craft brands; for a music school the best-known academies and lesson platforms. Prefer sites with many real users or a reputation in the field over portfolio pieces.
2. **Leaders with the same main job in a neighbouring field** — when the field has few good sites: a booking leader for a class schedule, a transit or match-centre product for "what is next, where, when".
3. **Award and showcase entries in that category** — Awwwards, CSS Design Awards, Godly, Landbook, filtered by the field (Sports, Music, Shop), for one strong trait each.
4. **Templates** — Framer Marketplace, Webflow, SaaSFrame, design-system docs for tools — only when a structure is needed that the real sites do not show (a sign-up form, an admin screen), or when the user wants to buy a starting point.

For each real site record what it is known for and which visual layers it carries (`reference-extraction.md` § Visual layers), because those layers are what the motif borrows. A famous site is a motif, not a source: borrow its grammar and layers, never its logo, illustrations, photos, text or a distinctive composition verbatim, and say so to the user.

When ui-ux-pro-max is installed, its style and product-pattern search can suggest directions to look for (`companion-skills.md`). A suggestion becomes a candidate only after a real site or template in that direction has been opened and inspected.

Use real sites and showcases for visual language and patterns; use templates when adopting page structure is plausible. Never imply that an inspiration item can be copied or purchased.

## 3. Curate candidates

Lead with the well-known real sites from § 2 and mark which candidate is a running site in the field, which is a neighbouring-field leader, and which is a template. A user without design vocabulary cannot read "just look at the mood" off a site whose content is unrelated: a piano-school owner shown a pharmacy app, a tool-rental shop and a children's English game could not picture her own page. Prefer candidates from the same or a neighbouring trade, and when the direction is still hard to read, render two or three directions with the user's own content in their language (as the layout step does) before asking them to choose; the layout step with real content was the one the user found most useful.

**Do not settle on the default reading of the brief.** Words such as “warm”, “clean” or “calm” have many readings but drift to one default: “warm” became cream paper, a brown button, a rounded heading face and a text-left/photo-right first screen for both a pottery studio and a piano school, and the two sites looked like one company's. Before presenting, write down the default you would reach for from the brief words alone, keep at most one part of it in any candidate unless the brief's own evidence calls for it (the user's wall colour, an existing sign, a font they insist on), and say which part you kept and why.

A reference from another trade can still be the right source for one trait (a train departure board for "the next match in three seconds"), but on its own it reads as irrelevant to an owner ("I'd have asked: why this?"). Show such a trait applied to the user's own content in the same step — one row of their data in that shape — rather than asking them to imagine it.

Present 5–8 individual candidates with working detail or preview links, not gallery homepages. The set should cover 2–4 relevant concept territories while remaining plausible for the product. Avoid near-duplicates, trend-only picks, and deliberately weak decoys.

Inspect enough of each candidate to evaluate it. Prefer candidates with multiple relevant pages, responsive previews, and visible component/state coverage. A beautiful hero with no evidence for the product's core screens is a secondary visual reference, not a whole-system candidate.

For every candidate include:

- name, direct link, source, and free/paid/inspiration-only status when known;
- kind: running site in the field / leader in a neighbouring field / award entry / template, and what it is known for;
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
