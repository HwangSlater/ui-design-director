# What a mockup must show

Layout and gates: [page-design.md](page-design.md). Owner screens: [owner-screens.md](owner-screens.md); its rules on filled selection and status words apply to customer screens too.

## Data and computed values

1. Keep sample data in one file the build reads (`site.json`): times, stock, prices, counts, seats, orders, customers. Customer and owner screens read it, and every count is derived (seats left = capacity − booked − held; 「오늘 보낼 것」 = orders since yesterday's cut-off). Retyped copies drifted.
2. A line shared by pages (「다 팔렸어요 · 오후 1시에 또 나와요」) is one component.
3. One 「today」 per screen and all its states, with every number true that day: weekdays computed, standings as of that day, seasonal bands that fit. Pick the day the supplied data describes.
4. Totals add up, a roster is the same everywhere, one snapshot date governs every count.
5. Sample states must be possible under the rules printed on the same screen.
6. When a state changes the page, everything depending on it changes; an 「11명이면 단체라 전화로」 notice sat above a live booking button.
7. A first version and a later one of a feature (hand-answered stock, then live shelf numbers) are separate frames, never mixed; label which customers see first.
8. Numbers carrying a date derive from it (order 1104-12), asserted in the build.
9. Sample dates sit just before 「today」; a year-old 「최근 공사」 reads as no work.
10. Print a total only when it is the real total (「공사 5건」 read as five jobs a year).
11. Sample data obeys its controls: selected chips match the list, 「전체」 holds every item, one sample case keeps its photos and numbers everywhere.
12. Entry pages open with an empty cart, signed out; judges named 「장바구니 3」.
13. Prices come from one function (discounts, bundles, shipping) with asserts on the client's examples, used by cart, order screen and owner list. When two client rules meet (10% bundle, 30,000-won free shipping), ask which applies first; show the result in the cart's words (「10% 빠지고 27,900원이라 택배비가 붙어요 · 2,100원 더 담으면 무료」).
14. Opening status comes from one function over weekday, hours, break, regular day off, preset closures and a sudden 「오늘 쉬어요」 (「지금 쉬는 시간 · 저녁은 5시 반부터」); each state is its own screen. A hard-coded 「내일 11시 반에 열어요」 ignored a Monday closure.
15. Every time-dependent line uses it: drop-off ready time (Sunday afternoon → Tuesday), seasonal footer hours, the main button (call while open; when closed, leave a message with 「○요일 ○시부터 전화 받아요」).
16. Turn rules into dates (「둘째·넷째 수요일 휴무」 → 「다음 쉬는 날 11월 11일(수)」) and write hours, not 「아침」.

## Facts and wording

1. Only facts the user gave. Anything filled in (directions, walking times, days, policies, prices, staff names, FAQ answers, durations like 「보통 2주쯤」) carries 「확인 필요」 and is listed at handover; plausible guesses read as facts.
2. Never write shop rules or product descriptions, not even as 견본; leave a slot for the owner's words.
3. Descriptions the client did not give (how a tea tastes) carry 「확인 필요」 until the client writes them, even when true; then replace every tag the same day.
4. No role for a real name the user did not state; counts with units (「이준석 2골」).
5. Each fact and each heading once per screen (not 「아이 52마리」 then 「아이들」).
6. Tab titles from the page heading (「보리 · 들꽃쉼터」), never the option label.
7. Before the second page type, run `/ui-wording` and record the term table in `DESIGN.md`.
8. An empty optional block disappears; 「후기가 아직 없어요」 reads as 「후기 없는 집」.
9. Each fact-table row is one upload-form answer, so unknowns hide (「개와 지내요: 예」).
10. Reviews carry their month and a link to all reviews on their platform; drop efficacy claims (「태열 다 나았어요」).
11. Food: major allergens on every item, present or absent (「호두 들어가요 · 우유·계란 없어요」); butter is milk (「우유(버터 포함)」); one shared by every item goes on one top line.
12. Korean labels never break mid-word (「장바구 니」): `white-space: nowrap` on nav and short buttons; drop the least-used phone header item instead.
13. A text-only page may open as an enquiry desk only with the owner's real records; invented records are fake reviews. Give each record a bold one-line change (「누런 타일 → 밝은 회색 큰 타일」), a real customer line only where one exists, and only tables the owner filled completely.

## Photos

1. Supplied imagery, else licence-checked samples of the right subject and ratio, credited and labelled, hatched offline. No generated imagery; never present samples as the product.
2. Samples show only what the business makes; when none fits, use one true to the menu and ask the owner for that photo.
3. Crop people and animals on the face with a per-photo focus point (`object-position`, one tap in the upload form), checked at every ratio.
4. One subject once per screen; one sample photo in one place across the main flow; an item's gallery shows only that item (labelled slots for the rest).
5. Try every slot with a dim phone photo too.
6. Small organisations: labelled slots for a staff photo and 「이번 달」 news when the references show them.
7. Stand-ins count only if they could be the client's own (building type, region, same spot and angle for before/after, no near-duplicates); otherwise park the page as 「사장님 사진 기다림」.
8. With product photos, lists use the card grid the reference shops share, at their thumbnail size (two columns on phone, three or four at 1280); a 64px thumbnail row read as an order form. Pick columns so each last row fills; keep the grid even when one item is featured.
9. Until photos arrive, say lists will become cards and photo-less pages cap the score.
10. Before/after: 「고치기 전/고친 뒤」 as a corner tag; don't repeat the featured case as the first card; once photos arrive, list only items that have them.

## States and forms

1. Widths ≈375, ≈768 and ≈1280px+.
2. Work surfaces: each `SITE-PLAN.md` state as a frame (empty, loading, error, no permission, dense); controls in default, hover, focus, active, disabled, invalid.
3. Submit with gaps: a banner naming what is missing with links, a jump to the first, a message per field. Over-length text stays with 「2자 넘었어요」. A slot taken meanwhile says so and keeps the rest. A failed payment says no money left, in words fitting every method.
4. When the customer must know the shop saw the order, show paid → sent → confirmed; the last line changes only on staff confirm.
5. Unavailable items: greyed text plus the next action (「알림 받기」), never struck through.
6. A choice that ends the flow removes 「다음」.
7. Forms taking name, phone or address carry a consent line with purpose and retention (「개인정보 수집·이용에 동의해요 — 견적 상담에만 쓰고 3개월 뒤 지워요」, period marked 견본).
8. Before a quote or booking form, ask the owner which answers change price or date (rooms, size people know with 「모르면 비워 두세요」, move-in date, living there during work) and ask those.
9. Personal data only after the identity check the page mentions.
10. For audiences that phone first, large phone and messenger buttons at every page foot, or a labelled slot.
11. For older audiences, no controls hidden in a sideways scroll; wrap chips or show part of the next.
12. Timed interactions (undo toast) also as their own page, so captures show them.
13. Only approved motion, checked against emilkowalski/skills when installed (`companion-skills.md`).
