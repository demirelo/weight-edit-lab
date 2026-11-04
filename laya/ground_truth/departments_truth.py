"""Ground truth: Banking77 intent -> department. Kept outside the lab so editors cannot reach it."""

INTENT_DEPT = {
    # cards
    "activate_my_card": "cards", "apple_pay_or_google_pay": "cards", "atm_support": "cards",
    "card_about_to_expire": "cards", "card_acceptance": "cards", "card_arrival": "cards",
    "card_delivery_estimate": "cards", "card_linking": "cards", "card_not_working": "cards",
    "card_swallowed": "cards", "change_pin": "cards", "compromised_card": "cards",
    "contactless_not_working": "cards", "disposable_card_limits": "cards",
    "get_disposable_virtual_card": "cards", "get_physical_card": "cards", "getting_spare_card": "cards",
    "getting_virtual_card": "cards", "lost_or_stolen_card": "cards", "order_physical_card": "cards",
    "pin_blocked": "cards", "supported_cards_and_currencies": "cards", "virtual_card_not_working": "cards",
    "visa_or_mastercard": "cards",
    # disputes
    "card_payment_not_recognised": "disputes", "cash_withdrawal_not_recognised": "disputes",
    "declined_card_payment": "disputes", "declined_cash_withdrawal": "disputes",
    "direct_debit_payment_not_recognised": "disputes", "pending_card_payment": "disputes",
    "pending_cash_withdrawal": "disputes", "Refund_not_showing_up": "disputes", "request_refund": "disputes",
    "reverted_card_payment?": "disputes", "transaction_charged_twice": "disputes",
    "wrong_amount_of_cash_received": "disputes",
    # transfers and top-ups
    "automatic_top_up": "transfers_topups", "balance_not_updated_after_bank_transfer": "transfers_topups",
    "balance_not_updated_after_cheque_or_cash_deposit": "transfers_topups",
    "beneficiary_not_allowed": "transfers_topups", "cancel_transfer": "transfers_topups",
    "declined_transfer": "transfers_topups", "failed_transfer": "transfers_topups",
    "pending_top_up": "transfers_topups", "pending_transfer": "transfers_topups",
    "receiving_money": "transfers_topups", "top_up_by_cash_or_cheque": "transfers_topups",
    "top_up_failed": "transfers_topups", "top_up_limits": "transfers_topups", "top_up_reverted": "transfers_topups",
    "topping_up_by_card": "transfers_topups", "transfer_into_account": "transfers_topups",
    "transfer_not_received_by_recipient": "transfers_topups", "transfer_timing": "transfers_topups",
    "verify_top_up": "transfers_topups",
    # fees and FX
    "card_payment_fee_charged": "fees_fx", "card_payment_wrong_exchange_rate": "fees_fx",
    "cash_withdrawal_charge": "fees_fx", "exchange_charge": "fees_fx", "exchange_rate": "fees_fx",
    "exchange_via_app": "fees_fx", "extra_charge_on_statement": "fees_fx", "fiat_currency_support": "fees_fx",
    "top_up_by_bank_transfer_charge": "fees_fx", "top_up_by_card_charge": "fees_fx",
    "transfer_fee_charged": "fees_fx", "wrong_exchange_rate_for_cash_withdrawal": "fees_fx",
    # account and security
    "age_limit": "account_security", "country_support": "account_security",
    "edit_personal_details": "account_security", "lost_or_stolen_phone": "account_security",
    "passcode_forgotten": "account_security", "terminate_account": "account_security",
    "unable_to_verify_identity": "account_security", "verify_my_identity": "account_security",
    "verify_source_of_funds": "account_security", "why_verify_identity": "account_security",
}
