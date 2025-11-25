# WebGarden Architecture Documentation

## System Architecture Overview

WebGarden is a multi-site Flask hosting platform designed to efficiently host multiple small business websites from a single codebase using a monorepo architecture.

### Design Goals

1. **Code Reusability**: Share common functionality across all sites
2. **Site Independence**: Each site can be customized without affecting others
3. **Easy Scalability**: Adding new sites should be straightforward
4. **Production-Ready**: Built-in security, monitoring, and deployment automation
5. **Maintainability**: Clear separation of concerns and comprehensive documentation

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        Internet (HTTPS)                      │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    Nginx Reverse Proxy                       │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │ therapist.   │  │ keystone.    │  │ future.      │     │
│  │ domain.com   │  │ domain.com   │  │ domain.com   │     │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘     │
└─────────┼──────────────────┼──────────────────┼─────────────┘
          │                  │                  │
          │ :8001            │ :8002            │ :8003
          ▼                  ▼                  ▼
┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
│   Gunicorn      │  │   Gunicorn      │  │   Gunicorn      │
│   (4 workers)   │  │   (4 workers)   │  │   (4 workers)   │
└─────────┬───────┘  └─────────┬───────┘  └─────────┬───────┘
          │                    │                    │
          ▼                    ▼                    ▼
┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
│ Flask App       │  │ Flask App       │  │ Flask App       │
│ (Therapist)     │  │ (Keystone)      │  │ (Future Site)   │
│                 │  │                 │  │                 │
│ Uses:           │  │ Uses:           │  │ Uses:           │
│ - Shared Models │  │ - Shared Models │  │ - Shared Models │
│ - Shared Forms  │  │ - Shared Forms  │  │ - Shared Forms  │
│ - Shared Utils  │  │ - Shared Utils  │  │ - Shared Utils  │
└─────────┬───────┘  └─────────┬───────┘  └─────────┬───────┘
          │                    │                    │
          └────────────────────┴────────────────────┘
                            │
                            ▼
                  ┌───────────────────┐
                  │   PostgreSQL      │
                  │   Database        │
                  │                   │
                  │ ┌───────────────┐ │
                  │ │ therapist_db  │ │
                  │ └───────────────┘ │
                  │ ┌───────────────┐ │
                  │ │ keystone_db   │ │
                  │ └───────────────┘ │
                  └───────────────────┘
```

## Application Architecture

### Layered Architecture

```
┌──────────────────────────────────────────────────────────┐
│                    Presentation Layer                     │
│  (Templates, Static Files, Frontend JavaScript)          │
└───────────────────────────┬──────────────────────────────┘
                            │
┌───────────────────────────▼──────────────────────────────┐
│                    Application Layer                      │
│  (Flask Routes, View Functions, Form Handlers)           │
└───────────────────────────┬──────────────────────────────┘
                            │
┌───────────────────────────▼──────────────────────────────┐
│                    Business Logic Layer                   │
│  (Models, Validators, Email, Image Processing)           │
└───────────────────────────┬──────────────────────────────┘
                            │
┌───────────────────────────▼──────────────────────────────┐
│                    Data Access Layer                      │
│  (SQLAlchemy ORM, Database Queries)                      │
└───────────────────────────┬──────────────────────────────┘
                            │
