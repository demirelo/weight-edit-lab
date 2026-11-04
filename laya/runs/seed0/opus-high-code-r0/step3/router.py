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


# Step 2 correction: anything about a card PIN (changing it, blocked PIN,
# too many tries) is cards, not account_security. "Passcode" is the app
# login and stays with account_security.
_PIN = re.compile(r"\b(pins?|pin[- ]?(code|number)s?|pincodes?)\b")


# Step 3 correction: who may open or use an account (age limits, which
# countries are supported) is account_security, not cards.
_AGE = re.compile(
    r"\b(how old|age|minimum age|age (limit|requirement|restriction)s?|"
    r"under ?(18|age)|underage|minors?|teen\w*|juniors?|young\w*|"
    r"(1[0-9]|eighteen|seventeen|sixteen|fifteen|fourteen|thirteen|twelve)"
    r"[- ]?(years?|yrs?|y/?o)\b( old)?|years old|"
    r"(i'?m|i am) (only )?(1[0-7]|seventeen|sixteen|fifteen|fourteen|thirteen))\b"
)
# Children only count when the message asks whether they can have or open
# something, so "my son used my card" keeps Laya's answer.
_KIDS = re.compile(r"\b(kids?|child\w*|son|daughter|teens?)\b")
_KIDS_ACCESS = re.compile(
    r"\b(open|get|have|set up|setup|sign\w* up|join|create|register|apply|"
    r"eligible|allowed|account\w*|requirements?)\b"
)
_COUNTRY = re.compile(
    r"\b(countr\w*|resident\w*|residen\w*|nationalit\w*|citizen\w*|"
    r"locations?|located|regions?|"
    r"(lives?|living|reside|based|stay\w*)\s+(in|outside|abroad|overseas)|"
    r"(outside|not in|out of)\s+(of\s+)?(the\s+)?(uk|u\.k\.|united kingdom|eu|europe)|"
    r"in the (us|usa|u\.s\.?|eu|eea|states)|united states|america|"
    r"europe\w*|eu|eea|non[- ]?(uk|eu)|"
    r"where (are|is) (you|this|it|your)\w*|where do you (have|operate|work)|"
    r"which places|what places|"
    r"can i get support)\b"
)
# Things that are about a card, a transfer or a dispute even when a country
# is named: delivery, a lost card, ATMs, sending money, top-ups.
_NOT_ELIGIBILITY = re.compile(
    r"\b(deliver\w*|arriv\w*|ship\w*|mail\w*|post(ed|age)?|track\w*|"
    r"lost|stolen|expir\w*|atms?|send\w*|sent|transfer\w*|top[- ]?up\w*|"
    r"deposit\w*|currenc\w*|fees?|charg\w*|cost\w*)\b"
)


def route(text, laya_dept):
    t = text.lower().replace("’", "'")

    if _RATE.search(t):
        return "fees_fx"

    # A PIN message Laya sent to disputes stays there only when it carries a
    # real dispute signal (declined, unrecognised, ...).
    if _PIN.search(t) and laya_dept != "cards":
        if laya_dept != "disputes" or not _DISPUTE.search(t):
            return "cards"

    if laya_dept == "disputes" and not _DISPUTE.search(t):
        if _WRONG_AMOUNT.search(t) and (_PAYMENT.search(t) or _FOREIGN.search(t)):
            return "fees_fx"

    if laya_dept in ("cards", "disputes") and not _DISPUTE.search(t):
        if _FOREIGN.search(t) and _ATM_FX.search(t) and _COST.search(t):
            return "fees_fx"

    # Runs last so the step 1 FX rules win when a country is named
    # ("the price was wrong when I paid in Europe").
    if laya_dept in ("cards", "disputes", "transfers_topups") and not _DISPUTE.search(t):
        if _AGE.search(t) or (_KIDS.search(t) and _KIDS_ACCESS.search(t)):
            if not re.search(r"\b(lost|stolen|send\w*|sent|transfer\w*|top[- ]?up\w*)\b", t):
                return "account_security"
        if _COUNTRY.search(t) and not _NOT_ELIGIBILITY.search(t):
            return "account_security"

    return laya_dept
