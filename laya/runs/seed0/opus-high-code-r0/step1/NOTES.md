# Step 1: wrong exchange rate goes to fees_fx

## Rules in `router.py` (in order)
1. The message says "rate", "exchange" or "interbank" (typos included): `fees_fx`.
2. Laya said `disputes` and the amount is wrong or too high for a purchase, payment, withdrawal or foreign transaction: `fees_fx`.
3. Laya said `cards` or `disputes` and the message asks about fees or cost for cash abroad or in another currency: `fees_fx`.
4. Otherwise, the router keeps Laya's answer.

## Guards
Rules 2 and 3 do not apply if the message shows a real dispute:
- too little cash from the ATM
- unrecognised payment
- charged twice
- pending, declined or reverted payment
- refund, fraud or stolen card

## Earlier corrections
None.

## Verification
- I traced all 32 evidence rows and 19 hand-written probes by hand. All match.
- The harness did not let me run Python, so the code has not run yet.

## Known risk
"Charged the wrong amount of money for my withdrawal" stays in `disputes`.
