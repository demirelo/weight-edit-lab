# Patch task (step 2 of 3): write a code override, not weights

Laya routes customer messages to one of 5 departments: cards, disputes, transfers_topups, fees_fx, account_security.
`router.py` holds the current routing patch: `route(text, laya_dept) -> dept`.
It receives the message and Laya's current answer and returns the final answer.

## Department descriptions given to the model
- cards: getting, activating, delivering, replacing or using a payment card; PIN, contactless, virtual and disposable cards, Apple Pay or Google Pay, lost or stolen cards
- disputes: a payment, withdrawal or debit the customer does not recognise, was declined, is pending, was charged twice or reverted; refunds
- transfers_topups: sending or receiving money, bank transfers, topping up the account, balance not updated after a transfer or deposit
- fees_fx: fees and charges, exchange rates, currency exchange, supported currencies
- account_security: identity verification, passcode, personal details, closing the account, lost phone, age or country eligibility

## Corrections already applied in earlier steps (must stay true)
1. Complaints that a card payment or a cash withdrawal used a bad or wrong exchange rate belong to fees_fx, not disputes, even when the customer says the amount looks wrong.

## New correction for this step
Anything about a card PIN, such as changing the PIN or a PIN that is blocked, belongs to cards, not account_security.

`evidence.csv` has 32 labelled messages for this correction (text, Laya's
current answer, correct department).

Edit `router.py` so the final answers follow the new correction for all such
messages, keep earlier corrections, and otherwise keep Laya's answer. Plain Python
only (re, string ops); no ML libraries, no training. A hidden test set scores it.
Write `NOTES.md` (under 200 words).
