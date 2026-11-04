# Step 2 notes: card PIN correction

## Change
`router.py` adds one rule after correction 1:
if Laya answers `account_security` and the message contains the word "PIN"
(also "pins", "pincode", "pin-code", any case), the answer becomes `cards`.

## Why this scope
- The correction says PIN messages belong to cards "not account_security".
  All 16 wrong rows in `evidence.csv` are account_security -> cards.
- Other Laya answers stay. Example: "my payment was declined, my PIN was right"
  is a declined payment (disputes), not a PIN question.
- `\b` word bounds keep "spin", "pinned", "opinion" out.
- Passcode and identity messages without "PIN" stay in account_security.

## Earlier correction
Correction 1 (bad exchange rate -> fees_fx) runs first and is unchanged.
The two rules act on different Laya answers, so they cannot conflict.

## Check
All 32 evidence rows match, checked by hand against the regex.
This session could not run Python (approval needed), so no automated test ran.
Before you trust the result, score `route()` on `evidence.csv`.

## Risk
A message about the app passcode that calls it a "PIN" goes to cards.
