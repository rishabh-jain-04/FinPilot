from flask import Blueprint, request, jsonify, g

from api.auth_middleware import require_auth
from services.chat.chat_service import handle_message

chat_bp = Blueprint(
    "chat",
    __name__,
    url_prefix="/api/chat"
)


@chat_bp.route("/message", methods=["POST"])
@require_auth
def message():
    data = request.get_json() or {}

    result = handle_message(
        g.user_id,
        data.get("message")
    )

    return jsonify(result)
