# Step 3 notes

## Rule
A message is an eligibility question when none of the "not eligibility"
words appear (transfer, send, currency, rate, fee, delivery, declined,
Apple Pay, merchant, verify, lost, ...) and one of these holds:

- age words: "age", "how old", "years old", "be 18", "under 16", "teen", "young"
- child words (child, kids, son, daughter, minor) next to account, card,
  open, sign up, use, allowed
- "abroad" or "overseas" next to open, sign up, register, account
- a place word (country, nation, location, "live in", "outside the UK",
  a named country or continent, a capitalised place after in/to/from)
  plus an availability word (support, offer, available, operate, work in,
  open, sign up, get a card, use this, which, where are you, still)

Such a message goes to account_security from any department, except PIN
messages, which step 2 owns.

## Order in `route`
1. Step 2: account_security + PIN -> cards.
2. Step 3: eligibility -> account_security.
3. Step 1: disputes/cards + exchange-rate complaint -> fees_fx.
4. Otherwise Laya's answer.

## Checks
Hand-traced all 32 evidence rows (16 move, 16 stay) and 36 extra cases
(paraphrases, place names in delivery, transfer, FX and dispute messages,
step 1 and 2 regressions). Python could not be run in this session.
