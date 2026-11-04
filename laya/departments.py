"""Banking77 intents -> 5 support departments. This mapping is the ground truth."""

DEPARTMENTS = {
    "cards": "getting, activating, delivering, replacing or using a payment card; PIN, contactless, "
             "virtual and disposable cards, Apple Pay or Google Pay, lost or stolen cards",
    "disputes": "a payment, withdrawal or debit the customer does not recognise, was declined, is pending, "
                "was charged twice or reverted; refunds",
    "transfers_topups": "sending or receiving money, bank transfers, topping up the account, "
                        "balance not updated after a transfer or deposit",
    "fees_fx": "fees and charges, exchange rates, currency exchange, supported currencies",
    "account_security": "identity verification, passcode, personal details, closing the account, "
                        "lost phone, age or country eligibility",
}
