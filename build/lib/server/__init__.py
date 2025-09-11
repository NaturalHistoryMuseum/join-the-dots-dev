import os

from flask import Flask
from flask_jwt_extended import JWTManager

from server.config import Config
from server.extensions import cors
from server.register_routes import register_routes
from server.routes.auth import auth_bp


def create_app():
    # Allow insecure transport for testing purposes (for SSO) - DO NOT USE IN PRODUCTION!!
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    app = Flask(__name__)
    # Allows cross-origin requests from your Vue frontend
    cors.init_app(
        app,
        supports_credentials=True,
        expose_headers=["X-CSRF-TOKEN"],
        allow_headers=["Content-Type", "X-CSRF-TOKEN"],
    )
    app.config.from_object(Config)

    # Register blueprints (modular routes)
    register_routes(app)

    jwt = JWTManager(app)

    return app
