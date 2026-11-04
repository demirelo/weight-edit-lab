# Step 3 patch: eligibility goes to account_security

## Rule
If Laya answers `cards` or `disputes`, and the message asks who may open or use
an account, the router returns `account_security`. Signals:
- age: "age limit/requirement", "how old", "be 18", "minimum age", teen, minor
- children plus an account word (open, account, sign up, get a ...)
- countries: "country/countries", "locations", "live in", "outside the UK",
  "all over the world", resident, "where ... available/operate/support"

## Guards (keep Laya's answer)
- The message is about delivery, card acceptance, ATMs, transfers, top-ups,
  currencies, fees, rates, a lost or stolen card, or a disputed payment.
- The message mentions a PIN (step 2 stays true).
- Laya answered `transfers_topups` or `fees_fx` ("which countries can I send
  money to", "which currencies do you support").

## Order
Step 1 (bad FX rate to fees_fx) runs first, then step 2 (PIN to cards), then step 3.

## Verification
Python runs needed approval, so I traced the 32 evidence rows by hand: 32/32.
No command produced this number. Run a check before you trust it.

## Known gaps
Bare country names ("Do you operate in Spain?") keep Laya's answer.
