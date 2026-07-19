from flask import Blueprint, request, jsonify

from api.limiter import limiter
from services.auth.auth_service import (
    register_user,
    login_user
)

auth_bp = Blueprint(
    "auth",
    __name__,
    url_prefix="/api/auth"
)

@auth_bp.route("/register", methods=["POST"])
@limiter.limit("5 per hour")
def register():

    data = request.get_json()

    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    result = register_user(
        username,
        email,
        password
    )

    return jsonify(result)

@auth_bp.route("/login", methods=["POST"])
@limiter.limit("10 per minute")
def login():

    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    result = login_user(
        email,
        password
    )

    return jsonify(result)