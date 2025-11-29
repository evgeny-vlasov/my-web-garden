# Claude README - WebGarden Project

> This document is specifically designed for AI assistants (like Claude Sonnet) to quickly understand the WebGarden project structure, architecture, and conventions.

## Project Quick Reference

**Project Name:** WebGarden
**Type:** Multi-site Flask hosting platform (monorepo)
**Language:** Python 3.10+
**Framework:** Flask 3.0
**Database:** PostgreSQL
**Current Sites:** 2 (therapist, keystone)

## Architecture Overview

### High-Level Structure

```
WebGarden = Shared Modules + Individual Sites + Deployment System

Shared modules (shared/):
  └─ Provide common functionality to all sites
     (app factory, models, forms, email, security)

Individual sites (sites/):
  ├─ therapist/     (Professional psychotherapy website)
  └─ keystone/      (Hardscaping business website)

Deployment (deploy/):
  └─ Scripts for production deployment
     (nginx configs, systemd services, automation)
```

### Key Design Principles

1. **DRY (Don't Repeat Yourself)**: Common functionality lives in `shared/`
2. **Site Independence**: Each site has its own config, templates, static files
3. **Shared Database Models**: All sites use same User, BlogPost, ContactSubmission models
4. **Production-Ready**: Security, rate limiting, email, migrations built-in
5. **Easy Expansion**: Copy-paste a site to create a new one

## File Organization Map

```
/home/user/my-web-garden/
├── shared/                          # SHARED MODULES (used by all sites)
│   ├── base_app.py                 # Flask app factory + extensions
│   ├── models.py                   # Database models (User, BlogPost, etc.)
│   ├── forms.py                    # WTForms (ContactForm, LoginForm, etc.)
│   ├── email.py                    # Email utilities (Mailgun)
│   ├── image_handler.py            # Image upload/resize
│   ├── sanitizer.py                # HTML sanitization (XSS prevention)
│   ├── decorators.py               # @login_required, @admin_required
│   ├── auth.py                     # Authentication helpers
│   ├── templates/                  # Shared base templates
│   │   ├── base.html              # Master template
│   │   └── errors/                # Error pages (404, 500)
│   └── README.md                   # Comprehensive shared modules docs
│
├── sites/                           # INDIVIDUAL SITES
│   ├── therapist/                  # Psychotherapy website
│   │   ├── app.py                 # Main Flask app (uses create_base_app)
│   │   ├── config.py              # Site-specific configuration
│   │   ├── cli.py                 # CLI commands (create-admin, etc.)
│   │   ├── templates/             # Site-specific templates
│   │   │   ├── index.html
│   │   │   ├── about.html
│   │   │   ├── services.html
│   │   │   ├── contact.html
│   │   │   ├── post.html
│   │   │   └── admin/             # Admin panel templates
│   │   ├── static/                # Site-specific assets
│   │   │   ├── css/
│   │   │   ├── js/
│   │   │   └── images/
│   │   ├── migrations/            # Database migrations
│   │   └── README.md              # Comprehensive site docs
│   │
│   └── keystone/                   # Hardscaping business website
│       ├── app.py                 # Main Flask app
│       ├── config.py              # Site-specific configuration
│       ├── cli.py                 # CLI commands
│       ├── templates/             # Site-specific templates
│       │   ├── index.html
│       │   ├── about.html
│       │   ├── services.html
│       │   ├── contact.html
│       │   ├── portfolio.html
│       │   └── services/          # Service-specific pages
│       ├── static/                # Site-specific assets
│       ├── migrations/            # Database migrations
│       └── README.md              # Site documentation
│
├── deploy/                          # DEPLOYMENT SYSTEM
│   ├── nginx/                      # Nginx configurations
│   ├── systemd/                    # Systemd service files
│   ├── templates/                  # Config templates
│   ├── setup_site.sh              # Automated site setup script
│   ├── new_site.sh                # New site creation script
│   ├── webgarden-ctl.sh           # Service control wrapper
│   ├── README.md                  # Deployment documentation
│   ├── QUICKSTART.md              # Quick deployment guide
│   └── SITE_CREATION_PROMPT.md    # New site creation guide
│
├── .env.example                     # Environment variable template
├── requirements.txt                 # Global Python dependencies
├── README.md                        # Main project documentation
├── CHANGELOG.md                     # Project changelog
└── claude-readme.md                 # This file (for AI assistants)
```

## Database Schema Quick Reference

### Core Models (shared/models.py)

#### User
- Authentication: username, email, password_hash
- Roles: 'admin' or 'editor'
- Relationships: blog_posts, uploaded_files

#### ContactSubmission
- Fields: name, email, phone, message
- Status: 'new', 'read', 'responded'
- Tracking: submitted_at, notes

#### BlogPost
- Content: title, slug, content (HTML)
- Publishing: visible (bool), published_at
- Relationships: author (User)

#### UploadedFile
- Metadata: filename, filepath, file_size, mime_type
- Relationships: uploaded_by (User)

### Database Access Patterns

```python
# Import
from shared.models import User, BlogPost, ContactSubmission
from shared.base_app import db

# Query examples
User.query.filter_by(username='admin').first()
BlogPost.query.filter_by(visible=True).order_by(BlogPost.published_at.desc()).all()
ContactSubmission.query.filter_by(status='new').count()

# Create/Update
user = User(username='admin', email='admin@example.com', role='admin')
user.set_password('password')
db.session.add(user)
db.session.commit()
```

## Common Development Tasks

### Adding a New Route

**Location:** `sites/{sitename}/app.py`

```python
@app.route('/new-page')
def new_page():
    """Page description."""
    return render_template('new-page.html')
```

### Creating a Template

**Location:** `sites/{sitename}/templates/new-page.html`

```html
{% extends "base.html" %}

{% block title %}Page Title - {{ site_name }}{% endblock %}

{% block content %}
<div class="container">
  <h1>Page Content</h1>
  <!-- Your content -->
</div>
{% endblock %}
```

### Adding a Form

1. **Define form in** `shared/forms.py` (if reusable) or site's forms file
2. **Import in** `sites/{sitename}/app.py`
3. **Use in route:**

```python
@app.route('/form-page', methods=['GET', 'POST'])
def form_page():
    form = MyForm()
    if form.validate_on_submit():
        # Process form
        flash('Success!', 'success')
        return redirect(url_for('form_page'))
    return render_template('form-page.html', form=form)
```

### Database Migration

```bash
cd /var/www/webgarden/sites/{sitename}
source venv/bin/activate

# Create migration
flask db migrate -m "Description of changes"

# Review migration file
cat migrations/versions/{id}_description.py

# Apply migration
flask db upgrade
```

### Adding New Shared Functionality

1. **Add to appropriate shared module** (`shared/models.py`, `shared/forms.py`, etc.)
2. **Import in site's** `app.py`
3. **Use in routes/templates**

**Example:** Adding a new shared model

```python
# In shared/models.py
class Newsletter(db.Model):
    __tablename__ = 'newsletter_subscriptions'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    subscribed_at = db.Column(db.DateTime, default=datetime.utcnow)

# In sites/therapist/app.py
from shared.models import Newsletter

@app.route('/subscribe', methods=['POST'])
def subscribe():
    email = request.form.get('email')
    sub = Newsletter(email=email)
    db.session.add(sub)
    db.session.commit()
    return jsonify({'success': True})
```

## Configuration Patterns

### Environment Variables

**Location:** `/etc/webgarden/{sitename}.env` (production) or `.env` (dev)

**Required variables:**
```bash
SECRET_KEY=<random-secret>          # Flask secret key
DATABASE_URL=postgresql://...       # Database connection
MAIL_USERNAME=<mailgun-user>        # Mailgun SMTP username
MAIL_PASSWORD=<mailgun-password>    # Mailgun SMTP password
MAIL_DEFAULT_SENDER=<email>         # Default sender email
ADMIN_EMAIL=<email>                 # Admin notification email
SITE_NAME=<name>                    # Site name for display
SITE_DOMAIN=<domain>                # Site domain
```

### Config Classes

**Location:** `sites/{sitename}/config.py`

```python
class Config:
    """Base configuration"""
    SITE_NAME = 'My Site'
    SITE_TAGLINE = 'My tagline'

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_ECHO = True

class ProductionConfig(Config):
    DEBUG = False
```

## Security Features Built-In

1. **CSRF Protection**: All forms automatically protected
2. **Rate Limiting**: Configurable per-route limits
3. **Password Hashing**: Bcrypt with proper salt
4. **HTML Sanitization**: XSS prevention via bleach
5. **Session Security**: Secure cookies, httponly, samesite
6. **SQL Injection**: Protected via SQLAlchemy ORM
7. **File Upload Validation**: Type and size checking
8. **HTTPS Enforcement**: HTTP redirects to HTTPS (nginx)

## Common Code Patterns

### Authentication Check

```python
from flask_login import current_user, login_required
from shared.decorators import admin_required

@app.route('/protected')
@login_required
def protected():
    return f"Hello {current_user.username}"

@app.route('/admin-only')
@admin_required
def admin_only():
    return "Admin area"
```

### Email Sending

```python
from shared.email import send_email

send_email(
    subject='Test Email',
    recipients=['user@example.com'],
    text_body='Plain text content',
    html_body='<p>HTML content</p>'
)
```

### Image Upload

```python
from shared.image_handler import save_image, allowed_file

if 'file' in request.files:
    file = request.files['file']
    if allowed_file(file.filename):
        result = save_image(file, upload_dir, resize=True)
        # result = {'filename': ..., 'filepath': ..., ...}
```

### Form Handling

```python
from shared.forms import ContactForm

form = ContactForm()
if form.validate_on_submit():
    # Form is valid, process it
    name = form.name.data
    email = form.email.data
    message = form.message.data
```

### Database Queries

```python
# Get single record
user = User.query.filter_by(username='admin').first_or_404()

# Get multiple records
posts = BlogPost.query.filter_by(visible=True).all()

# Pagination
posts = BlogPost.query.order_by(BlogPost.created_at.desc()).paginate(
    page=page, per_page=20, error_out=False
)

# Count
count = ContactSubmission.query.filter_by(status='new').count()
```

## Testing Approach

### Manual Testing (Current)

Each site has a testing checklist in its README. Key areas:
- Public pages load correctly
- Forms submit and validate
- Admin login/logout
- CRUD operations for blog posts
- Contact form submissions
- Rate limiting
- Email delivery

### Unit Testing (Future)

Planned framework: pytest
Test structure: `sites/{sitename}/tests/`

## Deployment Architecture

### Production Stack

```
Internet
  ↓
Nginx (Port 80/443)
  ↓ Reverse Proxy
Gunicorn (Port 8001/8002/...)
  ↓
Flask Application
  ↓
PostgreSQL
```

### Service Management

```bash
# systemd services
sudo systemctl start webgarden-therapist
sudo systemctl start webgarden-keystone

# Wrapper script
sudo /var/www/webgarden/deploy/webgarden-ctl.sh start therapist
sudo /var/www/webgarden/deploy/webgarden-ctl.sh logs therapist -f
```

### Deployment Process

1. **Automated setup:** `deploy/setup_site.sh {sitename} {domain}`
2. **Manual steps:**
   - Configure environment variables
   - Create admin user
   - Upload static assets
   - Test site

## CLI Commands Reference

### Site-Level Commands

**Location:** Run from `sites/{sitename}/` directory

```bash
# Activate virtualenv first
source venv/bin/activate

# Database
flask db init              # Initialize migrations (first time)
flask db migrate -m "msg"  # Create migration
flask db upgrade           # Apply migrations
flask db downgrade         # Rollback migration

# User management
flask create-admin         # Create admin user (interactive)
flask test-email           # Test email configuration

# Development
flask run --debug          # Run development server
flask shell               # Python shell with app context
```

### System-Level Commands

**Location:** Run from `/var/www/webgarden/` directory

```bash
# Service control
sudo deploy/webgarden-ctl.sh start therapist
sudo deploy/webgarden-ctl.sh stop therapist
sudo deploy/webgarden-ctl.sh restart therapist
sudo deploy/webgarden-ctl.sh status therapist
sudo deploy/webgarden-ctl.sh logs therapist [-f]

# New site creation
sudo deploy/new_site.sh <sitename> <domain> <port>

# Site setup
sudo deploy/setup_site.sh <sitename> <domain>
```

## Troubleshooting Quick Reference

### Issue: ImportError for shared modules

**Cause:** Python path not set correctly

**Fix:**
```python
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
```

(Already in app.py of each site)

### Issue: Database connection error

**Check:**
1. PostgreSQL running: `sudo systemctl status postgresql`
2. Database exists: `sudo -u postgres psql -l | grep {sitename}`
3. DATABASE_URL correct in env file

### Issue: Templates not found

**Check:**
1. Template exists in `sites/{sitename}/templates/`
2. Jinja2 loader configured correctly in `create_base_app()`
3. Template name matches exactly (case-sensitive)

### Issue: Static files not loading

**Check:**
1. Files exist in `sites/{sitename}/static/`
2. Nginx configured to serve /static/ (production)
3. Using correct URL: `url_for('static', filename='css/style.css')`

### Issue: Email not sending

**Check:**
1. Mailgun credentials in env file
2. MAIL_* variables set correctly
3. Sender email verified in Mailgun
4. Check logs: `sudo journalctl -u webgarden-{sitename} -n 50`

## Git Workflow

### Branch Strategy

- `main`: Production-ready code
- Feature branches: `feature/description`
- Hotfix branches: `hotfix/description`

### Commit Messages

Follow conventional commits:
- `feat: Add new contact form field`
- `fix: Resolve email sending issue`
- `docs: Update shared modules documentation`
- `refactor: Simplify image upload logic`

## Performance Considerations

### Database
- Connection pooling enabled (pool_pre_ping=True)
- Indexes on: username, email, slug, submitted_at, published_at
- Use pagination for large result sets

### Static Files
- Images auto-resized on upload
- Consider CDN for production
- Nginx serves static files directly

### Caching
- Not currently implemented
- Consider Flask-Caching for frequently accessed data

## Extension Points

### Adding a New Site

1. Copy existing site: `cp -r sites/therapist sites/newsite`
2. Update `config.py` with new site info
3. Update `app.py` site name
4. Customize templates and static files
5. Run deployment script: `deploy/new_site.sh newsite domain.com 8003`

### Adding New Shared Models

1. Add to `shared/models.py`
2. Create migration: `flask db migrate -m "Add Model"`
3. Review and apply: `flask db upgrade`
4. Use in sites as needed

### Adding New Flask Extensions

1. Add to `requirements.txt`
2. Initialize in `shared/base_app.py`
3. Configure in site's `config.py`
4. Use in routes

## Code Style Conventions

- **Python:** Follow PEP 8
- **Docstrings:** Google style
- **Imports:** Grouped (stdlib, third-party, local)
- **Routes:** Docstrings with description
- **Templates:** 2-space indentation
- **CSS/JS:** 2-space indentation

## Important Notes for AI Assistants

1. **Always use shared modules** when functionality exists there
2. **Check site-specific config** before making assumptions
3. **Environment variables** differ per site
4. **Database migrations** must be created and applied
5. **Security is paramount** - never skip validation/sanitization
6. **Each site is independent** but shares core functionality
7. **Templates extend base.html** from shared/templates/
8. **Static files are site-specific** in sites/{sitename}/static/
9. **All forms need CSRF tokens** (automatic with WTForms)
10. **Rate limiting is configured** but can be adjusted per route

## Quick Navigation

- **Main Docs:** `/README.md`
- **Shared Modules:** `/shared/README.md`
- **Therapist Site:** `/sites/therapist/README.md`
- **Keystone Site:** `/sites/keystone/README.md`
- **Deployment:** `/deploy/README.md`
- **Changelog:** `/CHANGELOG.md`

## Version Info

- **Python:** 3.10+
- **Flask:** 3.0+
- **SQLAlchemy:** 2.0+
- **PostgreSQL:** 12+
- **Bootstrap:** 5.3+

## Support Resources

- Flask Documentation: https://flask.palletsprojects.com/
- SQLAlchemy Documentation: https://docs.sqlalchemy.org/
- Jinja2 Documentation: https://jinja.palletsprojects.com/
- WTForms Documentation: https://wtforms.readthedocs.io/

---

**Last Updated:** 2025-11-25
**Maintained For:** Claude Sonnet 4.5 and other AI assistants

This documentation is designed to provide AI assistants with a comprehensive understanding of the WebGarden project for efficient code generation, debugging, and maintenance assistance.
