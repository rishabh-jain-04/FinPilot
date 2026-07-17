from flask import Blueprint, request, jsonify, g

from api.auth_middleware import require_auth
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
@require_auth
def budget():
    data = request.get_json() or {}

    result = get_budget(
        g.user_id,
        data.get("monthly_income"),
        data.get("monthly_expenses")
    )

    return jsonify(result)


@finance_bp.route("/sip", methods=["POST"])
@require_auth
def sip():
    data = request.get_json() or {}

    result = get_sip_projection(
        data.get("monthly_investment"),
        data.get("years"),
        data.get("annual_return_rate")
    )

    return jsonify(result)


@finance_bp.route("/emi", methods=["POST"])
@require_auth
def emi():
    data = request.get_json() or {}

    result = get_emi(
        data.get("principal"),
        data.get("annual_interest_rate"),
        data.get("tenure_years")
    )

    return jsonify(result)


@finance_bp.route("/emi/affordability", methods=["POST"])
@require_auth
def emi_affordability():
    data = request.get_json() or {}

    result = get_max_loan_amount(
        data.get("annual_interest_rate"),
        data.get("tenure_years"),
        g.user_id,
        data.get("monthly_income"),
        data.get("existing_emi", 0),
        data.get("affordability_ratio")
    )

    return jsonify(result)


@finance_bp.route("/emergency-fund", methods=["POST"])
@require_auth
def emergency_fund():
    data = request.get_json() or {}

    result = get_emergency_fund(
        g.user_id,
        data.get("monthly_expenses"),
        data.get("dependants"),
        data.get("risk_profile")
    )

    return jsonify(result)


@finance_bp.route("/tax", methods=["POST"])
@require_auth
def tax():
    data = request.get_json() or {}

    result = get_tax(
        g.user_id,
        data.get("annual_gross_income")
    )

    return jsonify(result)
