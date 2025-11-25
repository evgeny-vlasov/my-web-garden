# Therapist Site Documentation

Professional psychotherapy website built on the WebGarden platform.

## Site Overview

The therapist site provides a professional online presence for a psychotherapy practice, featuring:
- Information about services and approach
- Contact form for inquiries
- Blog with mental health articles
- Admin panel for content management
- Contact submission management

## Site Structure

```
sites/therapist/
├── app.py                 # Main Flask application
├── config.py              # Site configuration
├── cli.py                 # CLI commands
├── requirements.txt       # Python dependencies
├── templates/             # Site-specific templates
│   ├── index.html        # Home page
│   ├── about.html        # About the therapist
│   ├── services.html     # Services offered
│   ├── contact.html      # Contact form
│   ├── post.html         # Blog post view
│   └── admin/            # Admin panel templates
│       ├── login.html
│       ├── dashboard.html
│       ├── posts_list.html
│       ├── post_form.html
│       ├── contacts_list.html
│       └── components/   # Reusable admin components
├── static/               # Static assets
│   ├── css/
│   │   └── style.css    # Site-specific styles
│   ├── js/
│   │   └── main.js      # Site-specific JavaScript
│   └── images/          # Site images
└── migrations/          # Database migrations
    └── versions/        # Migration files
```

## Routes

### Public Routes

#### `GET /`
**Home Page**
- Displays welcome message and site overview
- Shows 3 most recent blog posts
- Call-to-action for booking consultation

Template: `templates/index.html`

#### `GET /about`
**About Page**
- Therapist biography and credentials
- Professional approach and philosophy
- Education and certifications

Template: `templates/about.html`

#### `GET /services`
**Services Page**
- Detailed service descriptions
- Therapy approaches used
- Session information and pricing
- Specializations

Template: `templates/services.html`

#### `GET /contact` | `POST /contact`
**Contact Form**
- Contact form submission
- Rate limited: 5 submissions per hour per IP
- Sends notification email to admin
- Sends confirmation email to visitor

Form: `ContactForm`
Template: `templates/contact.html`

