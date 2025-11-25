# WebGarden - Multi-Site Flask Hosting Platform

WebGarden is a production-ready Flask-based web hosting platform designed to efficiently host multiple small business websites from a single codebase. Built with a monorepo architecture, it enables rapid deployment of new sites while sharing common functionality.

## 🌟 Features

- **Multi-Site Architecture**: Single codebase supporting multiple independent sites
- **Production-Ready**: Nginx + Gunicorn + systemd deployment
- **Security First**: HTTPS, CSRF protection, rate limiting, secure sessions
- **Modern Stack**: Flask 3.0, PostgreSQL, Bootstrap 5
- **Easy Management**: Control scripts for service management
- **Automated Setup**: Complete deployment automation
- **Scalable Design**: Ready for additional sites

## 📚 Documentation

**Core Documentation:**
- **[Architecture Guide](ARCHITECTURE.md)** - System architecture, design patterns, and technical decisions
- **[Claude README](claude-readme.md)** - Quick reference for AI assistants (Claude Sonnet)
- **[Changelog](CHANGELOG.md)** - Version history and release notes

**Module Documentation:**
- **[Shared Modules](shared/README.md)** - Comprehensive guide to shared components (base_app, models, forms, email, etc.)
- **[Therapist Site](sites/therapist/README.md)** - Therapist site routes, templates, and features
- **[Keystone Site](sites/keystone/README.md)** - Keystone hardscapes site documentation

**Deployment Documentation:**
- **[Deployment Guide](deploy/README.md)** - Production deployment procedures
- **[Quick Start](deploy/QUICKSTART.md)** - Fast deployment guide
- **[Site Creation](deploy/SITE_CREATION_PROMPT.md)** - How to add new sites

## 📋 Sprint 1 Status

✅ **Completed:**
- Therapist psychotherapy website (MVP)
- Shared module library
- Database schema and migrations
- Deployment configurations
- Control and setup scripts
- Complete documentation

🚧 **Coming in Sprint 2:**
- Blog functionality
- Admin panel with Flask-Admin
- User authentication system
- Image upload management

🔮 **Future Sprints:**
- Cal.com booking integration (Sprint 3)
- Bot widget integration (Sprint 3)
- Handyman business site
- Computer lab site

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
│   └── templates/              # Shared base templates
│       ├── base.html
│       └── errors/
├── sites/                      # Individual site applications
│   └── therapist/
│       ├── app.py              # Main application
│       ├── config.py           # Site configuration
│       ├── requirements.txt    # Site dependencies
│       ├── templates/          # Site-specific templates
│       │   ├── index.html
│       │   ├── about.html
│       │   ├── services.html
│       │   └── contact.html
│       ├── static/             # Static assets
│       │   ├── css/
│       │   ├── js/
│       │   └── images/
│       └── migrations/         # Database migrations
├── deploy/                     # Deployment configurations
│   ├── nginx/
│   │   └── therapist.conf
│   ├── systemd/
│   │   └── webgarden-therapist.service
│   ├── webgarden-ctl.sh       # Service control script
│   └── setup_site.sh          # Automated setup script
├── uploads/                    # File uploads (per site)
├── backups/                    # Backup storage
├── .env.example               # Environment template
├── requirements.txt           # Global dependencies
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

### Installation

1. **Clone the repository:**
```bash
cd /var/www
git clone <repository-url> webgarden
cd webgarden
```

2. **Run the automated setup:**
```bash
sudo ./deploy/setup_site.sh therapist therapist.example.com
```

This will:
- Create system user and directories
- Set up PostgreSQL database
- Create Python virtual environment
- Install dependencies
- Initialize database
- Configure nginx and systemd
- Obtain SSL certificate
- Start the service

3. **Configure environment variables:**
```bash
sudo nano /etc/webgarden/therapist.env
```

Update:
- Mail server credentials (Mailgun)
- Office contact information
- Any other site-specific settings

4. **Create admin user:**
```bash
cd /var/www/webgarden/sites/therapist
sudo -u webgarden venv/bin/flask create-admin
```

5. **Restart service:**
```bash
sudo systemctl restart webgarden-therapist
```

