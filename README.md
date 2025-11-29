# WebGarden - Multi-Site Flask Hosting Platform

WebGarden is a production-ready Flask-based web hosting platform designed to efficiently host multiple small business websites from a single codebase. Built with a monorepo architecture, it enables rapid deployment of new sites while sharing common functionality.

## 🌟 Features

- **Multi-Site Architecture**: Single codebase supporting multiple independent sites
- **Production-Ready**: Nginx + Gunicorn + systemd deployment
- **Security First**: HTTPS, CSRF protection, rate limiting, secure sessions
- **Modern Stack**: Flask 3.0, PostgreSQL, Bootstrap 5, TinyMCE
- **Complete CMS**: Blog system, admin panel, user authentication
- **Automated Deployment**: Deploy new sites in 15 minutes with automation scripts
- **AI-Assisted Development**: Claude Code integration for rapid site creation
- **Easy Management**: systemd service management
- **Scalable Design**: Proven architecture across multiple production sites

## 📋 Project Status

✅ **Sprint 1 - Foundation (Complete)**
- Therapist psychotherapy website (MVP)
- Shared module library
- Database schema and migrations
- Deployment configurations
- Control and setup scripts
- Complete documentation

✅ **Sprint 2 - Blog & Admin (Complete)**
- Blog functionality with rich text editor (TinyMCE)
- Full admin panel for content management
- User authentication system with Flask-Login
- Image upload management and optimization
- Contact submission management
- HTML sanitization and security features

✅ **Sprint 3 - Deployment Automation (Complete)**
- Automated site deployment script (new_site.sh)
- Site creation prompt template for Claude Code
- Complete deployment documentation
- Second production site (Keystone Hardscapes)
- Infrastructure templates for rapid site creation

🚀 **Active Sites:**
- **psyling** (Therapist/Psychotherapy) - Port 8001
- **keystone** (Hardscapes/Landscaping) - Port 8002

🔮 **Future Development:**
- Cal.com booking integration
- Bot widget integration
- Additional business sites as needed

## 🏗️ Project Structure

```
webgarden/
├── shared/                      # Shared modules for all sites
│   ├── __init__.py
│   ├── base_app.py             # Flask application factory
│   ├── models.py               # Common database models
│   ├── forms.py                # WTForms definitions
│   ├── email.py                # Email utilities (Mailgun)
│   ├── image_handler.py        # Image upload/resize
│   ├── auth.py                 # Authentication helpers
│   ├── decorators.py           # Custom route decorators
│   ├── sanitizer.py            # HTML sanitization
│   └── templates/              # Shared base templates
│       ├── base.html
│       └── errors/
├── sites/                      # Individual site applications
│   ├── therapist/              # Psychotherapy site (psyling)
│   │   ├── app.py              # Main application
│   │   ├── config.py           # Site configuration
│   │   ├── cli.py              # CLI commands
│   │   ├── templates/          # Site-specific templates
│   │   │   ├── index.html
│   │   │   ├── about.html
│   │   │   ├── services.html
│   │   │   ├── contact.html
│   │   │   ├── post.html
│   │   │   └── admin/          # Admin panel templates
│   │   ├── static/             # Static assets
│   │   │   ├── css/
│   │   │   ├── js/
│   │   │   └── images/
│   │   ├── migrations/         # Database migrations
│   │   └── venv/               # Python virtual environment
│   └── keystone/               # Hardscapes site
│       ├── app.py              # Main application
│       ├── config.py           # Site configuration
│       ├── cli.py              # CLI commands
│       ├── templates/          # Templates
│       ├── static/             # Static assets
│       ├── migrations/         # Database migrations
│       └── venv/               # Python virtual environment
├── deploy/                     # Deployment system
│   ├── new_site.sh            # Complete site deployment automation
│   ├── setup_site.sh          # Legacy setup script
│   ├── webgarden-ctl.sh       # Service control script
│   ├── SITE_CREATION_PROMPT.md # Claude Code prompt template
│   ├── QUICKSTART.md          # Quick deployment guide
│   ├── README.md              # Comprehensive deployment docs
│   ├── templates/             # Config templates
│   │   ├── site.env.template
│   │   ├── nginx.conf.template
│   │   └── systemd.service.template
│   ├── nginx/                 # Nginx configs
│   └── systemd/               # Systemd service files
├── uploads/                    # File uploads (per site)
│   ├── therapist/
│   └── keystone/
├── backups/                    # Backup storage
├── .env.example               # Environment template
├── requirements.txt           # Global dependencies
├── CHANGELOG.md               # Version history
├── SPRINT_2_COMPLETE.md       # Sprint 2 documentation
└── README.md                  # This file
```

