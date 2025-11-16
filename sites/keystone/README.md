# Keystone Hardscapes Website

Professional hardscaping and landscaping business website for Calgary, Alberta.

## Business Information

- **Owner:** Andrew (lead craftsman)
- **Phone:** 587-573-6005
- **Email:** info@keystonehardscapes.ca
- **Tagline:** "Expert Craftsmanship. Lasting Quality."
- **Service Area:** Calgary, Airdrie, Cochrane, Okotoks, Chestermere
- **Warranty:** 5-year warranty on all hardscape work

## Services

1. **Landscaping & Hardscape** - Patios, retaining walls, outdoor living spaces
2. **Snow Removal** - Residential & commercial, winter season
3. **Concrete Restoration** - Epoxy overlays, repair work

## Tech Stack

- **Framework:** Flask (Python)
- **Database:** PostgreSQL
- **Frontend:** Bootstrap 5, Bootstrap Icons
- **Template Engine:** Jinja2
- **Port:** 8002

## Setup Instructions

### 1. Database Setup

```bash
# Create the database
createdb keystone_db

# Initialize tables (from the webgarden root)
cd /var/www/webgarden/webgarden
python -c "from sites.keystone.app import app, db; app.app_context().push(); db.create_all()"
```

### 2. Create Admin User

```bash
# From the sites/keystone directory
export FLASK_APP=app.py
flask create-admin
# Follow prompts to create admin user
```

### 3. Environment Variables

Create a `.env` file in the project root with:

```env
SECRET_KEY=your-secret-key-here
DATABASE_URL=postgresql://localhost/keystone_db
FLASK_ENV=development

# Email settings (Mailgun)
MAIL_USERNAME=your-mailgun-username
MAIL_PASSWORD=your-mailgun-password
MAIL_DEFAULT_SENDER=info@keystonehardscapes.ca
ADMIN_EMAIL=info@keystonehardscapes.ca

# Site settings
SITE_NAME=Keystone Hardscapes
SITE_DOMAIN=keystonehardscapes.ca
```

### 4. Run the Development Server

```bash
# From sites/keystone directory
python app.py

# Or use Flask CLI
export FLASK_APP=app.py
flask run --port=8002
```

The site will be available at: http://localhost:8002

## File Structure

```
keystone/
├── app.py                  # Main Flask application
├── config.py               # Configuration settings
├── cli.py                  # CLI commands for admin tasks
├── README.md              # This file
├── templates/             # Jinja2 templates
│   ├── index.html         # Homepage
│   ├── about.html         # About page
│   ├── contact.html       # Contact/quote form
│   ├── portfolio.html     # Portfolio gallery
│   ├── post.html          # Blog post template
│   └── services/          # Service pages
│       ├── hardscape.html
│       ├── snow-removal.html
│       └── concrete-restoration.html
└── static/                # Static assets
    ├── css/
    │   └── keystone.css   # Custom styles
    ├── js/
    └── images/            # Site images (see below)
```

## Required Images

Place the following images in `static/images/`:

### Homepage
- `hero.jpg` - Large hero background (1920x1080+)
- `andrew-portrait.jpg` - Andrew headshot/portrait
- `service-hardscape.jpg` - Hardscape service preview
- `service-snow.jpg` - Snow removal preview
- `service-concrete.jpg` - Concrete restoration preview
- `project-1.jpg` through `project-4.jpg` - Portfolio previews
- `service-area-map.jpg` - Service area map

### About Page
- `andrew-at-work.jpg` - Andrew working on site
- `alberta-winter-hardscape.jpg` - Hardscape in winter

### Service Pages
- `service-hardscape-hero.jpg` - Hardscape page header
- `hardscape-detail.jpg` - Close-up of hardscape work
- `winter-patio.jpg` - Patio in winter
- `service-snow-hero.jpg` - Snow removal header
- `snow-removal-action.jpg` - Snow removal in action
- `snow-equipment.jpg` - Snow removal equipment
- `service-concrete-hero.jpg` - Concrete restoration header
- `concrete-before-after.jpg` - Before/after restoration
- `concrete-assessment.jpg` - Concrete assessment

### Portfolio Page
- `portfolio/patio-calgary-1.jpg`
- `portfolio/retaining-wall-airdrie.jpg`
- `portfolio/outdoor-kitchen-cochrane.jpg`
- `portfolio/driveway-okotoks.jpg`
- `portfolio/front-walkway-calgary.jpg`
- `portfolio/garage-floor-chestermere.jpg`
- `portfolio/backyard-transformation-calgary.jpg`
- `portfolio/commercial-parking-airdrie.jpg`
- `portfolio/patio-extension-calgary.jpg`

## Image Specifications

- **Hero images:** 1920x1080px minimum, landscape
- **Service images:** 1200x800px, landscape
- **Portfolio images:** 800x600px, landscape
- **Portrait images:** 600x800px, portrait
- **Format:** JPG (optimized for web, 80-90% quality)
- **Max file size:** 500KB per image (compressed)

## Admin Panel

Access the admin panel at: http://localhost:8002/admin/login

Features:
- Blog post management
- Contact form submissions
- User management

## CLI Commands

```bash
# Create admin user
flask create-admin

# Reset user password
flask reset-password

# List all users
flask list-users

# Delete user
flask delete-user

# Promote user to admin
flask promote-user

# Demote admin to editor
flask demote-user

# Create test blog post
flask create-test-post
```

## Design Notes

- **Color Palette:** Earth tones (greens, browns, grays)
- **Aesthetic:** Professional, rugged, contractor-focused
- **Typography:** Bold headings, clear hierarchy
- **CTAs:** Strong "Get Free Quote" buttons throughout
- **Mobile-first:** Fully responsive Bootstrap 5 design

## Content Strategy

- Visual-heavy with large project photos
- Owner-focused messaging (Andrew's personal involvement)
- Emphasis on quality, warranty, and transparency
- Climate-focused (Alberta freeze-thaw cycles)
- Portfolio showcases completed work
- Service area clearly defined

## Deployment

For production deployment:

1. Set `FLASK_ENV=production` in environment
2. Use Gunicorn or similar WSGI server
3. Configure reverse proxy (Nginx/Apache)
4. Set up SSL certificates
5. Configure email delivery (Mailgun)
6. Set up database backups
7. Configure file uploads directory

## Support

For issues or questions, contact the webmaster or refer to the main WebGarden documentation.
