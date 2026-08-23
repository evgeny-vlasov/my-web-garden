# Psyling Site Documentation

Production runs directly from `/var/www/webgarden/sites/psyling` through
`webgarden-psyling.service` on `127.0.0.1:5001`. Psyling has no canonical
versioned deployer, deployed-SHA marker, or code-version rollback tool. It uses
`shared/`, as does PoolEmergency, so shared changes can affect both sites.

`sites/therapist` is a historical compatibility symlink, but Psyling's current
virtual-environment shebangs still refer to it. Do not remove it casually. See
[Webgarden deployment](../../docs/deployment.md) and
[operations](../../docs/operations.md) for production discovery and safety.

Professional psychotherapy website built on the WebGarden platform.

## Site Overview

The Psyling site provides a professional online presence for a psychotherapy practice, featuring:
- Information about services and approach
- Contact form for inquiries
- Blog with mental health articles
- Admin panel for content management
- Contact submission management

## Site Structure

```
sites/psyling/
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
- Paginated contact inbox with Active, Unread, Spam, and Archived views
- Archived inquiries are excluded from Active and Unread but remain stored
- Unread filtering and counts use `is_read`, independently of workflow status
- Workflow filters use the compatible stored values `new`, `contacted`,
  `booked`, and `closed`; the UI displays `new` as **Needs reply**
- Search by name, email, or phone and open a full HTML detail page

Template: `templates/admin/contacts_list.html`

**Query Parameters:**
- `page`: Page number (default: 1)
- `show`: `inbox` (active), `unread`, `spam`, or `archived`
- `status`: `new`, `contacted`, `booked`, or `closed`
- `q`: Name, email, or phone search text

**Protected:** Requires login

#### `GET /admin/contacts/<contact_id>/view`
**View Contact Details**
- Returns a complete HTML page that works without JavaScript
- Automatically sets `is_read=true` without changing workflow status
- Shows **Unread** only when `is_read=false`
- Shows **Needs reply** when the compatible stored status is `new`
- The legacy `/admin/contacts/<contact_id>` link opens the same page

**Protected:** Requires login

#### Contact actions
- `POST /admin/contacts/<contact_id>/crm` updates workflow status, follow-up,
  and internal notes
- `POST /admin/contacts/<contact_id>/toggle-read` manually marks read/unread;
  marking unread returns to the Unread list so opening the detail does not
  immediately reverse the action
- `POST /admin/contacts/<contact_id>/mark-contacted` records outside contact
- `POST /admin/contacts/<contact_id>/reply` sends and records an email reply
- `POST /admin/contacts/<contact_id>/archive` removes an inquiry from the active
  list without deleting it, or restores it later
- `POST /admin/contacts/<contact_id>/toggle-spam` changes spam classification

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
  "location": "/uploads/psyling/blog/inline/uuid-filename.jpg"
}
```

**Protected:** Requires login

## Configuration

Located in `sites/psyling/config.py`

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

The application recognizes these configuration names:

- `SECRET_KEY`, `FLASK_ENV`
- `DATABASE_URL`
- `MAIL_SERVER`, `MAIL_PORT`, `MAIL_USERNAME`, `MAIL_PASSWORD`
- `MAIL_DEFAULT_SENDER`, `ADMIN_EMAIL`
- `SITE_NAME`, `SITE_DOMAIN`, `UPLOAD_FOLDER`, `MAX_UPLOAD_SIZE`

Do not infer their production values from this README. The protected
`/etc/webgarden/psyling.env` file was not read during the architecture audit,
and Psyling's effective upload path remains configuration-dependent. Inspect
key names only when necessary; never print complete assignments.

## CLI Commands

Located in `sites/psyling/cli.py`

The commands in this section create accounts, send mail, or change database
state. Use them in an isolated development environment. Production use requires
a separately reviewed data/configuration plan and explicit authorization; do
not source the protected environment merely to try a command.

### `flask init-db`
Initialize the database (create all tables).

