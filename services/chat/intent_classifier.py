import spacy
from spacy.matcher import Matcher, PhraseMatcher

from services.chat.constants import (
    SPACY_MODEL_NAME,
    INTENT_TOKEN_LEMMAS,
    INTENT_PHRASES,
    PHRASE_MATCH_WEIGHT
)

_nlp = None
_matcher = None
_phrase_matcher = None


def _load_model():
    global _nlp, _matcher, _phrase_matcher

    if _nlp is not None:
        return

    _nlp = spacy.load(SPACY_MODEL_NAME)

    _matcher = Matcher(_nlp.vocab)
    for intent, lemmas in INTENT_TOKEN_LEMMAS.items():
        _matcher.add(intent, [[{"LEMMA": lemma}] for lemma in lemmas])

    _phrase_matcher = PhraseMatcher(_nlp.vocab, attr="LEMMA")
    for intent, phrases in INTENT_PHRASES.items():
        _phrase_matcher.add(intent, [_nlp(phrase) for phrase in phrases])


def classify_intent(message):
    _load_model()

    doc = _nlp(message.lower())

    scores = {intent: 0 for intent in INTENT_TOKEN_LEMMAS}

    for match_id, _start, _end in _matcher(doc):
        scores[_nlp.vocab.strings[match_id]] += 1

    for match_id, _start, _end in _phrase_matcher(doc):
        scores[_nlp.vocab.strings[match_id]] += PHRASE_MATCH_WEIGHT

    best_intent = max(scores, key=scores.get)

    if scores[best_intent] == 0:
        return "general"

    return best_intent
