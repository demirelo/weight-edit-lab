# Step 1 notes

## Correction
Complaints about a bad or wrong exchange rate on a card payment or cash
withdrawal go to fees_fx, not disputes.

## Rule in `router.py`
The override applies only when Laya answers `disputes` or `cards`. Then the
answer becomes `fees_fx` if the text has one of these:

1. An exchange-rate phrase: "exchange/conversion/interbank rate", "wrong/bad rate",
   or "rate ... wrong/incorrect/applied".
2. "wrong amount" (also the typo "wing amount") on a purchase ("item", "bought",
   "abroad"), with no cash, ATM, "twice" or refund words.
3. Cash at an ATM in a "home/local/foreign currency".

All other answers stay as Laya gave them.

## Guards against over-reach
- Wrong cash amounts at an ATM ("I only got 80") stay `disputes`.
- Pending, declined, double charges, refunds and unknown debits do not match.
- Answers of `transfers_topups` or `account_security` never change, because the
  correction covers card payments and cash only.

## Check
A hand trace gives 32 of 32 evidence rows correct. I could not run the scorer
script (`check.py`) because the Python command needed an approval that this
session did not get. Run it before you trust the number.

## Earlier corrections
None.
