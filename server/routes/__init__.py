from flask import Blueprint
from .data import data_bp
from .auth import auth_bp
from .user import user_bp

def register_routes(app):
    app.register_blueprint(data_bp, url_prefix='/api')
    app.register_blueprint(user_bp, url_prefix='/api/user')
    app.register_blueprint(auth_bp, url_prefix='/api/auth')