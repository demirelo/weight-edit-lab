import re

# Step 1: complaints about the exchange rate on a card payment or cash
# withdrawal go to fees_fx, even when they say the amount looks wrong.
# "ex\w*" tolerates typos such as "exhange" or "exchnage".
_FX_RATE = re.compile(
    r"\b(ex\w*|currency|conversion|fx|forex)\s+rates?\b", re.I)
_BARE_RATE = re.compile(r"\brates?\b", re.I)
_RATE_COMPLAINT = re.compile(
    r"\b(wrong|incorrect|bad|error|mistake|correct|inaccurate|poor|unfair|"
    r"terrible|awful|off|applied|interbank|higher|lower|worse)\b", re.I)
# Exchange-rate complaints with the word "rate" missing: "charged the
# wrong amount for an item" (also the "wing amount" typo seen in the data).
_WRONG_ITEM_AMOUNT = re.compile(
    r"\b(wrong|wing|incorrect)\s+amount\b.*\b(item|purchase|product|"
    r"bought|thing)\b", re.I)
# Getting cash in another currency at an ATM and asking about the cost.
_ATM_CURRENCY_COST = re.compile(
    r"(?=.*\b(atm|withdraw\w*|cash)\b)(?=.*\bcurrenc\w*\b)"
    r"(?=.*\b(cost|fee|fees|charge\w*|rate)\b)", re.I | re.S)


def _is_fx_rate_complaint(text):
    if _FX_RATE.search(text):
        return True
    if _BARE_RATE.search(text) and _RATE_COMPLAINT.search(text):
        return True
    if _WRONG_ITEM_AMOUNT.search(text):
        return True
    return bool(_ATM_CURRENCY_COST.search(text))



# Step 2: anything about a card PIN (change, reset, blocked, tries) goes to
# cards, not account_security. Passcodes and passwords stay with
# account_security.
_PIN = re.compile(
    r"\b(pins?|pin-?codes?|pin-?numbers?|p\.i\.n\.?|"
    r"personal identification numbers?)(?![\w-])", re.I)
_PASSCODE = re.compile(r"\b(pass\s?codes?|pass\s?words?)\b", re.I)
# PIN lockout described without the word "PIN": "used all my tries".
_TRIES = re.compile(
    r"\b(too many|all (of )?(my|the))\s+(\w+\s+)?(tries|attempts)\b", re.I)
# A PIN mention alone is not enough to move a disputes answer: "a payment
# was made without my PIN" is still a dispute. Move it only when the PIN
# itself is the problem.
_PIN_PROBLEM = re.compile(
    r"\b(block\w*|unblock\w*|lock\w*|unlock\w*|chang\w*|reset\w*|"
    r"forg[eo]t\w*|tries|attempts|wrong|incorrect|new|receiv\w*|"
    r"get|set)\b", re.I)


def _is_card_pin(text, laya_dept):
    if laya_dept not in ("account_security", "disputes"):
        return False
    if _PIN.search(text):
        return laya_dept == "account_security" or bool(
            _PIN_PROBLEM.search(text))
    return (laya_dept == "account_security" and bool(_TRIES.search(text))
            and not _PASSCODE.search(text))


# Step 3: who may open or use an account (age limits, supported countries)
# goes to account_security. Laya also sends a few of these to disputes or
# transfers_topups, so the rule is not limited to a cards answer.
_AGE = re.compile(
    r"\b(how old|old enough|age (limit|limits|requirement\w*|restriction\w*)|"
    r"(minimum|min|maximum|max|legal|required) age|underage|under-age|"
    r"under (the age of )?1[0-9]|\d{1,2}\s*(years? old|yo|yrs? old)|"
    r"what age|age to|i'?m \d{1,2}|i am \d{1,2})\b", re.I)
_MINOR = re.compile(
    r"\b(kids?|child|children|minors?|teens?|teenagers?|son|daughter|"
    r"juniors?|youngsters?)\b", re.I)
_GET_ACCOUNT = re.compile(
    r"\b(get|open|opening|have|set up|setup|create|make|sign up|apply|"
    r"register|join|use|requirements?)\b.*\b(accounts?|cards?|app|service)\b"
    r"|\baccounts? for\b", re.I | re.S)
_COUNTRY = re.compile(
    r"\b(countr\w*|nations?|nationalit\w*|locations?|located|operate\w*|"
    r"residents?|resident|reside\w*|live in|living in|outside (of )?the|"
    r"europe\w*|united states|america(?!n express)\w*|united kingdom|britain|england|"
    r"canada|australia|china|india|spain|france|germany|italy)\b", re.I)
# Case-sensitive so the pronoun "us" is not read as the country.
_COUNTRY_ABBR = re.compile(r"\b(US|USA|U\.S\.?|UK|EU|EEA)\b")
_AVAILABLE = re.compile(
    r"\b(get|open|have|available|availability|support\w*|access|use|"
    r"offer\w*|provide\w*|apply|sign up|serv\w*|do business|work|operat\w*|where)\b",
    re.I)
_GET_SUPPORT = re.compile(r"^\W*can i get support\W*$", re.I)
# Topics that keep Laya's answer: delivery, money movement, fees and
# currencies, and complaints about a transaction.
_NOT_ELIGIBILITY = re.compile(
    r"\b(deliver\w*|ship\w*|arriv\w*|send\w*|sent|transfer\w*|top.?up\w*|"
    r"fees?|charg\w*|cost\w*|currenc\w*|exchange|rates?|atms?|withdr\w*|"
    r"payments?|paid|transactions?|purchases?|refund\w*|declin\w*|"
    r"pending|recogni[sz]\w*|twice)\b", re.I)


def _is_eligibility(text, laya_dept):
    if laya_dept in ("account_security", "fees_fx"):
        return False
    if _GET_SUPPORT.search(text):
        return True
    if _NOT_ELIGIBILITY.search(text):
        return False
    if _AGE.search(text):
        return True
    if _MINOR.search(text) and _GET_ACCOUNT.search(text):
        return True
    return bool((_COUNTRY.search(text) or _COUNTRY_ABBR.search(text))
                and _AVAILABLE.search(text))


def route(text, laya_dept):
    # Step 1 runs first so an exchange-rate complaint that mentions a PIN
    # still goes to fees_fx.
    if _is_fx_rate_complaint(text):
        return "fees_fx"
    if _is_card_pin(text, laya_dept):
        return "cards"
    if _is_eligibility(text, laya_dept):
        return "account_security"
    return laya_dept
