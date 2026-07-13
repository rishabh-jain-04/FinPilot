from flask import Blueprint, request, jsonify

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
def create():

    data = request.get_json()

    result = create_user_profile(
        data["user_id"],
        data["monthly_income"],
        data["monthly_expenses"],
        data["dependants"],
        data["employment_type"],
        data["risk_profile"],
        data.get("currency", "INR")
    )

    return jsonify(result)


@profile_bp.route("/<int:user_id>", methods=["GET"])
def get(user_id):

    return jsonify(
        get_user_profile(user_id)
    )


@profile_bp.route("/<int:user_id>", methods=["PUT"])
def update(user_id):

    data = request.get_json()

    result = update_user_profile(
        user_id,
        data["monthly_income"],
        data["monthly_expenses"],
        data["dependants"],
        data["employment_type"],
        data["risk_profile"],
        data.get("currency", "INR")
    )

    return jsonify(result)