BUDGET_ALLOCATION = {
    "needs": 0.50,
    "wants": 0.30,
    "savings": 0.20
}

DEFAULT_SIP_ANNUAL_RETURN_RATE = 0.12

DEFAULT_EMI_AFFORDABILITY_RATIO = 0.40

EMERGENCY_FUND_BASE_MONTHS = 6
EMERGENCY_FUND_MIN_MONTHS = 3
EMERGENCY_FUND_MAX_DEPENDANT_BONUS_MONTHS = 4
EMERGENCY_FUND_MONTHS_PER_DEPENDANT = 1
EMERGENCY_FUND_RISK_ADJUSTMENT_MONTHS = {
    "low": 3,
    "medium": 0,
    "high": -2
}

# New tax regime, FY2025-26 (Union Budget 2025). Verify against the latest
# Union Budget before relying on this for a later financial year.
STANDARD_DEDUCTION = 75000
REBATE_TAXABLE_INCOME_THRESHOLD = 1200000
CESS_RATE = 0.04
TAX_SLABS_NEW_REGIME = [
    (400000, 0.00),
    (800000, 0.05),
    (1200000, 0.10),
    (1600000, 0.15),
    (2000000, 0.20),
    (2400000, 0.25),
    (float("inf"), 0.30)
]
