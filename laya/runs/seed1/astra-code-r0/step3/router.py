import re


_CARD_PIN = re.compile(r"\b(?:pins?|personal identification numbers?)\b")


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


def _account_eligibility(message):
    """Recognise age and residence eligibility without changing card support."""
    account_or_service = bool(re.search(
        r"\b(?:accounts?|services?|sign[ -]?up|register|join)\b", message
    ))
    get_card = bool(re.search(
        r"\b(?:get|have|order|obtain|apply for|request)\b.{0,45}\bcards?\b",
        message,
    ))
    # Age questions can omit the account or service name entirely.
    if re.search(
        r"\b(?:age (?:limits?|requirements?|restrictions?|minimum|maximum)"
        r"|(?:minimum|maximum|legal|required) age|how old"
        r"|what age|old enough"
        r"|too young|too old|underage)\b", message
    ):
        # A card's age or expiry date is not the customer's age.
        if not re.search(r"\b(?:my|the|this|your) card\b", message) or (
            account_or_service or get_card
            or re.search(r"\b(?:i|you|we|they|kids?|children)\b", message)
        ):
            return True
    age_or_child = re.search(
        r"\b(?:children|child|kids?|minors?|teenagers?|teens?|son|daughter"
        r"|\d{1,2}[ -]years?[ -]old|(?:under|over|aged?|turning) \d{1,2}"
        r"|(?:i am|i'm|im|be) \d{1,2})\b", message
    )
    if age_or_child and (account_or_service or get_card):
        return True

    # These topics concern a transaction or a card feature, not residence.
    other_topic = re.search(
        r"\b(?:deliver\w*|ship\w*|postage|track\w*|merchants?|shops?"
        r"|stores?|currenc\w*|exchange|transfers?|top[ -]?ups?"
        r"|payments?|withdraw\w*|atms?|refunds?|fees?|travel\w*"
        r"|holiday|vacation|lost|stolen|replac\w*|languages?)\b", message
    )
    residence = re.search(
        r"\b(?:live|living|resid\w*|citizen\w*|nationalit\w*"
        r"|based in|(?:i am|i'm|im) from|from another country"
        r"|outside (?:of )?(?:the )?\w+)\b",
        message,
    )
    eligibility = re.search(
        r"\b(?:eligib\w*|qualif\w*|allowed|can|could|may|possible"
        r"|able|need|must|have to|requirements?)\b", message
    )
    if residence and eligibility and (account_or_service or get_card):
        if not other_topic:
            return True
    if other_topic:
        return False

    if re.search(r"\b(?:who|anyone|everyone)\b", message) and (
        account_or_service or get_card
    ) and re.search(r"\b(?:can|may|allowed|eligible|open|use|join|apply)\b", message):
        return True
    if re.search(r"\b(?:eligib\w*|qualif\w*)\b", message) and account_or_service:
        return True

    # Country coverage questions often refer to the provider as 'you'.
    geography = re.search(r"\b(?:countr(?:y|ies)|regions?|territories)\b", message)
    provider = re.search(r"\b(?:you|your|service|app|laya|accounts?)\b", message)
    coverage = re.search(
        r"\b(?:support\w*|offer\w*|availab\w*|operat\w*|work|use|open|access)\b",
        message,
    )
    if geography and coverage and (provider or re.search(r"\bsupport\w*\b", message)):
        # Explicit card usage abroad remains a card question.
        return not bool(re.search(r"\bcards?\b", message)) or get_card
    if re.search(r"\bwhere\b.{0,35}\b(?:locations?|available|operate|based)\b", message) and provider:
        return True
    if re.search(r"\b(?:worldwide|globally|all over the world|around the world)\b", message):
        return bool(re.search(r"\b(?:use|available|work|support)\b", message)) and not re.search(r"\bcards?\b", message)
    if provider and re.search(r"\b(?:available|offered|operate|supported) in\b", message):
        return not bool(re.search(r"\bcards?\b", message))
    if re.search(r"\b(?:support|accept)\b.{0,25}\b(?:customers?|users?|residents?) (?:in|from|of)\b", message):
        return True
    if re.search(
        r"\b(?:can|could|may)\b.{0,25}\b(?:open|register for|sign up for)\b"
        r".{0,20}\baccount\b.{0,15}\b(?:in|from)\b", message
    ) and not re.search(r"\b(?:app|website|online|browser|phone|minutes?)\b", message):
        return True
    return False


def route(text, laya_dept):
    """Correct account eligibility, card PINs, and transaction FX complaints."""
    message = " ".join(text.lower().replace("’", "'").split())
    if _account_eligibility(message):
        laya_dept = "account_security"
    # The routing examples use an unspecified PIN to mean a card PIN.
    # Keep the existing FX correction below as the higher-priority rule.
    if _CARD_PIN.search(message):
        laya_dept = "cards"
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
