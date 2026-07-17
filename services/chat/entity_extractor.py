import re

LAKH = 100_000
CRORE = 10_000_000
THOUSAND = 1_000

_AMOUNT_MULTIPLIERS = {
    "lakh": LAKH,
    "lac": LAKH,
    "crore": CRORE,
    "cr": CRORE,
    "k": THOUSAND,
    "thousand": THOUSAND
}

_PERCENT_PATTERN = re.compile(r"([\d,]+(?:\.\d+)?)\s*(?:%|percent)", re.IGNORECASE)
_YEARS_PATTERN = re.compile(r"([\d,]+(?:\.\d+)?)\s*(?:years?|yrs?)", re.IGNORECASE)
_MONTHS_PATTERN = re.compile(r"([\d,]+(?:\.\d+)?)\s*(?:months?|mos?)", re.IGNORECASE)
_AMOUNT_PATTERN = re.compile(
    r"(?:₹|rs\.?|inr)?\s*([\d,]+(?:\.\d+)?)\s*(lakh|lac|crore|cr|k|thousand)?",
    re.IGNORECASE
)


def _strip_match(pattern, text):
    match = pattern.search(text)
    if not match:
        return None, text

    value = float(match.group(1).replace(",", ""))
    remaining_text = text[:match.start()] + text[match.end():]
    return value, remaining_text


def _extract_duration_years(text):
    years, remaining_text = _strip_match(_YEARS_PATTERN, text)
    if years is not None:
        return years, remaining_text

    months, remaining_text = _strip_match(_MONTHS_PATTERN, text)
    if months is not None:
        return months / 12, remaining_text

    return None, text


def _extract_amount(text):
    match = _AMOUNT_PATTERN.search(text)
    if not match:
        return None, text

    value = float(match.group(1).replace(",", ""))
    unit = (match.group(2) or "").lower()
    value *= _AMOUNT_MULTIPLIERS.get(unit, 1)

    remaining_text = text[:match.start()] + text[match.end():]
    return value, remaining_text


def extract_emi_params(text):
    working_text = text

    interest_rate, working_text = _strip_match(_PERCENT_PATTERN, working_text)
    tenure_years, working_text = _extract_duration_years(working_text)
    principal, working_text = _extract_amount(working_text)

    return {
        "principal": principal,
        "annual_interest_rate": interest_rate,
        "tenure_years": tenure_years
    }


def extract_sip_params(text):
    working_text = text

    return_rate_percent, working_text = _strip_match(_PERCENT_PATTERN, working_text)
    years, working_text = _extract_duration_years(working_text)
    monthly_investment, working_text = _extract_amount(working_text)

    return {
        "monthly_investment": monthly_investment,
        "years": years,
        "annual_return_rate": (return_rate_percent / 100) if return_rate_percent is not None else None
    }


def extract_annual_income(text):
    amount, _ = _extract_amount(text)
    return amount
