# Step 3 notes: account eligibility -> account_security

## Rule
`route()` checks the corrections in order: FX rate complaints (step 1), card
PIN (step 2), then eligibility (step 3). Eligibility overrides any Laya answer
except `fees_fx`, because the evidence shows misroutes from cards, disputes and
transfers_topups. `fees_fx` is kept so "supported currencies" stays there.

## Eligibility signals
- Age: "how old", "age", "minor", "under 18", or a child word (kids, son,
  teen) together with account / open / get a / have an.
- Countries: "what/which countries", "supported countries", "my/your country",
  "where are you located", "have locations", and the exact "Can I get support?".
- Place word (upper-case EU/UK/US, residents, live in, outside...) together with
  an eligibility phrase (can I, available, provide, support, is it possible).

## Guards
- Country checks skip fee, rate, currency, delivery, replacement, lost/stolen,
  top-up, transfer, ATM, decline, refund and PIN texts ("Which ATMs take the
  card?" stays cards).
- EU/UK/US match upper-case only, so the pronoun "us" does not trigger.
- A child word alone ("my son used my card") does not trigger.

## Check
Hand-traced on all 32 `evidence.csv` rows: 32/32. Python runs were blocked here,
so this is not machine-checked.
