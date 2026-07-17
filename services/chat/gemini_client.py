from google import genai

from config import Config
from services.chat.constants import GEMINI_MODEL_NAME

_client = None


def _get_client():
    global _client

    if _client is None:
        _client = genai.Client(api_key=Config.GEMINI_API_KEY)

    return _client


def _build_prompt(intent, user_message, calculation_result):
    return (
        "You are a financial advisory assistant. A deterministic finance "
        "calculation engine has already computed the exact numbers below — "
        "do not perform any calculations yourself and do not invent numbers "
        "that are not present in the data. Explain this data to the user in "
        "plain, encouraging language, under 120 words.\n\n"
        f"Intent: {intent}\n"
        f"User's question: {user_message}\n"
        f"Calculated data: {calculation_result}\n"
    )


def _try_gemini(intent, user_message, calculation_result):
    if not Config.GEMINI_API_KEY:
        return None

    try:
        client = _get_client()
        response = client.models.generate_content(
            model=GEMINI_MODEL_NAME,
            contents=_build_prompt(intent, user_message, calculation_result)
        )
        return response.text
    except Exception:
        return None


def _fallback_explanation(intent, result):
    if intent == "budget":
        return (
            f"Based on a monthly income of Rs {result['monthly_income']:,.0f}, we recommend "
            f"Rs {result['recommended_needs']:,.0f} for needs, Rs {result['recommended_wants']:,.0f} "
            f"for wants, and Rs {result['recommended_savings']:,.0f} for savings. You are "
            f"currently saving Rs {result['actual_savings']:,.0f} per month."
        )

    if intent == "sip":
        return (
            f"Investing Rs {result['monthly_investment']:,.0f} per month for {result['years']:.0f} years "
            f"at an assumed {result['annual_return_rate'] * 100:.1f}% annual return could grow to "
            f"approximately Rs {result['future_value']:,.0f}, including Rs {result['estimated_returns']:,.0f} "
            f"in estimated returns."
        )

    if intent == "emi":
        return (
            f"For a loan of Rs {result['principal']:,.0f} at {result['annual_interest_rate']}% over "
            f"{result['tenure_years']:.0f} years, your estimated monthly EMI is Rs {result['monthly_emi']:,.0f}, "
            f"with total interest of Rs {result['total_interest']:,.0f}."
        )

    if intent == "emergency_fund":
        return (
            f"Based on monthly expenses of Rs {result['monthly_expenses']:,.0f} and a "
            f"{result['risk_profile']} risk profile, we recommend an emergency fund of "
            f"Rs {result['target_amount']:,.0f} ({result['recommended_months']} months of expenses)."
        )

    if intent == "tax":
        return (
            f"On an annual income of Rs {result['annual_gross_income']:,.0f}, your estimated tax "
            f"payable is Rs {result['total_tax_payable']:,.0f}, leaving a take-home of "
            f"Rs {result['take_home_annual']:,.0f} per year (Rs {result['take_home_monthly']:,.0f}/month)."
        )

    return "Here are your results."


def get_explanation(intent, user_message, calculation_result):
    explanation = _try_gemini(intent, user_message, calculation_result)

    if explanation:
        return explanation

    return _fallback_explanation(intent, calculation_result)
