from flask import Flask

from config import Config
from routes.health_routes import health_bp


def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    app.register_blueprint(health_bp)

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)