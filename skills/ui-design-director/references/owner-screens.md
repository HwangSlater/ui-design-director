# Owner and admin screens

Plan these in `SITE-PLAN.md` (`site-plan.md`); draw them by these rules, for an owner who "only knows how to upload a photo".

## What the screen shows

1. Show what the owner acts on, not the customer view reused: who arrives in which room tonight, not nightly prices and 「본채만 남았어요」, which the owner read backwards.
2. Read the same data file as the customer screens, so counts agree ([mockup-content.md](mockup-content.md) § Data and computed values). Order totals come from the shared price function, never typed.
3. Say who to contact for anything not on the screen.

## Signing in

1. Sign in once by text code and stay signed in on that phone.
2. Another phone needs the owner's approval.
3. Say what to do if the phone is lost (who to call).

## Changing things

1. Ask once before a change customers see at once (「오늘(수) 쉬는 걸로 바꿀까요?」).
2. Keep a large undo after it. One gloved mis-tap moved a dog to the public 「입양됨」 list.
3. Make every price a number field, never free text like 「45만~90만 원」.
4. Before saving prices, show only what changed (「8,000원 → 80,000원」), and ask again when a number more than doubles.

## Selection and status (every screen, customer or owner)

1. A selected option looks the same for every option, filled the same way. 「상담 중」 kept the outline style when chosen.
2. Only pressable things look pressable; fills are for things that can be pressed.
3. Status is coloured words: no chip, no dot before every state. A solid green 「있어요 · 2층 C-3」 looked more pressable than the button beside it.
4. Small labels on items (「포장 돼요」, 「소고기 호주산」, 「품절 임박」) are plain small text or a flat tint, never a bordered box.
5. Progress marks are filled circles, not empty boxes a customer will try to tick.

## Before sending

1. Capture owner and staff screens at 390. Grid inputs overflowed the phone: give grid children `min-width: 0` and inputs `width: 100%`.
2. Build timed parts (the undo toast) as their own page so the capture shows them.
