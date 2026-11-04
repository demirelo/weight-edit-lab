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


# Step 2 correction: anything about a card PIN (change, reset, blocked,
# rejected, compromised, ...) is cards, not account_security. Any mention of
# the PIN is enough: in this product "PIN" always means the card PIN; the app
# login secret is called "passcode", which is left alone.

_PIN = re.compile(r"\bpins?\b|\bpin[- ]?(codes?|numbers?)\b|\bp\.i\.n\.?\b", re.I)


def _pin_message(text):
    return bool(_PIN.search(text))


# Step 3 correction: "who may open or use an account" questions (age limits,
# supported countries) are account_security, not cards. Two signal families:
# an age signal, or a country/location signal. Either one fires the rule,
# unless a blocker shows the message is really about something else that
# merely mentions a place or a person (card delivery abroad, card acceptance,
# currencies, transfers, or a transaction).

_AGE = re.compile(
    r"\bages?\b|\baged\b|\bhow\s+old\b|\bold\s+enough\b|\btoo\s+young\b|"
    r"\bhow\s+young\b|\byoungest\b|\bunder[- ]?age\b|\bunder\s+(1[0-9]|2[01])\b|"
    r"\bminimum\s+age\b|\bage\s+(limit|requirement|restriction)s?\b|"
    r"\b(be|turn|turned|turns|over|above|below|least|i'?m)\s+(1[0-9]|2[01])\b|"
    r"\b(1[0-9]|2[01])\s*(\+|years?|yrs?|y/?o)\b|\b\d{1,2}[- ]?years?[- ]?old\b|"
    r"\bkids?\b|\bchild(ren)?\b|\bteen(ager)?s?\b|\bminors\b|"
    r"\bminor\b(?!\s+(issue|problem|charge|fee|thing|error|bug|mistake))|"
    r"\b(my|our)\s+(son|daughter)s?\b|\byoung(er)?\s+(person|people|adult)s?\b|"
    r"\badults?\s+only\b|\bgrown[- ]?ups?\b",
    re.I,
)

_PLACE_GENERIC = re.compile(
    r"\bcountr(y|ies)\b|\bnations?\b|\bnationalit(y|ies)\b|\bregions?\b|"
    r"\blocations?\b|\bworldwide\b|\binternational(ly)?\b|\bglobal(ly)?\b|"
    r"\b(all\s+over|anywhere\s+in|around|other\s+parts\s+of|rest\s+of)\s+the\s+(world|globe)\b|"
    r"\boverseas\b|\bnon[- ]?(uk|eu|european|british|us|american)\b|"
    r"\boutside\s+(of\s+)?(the\s+)?(uk|u\.k\.|eu|e\.u\.|europe|britain|england|us|u\.s\.|usa|america)\b|"
    r"\boutside\s+(of\s+)?(my|your|the)\s+country\b|\b(where|which\s+places?)\s+(are|do|is)\s+(you|it|this|we)\b.*"
    r"\b(available|operate|operating|offered|offer|work|support\w*|service|serve|located|based)\b|"
    r"\bwhere\s+can\s+(i|we|one)\s+(use\s+(this|it)|sign\s*up|register|join)\b",
    re.I,
)

_PLACE_NAMES = re.compile(
    r"\b(uk|u\.k\.|united\s+kingdom|britain|great\s+britain|england|scotland|wales|"
    r"northern\s+ireland|ireland|the\s+us|in\s+us|u\.s\.|u\.s\.a\.|usa|united\s+states|america|"
    r"eu|e\.u\.|europe|european\s+union|eea|eurozone|canada|australia|new\s+zealand|"
    r"india|china|japan|korea|singapore|hong\s+kong|thailand|vietnam|indonesia|"
    r"malaysia|philippines|pakistan|bangladesh|sri\s+lanka|nepal|"
    r"germany|france|spain|portugal|italy|netherlands|holland|belgium|luxembourg|"
    r"switzerland|austria|denmark|sweden|norway|finland|iceland|poland|czech|"
    r"czechia|slovakia|hungary|romania|bulgaria|greece|cyprus|malta|croatia|"
    r"slovenia|serbia|bosnia|albania|estonia|latvia|lithuania|ukraine|russia|turkey|"
    r"israel|egypt|morocco|nigeria|kenya|ghana|south\s+africa|africa|asia|"
    r"brazil|argentina|chile|colombia|peru|mexico|south\s+america|latin\s+america|"
    r"dubai|uae|saudi\s+arabia|qatar|middle\s+east|caribbean|"
    r"american|british|canadian|australian|indian|chinese|german|french|"
    r"spanish|italian|dutch|irish|scottish|polish|european|asian|african|"
    r"a\s+different\s+country|another\s+country|other\s+countries|my\s+country|"
    r"a\s+foreign\s+country|foreign\s+countries|home\s+country|this\s+country)\b",
    re.I,
)

