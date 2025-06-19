import os

from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS

from server.config import Config
from server.register_routes import register_routes
from server.routes.auth import auth_bp

load_dotenv()


def create_app():
    # Allow insecure transport for testing purposes (for SSO) - DO NOT USE IN PRODUCTION!!
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

    app = Flask(__name__)
    # Allows cross-origin requests from your Vue frontend
    CORS(app, supports_credentials=True)
    app.config.from_object(Config)

    # Force load .env file
    load_dotenv(override=True)

    # Register blueprints (modular routes)
    register_routes(app)

    return app
