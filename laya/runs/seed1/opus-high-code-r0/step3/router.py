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


# Correction 3: who may open or use an account (age limits, supported countries)
# goes to account_security, not cards.

# Age limits: "how old", "age limit", "be 18", "under 16", "I'm 15", "teenagers".
# Bare "age" only: "waiting for ages" is about a late card.
_AGE = re.compile(
    r"\bage\b|\baged\s+\d|\bhow\s+old\b|\byears?\s+old\b|\b1[0-9]\s*(?:\+|years?|yrs?|or\s+(?:older|over))"
    r"|\b(?:be|under|over|below|above|turn(?:ed)?|i[’']?m|i\s+am)\s+1[0-9]\b|\b(?:too\s+)?young\w*\b"
    r"|\bteen\w*|\bminors?\b|\bunder\s*age\b|\bunderage\b",
    re.I,
)

# Someone else's child, only an age question when they want an account or card.
_CHILD = re.compile(r"\b(?:child\w*|kids?|son|daughters?|sons)\b", re.I)
_SIGN_UP = re.compile(
    r"\b(?:accounts?|open\w*|sign\w*|register\w*|join\w*|use|using|service|app"
    r"|eligib\w*|allowed|card|have|get|apply\w*|create|make)\b",
    re.I,
)

# Supported countries: "which countries", "locations", "all over the world",
# "outside the UK", "I live in the US".
_PLACE = (
    r"(?:the\s+)?(?:uk|u\.k\.|us|u\.s\.|usa|eu|europe\w*|america\w*|united\s+(?:states|kingdom)"
    r"|britain|england|scotland|ireland|canada|mexico|brazil|china|india|japan|australia"
    r"|france|spain|germany|italy|portugal|netherlands|belgium|poland|switzerland"
    r"|another\s+country|my\s+country)"
)
_COUNTRY = re.compile(
    r"\bcountr(?:y|ies)\b|\bregions?\b|\blocations?\b|\bwhere\s+(?:are|do)\s+you\b"
    r"|\b(?:all\s+over|around)\s+the\s+world\b|\bworld\s*wide\b"
    r"|\b(?:live|living|reside|residing|resident|based|located|staying)\s+(?:in|outside|abroad)\b"
    # (?!\w), not \b, so "U.K." at the end of a sentence still matches.
    r"|\b(?:outside|not\s+(?:in|from))\s+" + _PLACE + r"(?!\w)"
    r"|\b(?:i[’']?m|i\s+am)\s+(?:in|from)\s+" + _PLACE + r"(?!\w)"
    r"|\b(?:available|operate|work|support\w*)\s+in\s+" + _PLACE + r"(?!\w)",
    re.I,
)

# Messages about a real card, payment or transfer problem keep Laya's answer,
# e.g. "how long to deliver my card to the US", "my card was declined abroad".
_NOT_ELIGIBILITY = re.compile(
    r"\b(?:deliver\w*|ship\w*|arriv\w*|track\w*|mail\w*|post(?:ed|al)?|express"
    r"|how\s+long|wait\w*|lost|stolen|missing|activat\w*|declin\w*|charg\w*|refund\w*|fees?"
    r"|currenc\w*|exchange|rates?|transfer\w*|send\w*|sent|top(?:ping)?[\s-]?ups?"
    r"|withdr\w*|atm|merchants?|shops?|accept\w*|transactions?|payments?)\b",
    re.I,
)


def _is_eligibility(text):
    if _NOT_ELIGIBILITY.search(text) or _PIN.search(text):
        return False
    if _AGE.search(text) or _COUNTRY.search(text):
        return True
    return bool(_CHILD.search(text) and _SIGN_UP.search(text))


def route(text, laya_dept):
    if laya_dept in ("disputes", "cards") and _is_rate_complaint(text):
        return "fees_fx"
    if laya_dept == "account_security" and _PIN.search(text):
        return "cards"
    if laya_dept != "account_security" and _is_eligibility(text):
        return "account_security"
    return laya_dept
