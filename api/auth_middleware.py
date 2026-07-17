from functools import wraps

import jwt
from flask import request, jsonify, g

from services.auth.auth_service import decode_token


def require_auth(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get("Authorization", "")

        if not auth_header.startswith("Bearer "):
            return jsonify({
                "success": False,
                "message": "Missing or invalid Authorization header."
            }), 401

        token = auth_header[len("Bearer "):]

        try:
            payload = decode_token(token)
        except jwt.ExpiredSignatureError:
            return jsonify({"success": False, "message": "Token has expired."}), 401
        except jwt.InvalidTokenError:
            return jsonify({"success": False, "message": "Invalid token."}), 401

        g.user_id = payload["user_id"]

        return f(*args, **kwargs)

    return wrapper
