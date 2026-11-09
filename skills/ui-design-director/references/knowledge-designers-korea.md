# Korean designers: free lessons distilled into rules

Researched 2026-11-09 from free material by practising designers, research groups and design-system teams; each rule links its source, rewritten in our own words. Rules here are background: `build-rules.md` and the chosen base win when they disagree. Read only the section you need.

## Contents
- 1. People
- 2. Rules by topic
- 3. Their warnings about generic or templated design
- 4. Disagreements and tensions
- 5. Not reached

Read on 2026-11-09. All rules are paraphrased. Each rule links to the page it came from. Credentials come from the person's own page or the publisher's byline/profile. Anyone whose credentials could not be checked is listed under "Excluded" and is not used as a rule source.

## 1. People

| # | Name | Verified credentials | Sources | Read |
|---|------|---------------------|---------|------|
| P1 | 김자유 | UX Writer at Toss (design chapter writing team); earlier content marketer, designer, agency design-system work; runs the 디독 newsletter (publisher profile) | [toss.tech 8 writing principles, 2022-11-15](https://toss.tech/article/8-writing-principles-of-toss) · [Toss Feed interview, 2021-02-18](https://toss.im/tossfeed/article/uxwriter-interview) · [ditoday PEOPLE, 2021-10-12](https://ditoday.com/?p=53919) | 2026-11-09 |
| P2 | 김지윤 | Brand designer at Toss; led Toss Product Sans with 산돌 and 이도타입 | [Toss Feed, 2021-10-08](https://toss.im/tossfeed/article/beginning-of-tps) | 2026-11-09 |
| P3 | 윤성권, 김소현, 강수영, 정희연 | Toss: Product Designer (송금), Product Designer (타임라인), UI/Platform Designer (TDS), Head of UX | [Toss Feed, 2019-03-11](https://toss.im/tossfeed/article/toss-designer-interview) · [Toss design conference recap, 2019-04-18](https://toss.im/tossfeed/article/toss-design-conference) | 2026-11-09 |
| P4 | 김현지 | Visual Designer, 토스뱅크 | [toss.tech, 2026-09-22](https://toss.tech/article/asset_management) | 2026-11-09 |
| P5 | 고명은 | Visual Designer, 토스뱅크 | [toss.tech, 2026-09-30](https://toss.tech/article/chipmunk) | 2026-11-09 |
| P6 | 서자영 | Product Designer, 토스뱅크 | [toss.tech, 2026-09-21](https://toss.tech/article/remittance_transfer) | 2026-11-09 |
| P7 | 길형진 | Designer of Pretendard (open-source Korean UI typeface, v1.3.9) | [cactus.tistory.com/306, 2021-06-28 (upd. 2023-11-06)](https://cactus.tistory.com/306) · [GitHub README](https://github.com/orioncactus/pretendard) | 2026-11-09 |
| P8 | 노은유 | Type designer, runs NohType; designed 네이버 마루 부리 (2021), Noh 옵티크, Noh 소리체; teaches typography | [Sandoll interview (c. 2022, undated)](https://www.sandollcloud.com/font-designer/interview/42) | 2026-11-09 |
| P9 | 양희재, 장수영 | Type studio 양장점 (since 2016): 양희재 Latin (Fifty, Palais, Sonora; Ktowntype), 장수영 Hangul (펜 series) | [월간 디자인, 2024-04-25](https://design.co.kr/article/14117/) · [월간 디자인, 2021-02-17](https://design.co.kr/article/19235/) | 2026-11-09 |
| P10 | 민지희, 태주희, 금재현 (우아한형제들) + 박부미, 김초롱, 강주연, 이도경 (산돌) | Makers of 배민 한나·주아·도현체 | [ditoday special, 2017-08-10](https://ditoday.com/?p=429) | 2026-11-09 |
| P11 | 진의준, 박안나, 박찬혁 | Product Designers at pxd (UX agency) | [pxd story 1798, 2024-10-02](https://story.pxd.co.kr/1798) · [pxd story 1805, 2024-10-10](https://story.pxd.co.kr/1805) | 2026-11-09 |
| P12 | 박인 | 과장, UI/UX design planning at KB국민카드; led its UX writing guideline | [ditoday, 2021-10-13](https://ditoday.com/?p=53998) | 2026-11-09 |
| P13 | 임주열 | UX designer, 17 years, NAVER Place design team (Naver Map) | [navercorp story, 2025-03-05](https://navercorp.com/story/storyDetail?seq=32348) | 2026-11-09 |
| P14 | 전상호 | 페이앱 설계 리더, 네이버페이; former agency designer | [Wanted article, c. 2025](https://www.wanted.co.kr/events/article_250704) | 2026-11-09 |
| P15 | 박가영 | Logo designer; hundreds of small-brand logos (어부아저씨, cafe calendar, lily annmarie, 몽상가들) | [ditoday, 2020-01-07](https://ditoday.com/로고를-디자인한다는-것-사랑하는-브랜드가-늘어간/) | 2026-11-09 |
| P16 | 뭐든지 스튜디오 (슬로워크) | Agency brand for start-ups and small shops; individuals not named | [ditoday, 2017-09-08](https://ditoday.com/?p=4011) | 2026-11-09 |

Team documents with no named author. Used only to back up a person's rule and marked [team]:
- Toss product principles, 2025-09-17: https://toss.im/tossfeed/article/tossproductprinciples
- Apps in Toss consumer UX guide (undated): https://developers-apps-in-toss.toss.im/landing-page/landing-page-en/design/consumer-ux-guide
- Toss design team Q&A, 2019-08-02: https://toss.im/tossfeed/article/toss-design-team-qna

Excluded because credentials could not be checked (pen name, no profile, or vendor page): 디자인 나침반 (요즘IT 1017, typography sizes), 마요 (요즘IT 1552), 방지니 (brunch microcopy), 프레이 @kim-yezi (brunch, "why AI screens all look alike"), 유은선 (brunch, "professor" with no affiliation), 김도영 (요즘IT 2799), 디자인씽킹 그룹 THIS (ppss, 이투스 density; credentials self-described only), 데이지 인사이터 (ditoday, KakaoTalk critique), and kmong/Wix/Hostinger vendor pages. Some of them are mentioned in section 4 as counterpoints only, labelled "unverified".

---

## 2. Rules by topic

### 2.1 UX writing: tone, sentences, buttons

1. **Write every product string in 해요체, and keep one voice across the site.** Users experience the service as one speaker, even when different teams write the screens. — Toss writes copy as if one person is speaking, and puts the writing rules inside the design system rather than in a separate document. — [P1 Toss Feed](https://toss.im/tossfeed/article/uxwriter-interview), [team: Apps in Toss guide](https://developers-apps-in-toss.toss.im/landing-page/landing-page-en/design/consumer-ux-guide)
2. **Drop stiff honorific forms by default (`~시`, `계시다`, `여쭈다`, `께`). Keep them only for questions about the user's situation, guesses about it, or favours you ask (surveys).** — Default copy should sound casual and polite, not ceremonial. — [team: Apps in Toss guide](https://developers-apps-in-toss.toss.im/landing-page/landing-page-en/design/consumer-ux-guide)
3. **Use active, positive sentences ("있어요", not "없지 않아요"). Use negative wording only when something cannot be used, and give the reason.** Use the passive only for service ending or expiry, or when reassuring. — [team: Apps in Toss guide](https://developers-apps-in-toss.toss.im/landing-page/landing-page-en/design/consumer-ux-guide)
4. **A button label or the line above it must say what happens next.** — A "다른 곳에서 후불결제 하기" button that silently opened a survey made users uneasy. — [P1 8 principles](https://toss.tech/article/8-writing-principles-of-toss)
5. **A single CTA ends in "~하기". Step buttons say "확인" or "다음". In a two-button dialog the dismiss button says "닫기" or "다음에", not "취소".** — "취소" reads as cancelling the task the user is in the middle of. — [P1 Toss Feed](https://toss.im/tossfeed/article/uxwriter-interview), [team: Apps in Toss guide](https://developers-apps-in-toss.toss.im/landing-page/landing-page-en/design/consumer-ux-guide)
6. **A bottom-sheet or modal title fits on one line.** — [P1 Toss Feed](https://toss.im/tossfeed/article/uxwriter-interview)
7. **Cut filler words. If deleting a word ("앞으로" etc.) leaves the meaning unchanged, delete it.** — The goal is removing filler, not shortening text for its own sake. — [P1 8 principles](https://toss.tech/article/8-writing-principles-of-toss)
8. **Do not add sentences because the layout looks empty, and do not repeat the title in the body.** — [P1 8 principles](https://toss.tech/article/8-writing-principles-of-toss)
9. **Show only what the user needs at this step. When there are two options, state the real difference between them.** — [P1 8 principles](https://toss.tech/article/8-writing-principles-of-toss); [team: "One Thing" per page](https://toss.im/tossfeed/article/tossproductprinciples)
10. **Write the way people talk: everyday words, one message per sentence, few 한자어 compounds, no formal written style. Test by reading the copy aloud.** — [P1 8 principles](https://toss.tech/article/8-writing-principles-of-toss); [team: break Sino-Korean compounds into verbs](https://developers-apps-in-toss.toss.im/landing-page/landing-page-en/design/consumer-ux-guide)
11. **Suggest rather than push. No loss-aversion threats ("놓치면 손해") and no pleading or guilt-trip copy or graphics.** — Keep the benefit and the facts, and leave the choice with the user. — [P1 8 principles](https://toss.tech/article/8-writing-principles-of-toss); [team: dark-pattern list](https://developers-apps-in-toss.toss.im/landing-page/landing-page-en/design/consumer-ux-guide)
12. **No slang, memes, or terms only one age group or trade understands.** — [P1 8 principles](https://toss.tech/article/8-writing-principles-of-toss); [P12 KB](https://ditoday.com/?p=53998)
13. **Acknowledge the user's effort or feeling at key moments (a loan paid off, an order completed), not just the system state.** — Toss saw much better metrics when it changed a repayment notice from a "check your balance" alert to a message that recognised the effort. — [P1 Toss Feed](https://toss.im/tossfeed/article/uxwriter-interview)
14. **Error messages give at least the cause, and then a fix. Never leave the user guessing by trial and error.** — [P1 ditoday](https://ditoday.com/?p=53919)
15. **A status label must show progress, not a frozen "정상".** Cut internal states down to what the user cares about (e.g. 9 to 3: 처리 중 / 해외 은행 도착 / 완료). — [P6](https://toss.tech/article/remittance_transfer)
16. **Echo cryptic input back in human terms (a code becomes the bank name), and replace free-text fields with guided selection where typos are costly (addresses).** — [P6](https://toss.tech/article/remittance_transfer)
17. **Turn jargon into plain words, but if plain wording changes the meaning, keep the term and add a short explanation.** — [P12 KB](https://ditoday.com/?p=53998); [P1 "Zero Jargon"](https://toss.im/tossfeed/article/uxwriter-interview)
18. **Never use exaggerated or misleading copy to raise clicks.** — [P1 Toss Feed](https://toss.im/tossfeed/article/uxwriter-interview)
19. **Lead with the value, then ask for the action, and say why an input is needed.** — [team: Value First, Explain Why](https://toss.im/tossfeed/article/tossproductprinciples)
20. **Build the voice from patterns already in good copy, and get the team to agree before writing a guideline.** An unwanted guideline goes unused. — [P1 ditoday](https://ditoday.com/?p=53919)
21. **Pick the headline message from the customer's real worry, not the feature list** ("cheapest" became "보내면 보이는", because fear of not knowing beat price). — [P6](https://toss.tech/article/remittance_transfer)

### 2.2 Korean typography for screens

22. **Use a typeface made for screens. Do not put a print-era Hangul face in body text without testing it on screen.** — Apple Gothic drew readability complaints on early iPhones. — [P8 노은유](https://www.sandollcloud.com/font-designer/interview/42); [P9 양희재: digital is now the final destination of type](https://design.co.kr/article/14117/)
23. **Do not use display or ornate faces at small sizes or on low-resolution screens. Give them large headline sizes.** — 펜돋움 Thin's designer asks that it not be output at low resolution because of its fine angled details. — [P9 장수영](https://design.co.kr/article/19235/), [P8](https://www.sandollcloud.com/font-designer/interview/42)
24. **When a family is split by optical size (Display/Text), pick the cut by set size, not by weight.** — [P8](https://www.sandollcloud.com/font-designer/interview/42)
25. **A safe default UI face is Pretendard (OFL). It matches Apple SD 산돌고딕 Neo spacing and SF heights, so it behaves like `-apple-system` on every OS.** Use the dynamic subset (or variable dynamic subset) to keep Korean font weight low. In Next.js, set the variable weight range (`'45 920'`) or WebKit renders the wrong weight. — [P7 blog](https://cactus.tistory.com/306), [P7 README](https://github.com/orioncactus/pretendard)
26. **Turn on tabular figures (`tnum`) for prices, dates, tables, and live numbers. Use proportional figures for a single hero number.** — Toss Product Sans ships both modes for this reason, and Pretendard exposes `tnum`. — [P2](https://toss.im/tossfeed/article/beginning-of-tps), [P7](https://cactus.tistory.com/306)
27. **Check mixed Hangul–Latin–digit lines. Digits and Latin in many Korean fonts look small and thin next to Hangul, and punctuation sized for one script looks wrong beside the other.** Choose a font that balances them rather than patching it per element. — [P2](https://toss.im/tossfeed/article/beginning-of-tps), [P8](https://www.sandollcloud.com/font-designer/interview/42), [P7: Noto Sans KR Hangul sits large](https://cactus.tistory.com/306)
28. **Treat %, +/−, ₩, arrows, and brackets as UI glyphs. Check that they are vertically centred and evenly spaced in buttons and price rows.** — [P2](https://toss.im/tossfeed/article/beginning-of-tps), [P7: adjusted @, ₩](https://cactus.tistory.com/306)
29. **Check text centring inside buttons on Windows/Chrome as well as iOS/Safari. Hangul vertical metrics differ by OS, and that is why developers add padding hacks.** — [P2](https://toss.im/tossfeed/article/beginning-of-tps)
30. **Make sure the font covers all 11,172 Hangul syllables (or loads a fallback). The 2,350-character KS set breaks on user-typed names and chat input.** — [P2](https://toss.im/tossfeed/article/beginning-of-tps)
31. **Use one middle dot code point (·, U+00B7) and one ellipsis style across the site.** Pretendard `ss05` gives a Korean-style ellipsis. — [P2](https://toss.im/tossfeed/article/beginning-of-tps), [P7](https://cactus.tistory.com/306)
32. **Keep two body text families: "Compact" with tight leading for UI labels, buttons, and tables, and "Body" with loose leading (about 160%, not 130%) for running text.** Do not make a new style for every component. — [P11 pxd](https://story.pxd.co.kr/1798)
33. **Name text sizes so they can grow in both directions: body `sm/md/lg` around a medium base, headings `01, 02…` counting up from the body base.** — [P11 pxd](https://story.pxd.co.kr/1798)
34. **A brand display face (배민 style) is for marketing, packaging, and headline moments, not body text.** Its deliberate irregularity (uneven weight, joined jamo) hurts readability at reading sizes. — [P10](https://ditoday.com/?p=429)
35. **If you borrow from Korean street signage for a display face or logo, follow the tool and material of the original (cut acrylic, brush on tin). Make the quirks systematic, not random.** — [P10](https://ditoday.com/?p=429)

### 2.3 Layout, density, hierarchy

36. **One page, one main job. Make the next action obvious at a glance.** — [P3 송금 keypad-first](https://toss.im/tossfeed/article/toss-designer-interview), [P3 "One Thing per One Page"](https://toss.im/tossfeed/article/toss-design-conference), [team](https://toss.im/tossfeed/article/tossproductprinciples)
37. **Merge scattered lookups into one chronological or unified list when users want the overview** (Toss Timeline merged all accounts and cards). — [P3](https://toss.im/tossfeed/article/toss-designer-interview)
38. **On a crowded screen, separate by role. The user's own data stays in the main layer, and suggestions go in a separate, smaller layer that shrinks on scroll and can be reopened.** — A structural change raised CTR and CVR about 3×, while restyling alone gave only 1.1×. — [P4](https://toss.tech/article/asset_management)
39. **Before restyling, ask whether the problem is structural.** — [P4](https://toss.tech/article/asset_management)
40. **Graphics must not push key information below the fold or add scrolling. Size graphics to the density of the information.** — [team: Apps in Toss guide](https://developers-apps-in-toss.toss.im/landing-page/landing-page-en/design/consumer-ux-guide)
41. **Align at the pixel level (bubble-to-character gaps, stat rows). Small misalignments make a screen feel assembled rather than designed.** — [P5](https://toss.tech/article/chipmunk)
42. **Build from shared components and tokens so every page looks and behaves the same. Rebuilding the same screen per page creates inconsistency and design debt.** — [P3](https://toss.im/tossfeed/article/toss-designer-interview), [P3 conference](https://toss.im/tossfeed/article/toss-design-conference)
43. **Add features or sections only as a last resort.** Every extra block adds complexity. — [P3 Minimum Feature](https://toss.im/tossfeed/article/toss-design-conference), [team](https://toss.im/tossfeed/article/tossproductprinciples)
44. **On a site that many businesses or old users depend on, move things cautiously. Even one moved button affects people who rely on it. Serve sub-groups in their own corner (e.g. a MY tab) rather than redesigning for one age group.** — [P13 Naver Map](https://navercorp.com/story/storyDetail?seq=32348)
45. **Make the service usable by everyone (older users, people left out of digital finance), not just easy for some.** — [P3](https://toss.im/tossfeed/article/toss-designer-interview)

### 2.4 Colour and imagery

46. **Functional UI should not look like an ad. Ads use big graphics and vivid colour, while features rely on text, buttons, and hierarchy. Strip colour and illustration from anything that must read as "your information".** — [P4](https://toss.tech/article/asset_management)
47. **Add finish with restraint: corner smoothing, a translucent surface, a faint button gradient. Avoid loud colour.** — [P4](https://toss.tech/article/asset_management)
48. **No decorative filler: meaningless illustrations, particles, heavy gradients. One icon or emoji at a time, sized 24–40px, and only where it matches the situation (no warning icon on a non-error, no spinner when nothing loads).** — [team: Apps in Toss guide](https://developers-apps-in-toss.toss.im/landing-page/landing-page-en/design/consumer-ux-guide)
49. **Take the accent from the brand or logo colour, and use mid-tones for graphics so they survive light and dark backgrounds.** — [team: Apps in Toss guide](https://developers-apps-in-toss.toss.im/landing-page/landing-page-en/design/consumer-ux-guide)
50. **Name colour tokens by element + intent + emphasis + state (`foreground/border/fill/background` × `basic/inverse/chromatic/static` × `subtle…strongest` × `hover/pressed/focus/disabled`).** Brand colour lives under `chromatic`, so it can be strengthened or softened without new names. — [P11 pxd](https://story.pxd.co.kr/1805)
51. **Test every illustration at the smallest size it will appear. Keep the face and silhouette readable and cut competing detail.** — [P5](https://toss.tech/article/chipmunk)
52. **When a character or mascot is the focus, rebuild the layout around it. Dropped onto a stock layout it reads as a sticker. Ground it with a shadow, and reuse its icon language across buttons and panels.** — [P5](https://toss.tech/article/chipmunk)
53. **For a series of illustrations, fix the shared style block and vary only named slots. Review the set side by side for both distinctness and cohesion.** — [P5](https://toss.tech/article/chipmunk)

### 2.5 Small shops and small brands

54. **Define the business in one or two plain sentences (why it exists, what the customer gets) before any visual work, and reuse those keywords in the name, intro, and headings.** — [P16 뭐든지 스튜디오](https://ditoday.com/?p=4011)
55. **Branding is not only a logo. Plan how the mark works on the website, signage, business cards, and the space together.** — [P16](https://ditoday.com/?p=4011)
56. **Collect a real brief first: business type, meaning of the name, interior, story, preferred style. Design from the story, not from a style list.** — [P15 박가영](https://ditoday.com/로고를-디자인한다는-것-사랑하는-브랜드가-늘어간/)
57. **Keep a small brand's mark simple and lasting, so the name or trade reads at once. If the shop sells many kinds of goods, express the value (carefully chosen goods) rather than one product.** — [P15](https://ditoday.com/로고를-디자인한다는-것-사랑하는-브랜드가-늘어간/)
58. **Do not define the audience too narrowly in the slogan.** — [P16](https://ditoday.com/?p=4011)
59. **Show business info a customer must check (price, address, hours, account or bank names) in human-readable, verifiable form.** — Reassurance beats cleverness. — Generalised from [P6](https://toss.tech/article/remittance_transfer)

### 2.6 Portfolio and critique

60. **Present each case as problem, then chosen approach and why, then result, then (optionally) what changed because of it.** — [team: Toss Q&A](https://toss.im/tossfeed/article/toss-design-team-qna)
61. **Show judgment, not just screens.** The field is moving from aesthetics to usability to business usefulness, and a designer should show service, operations, and data decisions. — [P14 전상호](https://www.wanted.co.kr/events/article_250704)
62. **Let the team feel the user's problem first-hand (have the PM send the money). Interview quotes alone rarely move priorities.** — [P6](https://toss.tech/article/remittance_transfer)
63. **Back decisions with data and user feedback, but keep human judgment for brand-sensitive copy.** — [P1](https://toss.im/tossfeed/article/uxwriter-interview), [P3](https://toss.im/tossfeed/article/toss-designer-interview), [P13](https://navercorp.com/story/storyDetail?seq=32348)

---

## 3. Their warnings about generic or templated design

- **Filler text to fill space** is a tell. Empty-looking layouts get padded with sentences that repeat the title. — [P1](https://toss.tech/article/8-writing-principles-of-toss)
- **Decoration without meaning**: stock illustrations, particles, heavy gradients, an icon on every line, warning icons on non-errors. — [team: Apps in Toss](https://developers-apps-in-toss.toss.im/landing-page/landing-page-en/design/consumer-ux-guide)
- **A loud, graphic-heavy block reads as an ad**, and users skip it. — [P4](https://toss.tech/article/asset_management)
- **A mascot or image dropped onto a stock layout** "looks like a sticker". Generic layout plus pasted art reads as a template. — [P5](https://toss.tech/article/chipmunk)
- **Pixel-level misalignment** makes a page feel "assembled". — [P5](https://toss.tech/article/chipmunk)
- **AI output is raw material.** The designer decides what to keep, cut, and refine. — [P5](https://toss.tech/article/chipmunk)
- **Logos that feel "stiff and formulaic"** (딱딱하고 틀에 박힌) come from designing without the shop's story. — [P15](https://ditoday.com/로고를-디자인한다는-것-사랑하는-브랜드가-늘어간/)
- **Branding reduced to a logo draft** (no mission, no touchpoint plan) gives interchangeable results. — [P16](https://ditoday.com/?p=4011)
- **Mismatched fonts and per-element patches** pile up as design debt. That is a sign no type decision was made. — [P7](https://cactus.tistory.com/306)
- **A print font on screen, or a display font at body size**, is the typical "it was just picked" mistake. — [P8](https://www.sandollcloud.com/font-designer/interview/42)
- **Pressure copy** (loss threats, pleading) is generic growth-hack language that Toss bans. — [P1](https://toss.tech/article/8-writing-principles-of-toss)
- Unverified, context only: a brunch writer (프레이, [link](https://brunch.co.kr/@kim-yezi/15)) traces the identical "AI page" look to shadcn/ui defaults: centred big headline, subtitle, 3–4 feature cards, testimonials, footer. The fix it gives is to replace the brand colour, font, radius, and shadow, and to give the tool reference designs and a `design.md`. This matches the Toss points above but comes from an unverified author.

---

## 4. Disagreements and tensions

1. **One voice vs tone per channel.** Toss keeps one voice for 40+ services ([P1](https://toss.im/tossfeed/article/uxwriter-interview)). KB국민카드 keeps one brand voice but changes tone by channel: polite and friendly on the homepage, terse in payments, playful in points and events ([P12](https://ditoday.com/?p=53998)). For a small business site: one voice, but terse on checkout or booking forms and warmer on story or event pages.
2. **Plain words at any cost vs keep the term.** Toss aims at "Zero Jargon" and breaking up 한자어 ([P1](https://toss.im/tossfeed/article/uxwriter-interview)). KB keeps the original term and adds an explanation when a plain rewrite distorts it ([P12](https://ditoday.com/?p=53998)). For regulated terms (contracts, refunds, medical), follow KB.
3. **Emotion vs restraint.** Toss says to find the hidden emotion and congratulate the user ([P1](https://toss.tech/article/8-writing-principles-of-toss)), but also bans emotional pleading in copy and graphics ([team](https://developers-apps-in-toss.toss.im/landing-page/landing-page-en/design/consumer-ux-guide)). The line: recognise what the user did, never guilt the user.
4. **Simplicity vs business room.** Toss designers admit the keypad-first screen leaves little room for business features ([P3](https://toss.im/tossfeed/article/toss-designer-interview)). Naver's map designer has to balance users against business owners and avoids drastic simplification ([P13](https://navercorp.com/story/storyDetail?seq=32348)). Unverified context: a 2018 ppss column ([link](https://www.ppss.kr/news/articleView.html?idxno=173074)) argues dense, decorated Korean PC layouts (이투스) were abandoned because they could not survive mobile, not because of fashion.
5. **Neutral type vs rule-breaking type.** Toss Product Sans and Pretendard aim to be unobtrusive and need no adjustment ([P2](https://toss.im/tossfeed/article/beginning-of-tps), [P7](https://github.com/orioncactus/pretendard)). 배민 deliberately broke type rules for wit, and type professionals criticised its uneven weight and spacing ([P10](https://ditoday.com/?p=429)). The two views fit together if the rule-breaking face stays at display sizes and a neutral face carries the body.
6. **Letter-spacing.** Pretendard's author tuned spacing at body size to SF/Helvetica Neue, so the font should need no extra adjustment ([P7](https://cactus.tistory.com/306)). Korean web practice often adds negative tracking to body text. The only source found recommending that (about -0.3 for 16–17pt) is a pen-name 요즘IT article ([link](https://yozm.wishket.com/magazine/detail/1017/)), so it is unverified. Default: no tracking on body, slight negative tracking on large headings only, and check per font.
7. **Graphics: remove vs centre on them.** Toss Bank's 김현지 removed graphics so a feature reads as information ([P4](https://toss.tech/article/asset_management)). 고명은 built a whole screen around a character ([P5](https://toss.tech/article/chipmunk)). The deciding question is the job of the block: user data or utility means no graphics, and an emotional or brand moment means the graphic leads and the layout serves it.
8. **Family by weight vs by optical size.** Most Korean families ship many weights, while 노은유 splits Optique into Display and Text cuts ([P8](https://www.sandollcloud.com/font-designer/interview/42)). When both exist, choose by size first.

## 5. Not reached

- medium.com/daangn returned 403. No 당근 designer article was readable, and the SEED information came only from third-party news, so it was not used.
- hangeul.naver.com (마루 부리 design notes) could not be fetched.
- No readable first-person material was found from designers at 카카오, 라인, 쿠팡, 무신사, 29CM, 오늘의집, 리디, 삼성, or LG. Search returned only news, vendor pages, or pen-name posts. 29CM coverage (ditoday 2017) named no designers.
- No transcripts of 토스 SIMPLICITY sessions beyond the 2019 conference recap. No if(kakao), DEVIEW, 우아콘, or 인프콘 design talk texts were found.
