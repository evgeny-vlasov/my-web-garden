"""
Keystone Hardscapes Configuration
Site-specific configuration for the hardscaping business website.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Base configuration with defaults."""

    # Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-CHANGE-IN-PRODUCTION')
    FLASK_ENV = os.getenv('FLASK_ENV', 'production')

    # Database
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://localhost/keystone_db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,
        'pool_recycle': 300,
        'pool_size': 10,
        'max_overflow': 20
    }

    # Security
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    PERMANENT_SESSION_LIFETIME = 3600  # 1 hour
    WTF_CSRF_ENABLED = True
    WTF_CSRF_TIME_LIMIT = None  # No time limit on CSRF tokens

    # Upload settings
    MAX_CONTENT_LENGTH = int(os.getenv('MAX_UPLOAD_SIZE', 10485760))  # 10MB default for project photos
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', '/var/www/webgarden/uploads/keystone')
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

    # Mail settings (Mailgun)
    MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.mailgun.org')
    MAIL_PORT = int(os.getenv('MAIL_PORT', 587))
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER', 'info@keystonehardscapes.ca')
    ADMIN_EMAIL = os.getenv('ADMIN_EMAIL', os.getenv('MAIL_DEFAULT_SENDER', 'info@keystonehardscapes.ca'))

    # Site information
    SITE_NAME = os.getenv('SITE_NAME', 'Keystone Hardscapes')
    SITE_DOMAIN = os.getenv('SITE_DOMAIN', 'localhost')
    SITE_TAGLINE = 'Expert Craftsmanship. Lasting Quality.'
    BUSINESS_OWNER = 'Andrew'
    BUSINESS_PHONE = '587-573-6005'
    BUSINESS_EMAIL = 'info@keystonehardscapes.ca'
    SERVICE_AREA = 'Calgary, Airdrie, Cochrane, Okotoks, Chestermere'
    WARRANTY_YEARS = 5

    # Rate limiting
    RATELIMIT_ENABLED = True
    RATELIMIT_STORAGE_URL = 'memory://'
    CONTACT_FORM_RATE_LIMIT = '5 per hour'  # 5 quote requests per hour per IP


class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    FLASK_ENV = 'development'
    SESSION_COOKIE_SECURE = False  # Allow HTTP in development
    MAIL_SUPPRESS_SEND = False  # Actually send emails in dev (set to True to suppress)


class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    FLASK_ENV = 'production'
    # All security settings from base Config apply


class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/keystone_test_db'
    WTF_CSRF_ENABLED = False  # Disable CSRF for testing
    MAIL_SUPPRESS_SEND = True


# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': ProductionConfig
}