## 🚀 Quick Start

### Prerequisites

- Debian/Ubuntu Linux server
- Python 3.10+
- PostgreSQL 12+
- Nginx
- Certbot (for SSL)
- Root/sudo access

### Deploying a New Site (15 Minutes)

WebGarden now includes complete deployment automation. Deploy a new site in just 2 steps:

**Step 1: Deploy Infrastructure (5 minutes)**
```bash
cd /var/www/webgarden/webgarden/deploy
sudo ./new_site.sh mysite mysite.example.com 8003 "SecurePass123!" "My Site Name"
```

This automatically:
- Creates PostgreSQL database and user
- Sets up Python virtual environment
- Configures Nginx reverse proxy
- Creates systemd service
- Installs all dependencies
- Initializes database migrations
- Prompts for admin user creation
- Optionally sets up SSL certificate

**Step 2: Build Site with Claude Code (10 minutes)**
```bash
# 1. Open the prompt template
cat deploy/SITE_CREATION_PROMPT.md

# 2. Fill in [BRACKETED] sections with your business info

# 3. Copy and paste the filled prompt into Claude Code

# 4. Wait for Claude to build your complete site

# 5. Restart the service
sudo systemctl restart mysite.service

# 6. Visit your site!
```

**Quick Reference:**
- Next available port: 8003 (8001 and 8002 are in use)
- Full documentation: `deploy/README.md`
- Quick guide: `deploy/QUICKSTART.md`

### Manual Installation (Legacy)

