import bcrypt
import jwt
from datetime import datetime, timedelta

from config import Config
from db.user_repo import create_user, get_user_by_email

def hash_password(password):
    password_bytes = password.encode("utf-8")
    hashed = bcrypt.hashpw(
     password_bytes,
     bcrypt.gensalt()
    )

    return hashed.decode("utf-8")

def register_user(username, email, password):

    existing_user = get_user_by_email(email)

    if existing_user:
        return {
            "success": False,
            "message": "Email already registered."
        }

    password_hash = hash_password(password)

    create_user(
        username,
        email,
        password_hash
    )

    return {
        "success": True,
        "message": "User registered successfully."
    }

def login_user(email, password):
    user = get_user_by_email(email)

    if user is None:
        return {
            "success": False,
            "message": "Invalid email or password."
        }
    
    password_matches = bcrypt.checkpw(
        password.encode("utf-8"),
        user["password_hash"].encode("utf-8")
    )
    
    if not password_matches:
        return {
            "success": False,
            "message": "Invalid email or password."
        }

    payload = {
        "user_id": user["id"],
        "email": user["email"],
        "exp": datetime.utcnow() + timedelta(hours=24)
    }
    token = jwt.encode(
        payload,
        Config.SECRET_KEY,
        algorithm="HS256"
    )
    return {
        "success": True,
        "message": "Login successful.",
        "token": token
}