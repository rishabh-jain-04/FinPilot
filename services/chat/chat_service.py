from services.chat.intent_classifier import classify_intent
from services.chat.entity_extractor import (
    extract_emi_params,
    extract_sip_params,
    extract_annual_income
)
from services.chat.gemini_client import get_explanation
from services.chat.constants import FINANCE_INTENTS, GENERAL_INTENT_REPLY

from services.finance.finance_service import (
    get_budget,
    get_sip_projection,
    get_emi,
    get_emergency_fund,
    get_tax
)

from db.conversation_repo import save_message


def _run_finance_calculation(intent, user_id, message):
    if intent == "budget":
        return get_budget(user_id, None, None)

    if intent == "sip":
        params = extract_sip_params(message)
        if params["monthly_investment"] is None or params["years"] is None:
            return {
                "success": False,
                "message": "I couldn't find a monthly investment amount and a duration in your "
                           "message. Try something like '10000 per month for 10 years at 12%'."
            }
        return get_sip_projection(
            params["monthly_investment"],
            params["years"],
            params["annual_return_rate"]
        )

    if intent == "emi":
        params = extract_emi_params(message)
        if params["principal"] is None or params["annual_interest_rate"] is None or params["tenure_years"] is None:
            return {
                "success": False,
                "message": "I couldn't find a loan amount, interest rate, and tenure in your "
                           "message. Try something like '20 lakh loan at 9% for 15 years'."
            }
        return get_emi(
            params["principal"],
            params["annual_interest_rate"],
            params["tenure_years"]
        )

    if intent == "emergency_fund":
        return get_emergency_fund(user_id, None, None, None)

    if intent == "tax":
        annual_income = extract_annual_income(message)
        return get_tax(user_id, annual_income)

    return {"success": False, "message": "Unrecognized finance intent."}


def handle_message(user_id, message):
    if not user_id:
        return {"success": False, "message": "user_id is required."}

    if not message:
        return {"success": False, "message": "message is required."}

    intent = classify_intent(message)

    if intent not in FINANCE_INTENTS:
        return {
            "success": True,
            "intent": "general",
            "reply": GENERAL_INTENT_REPLY
        }

    calculation = _run_finance_calculation(intent, user_id, message)

    if not calculation["success"]:
        reply = calculation["message"]
        data = None
    else:
        reply = get_explanation(intent, message, calculation["result"])
        data = calculation["result"]

    save_message(user_id, "user", message, intent)
    save_message(user_id, "assistant", reply, intent)

    return {
        "success": True,
        "intent": intent,
        "reply": reply,
        "data": data
    }
