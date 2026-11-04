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


# Step 3: who may open or use an account (age limits, supported countries)
# goes to account_security. Laya mostly says cards, sometimes disputes or
# transfers_topups, so any answer is overridden when the signal is clear.

# Age: "how old", "age limit", "minor", or a child word next to opening or
# having an account. "My son used my card" has no such verb, so it stays.
_AGE = re.compile(
    r"\bhow\s+old\b|\bage\b|\bminors?\b|\bunder\s*-?\s*age\b|\bunder\s+1\d\b"
    r"|\b1\d\s*(years?|yrs?)\s*old\b",
    re.I,
)
_CHILD = re.compile(r"\b(child|children|kids?|son|daughter|teens?|teenagers?)\b", re.I)
_CHILD_ELIGIBLE = re.compile(
    r"\b(accounts?|open|sign\s*up|join|register|eligib\w*|allowed|requirements?)\b"
    r"|\b(get|have)\s+(a|an|one|their\s+own)\b",
    re.I,
)

# Countries: "what/which countries", "supported countries", "where do you have
# locations", or a place word (EU, UK, US, residents, live in...) together with
# an eligibility verb (can I get, available, provide, support...).
_COUNTRY_STRONG = re.compile(
    r"\b(what|which)\s+countr(y|ies)\b|\bcountries\b.{0,30}\b(support|access|available|serve|operate)\w*"
    r"|\bsupported\s+countr(y|ies)\b|\b(my|your)\s+country\b"
    r"|\bwhere\s+(do|are)\s+you\b.{0,30}\b(locat\w*|operat\w*|availab\w*|based|support\w*)"
    r"|\b(have|your)\s+locations?\b|^\s*can\s+i\s+get\s+support\s*\??\s*$",
    re.I,
)
# Upper-case only, so the pronoun "us" does not match.
_PLACE_ABBR = re.compile(r"\b(EU|UK|US|USA|EEA)\b")
_PLACE = re.compile(
    r"\b(europe\w*|united\s+states|united\s+kingdom|residen(ts?|ce|cy)|citizens?\w*"
    r"|nationalit\w*|non-?resident\w*|live\s+in|living\s+in|not\s+in\s+the|outside|countr(y|ies))\b",
    re.I,
)
_ELIGIBLE = re.compile(
    r"\b(can|could|may)\s+(i|we|one|someone|people|a\s+person|my)\b|\bavailab\w*|\bprovide\w*"
    r"|\bsupport\w*|\baccess\b|\beligib\w*|\ballowed\b|\boffer\w*|\bopen\b|\bsign\s*up\b"
    r"|\bget\s+(a|an|one|your)\b|\brequirements?\b|\bis\s+it\s+possible\b",
    re.I,
)
# Card fees, delivery, replacement, transfers and cash questions that mention a
# country stay with Laya's answer.
_COUNTRY_BLOCK = re.compile(
    r"\b(fees?|charg\w*|rates?|exchange|currenc\w*|deliver\w*|arriv\w*|ship\w*|replac\w*"
    r"|lost|stolen|top\s*-?\s*up\w*|transfer\w*|withdr\w*|atms?|declin\w*|refund\w*|pin)\b",
    re.I,
)


def _is_eligibility_question(text):
    if _AGE.search(text):
        return True
    if _CHILD.search(text) and _CHILD_ELIGIBLE.search(text):
        return True
    if _COUNTRY_BLOCK.search(text):
        return False
    if _COUNTRY_STRONG.search(text):
        return True
    return bool(
        (_PLACE_ABBR.search(text) or _PLACE.search(text)) and _ELIGIBLE.search(text)
    )


def route(text, laya_dept):
    if laya_dept in _FX_FROM and _is_fx_rate_complaint(text):
        return "fees_fx"
    if _PIN.search(text):
        return "cards"
    if laya_dept != "fees_fx" and _is_eligibility_question(text):
        return "account_security"
    return laya_dept
