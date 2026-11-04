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


# Step 3 correction: who may open or use an account (age limits, supported
# countries, where the customer lives) is account_security, not cards.

# Age eligibility: the word "age", "how old", "years old", "be 18",
# "under 16", "old enough", "too young", "underage", "teenager".
_AGE = re.compile(
    r"\bages?\b"
    r"|\bhow old\b"
    r"|\b(years?|yrs?)[\s-]*old\b"
    r"|\bold enough\b"
    r"|\btoo young\b"
    r"|\bunder[\s-]*age\w*\b"
    r"|\bteen\w*\b"
    r"|\byoung\w*\b"
    r"|\bjuniors?\b"
    r"|\b(be|being|turn\w*|i'?m|over|under|above|below|at least|"
    r"older than|younger than|minimum|aged?)\s+(of\s+)?(1[0-9]|2[0-5])\b",
    re.I,
)
# Children / kids only count next to opening, using or being allowed an
# account or card, so that "send money to my kid" stays with transfers.
_CHILD = re.compile(r"\b(child|children|kids?|son|daughter|minors?)\b", re.I)
_CHILD_CONTEXT = re.compile(
    r"\b(accounts?|cards?|open\w*|sign\w*\s*up|register\w*|join\w*|use|using|"
    r"service|allow\w*|eligib\w*|limit\w*|permitted|old|age)\b",
    re.I,
)

# Country / region eligibility.
_PLACES = (
    r"us|usa|uk|eu|europe|america|canada|australia|india|asia|africa|"
    r"united states|united kingdom|england|scotland|wales|ireland|germany|"
    r"france|spain|italy|portugal|netherlands|holland|belgium|austria|"
    r"switzerland|poland|sweden|norway|denmark|finland|greece|turkey|"
    r"mexico|brazil|argentina|japan|china|singapore|hong kong|new zealand|"
    r"south africa|nigeria|pakistan|russia|ukraine|dubai|uae|israel|"
    r"my country|another country|other countries"
)
_COUNTRY_WORD = re.compile(
    r"\b(countr(y|ies)|nations?|nationalit\w*|regions?|locations?|"
    r"territor(y|ies)|states|markets|worldwide|world[\s-]*wide|"
    r"based|headquarter\w*|offices?|"
    r"international\w*|globally|global|"
    r"(all over|around|anywhere in) the world|the world|"
    r"outside (of )?(the )?\w+|"
    r"(non[\s-]*)?residen(t|ts|cy)|citizens?(hip)?|"
    r"(live|living|reside|residing|based|located|staying|"
    r"moving|moved)\s+(in|to|outside)\b|"
    r"\b(from|in|to)\s+(the\s+)?(" + _PLACES + r")\b)",
    re.I,
)
# A capitalised place name after "in", "to" or "from": "in Germany".
# Case-sensitive on purpose.
_PLACE_CAP = re.compile(r"\b([Ii]n|to|from|outside|within)\s+(the\s+)?[A-Z][a-z]{2,}\b")
# "abroad" / "overseas" only count next to signing up or opening an
# account; "use my card abroad" is a card question.
_ABROAD = re.compile(r"\b(abroad|overseas)\b", re.I)
_ABROAD_CONTEXT = re.compile(
    r"\b(open\w*|sign\w*\s*up|register\w*|join\w*|apply\w*|eligib\w*|"
    r"accounts?)\b",
    re.I,
)
# The customer asks whether the service is offered / available / usable there.
_AVAILABILITY = re.compile(
    r"\b(support\w*|offer\w*|available|availab\w*|operat\w*|serve|serving|"
    r"cover\w*|eligib\w*|allow\w*|work\s+(with|in)|works?\b|"
    r"open\w*|sign\w*\s*up|register\w*|join\w*|apply\w*|"
    r"get\s+(a|an|the|my)?\s*(card|account)|"
    r"have\s+(a|an)?\s*(card|account)|"
    r"use\s+(this|it|your|the|my)\b|"
    r"where (are|do|is)\s+(you|your)|"
    r"which|what|how many|all|every|still|possible)\b",
    re.I,
)
# Not an eligibility question: moving money, currency, fees or card
# delivery that happens to name a place.
_NOT_ELIGIBILITY = re.compile(
    r"\b(transfer\w*|send\w*|sent|receiv\w*|exchang\w*|currenc\w*|rates?|"
    r"fees?|charg\w*|cost\w*|deliver\w*|shipp\w*|ship|shipped|track\w*|"
    r"post\w*|mail\w*|arriv\w*|dispatch\w*|top[\s-]*ups?|withdraw\w*|atm|"
    r"declin\w*|refund\w*|payment|paid|pending|duplicate|twice|"
    r"verif\w*|identity|passcode|password|phone|lost|stolen|"
    r"apple pay|google pay|contactless|activat\w*|merchant\w*|accept\w*|"
    r"shops?|stores?|restaurants?)\b",
    re.I,
)


def _is_eligibility_question(text):
    if _NOT_ELIGIBILITY.search(text):
        return False
    if _AGE.search(text):
        return True
    if _CHILD.search(text) and _CHILD_CONTEXT.search(text):
        return True
    if _ABROAD.search(text) and _ABROAD_CONTEXT.search(text):
        return True
    place = _COUNTRY_WORD.search(text) or _PLACE_CAP.search(text)
    return bool(place and _AVAILABILITY.search(text))


def route(text, laya_dept):
    text = text or ""
    # Step 2: the correction only moves PIN messages away from
    # account_security. Other departments keep their own handling, e.g. a
    # declined card payment that mentions the PIN stays with disputes.
    if laya_dept == "account_security" and _is_pin_message(text):
        return "cards"
    # Step 3: eligibility questions go to account_security whatever Laya
    # said, except PIN messages, which step 2 owns.
    if (
        laya_dept != "account_security"
        and not _is_pin_message(text)
        and _is_eligibility_question(text)
    ):
        return "account_security"
    # Step 1: only card payments and cash withdrawals are in scope, so only
    # the two departments Laya uses for those get overridden. Transfers keep
    # their own handling.
    if laya_dept in ("disputes", "cards") and _is_exchange_rate_complaint(text):
        return "fees_fx"
    return laya_dept
