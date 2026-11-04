# Step 2 notes: card PIN messages go to cards

## Rule

`route()` returns `cards` when Laya says `account_security` and the message
mentions a PIN. The step 1 exchange-rate rule is unchanged and runs after it.

A message mentions a PIN when it contains "PIN" or "PINs" as a whole word, in
any case, or the written form "P.I.N.". Word boundaries keep "pinned",
"pinpoint" and "spin" out. "Passcode" is not a PIN and stays with
account_security.

## Why the scope

The correction moves PIN messages away from account_security only, so no
other department is overridden. A declined card payment that mentions the
PIN stays with disputes. A fee question about a PIN change stays with
fees_fx.

The two rules never collide: step 2 touches account_security answers, step 1
touches disputes and cards answers.

## Checks

Python could not run in this session, so the regex was checked with ripgrep.
All 16 evidence rows labelled account_security -> cards match. None of the
account_security rows that stay match. No step 1 evidence row matches, so
that correction is unaffected. Ten hand-written edge cases (PIN code, PIN
number, P.I.N., PIN-code, pinned, pinpoint, passcode, spinning) resolve
correctly.
