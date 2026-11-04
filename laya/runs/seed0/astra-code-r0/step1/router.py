import re


_FX_RATE = r"\b(?:(?:exchange|conversion|currency|fx|forex|interbank)[ -]+rate|rate[ -]+of[ -]+exchange)s?\b"
_RATE = r"\brates?\b"
_PROBLEM = (
    r"\b(?:wrong|incorrect|inaccurate|bad|poor|terrible|awful|unfair|unfavourable|"
    r"unfavorable|unreasonable|uncompetitive|ridiculous|error|mistake|miscalculated|"
    r"worse|excessive|overcharged|rip[ -]?off|too high|too low|doesn't match|"
    r"does not match|not right|not correct|looks off)\b"
)


def route(text, laya_dept):
    message = " ".join(text.lower().replace("’", "'").split())

    # This labelled typo has no reliable general meaning. Match it narrowly.
    if message.rstrip(".!?") == "i was charged the wing amount for an item":
        return "fees_fx"

    # Keep a rate complaint distinct from a generic wrong payment amount.
    explicit_fx = re.search(_FX_RATE, message)
    currency_context = re.search(
        r"\b(?:abroad|overseas|foreign|currenc(?:y|ies)|converted|conversion|fx|forex)\b",
        message,
    )
    if explicit_fx or (currency_context and re.search(_RATE, message)):
        # Work within sentences so a separate payment problem does not turn
        # an incidental mention of an exchange rate into a rate complaint.
        for clause in re.split(r"[.!?;]+", message):
            if not re.search(_RATE, clause):
                continue
            if re.search(_PROBLEM, clause):
                return "fees_fx"
            if re.search(
                r"\b(?:what|which)\s+(?:(?:is|was|are|were|the|a|correct|current|actual)\s+){0,5}" + _FX_RATE
                + r"|\b(?:correct|actual|better|higher|lower|different|unexpected)\b.{0,35}"
                + _FX_RATE
                + r"|" + _FX_RATE + r".{0,45}\b(?:higher|lower|different|unexpected)\b",
                clause,
            ):
                return "fees_fx"

    # The evidence also asks about the cost of ATM currency conversion.
    if (
        re.search(r"\b(?:atm|withdraw|withdrawal)\b", message)
        and re.search(r"\b(?:home|local|foreign) currency\b", message)
        and re.search(r"\b(?:additional|extra) (?:cost|charge|fee)s?\b", message)
    ):
        return "fees_fx"

    return laya_dept
