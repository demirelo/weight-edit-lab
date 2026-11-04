import re

# Step 1: complaints that a card payment or cash withdrawal used a bad or wrong
# exchange rate go to fees_fx, even if the customer says the amount is wrong.
# Laya puts these in disputes (sometimes cards), so only those answers change.
_FX_FROM = {"disputes", "cards"}

# "exchange rate", "conversion rate", "rate applied", "wrong rate", "interbank rate".
_RATE = re.compile(
    r"\b(exchange|conversion|currency|interbank|fx)\s+rates?\b"
    r"|\brates?\b.{0,40}\b(wrong|incorrect|bad|off|applied|error)\b"
    r"|\b(wrong|incorrect|bad|poor|terrible|awful)\s+(exchange\s+)?rates?\b",
    re.I,
)

# "charged the wrong amount for an item" (also the typo "wing amount") on a
# purchase. Cash shortfalls at an ATM stay disputes, so cash words block this.
_WRONG_AMOUNT = re.compile(r"\b(wrong|wing|wron|incorrect)\s+amount\b", re.I)
_PURCHASE = re.compile(
    r"\b(item|bought|buy|purchas\w*|abroad|overseas|foreign|currency)\b", re.I
)
_CASH = re.compile(r"\b(atm|cash|withdr\w*|twice|double|refund)\b", re.I)

# Cash in a home or foreign currency at an ATM.
_ATM_CURRENCY = re.compile(
    r"\b(home|local|foreign|other|different)\s+currenc\w*\b.*\b(atm|cash|withdr\w*)\b"
    r"|\b(atm|cash|withdr\w*)\b.*\b(home|local|foreign|other|different)\s+currenc\w*\b",
    re.I,
)


def _is_fx_rate_complaint(text):
    if _RATE.search(text) or _ATM_CURRENCY.search(text):
        return True
    return bool(
        _WRONG_AMOUNT.search(text) and _PURCHASE.search(text) and not _CASH.search(text)
    )


# Step 2: anything about a card PIN (change, reset, blocked, too many tries)
# goes to cards. Laya sends these to account_security, sometimes disputes, so
# any answer is overridden. "passcode" (app login) stays account_security;
# \bpins?\b does not match it.
_PIN = re.compile(r"\bpins?\b|\bpersonal\s+identification\s+number\b", re.I)


def route(text, laya_dept):
    if laya_dept in _FX_FROM and _is_fx_rate_complaint(text):
        return "fees_fx"
    if _PIN.search(text):
        return "cards"
    return laya_dept
