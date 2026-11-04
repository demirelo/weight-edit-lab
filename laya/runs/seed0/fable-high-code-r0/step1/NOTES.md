# Step 1 notes: wrong exchange rate -> fees_fx

## Rule
`route()` returns `fees_fx` when:

1. The text names an exchange, conversion, FX, interbank or currency rate, whatever Laya answered (except it already said fees_fx).
2. Laya said `disputes` and a bare "rate" sits near a complaint word (wrong, bad, incorrect, off, correct, better).
3. Laya said `disputes` and the customer was "charged the wrong amount" for an item or purchase, with no ATM, cash, withdrawal, double-charge or fee words. The typo "wing amount" from the evidence is accepted.
4. Laya said `cards` and the text asks what foreign cash or currency will cost, with no card-service words (replace, deliver, PIN).

Everything else keeps Laya's answer.

## Why these limits
- "Wrong amount" at an ATM is a dispute (cash not dispensed), so rule 3 excludes cash context.
- Pending, declined, duplicate, unrecognised and refund messages contain no rate word, so they stay in disputes.
- Rule 2 is disputes-only because "rate" is unambiguous there.

## Check
Traced all 32 evidence rows by hand: 32/32 match. Python execution was blocked in this sandbox, so no automated run.
