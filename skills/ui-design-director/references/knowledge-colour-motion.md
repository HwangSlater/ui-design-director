# Colour, motion and brand expression: rules for a design agent

Researched 2026-11-09 from free material by practising designers, research groups and design-system teams; each rule links its source, rewritten in our own words. Rules here are background: `build-rules.md` and the chosen base win when they disagree. Read only the section you need.

## Contents
- 1. Sources
- 2. Rules
- 3. Warnings: colour and motion that look generated
- 4. Disagreements at a glance

Read on 2026-11-09. Every rule is paraphrased. Numbers are the source's own. "Source" links to the page that was actually read. Where sources disagree, the disagreement is written next to the rule, and section 4 collects them.

## 1. Sources

| # | Title | Author | Credentials | URL | Read |
|---|---|---|---|---|---|
| S1 | Building Your Color Palette | Steve Schoger and Adam Wathan (Refactoring UI; no byline on the page) | Authors of *Refactoring UI*; Wathan created Tailwind CSS | https://www.refactoringui.com/previews/building-your-color-palette | 2026-11-09 |
| S2 | Color in UI Design: A (Practical) Framework (2024 update) | Erik D. Kennedy | Runs the Learn UI Design course; has consulted for clients from Fortune 100 companies to YC startups | https://www.learnui.design/blog/color-in-ui-design-a-practical-framework.html | 2026-11-09 |
| S3 | 7 Rules for Creating Gorgeous UI, Part 1 (2024) | Erik D. Kennedy | as above | https://www.learnui.design/blog/7-rules-for-creating-gorgeous-ui-part-1.html | 2026-11-09 |
| S4 | 7 Rules for Creating Gorgeous UI, Part 2 (2024) | Erik D. Kennedy | as above | https://www.learnui.design/blog/7-rules-for-creating-gorgeous-ui-part-2.html | 2026-11-09 |
| S5 | Designing accessible color systems (2019) | Daryl Koopersmith, Wilson Miner | Stripe Design team | https://stripe.com/blog/accessible-color-systems | 2026-11-09 |
| S6 | Understanding the scale (Radix Colors) | Radix / WorkOS team | Maintainers of the Radix design system | https://www.radix-ui.com/colors/docs/palette-composition/understanding-the-scale | 2026-11-09 |
| S7 | Color fundamentals | Adobe Spectrum team | Adobe's official design system | https://spectrum.adobe.com/page/color-fundamentals/ | 2026-11-09 |
| S8 | Color overview | IBM Carbon team | IBM's official design system | https://carbondesignsystem.com/elements/color/overview/ | 2026-11-09 |
| S9 | Colour | GOV.UK Design System team | UK Government Digital Service | https://design-system.service.gov.uk/styles/colour/ | 2026-11-09 |
| S10 | 색상 (Colour), KRDS style guide | Ministry of the Interior and Safety (Korea) | Official Korean government design system | https://www.krds.go.kr/html/site/style/style_02.html | 2026-11-09 |
| S11 | Color role (SEED) | Daangn (당근) design system team | Official SEED design system docs | https://seed-design.io/llms/foundations/color/color-role.txt (overview: https://seed-design.io/llms/foundations/color.txt) | 2026-11-09 |
| S12 | How we redesigned the Linear UI (2024) | Karri Saarinen, Yann-Edern Gillet, Andreas Eldh, Romain Cascino | Linear co-founder/CEO (Saarinen, ex-Airbnb design lead) and Linear designers | https://linear.app/now/how-we-redesigned-the-linear-ui | 2026-11-09 |
| S13 | How to design delightful dark themes (2019) | Teresa Man | Designer, Superhuman blog contributor | https://blog.superhuman.com/how-to-design-delightful-dark-themes/ | 2026-11-09 |
| S14 | Theming (Learn Design) | web.dev / Google Chrome team | Google's official web guidance | https://web.dev/learn/design/theming | 2026-11-09 |
| S15 | Color and contrast (Learn Accessibility) | web.dev / Google Chrome team | as above | https://web.dev/learn/accessibility/color-contrast | 2026-11-09 |
| S16 | Material Web: Color | Google Material team | Official Material 3 implementation docs | https://material-web.dev/theming/color/ | 2026-11-09 |
| S17 | Color extraction (material-color-utilities) | Google Material Foundation | Official Material colour library | https://github.com/material-foundation/material-color-utilities/blob/main/concepts/color_extraction.md | 2026-11-09 |
| S18 | Designing Shadows (2021, updated 2026) | Josh W. Comeau | Former staff engineer at Gatsby; teaches CSS for JavaScript Developers | https://www.joshwcomeau.com/css/designing-shadows/ | 2026-11-09 |
| S19 | An Interactive Guide to CSS Transitions (2021, updated 2026) | Josh W. Comeau | as above | https://www.joshwcomeau.com/animation/css-transitions/ | 2026-11-09 |
| S20 | Accessible Animations in React (prefers-reduced-motion) (2020, updated 2026) | Josh W. Comeau | as above | https://www.joshwcomeau.com/react/prefers-reduced-motion/ | 2026-11-09 |
| S21 | A Friendly Introduction to Spring Physics (2020, updated 2025) | Josh W. Comeau | as above | https://www.joshwcomeau.com/animation/a-friendly-introduction-to-spring-physics/ | 2026-11-09 |
| S22 | 7 Practical Animation Tips | Emil Kowalski | Design engineer (Vercel, Linear); author of Sonner and Vaul | https://emilkowal.ski/ui/7-practical-animation-tips | 2026-11-09 |
| S23 | What makes a great animation | Emil Kowalski | as above | https://emilkowal.ski/ui/great-animations | 2026-11-09 |
| S24 | You don't need animations | Emil Kowalski | as above | https://emilkowal.ski/ui/you-dont-need-animations | 2026-11-09 |
| S25 | Invisible Details of Interaction Design (2023) | Rauno Freiberg (no byline on the page) | Design engineer at Vercel | https://rauno.me/craft/interaction-design | 2026-11-09 |
| S26 | Web Interface Guidelines | Rauno Freiberg and contributors | as above; community-maintained document | https://interfaces.rauno.me/ | 2026-11-09 |
| S27 | Web Interface Guidelines | Vercel design team | Vercel's official guidelines | https://vercel.com/design/guidelines | 2026-11-09 |
| S28 | Motion overview | IBM Carbon team | IBM's official design system | https://carbondesignsystem.com/elements/motion/overview/ | 2026-11-09 |
| S29 | Executing UX Animations: Duration and Motion Characteristics (2020) | Page Laubheimer | Nielsen Norman Group | https://www.nngroup.com/articles/animation-duration/ | 2026-11-09 |
| S30 | Designing Safer Web Animation for Motion Sensitivity (2015, updated 2020) | Val Head | Web animation consultant; author of *Designing Interface Animations* | https://alistapart.com/article/designing-safer-web-animation-for-motion-sensitivity/ | 2026-11-09 |
| S31 | prefers-reduced-motion | Thomas Steiner | Google Chrome developer relations | https://web.dev/articles/prefers-reduced-motion | 2026-11-09 |
| S32 | Understanding SC 2.3.3 Animation from Interactions | W3C WAI | Standards body | https://www.w3.org/WAI/WCAG22/Understanding/animation-from-interactions.html | 2026-11-09 |
| S33 | Understanding SC 2.2.2 Pause, Stop, Hide | W3C WAI | Standards body | https://www.w3.org/WAI/WCAG22/Understanding/pause-stop-hide.html | 2026-11-09 |
| S34 | Scrolljacking 101 (2023) | Sara Paul | Nielsen Norman Group | https://www.nngroup.com/articles/scrolljacking-101/ | 2026-11-09 |
| S35 | hover media feature | MDN | Mozilla reference docs | https://developer.mozilla.org/en-US/docs/Web/CSS/@media/hover | 2026-11-09 |
| S36 | 모션, 금융을 즐겁고 쉬운 경험으로 만드는 방법 (2022) | 고현선 (Ko Hyun-sun) | Graphic designer at Toss | https://toss.im/tossfeed/article/why-motion-in-finance | 2026-11-09 |
| S37 | 토스가 모바일 접근성에 진심인 이유는? (2021) | 정희연, 김준모 | Toss feed writers | https://toss.im/tossfeed/article/tinyquestions-disability-5 | 2026-11-09 |
| S38 | Website Logo Placement for Maximum Brand Recall (2016) | Kathryn Whitenton | Nielsen Norman Group | https://www.nngroup.com/articles/logo-placement-brand-recall/ | 2026-11-09 |
| S39 | Photos as Web Content (2010, reviewed 2026) | Jakob Nielsen | Co-founder of Nielsen Norman Group | https://www.nngroup.com/articles/photos-as-web-content/ | 2026-11-09 |
| S40 | AI-Generated Images Can Perform as Well as Stock Photography (2026) | Rachel Banawa | Nielsen Norman Group | https://www.nngroup.com/articles/ai-generated-images/ | 2026-11-09 |
| S41 | Using Imagery in Visual Design (2023) | Rachel Krause | Nielsen Norman Group | https://www.nngroup.com/articles/imagery-in-visual-design/ | 2026-11-09 |
| S42 | How To Use Illustrations To Elicit Emotions (2017) | Blair Culbreth | Web designer; Smashing Magazine author | https://www.smashingmagazine.com/2017/05/emotional-design-illustrations/ | 2026-11-09 |
| S43 | How we refreshed the GDS brand (2025) | Kuba Bartwicki, Laura Yarrow, Chris Bellamy, Simon Williams | GDS heads of design, government chief product officer, brand strategist | https://designnotes.blog.gov.uk/2025/04/04/how-we-refreshed-the-government-digital-service-brand-and-what-were-doing-differently | 2026-11-09 |
| S44 | 배달의민족, 15년 만에 '배민 2.0' 리브랜딩 (2025) | Design Compass (press report on Woowa Brothers) | Design trade press, not a practitioner blog | https://designcompass.org/2025/07/23/baemin-2-rebranding/ | 2026-11-09 |

