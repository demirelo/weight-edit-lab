# Step 1 notes

## Correction 1: wrong exchange rate on card payment or cash withdrawal -> fees_fx

`route()` changes Laya's answer to `fees_fx` only when all of these hold:

1. Laya said `disputes` (the observed error) or `cards` (a likely near miss).
2. The text names a rate: "rate", "exchange rate", "withdrawal rate", "conversion".
3. The text complains or asks about it: wrong, incorrect, bad, take issue, less
   than expected, why, how come, explain, figure out.
4. The text names a card payment, purchase, cash withdrawal, ATM or being abroad,
   or says "exchange rate" outright.
5. It is not about a transfer or top-up (unless it also names a withdrawal or purchase).

Every other message keeps Laya's answer. A "rate" term is required, so plain
disputes (declined, pending, reverted, charged twice, wrong amount of cash from
the ATM) stay in `disputes`.

## Verification

I could not run Python in this session (the command needed approval). I traced
all 32 evidence rows by hand: 16 corrections fire, 16 controls are unchanged.
Run `python3 -c` over `evidence.csv` to confirm before relying on it.

## Earlier corrections

None existed; nothing to keep.
