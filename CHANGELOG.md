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

## [2.0.0] - 2025-11-25

### Added - Sprint 2 Complete
- ✅ Blog functionality with rich text editor (TinyMCE)
- ✅ Full admin panel for content management
- ✅ User authentication and login system with Flask-Login
- ✅ Image upload management and optimization
- ✅ Blog post creation and editing
- ✅ Contact submission management
- ✅ HTML sanitization and security features
- ✅ User role management (admin, editor)
- ✅ CLI commands for user management

## [3.0.0] - 2025-11-29

### Added - Sprint 3 Complete
- ✅ Automated site deployment script (new_site.sh)
- ✅ Site creation prompt template for Claude Code
- ✅ Complete deployment documentation
- ✅ Second production site (Keystone Hardscapes)
- ✅ Infrastructure templates for rapid site creation
- ✅ Nginx configuration templates
- ✅ Systemd service templates

## [4.0.0] - 2026-01-18

### Added - Sprint 4 Complete
- ✅ Self-contained JavaScript chat widget (bot-widget.js)
- ✅ Flask API proxy endpoint at /api/chat
- ✅ Session management with localStorage
- ✅ Mobile-responsive chat interface
- ✅ Typing indicators and auto-scroll
- ✅ Accessibility features (ARIA labels, keyboard navigation)
- ✅ Configurable bot names and themes per site
- ✅ Graceful error handling for offline scenarios
- ✅ Bot widget deployed on psyling site (Psyling Assistant)
- ✅ Bot widget deployed on keystone site (Keystone Assistant)
- ✅ API proxy integration with external bot service

### Technical Details
- Widget is fully self-contained with inline styles
- No external dependencies required
- Uses fetch API for communication
- Supports custom theming via data attributes
- Session persistence across page reloads
- Timeout handling for slow API responses

## [Future] - Sprint 5

### Planned
- [ ] Cal.com booking integration
- [ ] Advanced email templates
- [ ] Analytics dashboard
- [ ] Additional business sites as needed

---

## Version History

- **4.0.0** (2026-01-18): Sprint 4 Complete - AI Chatbot Integration
- **3.0.0** (2025-11-29): Sprint 3 Complete - Deployment Automation
- **2.0.0** (2025-11-25): Sprint 2 Complete - Blog & Admin Panel
- **1.0.0** (2025-11-12): Sprint 1 Complete - Therapist site MVP
- **0.1.0** (2025-11-12): Initial project setup