**Could not read** (JavaScript-only pages or blocked): Apple HIG Color and Motion (body did not load), Material 3 site m3.material.io (motion tokens, colour roles), Material 2 speed-and-easing, IBM Design Language colour (page too long, truncated), web.dev/learn/design/color (404), the Medium copy of Kennedy's rules (403), the Refactoring UI previews index (404), material-web motion page (404). Toss/toss.tech: no colour-system or motion-guide article was found. Only Toss feed articles (S36, S37) were usable. Kakao: no first-party design blog post was found; the only hits were third-party summaries, which were skipped. Baemin: only a press report (S44).

---

## 2. Rules

Format: **rule** — why — source.

### 2.1 Palette building (scales, tints, shades)

1. **Define the palette up front as fixed steps: 8–10 greys, 5–10 shades for each of the primary and accent colours.** — Ad-hoc shades break the system, and an unlimited palette is no system. — S1
2. **Build each scale in this order: base 500 (a colour that works as a button background), then the edges (900 for text, 100 for tinted backgrounds), then 700/300, then 800/600/400/200.** — Picking the edges by how they will be used gives shades that actually work on an alert component. — S1
3. **Do not generate shades at runtime with `lighten()`/`darken()`, `color-mix()` or similar colour functions. Reference fixed tokens.** — Hand-tuned steps stay perceptually even, and function output does not. — S1, S7
4. **Darker variant: lower brightness and raise saturation. Lighter variant: raise brightness and lower saturation (HSB).** — A plain black overlay only drops brightness, so the result looks muddy. — S2. Stripe agrees that you should not just darken base colours, because the result is muddy. — S5
5. **Optional hue shift: darker shades move toward the nearest luminance minimum (red 0°, green 120°, blue 240°); lighter shades move toward the nearest maximum (yellow 60°, cyan 180°, magenta 300°).** — This keeps shades vivid instead of dull. — S2. *Disagreement:* Stripe keeps each colour's hue fixed and only adjusts lightness in a perceptual space (S5). KRDS fixes hue and saturation per colour (S10). Spectrum shifts a few key colours' hue only to avoid neighbour confusion (S7).
6. **Build scales in a perceptual space (CIELAB/LCH/OKLCH), not HSL lightness.** — Equal HSL lightness looks different from hue to hue, so equal steps do not give equal contrast. — S5, S12
7. **Tune every hue so that the same step number means the same contrast.** Stripe's result: any two steps 5+ apart pass for small text, and 4+ apart pass for icons and large text. — Contrast then becomes a rule an agent can check by step number. — S5
8. **KRDS "magic numbers": step 40 = 3:1, 50 = 4.5:1, 70 = 7:1, 90 = 15:1 against the background end of the scale.** KRDS builds the base at HSL L50% and then moves it until it meets contrast (primary-50 went from L50% to L55% because it only reached 3.9:1). — The step name alone tells you whether a pair passes. — S10
9. **Assign scale steps to roles (Radix 12-step model):** 1–2 app backgrounds; 3/4/5 component background default/hover/pressed; 6 subtle non-interactive border; 7 interactive border; 8 strong border and focus ring; 9 solid fill (the most saturated step); 10 solid hover; 11 low-contrast text; 12 high-contrast text. Steps 11 and 12 reach APCA Lc 60 and Lc 90 on step 2. — Each step has one job, so nothing gets picked at random. — S6
10. **Yellow, amber, lime and similar light hues take dark text on their solid step. Most other hues take white.** — Their solid steps are too light for white text. — S6, S7, S11
11. **Make the lightest tint of every hue safe as a text background as well as white.** — Text then works on highlighted sections without re-checking each pair. — S5
12. **Some colours are physically impossible (for example, a very dark yellow). Check the gamut instead of forcing them.** — S5
13. **Contrast is not vibrancy. Check separately that hues are distinguishable from each other.** — WCAG measures only luminance contrast. — S5
14. **Use palette values first. Add a new colour only if it will be reused.** — S10, S1
15. **Design in greyscale first, then add colour last and only with a purpose.** — It forces hierarchy to come from spacing, size and weight. — S3
16. **Simplest working scheme: one accent on a greyscale base, or several shades of one hue.** — S3. Kennedy builds whole interfaces from one base colour (S2).
17. **When a theme must be user-customisable or derived, generate it from very few inputs: Linear uses base colour, accent colour and a contrast value (down from 98 variables).** — Fewer inputs give consistent themes and allow a high-contrast variant. — S12