**POST Data:**
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "phone": "+1234567890",
  "message": "I would like to schedule a consultation..."
}
```

#### `GET /post/<slug>`
**View Blog Post**
- Display single blog post by URL slug
- Shows 3 related/recent posts in sidebar
- Only shows published posts
- 404 if post not found or not published

Template: `templates/post.html`

### Admin Authentication Routes

#### `GET /admin/login` | `POST /admin/login`
**Admin Login**
- Login form for admin users
- Rate limited: 5 attempts per 15 minutes
- Redirects to dashboard on success
- Available only to anonymous users

Form: `LoginForm`
Template: `templates/admin/login.html`

#### `POST /admin/logout`
**Admin Logout**
- Logout current user
- POST-only for security
- Redirects to home page

### Admin Dashboard Routes

#### `GET /admin` | `GET /admin/dashboard`
**Admin Dashboard**
- Overview statistics (total posts, contacts, unread count)
- 5 most recent blog posts
- 5 most recent contact submissions
- Quick action links

Template: `templates/admin/dashboard.html`

**Protected:** Requires login

### Admin Blog Post Routes

#### `GET /admin/posts`
**List Blog Posts**
- Paginated list of all blog posts
- Filter by status (all/published/draft)
- Shows title, status, published date, author
- Links to edit/delete

Template: `templates/admin/posts_list.html`

**Query Parameters:**
- `page`: Page number (default: 1)
- `status`: Filter by status ('published', 'draft', or none for all)

**Protected:** Requires login

#### `GET /admin/posts/new` | `POST /admin/posts/new`
**Create New Blog Post**
- Form to create new blog post
- Auto-generates slug from title if not provided
- Validates slug uniqueness
- Sanitizes HTML content
- Sets publication date if "Published" is checked

Form: `BlogPostForm`
Template: `templates/admin/post_form.html`

**Protected:** Requires login

#### `GET /admin/posts/<post_id>/edit` | `POST /admin/posts/<post_id>/edit`
**Edit Blog Post**
- Form to edit existing blog post
- Pre-populated with current values
- Auto-generates slug if empty
- Validates slug uniqueness (excluding current post)
- Sanitizes HTML content

Form: `BlogPostForm`
Template: `templates/admin/post_form.html`

**Protected:** Requires login

#### `POST /admin/posts/<post_id>/delete`
**Delete Blog Post**
- Permanently delete blog post
- POST-only for security
- Shows confirmation flash message
- Redirects to posts list

**Protected:** Requires login

### Admin Contact Routes

#### `GET /admin/contacts`
**List Contact Submissions**
- Paginated list of all contact submissions
- Filter by status (all/new/read/responded)
- Shows name, email, date, status
- Click to view details

Template: `templates/admin/contacts_list.html`

**Query Parameters:**
- `page`: Page number (default: 1)
- `status`: Filter by status ('new', 'read', 'responded', or none for all)

**Protected:** Requires login

#### `GET /admin/contacts/<contact_id>`
**View Contact Details (JSON)**
- Returns contact submission details as JSON
- Automatically marks as "read" if status is "new"
- Used by AJAX modal

**Response:**
```json
{
  "id": 123,
  "name": "John Doe",
  "email": "john@example.com",
  "phone": "+1234567890",
  "message": "I would like to...",
  "submitted_at": "November 25, 2025 at 02:30 PM",
  "status": "read",
  "notes": "Called back on Nov 26"
}
```

**Protected:** Requires login

#### `POST /admin/contacts/<contact_id>/status`
**Update Contact Status**
- Update contact submission status
- Accepts JSON payload
- Valid statuses: 'new', 'read', 'responded'

**Request Body:**
```json
{
  "status": "responded"
}
```

**Protected:** Requires login

#### `POST /admin/contacts/<contact_id>/notes`
**Update Contact Notes**
- Update admin notes for contact submission
- Accepts JSON payload

**Request Body:**
```json
{
  "notes": "Called back and scheduled appointment for Dec 5"
}
```

**Protected:** Requires login

### Admin Utility Routes

#### `POST /admin/generate-slug`
**Generate URL Slug (JSON)**
- Generate URL-friendly slug from title
- Used by JavaScript for auto-slug generation

**Request Body:**
```json
{
  "title": "My Blog Post Title"
}
```

**Response:**
```json
{
  "slug": "my-blog-post-title"
}
```

**Protected:** Requires login

#### `POST /admin/upload-image`
**Upload Image for Blog Content**
- Upload image for use in blog post content
- TinyMCE integration
- Validates file type and size
- Automatically resizes large images
- Saves metadata to database

**Form Data:**
- `file`: Image file (png, jpg, jpeg, gif, webp)

**Response:**
```json
{
  "location": "/static/uploads/therapist/blog/inline/uuid-filename.jpg"
}
```

**Protected:** Requires login

## Configuration

Located in `sites/therapist/config.py`

### Configuration Classes

#### `Config` (Base)
Common configuration for all environments:
```python
class Config:
    SITE_NAME = 'Professional Psychotherapy'
    SITE_TAGLINE = 'Compassionate care for mental wellness'
    CONTACT_FORM_RATE_LIMIT = '5 per hour'
    BLOG_POSTS_PER_PAGE = 20
```

#### `DevelopmentConfig`
Development-specific settings:
```python
class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_ECHO = True  # Log SQL queries
```

#### `ProductionConfig`
Production-specific settings:
```python
class ProductionConfig(Config):
    DEBUG = False
    TESTING = False
```

### Environment Variables

Required variables in `/etc/webgarden/therapist.env`:

```bash
# Flask
SECRET_KEY=<generated-secret-key>
FLASK_ENV=production

# Database
DATABASE_URL=postgresql://webgarden:password@localhost/therapist_db

# Mail
MAIL_SERVER=smtp.mailgun.org
MAIL_PORT=587
MAIL_USERNAME=postmaster@therapist.example.com
MAIL_PASSWORD=<mailgun-api-key>
MAIL_DEFAULT_SENDER=info@therapist.example.com
ADMIN_EMAIL=admin@therapist.example.com

# Site
SITE_NAME=Professional Psychotherapy
SITE_DOMAIN=therapist.example.com
UPLOAD_FOLDER=/var/www/webgarden/uploads/therapist
MAX_UPLOAD_SIZE=5242880
```

## CLI Commands

Located in `sites/therapist/cli.py`

### `flask init-db`
Initialize the database (create all tables).

```bash
cd /var/www/webgarden/sites/therapist
source venv/bin/activate
flask init-db
```

### `flask create-admin`
Create an admin user interactively.

```bash
flask create-admin
# Enter username: admin
# Enter email: admin@example.com
# Enter password: ********
```

### `flask test-email`
Test email configuration by sending a test email.

```bash
flask test-email
# Enter recipient email: test@example.com
```

## Database Schema

### Tables Used

The therapist site uses these tables from shared models:

1. **users**
   - Admin and editor accounts
   - See shared/README.md for schema

2. **contact_submissions**
   - Contact form submissions
   - See shared/README.md for schema

3. **blog_posts**
   - Blog articles
   - See shared/README.md for schema

4. **uploaded_files**
   - File upload metadata
   - See shared/README.md for schema

### Migrations

```bash
# Create migration after model changes
flask db migrate -m "Description of changes"

