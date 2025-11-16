# WebGarden Site Creation Prompt

This is a standardized template for instructing Claude Code to build a complete Flask website on the WebGarden platform.

## How to Use This Template

1. Fill in all the `[BRACKETED]` sections below with your specific requirements
2. Copy the entire filled-in prompt
3. Paste it into a new Claude Code session
4. Claude Code will build your complete site following WebGarden patterns

---

## SITE CREATION PROMPT

I need you to build a complete professional website for the WebGarden multi-site Flask platform.

### BUSINESS INFORMATION

**Business Name:** [Your Business Name]

**Business Type:** [e.g., Therapist/Counseling Practice, Landscaping Company, Restaurant, Law Firm, Dental Office, etc.]

**Business Tagline/Slogan:** [One-line tagline that captures your value proposition]

**Business Description:** [2-3 sentences about what makes this business unique]

**Target Audience:** [Who are the ideal customers?]

### CONTACT INFORMATION

**Owner/Principal Name:** [Name]

**Business Phone:** [Phone number]

**Business Email:** [Email address]

**Physical Address:** [Street address, City, Province/State, Postal Code] (optional)

**Service Area:** [Geographic area served, e.g., "Calgary and surrounding areas"]

**Hours of Operation:** [Business hours] (optional)

### SERVICES/OFFERINGS

List the main services or products offered (3-6 items recommended):

1. **[Service 1 Name]**
   - Description: [Brief description]
   - Key features/benefits: [2-3 bullet points]

2. **[Service 2 Name]**
   - Description: [Brief description]
   - Key features/benefits: [2-3 bullet points]

3. **[Service 3 Name]**
   - Description: [Brief description]
   - Key features/benefits: [2-3 bullet points]

[Add more services as needed]

### DESIGN & AESTHETIC

**Color Scheme:** [e.g., "Professional blue and white", "Warm earth tones", "Modern minimalist with accent color"]

**Primary Color:** [Hex code if you have one, or description like "Deep blue"]

**Overall Feel:** [e.g., "Professional and trustworthy", "Warm and welcoming", "Modern and tech-forward", "Rustic and authentic"]

**Reference Sites:** [Any websites you like the style of] (optional)

### REQUIRED PAGES

Check which pages you need:

- [ ] **Home Page** - Hero section, services overview, about preview, testimonials, CTA
- [ ] **About Page** - Business story, team/owner bio, credentials, values
- [ ] **Services Page** - Overview of all services with cards linking to detail pages
- [ ] **Individual Service Pages** - One page for each service (auto-create from services list above)
- [ ] **Portfolio/Gallery Page** - Project showcase with images
- [ ] **Blog** - News/tips/insights section with admin panel
- [ ] **Contact Page** - Contact form with quote request functionality
- [ ] **Testimonials Page** - Customer reviews and success stories
- [ ] **FAQ Page** - Common questions and answers
- [ ] **Booking/Appointment Page** - Schedule consultation or service
- [ ] **Other:** [Specify any other pages needed]

### SPECIAL FEATURES & FUNCTIONALITY

**Contact Form Fields:**
- [ ] Name (required)
- [ ] Email (required)
- [ ] Phone (required)
- [ ] Subject/Service Interest
- [ ] Message (required)
- [ ] Best time to contact
- [ ] Preferred contact method
- [ ] Other: [Specify]

**Special Requirements:**
- [e.g., "5-year warranty prominently displayed", "Before/after image galleries", "Online booking integration", "Service area map", "Insurance accepted section", "Certifications/licenses display"]

**Call-to-Action Focus:**
- Primary CTA: [e.g., "Get Free Quote", "Book Consultation", "Schedule Appointment"]
- Secondary CTA: [e.g., "View Portfolio", "Call Now", "Learn More"]

### CONTENT HIGHLIGHTS

**Unique Selling Points:** (What sets this business apart?)
1. [USP 1]
2. [USP 2]
3. [USP 3]

**Trust Indicators:** (Check what applies)
- [ ] Years in business: [Number]
- [ ] Warranty/Guarantee: [Details]
- [ ] Certifications/Licenses: [List]
- [ ] Insurance: [Details]
- [ ] Awards/Recognition: [List]
- [ ] Professional associations: [List]
- [ ] Customer satisfaction rate/reviews

**Social Proof:**
- [ ] Include testimonials section
- [ ] Display number of clients served
- [ ] Show years of experience
- [ ] Feature case studies/success stories

### TECHNICAL REQUIREMENTS

