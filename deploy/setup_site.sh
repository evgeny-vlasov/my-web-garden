#!/bin/bash
#
# WebGarden Site Setup Script
# Automated setup for new WebGarden sites
#
# Usage: sudo ./setup_site.sh {site-name} {domain}
#
# Example: sudo ./setup_site.sh therapist therapist.example.com

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Configuration
WEBGARDEN_ROOT="/var/www/webgarden"
WEBGARDEN_USER="webgarden"
WEBGARDEN_GROUP="webgarden"
LOG_DIR="/var/log/webgarden"
RUN_DIR="/var/run/webgarden"
CONFIG_DIR="/etc/webgarden"

# Print colored message
print_message() {
    local color=$1
    shift
    echo -e "${color}$@${NC}"
}

# Print step header
print_step() {
    echo ""
    print_message "$BLUE" "═══════════════════════════════════════════════════════"
    print_message "$BLUE" "  $1"
    print_message "$BLUE" "═══════════════════════════════════════════════════════"
}

# Check if running as root
check_root() {
    if [[ $EUID -ne 0 ]]; then
        print_message "$RED" "Error: This script must be run as root (use sudo)"
        exit 1
    fi
}

# Usage
usage() {
    cat << EOF
WebGarden Site Setup Script

Usage: sudo $(basename $0) {site-name} {domain}

Arguments:
  site-name    Name of the site (e.g., therapist, handyman, lab)
  domain       Domain name for the site (e.g., therapist.example.com)

Example:
  sudo $(basename $0) therapist therapist.example.com

This script will:
  1. Create system user and directories
  2. Create PostgreSQL database and user
  3. Set up Python virtual environment
  4. Install dependencies
  5. Initialize database
  6. Configure environment variables
  7. Set up nginx configuration
  8. Set up systemd service
  9. Obtain SSL certificate
  10. Enable and start service

EOF
    exit 1
}

# Create system user
create_user() {
    print_step "Creating system user: $WEBGARDEN_USER"

    if id "$WEBGARDEN_USER" &>/dev/null; then
        print_message "$YELLOW" "User $WEBGARDEN_USER already exists, skipping..."
    else
        useradd -r -s /bin/bash -d "$WEBGARDEN_ROOT" -m "$WEBGARDEN_USER"
        print_message "$GREEN" "✓ User $WEBGARDEN_USER created"
    fi
}

# Create directories
create_directories() {
    print_step "Creating directories"

    mkdir -p "$LOG_DIR"
    mkdir -p "$RUN_DIR"
    mkdir -p "$CONFIG_DIR"
    mkdir -p "$WEBGARDEN_ROOT/uploads/$SITE_NAME"
    mkdir -p "$WEBGARDEN_ROOT/backups/databases"
    mkdir -p "$WEBGARDEN_ROOT/backups/uploads"

    chown -R $WEBGARDEN_USER:$WEBGARDEN_GROUP "$WEBGARDEN_ROOT"
    chown -R $WEBGARDEN_USER:$WEBGARDEN_GROUP "$LOG_DIR"
    chown -R $WEBGARDEN_USER:$WEBGARDEN_GROUP "$RUN_DIR"
    chmod 755 "$WEBGARDEN_ROOT"
    chmod 755 "$LOG_DIR"
    chmod 755 "$RUN_DIR"

    print_message "$GREEN" "✓ Directories created"
}

# Create database
create_database() {
    print_step "Creating PostgreSQL database"

    local db_name="${SITE_NAME}_db"
    local db_user="${SITE_NAME}_user"
    local db_pass=$(openssl rand -base64 32)

    # Check if database exists
    if sudo -u postgres psql -lqt | cut -d \| -f 1 | grep -qw "$db_name"; then
        print_message "$YELLOW" "Database $db_name already exists, skipping..."
        print_message "$YELLOW" "If you need to reset the database, run: sudo -u postgres dropdb $db_name"
        return
    fi

    # Create database and user
    sudo -u postgres psql << EOF
CREATE DATABASE ${db_name};
CREATE USER ${db_user} WITH ENCRYPTED PASSWORD '${db_pass}';
GRANT ALL PRIVILEGES ON DATABASE ${db_name} TO ${db_user};
\c ${db_name}
GRANT ALL ON SCHEMA public TO ${db_user};
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO ${db_user};
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO ${db_user};
EOF

    print_message "$GREEN" "✓ Database created: $db_name"
    print_message "$GREEN" "✓ Database user created: $db_user"
    print_message "$YELLOW" "Database password: $db_pass"
    print_message "$YELLOW" "Save this password! It will be written to the .env file."

    # Store credentials for env file
    DB_URL="postgresql://${db_user}:${db_pass}@localhost/${db_name}"
}

