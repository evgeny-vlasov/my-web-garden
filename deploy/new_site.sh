#!/bin/bash

################################################################################
# WebGarden Site Deployment Script
#
# Automates the deployment of a new Flask site on the WebGarden platform
#
# Usage: sudo ./new_site.sh <site_id> <domain> <port> <db_password>
# Example: sudo ./new_site.sh mysite mysite.example.com 8003 "SecurePass123!"
#
# Author: WebGarden Team
# Version: 1.0
################################################################################

set -e  # Exit on any error
set -u  # Exit on undefined variable

################################################################################
# Configuration
################################################################################

WEBGARDEN_ROOT="/var/www/webgarden/webgarden"
SITES_DIR="$WEBGARDEN_ROOT/sites"
UPLOAD_DIR="/var/www/webgarden/uploads"
TEMPLATES_DIR="$WEBGARDEN_ROOT/deploy/templates"
ENV_DIR="/etc/webgarden"
LOG_DIR="/var/log/webgarden"
NGINX_AVAILABLE="/etc/nginx/sites-available"
NGINX_ENABLED="/etc/nginx/sites-enabled"
SYSTEMD_DIR="/etc/systemd/system"
WEBGARDEN_USER="chip"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

################################################################################
# Helper Functions
################################################################################

log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

check_root() {
    if [[ $EUID -ne 0 ]]; then
        log_error "This script must be run as root (use sudo)"
        exit 1
    fi
}

