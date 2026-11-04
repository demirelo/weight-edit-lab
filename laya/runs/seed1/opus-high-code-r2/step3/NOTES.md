# Step 3 notes

## Change
`router.py` has a new rule. If Laya answers cards, disputes, transfers_topups
or fees_fx, and the message asks who may open or use an account, the final
answer is account_security. The rule detects:

- Age: "how old", "age limit", "minimum age", "be 18", "18+", minors, teens.
- Children plus account words: "account for my children", "card for my son".
- Countries: "which countries", "outside the UK", "live in the US",
  "resident of", "all over the world", "where ... locations".

## Guards
The rule does not fire if the message is about delivery, tracking, lost or
stolen cards, transfers, top-ups, fees, rates, currencies, ATMs, cash,
declines, refunds, payments or a PIN. Example: "express delivering my card
to the US" stays cards. Step 1 (rate complaints) and step 2 (PIN) rules run
first and do not change.

## Test
Command: `.venv/bin/python test_router.py <dir>` (in the session scratchpad).
Result: 121/121 pass (step 1-3 evidence, 32 rows each, plus 25 hand-written
cases).

## Risk
The hand-written cases are my guesses, not real data. Country questions about
using a card abroad can be ambiguous between cards and account_security.