# Set up virtual environment
setup_venv() {
    print_step "Setting up Python virtual environment"

    local site_dir="$WEBGARDEN_ROOT/sites/$SITE_NAME"
    local venv_dir="$site_dir/venv"

    if [[ -d "$venv_dir" ]]; then
        print_message "$YELLOW" "Virtual environment already exists, recreating..."
        rm -rf "$venv_dir"
    fi

    sudo -u $WEBGARDEN_USER python3 -m venv "$venv_dir"
    sudo -u $WEBGARDEN_USER "$venv_dir/bin/pip" install --upgrade pip wheel
    sudo -u $WEBGARDEN_USER "$venv_dir/bin/pip" install -r "$site_dir/requirements.txt"

    print_message "$GREEN" "✓ Virtual environment created and dependencies installed"
}

# Configure environment
configure_env() {
    print_step "Configuring environment variables"

    local env_file="$CONFIG_DIR/$SITE_NAME.env"
    local secret_key=$(openssl rand -base64 48)

    cat > "$env_file" << EOF
# WebGarden $SITE_NAME Site Environment Configuration
# Generated: $(date)

# Flask
SECRET_KEY=$secret_key
FLASK_ENV=production

# Database
DATABASE_URL=$DB_URL

# Mail (Mailgun) - CONFIGURE THESE
MAIL_SERVER=smtp.mailgun.org
MAIL_PORT=587
MAIL_USERNAME=postmaster@$DOMAIN
MAIL_PASSWORD=YOUR_MAILGUN_API_KEY
MAIL_DEFAULT_SENDER=info@$DOMAIN
ADMIN_EMAIL=admin@$DOMAIN

# Site
SITE_NAME=Professional Psychotherapy
SITE_DOMAIN=$DOMAIN
UPLOAD_FOLDER=$WEBGARDEN_ROOT/uploads/$SITE_NAME
MAX_UPLOAD_SIZE=5242880

# Office Info - UPDATE THESE
OFFICE_PHONE=(416) 555-0100
OFFICE_EMAIL=info@$DOMAIN
EOF

    chmod 600 "$env_file"
    chown $WEBGARDEN_USER:$WEBGARDEN_GROUP "$env_file"

    print_message "$GREEN" "✓ Environment file created: $env_file"
    print_message "$YELLOW" "Remember to update mail settings in $env_file"
}

# Initialize database
init_database() {
    print_step "Initializing database"

    local site_dir="$WEBGARDEN_ROOT/sites/$SITE_NAME"
    cd "$site_dir"

    # Source env file and run migrations
    export $(grep -v '^#' "$CONFIG_DIR/$SITE_NAME.env" | xargs)

    sudo -u $WEBGARDEN_USER "$site_dir/venv/bin/flask" db init || true
    sudo -u $WEBGARDEN_USER "$site_dir/venv/bin/flask" db migrate -m "Initial migration" || true
    sudo -u $WEBGARDEN_USER "$site_dir/venv/bin/flask" db upgrade

    print_message "$GREEN" "✓ Database initialized"
}

# Configure nginx
configure_nginx() {
    print_step "Configuring nginx"

    local nginx_conf="/etc/nginx/sites-available/$SITE_NAME"
    local source_conf="$WEBGARDEN_ROOT/deploy/nginx/$SITE_NAME.conf"

    # Copy and update nginx config
    cp "$source_conf" "$nginx_conf"
    sed -i "s/therapist\.example\.com/$DOMAIN/g" "$nginx_conf"
    sed -i "s/www\.therapist\.example\.com/www.$DOMAIN/g" "$nginx_conf"

    # Enable site
    ln -sf "$nginx_conf" "/etc/nginx/sites-enabled/$SITE_NAME"

    # Test nginx config
    nginx -t

    print_message "$GREEN" "✓ Nginx configured"
}