6. **Visit your site:**
```
https://therapist.example.com
```

## 🎮 Service Management

### Using Control Script (Recommended)

```bash
# Start service
sudo /var/www/webgarden/deploy/webgarden-ctl.sh start therapist

# Stop service
sudo /var/www/webgarden/deploy/webgarden-ctl.sh stop therapist

# Restart service
sudo /var/www/webgarden/deploy/webgarden-ctl.sh restart therapist

# Check status
sudo /var/www/webgarden/deploy/webgarden-ctl.sh status therapist

# View logs
sudo /var/www/webgarden/deploy/webgarden-ctl.sh logs therapist

# Follow logs in real-time
sudo /var/www/webgarden/deploy/webgarden-ctl.sh logs therapist -f
```

### Using systemctl Directly

```bash
sudo systemctl start webgarden-therapist
sudo systemctl stop webgarden-therapist
sudo systemctl restart webgarden-therapist
sudo systemctl status webgarden-therapist
```

## 📝 Configuration

### Environment Variables

Configuration is managed through environment files located in `/etc/webgarden/`.

**Example: `/etc/webgarden/therapist.env`**

```bash
# Flask
SECRET_KEY=<generated-secret-key>
FLASK_ENV=production

# Database
DATABASE_URL=postgresql://user:password@localhost/therapist_db

# Mail (Mailgun)
MAIL_SERVER=smtp.mailgun.org
MAIL_PORT=587
MAIL_USERNAME=postmaster@therapist.example.com
MAIL_PASSWORD=<your-mailgun-api-key>
MAIL_DEFAULT_SENDER=info@therapist.example.com
ADMIN_EMAIL=admin@therapist.example.com

# Site
SITE_NAME=Professional Psychotherapy
SITE_DOMAIN=therapist.example.com
UPLOAD_FOLDER=/var/www/webgarden/uploads/therapist
MAX_UPLOAD_SIZE=5242880

# Office Info
OFFICE_PHONE=(416) 555-0100
OFFICE_EMAIL=info@therapist.example.com
```

### Database Configuration

Each site has its own PostgreSQL database:

```bash
# Access database
sudo -u postgres psql therapist_db

# Backup database
sudo -u postgres pg_dump therapist_db > /var/www/webgarden/backups/databases/therapist_$(date +%Y%m%d).sql

# Restore database
sudo -u postgres psql therapist_db < backup_file.sql
```

### Nginx Configuration

Nginx configuration files are located in `/etc/nginx/sites-available/`.

```bash
# Edit nginx config
sudo nano /etc/nginx/sites-available/therapist

# Test nginx config
sudo nginx -t

# Reload nginx
sudo systemctl reload nginx
```

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

To add a new site (e.g., handyman business):

1. **Copy site template:**
```bash
cp -r sites/therapist sites/handyman
```

2. **Update configuration:**
```bash
cd sites/handyman
# Update config.py, app.py, templates, etc.
```

3. **Copy deployment configs:**
```bash
cp deploy/nginx/therapist.conf deploy/nginx/handyman.conf
cp deploy/systemd/webgarden-therapist.service deploy/systemd/webgarden-handyman.service
# Update references to 'therapist' -> 'handyman'
```

4. **Run setup script:**
```bash
sudo ./deploy/setup_site.sh handyman handyman.example.com
```

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
cd /var/www/webgarden/sites/therapist
source venv/bin/activate

# Create admin user
flask create-admin

# Initialize database
flask init-db

# Test email configuration
flask test-email

# Run Flask shell
flask shell
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

### Sprint 2
- [ ] Blog functionality with rich text editor
- [ ] Admin panel with Flask-Admin
- [ ] User authentication and roles
- [ ] Image upload management

### Sprint 3
- [ ] Cal.com booking integration
- [ ] Bot widget integration
- [ ] Email templates and scheduling

### Sprint 4
- [ ] Handyman business site
- [ ] Computer lab site
- [ ] Advanced analytics
- [ ] Multi-language support

---

**Built with ❤️ for small businesses**

Last Updated: 2025-11-12
