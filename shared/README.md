# Shared Modules Documentation

The `shared/` directory contains common modules, utilities, and templates used across all WebGarden sites. This promotes code reuse, consistency, and maintainability.

## Overview

All WebGarden sites share:
- Flask application factory
- Database models
- Form definitions
- Email utilities
- Security features
- Template base layouts
- Authentication & authorization

## Module Reference

### base_app.py

Flask application factory and core extensions initialization.

**Key Functions:**

- `create_base_app(site_name, config_object=None)`: Creates and configures a Flask application instance
  - Initializes all Flask extensions (SQLAlchemy, Flask-Login, Flask-Mail, etc.)
  - Configures Jinja2 template loader for shared templates
  - Sets up security configurations (CSRF, session cookies, rate limiting)
  - Registers error handlers and template filters

**Extensions Initialized:**
- `db`: SQLAlchemy for database ORM
- `migrate`: Flask-Migrate for database migrations
- `login_manager`: Flask-Login for user session management
- `bcrypt`: Flask-Bcrypt for password hashing
- `mail`: Flask-Mail for email functionality
- `csrf`: CSRFProtect for CSRF protection
- `limiter`: Flask-Limiter for rate limiting (default: 100 requests/minute)

**Security Features:**
- Secure session cookies (httponly, secure, samesite='Lax')
- CSRF protection on all forms
- Rate limiting on endpoints
- Connection pooling with pre-ping and 5-minute recycle

**Template Filters:**
- `datetime`: Format datetime objects (default: `%Y-%m-%d %H:%M`)
- `date`: Format date objects (default: `%Y-%m-%d`)

### models.py

Database models used across all sites.

#### User Model

Admin and editor user accounts with role-based access control.

**Fields:**
- `id`: Primary key
- `username`: Unique username (indexed)
- `email`: Unique email address (indexed)
- `password_hash`: Bcrypt password hash
- `role`: User role ('admin' or 'editor')
- `created_at`: Account creation timestamp
- `last_login`: Last login timestamp

**Methods:**
- `set_password(password)`: Hash and store password
- `check_password(password)`: Verify password
- `update_last_login()`: Update last login timestamp
- `is_admin()`: Check if user has admin role

**Relationships:**
- `blog_posts`: One-to-many with BlogPost
- `uploaded_files`: One-to-many with UploadedFile

#### ContactSubmission Model

Contact form submissions from website visitors.

**Fields:**
- `id`: Primary key
- `name`: Submitter name
- `email`: Submitter email
- `phone`: Optional phone number
- `message`: Message content
- `submitted_at`: Submission timestamp (indexed)
- `status`: Submission status ('new', 'read', 'responded')
- `notes`: Admin notes

**Methods:**
- `mark_as_read()`: Change status to 'read'
- `mark_as_responded()`: Change status to 'responded'

#### BlogPost Model

Blog post content with publication management.

**Fields:**
- `id`: Primary key
- `title`: Post title
- `slug`: URL-friendly slug (unique, indexed)
- `content`: Post content (HTML)
- `author_id`: Foreign key to User
- `published_at`: Publication timestamp (indexed)
- `updated_at`: Last update timestamp
- `visible`: Publication visibility flag

**Methods:**
- `publish()`: Publish the post (sets published_at and visible=True)
- `unpublish()`: Unpublish the post (sets visible=False)
- `is_published()`: Check if post is published and visible

**Relationships:**
- `author`: Many-to-one with User

#### UploadedFile Model

Metadata for files uploaded through the system.

**Fields:**
- `id`: Primary key
- `filename`: Stored filename
- `original_filename`: Original filename
- `filepath`: Full file path
- `file_size`: File size in bytes
- `mime_type`: MIME type
- `uploaded_by`: Foreign key to User
- `uploaded_at`: Upload timestamp (indexed)

**Relationships:**
- `uploader`: Many-to-one with User

### forms.py

WTForms form definitions with validation.

#### ContactForm

Public contact form for visitor inquiries.

**Fields:**
- `name`: Required, 2-100 characters
- `email`: Required, valid email format
- `phone`: Optional, max 20 characters
- `message`: Required, 10-5000 characters

#### LoginForm

Admin/editor login form.

**Fields:**
- `username`: Required, 3-80 characters
- `password`: Required
- `remember_me`: Optional checkbox

#### BlogPostForm

Blog post creation and editing form.

**Fields:**
- `title`: Required, 5-200 characters
- `slug`: Optional URL slug (auto-generated from title if empty)
- `content`: Required, rich text content
- `visible`: Published status checkbox

#### UserForm

User account creation/editing form.

**Fields:**
- `username`: Required, 3-80 characters, must be unique
- `email`: Required, valid email, must be unique
- `password`: Optional (for edits), min 8 characters
- `password_confirm`: Must match password
- `role`: Select 'editor' or 'admin'

**Validators:**
- Username uniqueness validation
- Email uniqueness validation
- Password confirmation matching

### email.py

Email sending utilities with Mailgun integration via Flask-Mail.

#### Core Functions

**`send_email(subject, recipients, text_body=None, html_body=None, sender=None)`**