# Configure systemd
configure_systemd() {
    print_step "Configuring systemd service"

    local service_file="/etc/systemd/system/webgarden-$SITE_NAME.service"
    local source_service="$WEBGARDEN_ROOT/deploy/systemd/webgarden-$SITE_NAME.service"

    cp "$source_service" "$service_file"

    systemctl daemon-reload
    systemctl enable "webgarden-$SITE_NAME.service"

    print_message "$GREEN" "✓ Systemd service configured and enabled"
}

# Obtain SSL certificate
obtain_ssl() {
    print_step "Obtaining SSL certificate"

    print_message "$YELLOW" "About to request SSL certificate from Let's Encrypt..."
    print_message "$YELLOW" "Make sure:"
    print_message "$YELLOW" "  1. DNS records for $DOMAIN point to this server"
    print_message "$YELLOW" "  2. Ports 80 and 443 are open"

    read -p "Continue with SSL setup? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        print_message "$YELLOW" "Skipping SSL setup. Run manually later:"
        print_message "$YELLOW" "  sudo certbot --nginx -d $DOMAIN -d www.$DOMAIN"
        return
    fi

    certbot --nginx -d "$DOMAIN" -d "www.$DOMAIN" --non-interactive --agree-tos --email "admin@$DOMAIN"

    print_message "$GREEN" "✓ SSL certificate obtained"
}

# Start service
start_service() {
    print_step "Starting service"

    systemctl restart "webgarden-$SITE_NAME.service"
    systemctl reload nginx

    print_message "$GREEN" "✓ Service started"
}

# Print summary
print_summary() {
    print_step "Setup Complete!"

    cat << EOF

${GREEN}✓ $SITE_NAME site has been set up successfully!${NC}

${BLUE}Service Management:${NC}
  Start:   sudo systemctl start webgarden-$SITE_NAME
  Stop:    sudo systemctl stop webgarden-$SITE_NAME
  Restart: sudo systemctl restart webgarden-$SITE_NAME
  Status:  sudo systemctl status webgarden-$SITE_NAME
  Logs:    sudo journalctl -u webgarden-$SITE_NAME -f

  Or use: sudo $WEBGARDEN_ROOT/deploy/webgarden-ctl.sh {command} $SITE_NAME

${BLUE}Site Information:${NC}
  URL:     https://$DOMAIN
  Root:    $WEBGARDEN_ROOT/sites/$SITE_NAME
  Uploads: $WEBGARDEN_ROOT/uploads/$SITE_NAME
  Logs:    $LOG_DIR

${BLUE}Configuration Files:${NC}
  Environment: $CONFIG_DIR/$SITE_NAME.env
  Nginx:       /etc/nginx/sites-available/$SITE_NAME
  Systemd:     /etc/systemd/system/webgarden-$SITE_NAME.service

${YELLOW}Next Steps:${NC}
  1. Update mail settings in $CONFIG_DIR/$SITE_NAME.env
  2. Update office info in $CONFIG_DIR/$SITE_NAME.env
  3. Create admin user: cd $WEBGARDEN_ROOT/sites/$SITE_NAME && sudo -u $WEBGARDEN_USER venv/bin/flask create-admin
  4. Visit https://$DOMAIN to test

EOF
}

# Main
main() {
    check_root

    if [[ $# -lt 2 ]]; then
        usage
    fi

    SITE_NAME=$1
    DOMAIN=$2

    print_message "$GREEN" "WebGarden Site Setup"
    print_message "$GREEN" "Site: $SITE_NAME"
    print_message "$GREEN" "Domain: $DOMAIN"

    # Check if PostgreSQL is installed
    if ! command -v psql &> /dev/null; then
        print_message "$RED" "Error: PostgreSQL is not installed"
        print_message "$YELLOW" "Install it with: sudo apt install postgresql"
        exit 1
    fi

    # Check if Python 3 is installed
    if ! command -v python3 &> /dev/null; then
        print_message "$RED" "Error: Python 3 is not installed"
        exit 1
    fi

    # Check if certbot is installed
    if ! command -v certbot &> /dev/null; then
        print_message "$YELLOW" "Warning: certbot is not installed. SSL setup will be skipped."
        print_message "$YELLOW" "Install it with: sudo apt install certbot python3-certbot-nginx"
    fi

    # Run setup steps
    create_user
    create_directories
    create_database
    setup_venv
    configure_env
    init_database
    configure_nginx
    configure_systemd
    obtain_ssl
    start_service
    print_summary
}

main "$@"