┌───────────────────────────▼──────────────────────────────┐
│                    Database Layer                         │
│  (PostgreSQL)                                            │
└──────────────────────────────────────────────────────────┘
```

## Component Architecture

### Shared Modules System

The shared modules provide a foundation that all sites build upon:

```
┌─────────────────────────────────────────────────────────┐
│                    Shared Modules                        │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │  base_app.py │  │  models.py   │  │  forms.py    │ │
│  │              │  │              │  │              │ │
│  │ • App factory│  │ • User       │  │ • Contact    │ │
│  │ • Extensions │  │ • BlogPost   │  │ • Login      │ │
│  │ • Config     │  │ • Contact    │  │ • BlogPost   │ │
│  │ • Errors     │  │ • Upload     │  │ • User       │ │
│  └──────────────┘  └──────────────┘  └──────────────┘ │
│                                                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │  email.py    │  │image_handler │  │sanitizer.py  │ │
│  │              │  │              │  │              │ │
│  │ • Send email │  │ • Save image │  │ • Clean HTML │ │
│  │ • Contact    │  │ • Resize     │  │ • Excerpt    │ │
│  │   notif      │  │ • Thumbnail  │  │              │ │
│  │ • Confirm    │  │ • Validate   │  │              │ │
│  └──────────────┘  └──────────────┘  └──────────────┘ │
│                                                          │
│  ┌──────────────┐  ┌──────────────┐                    │
│  │decorators.py │  │   auth.py    │                    │
│  │              │  │              │                    │
│  │ • @login_req │  │ • Password   │                    │
│  │ • @admin_req │  │   helpers    │                    │
│  │ • @anon_req  │  │ • Session    │                    │
│  └──────────────┘  └──────────────┘                    │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

### Flask Extensions Integration

```
┌─────────────────────────────────────────────────────────┐
│               Flask Application Context                  │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  Flask-SQLAlchemy     ─────►  Database ORM              │
│  Flask-Migrate        ─────►  Database Migrations       │
│  Flask-Login          ─────►  User Authentication       │
│  Flask-Bcrypt         ─────►  Password Hashing          │
│  Flask-Mail           ─────►  Email Sending             │
│  Flask-WTF            ─────►  Form Handling + CSRF      │
│  Flask-Limiter        ─────►  Rate Limiting             │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

## Data Flow

### Request Processing Flow

```
1. Client Request
   │
   ▼
2. Nginx receives request
   │ (SSL termination, static file serving)
   ▼
3. Nginx forwards to Gunicorn (if not static)
   │
   ▼
4. Gunicorn worker picks up request
   │
   ▼
5. Flask application receives request
   │
   ├─► CSRF validation (if POST)
   ├─► Rate limit check
   ├─► Session validation
   │
   ▼
6. Route handler executes
   │
   ├─► Load user session (if authenticated)
   ├─► Process form data (if form submission)
   ├─► Query database (if needed)
   ├─► Business logic execution
   │
   ▼
7. Template rendering
   │ (Jinja2 with context data)
   ▼
8. Response sent back
   │
   ├─► Through Gunicorn
   ├─► Through Nginx
   │
   ▼
9. Client receives response
```

### Form Submission Flow

```
User submits form
   │
   ▼
POST request to Flask
   │
   ├─► CSRF token validation ────► Fail? ──► 400 Error
   │   (Flask-WTF)                    │
   │                                  ▼
   │                                Pass
   ▼
Rate limit check ──────────────► Exceeded? ──► 429 Error
   │                                  │
   │                                  ▼
   │                               Within limit
   ▼
Form validation
   │ (WTForms validators)
   │
   ├─► Valid? ────► No ──► Re-render with errors
   │       │
   │       Yes
   ▼
Business logic
   │
   ├─► Create database record
   ├─► Send emails (if applicable)
   ├─► Process uploads (if applicable)
   │
   ▼
Flash success message
   │
   ▼
Redirect to prevent resubmission
```

## Database Architecture

### Schema Design

```
users
├── id (PK)
├── username (UNIQUE, INDEXED)
├── email (UNIQUE, INDEXED)
├── password_hash
├── role ('admin' | 'editor')
├── created_at
└── last_login

blog_posts
├── id (PK)
├── title
├── slug (UNIQUE, INDEXED)
├── content (TEXT)
├── author_id (FK → users.id)
├── published_at (INDEXED)
├── updated_at
└── visible (BOOLEAN)

contact_submissions
├── id (PK)
├── name
├── email
├── phone
├── message (TEXT)
├── submitted_at (INDEXED)
├── status ('new'|'read'|'responded')
└── notes (TEXT)

