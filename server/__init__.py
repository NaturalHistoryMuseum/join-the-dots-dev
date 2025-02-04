from flask import Flask
from flask_cors import CORS
from server.config import Config
from server.database import get_db_connection, get_test_db_connection
from server.register_routes import register_routes
from flask_dance.contrib.azure import make_azure_blueprint
from server.routes.auth import auth_bp

import os
from dotenv import load_dotenv

load_dotenv()

def create_app():

    # Allow insecure transport for testing purposes (for SSO) - DO NOT USE IN PRODUCTION!!
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

    app = Flask(__name__)
    # Allows cross-origin requests from your Vue frontend
    CORS(app, supports_credentials=True)
    app.config.from_object(Config)

    # Initialize databases
    # with app.app_context():
    #     app.jtd_db = get_db_connection()
    #     app.test_db = get_test_db_connection()

    # Force load .env file
    load_dotenv(override=True)

    # Register blueprints (modular routes)
    register_routes(app)

    return app
