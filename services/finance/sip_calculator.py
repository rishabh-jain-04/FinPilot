from services.finance.constants import DEFAULT_SIP_ANNUAL_RETURN_RATE


def calculate_sip_future_value(monthly_investment, years, annual_return_rate=None):
    monthly_investment = float(monthly_investment)
    years = float(years)

    if monthly_investment <= 0:
        raise ValueError("monthly_investment must be greater than zero.")

    if years <= 0:
        raise ValueError("years must be greater than zero.")

    rate = float(annual_return_rate) if annual_return_rate is not None else DEFAULT_SIP_ANNUAL_RETURN_RATE

    if rate <= 0:
        raise ValueError("annual_return_rate must be greater than zero.")

    monthly_rate = rate / 12
    months = round(years * 12)

    future_value = monthly_investment * (
        ((1 + monthly_rate) ** months - 1) / monthly_rate
    ) * (1 + monthly_rate)

    total_invested = monthly_investment * months
    estimated_returns = future_value - total_invested

    return {
        "monthly_investment": round(monthly_investment, 2),
        "years": years,
        "annual_return_rate": rate,
        "total_invested": round(total_invested, 2),
        "estimated_returns": round(estimated_returns, 2),
        "future_value": round(future_value, 2)
    }
