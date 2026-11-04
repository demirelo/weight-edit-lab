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


def route(text, laya_dept):
    if _is_fx_rate_complaint(text):
        return "fees_fx"
    return laya_dept
