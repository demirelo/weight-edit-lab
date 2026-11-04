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


def route(text, laya_dept):
    t = text or ""
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
    return laya_dept
