from flask import Flask
from server.routes.auth import auth_bp
from server.routes.data import data_bp

def register_routes(app: Flask):
    """
    Register all route blueprints to the Flask app.

    This helps in keeping the main app configuration clean and modular.
    """
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(data_bp, url_prefix="/api/data")