**Site Structure:**
- Site ID: [Short identifier, e.g., "mysite"]
- Port: [e.g., 8003]
- Domain: [e.g., mysite.mywebgarden.qzz.io]

**Email Configuration:**
- Contact form submissions should go to: [Email address]
- Send confirmation emails to customers: [Yes/No]

**Admin Panel Features:**
- [ ] Blog post management
- [ ] Contact form submissions inbox
- [ ] User management
- [ ] Portfolio/gallery management (if applicable)

### BRAND VOICE & TONE

**Writing Style:** [e.g., "Professional but approachable", "Warm and empathetic", "Expert and authoritative", "Friendly and casual"]

**Key Messaging Points:**
- [Key point 1 to emphasize throughout site]
- [Key point 2 to emphasize throughout site]
- [Key point 3 to emphasize throughout site]

### EXISTING ASSETS

**Do you have:**
- [ ] Logo: [Yes/No - if yes, mention it will be provided separately]
- [ ] Brand guidelines: [Yes/No]
- [ ] Existing photos: [Yes/No]
- [ ] Existing content/copy: [Yes/No]

**Placeholder Content:**
If no existing assets: "Use professional placeholder content, descriptions, and suggest image types needed for each section. I will provide actual photos later."

---

## IMPLEMENTATION INSTRUCTIONS FOR CLAUDE CODE

Based on the above information, please:

1. **Review the WebGarden structure** by examining:
   - `/var/www/webgarden/webgarden/sites/keystone/` - Reference this as the pattern to follow
   - `/var/www/webgarden/webgarden/shared/` - Shared base classes and templates

2. **Create the complete site** at `/var/www/webgarden/webgarden/sites/[SITE_ID]/` including:
   - `app.py` - All routes and Flask app configuration
   - `config.py` - Site-specific configuration extending base config
   - `cli.py` - Copy from keystone (standard CLI commands)
   - `templates/` - All HTML templates extending `base.html`
   - `static/` - CSS, JavaScript, and placeholder images

3. **Follow these patterns from Keystone:**
   - Use `shared.base_app.create_base_app()` for app initialization
   - Extend `shared.models` for User, BlogPost, ContactSubmission
   - Use `shared.forms` for WTForms (ContactForm, LoginForm, BlogPostForm)
   - Implement Flask-Login for admin authentication
   - Use Flask-Limiter for rate limiting on contact form
   - Implement blog system with admin panel (if requested)
   - Use Bootstrap 5 for styling
   - Include security best practices (CSRF, secure sessions, input sanitization)

4. **Create these route groups:**
   - Public routes: home, about, services, individual service pages, portfolio, blog, contact
   - Admin routes: login/logout, dashboard, blog management, contact submissions
   - Utility routes: admin utilities (slug generation, image upload)

5. **Design Requirements:**
   - Professional, responsive design using Bootstrap 5
   - Match the aesthetic and color scheme specified above
   - Include proper meta tags for SEO
   - Implement proper error handling and flash messages
   - Use the specified CTAs throughout

6. **Testing Checklist:**
   - All routes should work without errors
   - Templates should properly extend base.html
   - Forms should have CSRF protection
   - Admin panel should require authentication
   - Contact form should have rate limiting
   - Database models should work with Flask-Migrate

7. **Deliverables:**
   - Complete, working Flask application
   - All templates with professional copy based on the information provided
   - Styled with custom CSS matching brand aesthetic
   - README.md with site-specific documentation
   - Notes on what images/assets need to be provided

Please build this site following the exact patterns used in the Keystone site, but customized with all the specific information provided above. Ask questions if any critical information is missing.

---

## AFTER SITE CREATION

Once Claude Code has built your site:

1. **Run the deployment script** (if not already done):
   ```bash
   sudo /var/www/webgarden/webgarden/deploy/new_site.sh [SITE_ID] [DOMAIN] [PORT] [DB_PASSWORD] "[SITE_NAME]"
   ```

2. **Create admin user:**
   ```bash
   cd /var/www/webgarden/webgarden/sites/[SITE_ID]
   venv/bin/flask create-admin
   ```

3. **Restart the service:**
   ```bash
   sudo systemctl restart [SITE_ID].service
   ```

4. **Test the site:**
   - Visit http://[DOMAIN]
   - Log into admin panel
   - Test contact form
   - Create a test blog post

5. **Add real content:**
   - Upload real photos
   - Replace placeholder content
   - Add real testimonials
   - Create actual blog posts

6. **Launch:**
   - Set up SSL with certbot
   - Configure email sending
   - Update DNS
   - Monitor logs
