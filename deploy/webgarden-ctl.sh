#!/bin/bash
#
# WebGarden Control Script
# Manage WebGarden site services
#
# Usage: webgarden-ctl {start|stop|restart|status|logs|reload} {site-name}
#
# Examples:
#   webgarden-ctl restart therapist
#   webgarden-ctl status therapist
#   webgarden-ctl logs therapist
#   webgarden-ctl logs therapist -f  (follow logs)

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
WEBGARDEN_ROOT="/var/www/webgarden"
LOG_DIR="/var/log/webgarden"

# Print colored message
print_message() {
    local color=$1
    shift
    echo -e "${color}$@${NC}"
}

# Print usage
usage() {
    cat << EOF
WebGarden Control Script

Usage: $(basename $0) {start|stop|restart|reload|status|logs} {site-name} [options]

Commands:
  start       Start the site service
  stop        Stop the site service
  restart     Restart the site service
  reload      Reload the site service (graceful restart)
  status      Show service status
  logs        View service logs

Sites:
  therapist   Therapist psychotherapy site
  handyman    Handyman business site (coming soon)
  lab         Computer lab site (coming soon)

Examples:
  $(basename $0) start therapist
  $(basename $0) restart therapist
  $(basename $0) status therapist
  $(basename $0) logs therapist
  $(basename $0) logs therapist -f    # Follow logs in real-time

EOF
    exit 1
}

# Check if running as root or with sudo
check_privileges() {
    if [[ $EUID -ne 0 ]] && ! groups | grep -q webgarden; then
        print_message "$RED" "Error: This script must be run as root, with sudo, or as webgarden user"
        exit 1
    fi
}

# Validate site name
validate_site() {
    local site=$1
    case $site in
        therapist|handyman|lab)
            return 0
            ;;
        *)
            print_message "$RED" "Error: Invalid site name '$site'"
            print_message "$YELLOW" "Valid sites: therapist, handyman, lab"
            exit 1
            ;;
    esac
}

# Get service name
get_service_name() {
    echo "webgarden-$1.service"
}

# Start service
start_site() {
    local site=$1
    local service=$(get_service_name $site)

    print_message "$BLUE" "Starting $site site..."
    systemctl start $service

    if systemctl is-active --quiet $service; then
        print_message "$GREEN" "✓ $site site started successfully"
    else
        print_message "$RED" "✗ Failed to start $site site"
        print_message "$YELLOW" "Check logs: journalctl -u $service -n 50"
        exit 1
    fi
}

# Stop service
stop_site() {
    local site=$1
    local service=$(get_service_name $site)

    print_message "$BLUE" "Stopping $site site..."
    systemctl stop $service

    if ! systemctl is-active --quiet $service; then
        print_message "$GREEN" "✓ $site site stopped successfully"
    else
        print_message "$RED" "✗ Failed to stop $site site"
        exit 1
    fi
}

# Restart service
restart_site() {
    local site=$1
    local service=$(get_service_name $site)

    print_message "$BLUE" "Restarting $site site..."
    systemctl restart $service

    if systemctl is-active --quiet $service; then
        print_message "$GREEN" "✓ $site site restarted successfully"
    else
        print_message "$RED" "✗ Failed to restart $site site"
        print_message "$YELLOW" "Check logs: journalctl -u $service -n 50"
        exit 1
    fi
}

# Reload service (graceful restart)
reload_site() {
    local site=$1
    local service=$(get_service_name $site)

    print_message "$BLUE" "Reloading $site site (graceful restart)..."
    systemctl reload-or-restart $service

    if systemctl is-active --quiet $service; then
        print_message "$GREEN" "✓ $site site reloaded successfully"
    else
        print_message "$RED" "✗ Failed to reload $site site"
        exit 1
    fi
}

# Show service status
status_site() {
    local site=$1
    local service=$(get_service_name $site)

    print_message "$BLUE" "Status for $site site:"
    systemctl status $service --no-pager
}

# View service logs
logs_site() {
    local site=$1
    local service=$(get_service_name $site)
    shift

    # Pass additional arguments to journalctl (e.g., -f for follow)
    print_message "$BLUE" "Logs for $site site:"
    journalctl -u $service "$@"
}

# Main script
main() {
    if [[ $# -lt 2 ]]; then
        usage
    fi

    local command=$1
    local site=$2
    shift 2

    # Validate inputs
    validate_site $site
    check_privileges

    # Execute command
    case $command in
        start)
            start_site $site
            ;;
        stop)
            stop_site $site
            ;;
        restart)
            restart_site $site
            ;;
        reload)
            reload_site $site
            ;;
        status)
            status_site $site
            ;;
        logs)
            logs_site $site "$@"
            ;;
        *)
            print_message "$RED" "Error: Unknown command '$command'"
            usage
            ;;
    esac
}

# Run main function
main "$@"
