# Step 2 notes: card PIN belongs to cards

## Rule added

One regex, `\bpins?\b` (case-insensitive), checked first in `route()`.
If the message mentions a PIN, the answer is `cards`, whatever Laya said.

The only exception keeps step 1 true: if the message also names an
explicit exchange / conversion / FX rate, the step-1 logic runs instead.

## Why a bare word match is safe

- In this domain "PIN" always means the card PIN. The app login is called
  "passcode", which stays with account_security.
- Word boundaries exclude "pinned", "pinpoint", "spin".
- The rule runs before the `fees_fx` early return and before the
  `disputes` branch, because the evidence shows Laya filing PIN messages
  under both account_security and disputes.

## Evidence check

All 17 PIN rows (account_security or disputes -> cards) match the regex.
The 15 non-PIN rows contain no "pin" word, so they pass through unchanged.
The one account_security row ("identity verification") stays put.

## Known limits

- A PIN message that also complains about an exchange rate goes to fees_fx.
- Misspellings such as "pim" or "p.i.n." are not caught.
