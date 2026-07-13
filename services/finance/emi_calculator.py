from services.finance.constants import DEFAULT_EMI_AFFORDABILITY_RATIO


def calculate_emi(principal, annual_interest_rate, tenure_years):
    principal = float(principal)
    annual_interest_rate = float(annual_interest_rate)
    tenure_years = float(tenure_years)

    if principal <= 0:
        raise ValueError("principal must be greater than zero.")

    if annual_interest_rate < 0:
        raise ValueError("annual_interest_rate cannot be negative.")

    if tenure_years <= 0:
        raise ValueError("tenure_years must be greater than zero.")

    monthly_rate = (annual_interest_rate / 100) / 12
    months = round(tenure_years * 12)

    if monthly_rate == 0:
        emi = principal / months
    else:
        emi = principal * monthly_rate * (1 + monthly_rate) ** months / (
            (1 + monthly_rate) ** months - 1
        )

    total_payment = emi * months
    total_interest = total_payment - principal

    return {
        "principal": round(principal, 2),
        "annual_interest_rate": annual_interest_rate,
        "tenure_years": tenure_years,
        "monthly_emi": round(emi, 2),
        "total_payment": round(total_payment, 2),
        "total_interest": round(total_interest, 2)
    }


def calculate_max_loan_amount(
    monthly_income,
    annual_interest_rate,
    tenure_years,
    existing_emi=0,
    affordability_ratio=None
):
    monthly_income = float(monthly_income)
    annual_interest_rate = float(annual_interest_rate)
    tenure_years = float(tenure_years)
    existing_emi = float(existing_emi or 0)
    ratio = float(affordability_ratio) if affordability_ratio is not None else DEFAULT_EMI_AFFORDABILITY_RATIO

    if monthly_income <= 0:
        raise ValueError("monthly_income must be greater than zero.")

    if tenure_years <= 0:
        raise ValueError("tenure_years must be greater than zero.")

    max_affordable_emi = (monthly_income * ratio) - existing_emi

    if max_affordable_emi <= 0:
        return {
            "monthly_income": round(monthly_income, 2),
            "affordability_ratio": ratio,
            "max_affordable_emi": 0,
            "max_loan_amount": 0
        }

    monthly_rate = (annual_interest_rate / 100) / 12
    months = round(tenure_years * 12)

    if monthly_rate == 0:
        max_loan_amount = max_affordable_emi * months
    else:
        max_loan_amount = max_affordable_emi * (
            (1 + monthly_rate) ** months - 1
        ) / (monthly_rate * (1 + monthly_rate) ** months)

    return {
        "monthly_income": round(monthly_income, 2),
        "affordability_ratio": ratio,
        "max_affordable_emi": round(max_affordable_emi, 2),
        "max_loan_amount": round(max_loan_amount, 2)
    }
