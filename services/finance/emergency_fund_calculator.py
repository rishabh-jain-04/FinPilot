from services.finance.constants import (
    EMERGENCY_FUND_BASE_MONTHS,
    EMERGENCY_FUND_MIN_MONTHS,
    EMERGENCY_FUND_MAX_DEPENDANT_BONUS_MONTHS,
    EMERGENCY_FUND_MONTHS_PER_DEPENDANT,
    EMERGENCY_FUND_RISK_ADJUSTMENT_MONTHS
)


def calculate_emergency_fund(monthly_expenses, dependants, risk_profile):
    monthly_expenses = float(monthly_expenses)
    dependants = int(dependants or 0)
    risk_profile = risk_profile or "medium"

    if monthly_expenses <= 0:
        raise ValueError("monthly_expenses must be greater than zero.")

    if dependants < 0:
        raise ValueError("dependants cannot be negative.")

    if risk_profile not in EMERGENCY_FUND_RISK_ADJUSTMENT_MONTHS:
        raise ValueError("risk_profile must be one of: low, medium, high.")

    dependant_bonus_months = min(dependants, EMERGENCY_FUND_MAX_DEPENDANT_BONUS_MONTHS) * EMERGENCY_FUND_MONTHS_PER_DEPENDANT

    recommended_months = (
        EMERGENCY_FUND_BASE_MONTHS
        + EMERGENCY_FUND_RISK_ADJUSTMENT_MONTHS[risk_profile]
        + dependant_bonus_months
    )
    recommended_months = max(recommended_months, EMERGENCY_FUND_MIN_MONTHS)

    target_amount = monthly_expenses * recommended_months

    return {
        "monthly_expenses": round(monthly_expenses, 2),
        "dependants": dependants,
        "risk_profile": risk_profile,
        "recommended_months": recommended_months,
        "target_amount": round(target_amount, 2)
    }
