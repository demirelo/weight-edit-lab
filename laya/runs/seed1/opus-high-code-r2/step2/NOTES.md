# Step 2 notes: card PIN -> cards

## Change
`router.py` adds one rule after the step-1 rules:
if Laya says `account_security` and the text contains the word `PIN`
(`\bpins?\b`, or "personal identification number"), return `cards`.

## Why this shape
- All 16 errors in `evidence.csv` are PIN messages that Laya sent to
  `account_security`. No PIN message went to another department.
- The rule fires only on `account_security`, so a PIN message that Laya
  sends elsewhere (for example a fee to change a PIN, in `fees_fx`) keeps
  its answer.
- The word boundary keeps "pinned", "spin" and similar words out.
- "passcode" (app login) does not match, so it stays in `account_security`.
- Step-1 rules fire only on `disputes` or `cards`, so the two corrections
  do not overlap. Step-1 code is unchanged.

## Results
Command: `python -I check.py router.py evidence.csv` (venv Python).
- Patched: evidence 32/32; 8/8 extra cases (step-1 rate cases, passcode,
  "pinned", identity, PIN in `fees_fx`).
- Original router: evidence 16/32 (negative test, so the check catches the bug).

## Risk
A message that says "PIN" but is really about the app login would move to
`cards`. The evidence has no such case.
