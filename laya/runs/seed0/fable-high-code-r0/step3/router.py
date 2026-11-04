import re

# Step 1 correction: complaints that a card payment or cash withdrawal used a
# bad or wrong exchange rate belong to fees_fx, not disputes.

# Explicit exchange / conversion / FX rate mention. Rates are a fees_fx topic by
# the department descriptions, whatever Laya answered.
_EXPLICIT_RATE_RE = re.compile(
    r"\b(exchange|conversion|fx|interbank|currency)\s+rates?\b"
    r"|\brates?\s+(of|for)\s+(exchange|conversion)\b",
    re.I,
)

# Bare "rate" next to a complaint word, e.g. "the wrong rate was applied",
# "the rate I got was terrible". Only trusted when Laya said disputes, where
# "rate" never means anything but the exchange rate.
_BAD = r"(wrong|bad|incorrect|poor|terrible|awful|unfair|off|too high|better|correct|right)"
_BAD_RATE_RE = re.compile(
    r"\b" + _BAD + r"\b[^.?!]{0,30}\brates?\b"
    r"|\brates?\b[^.?!]{0,40}\b" + _BAD + r"\b",
    re.I,
)

# "charged the wrong amount for an item": the exchange-rate complaint phrased
# without the word "rate". Evidence spells it "wing amount" (typo). ATM / cash
# "wrong amount" is a dispute (cash not dispensed), so those are excluded.
_WRONG_AMOUNT_RE = re.compile(
    r"\b(charged|billed|paid)\b[^.?!]{0,40}\b(wrong|wing|incorrect|wrng)\s+amount\b", re.I
)
_PURCHASE_RE = re.compile(r"\b(item|purchase|purchased|bought|buy|shop|store|product|paid)\b", re.I)
_CASH_RE = re.compile(r"\b(atm|cash|withdr\w*|twice|double|duplicate|fee|fees)\b", re.I)

# Cost of foreign cash / currency exchange that Laya filed under cards.
_FOREIGN_RE = re.compile(r"\b(currenc(y|ies)|exchange|foreign|abroad|overseas|atm|cash|withdr\w*)\b", re.I)
_COST_RE = re.compile(r"\b(cost|costs|fee|fees|charge|charges|charged|rate|rates|markup|mark-up)\b", re.I)
_CARD_SERVICE_RE = re.compile(r"\b(replace\w*|deliver\w*|order\w*|new card|activat\w*|pin)\b", re.I)

# Step 2 correction: anything about a card PIN (changing it, resetting it,
# a blocked PIN, too many wrong PIN tries) belongs to cards, not
# account_security. "PIN" only ever means the card PIN in this domain; the
# app passcode is called "passcode", so a bare word match is safe. Word
# boundaries keep "pinned" / "pinpoint" out.
_PIN_RE = re.compile(r"\bpins?\b", re.I)

# Step 3 correction: questions about who may open or use an account (age
# limits, supported countries, residency) belong to account_security, not
# cards. Laya files most of them under cards because the customer asks for
# "a card"; the real question is eligibility.

# Country / region / residency vocabulary. Lower-case "us" is a pronoun
# ("contact us"), so it only counts after a place preposition; the
# capitalised forms are matched case-sensitively below.
_PLACE_RE = re.compile(
    r"\bcountr(y|ies)\b|\bnationalit(y|ies)\b|\bcitizen\w*\b|\bresiden\w*\b"
    r"|\b(uk|u\.k\.|usa|u\.s\.a?\.?|eu|e\.u\.|united states|united kingdom|great britain|britain|england"
    r"|scotland|wales|ireland|europe|european|america|american|british|canada|australia|india"
    r"|france|germany|spain|italy|netherlands|poland|portugal|switzerland|singapore|japan|china"
    r"|brazil|mexico|africa|asia|middle east)\b"
    r"|\b(in|to|from|outside|within|of)\s+(the\s+)?us\b"
    r"|\b(live|lives|living|based|located|reside|residing|staying|stay)\s+(in|outside|abroad)\b"
    r"|\b(locations?|branch(es)?|offices?|regions?|territor\w*|cities)\b"
    r"|\b(available|availability|operate|operating|offered|offer|provide|provided|supported|support)\s+"
    r"(in|outside|anywhere|everywhere|where|internationally|globally|worldwide)\b"
    r"|\b(what|which|where)\b[^.?!]{0,30}\b(available|operate|supported|support|access)\b",
    re.I,
)
_PLACE_CS_RE = re.compile(r"\b(US|USA|UK|EU)\b")

