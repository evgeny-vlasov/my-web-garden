"""
Base Flask Application Factory
Provides common configuration and initialization for all WebGarden sites.
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_mail import Mail
from flask_wtf.csrf import CSRFProtect
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import os

# Initialize extensions (without app context)
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
bcrypt = Bcrypt()
mail = Mail()
csrf = CSRFProtect()
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["100 per minute"],
    storage_uri="memory://"
)


def create_base_app(site_name, config_object=None):
    """
    Create and configure a Flask application instance.

    Args:
        site_name: Name of the site (e.g., 'therapist', 'handyman')
        config_object: Configuration object/class to load

    Returns:
        Configured Flask application instance
    """
    app = Flask(
        site_name,
        template_folder='templates',
        static_folder='static'
    )

    # Load configuration
    if config_object:
        app.config.from_object(config_object)
    else:
        # Load from environment variables
        app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
        app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
            'pool_pre_ping': True,
            'pool_recycle': 300,
        }

    # Security configurations
    app.config['SESSION_COOKIE_SECURE'] = True
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
    app.config['PERMANENT_SESSION_LIFETIME'] = 3600  # 1 hour

    # Upload configurations
    app.config['MAX_CONTENT_LENGTH'] = int(os.getenv('MAX_UPLOAD_SIZE', 5242880))  # 5MB default
    app.config['UPLOAD_FOLDER'] = os.getenv('UPLOAD_FOLDER', f'/var/www/webgarden/uploads/{site_name}')

    # Mail configurations
    app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER', 'smtp.mailgun.org')
    app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', 587))
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
    app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER')

    # Site-specific configurations
    app.config['SITE_NAME'] = os.getenv('SITE_NAME', site_name.title())
    app.config['SITE_DOMAIN'] = os.getenv('SITE_DOMAIN', 'localhost')

    # Initialize extensions with app
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    mail.init_app(app)
    csrf.init_app(app)
    limiter.init_app(app)

    # Configure login manager
    login_manager.login_view = 'admin.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'info'

    # Register error handlers
    register_error_handlers(app)

    # Register template filters
    register_template_filters(app)

    return app


def register_error_handlers(app):
    """Register error handlers for common HTTP errors."""

    @app.errorhandler(404)
    def not_found_error(error):
        return app.send_static_file('errors/404.html') if os.path.exists(
            os.path.join(app.static_folder, 'errors/404.html')
        ) else ('Page not found', 404)

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return app.send_static_file('errors/500.html') if os.path.exists(
            os.path.join(app.static_folder, 'errors/500.html')
        ) else ('Internal server error', 500)

    @app.errorhandler(403)
    def forbidden_error(error):
        return ('Access forbidden', 403)

    @app.errorhandler(413)
    def request_entity_too_large(error):
        return ('File too large', 413)


def register_template_filters(app):
    """Register custom Jinja2 template filters."""

    @app.template_filter('datetime')
    def format_datetime(value, format='%Y-%m-%d %H:%M'):
        """Format a datetime object."""
        if value is None:
            return ""
        return value.strftime(format)

    @app.template_filter('date')
    def format_date(value, format='%Y-%m-%d'):
        """Format a date object."""
        if value is None:
            return ""
        return value.strftime(format)
