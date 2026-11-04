import re

# Step 1 correction: complaints that a card payment, purchase or cash
# withdrawal used a bad or wrong exchange rate go to fees_fx, not disputes.

# Any explicit exchange-rate / conversion-rate talk. "rate" alone is kept out
# so that unrelated uses of the word do not fire.
_EXCHANGE_RATE = re.compile(
    r"\b(exchange|conversion|convertion|fx|forex|currency|interbank)\b[^.?!]{0,20}\brates?\b"
    r"|\brates?\b[^.?!]{0,25}\b(exchange|conversion|currency|currencies|interbank)\b",
    re.I,
)

# "the wrong rate was applied" style complaints that never say "exchange".
_BAD_RATE = re.compile(
    r"\b(wrong|bad|incorrect|unfair|poor|terrible|awful|off)\b[^.?!]{0,15}\brates?\b"
    r"|\brates?\b[^.?!]{0,25}\b(wrong|bad|incorrect|unfair|poor|terrible|awful|off)\b",
    re.I,
)

# "charged the wrong amount for an item / purchase" (card payment, not cash).
# Tolerates typos such as "wing amount" for "wrong amount".
_WRONG_AMOUNT_CHARGED = re.compile(
    r"\b(charged|charge|amount|price|cost)\b[^.?!]{0,30}\b(w[a-z]{1,3}ng|incorrect|not (?:the )?(?:right|correct))\b"
    r"|\b(w[a-z]{1,3}ng|incorrect)\s+amount\b",
    re.I,
)
_CASH_CONTEXT = re.compile(r"\b(cash|atm|withdr\w*|notes?|bills?)\b", re.I)
_PURCHASE_CONTEXT = re.compile(
    r"\b(item|purchas\w*|bought|buy|shop\w*|store|merchant|paid|pay\w*|card)\b", re.I
)

# Paying abroad and the amount came out higher than expected (bad rate).
_FOREIGN = re.compile(
    r"\b(abroad|overseas|foreign|another country|different country|other country|"
    r"different currency|another currency|other currency|foreign currency|in (?:euros?|dollars?|pounds?|usd|eur|gbp))\b",
    re.I,
)
_OVERCHARGED = re.compile(
    r"\b(charged|cost|amount|paid)\b[^.?!]{0,30}\b(more than|too much|higher|wrong|incorrect|different|off|expected)\b",
    re.I,
)

# Signals that this really is a dispute, not a rate complaint.
_DISPUTE_SIGNAL = re.compile(
    r"\b(twice|double|duplicate|declined|pending|revert\w*|refund\w*|"
    r"(?:don'?t|do not|did not|didn'?t|not) (?:recogni[sz]e|make|know|remember|authori[sz]e)|"
    r"unrecogni[sz]ed|unknown|fraud\w*|stolen|scam\w*)\b",
    re.I,
)

# ATM / cash withdrawal cost questions that Laya sent to cards.
_ATM_COST = re.compile(
    r"\b(cost|costs|fee|fees|charge|charges|charged|commission|surcharge)\b", re.I
)


# Step 2 correction: anything about a card PIN (changing it, resetting it,
# a blocked PIN, too many wrong PIN tries, where to unblock it) goes to
# cards, not account_security. Only the literal word "PIN" counts; the
# app "passcode" stays with account_security.
_PIN = re.compile(r"\bpins?\b", re.I)

# A PIN mention inside a genuine unrecognised-transaction complaint is still
# a dispute ("someone used my card and PIN, I don't recognise this payment").
_UNRECOGNISED = re.compile(
    r"\b(?:don'?t|do not|did not|didn'?t|never|not)\s+(?:recogni[sz]e|make|authori[sz]e)\b"
    r"|\bunrecogni[sz]ed\b|\bunauthori[sz]ed\b",
    re.I,
)


def _is_pin_query(text):
    if not _PIN.search(text):
        return False
    if _UNRECOGNISED.search(text):
        return False
    return True


# Step 3 correction: who may open or use an account (age limits, minors,
# which countries / residents are supported, where the service is available)
# goes to account_security, not cards.

# Age and minors.
_AGE = re.compile(
    r"\b(how old|age limits?|age requirements?|minimum age|what age|ages?|old enough|"
    r"years? old|minors?|under ?age|underage|under 1[0-9]|child(?:ren)?|kids?|"
    r"teen(?:ager)?s?)\b",
    re.I,
)

