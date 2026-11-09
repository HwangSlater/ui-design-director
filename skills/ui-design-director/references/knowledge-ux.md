# UX and interaction rules for website pages and simple web apps

Researched 2026-11-09 from free material by practising designers, research groups and design-system teams; each rule links its source, rewritten in our own words. Rules here are background: `build-rules.md` and the chosen base win when they disagree. Read only the section you need.

## Contents
- 1. Sources
- 2. Rules
- 3. Disagreements between sources
- 4. Korean-specific notes
- 5. Not accessed / limits

Scope: Korean small businesses, booking, shops, public services. Distilled from free, publicly readable material by practitioners and research groups. Rules are paraphrased, not quoted at length. Each rule: **rule** — why — source.
Date read for every source: 2026-11-09.

---

## 1. Sources

| # | Title | Author | Credentials | URL | Pub. date |
|---|---|---|---|---|---|
| S1 | 10 Usability Heuristics for User Interface Design | Jakob Nielsen | Co-founder NN/g, PhD HCI | https://www.nngroup.com/articles/ten-usability-heuristics/ | 1994, reviewed 2024-01 |
| S2 | Error-Message Guidelines | Tim Neusesser, Evan Sunwall | NN/g UX specialists | https://www.nngroup.com/articles/error-message-guidelines/ | 2023-05 |
| S3 | Placeholders in Form Fields Are Harmful | Katie Sherwin | NN/g UX specialist | https://www.nngroup.com/articles/form-design-placeholders/ | 2014, reviewed 2018 |
| S4 | Website Forms Usability: Top 10 Recommendations | Kathryn Whitenton | NN/g Director of Digital Strategy | https://www.nngroup.com/articles/web-form-design/ | 2016-05 |
| S5 | Designing Empty States in Complex Applications | Kate Kaplan | NN/g UX specialist | https://www.nngroup.com/articles/empty-state-interface-design/ | 2021-09 |
| S6 | Progress Indicators Make a Slow System Less Insufferable | Katie Sherwin | NN/g | https://www.nngroup.com/articles/progress-indicators/ | 2014-10 |
| S7 | Laws of UX | Jon Yablonski (author per general knowledge; About page returned 404, not verified) | Designer, author of the book "Laws of UX" | https://lawsofux.com/ | n/a |
| S8 | Web Application Form Design | Luke Wroblewski | Author of "Web Form Design", "Mobile First"; product lead at Google, Yahoo | https://www.lukew.com/ff/entry.asp?1502 | 2005-01 |
| S9 | Dropdowns Should be the UI of Last Resort | Luke Wroblewski | as above | https://www.lukew.com/ff/entry.asp?1950 | 2015-07 |
| S10 | Touch Target Sizes | Luke Wroblewski | as above | https://www.lukew.com/ff/entry.asp?1085 | 2010-05 |
| S11 | Checkout Optimization: 5 Ways to Minimize Form Fields | Edward Scott | Research Lead, Baymard Institute | https://baymard.com/blog/checkout-flow-average-form-fields | 2024-06 |
| S12 | Cart Abandonment Rate statistics | Baymard Institute | E-commerce UX research firm | https://baymard.com/lists/cart-abandonment-rate | 2026-10 |
| S13 | Checkout UX 2026: 10 Pitfalls and Best Practices | Edward Scott | Baymard | https://baymard.com/blog/current-state-of-checkout-ux | 2024-11, upd. 2026-11 |
| S14 | Usability Testing of Inline Form Validation | Edward Scott | Baymard | https://baymard.com/blog/inline-form-validation | 2024-01 |
| S15 | Perceived Security of Payment Form | Jamie Holst | Co-founder, Baymard | https://baymard.com/blog/perceived-security-of-payment-form | 2016, upd. 2025 |
| S16 | Validation pattern | GOV.UK Design System team | UK Government Digital Service | https://design-system.service.gov.uk/patterns/validation/ | living doc |
| S17 | Button component | GOV.UK Design System | GDS | https://design-system.service.gov.uk/components/button/ | living doc |
| S18 | Error message component | GOV.UK Design System | GDS | https://design-system.service.gov.uk/components/error-message/ | living doc |
| S19 | Question pages pattern | GOV.UK Design System | GDS | https://design-system.service.gov.uk/patterns/question-pages/ | living doc |
| S20 | Check answers pattern | GOV.UK Design System | GDS | https://design-system.service.gov.uk/patterns/check-answers/ | living doc |
| S21 | Structuring forms | GOV.UK Service Manual | GDS | https://www.gov.uk/service-manual/design/form-structure | living doc |
| S22 | Homepage Design: 5 Fundamental Principles | Huei-Hsin Wang | NN/g | https://www.nngroup.com/articles/homepage-design-principles/ | 2024-03 |
| S23 | Trustworthiness in Web Design: 4 Credibility Factors | Aurora Harley | NN/g | https://www.nngroup.com/articles/trustworthy-design/ | 2016-05 |
| S24 | Menu-Design Checklist: 17 UX Guidelines | Page Laubheimer | NN/g | https://www.nngroup.com/articles/menu-design/ | 2024-06 |
| S25 | Hamburger Menus and Hidden Navigation Hurt UX Metrics | Kara Pernice, Raluca Budiu | NN/g (Pernice SVP; Budiu Director of Research) | https://www.nngroup.com/articles/hamburger-menus/ | 2016-06 |
| S26 | Understanding SC 2.5.8 Target Size (Minimum) | W3C WAI | Web standards body | https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html | WCAG 2.2 |
| S27 | Learn Forms | Michael Scharnagl, Sam Dutton, Rachel Andrew | Google web.dev | https://web.dev/learn/forms/ | n/a |
| S28 | Forms Tutorial | W3C WAI | W3C | https://www.w3.org/WAI/tutorials/forms/ | n/a |
| S29 | Command Links | Jakob Nielsen | NN/g | https://www.nngroup.com/articles/command-links/ | 2007-05 |
| S30 | HIG: Buttons (JSON data endpoint) | Apple | Platform owner | https://developer.apple.com/design/human-interface-guidelines/buttons | living doc |
| S31 | HIG: Accessibility (JSON data endpoint) | Apple | Platform owner | https://developer.apple.com/design/human-interface-guidelines/accessibility | living doc |
| S32 | Mobile User Experience: Limitations and Strengths | Raluca Budiu | NN/g | https://www.nngroup.com/articles/mobile-ux/ | 2015-04 |
| S33 | Confirmation Dialogs Can Prevent User Errors | Jakob Nielsen | NN/g | https://www.nngroup.com/articles/confirmation-dialog/ | 2018, reviewed 2026-08 |
| S34 | Skeleton Screens 101 | Samhita Tankala | NN/g | https://www.nngroup.com/articles/skeleton-screens/ | 2023-06 |
| S35 | The Four Dimensions of Tone of Voice | Kate Moran | NN/g VP | https://www.nngroup.com/articles/tone-of-voice-dimensions/ | 2016-07 |
| S36 | Response Times: The 3 Important Limits | Jakob Nielsen | NN/g | https://www.nngroup.com/articles/response-times-3-important-limits/ | 1993, upd. 2014 |
| S37 | F-Shaped Pattern of Reading on the Web | Kara Pernice | NN/g | https://www.nngroup.com/articles/f-shaped-pattern-reading-web-content/ | 2017-11 |
| S38 | Breadcrumbs: 11 Design Guidelines | Page Laubheimer | NN/g | https://www.nngroup.com/articles/breadcrumbs/ | 2018-12 |
| S39 | Carousel Usability | Kara Pernice | NN/g | https://www.nngroup.com/articles/designing-effective-carousels/ | 2013, reviewed 2026-08 |
| S40 | Footer Design | Therese Fessenden | NN/g | https://www.nngroup.com/articles/footers/ | 2019-02 |
| S41 | Date-Input Form Fields | Angie Li | NN/g | https://www.nngroup.com/articles/date-input/ | 2017-01 |
| S42 | Easy Checks – A First Review of Web Accessibility | W3C WAI | W3C | https://www.w3.org/WAI/test-evaluate/easy-checks/ | n/a |
| S43 | Material's Communication Principles: Intro to UX Writing (codelab) | Google Material team | Google | https://codelabs.developers.google.com/codelabs/material-communication-guidance | n/a |
| S44 | E-commerce Product Pages | Katie Sherwin | NN/g | https://www.nngroup.com/articles/ecommerce-product-pages/ | 2019-11 |
| S45 | "Learn More" Links: You Can Do Better | Katie Sherwin | NN/g | https://www.nngroup.com/articles/learn-more-links/ | 2015-12 |
| S46 | Learn Accessibility: Focus | Google web.dev | Google | https://web.dev/learn/accessibility/focus | n/a |
| S47 | Infinite Scrolling: When to Use It | Tim Neusesser | NN/g | https://www.nngroup.com/articles/infinite-scrolling-tips/ | 2022-09 |
| K1 | 토스의 8가지 라이팅 원칙들 | 김자유 | Toss's first UX Writer, writing team lead | https://toss.tech/article/8-writing-principles-of-toss | 2022-11 |
| K2 | 좋은 에러 메시지를 만드는 6가지 원칙 | 김자유 | Toss | https://toss.tech/article/21021 | 2022-09 |
| K3 | 가이드라인을 시스템으로 만드는 법 | 김자유 | Toss | https://toss.tech/article/introducing-toss-error-message-system | 2022-11 |
| K4 | 토스 피플 #2: UX 라이팅의 새로운 기준 | Toss (interview of 김자유) | Toss | https://toss.tech/article/toss-people-2 | 2024-10 |
| K5 | KRDS 디자인 원칙 | 행정안전부 KRDS | Korean government design system | https://www.krds.go.kr/html/site/utility/utility_02.html | living doc |
| K6 | KRDS 기본 패턴 – 오류 | KRDS | as above | https://www.krds.go.kr/html/site/global/global_07.html | living doc |
| K7 | KRDS 기본 패턴 – 입력폼 | KRDS | as above | https://www.krds.go.kr/html/site/global/global_08.html | living doc |
| K8 | KRDS 기본 패턴 – 확인 | KRDS | as above | https://www.krds.go.kr/html/site/global/global_11.html | living doc |
| K9 | KRDS 서비스 패턴 – 로그인 | KRDS | as above | https://www.krds.go.kr/html/site/service/service_03_01.html | living doc |
| K10 | KRDS 서비스 패턴 – 신청 | KRDS | as above | https://www.krds.go.kr/html/site/service/service_04_01.html | living doc |
| K11 | KRDS 기본 패턴 목록 / 사이트 첫 화면 | KRDS | as above | https://www.krds.go.kr/html/site/global/global_summary.html | living doc |
| K12 | 카카오 '더 쉬운 카톡설명서' 보도자료 | Kakao Corp. | Kakao (first-party press release) | https://www.kakaocorp.com/page/detail/11024 | 2024-05-16 |

