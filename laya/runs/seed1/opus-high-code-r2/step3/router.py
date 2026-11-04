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

# Step 3: who may open or use an account (age limits, supported countries)
# goes to account_security. Laya mostly files these under cards ("can I get a
# card if I live in the US?"), sometimes disputes.
_AGE = re.compile(
    r"\bhow old\b|\bage (limit|limits|requirement|requirements|restriction|"
    r"restrictions|minimum|range)\b|\bminimum age\b|\bwhat age\b|\bages?\b.{0,20}\b(open|account|use|join|sign)|"
    r"\b(be|turn|turned|am|i'?m|under|over|aged?) (1[0-9]|2[01])\b|"
    r"\b(1[0-9]|2[01]) (years|yrs|or older|and over|and older)\b|\b(1[0-9]|2[01]) ?\+|"
    r"\b(underage|under-age|minors?|teens?|teenagers?|adolescents?)\b",
    re.I,
)
_CHILD = re.compile(r"\b(child|children|childs|kids?|son|daughter|teen|teenager)'?s?\b", re.I)
_CHILD_ELIG = re.compile(
    r"\b(open|opening|account|accounts|sign (them |him |her )?up|join|register|"
    r"use (your|the|this) (service|app)|eligible|allowed|old|age)\b|\bfor (my|our)\b",
    re.I,
)
_COUNTRY = re.compile(
    r"\bcountr(y|ies)\b|\b(outside|out of) (of )?(the )?(uk|u\.k\.|eu|eea|europe|united kingdom)\b|"
    r"\b(live|living|reside|residing|resident|residents|based|located) "
    r"(in|outside|abroad|overseas)\b|\bnot (from|in) the (uk|eu|eea)\b|"
    r"\b(residents?|citizens?|nationals?) of\b|\b(non-?resident|citizenship|nationality)\b|"
    r"\ball over the world\b|\bworld ?wide\b|\bglobally\b|\bany ?where in the world\b|"
    r"\b(where|which|what) .{0,25}\blocations?\b|\blocations? do you\b|"
    r"\b(available|operate|operating|offered|supported) in (my|your|which|what|other|[a-z]+ ?\?)",
    re.I,
)
# Things that make a country/age mention about something else: delivery and
# lost cards stay cards, money movement stays transfers, rates/fees stay fees_fx.
_NOT_ELIG = re.compile(
    r"\b(deliver|delivered|delivering|delivery|ship|shipped|shipping|track|tracking|"
    r"arrive|arrived|arriving|post|posted|mail|mailed|lost|stolen|"
    r"send|sending|sent|transfer|transfers|transferring|top ?up|topping|deposit|wire|receive|"
    r"fee|fees|charge|charged|charges|rate|rates|exchange|currenc(y|ies)|atm|cash|"
    r"declined|refund|payment|payments)\b",
    re.I,
)
_ELIG_FROM = {"cards", "disputes", "transfers_topups", "fees_fx"}


def _is_eligibility(t):
    if _NOT_ELIG.search(t) or _PIN.search(t):
        return False
    if _AGE.search(t) or _COUNTRY.search(t):
        return True
    return bool(_CHILD.search(t) and _CHILD_ELIG.search(t))


def route(text, laya_dept):
    t = text or ""
    if laya_dept == "disputes" and _RATE.search(t):
        return "fees_fx"
    # Cards can also catch "card payment + wrong rate"; require a complaint word.
    if laya_dept == "cards" and _RATE.search(t) and _WRONG.search(t):
        return "fees_fx"
    if laya_dept == "account_security" and _PIN.search(t):
        return "cards"
    if laya_dept in _ELIG_FROM and _is_eligibility(t):
        return "account_security"
    return laya_dept
