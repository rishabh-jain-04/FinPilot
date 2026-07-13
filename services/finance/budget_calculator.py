from services.finance.constants import BUDGET_ALLOCATION


def calculate_budget(monthly_income, monthly_expenses):
    monthly_income = float(monthly_income)
    monthly_expenses = float(monthly_expenses)

    if monthly_income <= 0:
        raise ValueError("monthly_income must be greater than zero.")

    if monthly_expenses < 0:
        raise ValueError("monthly_expenses cannot be negative.")

    recommended_needs = monthly_income * BUDGET_ALLOCATION["needs"]
    recommended_wants = monthly_income * BUDGET_ALLOCATION["wants"]
    recommended_savings = monthly_income * BUDGET_ALLOCATION["savings"]

    actual_savings = monthly_income - monthly_expenses
    actual_savings_rate = actual_savings / monthly_income
    savings_gap = actual_savings - recommended_savings

    return {
        "monthly_income": round(monthly_income, 2),
        "monthly_expenses": round(monthly_expenses, 2),
        "recommended_needs": round(recommended_needs, 2),
        "recommended_wants": round(recommended_wants, 2),
        "recommended_savings": round(recommended_savings, 2),
        "actual_savings": round(actual_savings, 2),
        "actual_savings_rate": round(actual_savings_rate, 4),
        "savings_gap": round(savings_gap, 2),
        "is_overspending": actual_savings < 0
    }
