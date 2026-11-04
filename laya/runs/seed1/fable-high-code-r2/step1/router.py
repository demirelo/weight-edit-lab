import re

# Step 1 correction: a complaint that a card payment or cash withdrawal used a
# bad/wrong exchange rate is fees_fx, not disputes. The rule needs BOTH a
# rate word and a complaint word so that plain "what is your rate?" questions
# and plain "wrong amount" disputes are left to Laya.

_RATE = re.compile(
    r"\b(exchange\s*rates?|fx\s*rates?|conversion\s*rates?|rates?|"
    r"exchange|fx|conversion|converted|convert)\b",
    re.I,
)

_COMPLAINT = re.compile(
    r"\b(wrong|incorrect|bad|poor|terrible|awful|horrible|unfair|ridiculous|"
    r"inaccurate|mistake|error|(was|is|seems|looks|be|been)\s+(way\s+|far\s+)?off|"
    r"rip[- ]?off|rip(ped|s)?\s+(me|us)?\s*off|overcharg\w*|"
    r"too\s+(high|much|low|expensive)|not\s+(right|correct|fair|accurate|"
    r"what|the\s+same|match\w*)|isn'?t\s+(right|correct|fair)|"
    r"wasn'?t\s+(right|correct|fair)|does\s*n[o']t\s+match|did\s*n[o']t\s+match|"
    r"doesn'?t\s+match|didn'?t\s+match|take\s+issue|issue\s+with|unhappy|"
    r"complain\w*|disagree|dispute|worse|higher\s+than|lower\s+than|"
    r"different\s+(from|than|to)|less\s+(money|cash|than)|"
    r"than\s+(i\s+)?expected|than\s+(it\s+)?should|than\s+(the\s+)?(market|"
    r"official|google|real|actual|mid)|short[- ]?changed|cheated|"
    r"lost\s+money|markup|marked\s+up|hidden)\b",
    re.I,
)


def _rate_complaint(text):
    t = text.lower()
    return bool(_RATE.search(t)) and bool(_COMPLAINT.search(t))


def route(text, laya_dept):
    if _rate_complaint(text):
        return "fees_fx"
    return laya_dept