Send an email via Mailgun.

Parameters:
- `subject`: Email subject line
- `recipients`: List of recipient email addresses (or single string)
- `text_body`: Plain text email body
- `html_body`: HTML email body
- `sender`: Sender email (uses MAIL_DEFAULT_SENDER if not provided)

Returns: `True` if sent successfully, `False` otherwise

**`send_contact_notification(contact_submission)`**

Sends notification to admin when contact form is submitted.

Parameters:
- `contact_submission`: ContactSubmission model instance

Features:
- Professionally formatted HTML email
- Includes all submission details
- Sent to ADMIN_EMAIL or MAIL_DEFAULT_SENDER

**`send_contact_confirmation(contact_submission)`**

Sends confirmation email to person who submitted contact form.

Parameters:
- `contact_submission`: ContactSubmission model instance

Features:
- Thank you message
- Quote of their original message
- Professional branding

### decorators.py

Custom decorators for route protection.

**`@login_required`**

Require user to be authenticated. Redirects to login page if not authenticated.

**`@admin_required`**

Require user to be authenticated AND have admin role. Returns 403 if not admin.

**`@anonymous_required`**

Require user to NOT be authenticated (for login/register pages). Redirects to dashboard if already logged in.

### sanitizer.py

HTML sanitization and text processing utilities.

**`sanitize_html(html_content, allowed_tags=None, allowed_attributes=None)`**

Sanitize HTML content to prevent XSS attacks using bleach library.

Default allowed tags: `p, br, strong, em, u, h1-h6, ul, ol, li, a, img, blockquote, code, pre`

Default allowed attributes:
- `a`: href, title, target
- `img`: src, alt, width, height

Parameters:
- `html_content`: Raw HTML content
- `allowed_tags`: Custom list of allowed tags (optional)
- `allowed_attributes`: Custom dict of allowed attributes (optional)

Returns: Sanitized HTML string

**`create_excerpt(html_content, max_length=150)`**

Create plain text excerpt from HTML content.

Parameters:
- `html_content`: HTML content
- `max_length`: Maximum excerpt length in characters

Returns: Plain text excerpt with ellipsis if truncated

Features:
- Strips all HTML tags
- Respects word boundaries
- Adds ellipsis (...) if truncated

### image_handler.py

Image upload and processing utilities.

**`allowed_file(filename)`**

Check if file extension is allowed.

Allowed extensions: `png, jpg, jpeg, gif, webp`

**`save_image(file, upload_dir, resize=True, max_width=1200, max_height=1200, create_thumbnail=True, thumb_size=(300, 300))`**

Save and process uploaded image.

Parameters:
- `file`: FileStorage object from request.files
- `upload_dir`: Directory to save file
- `resize`: Resize large images (default: True)
- `max_width`: Maximum width in pixels (default: 1200)
- `max_height`: Maximum height in pixels (default: 1200)
- `create_thumbnail`: Generate thumbnail (default: True)
- `thumb_size`: Thumbnail size tuple (default: 300x300)

Returns: Dictionary with file metadata or None if failed
```python
{
    'filename': 'uuid-filename.jpg',
    'original_filename': 'original.jpg',
    'filepath': '/full/path/to/file.jpg',
    'file_size': 123456,
    'thumbnail_path': '/full/path/to/thumb_file.jpg'  # if create_thumbnail=True
}
```

Features:
- Generates UUID-based filenames
- Maintains aspect ratio when resizing
- Supports EXIF orientation correction
- Creates thumbnails with proper scaling
- Validates file types

### auth.py

Authentication utilities and helpers.

**Functions for password management, session handling, and user verification.**

## Template Structure

```
shared/templates/
├── base.html              # Base template with common structure
└── errors/
    ├── 403.html          # Forbidden error page
    ├── 404.html          # Not found error page
    └── 500.html          # Server error page
```

### base.html

Master template providing:
- Common HTML structure
- Meta tags and SEO
- Navigation structure
- Footer
- Flash message display
- Block definitions for:
  - `title`: Page title
  - `extra_css`: Additional CSS
  - `content`: Main content area
  - `extra_js`: Additional JavaScript

Sites extend this template and override blocks as needed.

## Configuration Requirements

Sites using these shared modules must provide these environment variables:

### Required Variables

```bash
# Flask
SECRET_KEY=<random-secret-key>
FLASK_ENV=production

# Database
DATABASE_URL=postgresql://user:password@localhost/database_name

# Mail (Mailgun)
MAIL_SERVER=smtp.mailgun.org
MAIL_PORT=587
MAIL_USERNAME=postmaster@yourdomain.com
MAIL_PASSWORD=<mailgun-api-key>
MAIL_DEFAULT_SENDER=noreply@yourdomain.com
ADMIN_EMAIL=admin@yourdomain.com

# Site
SITE_NAME=Your Site Name
SITE_DOMAIN=yourdomain.com
UPLOAD_FOLDER=/path/to/uploads
MAX_UPLOAD_SIZE=5242880  # 5MB in bytes
```

### Optional Variables

```bash
# Rate Limiting
CONTACT_FORM_RATE_LIMIT="5 per hour"

# Session
PERMANENT_SESSION_LIFETIME=3600  # seconds
```

