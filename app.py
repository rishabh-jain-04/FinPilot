from flask import Flask
from flask_cors import CORS

from config import Config
from api.health_routes import health_bp
from db.db import init_db

from api.auth_routes import auth_bp
from api.profile_routes import profile_bp
from api.finance_routes import finance_bp
from api.chat_routes import chat_bp

def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)
    init_db()

    CORS(app, origins=Config.CORS_ORIGINS)

    app.register_blueprint(health_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(profile_bp)
    app.register_blueprint(finance_bp)
    app.register_blueprint(chat_bp)

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)