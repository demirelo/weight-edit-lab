import re

# Step 1: complaints about a bad/wrong exchange rate on a card payment or
# cash withdrawal go to fees_fx, even when they read like a dispute.
_RATE = re.compile(r"\b(exchange|conversion|fx)\b|\brates?\b|\bconver(t|ted|sion)\b", re.I)
_WRONG = re.compile(
    r"\b(wrong|incorrect|bad|poor|terrible|awful|off|unfair|less|lower|"
    r"issue|problem|mistake|error|not right|didn'?t match|doesn'?t match)\b",
    re.I,
)

# Step 2: anything about a card PIN (change, unblock, reset, compromised)
# goes to cards, not account_security. Word boundary keeps "pinned" etc. out;
# "passcode" is the app login and stays in account_security.
_PIN = re.compile(r"\bpins?\b|\bpersonal identification number\b", re.I)


def route(text, laya_dept):
    t = text or ""
    if laya_dept == "disputes" and _RATE.search(t):
        return "fees_fx"
    # Cards can also catch "card payment + wrong rate"; require a complaint word.
    if laya_dept == "cards" and _RATE.search(t) and _WRONG.search(t):
        return "fees_fx"
    if laya_dept == "account_security" and _PIN.search(t):
        return "cards"
    return laya_dept
