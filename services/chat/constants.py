SPACY_MODEL_NAME = "en_core_web_md"

FINANCE_INTENTS = {"budget", "sip", "emi", "emergency_fund", "tax"}

GENERAL_INTENT_REPLY = (
    "I can help with budgeting, SIP, EMI, emergency fund, and tax questions "
    "— try asking about one of those!"
)

GEMINI_MODEL_NAME = "gemini-flash-latest"

# Single-token lemmas. Matched via spaCy's Matcher on the LEMMA attribute,
# so "investing"/"invested"/"invests" all normalize to "invest".
INTENT_TOKEN_LEMMAS = {
    "budget": ["budget", "spend", "spending", "expense", "save", "saving", "overspend", "allocate"],
    "sip": ["sip", "invest", "investment", "investing", "grow", "growth", "return"],
    "emi": ["emi", "loan", "installment", "instalment", "borrow", "borrowing", "mortgage", "lend", "afford", "affordable"],
    "emergency_fund": ["emergency", "reserve", "cushion", "safety"],
    "tax": ["tax", "liability", "taxable"]
}

# Multi-word phrases. Matched via spaCy's PhraseMatcher (also on LEMMA) and
# weighted higher than single-token matches, since a full phrase is a
# stronger signal than one shared word (e.g. "fund" alone is ambiguous
# between "mutual fund" and "emergency fund" — the phrase is not).
INTENT_PHRASES = {
    "sip": ["mutual fund", "systematic investment plan"],
    "emi": ["car loan", "home loan", "personal loan"],
    "emergency_fund": ["emergency fund", "rainy day fund", "safety net"],
    "tax": ["income tax", "tax liability"]
}

PHRASE_MATCH_WEIGHT = 2
