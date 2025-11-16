# WebGarden Deployment System

Complete automation for deploying new Flask sites on the WebGarden multi-site hosting platform.

## Quick Start

Deploy a new site in 15 minutes with just two steps:

1. **Run the deployment script** to set up infrastructure
2. **Use Claude Code** with the prompt template to build the site

```bash
# Step 1: Deploy infrastructure
sudo ./deploy/new_site.sh mysite mysite.example.com 8003 "SecurePass123!" "My Site Name"

# Step 2: Use Claude Code with deploy/SITE_CREATION_PROMPT.md to build the site
```

---

## Table of Contents

- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Deployment Process](#deployment-process)
- [File Structure](#file-structure)
- [Usage Guide](#usage-guide)
- [Port Management](#port-management)
- [Troubleshooting](#troubleshooting)
- [Advanced Configuration](#advanced-configuration)

---

## Overview

The WebGarden deployment system automates the creation of new Flask-based websites, handling:

- PostgreSQL database creation
- Python virtual environment setup
- Nginx reverse proxy configuration
- Systemd service management
- SSL certificate provisioning
- File permissions and directory structure
- Initial database migrations

Each site is isolated with its own:
- Database and database user
- Python virtual environment
- Port number
- Configuration files
- Upload directory
- Log files
- Systemd service

---

## Prerequisites

### System Requirements

- **Operating System**: Ubuntu 20.04+ or Debian 11+
- **User**: Root access (via sudo)
- **Services**: PostgreSQL, Nginx, Python 3.8+

### Required Software

Install all prerequisites with:

```bash
sudo apt-get update
sudo apt-get install -y \
    postgresql \
    postgresql-contrib \
    nginx \
    python3 \
    python3-pip \
    python3-venv \
    certbot \
    python3-certbot-nginx \
    git
```

### Verify PostgreSQL Setup

```bash
# Check PostgreSQL is running
sudo systemctl status postgresql

# Should show "active (running)"
```

### Verify Nginx Setup

```bash
# Check Nginx is running
sudo systemctl status nginx

# Test Nginx configuration
sudo nginx -t
```

### WebGarden Structure

Ensure the WebGarden platform is set up at:

```
/var/www/webgarden/
├── webgarden/
│   ├── sites/           # Individual site applications
│   ├── shared/          # Shared code (base_app, models, forms, etc.)
│   └── deploy/          # This deployment system
└── uploads/             # Site upload directories
```

---

## Deployment Process

### Overview of Automation

The `new_site.sh` script performs these steps automatically:

1. ✓ Validates prerequisites and inputs
2. ✓ Creates directory structure
3. ✓ Generates environment file from template
4. ✓ Creates PostgreSQL database and user
5. ✓ Generates Nginx configuration
6. ✓ Creates systemd service
7. ✓ Sets up Python virtual environment
8. ✓ Installs Python dependencies
9. ✓ Initializes database migrations
10. ✓ Prompts for admin user creation
11. ✓ Starts and enables services
12. ✓ Optionally sets up SSL certificate

**Total time: ~5-10 minutes** (excluding SSL verification)

---

## Usage Guide

### Step 1: Choose Site Parameters

Before running the deployment script, decide on:

1. **Site ID**: Short identifier (lowercase, no spaces)
   - Used for directories, configs, database name
   - Example: `mysite`, `acmecorp`, `dentist`

2. **Domain**: Full domain name
   - Example: `mysite.example.com`
   - Must be pointed to your server's IP

3. **Port**: Unique port number (8001-9000)
   - Check existing ports: `sudo netstat -tuln | grep LISTEN`
   - Current sites: psyling (8001), keystone (8002)
   - Next available: 8003

4. **Database Password**: Strong password for PostgreSQL
   - Use special characters: `SecurePass123!`
   - Will be stored in `/etc/webgarden/{site_id}.env`

5. **Site Name**: Display name (optional)
   - Used in templates and configurations
   - Example: "My Awesome Business"
   - Defaults to site_id if not provided

### Step 2: Run Deployment Script

```bash
cd /var/www/webgarden/webgarden/deploy

sudo ./new_site.sh <site_id> <domain> <port> <db_password> [site_name]
```

**Example:**

```bash
sudo ./new_site.sh dentist dentist.mywebgarden.com 8003 "DentPass2024!" "Smile Dental Clinic"
```

**What happens:**
- Script validates all inputs
- Creates all directories and configs
- Sets up database
- Installs dependencies
- Prompts for admin user creation
- Starts services
- Optionally sets up SSL

**Interactive prompts:**
1. Create admin user? (y/n)
   - Choose 'y' to create now
   - Choose 'n' to create later with Flask CLI

2. Set up SSL with Let's Encrypt? (y/n)
   - Choose 'y' if domain DNS is already configured
   - Choose 'n' to set up later

### Step 3: Build Site with Claude Code

1. **Open the prompt template:**
   ```bash
   cat /var/www/webgarden/webgarden/deploy/SITE_CREATION_PROMPT.md
   ```

2. **Fill in all [BRACKETED] sections** with your site requirements

3. **Copy the filled-in prompt** and paste into Claude Code

4. **Claude Code will build** your complete site following WebGarden patterns

5. **Wait for completion** (~10 minutes for a complete site)

### Step 4: Restart and Test

```bash
# Restart the service to load new code
sudo systemctl restart dentist.service

# Check service status
sudo systemctl status dentist.service

# View logs
sudo journalctl -u dentist.service -f
```

**Test in browser:**
- Visit http://your-domain.com
- Check all pages load correctly
- Test contact form
- Log into admin panel

### Step 5: Finalize Deployment

1. **Set up SSL** (if not done during deployment):
   ```bash
   sudo certbot --nginx -d your-domain.com
   ```

2. **Create admin user** (if not done during deployment):
   ```bash
   cd /var/www/webgarden/webgarden/sites/dentist
   venv/bin/flask create-admin
   ```

3. **Configure email** (update Mailgun settings in env file):
   ```bash
   sudo nano /etc/webgarden/dentist.env
   # Update MAIL_PASSWORD and MAIL_USERNAME
   sudo systemctl restart dentist.service
   ```

4. **Add real content:**
   - Upload photos
   - Update copy
   - Add testimonials
   - Create blog posts

---

## File Structure

After deployment, your site will have this structure:

```
/var/www/webgarden/
├── webgarden/
│   └── sites/
│       └── mysite/              # Your new site
│           ├── app.py           # Main Flask application
│           ├── config.py        # Site configuration
│           ├── cli.py           # Flask CLI commands
│           ├── venv/            # Python virtual environment
│           ├── migrations/      # Database migrations
│           ├── templates/       # Jinja2 templates
│           │   ├── index.html
│           │   ├── about.html
│           │   └── contact.html
│           └── static/          # Static files
│               ├── css/
│               ├── js/
│               └── images/
├── uploads/
│   └── mysite/                  # Upload directory
│
/etc/
├── webgarden/
│   └── mysite.env               # Environment variables
├── nginx/
│   └── sites-available/
│       └── mysite               # Nginx config
└── systemd/system/
    └── mysite.service           # Systemd service

/var/log/webgarden/
├── mysite-access.log            # Access logs
└── mysite-error.log             # Error logs
```

---

## Port Management

### Current Port Assignments

Track your port assignments to avoid conflicts:

| Site ID   | Port | Domain                      | Status |
|-----------|------|-----------------------------|--------|
| psyling   | 8001 | psyling.mywebgarden.qzz.io  | Active |
| keystone  | 8002 | keystone.mywebgarden.qzz.io | Active |
| [next]    | 8003 | [your-domain]               | Available |

### Check Available Ports

```bash
# List all listening ports
sudo netstat -tuln | grep LISTEN

# Check if specific port is in use
sudo lsof -i :8003
```

### Port Range

- Recommended range: 8001-8999
- System ports (0-1023): Avoid
- Common services (1024-8000): Avoid
- WebGarden sites: 8001+

---

## Troubleshooting

### Service Won't Start

**Check service status:**
```bash
sudo systemctl status mysite.service
```

**View detailed logs:**
```bash
sudo journalctl -u mysite.service -n 50 --no-pager
```

**Common issues:**
- Database connection error → Check DATABASE_URL in env file
- Module not found → Reinstall dependencies in venv
- Port already in use → Choose different port
- Permission denied → Check file ownership

**Fix permissions:**
```bash
sudo chown -R chip:chip /var/www/webgarden/webgarden/sites/mysite
sudo chown -R chip:chip /var/www/webgarden/uploads/mysite
```

### Database Connection Issues

**Test database connection:**
```bash
sudo -u postgres psql -d mysite_db -U mysite_user -W
```

**Reset database password:**
```bash
sudo -u postgres psql -c "ALTER USER mysite_user WITH PASSWORD 'NewPassword';"
```

**Check database exists:**
```bash
sudo -u postgres psql -l | grep mysite
```

### Nginx Configuration Errors

**Test nginx config:**
```bash
sudo nginx -t
```

**View nginx error log:**
```bash
sudo tail -f /var/log/nginx/error.log
```

**Reload nginx:**
```bash
sudo systemctl reload nginx
```

### SSL Certificate Issues

**Check certificate status:**
```bash
sudo certbot certificates
```

**Renew certificate:**
```bash
sudo certbot renew --nginx
```

**Test SSL configuration:**
```bash
sudo nginx -t
```

### Site Returns 502 Bad Gateway

This means Nginx can't connect to the Flask app.

**Check Flask app is running:**
```bash
sudo systemctl status mysite.service
```

**Check port is correct in Nginx config:**
```bash
grep proxy_pass /etc/nginx/sites-available/mysite
```

**Check Flask app is listening on correct port:**
```bash
sudo netstat -tuln | grep 8003
```

### Import Errors / Module Not Found

**Reinstall dependencies:**
```bash
cd /var/www/webgarden/webgarden/sites/mysite
source venv/bin/activate
pip install -r requirements.txt
deactivate
sudo systemctl restart mysite.service
```

### Database Migration Errors

**Reset migrations (DANGER: Destroys data):**
```bash
cd /var/www/webgarden/webgarden/sites/mysite
rm -rf migrations/
source venv/bin/activate
export DATABASE_URL="postgresql://mysite_user:password@localhost/mysite_db"
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
deactivate
```

---

## Advanced Configuration

### Customizing Templates

Edit templates in `/var/www/webgarden/webgarden/deploy/templates/`:

- `site.env.template` - Environment variables
- `nginx.conf.template` - Nginx configuration
- `systemd.service.template` - Systemd service

Placeholders are replaced during deployment:
- `{{SITE_ID}}` - Site identifier
- `{{SITE_NAME}}` - Display name
- `{{DOMAIN}}` - Domain name
- `{{PORT}}` - Port number
- `{{DB_NAME}}` - Database name
- `{{DB_USER}}` - Database user
- `{{DB_PASSWORD}}` - Database password

### Adding Custom Dependencies

Edit the `setup_virtualenv()` function in `new_site.sh` to add more Python packages:

```bash
sudo -u "$WEBGARDEN_USER" venv/bin/pip install \
    flask \
    # ... existing packages ...
    your-package-name
```

### Changing Default Settings

Edit these sections in `new_site.sh`:

- `WEBGARDEN_USER` - Change from "chip" to your user
- Gunicorn workers - Change `-w 4` to different worker count
- File permissions - Modify `set_permissions()` function

### Multi-Domain Support

To add additional domains to a site:

```bash
# Edit Nginx config
sudo nano /etc/nginx/sites-available/mysite

# Add to server_name line:
server_name mysite.com www.mysite.com alternate.com;

# Get SSL for all domains
sudo certbot --nginx -d mysite.com -d www.mysite.com -d alternate.com
```

### Environment-Specific Configuration

The `config.py` file supports multiple environments:

- `development` - Debug mode, relaxed security
- `production` - No debug, full security (default)
- `testing` - For unit tests

Set environment in systemd service:
```bash
sudo nano /etc/systemd/system/mysite.service

# Add to [Service] section:
Environment="FLASK_ENV=development"
```

---

## Maintenance

### Backup Site

```bash
# Backup database
sudo -u postgres pg_dump mysite_db > mysite_backup.sql

# Backup files
tar -czf mysite_files.tar.gz /var/www/webgarden/webgarden/sites/mysite

# Backup uploads
tar -czf mysite_uploads.tar.gz /var/www/webgarden/uploads/mysite
```

### Update Site

```bash
# Pull changes (if using git)
cd /var/www/webgarden/webgarden/sites/mysite
sudo -u chip git pull

# Restart service
sudo systemctl restart mysite.service
```

### Monitor Logs

```bash
# Follow service logs
sudo journalctl -u mysite.service -f

# View access logs
sudo tail -f /var/log/webgarden/mysite-access.log

# View error logs
sudo tail -f /var/log/webgarden/mysite-error.log
```

### Delete Site

```bash
# Stop and disable service
sudo systemctl stop mysite.service
sudo systemctl disable mysite.service

# Remove files
sudo rm -rf /var/www/webgarden/webgarden/sites/mysite
sudo rm -rf /var/www/webgarden/uploads/mysite
sudo rm /etc/webgarden/mysite.env
sudo rm /etc/nginx/sites-enabled/mysite
sudo rm /etc/nginx/sites-available/mysite
sudo rm /etc/systemd/system/mysite.service

# Drop database
sudo -u postgres psql -c "DROP DATABASE mysite_db;"
sudo -u postgres psql -c "DROP USER mysite_user;"

# Reload services
sudo systemctl daemon-reload
sudo systemctl reload nginx
```

---

## Getting Help

### Useful Commands

```bash
# Service management
sudo systemctl status mysite.service    # Check status
sudo systemctl restart mysite.service   # Restart
sudo systemctl start mysite.service     # Start
sudo systemctl stop mysite.service      # Stop

# View logs
sudo journalctl -u mysite.service -f    # Follow logs
sudo journalctl -u mysite.service -n 100 # Last 100 lines

# Database management
cd /var/www/webgarden/webgarden/sites/mysite
venv/bin/flask db migrate -m "Description"  # Create migration
venv/bin/flask db upgrade                   # Apply migrations
venv/bin/flask create-admin                 # Create admin user

# Nginx management
sudo nginx -t                           # Test configuration
sudo systemctl reload nginx             # Reload config
sudo systemctl restart nginx            # Restart nginx
```

### Log Files

- **Service logs**: `journalctl -u mysite.service`
- **Access logs**: `/var/log/webgarden/mysite-access.log`
- **Error logs**: `/var/log/webgarden/mysite-error.log`
- **Nginx logs**: `/var/log/nginx/error.log`
- **PostgreSQL logs**: `/var/log/postgresql/`

### Common Questions

**Q: Can I run the deployment script multiple times?**
A: No, the script will exit if the site already exists. Delete the site first or use a different site_id.

**Q: How do I change the port after deployment?**
A: Edit these files, then restart:
- `/etc/webgarden/mysite.env` (not needed for port)
- `/etc/nginx/sites-available/mysite` (proxy_pass line)
- `/etc/systemd/system/mysite.service` (ExecStart line)

**Q: Can I use a subdomain?**
A: Yes, just use the full subdomain as the domain parameter: `mysite.example.com`

**Q: How do I add HTTPS after initial deployment?**
A: Run `sudo certbot --nginx -d your-domain.com`

**Q: Where are passwords stored?**
A: In `/etc/webgarden/mysite.env` with 600 permissions (owner read/write only)

---

## Contributing

To improve this deployment system:

1. Test changes on a development server first
2. Update this README with any new features
3. Keep templates in sync with site requirements
4. Document any breaking changes

---

## License

Part of the WebGarden multi-site hosting platform.

---

**Ready to deploy?** Start with the Quick Start guide at the top of this document!
