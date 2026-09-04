from flask import Flask, current_app
from sqlalchemy.exc import (
    IntegrityError,
    OperationalError,
    SQLAlchemyError,
    TimeoutError,
)

from server.config import get_config
from server.database import db
from server.routes.data import data_bp
from server.routes.export import export_bp
from server.routes.powerbi import powerbi_bp
from server.routes.user import user_bp
from server.utils import refresh_jwt_token


def register_routes(app: Flask):
    """Register all route blueprints to the Flask app.

    This helps in keeping the main app configuration clean and modular.
    Register the JWT token refresh and global error handlers for db
    errors.
    """
    # Refresh jwt token after request is made
    app.after_request(refresh_jwt_token)

    # Add global error catchers
    @app.errorhandler(OperationalError)
    def handle_operational_error(error):
        db.session.rollback()
        current_app.logger.error(
            'Database operational error: %s', str(error), exc_info=True
        )
        return {
            'error': """Database operational error.
            Database could be temporarily unavailable."""
        }, 503

    @app.errorhandler(IntegrityError)
    def handle_integrity_error(error):
        db.session.rollback()
        current_app.logger.error(
            'Database integrity error: %s', str(error), exc_info=True
        )
        return {'error': 'Request voilates database constraints.'}, 409

    @app.errorhandler(TimeoutError)
    def handle_timeout_error(error):
        db.session.rollback()
        current_app.logger.error('Request timeout: %s', str(error), exc_info=True)
        return {'error': 'Request timed out.'}, 408

    @app.errorhandler(SQLAlchemyError)
    def handle_sqlalchemy_error(error):
        db.session.rollback()
        current_app.logger.error('SQLAlchemy error: %s', str(error), exc_info=True)
        return {'error': 'An error occured while processing this request.'}, 500

    # Register routes
    app.register_blueprint(data_bp, url_prefix='/api/data')
    app.register_blueprint(user_bp, url_prefix='/api/user')
    app.register_blueprint(powerbi_bp, url_prefix='/api/powerbi')
    app.register_blueprint(export_bp, url_prefix='/api/export')
    # Register test auth routes only if testing mode is enabled
    if get_config().TEST_AUTH_ENABLED:
        from server.routes.auth_test import auth_test_bp

        app.register_blueprint(auth_test_bp, url_prefix='/api/auth_test')
    else:
        from server.routes.auth import auth_bp

        app.register_blueprint(auth_bp, url_prefix='/api/auth')
