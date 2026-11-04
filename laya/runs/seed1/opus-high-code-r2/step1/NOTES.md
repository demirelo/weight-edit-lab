# Step 1 notes

## Correction
Complaints about a bad or wrong exchange rate on a card payment or cash
withdrawal go to `fees_fx`, not `disputes`.

## Patch (`router.py`)
- If Laya says `disputes` and the text has an FX term (`exchange`,
  `conversion`, `convert`, `fx`, `rate`/`rates`), return `fees_fx`.
- If Laya says `cards`, the text has an FX term, and it also has a complaint
  word (`wrong`, `incorrect`, `bad`, `off`, `less`, ...), return `fees_fx`.
- In all other cases, return Laya's answer unchanged.

Earlier corrections: none existed, so nothing to keep.

## Checks
- `evidence.csv`: 32/32 correct (was 16/32 with the pass-through router).
- 14 hand-written probes (paraphrases plus disputes/cards/transfers
  negatives such as "charged twice", "pending", "declined", "wrong amount of
  cash"): 14/14 correct.

## Known risks
- A real dispute that also names an FX term (for example "I don't recognise
  this payment in euros at a strange rate") moves to `fees_fx`.
- FX complaints that use no FX word at all ("I got less cash than I
  expected abroad") stay with Laya's answer.
- Transfers with a wrong rate are out of scope and are not changed.
