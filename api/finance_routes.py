from flask import Blueprint, request, jsonify

from services.finance.finance_service import (
    get_budget,
    get_sip_projection,
    get_emi,
    get_max_loan_amount,
    get_emergency_fund,
    get_tax
)

finance_bp = Blueprint(
    "finance",
    __name__,
    url_prefix="/api/finance"
)


@finance_bp.route("/budget", methods=["POST"])
def budget():
    data = request.get_json() or {}

    result = get_budget(
        data.get("user_id"),
        data.get("monthly_income"),
        data.get("monthly_expenses")
    )

    return jsonify(result)


@finance_bp.route("/sip", methods=["POST"])
def sip():
    data = request.get_json() or {}

    result = get_sip_projection(
        data.get("monthly_investment"),
        data.get("years"),
        data.get("annual_return_rate")
    )

    return jsonify(result)


@finance_bp.route("/emi", methods=["POST"])
def emi():
    data = request.get_json() or {}

    result = get_emi(
        data.get("principal"),
        data.get("annual_interest_rate"),
        data.get("tenure_years")
    )

    return jsonify(result)


@finance_bp.route("/emi/affordability", methods=["POST"])
def emi_affordability():
    data = request.get_json() or {}

    result = get_max_loan_amount(
        data.get("annual_interest_rate"),
        data.get("tenure_years"),
        data.get("user_id"),
        data.get("monthly_income"),
        data.get("existing_emi", 0),
        data.get("affordability_ratio")
    )

    return jsonify(result)


@finance_bp.route("/emergency-fund", methods=["POST"])
def emergency_fund():
    data = request.get_json() or {}

    result = get_emergency_fund(
        data.get("user_id"),
        data.get("monthly_expenses"),
        data.get("dependants"),
        data.get("risk_profile")
    )

    return jsonify(result)


@finance_bp.route("/tax", methods=["POST"])
def tax():
    data = request.get_json() or {}

    result = get_tax(
        data.get("user_id"),
        data.get("annual_gross_income")
    )

    return jsonify(result)