# Age / minor vocabulary. "old" only in the age sense; "old card" stays cards.
_AGE_RE = re.compile(
    r"\bages?\b|\bhow old\b|\byears?[- ]old\b|\bold enough\b|\bminors?\b|\bchild(ren)?\b"
    r"|\bkids?\b|\bteen\w*\b|\bunderage\b|\bunder\s*(18|16|21)\b|\bsons?\b|\bdaughters?\b"
    r"|\badults?\b|\btoo young\b|\byoung(er)? (people|person|users?)\b",
    re.I,
)

# "Can I get support?" / "Do you support my area?": service coverage, not a
# help request. Excluded when the customer names a problem to get help with.
_SUPPORT_RE = re.compile(r"\b(get|have|receive|offer|provide|give)\s+support\b", re.I)

# Messages that mention a country but are really about a transaction, a
# transfer, a card service, currency or security details keep Laya's answer.
_ELIG_GUARD_RE = re.compile(
    r"\b(charg\w*|payment|payments|paid|transaction\w*|refund\w*|declin\w*|pending|withdr\w*"
    r"|revert\w*|twice|double|duplicate|dispute\w*|recogni[sz]e"
    r"|transfer\w*|sent|send|sending|receiv\w*|top[- ]?up\w*|topup\w*|deposit\w*|funds?|funding|balance|iban|swift"
    r"|deliver\w*|shipp\w*|ship|replace\w*|activat\w*|lost|stolen|contactless|apple pay|google pay"
    r"|virtual|disposable|expir\w*|block\w*|freez\w*|frozen|cancel\w*"
    r"|currenc\w*|exchange|fee|fees|rate|rates"
    r"|passcode|password|verif\w*|identity|id\b|document\w*|address|phone|number|email|name"
    r"|close|closing|closed)\b",
    re.I,
)


# "American Express" is a card brand, not a country.
_BRAND_RE = re.compile(r"\bamerican express\b|\bamex\b", re.I)


def _is_eligibility(t):
    t = _BRAND_RE.sub(" ", t)
    if _ELIG_GUARD_RE.search(t):
        return False
    return bool(
        _PLACE_RE.search(t)
        or _PLACE_CS_RE.search(t)
        or _AGE_RE.search(t)
        or _SUPPORT_RE.search(t)
    )


def route(text, laya_dept):
    t = text or ""
    # PIN beats everything except an explicit exchange-rate complaint
    # (step 1 correction stays true).
    if _PIN_RE.search(t) and not _EXPLICIT_RATE_RE.search(t):
        return "cards"
    if laya_dept == "fees_fx":
        return laya_dept
    if _EXPLICIT_RATE_RE.search(t):
        return "fees_fx"
    if laya_dept == "disputes":
        if _BAD_RATE_RE.search(t):
            return "fees_fx"
        if _WRONG_AMOUNT_RE.search(t) and _PURCHASE_RE.search(t) and not _CASH_RE.search(t):
            return "fees_fx"
    if laya_dept == "cards":
        if _FOREIGN_RE.search(t) and _COST_RE.search(t) and not _CARD_SERVICE_RE.search(t):
            return "fees_fx"
    # Step 3: eligibility questions. fees_fx was already returned above, so
    # "supported currencies" never reaches this rule.
    if laya_dept != "account_security" and _is_eligibility(t):
        return "account_security"
    return laya_dept
