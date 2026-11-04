# Step 3 notes: eligibility (age, country) -> account_security

## Rule
`_eligibility(text)` fires when the message has an **age signal** (age, how old,
old enough, be 18, kids, children, teenager, minors) or a **country signal**.
A country signal is either a generic place word (countries, locations, regions,
worldwide, internationally, all over the world, outside the UK, "where are you
available") or a named country/region together with a residence or eligibility
word (live in, from, resident, outside, open an account, get a card, use this).

## Blockers
The rule stays silent when the message is really about something else that
mentions a place or a person: card delivery (deliver, express, track, arrive),
card acceptance (use/accept/work ... card), currencies and rates, money movement
(transfer, send, top up, deposit), a transaction (payment, purchase, refund,
charged), travel, or a spare/additional card. This keeps "express delivering my
card to the US" and "which merchants accept my card" with cards.

## Order
Rate complaint (step 1) -> PIN (step 2) -> eligibility (step 3) -> Laya.

## Check
`test_router.py` (scratchpad) runs the 32 evidence rows and 50 extra probes.
Result: 32/32 and 50/50 correct.
