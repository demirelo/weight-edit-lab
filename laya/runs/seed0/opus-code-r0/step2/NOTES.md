# Step 2 notes: card PIN goes to cards

## Change
`router.py` adds `_PIN` (`\bpins?\b` or "personal identification number",
case-insensitive). If a message matches, `route` returns `cards`.

## Order
1. Step 1 FX rule (bad or wrong exchange rate on a card payment or cash
   withdrawal goes to `fees_fx`). It runs first, so it stays true.
2. Step 2 PIN rule. It overrides any Laya answer, not only
   `account_security`, because the evidence has one PIN message that Laya
   sent to `disputes`.
3. Otherwise, keep Laya's answer.

## Boundaries
- "passcode" (app login) does not match `\bpins?\b`, so it stays
  `account_security`. The same is true for words such as "spinning".
- Lost phone, identity checks and personal details have no PIN word, so
  they stay unchanged.

## Evidence check
32 rows (one blank line ignored). 17 rows contain a PIN word (Grep count,
`\bpins?\b`, case-insensitive). All 17 have the correct answer `cards`.
The other 15 rows have Laya's answer equal to the correct answer, and
none of them match the FX rule. Result by inspection: 32/32.

Not run: Python execution needed approval in this session, so the
scratchpad test script (`check.py`) was not run.
