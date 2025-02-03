from flask import Flask
from flask_cors import CORS
from server.config import Config
from server.database import get_db_connection, get_test_db_connection
from server.register_routes import register_routes
from flask_dance.contrib.azure import make_azure_blueprint

import os
from dotenv import load_dotenv

load_dotenv()

def create_app():
    app = Flask(__name__)
    # Allows cross-origin requests from your Vue frontend
    CORS(app)
    app.config.from_object(Config)

    # Initialize databases
    with app.app_context():
        app.jtd_db = get_db_connection()
    #     app.test_db = get_test_db_connection()

    # Force load .env file
    load_dotenv(override=True)

    # Register blueprints (modular routes)
    register_routes(app)

    # Azure AD OAuth
    azure_blueprint = make_azure_blueprint(
        client_id=app.config["AZURE_CLIENT_ID"],
        client_secret=app.config["AZURE_CLIENT_SECRET"],
        tenant=app.config["AZURE_TENANT_ID"],
        redirect_url=app.config["AZURE_REDIRECT_URI"],
    )
    app.register_blueprint(azure_blueprint, url_prefix="/api/auth/login")

    return app
