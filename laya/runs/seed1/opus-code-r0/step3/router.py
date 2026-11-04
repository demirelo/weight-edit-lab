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


# Step 3: who may open or use an account (age limits, children, supported
# countries, living abroad) is account_security, not cards.
_AGE = re.compile(
    r"\bage\s+(limit|requirement|restriction|minimum|range)s?\b|\bminimum\s+age\b|"
    r"\bage\s+(do|must|should)\b|\bhow\s+old\b|\b(be|over|under|turned?)\s+(1[0-9]|eighteen)\b|"
    r"\bunder\s?-?age\b|\btoo\s+young\b|\bteen(age(r|d)?)?s?\b|\bminors?\b",
    re.I,
)
_CHILD = re.compile(r"\b(child(ren)?|kids?|sons?|daughters?|teens?|minors?)\b", re.I)
_JOIN = re.compile(
    r"\b(open|opening|make|create|sign\w*\s+up|join|register|account|accounts|"
    r"use\s+(your|the|this)\s+(service|app)|get\s+(a|an|one)\b|eligib\w*|allowed)\b",
    re.I,
)
_COUNTRY = re.compile(
    r"\bcountr(y|ies)\b|\blocations?\b|\b(all\s+over|around)\s+the\s+world\b|\bworldwide\b|"
    r"\b(live|living|reside|residing|based|located|from)\s+(in|outside|abroad)\b|"
    r"\b(outside|out\s+of)\s+(of\s+)?(the\s+)?(uk|u\.k\.|united\s+kingdom|eu|europe|eea)\b|"
    r"\b(non|not\s+a)[\s-]?(uk|eu|eea)\s+(resident|citizen)s?\b|\bresiden(t|cy|ce)\b|"
    r"\bwhere\b[^.?!]{0,30}\b(available|operate|offer|support(ed)?)\b",
    re.I,
)
# Keep other departments' topics: delivery or acceptance of a card, sending
# money abroad, currencies or fees, a lost or stolen card, and disputed payments.
_NOT_ELIGIBILITY = re.compile(
    r"\b(deliver\w*|ship\w*|arriv\w*|track\w*|post(ed|age)?|mail(ed)?|courier|"
    r"accept\w*|merchants?|atms?|withdr[ae]w\w*|transfer\w*|send\w*|sent|receiv\w*|"
    r"top[\s-]?up\w*|topping|currenc(y|ies)|exchange|fees?|charge[sd]?|rates?|"
    r"lost|stolen|missing|declined|refund\w*|recogni[sz]\w*|pending|"
    r"payments?|transactions?|purchases?|bought|paid)\b",
    re.I,
)


def _is_eligibility(text):
    if _NOT_ELIGIBILITY.search(text):
        return False
    if _AGE.search(text) or _COUNTRY.search(text):
        return True
    return bool(_CHILD.search(text) and _JOIN.search(text))


def route(text, laya_dept):
    if laya_dept in ("disputes", "cards") and _is_fx_rate_complaint(text):
        return "fees_fx"
    if laya_dept == "account_security" and _PIN.search(text):
        return "cards"
    if laya_dept in ("cards", "disputes") and not _PIN.search(text) and _is_eligibility(text):
        return "account_security"
    return laya_dept
