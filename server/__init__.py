import logging
import os
import sys

from flask import Flask
from flask_jwt_extended import JWTManager

from server.config import get_config
from server.database import db
from server.extensions import cors, ma


def create_app():
    app = Flask(__name__)

    config_class = get_config()
    app.config.from_object(get_config())

    db.init_app(app)
    ma.init_app(app)

    if config_class.VITE_APP_ENV == 'dev':
        # Allow insecure transport for testing purposes (for SSO)
        os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

    # Ensure JSON responses are UTF-8 encoded
    app.json.ensure_ascii = False

    # Allows cross-origin requests from your Vue frontend
    cors.init_app(
        app,
        supports_credentials=True,
        expose_headers=['X-CSRF-TOKEN'],
        allow_headers=['Content-Type', 'X-CSRF-TOKEN'],
    )

    # Add logging
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(
        logging.Formatter('%(asctime)s %(levelname)s %(name)s: %(message)s')
    )
    app.logger.addHandler(handler)
    app.logger.setLevel(logging.INFO)

    # Register blueprints (modular routes)
    from server.register_routes import register_routes

    register_routes(app)

    jwt = JWTManager(app)

    return app
