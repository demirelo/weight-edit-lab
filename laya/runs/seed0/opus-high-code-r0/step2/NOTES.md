# Step 2 patch: card PIN goes to cards

## Rule
If the message mentions a PIN (`pin`, `pins`, `pin code`, `pin number`,
`pincode`, whole words only, so "spin" does not match) and Laya did not
answer `cards`, the final answer is `cards`.

## Order of checks in `route()`
1. Step 1 exchange-rate rule (`fees_fx`) runs first, unchanged.
2. New PIN rule.
3. Other step 1 rules, then Laya's answer.

## Guard for real disputes
If Laya said `disputes` and the message has a real dispute signal from the
step 1 list (declined, unrecognised, someone else, fraud, twice, pending,
refund), the answer stays `disputes`. Example: "My payment was declined after
I entered my PIN."

## Not changed
- "Passcode" (app login) stays with `account_security`. The new rule only
  matches the word PIN.
- Messages Laya already sends to `cards` are not touched.

## Verification
I traced all 32 evidence rows by hand against the code: all 32 match the
`correct` column. I could not run Python in this session, because the
permission was not granted. To confirm, run the check script (it scores
the evidence and 10 probe messages, including step 1 rate cases):

    python3 <scratchpad>/check.py <this folder>
