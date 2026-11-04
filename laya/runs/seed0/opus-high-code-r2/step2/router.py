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


def route(text, laya_dept):
    # Step 1 runs first so an exchange-rate complaint that mentions a PIN
    # still goes to fees_fx.
    if _is_fx_rate_complaint(text):
        return "fees_fx"
    if _is_card_pin(text, laya_dept):
        return "cards"
    return laya_dept
