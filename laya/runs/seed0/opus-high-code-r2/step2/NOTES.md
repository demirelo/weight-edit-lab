# Step 2 notes

## Change
`router.py` sends card-PIN messages to `cards`. Otherwise it keeps the step 1 rule, then Laya's answer.

## Order
1. The step 1 exchange-rate rule runs first, so an exchange-rate complaint that mentions a PIN stays `fees_fx`.
2. The PIN rule runs second.

## PIN rule
- PIN word ("pin", "pin code", "pin number", "P.I.N.", "personal identification number") and Laya said `account_security`: `cards`.
- PIN word and Laya said `disputes`: `cards` only if the PIN is the problem (blocked, changed, reset, wrong, tries). "Payment without my PIN" stays a dispute.
- No PIN word, but "too many tries" or "all my attempts", Laya said `account_security`, no "passcode" or "password": `cards`.
- Other Laya answers stay.

## Checks
Command: `python t.py step2/router.py step2/evidence.csv step1/evidence.csv` (script in my scratchpad).
- Step 2 evidence: 32/32.
- Step 1 evidence: 32/32.
- 12 hand-written negatives (passcode, identity, lost phone, PIN with exchange rate): 12/12.

## Risks
- A PIN message that Laya sends to `transfers_topups` or `fees_fx` does not move.
- "Too many tries" without "PIN" can catch an unnamed passcode lockout.
