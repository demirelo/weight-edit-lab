import re


_FX_RATE = re.compile(
    r"\b(?:(?:exchange|conversion|currency|fx|foreign exchange)\s+rates?"
    r"|rates?\s+of\s+exchange|currency\s+conversion)\b"
)
_CARD_OR_CASH = re.compile(
    r"\b(?:cards?|payments?|paid|purchases?|bought|buy|shopping|spent"
    r"|withdraw\w*|cash|atm)\b"
)
_TRANSFER = re.compile(r"\b(?:transfers?|top[ -]?ups?|deposits?|remittances?)\b")
_COMPLAINT = re.compile(
    r"\b(?:wrong|incorrect|inaccurate|bad|poor|terrible|awful|unfair"
    r"|unfavo(?:u)?rable|unreasonable|unexpected|worse|too high|too low"
    r"|overcharg\w*|rip[ -]?off|take issue|does(?:n't| not) (?:match|look right)"
    r"|is(?:n't| not) (?:right|correct)|was(?:n't| not) (?:right|correct)"
    r"|less (?:\w+\s+){0,4}than (?:\w+\s+){0,3}expected"
    r"|more (?:\w+\s+){0,4}than (?:\w+\s+){0,3}expected"
    r"|(?:amount|rate|conversion) (?:\w+\s+){0,3}looks? (?:off|wrong)"
    r"|(?:charged|paid|cost) (?:me )?(?:too much|more))\b"
)


def route(text, laya_dept):
    """Correct complaints about the FX rate used for a card or cash transaction."""
    message = " ".join(text.lower().replace("’", "'").split())
    card_or_cash = bool(_CARD_OR_CASH.search(message))
    explicit_fx = bool(_FX_RATE.search(message))
    # Some complaints call this only the ATM or withdrawal "rate".
    implied_fx = card_or_cash and bool(re.search(r"\brates?\b", message))
    if not (explicit_fx or implied_fx):
        return laya_dept
    # Leave complaints that explicitly concern only a transfer or top-up alone.
    if _TRANSFER.search(message) and not card_or_cash:
        return laya_dept
    for complaint in _COMPLAINT.finditer(message):
        prefix = message[max(0, complaint.start() - 30):complaint.start()]
        if re.search(r"\b(?:not|never|isn't|wasn't|isnt|wasnt)\s+(?:\w+\s+){0,2}$", prefix):
            continue
        return "fees_fx"
    return laya_dept