uploaded_files
├── id (PK)
├── filename
├── original_filename
├── filepath
├── file_size
├── mime_type
├── uploaded_by (FK → users.id)
└── uploaded_at (INDEXED)
```

### Database Access Patterns

**Connection Management:**
- Connection pooling enabled
- Pre-ping to detect stale connections
- Connections recycled every 5 minutes
- Graceful handling of connection failures

**Query Optimization:**
- Indexes on frequently queried fields
- Pagination for large result sets
- Eager loading for relationships when needed
- Query result caching (future enhancement)

## Security Architecture

### Defense in Depth

```
┌─────────────────────────────────────────────────────────┐
│                    Security Layers                       │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  Layer 1: Network                                        │
│  ├─ HTTPS enforced (Let's Encrypt SSL)                 │
│  ├─ HTTP redirects to HTTPS                             │
│  └─ Rate limiting at nginx level                        │
│                                                          │
│  Layer 2: Application                                    │
│  ├─ CSRF protection (Flask-WTF)                         │
│  ├─ Rate limiting (Flask-Limiter)                       │
│  ├─ Input validation (WTForms)                          │
│  ├─ HTML sanitization (bleach)                          │
│  └─ File upload validation                              │
│                                                          │
│  Layer 3: Authentication                                 │
│  ├─ Bcrypt password hashing                             │
│  ├─ Secure session cookies                              │
│  ├─ Role-based access control                           │
│  └─ Login attempt throttling                            │
│                                                          │
│  Layer 4: Data                                           │
│  ├─ SQL injection prevention (ORM)                      │
│  ├─ XSS prevention (sanitization)                       │
│  ├─ CSRF token on all forms                             │
│  └─ Parameterized queries                               │
│                                                          │
│  Layer 5: Infrastructure                                 │
│  ├─ Firewall rules                                      │
│  ├─ Regular security updates                            │
│  ├─ Database access restrictions                        │
│  └─ Secrets in environment variables                    │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

### Authentication Flow

```
User Login Attempt
   │
   ▼
Rate limit check (5 per 15 min)
   │
   ├─► Exceeded? ──► Block with 429
   │       │
   │       OK
   ▼
Retrieve user by username
   │
   ├─► User exists?
   │       │
   │       ├─ Yes ──► Check password (bcrypt)
   │       │              │
   │       │              ├─ Match? ──► Yes ──┐
   │       │              │                   │
   │       │              └─ No ───────────┐  │
   │       │                                │  │
   │       └─ No ─────────────────────────►│  │
   │                                        │  │
   ▼                                        ▼  ▼
Invalid credentials                    Log    Create
Flash error                           failure session
   │                                     │     │
   │                                     │     ├─ Set secure cookie
   │                                     │     ├─ Update last_login
   │                                     │     └─ Load user object
   │                                     │           │
   │                                     │           ▼
   └─────────────────────────────────────┴──► Redirect to dashboard
```

## Deployment Architecture

### Production Environment

```
┌──────────────────────────────────────────────────────────┐
│                      VPS/Dedicated Server                 │
├──────────────────────────────────────────────────────────┤
│                                                           │
│  Debian/Ubuntu Linux                                      │
│  ├─ Python 3.10+ virtualenvs                             │
│  ├─ Nginx 1.18+                                          │
│  ├─ PostgreSQL 12+                                       │
│  ├─ Certbot (Let's Encrypt)                              │
│  └─ systemd (process management)                         │
│                                                           │
│  Directory Structure:                                     │
│  /var/www/webgarden/                                     │
│  ├─ shared/          (shared modules)                    │
│  ├─ sites/           (individual sites)                  │
│  │  ├─ therapist/                                        │
│  │  │  └─ venv/      (isolated virtualenv)              │
│  │  └─ keystone/                                         │
│  │     └─ venv/      (isolated virtualenv)              │
│  ├─ deploy/          (deployment scripts)                │
│  └─ uploads/         (file uploads per site)             │
│                                                           │
│  Configuration:                                           │
│  /etc/webgarden/                                         │
│  ├─ therapist.env    (site environment variables)        │
│  └─ keystone.env     (site environment variables)        │
│                                                           │
│  Systemd Services:                                        │
│  /etc/systemd/system/                                    │
│  ├─ webgarden-therapist.service                          │
│  └─ webgarden-keystone.service                           │
│                                                           │
│  Nginx Configuration:                                     │
│  /etc/nginx/                                             │
│  ├─ sites-available/                                     │
│  │  ├─ therapist                                         │
│  │  └─ keystone                                          │
│  └─ sites-enabled/   (symlinks)                          │
│                                                           │
│  SSL Certificates:                                        │
│  /etc/letsencrypt/live/                                  │
│  ├─ therapist.domain.com/                                │
│  └─ keystone.domain.com/                                 │
│                                                           │
└──────────────────────────────────────────────────────────┘
```

### Service Management

Each site runs as an independent systemd service:

**Service Configuration:**
```ini
[Unit]
Description=WebGarden Therapist Site
After=network.target postgresql.service

[Service]
Type=notify
User=webgarden
Group=webgarden
WorkingDirectory=/var/www/webgarden/sites/therapist
EnvironmentFile=/etc/webgarden/therapist.env
ExecStart=/var/www/webgarden/sites/therapist/venv/bin/gunicorn \
    --bind 127.0.0.1:8001 \
    --workers 4 \
    --worker-class sync \
    --timeout 120 \
    --access-logfile /var/log/webgarden/therapist-access.log \
    --error-logfile /var/log/webgarden/therapist-error.log \
    app:app
ExecReload=/bin/kill -s HUP $MAINPID
Restart=always

[Install]
WantedBy=multi-user.target
```

## Scalability Considerations

### Current Scale

- **Sites:** 2 (therapist, keystone)
- **Traffic:** Low to medium (< 10k requests/day per site)
- **Database:** Single PostgreSQL instance, separate DB per site
- **Workers:** 4 Gunicorn workers per site

### Scaling Strategy

#### Vertical Scaling (Current Approach)
- Increase server resources (CPU, RAM)
- Increase Gunicorn workers
- Optimize database queries
- Add Redis for caching

#### Horizontal Scaling (Future)
- Load balancer in front of multiple servers
- Database replication (read replicas)
- Shared session storage (Redis)
- CDN for static assets
- Object storage for uploads (S3-compatible)

### Performance Optimizations

**Current:**
- Connection pooling
- Image resizing on upload
- Indexed database columns
- Static file serving by nginx

**Planned:**
- Redis caching layer
- CDN integration
- Database query caching
- Lazy loading for images
- Asset minification and bundling

## Monitoring & Logging

### Log Locations

```
Application Logs:
├─ systemd journal: journalctl -u webgarden-{sitename}
├─ Gunicorn access: /var/log/webgarden/{sitename}-access.log
└─ Gunicorn error:  /var/log/webgarden/{sitename}-error.log

Web Server Logs:
├─ Nginx access: /var/log/nginx/{sitename}-access.log
└─ Nginx error:  /var/log/nginx/{sitename}-error.log

Database Logs:
└─ PostgreSQL: /var/log/postgresql/postgresql-*.log
```

### Monitoring Approach

**Current (Manual):**
- Log file inspection
- systemctl status checks
- Database query logs
- Email delivery logs

**Planned:**
- Application metrics (Prometheus)
- Error tracking (Sentry)
- Uptime monitoring (UptimeRobot)
- Performance monitoring (New Relic)

## Backup Strategy

### Database Backups

```bash
# Daily backup script (cron)
#!/bin/bash
DATE=$(date +%Y%m%d)
sudo -u postgres pg_dump therapist_db > /var/www/webgarden/backups/databases/therapist_$DATE.sql
sudo -u postgres pg_dump keystone_db > /var/www/webgarden/backups/databases/keystone_$DATE.sql

# Retention: 30 days
find /var/www/webgarden/backups/databases/ -name "*.sql" -mtime +30 -delete
```

### File Backups

```bash
# Weekly backup of uploads
tar -czf /var/www/webgarden/backups/uploads/uploads_$DATE.tar.gz /var/www/webgarden/uploads/

# Retention: 90 days
find /var/www/webgarden/backups/uploads/ -name "*.tar.gz" -mtime +90 -delete
```

### Configuration Backups

```bash
# Before deployment
cp -r /etc/webgarden/ /var/www/webgarden/backups/config/config_$DATE/
cp -r /etc/nginx/sites-available/ /var/www/webgarden/backups/config/nginx_$DATE/
```

## Technology Stack

### Backend
- **Language:** Python 3.10+
- **Framework:** Flask 3.0+
- **ORM:** SQLAlchemy 2.0+
- **Migrations:** Alembic (via Flask-Migrate)
- **Authentication:** Flask-Login + Bcrypt
- **Forms:** WTForms + Flask-WTF
- **Email:** Flask-Mail (Mailgun)
- **Rate Limiting:** Flask-Limiter

### Frontend
- **CSS Framework:** Bootstrap 5.3
- **Icons:** Bootstrap Icons
- **JavaScript:** Vanilla JS (minimal)
- **Rich Text Editor:** TinyMCE
- **Forms:** HTML5 validation + WTForms

### Database
- **DBMS:** PostgreSQL 12+
- **Connection:** psycopg2-binary
- **Pooling:** SQLAlchemy built-in

### Web Server
- **Application Server:** Gunicorn
- **Reverse Proxy:** Nginx
- **SSL:** Let's Encrypt (Certbot)

### Process Management
- **Init System:** systemd
- **Service Control:** webgarden-ctl.sh wrapper

### Development Tools
- **Environment:** python-dotenv
- **Linting:** flake8 (planned)
- **Testing:** pytest (planned)
- **Version Control:** Git

## Design Patterns

### Application Factory Pattern

```python
# shared/base_app.py
def create_base_app(site_name, config_object=None):
    app = Flask(site_name)
    # Configure app
    # Initialize extensions
    # Register handlers
    return app

# sites/therapist/app.py
app = create_base_app('therapist', config['production'])
```

### Repository Pattern (via ORM)

```python
# Data access through SQLAlchemy models
user = User.query.filter_by(username='admin').first()
posts = BlogPost.query.filter_by(visible=True).all()
```

### Decorator Pattern

```python
# Shared decorators for common functionality
@app.route('/admin')
@login_required
@admin_required
def admin_panel():
    # Admin-only functionality
    pass
```

### Template Method Pattern

```python
# Base template with blocks
# sites extend and override specific blocks
{% extends "base.html" %}
{% block content %}
    <!-- Site-specific content -->
{% endblock %}
```

## Future Enhancements

### Short-term (Sprint 3-4)
- [ ] Automated testing suite (pytest)
- [ ] CI/CD pipeline
- [ ] Redis caching layer
- [ ] Enhanced admin dashboard
- [ ] Blog categories and tags

### Medium-term (Sprints 5-8)
- [ ] Calendar integration (Cal.com)
- [ ] Chat widget integration
- [ ] Advanced analytics
- [ ] API endpoints (REST)
- [ ] Multi-language support

### Long-term (Future)
- [ ] Microservices architecture
- [ ] GraphQL API
- [ ] Progressive Web App features
- [ ] Mobile app integration
- [ ] Advanced AI features

## Conclusion

WebGarden's architecture is designed to be:
- **Simple** yet powerful
- **Scalable** with clear upgrade paths
- **Maintainable** with comprehensive documentation
- **Secure** with defense-in-depth approach
- **Extensible** for future enhancements

The monorepo approach with shared modules allows for rapid development of new sites while maintaining consistency and reducing technical debt.

---

**Last Updated:** 2025-11-25
**Version:** 2.0 (Post-Sprint 2)
