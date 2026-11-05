# Owner and admin screens

Plan these in `SITE-PLAN.md` (`site-plan.md`); draw them by these rules, for an owner who "only knows how to upload a photo". Selection and status styles: [mockup-content.md](mockup-content.md) § Selection and status.

## What the screen shows

1. Show what the owner acts on, not the customer view reused: who arrives in which room tonight, not nightly prices.
2. Read the same data file and price function as the customer screens ([mockup-content.md](mockup-content.md) § Data and computed values); totals are never typed.
3. Say who to contact for anything not on the screen.

## Signing in

1. For a single owner without accounts: sign in once by text code and stay signed in on that phone; where the product already has accounts, use its sign-in.
2. Another phone needs the owner's approval.
3. Say what to do if the phone is lost (who to call).

## Changing things

1. Ask once before a change customers see at once (「오늘(수) 쉬는 걸로 바꿀까요?」).
2. Keep a large undo after it; one mis-tap can publish a wrong status.
3. Make every price a number field, never free text like 「45만~90만 원」.
4. Before saving prices, show only what changed (「8,000원 → 80,000원」), and ask again when a number more than doubles.

## Before sending

Capture owner and staff screens at 390. Grid inputs overflow the phone unless grid children get `min-width: 0` and inputs `width: 100%`.
