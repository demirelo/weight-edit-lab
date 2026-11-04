The override detects complaints about exchange or conversion rates. It also detects a complaint about a bare “rate” when the message mentions a card payment, purchase, ATM, or cash withdrawal.

The rule returns `fees_fx` for these complaints, including complaints about an unexpected amount. It preserves Laya's answer when no rule matches. It excludes explicit transfer-only complaints and negated complaint terms.

The implementation uses Python regular expressions and string operations. It uses no model, training, or message lookup table.

Validation: all 32 labelled evidence messages pass. Additional checks cover rate wording, amount complaints, ordinary disputes, negation, and transfer-only complaints. These checks do not establish hidden-test results.
