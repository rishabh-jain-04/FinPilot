from services.finance.constants import (
    STANDARD_DEDUCTION,
    REBATE_TAXABLE_INCOME_THRESHOLD,
    CESS_RATE,
    TAX_SLABS_NEW_REGIME
)


def _slab_tax(taxable_income):
    tax = 0
    lower_bound = 0

    for upper_bound, rate in TAX_SLABS_NEW_REGIME:
        if taxable_income <= lower_bound:
            break

        slab_amount = min(taxable_income, upper_bound) - lower_bound
        tax += slab_amount * rate
        lower_bound = upper_bound

    return tax


def calculate_tax(annual_gross_income):
    annual_gross_income = float(annual_gross_income)

    if annual_gross_income < 0:
        raise ValueError("annual_gross_income cannot be negative.")

    taxable_income = max(0, annual_gross_income - STANDARD_DEDUCTION)

    tax_before_cess = _slab_tax(taxable_income)

    # Section 87A rebate: full rebate below the threshold. Marginal relief
    # just above the threshold is not modeled — a known simplification.
    if taxable_income <= REBATE_TAXABLE_INCOME_THRESHOLD:
        tax_before_cess = 0

    cess = tax_before_cess * CESS_RATE
    total_tax_payable = tax_before_cess + cess

    take_home_annual = annual_gross_income - total_tax_payable
    effective_tax_rate = (total_tax_payable / annual_gross_income) if annual_gross_income > 0 else 0

    return {
        "annual_gross_income": round(annual_gross_income, 2),
        "standard_deduction": STANDARD_DEDUCTION,
        "taxable_income": round(taxable_income, 2),
        "tax_before_cess": round(tax_before_cess, 2),
        "cess": round(cess, 2),
        "total_tax_payable": round(total_tax_payable, 2),
        "effective_tax_rate": round(effective_tax_rate, 4),
        "take_home_annual": round(take_home_annual, 2),
        "take_home_monthly": round(take_home_annual / 12, 2)
    }
