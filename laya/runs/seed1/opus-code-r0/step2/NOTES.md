# Step 2 notes: card PIN -> cards

## Change
`router.py` adds one rule after the step 1 rule:
if Laya answers `account_security` and the message names a PIN
(`pin`, `pins`, `pin number`, `pin code`, whole word, any case),
the final answer is `cards`.

## Why this scope
- The correction says PIN messages belong to cards, "not account_security".
  So the rule only changes `account_security` answers. All other Laya answers stay.
- Whole-word match, so "spin" and "pinned" do not fire.
- "passcode" is the app login. It stays `account_security`.

## Earlier corrections
- Step 1 (bad exchange rate on a card payment or cash withdrawal -> `fees_fx`)
  is unchanged and runs first. It only acts on `disputes` or `cards`
  answers, so the two rules cannot conflict.

## Check
- Evidence: 32/32 rows correct. I checked this by hand against each row,
  because the sandbox did not approve a Python run.
  To check by machine, loop over `evidence.csv` and compare
  `route(text, laya_answer)` with `correct`.

## Risk
- A PIN message that Laya sends to a department other than
  `account_security` is not changed.