check_prerequisites() {
    log_info "Checking prerequisites..."

    local missing_tools=()

    # Check for required commands
    for cmd in psql nginx systemctl certbot python3 pip3; do
        if ! command -v $cmd &> /dev/null; then
            missing_tools+=($cmd)
        fi
    done

    if [ ${#missing_tools[@]} -ne 0 ]; then
        log_error "Missing required tools: ${missing_tools[*]}"
        log_info "Install them with: apt-get install postgresql nginx python3 python3-pip python3-venv certbot python3-certbot-nginx"
        exit 1
    fi

    # Check if PostgreSQL is running
    if ! systemctl is-active --quiet postgresql; then
        log_error "PostgreSQL is not running. Start it with: systemctl start postgresql"
        exit 1
    fi

    # Check if Nginx is running
    if ! systemctl is-active --quiet nginx; then
        log_warning "Nginx is not running. Will start it later."
    fi

    # Check if user exists
    if ! id "$WEBGARDEN_USER" &>/dev/null; then
        log_error "User '$WEBGARDEN_USER' does not exist"
        exit 1
    fi

    log_success "All prerequisites met"
}

validate_inputs() {
    log_info "Validating inputs..."

    # Check if site already exists
    if [ -d "$SITES_DIR/$SITE_ID" ]; then
        log_error "Site directory already exists: $SITES_DIR/$SITE_ID"
        exit 1
    fi

    # Check if port is already in use
    if netstat -tuln | grep -q ":$PORT "; then
        log_error "Port $PORT is already in use"
        exit 1
    fi

    # Check if domain nginx config exists
    if [ -f "$NGINX_AVAILABLE/$SITE_ID" ]; then
        log_error "Nginx config already exists: $NGINX_AVAILABLE/$SITE_ID"
        exit 1
    fi

    # Check if systemd service exists
    if [ -f "$SYSTEMD_DIR/$SITE_ID.service" ]; then
        log_error "Systemd service already exists: $SYSTEMD_DIR/$SITE_ID.service"
        exit 1
    fi

    # Validate port number
    if ! [[ "$PORT" =~ ^[0-9]+$ ]] || [ "$PORT" -lt 1024 ] || [ "$PORT" -gt 65535 ]; then
        log_error "Invalid port number: $PORT (must be between 1024-65535)"
        exit 1
    fi

    log_success "Input validation passed"
}

generate_secret_key() {
    python3 -c "import secrets; print(secrets.token_hex(32))"
}

create_directories() {
    log_info "Creating directory structure..."

    # Create site directory
    mkdir -p "$SITES_DIR/$SITE_ID"/{static/{css,js,images},templates}

    # Create upload directory
    mkdir -p "$UPLOAD_DIR/$SITE_ID"

    # Create env directory if it doesn't exist
    mkdir -p "$ENV_DIR"

    # Create log directory if it doesn't exist
    mkdir -p "$LOG_DIR"

    log_success "Directory structure created"
}

create_env_file() {
    log_info "Generating .env file..."

    local secret_key=$(generate_secret_key)
    local mail_password=${MAIL_PASSWORD:-"your-mailgun-key"}
    local date=$(date '+%Y-%m-%d %H:%M:%S')

    # Read template and replace placeholders
    sed -e "s|{{SITE_NAME}}|$SITE_NAME|g" \
        -e "s|{{SITE_ID}}|$SITE_ID|g" \
        -e "s|{{DOMAIN}}|$DOMAIN|g" \
        -e "s|{{DB_NAME}}|$DB_NAME|g" \
        -e "s|{{DB_USER}}|$DB_USER|g" \
        -e "s|{{DB_PASSWORD}}|$DB_PASSWORD|g" \
        -e "s|{{SECRET_KEY}}|$secret_key|g" \
        -e "s|{{MAIL_PASSWORD}}|$mail_password|g" \
        -e "s|{{DATE}}|$date|g" \
        "$TEMPLATES_DIR/site.env.template" > "$ENV_DIR/$SITE_ID.env"

    # Set secure permissions
    chmod 600 "$ENV_DIR/$SITE_ID.env"

    log_success "Environment file created: $ENV_DIR/$SITE_ID.env"
}

create_database() {
    log_info "Creating PostgreSQL database and user..."

    # Check if database already exists
    if sudo -u postgres psql -lqt | cut -d \| -f 1 | grep -qw "$DB_NAME"; then
        log_warning "Database '$DB_NAME' already exists, skipping creation"
    else
        sudo -u postgres psql -c "CREATE DATABASE $DB_NAME;" 2>&1 | grep -v "already exists" || true
        log_success "Database created: $DB_NAME"
    fi

    # Check if user already exists
    if sudo -u postgres psql -tAc "SELECT 1 FROM pg_roles WHERE rolname='$DB_USER'" | grep -q 1; then
        log_warning "User '$DB_USER' already exists, updating password"
        sudo -u postgres psql -c "ALTER USER $DB_USER WITH PASSWORD '$DB_PASSWORD';"
    else
        sudo -u postgres psql -c "CREATE USER $DB_USER WITH PASSWORD '$DB_PASSWORD';" 2>&1 | grep -v "already exists" || true
        log_success "Database user created: $DB_USER"
    fi

    # Grant privileges
    sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;"
    sudo -u postgres psql -d "$DB_NAME" -c "GRANT ALL ON SCHEMA public TO $DB_USER;"

    log_success "Database setup complete"
}

create_nginx_config() {
    log_info "Creating Nginx configuration..."

    # Read template and replace placeholders
    sed -e "s|{{SITE_NAME}}|$SITE_NAME|g" \
        -e "s|{{SITE_ID}}|$SITE_ID|g" \
        -e "s|{{DOMAIN}}|$DOMAIN|g" \
        -e "s|{{PORT}}|$PORT|g" \
        "$TEMPLATES_DIR/nginx.conf.template" > "$NGINX_AVAILABLE/$SITE_ID"

    # Create symlink to enable site
    if [ ! -L "$NGINX_ENABLED/$SITE_ID" ]; then
        ln -s "$NGINX_AVAILABLE/$SITE_ID" "$NGINX_ENABLED/$SITE_ID"
    fi

    # Test nginx configuration
    if nginx -t 2>/dev/null; then
        log_success "Nginx configuration created and validated"
    else
        log_error "Nginx configuration test failed"
        nginx -t
        exit 1
    fi
}

create_systemd_service() {
    log_info "Creating systemd service..."

    # Read template and replace placeholders
    sed -e "s|{{SITE_NAME}}|$SITE_NAME|g" \
        -e "s|{{SITE_ID}}|$SITE_ID|g" \
        -e "s|{{PORT}}|$PORT|g" \
        -e "s|{{USER}}|$WEBGARDEN_USER|g" \
        "$TEMPLATES_DIR/systemd.service.template" > "$SYSTEMD_DIR/$SITE_ID.service"

    # Reload systemd
    systemctl daemon-reload

    log_success "Systemd service created: $SITE_ID.service"
}

create_basic_files() {
    log_info "Creating basic site files..."

    # Create __init__.py
    touch "$SITES_DIR/$SITE_ID/__init__.py"

    # Create config.py
    cat > "$SITES_DIR/$SITE_ID/config.py" <<'EOFCONFIG'
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
EOFCONFIG

    # Create minimal app.py
    cat > "$SITES_DIR/$SITE_ID/app.py" <<'EOFAPP'
"""
Flask Application
"""

import os
import sys
from datetime import datetime

# Add parent directories to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from flask import render_template
from dotenv import load_dotenv

load_dotenv()

# Import shared modules
from shared.base_app import create_base_app, db, login_manager
from shared.models import User
from config import config
from cli import register_cli_commands

# Create Flask application
config_name = os.getenv('FLASK_ENV', 'production')
app = create_base_app('CHANGEME', config[config_name])

# Register CLI commands
register_cli_commands(app)

# User loader for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    """Load user by ID for Flask-Login."""
    return User.query.get(int(user_id))

# Context processor
@app.context_processor
def inject_globals():
    """Inject global variables into all templates."""
    return {
        'current_year': datetime.now().year,
        'site_name': app.config['SITE_NAME']
    }

# Routes
@app.route('/')
def index():
    """Home page."""
    return render_template('index.html')

@app.route('/about')
def about():
    """About page."""
    return render_template('about.html')

@app.route('/contact')
def contact():
    """Contact page."""
    return render_template('contact.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=app.config['DEBUG'])
EOFAPP

    # Create cli.py (copy from keystone)
    cp "$SITES_DIR/keystone/cli.py" "$SITES_DIR/$SITE_ID/cli.py"

    # Create basic index.html
    cat > "$SITES_DIR/$SITE_ID/templates/index.html" <<'EOFHTML'
{% extends "base.html" %}

{% block title %}{{ site_name }}{% endblock %}

{% block content %}
<div class="container py-5">
    <div class="row">
        <div class="col-lg-8 mx-auto text-center">
            <h1 class="display-4 fw-bold mb-4">Welcome to {{ site_name }}</h1>
            <p class="lead mb-4">This is a new WebGarden site. Start customizing it with Claude Code!</p>
            <div class="d-flex gap-3 justify-content-center">
                <a href="{{ url_for('about') }}" class="btn btn-primary btn-lg">Learn More</a>
                <a href="{{ url_for('contact') }}" class="btn btn-outline-primary btn-lg">Contact Us</a>
            </div>
        </div>
    </div>
</div>
{% endblock %}
EOFHTML

    # Create basic about.html
    cat > "$SITES_DIR/$SITE_ID/templates/about.html" <<'EOFHTML'
{% extends "base.html" %}

{% block title %}About - {{ site_name }}{% endblock %}

{% block content %}
<div class="container py-5">
    <h1>About Us</h1>
    <p>Add your content here.</p>
</div>
{% endblock %}
EOFHTML

    # Create basic contact.html
    cat > "$SITES_DIR/$SITE_ID/templates/contact.html" <<'EOFHTML'
{% extends "base.html" %}

{% block title %}Contact - {{ site_name }}{% endblock %}

{% block content %}
<div class="container py-5">
    <h1>Contact Us</h1>
    <p>Add your contact form here.</p>
</div>
{% endblock %}
EOFHTML

    # Create basic CSS file
    cat > "$SITES_DIR/$SITE_ID/static/css/style.css" <<'EOFCSS'
/* Custom site styles */

:root {
    --primary-color: #007bff;
    --secondary-color: #6c757d;
}

/* Add your custom styles here */
EOFCSS

    # Create basic JS file
    cat > "$SITES_DIR/$SITE_ID/static/js/main.js" <<'EOFJS'
// Custom site JavaScript

document.addEventListener('DOMContentLoaded', function() {
    console.log('Site loaded successfully');
});
EOFJS

    log_success "Basic site files created"
}

setup_virtualenv() {
    log_info "Setting up Python virtual environment..."

    cd "$SITES_DIR/$SITE_ID"

    # Create virtual environment
    sudo -u "$WEBGARDEN_USER" python3 -m venv venv

    # Upgrade pip
    sudo -u "$WEBGARDEN_USER" venv/bin/pip install --upgrade pip

    # Install Flask and dependencies
    log_info "Installing Python dependencies..."
    sudo -u "$WEBGARDEN_USER" venv/bin/pip install \
        flask \
        flask-sqlalchemy \
        flask-login \
        flask-wtf \
        flask-migrate \
        flask-limiter \
        gunicorn \
        psycopg2-binary \
        python-dotenv \
        python-slugify \
        bleach \
        pillow \
        email-validator

    log_success "Virtual environment setup complete"
}

initialize_database() {
    log_info "Initializing database..."

    cd "$SITES_DIR/$SITE_ID"

    # Export environment variables
    export DATABASE_URL="postgresql://$DB_USER:$DB_PASSWORD@localhost/$DB_NAME"
    export FLASK_APP=app.py
    export FLASK_ENV=production

    # Initialize Flask-Migrate
    if [ ! -d "migrations" ]; then
        sudo -u "$WEBGARDEN_USER" -E venv/bin/flask db init
        log_success "Database migrations initialized"
    fi

    # Create initial migration
    sudo -u "$WEBGARDEN_USER" -E venv/bin/flask db migrate -m "Initial migration"

    # Apply migration
    sudo -u "$WEBGARDEN_USER" -E venv/bin/flask db upgrade

    log_success "Database initialized"
}

create_admin_user() {
    log_info "Admin user creation..."

    read -p "Do you want to create an admin user now? (y/n): " -n 1 -r
    echo

    if [[ $REPLY =~ ^[Yy]$ ]]; then
        cd "$SITES_DIR/$SITE_ID"

        export DATABASE_URL="postgresql://$DB_USER:$DB_PASSWORD@localhost/$DB_NAME"
        export FLASK_APP=app.py
        export FLASK_ENV=production

        sudo -u "$WEBGARDEN_USER" -E venv/bin/flask create-admin

        log_success "Admin user created"
    else
        log_warning "Skipped admin user creation. You can create one later with:"
        log_warning "cd $SITES_DIR/$SITE_ID && venv/bin/flask create-admin"
    fi
}

set_permissions() {
    log_info "Setting file permissions..."

    # Set ownership
    chown -R "$WEBGARDEN_USER:$WEBGARDEN_USER" "$SITES_DIR/$SITE_ID"
    chown -R "$WEBGARDEN_USER:$WEBGARDEN_USER" "$UPLOAD_DIR/$SITE_ID"
    chown -R "$WEBGARDEN_USER:$WEBGARDEN_USER" "$LOG_DIR"

    # Set directory permissions
    find "$SITES_DIR/$SITE_ID" -type d -exec chmod 755 {} \;
    find "$SITES_DIR/$SITE_ID" -type f -exec chmod 644 {} \;

    # Make venv scripts executable
    if [ -d "$SITES_DIR/$SITE_ID/venv/bin" ]; then
        chmod +x "$SITES_DIR/$SITE_ID/venv/bin/"*
    fi

    log_success "Permissions set"
}

start_services() {
    log_info "Starting services..."

    # Enable and start systemd service
    systemctl enable "$SITE_ID.service"
    systemctl start "$SITE_ID.service"

    # Check if service started successfully
    sleep 2
    if systemctl is-active --quiet "$SITE_ID.service"; then
        log_success "Service started: $SITE_ID.service"
    else
        log_error "Service failed to start. Check logs with: journalctl -u $SITE_ID.service"
        exit 1
    fi

    # Reload and restart nginx
    systemctl reload nginx

    log_success "Services started"
}

setup_ssl() {
    log_info "SSL Certificate setup..."

    read -p "Do you want to set up SSL with Let's Encrypt now? (y/n): " -n 1 -r
    echo

    if [[ $REPLY =~ ^[Yy]$ ]]; then
        log_info "Running certbot..."
        certbot --nginx -d "$DOMAIN"

        if [ $? -eq 0 ]; then
            log_success "SSL certificate obtained and configured"
        else
            log_warning "SSL setup failed or was cancelled. You can run it later with:"
            log_warning "certbot --nginx -d $DOMAIN"
        fi
    else
        log_warning "Skipped SSL setup. You can run it later with:"
        log_warning "certbot --nginx -d $DOMAIN"
    fi
}

print_summary() {
    echo ""
    echo "================================================================================"
    log_success "Site deployment complete!"
    echo "================================================================================"
    echo ""
    echo "Site Details:"
    echo "  Site ID:       $SITE_ID"
    echo "  Site Name:     $SITE_NAME"
    echo "  Domain:        $DOMAIN"
    echo "  Port:          $PORT"
    echo "  Database:      $DB_NAME"
    echo ""
    echo "Directories:"
    echo "  Site:          $SITES_DIR/$SITE_ID"
    echo "  Uploads:       $UPLOAD_DIR/$SITE_ID"
    echo "  Logs:          $LOG_DIR"
    echo ""
    echo "Configuration Files:"
    echo "  Environment:   $ENV_DIR/$SITE_ID.env"
    echo "  Nginx:         $NGINX_AVAILABLE/$SITE_ID"
    echo "  Systemd:       $SYSTEMD_DIR/$SITE_ID.service"
    echo ""
    echo "Useful Commands:"
    echo "  View logs:     journalctl -u $SITE_ID.service -f"
    echo "  Restart:       systemctl restart $SITE_ID.service"
    echo "  Status:        systemctl status $SITE_ID.service"
    echo "  Create admin:  cd $SITES_DIR/$SITE_ID && venv/bin/flask create-admin"
    echo ""
    echo "Next Steps:"
    echo "  1. Update DNS to point $DOMAIN to this server"
    echo "  2. Customize the site using Claude Code (see deploy/SITE_CREATION_PROMPT.md)"
    echo "  3. Test the site at http://$DOMAIN or http://$(hostname -I | awk '{print $1}'):$PORT"
    echo ""
    echo "================================================================================"
}

################################################################################
# Main Script
################################################################################

main() {
    echo "================================================================================"
    echo "                    WebGarden Site Deployment Script"
    echo "================================================================================"
    echo ""

    # Check if running as root
    check_root

    # Parse arguments
    if [ $# -lt 4 ]; then
        log_error "Usage: $0 <site_id> <domain> <port> <db_password> [site_name]"
        echo ""
        echo "Arguments:"
        echo "  site_id      - Short identifier (e.g., 'mysite', used for directories/configs)"
        echo "  domain       - Full domain name (e.g., 'mysite.example.com')"
        echo "  port         - Port number (e.g., 8003)"
        echo "  db_password  - PostgreSQL password for site database"
        echo "  site_name    - Display name (optional, defaults to site_id)"
        echo ""
        echo "Example:"
        echo "  $0 mysite mysite.example.com 8003 'SecurePass123!' 'My Awesome Site'"
        exit 1
    fi

    SITE_ID="$1"
    DOMAIN="$2"
    PORT="$3"
    DB_PASSWORD="$4"
    SITE_NAME="${5:-$SITE_ID}"

    # Derived variables
    DB_NAME="${SITE_ID}_db"
    DB_USER="${SITE_ID}_user"

    log_info "Deploying site: $SITE_NAME"
    log_info "Site ID: $SITE_ID"
    log_info "Domain: $DOMAIN"
    log_info "Port: $PORT"
    echo ""

    # Run deployment steps
    check_prerequisites
    validate_inputs
    create_directories
    create_env_file
    create_database
    create_basic_files
    setup_virtualenv
    create_nginx_config
    create_systemd_service
    set_permissions
    initialize_database
    create_admin_user
    start_services
    setup_ssl

    # Print summary
    print_summary
}

# Run main function
main "$@"
