# Step 3 notes: age and country eligibility

## What changed
`router.py` has a third rule. If Laya's answer is not account_security and the
message asks who may open or use an account, the answer becomes account_security.

- Age signals: "age", "how old", "be 18", "under 16", "I'm 15", teen, minor, young.
- Child signals: child, kids, son, daughter, but only together with account, open, use, card or similar words.
- Country signals: country, region, locations, "all over the world", "live in", "outside the UK", "I'm in the EU", "available in the US".

## Guard against false positives
The rule does not fire on card, payment or transfer problems: delivery, tracking,
waiting, lost, declined, charged, refund, fees, currency, rates, transfers, top-ups,
withdrawals, merchants, payments. So "how long to deliver my card to the US" stays cards.
A PIN message never fires this rule, so correction 2 stays true.

## Order
Correction 1 (rate complaints) runs first, then correction 2 (PIN), then this rule.

## Verification
Python execution needed approval in this session, so the code was not run.
A hand trace of all 32 evidence rows gives 32/32. Run `evidence.csv` to confirm.
