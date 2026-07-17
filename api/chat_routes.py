from flask import Blueprint, request, jsonify

from services.chat.chat_service import handle_message

chat_bp = Blueprint(
    "chat",
    __name__,
    url_prefix="/api/chat"
)


@chat_bp.route("/message", methods=["POST"])
def message():
    data = request.get_json() or {}

    result = handle_message(
        data.get("user_id"),
        data.get("message")
    )

    return jsonify(result)
