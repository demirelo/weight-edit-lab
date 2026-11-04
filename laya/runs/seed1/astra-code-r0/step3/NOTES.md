# Routing update

The router now sends age, residence, and country eligibility questions to
`account_security`. It also covers questions about children's accounts,
provider locations, and worldwide service access.

The rules use regular expressions and string operations. They exclude card
delivery, merchant acceptance, explicit card use abroad, transfers, currencies,
and other transaction topics from country eligibility matching. Messages that
match no correction keep Laya's answer.

The existing PIN and exchange-rate rules remain unchanged. PIN questions take
priority over eligibility. Exchange-rate complaints retain their existing
priority over both rules.

Validation passed all 32 labelled evidence cases and 124 additional checks.
The additional checks cover eligibility variants, both earlier corrections,
rule priority, and unchanged answers across all five departments. The hidden
test set was not available. These rules depend on wording and can miss unseen
phrases.
