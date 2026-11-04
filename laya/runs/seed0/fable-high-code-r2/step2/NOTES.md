# Step 2 notes: card PIN -> cards

## Rule added
A message that contains the word "PIN" (or "pins") is routed to `cards`.
This covers changing, resetting, unblocking a PIN, wrong PIN tries, and an
account locked by PIN tries. It fires on any Laya answer, so the one evidence
row Laya sent to `disputes` is fixed too.

## Boundaries kept
- "passcode" is not matched. The app passcode stays with `account_security`.
- An unrecognised or unauthorised transaction that mentions a PIN stays a
  dispute ("someone used my card and PIN, I don't recognise this").
- Correction 1 (bad exchange rate -> `fees_fx`) runs first and is unchanged.
- The ATM cost rule from step 1 is unchanged.

## Order in `route`
1. Exchange-rate complaint -> `fees_fx`
2. PIN query -> `cards`
3. ATM cost with Laya = cards -> `fees_fx`
4. Otherwise Laya's answer

## Check
Ran all 32 evidence rows plus 9 guard cases (earlier correction, passcode,
identity, close account, dispute with PIN) with the lab venv Python.
Result: 32/32 evidence, 9/9 guards.
