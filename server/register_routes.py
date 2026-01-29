from flask import Flask

from server.config import get_config
from server.routes.data import data_bp
from server.routes.export import export_bp
from server.routes.powerbi import powerbi_bp
from server.routes.report import report_bp
from server.routes.stats import stats_bp
from server.routes.user import user_bp


def register_routes(app: Flask):
    """
    Register all route blueprints to the Flask app.

    This helps in keeping the main app configuration clean and modular.
    """

    app.register_blueprint(data_bp, url_prefix='/api/data')
    app.register_blueprint(user_bp, url_prefix='/api/user')
    app.register_blueprint(report_bp, url_prefix='/api/report')
    app.register_blueprint(stats_bp, url_prefix='/api/stats')
    app.register_blueprint(powerbi_bp, url_prefix='/api/powerbi')
    app.register_blueprint(export_bp, url_prefix='/api/export')
    # Register test auth routes only if testing mode is enabled
    if get_config().TEST_AUTH_ENABLED:
        from server.routes.auth_test import auth_test_bp

        app.register_blueprint(auth_test_bp, url_prefix='/api/auth_test')
    else:
        from server.routes.auth import auth_bp

        app.register_blueprint(auth_bp, url_prefix='/api/auth')
