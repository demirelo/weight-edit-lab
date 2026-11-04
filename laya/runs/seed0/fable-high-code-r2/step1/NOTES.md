# Step 1 notes: wrong exchange rate -> fees_fx

`route()` now checks the message before it trusts Laya's answer.

## Rules added
1. **Exchange-rate talk** (`exchange|conversion|currency ... rate`, or `wrong|bad|incorrect ... rate`) -> `fees_fx`, whatever Laya said.
2. **Charged the wrong amount for an item or purchase** (typo-tolerant, e.g. "wing amount") -> `fees_fx`, unless the text is about cash or an ATM. "Got the wrong amount of cash" stays a dispute.
3. **Paid abroad or in a foreign currency and the charge was higher than expected** -> `fees_fx`.
4. **ATM or cash cost question that Laya sent to cards** -> `fees_fx`.

Rules 2 and 3 do not fire when the text has a dispute signal: charged twice, declined, pending, reverted, refund, not recognised, fraud.

## Result
Evidence: 32/32 correct (command: `python -I test_router.py <task dir>`). Extra probes kept disputes for "charged twice", "declined", "wrong amount of cash", "not recognised", and moved "charged more than expected abroad" and "terrible exchange rate" to fees_fx.

## Risk
A dispute phrased only as "the amount is wrong for an item" with no dispute signal moves to fees_fx. The correction says that is intended.
