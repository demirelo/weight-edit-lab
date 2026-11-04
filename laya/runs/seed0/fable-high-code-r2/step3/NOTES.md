# Step 3 notes: eligibility questions go to account_security

## What changed
`router.py` gets a third rule, `_is_eligibility_query`, checked after the
exchange-rate and PIN rules and before the ATM-cost rule. It returns
`account_security` when the message asks who may open or use an account:

- Age or minors: "how old", "age limit", "minor", "child", "kids", "teenager".
- Country or residency words: "country", "nationality", "resident", "citizen",
  "eligible", "locations", "worldwide", "not in the UK", "don't live in".
- A named region (UK, EU, US, Europe, Germany, ...) together with an
  availability verb (get, open, apply, available, live, support, use, ...).
- A bare service-availability ask ("Can I get support?") with no other
  department words in the message.

## Guards (keep Laya's answer)
- Dispute signals, unrecognised transactions.
- Money movement and cost words: send, transfer, top up, withdraw, balance,
  payment, exchange, currency, fee, rate, ATM, cash.
- Brand names with a region word ("American Express", "Bank of America") are
  removed before matching.

## Test
Command: `.venv/bin/python -I test_router.py <task dir>`
Result: 32/32 evidence rows correct, 20 extra sanity cases correct, and the
test fails when the new rule is disabled.
