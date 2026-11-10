# Selecting the overall design concept

## 1. Create the concept brief

Derive what is safe from the repository and conversation, then confirm only consequential unknowns:

- product type, primary user, main job, and interaction archetype;
- essential page types and the most information-dense screen;
- desired brand traits; trust, familiarity, distinctiveness and conversion needs;
- mobile/desktop priority and accessibility constraints;
- existing logo, palette, typeface, component library, or technical constraints;
- explicit dislikes and examples the user considers “too much” or “too plain”;
- **what only this business has**: two or three materials, objects, places or habits of this trade or community (a pottery studio: clay, the wheel, glaze drips). At least one candidate direction is built around one of them, so the site could not be mistaken for another field;
- whether paid templates are acceptable and whether the goal is inspiration or licensed reuse;
- **photos taken in one sitting**: ask for one session of everything sold or shown — same light, same surface, full phone resolution — plus the storefront and sign if customers find the place in person. For a marketplace or app, ask what a real listing or screen looks like instead;
- **2–3 photos per item** (front, side or cut face, in a hand), taken the same way; say what one photo per item will cap;
- **the package first**: on a product page the first photo is what the customer receives (bag, box, label), the contents second. A stand-in product photo never ships — customers take any photo on a product page for the thing they will receive;
- **the five questions customers ask most** (by phone, chat or support; ask in those words). They become the page order, the form's questions and the facts to collect.

Summarize these as **confirmed**, **inferred**, and **open**.

## 2. Search two kinds of source side by side

- **Well-known real sites in the field** — what owners compare their result with and can read without design vocabulary.
- **Template marketplaces** — Framer Marketplace, Webflow Templates, ThemeForest, SaaSFrame, and design-system docs for tools. They often show the screens real sites hide (sign-up, checkout, admin).

Derive the search from the brief, not from a gallery: the **field**, the **job** of the main screen (find my next match, book a trial lesson, buy a mug), the **concept words** and the **audience**. Use the same words for both kinds of source.

Real sites, best first:

1. **Leaders in the same field**, domestic and international (futsal: K League, FotMob, PLAB). Prefer sites with many real users over portfolio pieces.
2. **Leaders with the same main job in a neighbouring field**, when the field has few good sites: a booking leader for a class schedule, a transit product for "what is next, where, when".
3. **Only when the first two give fewer than five:** award and showcase entries in that category (Awwwards, CSS Design Awards, Godly, Landbook) for one strong trait each.

Templates: search each marketplace's category and keyword for the field and the main job, open the live preview, and judge it like a real site — its visual layers, phone layout, and coverage of the product's core screens. Prefer previews with several real pages over single landing pages.

**Quality bar.** A candidate is a site a working designer would show as a good example: many real users, a known brand, or an award. A small local shop's own site is not a base candidate even when it is in the same field — it sets the ceiling of the result (dog groomer 18th: two small Japanese salons, a local salon and a template; the client found the result poor before judging anything else). When the field has few such sites (a neighbourhood trade), take leaders with the same main job from neighbouring fields — booking a service (hair and nail booking, clinics), a pet brand or pet-care app — and keep local shops only for the client's named channels.

**Fits the customers.** A foreign site brings its country's web style (dense small text and centred thin titles on many Japanese local sites). Recommend one only when that style suits the client's customers, and say why; otherwise recommend a site their customers already use or a global brand.

Aim for about five well-known running sites and one or two templates, and say which is which. Record for each what it is known for (real site) or covers (template), and which visual layers it carries (`build-rules.md` § Follow the base 6). Use a template's code or assets only within its licence, and tell the user a real site is a motif, not something to copy or buy.

## 3. Curate candidates

Mark each candidate as a running site in the field, a neighbouring-field leader, an award entry, or a template. Prefer the same or a neighbouring field: an owner cannot picture their page from a site whose content is unrelated. Cover 2–4 concept territories; avoid near-duplicates, trend-only picks and weak decoys.

**Do not settle on the default reading of the brief.** Words such as “warm”, “clean” or “calm” drift to one default (“warm” gave two different trades the same cream paper and brown button). Before presenting, write down the default you would reach for from the brief words alone, keep at most one part of it in any candidate unless the brief's evidence calls for it (the user's wall colour, an existing sign), and say which part you kept and why.

A reference from another field can be the right source for one trait (a train departure board for "the next match in three seconds"); show that trait applied to one row of the user's own data in the same step.

Two candidates are not optional: every site or channel the client named (Naver Place, Instagram, Kakao, a competitor — customers see those first), and at least one site that shows what the client called most important (before-and-after photos for a renovation firm). If a named site cannot be captured cleanly, include it anyway with a note.

Before sending, read the words inside every screenshot — badges (「Made in Framer」), founding years (「SINCE 1952」), certification claims, promo bands — against the brief's dislikes and the client's facts, and say that none of it carries over. Show, next to the recommended candidate's home page, its screen for the client's main job.

A beautiful hero with no evidence for the product's core screens is a trait-only reference, not a whole-system candidate. The recommendation names a visual reason (photos, type, finish), not only functions on the first screen. Record for each candidate in `formats/` (not in chat): link, kind, why it is well known, its country, licence status when known, one transferable trait, and scope — **whole-system**, **marketing-only**, **product-UI-only**, or **trait-only**.

## 4. Make comparison easy

Include running sites from the user's own country and language, shown at phone width first. Show the candidates on the board (`comparison-board.md` § The board).

Before asking, run `node ${CLAUDE_SKILL_DIR}/scripts/skeleton.mjs formats/뼈대-390.md --width 390 name=url …` and again at 1280 on the shortlist, templates included (pages from one platform such as Naver Place count as one site), and put the shared traits with counts in the message (「사진이 첫 화면을 채움 4/6곳」), phone and desktop separately.

In chat: licence and reuse status, what could not be verified, and one or two recommended finalists tied to the brief's content and task.

Ask the user for:

1. **one base** — the template or site the whole site will look and be laid out like. When the client names several, ask which is the base; the others become named traits;
2. definite rejections and why;
3. optionally one named trait from a secondary reference (“B's type hierarchy”, not “mix B and C”).

If no candidate fits, use the user's reactions as new constraints and return a narrower second shortlist.

## 5. Record the choice

Before extraction, state the proposed selection record and obtain confirmation:

- primary reference and direct URL;
- selected secondary trait(s) and their scope;
- rejected directions and the reason;
- known licensing/reuse status;
- confirmed product-specific departures from the reference;
- whether the template's original palette is rejected, retained as a finalist, or undecided.

Hold this record until the palette decision is also recorded; together they become the first entries in `DESIGN.md`'s decision log.

For a single component or minor page, two or three targeted references may replace the full shortlist. Do not use that exception for an overall product concept.