# Explicit country / residency / availability words. These fire on their own.
_COUNTRY = re.compile(
    r"\b(countr(?:y|ies)|nationalit(?:y|ies)|residen(?:t|ts|cy|tial)|citizen\w*|"
    r"eligib\w*|locations?|worldwide|internationally|international customers?|"
    r"outside (?:the |of )?(?:uk|eu|us|country)|not in the (?:uk|eu|us)|"
    r"(?:don'?t|do not) live in)\b",
    re.I,
)

# Named regions only count together with an availability / residency verb,
# so "card declined in Spain" style messages are left alone.
_REGION = re.compile(
    r"\b(uk|u\.k\.|united kingdom|britain|great britain|england|scotland|wales|"
    r"ireland|eu|e\.u\.|europe|european|eea|us|u\.s\.|usa|united states|america|"
    r"american|canada|canadian|australia|australian|india|indian|asia|africa|"
    r"germany|france|spain|italy|netherlands|poland|switzerland|norway|japan|china|"
    r"brazil|mexico|singapore|new zealand|south africa|nigeria|pakistan|turkey)\b",
    re.I,
)
_AVAILABILITY = re.compile(
    r"\b(get|got|obtain|open|opening|apply|applying|application|available|availability|"
    r"offer\w*|provide\w*|sign ?up|signing up|register\w*|live|lives|living|based|"
    r"located|support\w*|access|eligible|use|using|serve|operate\w*|work|works)\b",
    re.I,
)

# "Can I get support?" / "Do you offer this service?" style availability asks.
_SERVICE_AVAILABLE = re.compile(
    r"\b(get|have|access to|offer|provide|available)\b[^.?!]{0,12}\b(support|services?)\b",
    re.I,
)

# Context that means the message is really about something else.
_MONEY_MOVEMENT = re.compile(
    r"\b(send\w*|sent|transfer\w*|top[ -]?up\w*|topping up|receiv\w*|deposit\w*|"
    r"withdraw\w*|balance|payment|paid|pay|exchange|currenc\w*|fees?|charge\w*|"
    r"rates?|atm|cash)\b",
    re.I,
)
_OTHER_DEPT_WORDS = re.compile(
    r"\b(card|cards|pin|dispute\w*|refund\w*|deliver\w*|passcode|verif\w*|"
    r"identity|close|closing|phone)\b",
    re.I,
)
# Brand names that contain a region word.
_BRAND_NOISE = re.compile(r"\bamerican express\b|\bamex\b|\bbank of america\b", re.I)


def _is_eligibility_query(text):
    t = _BRAND_NOISE.sub(" ", text)
    if _DISPUTE_SIGNAL.search(t) or _UNRECOGNISED.search(t):
        return False
    if _MONEY_MOVEMENT.search(t):
        return False
    if _AGE.search(t):
        return True
    if _COUNTRY.search(t):
        return True
    if _REGION.search(t) and _AVAILABILITY.search(t):
        return True
    if _SERVICE_AVAILABLE.search(t) and not _OTHER_DEPT_WORDS.search(t):
        return True
    return False


def _is_rate_complaint(text):
    if _EXCHANGE_RATE.search(text):
        return True
    if _BAD_RATE.search(text):
        return True
    if _DISPUTE_SIGNAL.search(text):
        return False
    if _WRONG_AMOUNT_CHARGED.search(text) and not _CASH_CONTEXT.search(text):
        return True
    if _FOREIGN.search(text) and _OVERCHARGED.search(text):
        return True
    return False


def route(text, laya_dept):
    t = text or ""

    # Correction 1: bad / wrong exchange rate on a card payment or withdrawal.
    if _is_rate_complaint(t):
        return "fees_fx"

    # Correction 2: card PIN questions (change, reset, blocked, tries) -> cards.
    if _is_pin_query(t):
        return "cards"

    # Correction 3: who may open or use an account (age, country, residency,
    # service availability) -> account_security.
    if _is_eligibility_query(t):
        return "account_security"

    # Cost of getting cash at an ATM is a fee question, not a card question.
    if laya_dept == "cards" and _CASH_CONTEXT.search(t) and _ATM_COST.search(t):
        return "fees_fx"

    return laya_dept
