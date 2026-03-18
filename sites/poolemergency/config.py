"""
Site Configuration
"""

import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Base configuration with defaults."""

    # Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-CHANGE-IN-PRODUCTION')
    FLASK_ENV = os.getenv('FLASK_ENV', 'production')

    # Database
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
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
    PERMANENT_SESSION_LIFETIME = 3600
    WTF_CSRF_ENABLED = True
    WTF_CSRF_TIME_LIMIT = None

    # Upload settings
    MAX_CONTENT_LENGTH = int(os.getenv('MAX_UPLOAD_SIZE', 10485760))
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER')
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

    # Mail settings
    MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.mailgun.org')
    MAIL_PORT = int(os.getenv('MAIL_PORT', 587))
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER')
    ADMIN_EMAIL = os.getenv('ADMIN_EMAIL')

    # Site information
    SITE_NAME = os.getenv('SITE_NAME')
    SITE_DOMAIN = os.getenv('SITE_DOMAIN')

    # Rate limiting
    RATELIMIT_ENABLED = True
    RATELIMIT_STORAGE_URL = 'memory://'
    CONTACT_FORM_RATE_LIMIT = '5 per hour'

class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    FLASK_ENV = 'development'
    SESSION_COOKIE_SECURE = False

class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    FLASK_ENV = 'production'

class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    WTF_CSRF_ENABLED = False
    MAIL_SUPPRESS_SEND = True

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': ProductionConfig
}