### 2.2 Neutrals

18. **Start greys from a very dark grey, never pure black. Take the darkest grey from your darkest text colour and the lightest from an off-white background.** — S1
19. **Let neutrals dominate. Carbon's default themes are mostly grey, and other colours are used sparingly.** — S8
20. **Tint neutrals toward the brand hue only lightly. Linear deliberately limited how much accent blue entered its neutral calculation.** — The result looks more neutral and dates less. — S12. Government systems tint their greys blue: KRDS uses blue-grey (S10).
21. **Build hierarchy with background layer tokens (for example gray-75/100/200, or white/gray-10), not ad-hoc fills.** — The structure then carries across themes. — S7, S8
22. **Light theme layering: alternate white and grey-10 for each added layer (Carbon). KRDS: gray10 → gray0 → gray5 → gray0.** — S8, S10

### 2.3 Accent and brand colour use, proportions

23. **Proportion rule (KRDS): 60% background and neutrals, 30% secondary, 10% primary for key actions. Accent colour never above 5% of the design.** — S10
24. **Reserve the brand colour for brand elements and the single most important action on the screen (Daangn SEED `bg.brand-solid`).** — When the brand colour appears everywhere, nothing stands out. — S11
25. **Most sites need one, maybe two primary colours. Semantic accents (red destructive, yellow warning, green positive) get shades but are used sparingly.** — S1
26. **Use colour only where it adds meaning. Use colour backgrounds sparingly.** — Key actions and states then stand out. — S7
27. **Interaction states are lighter or darker steps of the same hue. Never switch hue for a state.** — S10, S2
28. **Carbon state offsets: hover = half a step, selected = one full step, active = two full steps (for example Blue 60 → Blue 80).** — Gives checkable, consistent state deltas. — S8
29. **Hover, active and focus states must have more contrast than the rest state.** — S27
30. **Separate the logo colour from the UI colour where needed.** GOV.UK separates its brand blue (#1d70b8) from its link blue (#1a65a6). — S9
31. **Focus colour is used only for focus.** GOV.UK uses yellow #ffdd00 with black text for this alone. — The focus indicator is never confused with brand decoration. — S9
32. **On a coloured (non-neutral) background, tint borders, shadows and secondary text toward that background's hue instead of using grey.** — Plain grey looks dirty on colour. — S27, S18

### 2.4 Contrast and accessibility

33. **Text contrast ≥ 4.5:1. Large text (≥ 24px, or ≥ 18.5px bold) ≥ 3:1. Essential icons and UI component boundaries ≥ 3:1. Logos and decoration are exempt.** — WCAG 1.4.3/1.4.11. — S15, S8, S9
34. **Focus indicator contrast ≥ 3:1. Carbon uses a 2px Blue 60 border on light themes and white on dark themes.** — S8
35. **Never rely on colour alone. Every status needs an icon or text label, and "a red border alone fails".** — S7, S10, S15, S27
36. **Review the page in greyscale to find colour-only meaning.** — S15
37. **Do not put high-hue-contrast colours of similar lightness next to each other. They vibrate. Over images or colour, use static white or black components.** — S7
38. **Offer `prefers-color-scheme` (dark) and `prefers-contrast` (high-contrast) variants. They can be combined.** — S15
39. *Contrast metric disagreement:* Vercel says to prefer APCA over WCAG 2 for perceptual accuracy (S27). Radix and SEED design to APCA targets (S6, S11). GOV.UK, Carbon and web.dev use WCAG 2 ratios (S9, S8, S15). **Practical rule: pass WCAG 2 AA (it is the legal baseline), and use APCA as an extra perceptual check.**
40. **Do not use alpha transparency on disabled states.** — Contrast becomes unpredictable over varied backgrounds. — S10

### 2.5 Dark themes and dark sections

41. **Do not simply invert the light theme. Closer surfaces are lighter and distant surfaces darker.** Carbon: each added layer is one step lighter. KRDS dark: gray90 → gray100 → gray95 → gray90. SEED dark layers: gray-00 / gray-100 / gray-200. — Inversion flips the depth cues. — S13, S8, S10, S11
42. **Avoid #000000 backgrounds and pure white text. Even #010101 avoids OLED smearing. Superhuman sets primary white text at 90% opacity.** — 21:1 contrast causes halation, especially for people with astigmatism. — S13
43. **Accents in dark mode: keep the hue and lower the lightness (S13 also raises saturation). SEED moves solid fills down one shade in dark mode (for example red-700 → red-600). KRDS swaps in a lighter tone of a similar hue where secondary-70 would be confused with primary.** — S13, S11, S10. *Disagreement:* web.dev suggests a more subdued brand shade in dark mode (S14), while Superhuman says to raise saturation (S13). Both lower lightness.
44. **KRDS dark-mode minimums: text step 70 (body 90), icons 70. System colours in dark mode: icon/text -20, background -95, border -90.** — S10
45. **In dark mode, remove or tone down large bright colour blocks.** — They pull focus from content. — S13
46. **Tune perceived contrast by eye after meeting AA. Superhuman: secondary text went from 60% black (light) to 65% white (dark).** — S13
47. **Dark components should not be darker than their background (except in high-contrast mode).** — S8
48. **Dim photos in dark mode, for example `filter: brightness(.8) contrast(1.2)`. Swap images such as maps with `<picture>` + a `prefers-color-scheme` source.** — S14
49. **Store theme colours in custom properties on `html` and redefine them in the dark media query. Declare `color-scheme: light dark` (or `dark` on dark pages) so form controls and scrollbars match. Set `accent-color` and `<meta name="theme-color">` per scheme.** — S14, S27
50. **Disable transitions while switching theme.** — Otherwise every hover-bound property animates at once. — S26

### 2.6 Shadows and depth

51. **One light source for the whole page. Every shadow uses the same x:y offset ratio (Comeau's demo: y = 2 × x).** — S18. Kennedy: light comes from above, so tops are brighter and bottoms darker (S3).
52. **Higher elevation means larger offset, larger blur and lower opacity.** — S18
53. **Layer shadows. Comeau: 5 layers at offsets 1/2/4/8/16px, each at about 7.5% opacity. Vercel: at least two layers, paired with a semi-transparent border.** Do not animate layered shadows. — S18, S27
54. **Tint shadows with the background hue (higher saturation, lower lightness) instead of semi-transparent black. Too much saturation reads as a glow.** — Black shadows grey out coloured backgrounds. — S18, S2
55. **Use `filter: drop-shadow()` for irregular shapes such as cut-out images and tooltips with tails.** — S18

### 2.7 Colour from photography and brand

56. **To derive a theme from a photo, quantise it to a small set of colours, then score them: prefer colours common in the image, hue diversity within about a 30° neighbourhood, and chroma near 48 (HCT). Drop near-greys and rare colours.** — This is Material's dynamic-colour method. — S17
57. **Map a few key colours (Material: 5) to roles automatically: primary, secondary, tertiary, error, plus neutral surfaces. Every role has an `on-` partner colour for text on it.** — Text colours are designed together with their fills, not picked later. — S16, S11
58. **Over photos, choose one text-protection method (Kennedy):** whole-image overlay (example: 35% black); text in a slightly transparent black box; blur behind the text; floor fade (0% at the middle → about 20% black at the bottom, plus a slight text shadow); or an elliptical scrim. Text straight on the image only works if the image is dark and low-contrast and you test it at every width. — S4
59. **Keep photos consistent in exposure, brightness and contrast so no single image dominates.** — S41

### 2.8 Motion: durations

60. **Default UI motion range: 100–400ms (NN/g); 500ms already feels like a drag.** About 100ms for simple feedback (checkbox, toggle), 200–300ms for a modal, up to 400ms for large movement across the screen. — S29
61. **Product UI animations stay under 300ms (Kowalski). A 180ms dropdown feels more responsive than a 400ms one.** — S22, S23, S24. Rauno is stricter: no more than 200ms for interaction animations (S26). Carbon micro-interactions: 90–120ms (S28).
62. **Carbon duration tokens:** fast-01 70ms (buttons, toggles), fast-02 110ms (fades), moderate-01 150ms (small expansions), moderate-02 240ms (expansions, toasts), slow-01 400ms (large expansions, important notifications), slow-02 700ms (background dimming only). — S28
63. **Duration grows with distance and size. Small travel is fast and large travel is slower (non-linear).** — S28, S29
64. **Enter is slightly longer than exit, for example a popup at 300ms in and 200–250ms out.** — S29. *Disagreement:* for hover, Comeau makes the enter fast and the exit slow (125ms in, 450ms out) so the response feels snappy and the release relaxed; his dropdown example is 100ms in, 400ms out (S19).
65. **The more often an animation is seen, the shorter and subtler it should be.** — S29, S23, S24, S25
66. **Spinners and skeletons: wait about 150–300ms before showing them, then keep them visible at least 300–500ms.** — This avoids flicker. — S27
67. **Use the shortest duration that does not feel jarring. Animations are more often too long than too short. Test small differences (250 vs 300ms is noticeable).** — S29

### 2.9 Motion: easing

68. **Entering or appearing elements use ease-out.** — It starts fast, so it feels responsive. — S19, S22, S23, S29. Carbon entrance curve: productive `cubic-bezier(0, 0, 0.38, 0.9)`, expressive `cubic-bezier(0, 0, 0.3, 1)` (S28).
69. **Elements visible throughout the motion use the standard curve.** Carbon standard: productive `cubic-bezier(0.2, 0, 0.38, 0.9)`, expressive `cubic-bezier(0.4, 0.14, 0.3, 1)`. CSS `ease` is a good general default for things that move but stay on screen. — S28, S19
70. **Permanently leaving elements use an accelerating exit curve.** Carbon exit: productive `cubic-bezier(0.2, 0, 1, 0.9)`, expressive `cubic-bezier(0.4, 0.14, 1, 1)`. A panel that may return (side panel) uses standard easing. — S28. Comeau and NN/g also use ease-in for exits (S19, S29). *Disagreement:* Kowalski says to avoid ease-in in UI altogether and use (custom, stronger) ease-out for both enter and exit (S22).
71. **Never use `linear` for movement (only for progress or looping rotations). Use `ease-in-out` for loops.** — S19, S29
72. **Built-in CSS easings are weak. Prefer custom ease-out curves.** — S22
73. **Productive (subtle, fast) motion for task UI such as buttons, dropdowns and tables. Expressive (bigger, slower) motion only for significant moments such as a page open, a primary action or an alert.** — S28. Kowalski: marketing sites may be expressive, but product UI must be fast (S24).
74. **Springs suit position and transform where realism matters. They don't have to bounce. Don't use springs for colour or opacity. Stay with CSS transitions when they are enough.** — S21, S23

### 2.10 Motion: what to animate, origin, interruptibility

75. **Animate `transform` and `opacity` only, where possible. Avoid `width/height/top/left/margin`. `background-color` costs a repaint.** — Layout properties reflow siblings and drop frames. — S19, S23, S27
76. **Never write `transition: all`. List the properties.** — S19, S27
77. **Never scale in from 0. Start popovers at about 0.9+ (Kowalski uses 0.93). Rauno starts dialogs at about 0.8.** — Nothing real appears from nothing. — S22, S26. *(Minor disagreement on the exact start value.)*
78. **Set `transform-origin` at the trigger (popover from its button), not the default centre.** — S22, S27
79. **Animations must be interruptible: user input can reverse or cancel them mid-flight without a jump.** — S23, S25, S27
80. **Use `will-change: transform` only on elements that will animate, and only during the animation.** — It costs video memory. — S19, S26
81. **Pause looping animations when they are off-screen.** — S26
82. **If a crossfade still looks wrong after tuning easing and duration, add about 2px of `filter: blur()` during the swap.** — S22
83. **Use motion to show spatial relationships: things come from where they live and leave toward where they go.** — S25
84. **Test animation on the slowest target device.** — S19

### 2.11 Hover and press states

85. **Press feedback: scale to about 0.97 on `:active` (Kowalski). Rauno allows 0.96 down to 0.9, never 0.8.** — S22, S26
86. **Wrap hover styles in `@media (hover: hover)`.** — Otherwise taps leave a sticky hover on touch screens. — S26, S35
87. **Never hide essential content or actions behind hover. Pair `:hover` with `:focus-visible`.** — S35, S27
88. **Don't change font weight, size or case on hover or selection. Use colour, background, shadow or underline.** — It shifts layout. — S4, S26
89. **Don't let a hover effect move the element out from under the cursor. Hover the wrapper and animate the child.** — Otherwise the element flickers. — S19
90. **Delayed close for dropdowns (example: 300ms `transition-delay` on leave, 0ms on enter).** — S19
91. **Tooltips: delay the first one, then show neighbouring tooltips instantly with no animation.** Base tooltip motion: `transform` and `opacity` at 125ms ease-out from scale 0.97. — S22, S27
92. **Skip hover animation on trivial buttons and other high-frequency elements.** — S26, S24
93. **Decorative glows and gradients get `pointer-events: none`.** — They should not steal hover. — S26
94. **Hit targets: at least 24px on desktop, 44px on mobile.** — S27
95. **Never animate keyboard-initiated actions. Consider opening menus on `mousedown`.** — S24, S26

### 2.12 Scroll effects

96. **Avoid scrolljacking. If it is used: short, below the fold, vertical only, responsive within 1–2 scroll actions, never holding important text, alternating with normal scroll, sticky navigation as an escape, and avoided or redone on mobile. Key CTAs stay above the fold.** — Users get lost, think the page is broken, and leave. — S34
97. **Parallax and scroll-linked motion of non-scrolling elements are vestibular triggers. Keep them small relative to the viewport, or skip them, and make them removable.** — S30, S31, S32
98. **Motion is judged by its size relative to the screen: a small rotating button is fine, a full-screen wipe is not.** — S30
99. **Use `scroll-behavior: smooth` with `scroll-margin-top` for in-page anchors. Use `overscroll-behavior: contain` on modals and drawers.** — S26, S27

### 2.13 Reduced motion and auto-playing motion

100. **Write motion inside `@media (prefers-reduced-motion: no-preference)` (opt-in), so no-support browsers get no motion.** — S20, S31. Comeau rejects the global `* { transition-duration: 0.01ms !important }` override (S20).
101. **Under reduced motion, replace movement, zoom and parallax with a fade or no animation. Opacity, colour and blur changes are low-risk.** — S30, S20, S23. Note: WCAG errata now counts blur as motion (S32).
102. **For JS-driven motion, read `matchMedia('(prefers-reduced-motion: no-preference)')` and listen for `change`.** — S20, S31
103. **Swap animated images and background videos for static versions under reduced motion. Don't autoplay decorative video.** — S31, S27
104. **Anything that moves, blinks or scrolls automatically for more than 5 seconds alongside other content needs a real pause/stop/hide control. Auto-advancing carousels need one regardless of length.** — WCAG 2.2.2 (Level A). — S33, S27
105. **Nothing flashes more than 3 times per second, and avoid hard colour cuts.** — Seizure risk. — S33, S29
106. **Offer a site-level control to reduce motion if the page is animation-heavy.** — S30, S32

### 2.14 Motion with meaning and tone (Korean practice)

107. **Use motion where it replaces reading on small screens: summarise a concept in movement, cover waits with a loop, then confirm with a check animation.** — S36
108. **Match motion tone to the news: celebration motion for good moments; light, gentle motion to soften bad news such as a network error or long terms.** — S36
109. **Prefer Lottie, and use hybrid 3D (a few rendered frames as PNG sequences inside Lottie) over full 3D in-product. Save rich 3D for web and social channels.** — Smaller files, no visible quality loss. — S36
110. **Design dark mode and large text into every screen from the system level, not as a retrofit.** — S37

### 2.15 Brand expression on a page

111. **Logo top-left (in left-to-right languages). Brand recall was 39% top-left vs 21% right-aligned, an 89% lift. Right-aligned logos did not make the brand seem more distinctive.** — S38
112. **Keep the wordmark readable. Hard-to-read script names were remembered much less, wherever the logo sat.** — S38
113. **Prepare logo lockups for different contexts (GDS: formal, acronym, spelled-out). The symbol must work alone in small digital spaces. Keep known elements during a refresh to carry existing recognition.** — S43
114. **Brand colours can be borrowed from a parent palette (GDS took cyan and midnight blue from the DSIT palette). A strong symbol can sit on department colour backgrounds.** — S43
115. **Roll out a refresh in stages (Baemin 2.0: app icon first, then colour and the new typeface WORK체 two weeks later), and lead with mission rather than colour.** — Gradual change avoids alienating users. — S44
116. **Show real people and real products. Generic stock people are ignored. Real staff portraits drew 10% more viewing time than bios that took 316% more space.** — S39
117. **Decorative feel-good images are filler. Informative images (product, people, process) deserve the most space. Enlargements should be at least 2× the thumbnail.** — S39, S41
118. **Pick the image type by content: photos for products, places and people; illustration for abstract services and processes; icons for actions.** — S41, S42
119. **Check the mood: hide all text and see whether the images alone still give the right feeling.** — S41
120. **Pair rich imagery with text-heavy layouts and simple imagery with airy layouts.** — S41
121. **Illustration style must be consistent: one core idea, a limited set of shapes and colours, written guidelines. For icons: same stroke weight (matched to the font weight), corner style and fill.** — S41, S42
122. **If full illustration is out of reach, use illustration only on edge states (404, empty, onboarding, error).** — S42
123. **A mascot must reflect what the product actually does. Otherwise the warmth feels hollow.** — S42
124. **AI-generated hero images scored about the same as stock (slightly higher, but only authenticity was significant, about +0.4/7). Users who suspected AI rated the site lower. Before using one, check hands, text, screens, reflections and backgrounds, plus representation and roles.** — S40
125. **For a small business, the strongest brand signals the sources support are: its own photos of its people, place and products (S39, S41); a logo in the expected spot with a legible name (S38); one brand colour used sparingly on the main action (S10, S11); and a consistent image style (S41, S42).** — Synthesis of the above. No single source covers "small business" directly.

---

## 3. Warnings: colour and motion that look generated

Each item is something the sources name as a mistake or a cheap default:

- **Shades made with `lighten()`/`darken()` or black/white overlays** instead of a tuned scale (muddy, uneven). — S1, S2, S5, S7
- **A different hue for hover or active states**, or new one-off colours outside the palette. — S10, S1
- **Brand or accent colour spread everywhere** (accent well above 5%, brand colour on many buttons). — S10, S11
- **Pure #000 dark backgrounds with pure white text**, or a light theme simply inverted (depth flipped). — S13, S8
- **Large bright colour blocks in dark sections.** — S13
- **Flat grey or black shadows on coloured backgrounds**, and over-saturated shadows that read as glows. — S18, S27
- **Shadows with inconsistent angles** across cards and buttons. — S18, S3
- **Vibrating neighbours**: saturated hues of equal lightness side by side. — S7
- **Status shown only by colour** (red border, green dot without a label). — S7, S15
- **Things that scale in from 0**, popovers growing from their centre, and 0.8 button squash on press. — S22, S26
- **`transition: all`**, animated width/height/top, and animated layered shadows. — S19, S27, S18
- **Durations of 400–500ms+ on everyday UI**, and ease-in or linear movement on interface elements. — S29, S22, S24
- **Hover animation on every trivial button**, delight animation on frequent actions, and animated keyboard actions. — S24, S26
- **Font-weight jumps on hover**, and hover effects that slide the target away from the cursor. — S26, S19
- **Hover styles not wrapped in `(hover: hover)`** (sticky taps on phones). — S26, S35
- **Decorative glows and gradient overlays that block hover.** — S26
- **Gradient text that stays gradient when selected.** — S26
- **Parallax, scroll-jacked storytelling above the fold, and auto-advancing carousels with no pause.** — S34, S30, S33
- **Motion that ignores `prefers-reduced-motion`**, or a global 0.01ms override. — S20, S31
- **Generic stock people and feel-good decoration photos**, and AI images with broken hands, text or reflections. — S39, S40, S41
- **Mixed illustration styles**, and icons with mismatched stroke and fill. — S41, S42
- **A centred or right-aligned logo used to look "different"**: no gain in distinctiveness, and recall drops. — S38

## 4. Disagreements at a glance

| Topic | Positions |
|---|---|
| Max UI duration | Rauno ≤200ms (S26); Kowalski <300ms (S23); NN/g 100–400ms, 500 too slow (S29); Carbon up to 400ms, 700ms for dimming only (S28) |
| Exit easing | ease-in / accelerate for permanent exits (S19, S28, S29) vs avoid ease-in in UI and use ease-out both ways (S22) |
| Enter vs exit length | Enter longer than exit (S29) vs for hover, fast in and slow out (S19) |
| Start scale | ≥0.9, e.g. 0.93 (S22) vs about 0.8 for dialogs (S26) |
| Press scale | 0.97 (S22) vs 0.96–0.9 (S26) |
| Hue shift across shades | Shift toward luminance extremes (S2) vs keep hue fixed (S5, S10) |
| Dark-mode accent | Lower lightness, raise saturation (S13) vs a subdued shade (S14) vs one shade lower (S11) |
| Contrast metric | APCA preferred (S27, S6, S11) vs WCAG 2 ratios (S8, S9, S15) |
| AI images | Perform like stock (S40), but stock itself is ignored when generic (S39); suspicion lowers ratings (S40) |
