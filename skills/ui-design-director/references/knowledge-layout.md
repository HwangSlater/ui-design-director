# Layout and visual design: rules for a design agent

Researched 2026-11-09 from free material by practising designers, research groups and design-system teams; each rule links its source, rewritten in our own words. Rules here are background: `build-rules.md` and the chosen base win when they disagree. Read only the section you need.

## Contents
- 1. Sources
- 2. Rules
- 3. Disagreements between sources
- 4. What makes a page look templated or generated (per the sources)
- 5. Could not access

Scope: layout, spacing, visual hierarchy, composition, grids, responsive layout, imagery, icons, depth/shadows/borders, component styling (buttons, cards), and what makes a page look templated or generated. Target: website pages for Korean small businesses, services, shops and public sites.

All rules are paraphrased. Numbers are the source's own. "Date read" is 2026-11-09 for every row.

## 1. Sources

| # | Title | Author | Credentials | URL | Published |
|---|---|---|---|---|---|
| S1 | 7 Rules for Creating Gorgeous UI, Part 1 (2024 update) | Erik D. Kennedy | Runs Learn UI Design course; UI work for Fortune 100 and YC startups; designed the Figtree font | https://www.learnui.design/blog/7-rules-for-creating-gorgeous-ui-part-1.html | updated 2024-06-15 |
| S2 | 7 Rules for Creating Gorgeous UI, Part 2 | Erik D. Kennedy | as S1 | https://www.learnui.design/blog/7-rules-for-creating-gorgeous-ui-part-2.html | updated 2024-06-15 |
| S3 | The King vs. Pawn Game of UI Design | Erik D. Kennedy | as S1 | https://www.learnui.design/blog/king-vs-pawn-game-ui-design.html | updated 2021-08-07 |
| S4 | 3 Pro Tips on Alignment | Erik D. Kennedy | as S1 | https://www.learnui.design/blog/3-pro-tips-on-alignment.html | 2018-11-03 |
| S5 | The 3 Laws of Locality | Erik D. Kennedy | as S1 | https://www.learnui.design/blog/the-3-laws-of-locality.html | 2019-07-31 |
| S6 | Spacing Homework: Common Mistakes | Erik D. Kennedy | as S1 | https://www.learnui.design/blog/spacing-hw.html | undated |
| S7 | Refactoring UI home page (free tip "Use fewer borders" + free ToC) | Adam Wathan, Steve Schoger | Creators of Tailwind CSS / Tailwind UI; Schoger is a working UI designer | https://www.refactoringui.com/ | undated |
| S8 | Designing Beautiful Shadows in CSS | Josh W. Comeau | Former Gatsby/Khan Academy/DigitalOcean engineer, CSS educator (CSS for JS Developers) | https://www.joshwcomeau.com/css/designing-shadows/ | 2021-09-13, upd. 2026-04-27 |
| S9 | An Interactive Guide to Flexbox (design-level advice only) | Josh W. Comeau | as S8 | https://www.joshwcomeau.com/css/interactive-guide-to-flexbox/ | 2022-11-22, upd. 2026-04-27 |
| S10 | Learn Responsive Design: Macro layouts | Jeremy Keith (Clearleft) for Google web.dev | Co-founder Clearleft; course planned by Una Kravets (Google) | https://web.dev/learn/design/macro-layouts | 2021 |
| S11 | Learn Responsive Design: Micro layouts | as S10 | as S10 | https://web.dev/learn/design/micro-layouts | 2021 |
| S12 | Learn Responsive Design: Media queries | as S10 | as S10 | https://web.dev/learn/design/media-queries | 2021 |
| S13 | Learn Responsive Design: Responsive images | as S10 | as S10 | https://web.dev/learn/design/responsive-images | 2021 |
| S14 | Learn Responsive Design: Interaction | as S10 | as S10 | https://web.dev/learn/design/interaction | 2021 |
| S15 | Learn Responsive Design: Icons | as S10 | as S10 | https://web.dev/learn/design/icons | 2021 |
| S16 | Every Layout: Axioms | Heydon Pickering, Andy Bell | Independent front-end/UX practitioners, authors of Inclusive Components / Piccalilli | https://every-layout.dev/rudiments/axioms/ | undated |
| S17 | Every Layout: Modular scale | as S16 | as S16 | https://every-layout.dev/rudiments/modular-scale/ | undated |
| S18 | Every Layout: The Stack | as S16 | as S16 | https://every-layout.dev/layouts/stack/ | undated |
| S19 | Every Layout: The Sidebar | as S16 | as S16 | https://every-layout.dev/layouts/sidebar/ | undated |
| S20 | GOV.UK Design System: Layout | GOV.UK Design System team (UK Government Digital Service) | Official government design system | https://design-system.service.gov.uk/styles/layout/ | living doc |
| S21 | GOV.UK Design System: Spacing | as S20 | as S20 | https://design-system.service.gov.uk/styles/spacing/ | living doc |
| S22 | GOV.UK Design System: Button | as S20 | as S20 | https://design-system.service.gov.uk/components/button/ | living doc |
| S23 | KRDS (Korea Design System): Layout / grid / spacing | Ministry of the Interior and Safety (행정안전부) KRDS team | Official Korean government design system | https://www.krds.go.kr/html/site/style/style_05.html | living doc |
| S24 | Apple HIG: Layout (read via the page's JSON data) | Apple design team | Official platform guideline | https://developer.apple.com/design/human-interface-guidelines/layout | living doc |
| S25 | Use window size classes (Material 3 breakpoints) | Android Developers / Google | Official; maps to Material 3 layout guidance | https://developer.android.com/develop/ui/compose/layouts/adaptive/use-window-size-classes | living doc |
| S26 | Visual Hierarchy in UX: Definition | Kelley Gordon, Nielsen Norman Group | NN/g UX specialist; NN/g = research-based UX consultancy | https://www.nngroup.com/articles/visual-hierarchy-ux-definition/ | 2021-01-17 |
| S27 | Cards: UI-Component Definition | Page Laubheimer, NN/g | NN/g senior UX specialist | https://www.nngroup.com/articles/cards-component/ | 2016-11-06 |
| S28 | Photos as Web Content | Jakob Nielsen, NN/g | Co-founder NN/g | https://www.nngroup.com/articles/photos-as-web-content/ | 2010-10-31, reviewed 2026 |
| S29 | Icon Usability | Aurora Harley, NN/g | NN/g UX specialist | https://www.nngroup.com/articles/icon-usability/ | 2014-07-27 |
| S30 | Flat UI Elements Attract Less Attention and Cause Uncertainty | Kate Moran, NN/g | NN/g; eyetracking study, 71 users | https://www.nngroup.com/articles/flat-ui-less-attention-cause-uncertainty/ | 2017-09-03 |
| S31 | Design Principles: Dominance, Focal Points and Hierarchy | Steven Bradley, Smashing Magazine | Designer, author of *Design Fundamentals* | https://www.smashingmagazine.com/2015/02/design-principles-dominance-focal-points-hierarchy/ | 2015-02-27 |
| S32 | Practical Design Tips and Guidelines for Beginner Designers | Laurent Baumann, Smashing Magazine | Product designer/leader since 2005 | https://www.smashingmagazine.com/2023/05/practical-design-tips-guidelines-beginner-designers/ | 2023-05-22 |
| S33 | The Dribbblisation of Design | Paul Adams, Intercom blog | Former Facebook/Google product designer, VP Product at Intercom | https://www.intercom.com/blog/the-dribbblisation-of-design/ | 2013-09-18 |
| S34 | 토스 디자이너가 제품에만 집중할 수 있는 방법 (TDS menu redesign) | 박수현, Toss platform designer | Toss Design System team | https://toss.tech/article/toss-design-system | 2024-03-05 |
| S35 | [미디클] 라디오 vs 체크박스 | Toss 미스터리 디자인 클럽 | Toss product designers | https://toss.tech/article/mysterydesignclub1 | 2025-01-20 |
| S36 | 앱인토스 UI/UX 가이드 | Toss (Viva Republica), Apps in Toss | Official Toss partner guideline | https://developers-apps-in-toss.toss.im/landing-page/landing-page-en/design/consumer-ux-guide | undated |
| S37 | 셀프서비스 디자인시스템 #1 – 디자이너 편 | 태주희, 우아한형제들 배민사장님디자인팀 | Baemin platform designer | https://techblog.woowahan.com/6305/ | 2021-10-20 |

## 2. Rules

Format: **rule** — why — source.

### 2.1 Spacing and white space

1. **Start from generous space; add elements into it, not space between them.** When a screen feels cramped, try roughly doubling space between lines, between elements and between groups before changing anything else. — Default HTML/CSS starts at zero spacing and reads as cramped; space alone makes a layout look intentional. — S1
2. **Group with space first; add lines or background fills only if space is not enough.** — Space is the only grouping cue that adds no element; dividers and fills add clutter. — S6, S7, S26
3. **Inside a group, gaps are smaller than gaps between groups (proximity).** Check every pair: label to field < field to next field < section to section. — People read close items as related. — S26, S32, S24
4. **Use one spacing scale and only its steps.** Options: 4/8-pt (KRDS: all spacing on an 8-point grid; tokens 8, 16, 24, 32, 40, 64 px), GOV.UK scale 5, 10, 15, 20, 25, 30, 40, 50, 60 px, or a modular scale with one ratio (Every Layout: ratio 1.5 from 1rem → 1, 1.5, 2.25, 3.375). — Arbitrary values break rhythm; irregular gaps pull attention away from the focus. — S23, S21, S17, S32
5. **Shrink large spacing steps on small screens, keep small ones fixed.** GOV.UK: steps 0–3 (≤15px) are the same everywhere; step 9 is 60px desktop, 40px mobile; switch at 640px. — Big desktop gaps waste a phone screen; small inner gaps must stay readable. — S21
6. **Tie the base vertical gap to body line-height.** With 1rem text at line-height 1.5, the default gap between stacked blocks is 1.5rem; larger gaps are multiples (3rem, 4.5rem). — One line of text is the natural unit of a text-heavy page. — S17, S18
7. **Put spacing on the parent ("stack"), not on each child.** Space only between siblings (`* + *`), so containers get no stray top/bottom margin. Push a footer action to the bottom of a card with an auto margin rather than a fixed gap. — Margin is a relationship between neighbours; avoids doubled padding. — S18
8. **Korean public-site spacing reference (KRDS):** header→breadcrumb 24px; breadcrumb→H1 32–40px; content→footer 40–64px; card list gap 24px; stacked inputs 16–24px; label/helper/input/message stack 8px; input inner padding 16px; checkbox/radio vertical 16–24px, horizontal ≥24px. — Official values Korean users meet on government sites. — S23
9. **Inner padding of a text box is equal on all four sides, measured from the x-height, not the line box.** — Line boxes add invisible space above caps; centring on x-height looks centred. — S32
10. **An image inside a box gets a margin of at least half its shorter side.** — Smaller margins make the image feel jammed against the frame. — S32
11. **Nested rounded boxes: inner radius = outer radius − gap**, never the same radius. — Same radius on both gives an uneven band. — S32

### 2.2 Visual hierarchy

12. **One dominant element per view; at most three levels of emphasis (dominant, sub-dominant, subordinate).** — People reliably tell apart about three levels; each extra level weakens contrast between neighbours. Two dominant items compete. — S31, S26
13. **No more than three type sizes in a block, and at most two "large" elements on a screen.** Typical web: body 14–16px, subheads 18–22px, headings up to 32px. — More sizes flatten hierarchy. — S26
14. **Normal UI text (body, nav, buttons, captions) varies by no more than ~2pt** (e.g. body 18, nav/buttons 16, captions 14); only headings break out. — Wide size scatter reads as inconsistent. — S6
15. **Only the page title is fully "loud" (big + bold + high contrast).** Every other element mixes loud and quiet properties (e.g. small but bold uppercase label; large number but light weight and lighter grey). — Stacking all emphasis everywhere removes contrast. — S2
16. **De-emphasise with size, weight, contrast, case, tracking or margin; never with underline (reads as a link), background highlight or strikethrough.** — Those carry other meanings. — S2
17. **Hover/selected states change colour, background, shadow or small offset, not size, weight or case.** — Size/weight changes shift layout. — S2
18. **Run the squint/blur test** (blur 5–10px): the intended order must still be visible; check again with real photos in place. — Strong imagery can override intended hierarchy. — S26
19. **Order content by importance top → bottom and leading → trailing; indent to show subordination.** — Reading order. — S24, S27
20. **Design in greyscale first, then add one accent colour.** — Forces hierarchy to come from size, space and layout, not colour. — S1, S26 (max 2 primary + 2 secondary colours in simple designs)

### 2.3 Alignment and composition

21. **Align to as few edges as possible; pick the scheme that gives the cleanest edges.** Ragged right edges of left-aligned text do not count as an edge. — Fewer, stronger edges look tidy. — S4
22. **Hang bullets, icons and opening quote marks outside the text edge.** — Keeps the text's left edge clean. — S4
23. **Body text left-aligned; line length 8–12 words for main text, 5–6 for sidebars/captions.** — Comfortable reading; justified text needs hand tuning. — S32
24. **Centre polygons (play, star icons) on their circumscribed circle, not their bounding box.** — Optical centre differs from geometric centre. — S32
25. **Place a control on the thing it changes; controls for a whole list go above the list; the farther a control is from its target, the more it must stand out.** Keep the primary form action at the end of the form flow, not a far corner. — Users look for controls near the object. — S5
26. **Vary section layouts by a simple rule (e.g. alternate image left/right), and mark section starts/ends with a repeated element.** — Gives rhythm without chaos. — S32

### 2.4 Grids and page width

27. **Cap reading width: measure ≤ 60ch (Every Layout), ≤ ~75 characters (GOV.UK); acceptable range 45–75.** Set it in `ch`, not px. — Long lines tire readers; `ch` scales with font size. — S16, S20
28. **Max page content width: GOV.UK 1020px; KRDS 1200px (with 24px side margins it stays 1200 from 1248px viewport up).** — Wide screens otherwise stretch lines and gaps. — S20, S23
29. **Main reading content sits in a two-thirds column (GOV.UK)**; standard splits are 1/2+1/2, 2/3+1/3, 3/4+1/4. — Keeps measure in range while leaving a side column. — S20
30. **KRDS grid: 4 cols at ≥360px (gutter 16, margin 16), 8 cols at ≥768 (gutter 16–24, margin 24), 12 cols at ≥1024/1280 (gutter 24, margin 24); gutter ≤ half a column; never mix column counts on one screen.** — Official Korean grid; edge margins prevent mis-taps. — S23
31. **Use percentage columns, not fixed pixel widths/heights.** — Fixed sizes break responsive layout. — S16, S23

### 2.5 Responsive layout

32. **Mobile first: single column in source order, then widen.** Confirm content order makes sense before any layout. — Small screens use the source order. — S10, S20, S37
33. **Choose breakpoints where the content breaks, not at device widths; use `em` in media queries.** Example: two columns from 45em; two text columns only beyond ~50em. — Device sizes change every year. — S12, S10
34. **Prefer intrinsic layouts that need no media query:** card grid `repeat(auto-fill, minmax(15em, 1fr))` with 1em gap; sidebar that wraps when main content would drop below 50% width. — Fewer breakpoints, works in any container. — S10, S19, S16, S9
35. **Components respond to their container (container queries), pages to the viewport.** Example: media object stacks below 25em container width. — The same card may sit in a wide main column or a narrow sidebar. — S11
36. **If you need named breakpoints, use Material/Android widths: compact <600, medium 600–839, expanded 840–1199, large 1200–1599, extra-large ≥1600 (dp ≈ CSS px); or KRDS 360/768/1024/1280/1440 for Korean sites.** — Covers >93% of devices per class. — S25, S23
37. **Keep the same functions at every size; change only how much is shown (e.g. tab bar → sidebar).** Test the smallest and largest widths and the largest text size first. — Users switch devices; extremes reveal clipping. — S24
38. **Let text grow: support browser zoom/large text; stack side-by-side items when text gets large; set min/max widths in relative units.** Toss found many labels ≥5 characters and set menu widths as % of screen. — Korean labels and enlarged text overflow fixed widths. — S24, S34
39. **Do not infer touch vs mouse from width; use `pointer: coarse` to enlarge targets, never shrink targets for fine pointers.** — Fitts's law applies to everyone. — S14
40. **Never put essential content or controls behind hover; any hover reveal also opens on focus.** — Touch users cannot hover; keyboard users need parity. — S14, S29
41. **Toss mobile reference: base design width 360–420px (Figma base 375px); test on 3–5 real devices including one small screen and one with a large safe area.** — Covers 70–80% of Toss traffic. — S36

### 2.6 Imagery and photography

42. **Use photos that carry information: the actual product, shop, food, staff, place. Skip generic stock and "feel-good" filler.** — Eyetracking: users ignore decorative stock; real staff photos got ~10% more viewing time than bios that were 3× larger; generic thumbnails drew only 18% of viewing time. — S28
43. **Show detailed, specific product photos with alternate views; enlargements at least 2× the default.** — Users study detail when they choose it. — S28
44. **One primary graphic per screen; others become small icons.** Size graphics by information density; never let them cover key information or force extra scrolling. — Competing graphics outweigh text and CTA. — S36
45. **Text over photos: never rely on plain text on an uncontrolled image. Use a dark overlay (~35% black), a semi-opaque box behind the text, blur, or a bottom fade (0% → ~20% black).** Use white text. — Photos change and crop at different widths. — S2
46. **Always give images `width`/`height` (or `aspect-ratio`) and `object-fit: cover` with a set `object-position`; `max-inline-size: 100%`.** — Prevents layout jump and squashed photos. — S13
47. **Lazy-load below-the-fold images; load the hero eagerly and give only the LCP image `fetchpriority="high"`.** — Perceived speed. — S13
48. **Every image has `alt`; decorative ones `alt=""`; prefer CSS for purely decorative imagery.** — Screen readers. — S13
49. **Scale background art to fill; never distort its aspect ratio.** — S24

### 2.7 Icons

50. **Pair icons with visible text labels, except the few universal ones (home, search magnifier, print).** — Most icons are ambiguous; "obscure icon = wasted feature". — S29, S15
51. **If you cannot find a fitting icon in ~5 seconds, use a word instead.** — The concept probably has no clear icon. — S29
52. **One meaning per icon across the whole site.** — Inconsistent icons cannot be learned. — S29
53. **Match icon stroke weight to adjacent text weight, and icon corner radius to the font's corners.** — Reads as one unit. — S32, S3
54. **Size icons relative to text (≈1em) and scale them with text size.** Toss scales icons together with large text to keep hierarchy. Display range 24–40px for standalone icons (Toss). Menu (hamburger) icon ~20px wide, not 44px. — Oversized icons shout; fixed icons break under large text. — S15, S34, S36, S6
55. **Never stack two icons or icon + emoji on one item.** — Visual noise. — S36
56. **Use inline SVG; decorative icons `aria-hidden`; icon-only buttons need an accessible name.** — S15
57. **On desktop show navigation as text links instead of hiding it behind an icon.** — Icons that stand out on phones get lost on large screens. — S29

### 2.8 Depth, shadows, borders

58. **One light source for the whole page, from above (slightly left).** Lighter top edges, darker bottoms; raised items (buttons, cards, menus) cast shadows, recessed ones (inputs, tracks, checkboxes) look inset. — Mixed light directions look like blurry borders, not depth. — S1, S8
59. **All shadows share one x:y ratio (y = 2x) and grow together: higher elevation = larger offset, larger blur, lower opacity.** Define 3 named levels (small, medium, large) as tokens. — Consistency reads as a coherent space. — S8
60. **Tint shadows with the background hue (lower saturation and lightness), not pure black; layer several low-opacity shadows for softness (e.g. 5 layers at 0.075).** — Black shadows grey out coloured backgrounds. Avoid many layers on low-end phones and don't animate them. — S8
61. **Shadow and border strength follow background luminance:** on a mid-tone button a light shadow (0 1px 2px, 30% black) and 1px border at ~20% black; on dark buttons stronger (0 2px 4px, 50%; border ~50%). — The same shadow looks wrong on different luminances. — S3
62. **Keep "flatty", not ultra-flat: clickable things keep at least one cue (fill, shadow, contrasting colour, underline).** — Weak signifiers took 22% longer to find and caused 25% more fixations; ghost buttons and text-styled links were missed. Flat works only with low density, conventional layout and high-contrast actions. — S30, S1
63. **Use fewer borders: replace with a shadow, a background contrast or more space.** — Many borders make a design busy. — S7
64. **Overlays/popups can be lightened with background blur plus a thin bright outline instead of a heavy dark scrim.** — Toss uses this to reduce weight. — S34

### 2.9 Buttons

65. **One primary (filled) button per view; supporting actions secondary.** — Several primaries compete and hide the next step. — S22, S5
66. **Button label = the specific action in sentence case ("저장하고 계속", "주소 추가"); do not repeat on-screen text in the CTA.** — Says what happens next. — S22, S36
67. **Align the primary button to the form's left edge, inside the flow.** — Users finish forms there. — S22, S5
68. **Avoid disabled buttons; show why instead.** Destructive actions use a warning style only with a confirmation step and explanatory text (not red alone). — Disabled buttons have poor contrast and confuse. — S22
69. **Baseline button: 40px tall with 20px horizontal padding at 16px text; touch targets ≥44×44pt.** Larger padding under `pointer: coarse` (e.g. 1em 2em). — Default proportions; finger accuracy. — S3, S24, S14
70. **Radius, letter-spacing and shape follow the typeface:** rounded font → small radius (~3px); squared font → square corners; uppercase labels get added tracking. — Make deliberate choices instead of defaults. — S3
71. **Prevent double submit and show progress while waiting.** — Slow connections cause duplicate sends. — S22
72. **Give touch feedback (one-step darker background or haptic).** — S34
73. **On mobile, prefer large row-style choices over tiny round radios; make selection count clear from the question text.** Toss test: 13/15 chose correctly regardless of control shape. — Small circles are poor finger targets; context matters more than control shape. — S35

### 2.10 Cards and lists

74. **Use cards for browsing mixed content types (service menu with different kinds of items, dashboards). Use a list for similar items to compare (prices, schedules) and a plain grid for photo galleries.** — Cards are less scannable and harder to compare; they take more space. — S27
75. **Card build: one container, image → title → short summary → action; fixed width, height follows content; whole card is the link; secondary actions separated (e.g. by a rule).** — Bigger target, clear information scent. — S27
76. **Card signal: border or contrasting background, optional slight shadow.** — Signals grouping and clickability. — S27, S30
77. **Keep the same internal layout across cards in one set.** — Users compare back and forth. — S27
78. **Missing values in structured lists show "-", toolbars keep a fixed position and order.** — S23 (structured-list page)

## 3. Disagreements between sources

- **Borders vs no borders.** Refactoring UI and Kennedy push space instead of borders (S7, S6); NN/g recommends a visible border/background for cards (S27) and warns that ultra-flat hurts findability (S30). Resolution for the agent: use space for grouping inside content; give clickable containers one visible cue.
- **Shadow colour.** Kennedy's button examples use translucent black (S3); Comeau says black greys out backgrounds and wants hue-matched shadows (S8). On white/neutral pages black at low opacity is fine; on coloured backgrounds tint.
- **Flat vs depth.** Toss product UI is near-flat and uses blur/outline for layers (S34); NN/g and Kennedy argue for retaining depth cues (S30, S1). Flat is acceptable only with low density, conventional layout and strong-contrast actions.
- **Measure.** 60ch (S16) vs ~75 characters (S20) vs 8–12 words (S32). For Korean text, characters are wider; treat 60ch / ~35–40 Hangul syllables as an upper bound (agent inference, not stated by sources).
- **Fixed breakpoints vs intrinsic.** GOV.UK, KRDS, Material define named breakpoints (S20, S23, S25); Every Layout and web.dev prefer content- and container-driven layouts with few or no media queries (S16, S19, S10). Use named breakpoints for the page frame and intrinsic rules for components.
- **Hover-revealed actions.** Kennedy accepts revealing per-item actions on hover for a cleaner UI (S5); web.dev and NN/g warn against hiding anything important behind hover (S14, S29). On public/small-business sites (mostly mobile), do not hide.
- **Desktop design effort.** Baemin designers draw mobile only and QA desktop after build (S37); Android guidance suggests optimising the expanded layout first when a compact one exists (S25).

## 4. What makes a page look templated or generated (per the sources)

Each item is a checkable sign, with its source.

1. **Defaults left untouched**: default font, colour, radius, shadow and spacing chosen by nobody; the "plain blue 40px button". — S3 (whole article: replace defaults with deliberate choices), S1 (cramped default HTML)
2. **Designed to look good as a static picture, not for this business**: polish over function, surface styling ahead of content and task; styles converge so unrelated products look alike. — S33
3. **Generic stock photography and decorative filler images**, models instead of the real staff, shop or product. Users ignore them. — S28
4. **Decorative effects that carry no information**: particle effects, heavy gradients, decorative illustrations, several hero graphics on one screen, error/loading graphics used where nothing is wrong or loading. — S36
5. **Inconsistent depth**: shadows with different angles or offset ratios, pure-black shadows on coloured backgrounds, glow-like shadows. — S8
6. **Everything emphasised**: many sizes, more than two large elements, every element bold/large, accent colour on everything; no single dominant element. — S26, S31, S2, S1
7. **Font size scatter** among ordinary elements beyond ~2pt, or more than three sizes in a block. — S6, S26
8. **Irregular, off-scale gaps**, or uniform gaps that ignore grouping (same space inside and between groups). — S32, S26, S21
9. **Borders and dividers everywhere** instead of space. — S7, S6
10. **Cards used for everything**, including uniform lists and galleries, by habit ("cards look modern"). — S27
11. **Ghost buttons and text-styled links for primary actions** (flat to the point of no signifier). — S30
12. **Several primary buttons competing**, CTA text that repeats the heading. — S22, S36
13. **Icons without labels, invented icons, or icon + emoji stacks**; oversized hamburger icons. — S29, S36, S6
14. **Fixed pixel widths/heights** that break under long Korean labels or large text. — S16, S34, S24
15. **Text dropped straight on a photo** with no overlay, so it fails on some crops. — S2
16. **Copying a popular showcase look without the context** (the Dribbble effect). Kennedy recommends studying the best work, but Adams warns that copying the surface without the problem produces sameness. — S2 rule 7 vs S33

Not from the sources read (secondhand only, treat as unverified): commentary that AI-built sites converge on Inter + indigo/purple gradient + centred hero + three rounded cards (rounded-2xl, shadow-lg), linked to Tailwind's indigo-500 default and an August 2025 post by Adam Wathan. The original post was not read.

## 5. Could not access

- Refactoring UI Medium articles ("7 practical tips for cheating at design") and the Twitter tips: Medium returns 403; the book itself is paid. Only the home-page free tip and the chapter titles were used ("Grids are overrated", "Labels are a last resort", "Establish a spacing and sizing system" are titles only, contents not read).
- Material Design 3 site (m3.material.io): JavaScript-only, no text returned. Breakpoints taken from the Android Developers page instead; M3 margins/spacers not obtained.
- Apple HIG HTML page: empty; the JSON data endpoint worked (S24).
- KRDS button component page: URL not found from the navigation (links are "#").
- Jen Simmons "Modern Layouts: Getting Out of Our Ruts" and Boris Müller "Why do all websites look the same?": slides/video or Notion copy not readable.
- 당근, 카카오, 네이버 design blogs: no layout/spacing posts found within budget; 당근 posts are on Medium (blocked).