# Review migration file
cat migrations/versions/<migration_id>_description.py

# Apply migration
flask db upgrade

# Rollback if needed
flask db downgrade
```

## Templates

### Template Hierarchy

```
base.html (shared)
└── Site templates extend base.html
    ├── index.html
    ├── about.html
    ├── services.html
    ├── contact.html
    ├── post.html
    └── admin/
        └── All admin templates
```

### Template Variables

**Available in all templates:**
```python
{
    'current_year': 2025,
    'site_name': 'Professional Psychotherapy',
    'site_tagline': 'Compassionate care for mental wellness',
    'current_user': <User object or AnonymousUser>,
    'unread_contacts_count': 5  # Only when authenticated
}
```

### Custom Template Examples

#### Displaying Flash Messages
```html
{% with messages = get_flashed_messages(with_categories=true) %}
  {% if messages %}
    {% for category, message in messages %}
      <div class="alert alert-{{ category }}">
        {{ message }}
      </div>
    {% endfor %}
  {% endif %}
{% endwith %}
```

#### Displaying Blog Posts
```html
{% for post in recent_posts %}
  <article>
    <h3><a href="{{ url_for('view_post', slug=post.slug) }}">{{ post.title }}</a></h3>
    <p class="meta">{{ post.published_at|datetime }}</p>
    <p>{{ post.excerpt }}</p>
  </article>
{% endfor %}
```

## Static Assets

### CSS
- `static/css/style.css`: Site-specific styles
- Uses Bootstrap 5 as base framework
- Custom color scheme for professional appearance
- Responsive design for mobile devices

### JavaScript
- `static/js/main.js`: Site-specific JavaScript
- Form validation
- Contact form interaction
- Admin panel interactions (modal, AJAX)

### Images
- `static/images/`: Site images
  - Hero images
  - Profile photos
  - Service icons
  - Stock photos

## Admin Panel Features

### Dashboard
- Quick overview of site activity
- Statistics cards (total posts, contacts, unread)
- Recent posts list with status indicators
- Recent contacts with status badges
- Quick action buttons

### Blog Management
- Create, edit, delete blog posts
- Rich text editor (TinyMCE)
- Image upload and insertion
- Auto-save drafts
- Preview before publishing
- URL slug management
- Publication scheduling

### Contact Management
- View all submissions
- Filter by status
- Mark as read/responded
- Add internal notes
- Quick reply via email link
- Export to CSV (future feature)

### User Interface
- Clean, modern design
- Responsive for mobile admin
- Bootstrap 5 components
- AJAX interactions for smooth UX
- Toast notifications
- Modal dialogs

## Security Features

### Authentication & Authorization
- Login required for all admin routes
- Role-based access control
- Session timeout after 1 hour
- Secure session cookies

### Input Validation
- WTForms validation on all forms
- CSRF protection on all POST requests
- HTML sanitization for blog content
- File type validation for uploads
- File size limits enforced

### Rate Limiting
- Contact form: 5 per hour per IP
- Login attempts: 5 per 15 minutes per IP
- API endpoints: 100 per minute per IP

### Content Security
- XSS prevention via HTML sanitization
- SQL injection protection via ORM
- HTTPS enforced (HTTP redirects to HTTPS)
- Secure headers configured

## Deployment

### Production Deployment

The site runs with:
- **Web Server:** Nginx (reverse proxy)
- **Application Server:** Gunicorn (4 workers)
- **Process Manager:** systemd
- **Database:** PostgreSQL
- **SSL:** Let's Encrypt (auto-renewal)

### Service Management

```bash
# Start service
sudo systemctl start webgarden-therapist

# Stop service
sudo systemctl stop webgarden-therapist

# Restart service
sudo systemctl restart webgarden-therapist

# Check status
sudo systemctl status webgarden-therapist

# View logs
sudo journalctl -u webgarden-therapist -f
```

### Using Control Script

```bash
# Convenient wrapper around systemctl
sudo /var/www/webgarden/deploy/webgarden-ctl.sh start therapist
sudo /var/www/webgarden/deploy/webgarden-ctl.sh restart therapist
sudo /var/www/webgarden/deploy/webgarden-ctl.sh logs therapist -f
```

## Development

### Local Setup

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
nano .env  # Configure settings
```