## Usage Examples

### Creating a New Site

```python
# sites/newsite/app.py
from shared.base_app import create_base_app, db, login_manager
from shared.models import User, ContactSubmission, BlogPost
from shared.forms import ContactForm, LoginForm
from shared.email import send_contact_notification
from sites.newsite.config import config

# Create app
app = create_base_app('newsite', config['production'])

# Define routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        submission = ContactSubmission(
            name=form.name.data,
            email=form.email.data,
            message=form.message.data
        )
        db.session.add(submission)
        db.session.commit()
        send_contact_notification(submission)
        flash('Thank you for your message!', 'success')
        return redirect(url_for('contact'))
    return render_template('contact.html', form=form)
```

### Using Models

```python
from shared.models import User, BlogPost, ContactSubmission
from shared.base_app import db

# Create user
user = User(username='admin', email='admin@example.com', role='admin')
user.set_password('secure_password')
db.session.add(user)
db.session.commit()

# Create blog post
post = BlogPost(
    title='My First Post',
    slug='my-first-post',
    content='<p>Hello world!</p>',
    author_id=user.id
)
post.publish()
db.session.add(post)
db.session.commit()

# Query submissions
new_contacts = ContactSubmission.query.filter_by(status='new').all()
```

### Using Decorators

```python
from shared.decorators import login_required, admin_required

@app.route('/admin/dashboard')
@login_required
def dashboard():
    return render_template('admin/dashboard.html')

@app.route('/admin/users')
@admin_required
def manage_users():
    users = User.query.all()
    return render_template('admin/users.html', users=users)
```

## Security Considerations

### Password Security
- Passwords are hashed with bcrypt (cost factor 12)
- Never store plain text passwords
- Use `user.set_password()` and `user.check_password()`

### Input Validation
- All forms have validators
- HTML content is sanitized before storage
- File uploads are validated by type and size

### CSRF Protection
- All forms must include `{{ form.csrf_token() }}`
- AJAX requests need CSRF token in headers

### Rate Limiting
- Contact forms: 5 submissions per hour per IP
- Login attempts: 5 attempts per 15 minutes per IP
- Custom limits: Use `@limiter.limit()` decorator

### SQL Injection Protection
- Always use SQLAlchemy ORM queries
- Never use raw SQL with user input
- Use parameterized queries if raw SQL is necessary

## Testing

### Unit Testing Models

```python
import pytest
from shared.models import User, BlogPost
from shared.base_app import db

def test_user_password():
    user = User(username='test', email='test@test.com')
    user.set_password('password123')
    assert user.check_password('password123')
    assert not user.check_password('wrong')

def test_blog_post_publish():
    post = BlogPost(title='Test', slug='test', content='Content')
    assert not post.is_published()
    post.publish()
    assert post.is_published()
    assert post.visible == True
    assert post.published_at is not None
```

### Integration Testing

```python
def test_contact_form_submission(client):
    response = client.post('/contact', data={
        'name': 'Test User',
        'email': 'test@example.com',
        'message': 'This is a test message'
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b'Thank you' in response.data

    # Verify database record
    submission = ContactSubmission.query.filter_by(email='test@example.com').first()
    assert submission is not None
    assert submission.name == 'Test User'
```

## Database Migrations

### Creating Migrations

```bash
# Initialize migrations (first time only)
flask db init

# Create migration after model changes
flask db migrate -m "Add new field to User model"

# Review the generated migration file in migrations/versions/

# Apply migration
flask db upgrade

# Rollback if needed
flask db downgrade
```

### Migration Best Practices

1. **Always review generated migrations** - Alembic may not detect all changes
2. **Test migrations on development first** - Verify they work before production
3. **Backup database before migrating** - Always have a rollback plan
4. **Use descriptive migration messages** - Helps track changes over time
5. **Don't modify migrations after applying** - Create new migrations instead

## Performance Considerations

### Database
- Connection pooling enabled (pool_pre_ping=True)
- Connections recycled every 5 minutes
- Use indexes on frequently queried fields (username, email, slug)
- Use pagination for large result sets

### Caching
- Consider implementing Flask-Caching for frequently accessed data
- Cache blog posts, user sessions, and static content

### File Uploads
- Images automatically resized to reduce storage
- Thumbnails generated for gallery displays
- Consider CDN for serving static files in production

## Maintenance

### Routine Tasks

1. **Monitor logs** - Check for errors and security issues
2. **Update dependencies** - Keep packages current for security
3. **Backup database** - Regular automated backups
4. **Clean upload directory** - Remove orphaned files periodically
5. **Review user accounts** - Audit admin access regularly

### Debugging

Enable debug mode for development:
```python
# In config.py
class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_ECHO = True  # Log SQL queries
```

View SQL queries:
```python
from flask import current_app
current_app.config['SQLALCHEMY_ECHO'] = True
```

## Support

For issues with shared modules:
1. Check the logs for error messages
2. Verify environment variables are set correctly
3. Ensure database migrations are up to date
4. Review the example code in this documentation
5. Check individual module docstrings for detailed information
