import os
import sys

from flask import Flask
from flask_jwt_extended import JWTManager

from server.config import get_config
from server.extensions import cors


def create_app():
    # Allow insecure transport for testing purposes (for SSO) - DO NOT USE IN PRODUCTION!!
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

    app = Flask(__name__)

    config_class = get_config()
    app.config.from_object(get_config())

    # Allows cross-origin requests from your Vue frontend
    cors.init_app(
        app,
        supports_credentials=True,
        expose_headers=['X-CSRF-TOKEN'],
        allow_headers=['Content-Type', 'X-CSRF-TOKEN'],
    )

    # Register blueprints (modular routes)
    from server.register_routes import register_routes

    register_routes(app)

    jwt = JWTManager(app)

    return app
