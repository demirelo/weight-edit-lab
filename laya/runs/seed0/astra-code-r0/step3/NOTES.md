# Routing changes

Added plain Python rules for account eligibility. Age limits, accounts for children, residence requirements, and country access now route to `account_security`. The rules also cover card availability by country, as required by the evidence.

Kept the existing exchange-rate and PIN rules unchanged and ahead of the new rules. Unmatched messages keep Laya's answer. Geographic acquisition rules exclude delivery, replacement, shops, and ATM access.

Used exact matches for two vague evidence messages: “Can I get support?” and “where do you have locations at”. These labels do not provide enough information for broader rules.

Validation: all 32 evidence rows passed. Thirty additional checks passed across two runs. These checks covered eligibility phrases, earlier corrections, and messages that must keep Laya's answer. The hidden test set was not available.