For manual setup or understanding the internals, see the [Manual Setup Guide](#development) below.

## 🎮 Service Management

### Using systemctl

```bash
# Replace {sitename} with: therapist, keystone, or your site name

# Start service
sudo systemctl start {sitename}.service

# Stop service
sudo systemctl stop {sitename}.service

# Restart service
sudo systemctl restart {sitename}.service

# Check status
sudo systemctl status {sitename}.service

# View logs
sudo journalctl -u {sitename}.service -f

# Examples:
sudo systemctl restart therapist.service
sudo systemctl status keystone.service
```

### Legacy Control Script

```bash
# For sites deployed with old setup_site.sh
sudo /var/www/webgarden/deploy/webgarden-ctl.sh restart therapist
```

## 📝 Configuration

### Environment Variables

Configuration is managed through environment files located in `/etc/webgarden/`.

**Example: `/etc/webgarden/{sitename}.env`**

```bash
# Flask
SECRET_KEY=<auto-generated-secret-key>
FLASK_ENV=production

# Database
DATABASE_URL=postgresql://{sitename}_user:password@localhost/{sitename}_db

# Mail (Mailgun)
MAIL_SERVER=smtp.mailgun.org
MAIL_PORT=587
MAIL_USERNAME=postmaster@yourdomain.com
MAIL_PASSWORD=<your-mailgun-api-key>
MAIL_DEFAULT_SENDER=info@yourdomain.com
ADMIN_EMAIL=admin@yourdomain.com

# Site
SITE_NAME=Your Site Name
SITE_DOMAIN=yourdomain.com
UPLOAD_FOLDER=/var/www/webgarden/uploads/{sitename}
MAX_UPLOAD_SIZE=5242880

# Office/Business Info
OFFICE_PHONE=(123) 456-7890
OFFICE_EMAIL=info@yourdomain.com
```

**Active sites:**
- `/etc/webgarden/therapist.env` - Psychotherapy site
- `/etc/webgarden/keystone.env` - Hardscapes site

### Database Configuration

Each site has its own isolated PostgreSQL database:

```bash
# Access database (replace {sitename} with therapist, keystone, etc.)
sudo -u postgres psql {sitename}_db

# Backup database
sudo -u postgres pg_dump {sitename}_db > /var/www/webgarden/backups/databases/{sitename}_$(date +%Y%m%d).sql

# Restore database
sudo -u postgres psql {sitename}_db < backup_file.sql

# List all WebGarden databases
sudo -u postgres psql -l | grep "_db"
```

**Active databases:**
- `therapist_db` - Psychotherapy site
- `keystone_db` - Hardscapes site

### Nginx Configuration

Nginx configuration files are located in `/etc/nginx/sites-available/`.

```bash
# Edit nginx config (replace {sitename})
sudo nano /etc/nginx/sites-available/{sitename}

# Test nginx config
sudo nginx -t

# Reload nginx
sudo systemctl reload nginx

# List all WebGarden site configs
ls -l /etc/nginx/sites-available/ | grep -E '(therapist|keystone)'
```

**Active configs:**
- `/etc/nginx/sites-available/therapist` - Port 8001
- `/etc/nginx/sites-available/keystone` - Port 8002

## 🔧 Development

### Local Development Setup

1. **Create virtual environment:**
```bash
cd /var/www/webgarden/sites/therapist
python3 -m venv venv
source venv/bin/activate
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Set up environment:**
```bash
cp ../../.env.example .env
# Edit .env with your settings
nano .env
```

4. **Initialize database:**
```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

5. **Run development server:**
```bash
flask run --debug
```

### Database Migrations

```bash
# Create a new migration
flask db migrate -m "Description of changes"

# Apply migrations
flask db upgrade

# Rollback migration
flask db downgrade

# View migration history
flask db history
```

### Testing

```bash
# Run tests (Sprint 2)
pytest

# Run with coverage
pytest --cov=app

# Run specific test
pytest tests/test_contact.py
```

## 🔐 Security

### Implemented Security Features

- ✅ HTTPS only (HTTP redirects to HTTPS)
- ✅ Let's Encrypt SSL certificates with auto-renewal
- ✅ CSRF protection on all forms
- ✅ Rate limiting (100 requests/minute)
- ✅ Secure session cookies (httponly, secure)
- ✅ SQL injection protection (SQLAlchemy ORM)
- ✅ Input validation and sanitization
- ✅ Security headers (HSTS, X-Frame-Options, etc.)
- ✅ Environment-based secrets management

### Security Best Practices

1. **Never commit secrets:**
   - Use environment variables
   - Keep `.env` files out of git
   - Rotate secrets regularly

2. **Keep dependencies updated:**
```bash
pip list --outdated
pip install --upgrade -r requirements.txt
```

3. **Monitor logs:**
```bash
sudo journalctl -u webgarden-therapist -f
tail -f /var/log/nginx/therapist-access.log
tail -f /var/log/nginx/therapist-error.log
```

4. **Regular backups:**
   - Database backups (daily recommended)
   - Upload directory backups
   - Configuration backups

## 🆕 Adding a New Site

WebGarden includes complete deployment automation. Deploy a new site in 15 minutes:

### Automated Deployment (Recommended)

**Step 1: Run the deployment script**
```bash
cd /var/www/webgarden/webgarden/deploy
sudo ./new_site.sh dentist dentist.example.com 8003 "SecurePass2024!" "Smile Dental"
```

This creates all infrastructure: database, virtual environment, Nginx config, systemd service, and more.

**Step 2: Use the site creation prompt with Claude Code**
```bash
# 1. Copy the prompt template
cat deploy/SITE_CREATION_PROMPT.md

# 2. Fill in [BRACKETED] sections with business details

# 3. Paste into Claude Code to build the complete site
```

**Step 3: Restart and test**
```bash
sudo systemctl restart dentist.service
# Visit: https://dentist.example.com
```

**Port Reference:**
- 8001: therapist (psyling)
- 8002: keystone (hardscapes)
- 8003+: Available for new sites

**Full documentation:** See `deploy/README.md` for comprehensive deployment guide.

### Manual Deployment (Legacy)

For manual setup, copy an existing site directory and update configurations manually. See existing sites in `sites/` for reference patterns.

## 📊 Monitoring

### Check Service Status

```bash
# Service status
sudo systemctl status webgarden-therapist

# Process information
ps aux | grep gunicorn

# Port binding
sudo netstat -tlnp | grep 8001
```

### View Logs

```bash
# Application logs
sudo journalctl -u webgarden-therapist -n 100

# Nginx access logs
sudo tail -f /var/log/nginx/therapist-access.log

# Nginx error logs
sudo tail -f /var/log/nginx/therapist-error.log

# Gunicorn logs
sudo tail -f /var/log/webgarden/therapist-access.log
sudo tail -f /var/log/webgarden/therapist-error.log
```

## 🐛 Troubleshooting

### Service won't start

```bash
# Check service status
sudo systemctl status webgarden-therapist

# Check logs
sudo journalctl -u webgarden-therapist -n 50

# Check if port is in use
sudo netstat -tlnp | grep 8001

# Verify environment file
cat /etc/webgarden/therapist.env
```

### Database connection issues

```bash
# Test database connection
sudo -u postgres psql therapist_db -c "\conninfo"

# Check if database exists
sudo -u postgres psql -l | grep therapist

# Verify DATABASE_URL in env file
grep DATABASE_URL /etc/webgarden/therapist.env
```

### Nginx/SSL issues

```bash
# Test nginx configuration
sudo nginx -t

# Check SSL certificates
sudo certbot certificates

# Renew SSL manually
sudo certbot renew --dry-run
```

### Permission issues

```bash
# Fix ownership
sudo chown -R webgarden:webgarden /var/www/webgarden
sudo chown -R webgarden:webgarden /var/www/webgarden/uploads/therapist

# Fix permissions
sudo chmod 755 /var/www/webgarden
sudo chmod 644 /etc/webgarden/therapist.env
```

## 📚 Useful Commands

### Flask CLI

```bash
# Navigate to your site directory
cd /var/www/webgarden/webgarden/sites/{sitename}
source venv/bin/activate

# Create admin user
flask create-admin

# Reset password
flask reset-password

# List users
flask list-users

# Create test blog post
flask create-test-post

# Database migrations
flask db migrate -m "Description"
flask db upgrade

# Run Flask shell
flask shell

# Examples:
cd /var/www/webgarden/webgarden/sites/therapist && source venv/bin/activate && flask create-admin
cd /var/www/webgarden/webgarden/sites/keystone && source venv/bin/activate && flask list-users
```

### Database

```bash
# Connect to database
sudo -u postgres psql therapist_db

# List tables
\dt

# Describe table
\d users

# Run query
SELECT * FROM contact_submissions ORDER BY submitted_at DESC LIMIT 10;
```

## 🤝 Contributing

1. Follow Python PEP 8 style guide
2. Add docstrings to all functions
3. Write tests for new features
4. Update documentation

## 📄 License

[Specify license]

## 👥 Support

For issues or questions:
- Check the troubleshooting section
- Review logs for error messages
- Contact: [your-email]

## 🗺️ Roadmap

### ✅ Sprint 1 - Foundation (Complete)
- [x] Therapist psychotherapy website MVP
- [x] Shared module library
- [x] Database schema and migrations
- [x] Production deployment configurations
- [x] Control and setup scripts

### ✅ Sprint 2 - Blog & Admin (Complete)
- [x] Blog functionality with rich text editor (TinyMCE)
- [x] Admin panel for content management
- [x] User authentication and roles
- [x] Image upload management
- [x] Contact submission management
- [x] HTML sanitization and security

### ✅ Sprint 3 - Deployment Automation (Complete)
- [x] Automated site deployment script
- [x] Site creation prompt template
- [x] Infrastructure templates
- [x] Second production site (Keystone)
- [x] Comprehensive deployment documentation

### 🔮 Future Development
- [ ] Cal.com booking integration
- [ ] Bot/chat widget integration
- [ ] Email templates and scheduling
- [ ] Advanced analytics dashboard
- [ ] Multi-language support
- [ ] Additional business sites as needed

---

**Built with ❤️ for small businesses**

Last Updated: 2025-11-29
