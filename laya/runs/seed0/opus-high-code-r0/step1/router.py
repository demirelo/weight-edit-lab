import re

# Step 1 correction: complaints that a card payment or cash withdrawal used a
# bad/wrong exchange rate are fees_fx, not disputes, even if the customer only
# says the amount looks wrong.

# Any mention of an exchange rate (typos included) is an FX question.
_RATE = re.compile(
    r"\b(rates?|interbank|exch\w*|exhange\w*|excange\w*|exchnage\w*|echange\w*)\b"
)

_WRONG = r"(wrong|wing|wromg|worng|wron|incorrect|inaccurate|bad|off|weird|not right|isn'?t right|error)"
_WRONG_AMOUNT = re.compile(
    r"\b" + _WRONG + r"\s+(amount|price|total|sum)\b"
    r"|\b(amount|price|total|sum)\b[^.?!]{0,40}\b(is|was|looks|seems|appears)\s+(" + _WRONG + r"|too high|higher)"
    r"|\b(amount|price|total|sum)\b[^.?!]{0,60}\b(wrong|incorrect|inaccurate|too high|higher than)\b"
    r"|\b(charged|debited|deducted|billed)\s+(me\s+)?(more|too much|extra)\b"
    r"|\bovercharged\b"
)

# Context that ties a wrong amount to a purchase or a withdrawal.
_PAYMENT = re.compile(
    r"\b(item|purchase\w*|bought|buy\w*|card payment|payment|paid|pay\w*|shop\w*|"
    r"store|restaurant|merchant|card|cash|withdr\w*|atm)\b"
)
_FOREIGN = re.compile(
    r"\b(abroad|overseas|foreign|currenc\w*|another country|other country|"
    r"different country|international\w*|travel\w*|holiday|vacation|trip)\b"
)

# Real dispute signals that must stay with disputes: cash not dispensed,
# unrecognised, duplicate, pending, declined, reverted, refunds.
_DISPUTE = re.compile(
    r"\b(only (got|received|gave)|didn'?t (get|receive|give|come out)|"
    r"did not (get|receive|give|come out)|never (got|received)|"
    r"wasn'?t (able|given)|was not (able|given)|less (cash|money) (than|out)|"
    r"(gave|give|given|dispensed?|received?|came out|spat out)\b[^.?!]{0,20}\b(wrong|incorrect) amount|"
    r"(got|get) (me )?(the |a )?(wrong|incorrect) amount|"
    r"(wrong|incorrect) amount of (cash|money|notes|bills)|"
    r"recogni[sz]\w*|didn'?t make|did not make|not authori[sz]\w*|"
    r"twice|double|duplicate|pending|declin\w*|revert\w*|refund\w*|"
    r"stolen|fraud\w*|someone else)\b"
)

# Asking about fees or rates for cash in another currency at an ATM.
_ATM_FX = re.compile(r"\b(atm|cash|withdr\w*)\b")
_COST = re.compile(r"\b(cost\w*|fees?|charg\w*|rates?|extra|additional)\b")


def route(text, laya_dept):
    t = text.lower().replace("’", "'")

    if _RATE.search(t):
        return "fees_fx"

    if laya_dept == "disputes" and not _DISPUTE.search(t):
        if _WRONG_AMOUNT.search(t) and (_PAYMENT.search(t) or _FOREIGN.search(t)):
            return "fees_fx"

    if laya_dept in ("cards", "disputes") and not _DISPUTE.search(t):
        if _FOREIGN.search(t) and _ATM_FX.search(t) and _COST.search(t):
            return "fees_fx"

    return laya_dept
