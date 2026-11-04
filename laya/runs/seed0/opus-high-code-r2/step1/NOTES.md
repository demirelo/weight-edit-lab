# Step 1 notes

## Change
`router.py` now returns `fees_fx` for exchange-rate complaints. In all other cases it returns Laya's answer.

## Rules (any one triggers fees_fx)
1. "exchange rate" (typos such as "exhange" are allowed), "currency rate", "conversion rate" or "fx rate".
2. A bare "rate" together with a complaint word (wrong, incorrect, bad, error, correct, applied, interbank, and others).
3. "wrong amount" (or the typo "wing amount") for an item or a purchase.
4. ATM or cash, plus a currency, plus a cost, fee, charge or rate.

The rules apply whatever Laya answered. By the department descriptions, exchange rates always belong to fees_fx.

## Earlier corrections
None existed.

## Checks
- `evidence.csv`: 32/32 correct.
- 12 negative messages I wrote (double charge, wrong ATM cash amount, declined payment, top-up, and others): 12/12 keep Laya's answer.

## Risks
- Rule 3 can catch a real dispute such as "wrong amount for an item" when no currency is involved.
- Rule 4 can catch a cards question about using a card abroad.
