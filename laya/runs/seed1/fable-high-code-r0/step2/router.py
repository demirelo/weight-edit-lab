import re

# Step 1 correction: a complaint that a card payment or a cash withdrawal
# used a bad or wrong exchange rate is fees_fx, not disputes.

# Explicit mention of an exchange / conversion / FX rate.
_EXPLICIT_RATE = re.compile(
    r"\b(exchange|conversion|fx|forex|currency)[\s-]*rates?\b"
    r"|\brates? of exchange\b",
    re.I,
)

# "rate" used as a noun about the money, not as a verb ("I'd rate you 5 stars").
# Either a qualifier/owner sits right before it, or a verb/preposition right
# after it.
_NOUN_RATE = re.compile(
    r"\b(wrong|bad|incorrect|unfair|poor|terrible|awful|horrible|high|crazy|"
    r"ridiculous|different|weird|strange|odd|withdraw\w*|atm|cash|payment|"
    r"card|purchase|transaction|conversion|foreign|abroad|overseas|"
    r"the|this|that|my|your|a|an)\s+rates?\b"
    r"|\brates?\s+(is|was|were|applied|used|charged|seems?|looks?|on|for|at|of)\b",
    re.I,
)
# Bare "rate" only counts when the message is about a card payment,
# a purchase or a cash withdrawal, and the customer is unhappy or asking why.
_PAYMENT_CONTEXT = re.compile(
    r"\b(withdraw\w*|cash|atm|payment|paid|pay|bought|buy|purchase\w*|"
    r"spent|spend\w*|abroad|overseas|foreign|travel\w*|currency|"
    r"currencies|convert\w*|conversion|exchange\w*|card)\b",
    re.I,
)
_COMPLAINT = re.compile(
    r"\b(wrong|bad|incorrect|unfair|poor|terrible|awful|horrible|off|"
    r"too high|high|rip|robbed|cheated|overcharg\w*|less than|"
    r"issue|problem|complain\w*|not (right|correct)|don'?t (agree|understand)|"
    r"why|how come|explain)\b",
    re.I,
)
# Not exchange-rate talk: "top up rate" is a fee question, "interest rate" is
# a product question. Only the explicit pattern may override these.
_OTHER_RATE = re.compile(r"\b(top[\s-]*ups?|interest)\s+rates?\b", re.I)


def _is_exchange_rate_complaint(text):
    if _EXPLICIT_RATE.search(text):
        return True
    if _OTHER_RATE.search(text):
        return False
    return bool(
        _NOUN_RATE.search(text)
        and _PAYMENT_CONTEXT.search(text)
        and _COMPLAINT.search(text)
    )


# Step 2 correction: anything about a card PIN (changing it, a blocked or
# rejected PIN, a compromised PIN) is cards, not account_security.
#
# "PIN" as a whole word, in any case, with optional "number" or "code" after
# it. \b keeps "pinned", "pinpoint" and "spin" out. Written "P.I.N." counts too.
_PIN = re.compile(r"\bpins?\b|\bp\.i\.n\.?", re.I)


def _is_pin_message(text):
    return bool(_PIN.search(text))


def route(text, laya_dept):
    text = text or ""
    # Step 2: the correction only moves PIN messages away from
    # account_security. Other departments keep their own handling, e.g. a
    # declined card payment that mentions the PIN stays with disputes.
    if laya_dept == "account_security" and _is_pin_message(text):
        return "cards"
    # Step 1: only card payments and cash withdrawals are in scope, so only
    # the two departments Laya uses for those get overridden. Transfers keep
    # their own handling.
    if laya_dept in ("disputes", "cards") and _is_exchange_rate_complaint(text):
        return "fees_fx"
    return laya_dept
