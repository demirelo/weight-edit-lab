# Step 1 notes: exchange-rate complaints go to fees_fx

## Rule

`route()` returns `fees_fx` when Laya says `disputes` or `cards` and the
message is an exchange-rate complaint. All other answers pass through.

A message is an exchange-rate complaint when either:

1. It names the rate explicitly: "exchange rate", "conversion rate",
   "FX rate", "currency rate", "rate of exchange". No complaint word needed,
   because a disputes-routed question about the exchange rate is fees_fx anyway.
2. It uses "rate" as a noun (qualifier or owner before it, or verb/preposition
   after it), plus a card-payment or cash-withdrawal context word
   (withdrawal, ATM, cash, payment, paid, bought, abroad, foreign, card...),
   plus a complaint word (wrong, bad, incorrect, why, how come, less than...).

"Top up rate" and "interest rate" never trigger path 2.

## Why the scope

The correction covers card payments and cash withdrawals, so only the two
departments Laya uses for those are overridden. A transfer with a bad rate
stays with transfers_topups.

## Checks

Python could not run in this session, so the regexes were checked with
ripgrep against evidence.csv and 15 hand-written edge cases. All 32 evidence
rows and all edge cases resolve correctly. Verb uses of "rate" do not fire.