# Residence / eligibility context: a named place counts only with one of these
# so that "deliver my card to the US" or "my trip to Spain" do not fire.
_RESIDENCE = re.compile(
    r"\blive\b|\blives\b|\bliving\b|\bresid\w*\b|\bcitizen\w*\b|\bbased\s+in\b|"
    r"\blocated\s+in\b|\bmoved?\s+to\b|\bmoving\s+to\b|\brelocat\w*\b|"
    r"\b(i'?m|i\s+am|we\s+are|we'?re|am|are)\s+(from|in)\b|\bfrom\s+(the\s+)?(uk|us|usa|eu|europe|canada|australia|india|[a-z]+)\s*[,.?!]|"
    r"\boutside\b|\bnot\s+in\s+the\b|\bnot\s+from\b|\bdon'?t\s+live\b|\bdo\s+not\s+live\b|"
    r"\baddress\s+(is|in)\b|\bif\s+i\s+(am|live|stay)\b|\bavailable\b|\boperate\b|"
    r"\bsupport(ed)?\b|\bwork\s+in\b|\beligib\w*\b|\ballowed\b|\bopen\s+an?\s+account\b|"
    r"\bsign\s*up\b|\bregister\b|\bjoin\b|\bapply\b|\b(get|obtain|have|order)\s+an?\s+(card|account)\b|"
    r"\buse\s+(this|it|the\s+(app|service)|your\s+(app|service))\b|\bin\s+the\s+(us|usa|uk|eu)\b",
    re.I,
)

# Blockers: the message is about a card's delivery or acceptance, about
# currencies or rates, about moving money, or about a specific transaction.
_BLOCK = re.compile(
    r"\bdeliver\w*\b|\bship\w*\b|\bship(ping|ped)?\b|\bpost(ed|age)?\b|\bmail\w*\b|"
    r"\btrack\w*\b|\barriv\w*\b|\bexpress\b|\bhow\s+long\b|\bwhen\s+will\b|"
    r"\bcurrenc\w*\b|\bexchang\w*\b|\brates?\b|\bfx\b|\bfees?\b|\bcharg\w*\b|"
    r"\btransfer\w*\b|\bsend(ing)?\b|\bsent\b|\breceiv\w*\b|\btop[- ]?(up|ping)\b|"
    r"\bdeposit\w*\b|\bwire\b|\biban\b|\bswift\b|\bpayment\w*\b|\bpaid\b|\bpay\b|"
    r"\btransaction\w*\b|\bwithdraw\w*\b|\bdeclin\w*\b|\brefund\w*\b|\bpending\b|"
    r"\batm\b|\bcash\b|\bmerchant\w*\b|\bshop\w*\b|\bstore\b|\bstores\b|\btravel\w*\b|"
    r"\btrip\b|\bholiday\b|\bvacation\b|\babroad\b|\bcontactless\b|\bapple\s+pay\b|"
    r"\bgoogle\s+pay\b|\bvirtual\b|\bdisposable\b|\bactivat\w*\b|\breplac\w*\b|"
    r"\blost\b|\bstolen\b|\bblock\w*\b|\bfroz\w*\b|\bfreez\w*\b|\bexpir\w*\b|"
    r"\bpurchas\w*\b|\bbought\b|\bspent\b|\bspend\w*\b|\bdebit\w*\b|\bsubscri\w*\b|"
    r"\b(spare|second|additional|extra|another|more)\s+(\w+\s+)?cards?\b",
    re.I,
)

# Card acceptance ("can I use my card in X", "is the card accepted") stays
# with cards. "get a card" / "order a card" is eligibility and does not match.
_CARD_USE = re.compile(
    r"\b(use|using|used|accept\w*|work|works|working|take|taken|valid|swipe|tap)\b[^.?!]{0,40}\bcards?\b|"
    r"\bcards?\b[^.?!]{0,40}\b(accept\w*|work|works|working|valid|usable|use|used|support\w*)\b",
    re.I,
)


def _eligibility(text):
    t = text.lower()
    if _BLOCK.search(t) or _CARD_USE.search(t):
        return False
    if _AGE.search(t):
        return True
    if _PLACE_GENERIC.search(t):
        return True
    if _PLACE_NAMES.search(t) and _RESIDENCE.search(t):
        return True
    return False


def route(text, laya_dept):
    if _rate_complaint(text):
        return "fees_fx"
    if _pin_message(text):
        return "cards"
    if _eligibility(text):
        return "account_security"
    return laya_dept
