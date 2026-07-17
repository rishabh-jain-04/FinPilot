from flask import Blueprint, request, jsonify, g

from api.auth_middleware import require_auth
from services.profile.profile_service import (
    create_user_profile,
    get_user_profile,
    update_user_profile
)

profile_bp = Blueprint(
    "profile",
    __name__,
    url_prefix="/api/profile"
)


@profile_bp.route("/", methods=["POST"])
@require_auth
def create():

    data = request.get_json()

    result = create_user_profile(
        g.user_id,
        data["monthly_income"],
        data["monthly_expenses"],
        data["dependants"],
        data["employment_type"],
        data["risk_profile"],
        data.get("currency", "INR")
    )

    return jsonify(result)


@profile_bp.route("/me", methods=["GET"])
@require_auth
def get():

    return jsonify(
        get_user_profile(g.user_id)
    )


@profile_bp.route("/me", methods=["PUT"])
@require_auth
def update():

    data = request.get_json()

    result = update_user_profile(
        g.user_id,
        data["monthly_income"],
        data["monthly_expenses"],
        data["dependants"],
        data["employment_type"],
        data["risk_profile"],
        data.get("currency", "INR")
    )

    return jsonify(result)
