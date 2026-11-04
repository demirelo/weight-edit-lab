import re

# Step 1: a complaint that a card payment or cash withdrawal got a bad or
# wrong exchange rate is fees_fx, not disputes (even if "the amount looks wrong").
_RATE = re.compile(r"\b(exchange|conversion|currency|fx)\s+rates?\b|\brates?\b", re.I)
_COMPLAINT = re.compile(
    r"\b(wrong|incorrect|bad|poor|terrible|awful|unfair|mistaken?|error|off|"
    r"not\s+(right|correct|accurate|fair)|take\s+issue|issue\s+with|"
    r"(less|more|fewer)\b[^.?!]{0,30}\bthan\s+(i\s+)?(expected|anticipated|thought|should))\b"
    r"|\bisn'?t\s+(right|correct)|\bwasn'?t\s+(right|correct)|\bdidn'?t\s+get\s+the\s+right",
    re.I,
)
# Transfer / top-up rate complaints are out of scope for this correction.
_TRANSFER = re.compile(r"\b(transfer|top[\s-]?up|topping\s+up|sen[dt]|receiv\w*)\b", re.I)
_CARD_CASH = re.compile(
    r"\b(card|cash|atm|withdr[ae]w\w*|payment|paid|pay|bought|buy|purchase\w*|item|shop\w*)\b",
    re.I,
)


def _is_fx_rate_complaint(text):
    if not (_RATE.search(text) and _COMPLAINT.search(text)):
        return False
    if _TRANSFER.search(text) and not _CARD_CASH.search(text):
        return False
    return True


# Step 2: anything about a card PIN (change, reset, blocked, unblock) is cards,
# not account_security. "passcode" is the app login and stays account_security.
_PIN = re.compile(r"\bpins?\b|\bpin[\s-]?(number|code)s?\b", re.I)


def route(text, laya_dept):
    if laya_dept in ("disputes", "cards") and _is_fx_rate_complaint(text):
        return "fees_fx"
    if laya_dept == "account_security" and _PIN.search(text):
        return "cards"
    return laya_dept