4. **Initialize database:**
```bash
flask db upgrade
flask create-admin
```

5. **Run development server:**
```bash
flask run --debug --port 5000
```

Visit: http://localhost:5000

### Development Workflow

1. Make code changes
2. Test locally with `flask run --debug`
3. Run tests (when implemented)
4. Commit changes to git
5. Deploy to staging (when set up)
6. Deploy to production

### Adding New Routes

```python
@app.route('/new-page')
def new_page():
    """New page description."""
    return render_template('new-page.html')
```

### Creating New Templates

```html
{% extends "base.html" %}

{% block title %}Page Title{% endblock %}

{% block content %}
<div class="container">
  <h1>Page Content</h1>
  <!-- Your content here -->
</div>
{% endblock %}
```

## Testing

### Manual Testing Checklist

**Public Pages:**
- [ ] Home page loads correctly
- [ ] About page displays therapist info
- [ ] Services page lists all services
- [ ] Contact form submits successfully
- [ ] Contact form validation works
- [ ] Rate limiting prevents spam
- [ ] Blog posts display correctly
- [ ] Navigation works on all pages
- [ ] Mobile responsive design

**Admin Features:**
- [ ] Login with valid credentials
- [ ] Login rejects invalid credentials
- [ ] Dashboard shows correct statistics
- [ ] Create new blog post
- [ ] Edit existing blog post
- [ ] Delete blog post
- [ ] Upload images in blog editor
- [ ] View contact submissions
- [ ] Update contact status
- [ ] Add notes to contacts
- [ ] Logout functionality

### Unit Tests (Future Implementation)

```python
# tests/test_routes.py
def test_home_page(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Professional Psychotherapy' in response.data

def test_contact_form(client):
    response = client.post('/contact', data={
        'name': 'Test User',
        'email': 'test@example.com',
        'message': 'Test message content'
    })
    assert response.status_code == 302  # Redirect after success
```

## Troubleshooting

### Common Issues

**Issue: 500 Error on Contact Form**
- Check MAIL_* environment variables
- Verify Mailgun credentials
- Check application logs: `sudo journalctl -u webgarden-therapist -n 50`

**Issue: Blog Images Not Displaying**
- Check UPLOAD_FOLDER exists and has correct permissions
- Verify nginx is serving /uploads/ correctly
- Check file was actually uploaded: `ls /var/www/webgarden/uploads/therapist/blog/inline/`

**Issue: Can't Login to Admin**
- Verify user exists: `flask shell` then `User.query.all()`
- Reset password: `flask create-admin` with same username
- Check session configuration in config.py

**Issue: Database Connection Errors**
- Verify DATABASE_URL is correct
- Check PostgreSQL is running: `sudo systemctl status postgresql`
- Test connection: `sudo -u postgres psql therapist_db`

### Debug Mode

Enable debug mode for development only:

```python
# In .env
FLASK_ENV=development

# Then restart
flask run --debug
```

**Never enable debug mode in production!**

### Log Locations

- Application logs: `sudo journalctl -u webgarden-therapist`
- Nginx access: `/var/log/nginx/therapist-access.log`
- Nginx errors: `/var/log/nginx/therapist-error.log`
- Gunicorn logs: `/var/log/webgarden/therapist-access.log`

## Future Enhancements

### Planned Features

1. **Online Booking**
   - Cal.com integration
   - Appointment scheduling
   - Email reminders
   - Calendar sync

2. **Client Portal**
   - Secure client login
   - Session notes access
   - Document sharing
   - Messaging system

3. **Blog Enhancements**
   - Categories and tags
   - Comments system
   - Social sharing
   - RSS feed

4. **Analytics**
   - Visitor tracking
   - Form conversion metrics
   - Popular content analysis

5. **SEO Improvements**
   - Sitemap generation
   - Schema.org markup
   - Meta tag optimization
   - Open Graph tags

## Support & Maintenance

### Regular Maintenance Tasks

- **Weekly:** Review contact submissions
- **Weekly:** Publish new blog posts
- **Monthly:** Review and update services page
- **Monthly:** Check for security updates
- **Quarterly:** Backup database
- **Quarterly:** Review user accounts

### Getting Help

1. Check this documentation
2. Review shared module documentation in `/shared/README.md`
3. Check application logs for errors
4. Review Flask documentation: https://flask.palletsprojects.com/
5. Review SQLAlchemy documentation: https://docs.sqlalchemy.org/

## License

[Specify license information]

---

**Last Updated:** 2025-11-25
