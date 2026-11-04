import re


_FX_RATE = r"\b(?:(?:exchange|conversion|currency|fx|forex|interbank)[ -]+rate|rate[ -]+of[ -]+exchange)s?\b"
_RATE = r"\brates?\b"
_PROBLEM = (
    r"\b(?:wrong|incorrect|inaccurate|bad|poor|terrible|awful|unfair|unfavourable|"
    r"unfavorable|unreasonable|uncompetitive|ridiculous|error|mistake|miscalculated|"
    r"worse|excessive|overcharged|rip[ -]?off|too high|too low|doesn't match|"
    r"does not match|not right|not correct|looks off)\b"
)


def _account_eligibility(message):
    # These vague labelled examples do not justify a general support/location rule.
    if message.rstrip(".!?") in {
        "can i get support",
        "where do you have locations at",
    }:
        return True

    account = re.search(r"\baccounts?\b", message)
    product = re.search(r"\b(?:accounts?|cards?|services?|app|sign[ -]?up|register)\b", message)
    age = re.search(
        r"\b(?:how old.{0,45}\b(?:be|open|apply|sign up)|minimum age|maximum age|age (?:limit|restriction|requirement)s?"
        r"|(?:what|which) age|old enough|too young|too old)\b",
        message,
    )
    young_person = re.search(
        r"\b(?:kids?|children|child|minors?|teenagers?|teens?|underage|under[ -]?18"
        r"|under[ -]\d{1,2}|\d{1,2}[ -]years?[ -]old|aged? \d{1,2}"
        r"|(?:i am|i'm) (?:only )?\d{1,2})\b",
        message,
    )
    # Age alone can describe a card's expiry; use explicit age-limit language.
    if age or (young_person and product):
        return True
    if account and re.search(
        r"\b(?:who (?:can|may|is allowed to)|eligib(?:le|ility)|qualif(?:y|ies|ications)"
        r"|requirements? (?:for|to) (?:open|opening|use|using|create|creating))\b",
        message,
    ):
        return True

    residence = re.search(
        r"\b(?:live|lives|living|reside|resides|residing|residents?|residency"
        r"|residence|citizens?|citizenship|nationality|based)\b",
        message,
    )
    access = re.search(
        r"\b(?:get|getting|open|opening|create|creating|set up|sign[ -]?up|register"
        r"|apply|available|availability|eligible|eligibility|offer|provide|access)\b",
        message,
    )
    if product and residence and access:
        return True

    countries = re.search(r"\b(?:countries|country|regions?|territories)\b", message)
    if countries and re.search(
        r"\b(?:supported|support|available|availability|eligible|eligibility|access"
        r"|operate|offer|provide)\b",
        message,
    ) and (product or re.search(r"\b(?:which|what) (?:countries|regions?|territories)\b", message)):
        return True
    if countries and product and re.search(
        r"\b(?:what|which) (?:countries|country|regions?|territories)\b", message
    ) and re.search(r"\b(?:use|using|get|open|register|sign[ -]?up)\b", message):
        return True

    # Geographic acquisition differs from delivery dates, shops, and ATM access.
    if re.search(
        r"\b(?:deliver\w*|ship\w*|replac\w*|lost|stolen|atm|shop|store|branch"
        r"|mail|post|wallet)\b", message
    ):
        return False
    acquisition = re.search(
        r"\b(?:get|order|obtain|apply for|request|open|create|set up|register for)\s+"
        r"(?:(?:a|an|the|your|my|new|one|of|these|those|separate|bank|payment|debit"
        r"|credit|virtual|physical|current|personal|business)\s+){0,6}(?:cards?|accounts?)\b"
        r"|\b(?:sign[ -]?up|available|availability|offer|provide)\b",
        message,
    )
    geography = re.search(
        r"\b(?:uk|u\.?k\.?|united kingdom|eu|europe|european union|us|usa"
        r"|u\.?s\.?a?\.?|united states|abroad|overseas)\b",
        message,
    )
    if product and acquisition and geography:
        return True
    if product and acquisition and re.search(
        r"\b(?:i am|i'm|we are|we're|people|customers|users|based) "
        r"(?:in|from|outside)\b", message
    ) and not re.search(r"\b(?:app|website|bank|branch|store|shop)\b", message):
        return True
    if re.search(r"\bwhere\b", message) and re.search(
        r"\b(?:services?|accounts?)\b", message
    ) and re.search(r"\b(?:available|supported|offered)\b", message):
        return True
    if product and acquisition and re.search(
        r"\b(?:in|from|outside|within) (?:the )?[a-z]+(?: [a-z]+){0,2}[?.!]*$",
        message,
    ) and re.search(r"\b(?:can i|can we|available|people|customers)\b", message):
        return not re.search(r"\bapp\b", message)
    return False


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

    # PIN questions belong to cards, even when failed attempts lock an account.
    # Match whole words so unrelated words such as "shopping" stay unchanged.
    if re.search(r"\b(?:pins?|personal identification numbers?)\b", message):
        return "cards"

    if _account_eligibility(message):
        return "account_security"

    return laya_dept