---

## 2. Rules

### 2.1 Usability heuristics (baseline checklist)

1. **Every action gets visible feedback at once (pressed state, then result).** — Users must know what the system is doing; silent actions get repeated. — S1, S6
2. **Use the customer's words, not internal or industry jargon, in labels and menus.** — Matching the real world lowers learning cost. — S1, S24
3. **Every flow has a visible exit (Cancel / Back) and, where possible, Undo.** — User control and freedom; prevents lock-in after a mis-tap. — S1, S32
4. **The same thing has the same name and the same position everywhere.** — Consistency; follow conventions users learned on other sites (Jakob's Law). — S1, S7
5. **Prevent errors first: constraints, sensible defaults, disabled impossible choices.** — Cheaper than recovering. — S1, S41, K2
6. **Keep options and labels visible instead of making users remember them.** — Recognition beats recall. — S1, S3
7. **Remove any element that does not serve the page's main task.** — Every extra element competes with the important ones. — S1, K1
8. **Help is short, contextual, task-focused, and placed where the question arises.** — Users skip manuals (Paradox of the Active User). — S1, S5, S7

### 2.2 Cognitive principles (Laws of UX) turned into checks

9. **Make primary buttons large and close to where the eye/thumb already is.** — Fitts's Law: time to hit a target grows with distance and shrinks with size. — S7, S24
10. **Limit choices per decision point; group long lists into chunks.** — Hick's Law, Choice Overload, Chunking. — S7
11. **Use standard layouts (logo top-left, nav in header, cart top-right, footer utilities).** — Jakob's Law: users expect your site to work like others. — S7, S22, S24
12. **Group related items by proximity and shared containers; separate unrelated ones with space.** — Proximity, Common Region. — S7, S4
13. **Make only one thing visually distinct per area (the primary CTA).** — Von Restorff: the different item gets noticed; if everything stands out nothing does. — S7, S22
14. **Put the most important items first and last in lists/menus.** — Serial Position Effect. — S7
15. **Keep interface responses under ~0.4 s where possible; under 0.1 s for direct manipulation.** — Doherty Threshold; 0.1/1/10 s limits. — S7, S36
16. **Show progress in multi-step flows (step x of y) and make the end feel good (clear confirmation).** — Goal-Gradient, Peak-End, Zeigarnik. — S7, S28
17. **Absorb unavoidable complexity in the system, not the user (auto-fill, auto-format).** — Tesler's Law; Postel's Law: accept input liberally. — S7, S16

### 2.3 Navigation and information architecture

18. **On desktop, show the primary navigation; never hide it behind a hamburger.** — Hidden nav was used in 27% of desktop cases vs 48–50% visible; discoverability fell over 20%. — S25, S24
19. **On mobile, show up to 4 top-level items visibly; beyond that use a menu plus in-page links.** — Combo nav was used 86% vs 57% hidden on mobile. — S25
20. **Mark the current location (highlighted menu item, breadcrumb).** — Visibility of status. — S24, S38
21. **Menu labels are specific, familiar, front-loaded; icons only support text, never replace it.** — Vague or invented labels kill information scent. — S24
22. **Submenus open on click/tap, not hover only; mark them with a caret.** — Hover fails on touch and keyboard. — S24
23. **Avoid multi-level cascading menus; use mega menus or landing pages.** — Cascades are hard to steer. — S24
24. **Breadcrumbs show hierarchy (not history), end with the unlinked current page, and are skipped on sites only 1–2 levels deep.** — S38
25. **On mobile, shorten breadcrumbs to the parent level; do not let them wrap.** — S38
26. **Footer always carries contact, customer service, privacy policy, terms; repeat main nav on long pages; keep it to ~2 levels.** — Users look for these there. — S40
27. **Use infinite scroll only for browse-style feeds; for shops/search results use pagination or "Load more" so the footer stays reachable and items can be found again.** — S47
28. **Links navigate, buttons act.** — Links support new tabs and visited state; checkout steps are the accepted exception. — S29

### 2.4 Home page and landing page content

29. **Within the first screen, state who you are and what you offer in plain words (name + logo top-left + one concrete tagline).** — Generic "Welcome" lines waste the most-read space. — S22
30. **Use real photos of the actual business, product, staff and process, not stock decoration.** — Real imagery informs and builds credibility. — S22, S23
31. **Show concrete examples of content (actual products, menu items, services with prices), not only category links.** — S22, S44
32. **Avoid "false floors": make it obvious the page continues below the first screen.** — S22
33. **One visually dominant primary task; secondary paths grouped by audience.** — S22
34. **No autoplay video, no animated headline/logo, no splash screens or non-legal popups.** — Motion distracts and delays core content. — S22, S31
35. **Prefer one strong static hero over a carousel; if a carousel is used: ≤5 frames, visible position count, clear controls inside it, no auto-advance on mobile, and key messages repeated elsewhere.** — Many users never see later frames. — S39
36. **Front-load: key facts in the first two paragraphs; headings whose first two words carry the meaning; lists for lists; bold sparingly.** — Users scan in F-patterns. — S37

### 2.5 Forms and input

37. **Ask only what you need; justify every field (question protocol) and drop the rest.** — Each field adds abandonment. — S21, S4, S28, K7
38. **Single-column layout; only tightly related short fields share a row (e.g. city/postcode, start/end date).** — Keeps vertical flow. — S4, K7
39. **Labels above fields on mobile and short forms; always visible, never replaced by placeholder.** — Placeholders vanish, hurt review, contrast and screen readers. — S3, S4, S8, S42
40. **Put hints and format rules outside the field, before input; keep a hint to one short sentence.** — S3, S4, S19, K9
41. **Size inputs to the expected length; show units next to the field, not inside the label.** — S4, K7
42. **For 2–5 options use radio buttons/segmented buttons; for small counts use a stepper; reserve dropdowns for long lists.** — Dropdowns hide options and cost extra taps. — S9, S4
43. **One full-name field instead of first/last split (for Korean audiences this is also the native convention).** — 42% typed full name into "First name" in Baymard tests. — S11
44. **Hide rarely needed fields (address line 2, company, coupon) behind a link.** — Visible coupon fields send users off-site hunting codes. — S11, S13
45. **Explain why sensitive data (phone, ID) is needed, right next to the field.** — 68% are reluctant to give phone numbers at checkout. — S13, K11
46. **Use correct input types and `autocomplete` attributes so mobile keyboards and autofill work.** — S27, K7
47. **Never block paste; offer "show password".** — K9
48. **Ask each piece of information once per journey; pre-fill from earlier steps or the logged-in profile.** — S19, S41, K7, K10
49. **No Reset/Clear buttons; if Cancel exists, make it visually weaker than Submit.** — Accidental data loss. — S4, S8, K10
50. **Group related controls (radio sets) with `fieldset`/`legend`; every control has a programmatic `<label>`.** — S28, K7
51. **Split long forms into steps with a progress indicator; allow going back without data loss; offer save-draft for long applications.** — S28, K7, K10, S2
52. **Before final submit of a consequential form, show a "check your answers" summary with a change link per section; the change returns to the summary.** — Catches mistakes, raises confidence. — S20, K10
53. **Avoid time limits; if unavoidable, warn in advance (KRDS: at least 20 s before session expiry) with "extend" and "log out" buttons.** — S28, K9

### 2.6 Buttons and calls to action

54. **One primary (filled) button per view; at most two prominent buttons.** — Hierarchy guides the next step. — S17, S30, S22
55. **Button labels start with a verb and name the outcome ("예약하기", "장바구니 담기"); about four words or fewer.** — Users scan for buttons and read only the first words. — S29, S30, S17
56. **Replace generic "Learn more / Click here" with destination-specific text; every link label unique and understandable out of context.** — Information scent; screen-reader link lists. — S45, S22, S37
57. **Show work-in-progress inside the button (spinner, "결제 중…") and block duplicate submission; still dedupe on the server.** — Users re-click when nothing seems to happen. — S30, S17, K7, S6
58. **Destructive actions are never the default/primary role; use a two-step pattern with a warning style only on the final confirm, and do not rely on red alone.** — S17, S30, S33
59. **Highlight the preferred option by style, not by size; keep button sizes equal within a set.** — S30
60. **Touch targets: aim for 44×44 pt/CSS px (Apple, WCAG AAA 2.5.5); never below 24×24 CSS px without spacing (WCAG AA 2.5.8).** — Finger width limits density. — S26, S30, S31, S10
61. **Every custom button needs a visible pressed state and a visible keyboard focus state.** — S30, S46

### 2.7 Mobile UX

62. **Prioritise content: high content-to-chrome ratio; each new element must justify what it pushes off-screen.** — S32
63. **Lead with the gist, details on demand.** — S32, S43
64. **Save state continuously so interrupted users can resume.** — Mobile sessions are fragmented. — S32
65. **Make tasks self-contained; do not require copying data between apps.** — S32
66. **Use device capabilities to cut typing: location, camera, biometrics, wallet pay, phone dialer for "전화하기".** — S32
67. **Every gesture has a visible on-screen alternative (button).** — Gestures are hard to discover. — S32, S31
68. **Spacing between targets: about 8 px (2 mm) minimum; larger for frequent or costly actions.** — S10, S31
69. **Use +/- buttons (with an editable field) for quantities, not a bare text box.** — 95% of sites get this wrong; mobile suffers most. — S13

### 2.8 E-commerce and booking flows

70. **Show the full price, including delivery fee, tax and fees, on the product page and before payment details.** — Extra costs are the #1 abandonment reason (40%). — S12, S23, S44
71. **Offer guest checkout; offer account creation after purchase.** — 18% abandon when forced to register. — S12, S11, S13
72. **Target 8–14 form elements in checkout.** — Average is ~23; most sites need ~8 fields. — S11, S12
73. **Default billing = shipping address; reveal billing fields only on demand.** — S11
74. **Show an estimated delivery/pickup date (or range), not only a speed like "2–3일".** — Users should not have to calculate. — S13
75. **Collapse completed steps into readable summaries.** — S13
76. **Mark both required and optional fields** (Baymard) — 32% missed a required field when only optional was marked. See disagreements. — S13
77. **Product page: multiple real photos with zoom, descriptive name, short front-loaded description, per-option availability, clear add-to-cart with confirmation.** — S44
78. **Reviews: sortable/filterable, negative reviews easy to find, reviewer context, verified-purchase marks.** — Shoppers read negatives first. — S44
79. **Booking date pickers: calendar for dates within ~a year, typed entry for distant dates; grey out unavailable dates; disable impossible ranges (return before departure); keep the month view stable between start and end selection; highlight the selected range.** — S41
80. **For a short list of available slots (≤ ~10), show them as tappable buttons instead of a calendar.** — S41, S9
81. **Accept flexible formats (spaces, hyphens, leading zeros) and normalise them; do not reject "010 1234 5678" vs "010-1234-5678".** — Postel's Law. — S16, S41, S7
82. **Ask eligibility questions first and tell people early if they cannot use the service.** — S21, K10
83. **After completion: confirmation screen with key details summary, link to status, next action.** — S20, K10

### 2.9 Trust signals

84. **Show contact details (phone, address, business hours) prominently, at least in header utility area and footer.** — S23, S40
85. **Disclose prices, fees, refund/return policy and delivery charges up front; link policies near the purchase action.** — S23, S12
86. **Fix typos, broken links, layout bugs; they signal carelessness or even hacking.** — S23, S15
87. **Do not gate value behind login or personal-data walls.** — S23, K9
88. **Show the real process and the real people doing the work.** — S23
89. **Link to third-party reviews and presence (maps, review sites, social); users trust these more than self-hosted testimonials.** — S23
90. **Visually encapsulate the card/payment fields (distinct border/background) and place 1–2 recognisable security marks inside that area.** — 19% abandon for distrust of card handling; perception is a gut feeling. — S15, S12
91. **Keep information accurate and current; if an update is delayed, say so and when it will be fixed.** — K5

### 2.10 Error, empty and loading states

92. **Place each error message next to its field, plus (on submit) a summary at the top that receives focus.** — S16, S2, K6, K7
93. **Error text says what went wrong and how to fix it, in plain words, reusing the field's label.** — S18, S2, K6, K2
94. **Never only colour: combine icon, border, text and weight.** — S2, S4, S31
95. **Keep the user's input after an error; never clear the field.** — S2, S4, S16, K6, K7
96. **Do not show errors before the user has had a chance to type (no error on mere focus/empty blur).** — Feels like a false accusation. — S2, S14
97. **Clear the error as soon as the input becomes valid.** — S14
98. **Match severity to component: inline/toast for minor, dialog for severe; do not put an important error in a toast that disappears.** — S2, K2
99. **Offer the fix as an action (retry button, "문의하기" button, suggested correction) instead of instructions to phone someone.** — K2, S2
100. **Eligibility/permission problems are not validation errors: send users to a page that explains the outcome and next step.** — S16, S18
101. **No humour, "oops", blame words ("잘못된", "invalid", "forbidden") in routine errors.** — S2, S18, S43
102. **Empty state: never a blank box. Say there is nothing yet, what will appear here, and give a button to create/add the first item.** — S5
103. **Never show "no results" while data is still loading.** — Destroys trust. — S5
104. **Loading: <1 s show nothing; 1–10 s spinner (one module) or skeleton (whole page) with a line of text; >10 s percent-done or step count with time estimate and a way to cancel.** — S6, S34, S36
105. **Skeletons must preview the actual layout, not just header/footer frames.** — S34
106. **Confirm only serious, irreversible actions; name the item and effect; label buttons with outcomes ("삭제하기"/"취소"), no "예/아니요", no default on the destructive choice. Prefer Undo for everything else.** — Overused confirms get clicked blindly. — S33, K8

### 2.11 Accessibility

107. **Text contrast ≥ 4.5:1 (≥ 3:1 for large/bold text); focus indicators ≥ 3:1.** — S31, S46, S17
108. **Visible focus everywhere; never `outline: none` without an equal replacement; focus must not be hidden under sticky bars.** — S46, S42
109. **Focus order follows visual order; no positive `tabindex`; first focusable element is a "본문 바로가기" skip link.** — S46, S42
110. **Page has a descriptive `<title>`, `lang="ko"`, and a real heading hierarchy (form sections use h2–h6).** — S42, K7
111. **Meaningful images have short alt text describing purpose.** — S42
112. **Text can be enlarged to 200% without breaking layout.** — S31, S42, K11
113. **Respect reduced-motion preferences; no autoplay audio/video without controls.** — S31, S22
114. **After an error, move focus to the error (or first errored field); after a modal error closes, return focus to the field.** — K6, K7, S16
115. **Range sliders and drag-only controls need a non-drag alternative.** — S19, S31
116. **Provide built-in text-size and high-contrast options for public/senior-heavy services.** — K11 (5 text-size steps, light/dark/system), K12

### 2.12 UX writing / microcopy

117. **Pick a tone on four axes (formal–casual, serious–funny, respectful–irreverent, matter-of-fact–enthusiastic), stay near the middle, and shift by context (more serious for errors, money, health).** — S35
118. **Write so the next screen is predictable: the button/link says what will happen after tapping.** — K1, S45
119. **Cut words that change nothing ("앞으로", "해당", "~하실 수 있습니다 → ~할 수 있어요"), remove sentences that repeat the title.** — K1, S37
120. **One message per sentence; must sound natural when read aloud.** — K1, S18
121. **Suggest, do not threaten; no fear or loss framing to stop users leaving.** — K1, K2
122. **Use words anyone understands; no slang, memes, or industry terms.** — K1, S43, S1
123. **Frame around what users can do, not what they cannot.** — K2, S43
124. **Do not refer to controls by type ("저장 버튼을 누르세요" → "저장을 누르세요"); refer by the label text.** — S43
125. **A dialog's title and buttons alone should explain the decision.** — S43, K8
126. **Unify messages for the same situation and template recurring ones (maintenance: only bank/time vary).** — K3, K4
127. **Sentence case for English UI** (GOV.UK, NN/g) — Apple uses title case; irrelevant for Korean but matters for bilingual sites. — S17, S29, S30

---

## 3. Disagreements between sources

- **When to validate.** GOV.UK: validate on submit only, never on blur or while typing (S16). Baymard: validate inline on blur, or when a fixed-length field is complete, and clear on keystroke (S14). KRDS: keyup for rules like ID duplication/password, focus-out for whole values like dates, plus server check on submit (K7). NN/g: real-time only for fields with frequent first-try errors like passwords (S2). Practical rule: validate on blur for format, live only for password rules, always re-check on submit with summary.
- **Disabled buttons.** GOV.UK: avoid disabled submit buttons (poor contrast, confusing) (S17). KRDS: may disable submit until required fields are filled, and must disable during submission (K7). Practical rule: keep submit enabled and explain on press; disable only while processing.
- **Required vs optional marks.** GOV.UK: mark only optional with "(선택)", never asterisks (S19). Baymard: mark both required and optional, since marking only optional made 32% miss required fields (S13). KRDS: mark whichever is the minority, consistently site-wide (K7). NN/g: minimise optional fields and label them (S4).
- **Button placement.** GOV.UK: Continue left-aligned (S19). KRDS: action buttons bottom-right, submit rightmost (K7). Apple watchOS/iOS: full-width primary on small screens (S30). For Korean mobile web, full-width bottom primary is the market norm; on desktop forms follow KRDS for public services.
- **"Please" / "sorry".** GOV.UK bans both in error messages (S18). Toss and KRDS require a polite style even when the service is at fault (K3, K6). In Korean, politeness is carried by the ending (해요체), not by "죄송합니다" filler — keep endings polite, skip ritual apologies except for real service failures.
- **Humour in errors.** NN/g allows delight only in total outages (S2); Material and GOV.UK reject humour in errors (S43, S18); Baemin is known for witty copy (third-party commentary only, not verified).
- **Progress indicators.** W3C and KRDS want progress shown in multi-step forms (S28, K7); GOV.UK says add one only if research shows it is needed (S19).
- **Floating labels.** NN/g: acceptable only when space is tight; a label above the field remains best (S3).

---

## 4. Korean-specific notes

- **Speech level.** Toss applies polite 해요체 to all product copy, including errors caused by Toss itself (K3). Use 해요체 for consumer services (shops, booking). Public services (KRDS) require a "정중한 문체" that reassures (K6); 합니다체 is common in government notices, but do not mix the two on one screen. Pick one per product and record it.
- **Toss's 8 principles (K1)** as a checklist for every screen: 다음 화면 예측 힌트, 잡초 뽑기, 빈 문장 제거, 핵심 메시지 집중, 말하기 쉬운 표현(한자어·문어체·긴 호흡 피하기), 강요 대신 권유, 누구에게나 무해한 말, 숨은 감정 공감.
- **Toss error principles (K2):** the best error is one that never happens; pick the right component (toast vs dialog); give the self-fix; use user language; make the fix one tap; prefer "~할 수 있어요" over commands.
- **Avoid 한자어 and admin words** in consumer copy (해당, 상기, 기재, 금일, 익일 → 이, 위, 적기, 오늘, 다음 날). Read aloud test. (K1 principle 5)
- **Names.** One "이름" field; Korean users do not split family/given name. (S11 supports single field.)
- **Phone numbers.** Accept with or without hyphens/spaces and format automatically; use `type="tel"` and `autocomplete="tel"`. (S16, S27)
- **Address.** Korean convention is postcode search (도로명주소 검색) → auto-filled base address → one "상세주소" field. Matches Baymard's address-lookup advice (S11). Do not show a second address line by default.
- **Login (KRDS K9).** Login link in the same visible spot on every screen with icon + label; offer the common methods (간편인증, 아이디/비밀번호) without splitting equal methods into tabs; show ID format hints before input; show-password; never block paste; find-ID/password links; ask for login only when needed and offer "로그인 안 함"; warn ≥20 s before session expiry with extend/logout buttons.
- **Applications (KRDS K10).** Official service name as title, no ellipsis; state all channels incl. offline; list required documents with direct open; eligibility first; no tabs/accordions splitting sections inside one step; temp save for long forms; pre-fill from authentication; mandatory confirm step when submission cannot be edited; completion page with summary and a link to status; history with current processing state.
- **Confirm dialogs (KRDS K8).** Use only for hard-to-undo actions; buttons named by action ("동의함/동의안함"), readable without the body; say what is restricted if the user refuses.
- **Public-service trust.** Government sites show the official government banner and logo in header and footer (K5). Small businesses should mirror the Korean norm of a footer business-information block (상호, 대표자, 사업자등록번호, 통신판매업 신고번호, 주소, 연락처) — this is a legal/market convention in Korea, not taken from the sources above; verify per business type.
- **Accessibility in Korea.** KRDS cites KWCAG 2.2 alongside WCAG (K6, K7); the site itself offers 5 text-size steps and 기본/선명하게/시스템 display modes (K11). Kakao's accessibility guide stresses larger text, large touch areas and adjustable contrast, plus Easy-Read wording with illustrations for people with developmental disabilities (K12). For senior-heavy audiences (clinics, local services), offer text-size controls.
- **Consistency system.** Toss treats voice as one person speaking across ~40 services and ships error copy as reusable templates (K3, K4). Build a small glossary + message templates per project (fits the ui-wording skill).
- **Common Korean button wording.** Verb-noun with -하기 or plain noun is the market norm ("예약하기", "장바구니", "구매하기", "다음"). GOV.UK prefers "Continue" over "Next" (S19), but in Korean "다음" is the established convention for step buttons; use "확인" only when it truly confirms.

---

## 5. Not accessed / limits

- Material Design 3 (m3.material.io): JavaScript-only, no text returned. Replaced by the Google Material communication codelab (S43).
- Apple HIG HTML pages are JS-only; read via Apple's public JSON data endpoints instead (S30, S31).
- Baymard touch-target article: returned only a promotional snippet.
- lawsofux.com/about: 404; author attribution to Jon Yablonski is from general knowledge, unverified here.
- GOV.UK publishing "writing guidelines" pages: only navigation was returned; specific plain-English rules not read.
- 당근, 배민 official design/writing blogs: not found by search; only third-party commentary exists, not used as sources.
- Kakao accessibility design guide itself is not public; only the press release (K12) was read.
- KRDS summary pages carry concept text only; detailed rules were read only for 오류, 입력폼, 확인, 로그인, 신청.