```bash
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

The Psyling site uses these tables from shared models:

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

The sequence below is a development reference, not a production migration or
rollback runbook. Test and review generated migrations before requesting any
production database change.

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

## AI Chatbot Widget (Sprint 4)

### Overview
The site features an AI-powered chatbot assistant called "Psyling Assistant" that helps visitors with questions about therapy services, scheduling, and general mental health information.

### Features
- **Interactive Chat Interface**: Bubble widget in bottom-right corner
- **Persistent Sessions**: Conversations persist across page navigation
- **Mobile-Responsive**: Optimized for all device sizes
- **Typing Indicators**: Shows when bot is thinking
- **Smart Routing**: Messages proxied through Flask to bot API service

### Technical Details
- **Widget**: `/static/js/bot-widget.js` - Self-contained JavaScript
- **Template**: `/templates/bot_widget.html` - Configuration
- **API Endpoint**: `POST /api/chat` - Proxy to localhost:5002
- **Session Storage**: localStorage (client-side only)

### Configuration
```html
data-bot-id="psyling"
data-bot-name="Psyling Assistant"
data-position="bottom-right"
data-primary-color="#7c3aed"
```

### Pages with Chatbot
- Home page (index.html)
- About page (about.html)
- Services page (services.html)
- Contact page (contact.html)
- Blog post pages (post.html)

### Requirements
- Bot API service must be running on localhost:5002
- Python requests library installed

## Admin Panel Features

### Dashboard
- Quick overview of site activity
- Statistics cards (total posts, contacts, unread)
- Recent posts list with status indicators
- Recent active, non-spam inquiries with unread and reply-status badges
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
- View active, unread, spam, and archived inquiries
- Treat unread and reply workflow as separate concepts
- Opening clears unread automatically while an unanswered inquiry continues to
  display **Needs reply**
- Mark an inquiry read/unread manually
- Record **Contacted**, **Booked**, or **Closed** workflow states
- Archive from the active list without deleting the inquiry, and restore it
- Add internal notes
- Compose and send email replies from an inquiry detail page
- Review the chronological status and content of replies sent from Psyling
- Use the visitor's stored email address; the reply form cannot redirect mail to
  an address supplied by the browser
- Keep the local email-app link as a fallback
- Export to CSV (future feature)

Incoming contact messages remain stored with their original inquiry. When
Valery sends a reply from its detail page, Psyling sends it through the existing
Mailgun configuration and saves the outgoing subject, body, recipient, admin,
timestamp, and SMTP-acceptance status. The inquiry is marked contacted only
after SMTP accepts the message.

`is_read` records whether an admin has opened the inquiry. The stored `status`
continues to record workflow progress for compatibility: `new` is presented as
**Needs reply**, while a successfully sent reply changes it to `contacted`,
presented as **Contacted**. Archiving sets `archived_at`; it never permanently
deletes the inquiry or its history.

The email uses the configured admin address as `Reply-To`, so a later client
reply arrives in `psyling@gmail.com`. Replies written directly in Gmail or
another email application are not automatically imported into Psyling's CRM.
Spam-marked and archived inquiries must be restored to an active, non-spam
state before Psyling will send from them.

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

Nginx proxies to the systemd-managed Gunicorn service, which loads PostgreSQL
configuration from the protected `/etc/webgarden/psyling.env` file. Do not
print that file's values.

There is no generic Webgarden command that deploys Psyling. Source changes,
deployment, database migration, and service restart are distinct actions. A
clean checkout does not prove what a long-running worker loaded. Discover the
effective runtime and obtain separate authorization before any restart or
migration. The deprecated `deploy/webgarden-ctl.sh` wrapper is not a canonical
deployment tool. Use the central [deployment guide](../../docs/deployment.md)
and [read-only operations runbook](../../docs/operations.md).

## Development

Use a separate development checkout. `/var/www/webgarden/sites/psyling` is the
production runtime, so creating a venv, changing configuration, or running
migrations there is a production change.

### Local Setup

1. **Create virtual environment:**
```bash
cd /path/to/development-checkout/sites/psyling
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
5. Review the exact change and its database/data effects
6. Follow the central deployment guide; no canonical Psyling staging or
   versioned deployment tool currently exists

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
- Inspect a narrow, redaction-aware journal window using the central operations
  runbook

**Issue: Blog Images Not Displaying**
- Check UPLOAD_FOLDER exists and has correct permissions
- Verify nginx is serving /uploads/ correctly
- Check file was actually uploaded: `ls /var/www/webgarden/uploads/psyling/blog/inline/`

**Issue: Can't Login to Admin**
- Verify account state without printing user rows or private fields
- Treat account creation or password reset as a separately authorized admin-data
  change
- Check session configuration in config.py

**Issue: Database Connection Errors**
- Verify that `DATABASE_URL` is configured without displaying its value
- Check PostgreSQL is running: `sudo systemctl status postgresql`
- Follow the central operations runbook; do not open an interactive production
  database session as a generic diagnostic step

### Debug Mode

Enable debug mode for development only:

```python
# In .env
FLASK_ENV=development

# Then start the development server
flask run --debug
```

**Never enable debug mode in production!**

### Log Locations

Use the narrow, redaction-aware journal and nginx inspection procedures in
[the central operations runbook](../../docs/operations.md). Do not dump complete
access logs; paths and application output may contain private information.

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
- **Regularly:** Review backup job evidence and restoration testing; a successful
  timer run alone does not prove completeness or recoverability
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

**Last Updated:** 2026-01-18
**Current Version:** 4.0 (Sprint 4 - AI Chatbot Integration)
