from flask import Blueprint
from .data import data_bp
from .auth import auth_bp
from .user import user_bp
from .stats import stats_bp

def register_routes(app):
    app.register_blueprint(data_bp, url_prefix='/api')
    app.register_blueprint(user_bp, url_prefix='/api/user')
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(stats_bp, url_prefix='/api/stats')