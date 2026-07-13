from db.profile_repo import get_profile

from services.finance.budget_calculator import calculate_budget
from services.finance.sip_calculator import calculate_sip_future_value
from services.finance.emi_calculator import calculate_emi, calculate_max_loan_amount
from services.finance.emergency_fund_calculator import calculate_emergency_fund
from services.finance.tax_calculator import calculate_tax


def _resolve_profile_inputs(user_id, overrides):
    resolved = {}

    if user_id:
        profile = get_profile(user_id)
        if profile:
            resolved.update(dict(profile))

    for key, value in overrides.items():
        if value is not None:
            resolved[key] = value

    return resolved


def get_budget(user_id, monthly_income, monthly_expenses):
    inputs = _resolve_profile_inputs(user_id, {
        "monthly_income": monthly_income,
        "monthly_expenses": monthly_expenses
    })

    if inputs.get("monthly_income") is None or inputs.get("monthly_expenses") is None:
        return {
            "success": False,
            "message": "monthly_income and monthly_expenses are required, either directly or via a saved profile (user_id)."
        }

    try:
        result = calculate_budget(inputs["monthly_income"], inputs["monthly_expenses"])
    except (ValueError, TypeError) as error:
        return {"success": False, "message": str(error)}

    return {"success": True, "result": result}


def get_sip_projection(monthly_investment, years, annual_return_rate=None):
    if monthly_investment is None or years is None:
        return {
            "success": False,
            "message": "monthly_investment and years are required."
        }

    try:
        result = calculate_sip_future_value(monthly_investment, years, annual_return_rate)
    except (ValueError, TypeError) as error:
        return {"success": False, "message": str(error)}

    return {"success": True, "result": result}


def get_emi(principal, annual_interest_rate, tenure_years):
    if principal is None or annual_interest_rate is None or tenure_years is None:
        return {
            "success": False,
            "message": "principal, annual_interest_rate and tenure_years are required."
        }

    try:
        result = calculate_emi(principal, annual_interest_rate, tenure_years)
    except (ValueError, TypeError) as error:
        return {"success": False, "message": str(error)}

    return {"success": True, "result": result}


def get_max_loan_amount(
    annual_interest_rate,
    tenure_years,
    user_id=None,
    monthly_income=None,
    existing_emi=0,
    affordability_ratio=None
):
    if annual_interest_rate is None or tenure_years is None:
        return {
            "success": False,
            "message": "annual_interest_rate and tenure_years are required."
        }

    inputs = _resolve_profile_inputs(user_id, {"monthly_income": monthly_income})

    if inputs.get("monthly_income") is None:
        return {
            "success": False,
            "message": "monthly_income is required, either directly or via a saved profile (user_id)."
        }

    try:
        result = calculate_max_loan_amount(
            inputs["monthly_income"],
            annual_interest_rate,
            tenure_years,
            existing_emi,
            affordability_ratio
        )
    except (ValueError, TypeError) as error:
        return {"success": False, "message": str(error)}

    return {"success": True, "result": result}


def get_emergency_fund(user_id, monthly_expenses, dependants, risk_profile):
    inputs = _resolve_profile_inputs(user_id, {
        "monthly_expenses": monthly_expenses,
        "dependants": dependants,
        "risk_profile": risk_profile
    })

    if inputs.get("monthly_expenses") is None:
        return {
            "success": False,
            "message": "monthly_expenses is required, either directly or via a saved profile (user_id)."
        }

    try:
        result = calculate_emergency_fund(
            inputs["monthly_expenses"],
            inputs.get("dependants", 0),
            inputs.get("risk_profile", "medium")
        )
    except (ValueError, TypeError) as error:
        return {"success": False, "message": str(error)}

    return {"success": True, "result": result}


def get_tax(user_id, annual_gross_income):
    if annual_gross_income is None and user_id:
        profile = get_profile(user_id)
        if profile and profile["monthly_income"] is not None:
            annual_gross_income = profile["monthly_income"] * 12

    if annual_gross_income is None:
        return {
            "success": False,
            "message": "annual_gross_income is required, either directly or via a saved profile (user_id) with monthly_income set."
        }

    try:
        result = calculate_tax(annual_gross_income)
    except (ValueError, TypeError) as error:
        return {"success": False, "message": str(error)}

    return {"success": True, "result": result}
