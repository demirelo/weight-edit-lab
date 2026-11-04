# Step 1 notes

## Correction
Complaints that a card payment or cash withdrawal used a bad or wrong
exchange rate go to `fees_fx`, not `disputes`.

## Rule in `router.py`
Override to `fees_fx` only when all of these are true:

- Laya answered `disputes` or `cards`.
- The text names a rate (`exchange rate`, `rate`, `conversion rate`).
- The text has a complaint word: wrong, incorrect, bad, take issue,
  not right, or "less/more ... than expected".
- If the text names a transfer or a top-up, it also names a card, cash,
  ATM, withdrawal, payment or purchase. Transfer-only rate complaints
  stay with Laya.

All other messages keep Laya's answer.

## Evidence check (by hand)
- 16 of 16 rate complaints change from `disputes` to `fees_fx`.
- 16 of 16 other rows keep Laya's answer. None of them has the word "rate".
- I could not run Python here, so a scripted check is still open.

## Risks
- A message that has a real dispute (charged twice, unknown payment)
  and also a rate complaint goes to `fees_fx`.
- "rate" also matches unrelated rates (for example, interest rate)
  when the text also has a complaint word.
