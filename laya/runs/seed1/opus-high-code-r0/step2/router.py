import re

# Correction 1: complaints that a card payment or cash withdrawal used a bad or
# wrong exchange rate go to fees_fx, not disputes, even if the amount looks wrong.

# Any rate term: "exchange rate", "withdrawal rate", a bare "rate", "conversion".
_RATE = re.compile(r"\brates?\b|\bconver(?:sion|ted|t)\b", re.I)
_EXCHANGE_RATE = re.compile(r"\b(?:exchange|conversion)\s+rates?\b", re.I)

# The customer says the rate is off, or asks why / how it was worked out.
_COMPLAINT = re.compile(
    r"\b(?:wrong|incorrect|not\s+(?:right|correct)|bad|poor|terrible|awful|unfair"
    r"|off|mistake|error|issue|problem|less|more\s+than|lower|higher|worse"
    r"|expected|explain|why|how\s+come|figure\s+out|extremely)\b",
    re.I,
)

# Card payment, purchase, cash withdrawal or being abroad.
_CARD_OR_CASH = re.compile(
    r"\b(?:withdr\w*|atm|cash|card|pa(?:y|id|yment)s?|bought|buy|purchas\w*|item"
    r"|shop\w*|abroad|overseas|foreign|travel\w*|country|transaction|received)\b",
    re.I,
)
_WITHDRAWAL_OR_PURCHASE = re.compile(r"\b(?:withdr\w*|atm|cash|bought|purchas\w*)\b", re.I)

# Sending money or topping up is outside this correction.
_TRANSFER = re.compile(r"\b(?:transfer\w*|top(?:ping)?[\s-]?ups?|send\w*|sent)\b", re.I)


def _is_rate_complaint(text):
    if not (_RATE.search(text) and _COMPLAINT.search(text)):
        return False
    if _TRANSFER.search(text) and not _WITHDRAWAL_OR_PURCHASE.search(text):
        return False
    return bool(_CARD_OR_CASH.search(text) or _EXCHANGE_RATE.search(text))


# Correction 2: anything about a card PIN (changing it, blocked, forgotten,
# compromised) goes to cards, not account_security. Only the account_security
# answer is overridden, so a declined payment that mentions a PIN stays put.
# "PIN" also covers "pins", "pin number", "pincode"; \b keeps "spin", "pinned" out.
_PIN = re.compile(r"\bpin(?:s|code|-code)?\b", re.I)


def route(text, laya_dept):
    if laya_dept in ("disputes", "cards") and _is_rate_complaint(text):
        return "fees_fx"
    if laya_dept == "account_security" and _PIN.search(text):
        return "cards"
    return laya_dept
