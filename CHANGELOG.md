# Changelog

All notable changes to WebGarden will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-11-12

### Added - Sprint 1 Complete
- ✅ Complete project structure with monorepo architecture
- ✅ Shared modules library (base_app, models, forms, email, image_handler)
- ✅ Therapist psychotherapy website (MVP)
  - Home page with hero section and features
  - About page with professional bio and credentials
  - Services page with detailed offerings
  - Contact page with functional form
- ✅ Database schema and models
  - Users table for admin access
  - Contact submissions table
  - Blog posts table (prepared for Sprint 2)
  - Uploaded files metadata table
- ✅ Flask application factory pattern
- ✅ Bootstrap 5 responsive design
- ✅ Custom CSS and JavaScript
- ✅ Email functionality with Mailgun integration
- ✅ Form validation and CSRF protection
- ✅ Rate limiting for contact form
- ✅ Deployment configurations
  - Nginx virtual host with SSL support
  - Systemd service files
  - Gunicorn WSGI server setup
- ✅ Management scripts
  - webgarden-ctl.sh for service control
  - setup_site.sh for automated deployment
- ✅ Database migrations with Flask-Migrate
- ✅ Comprehensive documentation
- ✅ Security features
  - HTTPS enforcement
  - Secure session cookies
  - Input validation
  - SQL injection protection
  - Security headers

### Security
- Implemented CSRF protection on all forms
- Added rate limiting (100 requests/minute, 5 contact submissions/hour)
- Configured secure session cookies
- Added security headers (HSTS, X-Frame-Options, etc.)

## [Unreleased] - Sprint 2

### Planned
- [ ] Blog functionality with rich text editor (TinyMCE)
- [ ] Admin panel with Flask-Admin
- [ ] User authentication and login system
- [ ] Image upload management
- [ ] Blog post creation and editing
- [ ] User role management (admin, editor)

## [Future] - Sprint 3

### Planned
- [ ] Cal.com booking integration
- [ ] Bot widget integration
- [ ] Advanced email templates
- [ ] Appointment scheduling

## [Future] - Sprint 4

### Planned
- [ ] Handyman business site
- [ ] Computer lab site
- [ ] Multi-user support
- [ ] Advanced analytics

---

## Version History

- **1.0.0** (2025-11-12): Sprint 1 Complete - Therapist site MVP
- **0.1.0** (2025-11-12): Initial project setup
