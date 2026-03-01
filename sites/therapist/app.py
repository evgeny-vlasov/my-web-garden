"""csrf
Therapist Site Flask Application
Main application file for the professional psychotherapy website.
"""

import os
import sys
from datetime import datetime
from pathlib import Path
from werkzeug.utils import secure_filename
from slugify import slugify
import markdown

# Add parent directories to Python path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from shared.base_app import csrf

from flask import render_template, request, flash, redirect, url_for, jsonify, abort, session
from flask_login import login_user, logout_user, current_user, login_required
from flask_mail import Message
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import shared modules
from shared.base_app import create_base_app, db, limiter, login_manager, mail
from shared.models import ContactSubmission, User, BlogPost, UploadedFile
from shared.forms import ContactForm, LoginForm, BlogPostForm
from shared.email import send_contact_notification, send_contact_confirmation
from shared.decorators import login_required as custom_login_required, admin_required, anonymous_required
from shared.sanitizer import sanitize_html, create_excerpt
from shared.image_handler import save_image, allowed_file
from sites.therapist.config import config
from sites.therapist.cli import register_cli_commands

# Additional imports for page editing
from flask_wtf import FlaskForm
from wtforms import TextAreaField
from wtforms.validators import DataRequired

# Create Flask application
config_name = os.getenv('FLASK_ENV', 'production')
app = create_base_app('therapist', config[config_name])

# Register CLI commands
register_cli_commands(app)


# ============================================================================
# FORMS
# ============================================================================

class PageEditForm(FlaskForm):
    """Form for editing markdown pages"""
    content = TextAreaField('Content', validators=[DataRequired()])


# ============================================================================
# FLASK-LOGIN SETUP
# ============================================================================

# User loader for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    """Load user by ID for Flask-Login."""
    return User.query.get(int(user_id))

# Context processor to inject current year and site info
@app.context_processor
def inject_globals():
    """Inject global variables into all templates."""
    unread_count = 0
    if current_user.is_authenticated:
        unread_count = ContactSubmission.query.filter_by(status='new').count()

    # Get current language from session, default to English
    current_lang = session.get('lang', 'en')

    return {
        'current_year': datetime.now().year,
        'site_name': app.config['SITE_NAME'],
        'site_tagline': app.config['SITE_TAGLINE'],
        'unread_contacts_count': unread_count,
        'current_lang': current_lang
    }


# ============================================================================
# LANGUAGE SWITCHING
# ============================================================================

@app.route('/set-language/<lang>')
def set_language(lang):
    """Set the user's preferred language"""
    if lang in ['en', 'ru']:
        session['lang'] = lang
        session.permanent = True  # Make session persistent
    # Redirect back to the referring page or home
    return redirect(request.referrer or url_for('index'))


# ============================================================================
# PUBLIC ROUTES
# ============================================================================

@app.route('/')
def index():
    """Redirect homepage to schedule page."""
    return redirect(url_for('schedule'), code=302)


@app.route('/about')
def about():
    """About page route."""
    return render_template('about.html')


@app.route('/services')
def services():
    """Services page route."""
    return render_template('services.html')


@app.route('/faq')
def faq():
    """FAQ page route."""
    return render_template('faq.html')


# ============================================================================
# MARKDOWN PAGE ROUTES
# ============================================================================

def render_markdown_page(filename):
    """Render a markdown file as HTML page"""
    content_dir = Path(app.root_path) / 'content'

    # Check for language-specific version
    current_lang = session.get('lang', 'en')
    if current_lang == 'ru':
        # Try Russian version first
        base_name = filename.replace('.md', '')
        ru_filename = f"{base_name}_ru.md"
        ru_file_path = content_dir / ru_filename

        if ru_file_path.exists():
            file_path = ru_file_path
        else:
            file_path = content_dir / filename
    else:
        file_path = content_dir / filename

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            md_content = f.read()

        # Convert markdown to HTML
        html_content = markdown.markdown(
            md_content,
            extensions=['extra', 'nl2br', 'sane_lists']
        )

        return render_template('markdown_page.html',
                             content=html_content,
                             title=filename.replace('.md', '').title())
    except FileNotFoundError:
        abort(404)
    except Exception as e:
        app.logger.error(f"Error rendering {filename}: {str(e)}")
        abort(500)


@app.route('/fees')
def fees():
    """Display fees page from markdown"""
    return render_markdown_page('fees.md')


@app.route('/schedule', methods=['GET'])
def schedule():
    """Display schedule page with calendar and booking form."""
    form = ContactForm()
    today = datetime.now().strftime('%Y-%m-%d')
    return render_template('schedule.html', form=form, today=today)


@app.route('/schedule/request', methods=['POST'])
@limiter.limit(app.config.get('CONTACT_FORM_RATE_LIMIT', '5 per hour'))
def schedule_request():
    """Handle booking request submission."""
    form = ContactForm()

    if form.validate_on_submit():
        try:
            # Get form data
            name = form.name.data
            email = form.email.data
            phone = form.phone.data or ''
            preferred_date = request.form.get('preferred_date', '')
            preferred_time = request.form.get('preferred_time', '')
            alternative_date = request.form.get('alternative_date', '')
            alternative_time = request.form.get('alternative_time', '')
            reason = request.form.get('reason', '')
            notes = request.form.get('notes', '')

            # Validate required booking fields
            if not preferred_date or not preferred_time:
                flash('Please select both a preferred date and time.', 'danger')
                return redirect(url_for('schedule'))

            # Send booking request email to admin
            try:
                subject = f'New Booking Request from {name}'
                admin_email = app.config.get('ADMIN_EMAIL', app.config['MAIL_DEFAULT_SENDER'])

                text_body = f"""
New appointment booking request from {app.config.get('SITE_DOMAIN', 'psyling.com')}:

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

CLIENT INFORMATION:
Name:     {name}
Email:    {email}
Phone:    {phone or 'Not provided'}

REQUESTED APPOINTMENT:
Preferred Date:  {preferred_date}
Preferred Time:  {preferred_time}

Alternative Date:  {alternative_date or 'Not specified'}
Alternative Time:  {alternative_time or 'Not specified'}

REASON FOR APPOINTMENT:
{reason or 'Not specified'}

ADDITIONAL NOTES:
{notes or 'None'}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

NEXT STEPS:
• Click "Reply" to contact the client directly
• Or call: {phone or 'No phone provided'}
• Client will receive your response at: {email}

View all booking requests: https://{app.config.get('SITE_DOMAIN', 'psyling.com')}/admin/contacts

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{app.config['SITE_NAME']} - Booking Request Automated Notification
                """

                html_body = f"""
<html>
<head>
    <style>
        body {{ font-family: 'Segoe UI', Arial, sans-serif; line-height: 1.6; color: #333; background-color: #f5f5f5; }}
        .container {{ max-width: 600px; margin: 20px auto; background-color: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        h1 {{ color: #667eea; margin-bottom: 20px; font-size: 24px; }}
        .info-section {{ background-color: #f8f9fa; padding: 15px; border-radius: 5px; margin: 15px 0; }}
        .label {{ font-weight: bold; color: #495057; display: inline-block; width: 150px; }}
        .value {{ color: #212529; }}
        .message-box {{ background-color: #e9ecef; padding: 15px; border-radius: 5px; margin: 15px 0; white-space: pre-wrap; }}
        .footer {{ margin-top: 30px; padding-top: 20px; border-top: 1px solid #dee2e6; font-size: 12px; color: #6c757d; }}
        .button {{ display: inline-block; padding: 12px 24px; background-color: #667eea; color: white; text-decoration: none; border-radius: 5px; margin: 10px 0; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>📅 New Booking Request</h1>

        <div class="info-section">
            <h3 style="margin-top: 0; color: #495057;">Client Information</h3>
            <div><span class="label">Name:</span> <span class="value">{name}</span></div>
            <div><span class="label">Email:</span> <span class="value"><a href="mailto:{email}">{email}</a></span></div>
            <div><span class="label">Phone:</span> <span class="value">{phone or 'Not provided'}</span></div>
        </div>

        <div class="info-section">
            <h3 style="margin-top: 0; color: #495057;">Requested Appointment</h3>
            <div><span class="label">Preferred Date:</span> <span class="value"><strong>{preferred_date}</strong></span></div>
            <div><span class="label">Preferred Time:</span> <span class="value"><strong>{preferred_time}</strong></span></div>
            <hr style="margin: 10px 0; border: none; border-top: 1px solid #dee2e6;">
            <div><span class="label">Alternative Date:</span> <span class="value">{alternative_date or 'Not specified'}</span></div>
            <div><span class="label">Alternative Time:</span> <span class="value">{alternative_time or 'Not specified'}</span></div>
        </div>

        {f'<div class="info-section"><h3 style="margin-top: 0; color: #495057;">Reason for Appointment</h3><div class="message-box">{reason}</div></div>' if reason else ''}

        {f'<div class="info-section"><h3 style="margin-top: 0; color: #495057;">Additional Notes</h3><div class="message-box">{notes}</div></div>' if notes else ''}

        <div style="margin-top: 20px; padding: 15px; background-color: #d4edda; border-radius: 5px; border-left: 4px solid #28a745;">
            <strong style="color: #155724;">Next Steps:</strong><br>
            • Click "Reply" in your email to respond directly to the client<br>
            • Or call: {phone or 'No phone provided'}<br>
            • <a href="https://{app.config.get('SITE_DOMAIN', 'psyling.com')}/admin/contacts">View all booking requests in admin panel</a>
        </div>

        <div class="footer">
            <p>{app.config['SITE_NAME']} - Booking Request Automated Notification</p>
            <p>This email was sent from {app.config.get('SITE_DOMAIN', 'psyling.com')}</p>
        </div>
    </div>
</body>
</html>
                """

                # Send email with Reply-To header
                msg = Message(
                    subject=subject,
                    recipients=[admin_email],
                    sender=app.config['MAIL_DEFAULT_SENDER'],
                    reply_to=email
                )
                msg.body = text_body
                msg.html = html_body

                mail.send(msg)
                app.logger.info(f'Booking request email sent for {name} - {email}')

                flash('Your booking request has been submitted! I will confirm your appointment via email within 24 hours.', 'success')
                return redirect(url_for('schedule'))

            except Exception as email_error:
                app.logger.error(f'Failed to send booking request email: {str(email_error)}')
                flash('Your request was received, but there was an issue sending the notification. I will still review your request.', 'warning')
                return redirect(url_for('schedule'))

        except Exception as e:
            app.logger.error(f'Error processing booking request: {str(e)}')
            flash('An error occurred. Please try again or contact me directly.', 'danger')
            return redirect(url_for('schedule'))

    # Form validation failed
    flash('Please fill in all required fields correctly.', 'danger')
    return redirect(url_for('schedule'))


@app.route('/contact', methods=['GET', 'POST'])
@limiter.limit(app.config.get('CONTACT_FORM_RATE_LIMIT', '5 per hour'))
def contact():
    """Contact page with form submission."""
    form = ContactForm()

    if form.validate_on_submit():
        try:
            # Create contact submission record
            submission = ContactSubmission(
                name=form.name.data,
                email=form.email.data,
                phone=form.phone.data,
                message=form.message.data
            )

            # Save to database
            db.session.add(submission)
            db.session.commit()

            # Send notification emails
            try:
                send_contact_notification(submission)
                send_contact_confirmation(submission)
            except Exception as email_error:
                # Log email error but don't fail the submission
                app.logger.error(f'Failed to send email notification: {str(email_error)}')

            flash('Thank you for your message! We will get back to you soon.', 'success')
            return redirect(url_for('contact'))

        except Exception as e:
            db.session.rollback()
            app.logger.error(f'Error saving contact submission: {str(e)}')
            flash('An error occurred. Please try again later.', 'error')

    return render_template('contact.html', form=form)


@app.route('/post/<slug>')
def view_post(slug):
    """View a single blog post."""
    post = BlogPost.query.filter_by(slug=slug, visible=True).first_or_404()

    # Get 3 other recent posts for sidebar
    recent_posts = BlogPost.query.filter_by(visible=True).filter(
        BlogPost.id != post.id,
        BlogPost.published_at.isnot(None)
    ).order_by(BlogPost.published_at.desc()).limit(3).all()

    # Create excerpt for meta description
    excerpt = create_excerpt(post.content, 160)

    return render_template('post.html', post=post, recent_posts=recent_posts, excerpt=excerpt)


# ============================================================================
# ADMIN AUTHENTICATION ROUTES
# ============================================================================

@app.route('/admin/login', methods=['GET', 'POST'])
@anonymous_required
@limiter.limit('5 per 15 minutes')
def admin_login():
    """Admin login page."""
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            user.update_last_login()

            # Redirect to next page or dashboard
            next_page = request.args.get('next')
            if next_page and next_page.startswith('/admin'):
                return redirect(next_page)
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid username or password.', 'error')
            app.logger.warning(f'Failed login attempt for username: {form.username.data}')

    return render_template('admin/login.html', form=form)


@app.route('/admin/logout', methods=['POST'])
@login_required
def admin_logout():
    """Admin logout."""
    logout_user()
    flash('You have been logged out successfully.', 'success')
    return redirect(url_for('index'))


# ============================================================================
# ADMIN DASHBOARD
# ============================================================================

@app.route('/admin')
@app.route('/admin/dashboard')
@custom_login_required
def admin_dashboard():
    """Admin dashboard."""
    # Get statistics
    stats = {
        'total_posts': BlogPost.query.count(),
        'total_contacts': ContactSubmission.query.count(),
        'unread_contacts': ContactSubmission.query.filter_by(status='new').count()
    }

    # Get recent posts (5 most recent)
    recent_posts = BlogPost.query.order_by(BlogPost.updated_at.desc()).limit(5).all()

    # Get recent contacts (5 most recent)
    recent_contacts = ContactSubmission.query.order_by(
        ContactSubmission.submitted_at.desc()
    ).limit(5).all()

    return render_template(
        'admin/dashboard.html',
        stats=stats,
        recent_posts=recent_posts,
        recent_contacts=recent_contacts
    )


# ============================================================================
# ADMIN BLOG POST ROUTES
# ============================================================================

@app.route('/admin/posts')
@custom_login_required
def admin_posts_list():
    """List all blog posts with filtering."""
    page = request.args.get('page', 1, type=int)
    status_filter = request.args.get('status', None)

    query = BlogPost.query

    # Apply status filter
    if status_filter == 'published':
        query = query.filter_by(visible=True)
    elif status_filter == 'draft':
        query = query.filter_by(visible=False)

    # Paginate results
    pagination = query.order_by(BlogPost.updated_at.desc()).paginate(
        page=page,
        per_page=20,
        error_out=False
    )

    # Get counts for filter tabs
    counts = {
        'all': BlogPost.query.count(),
        'published': BlogPost.query.filter_by(visible=True).count(),
        'draft': BlogPost.query.filter_by(visible=False).count()
    }

    return render_template(
        'admin/posts_list.html',
        posts=pagination,
        pagination=pagination,
        counts=counts,
        status_filter=status_filter,
        endpoint='admin_posts_list',
        kwargs={}
    )


@app.route('/admin/posts/new', methods=['GET', 'POST'])
@custom_login_required
def admin_post_create():
    """Create a new blog post."""
    form = BlogPostForm()

    if form.validate_on_submit():
        try:
            # Generate slug if not provided
            slug = form.slug.data.strip()
            if not slug:
                slug = slugify(form.title.data)

            # Check if slug already exists
            existing_post = BlogPost.query.filter_by(slug=slug).first()
            if existing_post:
                flash('A post with this URL slug already exists. Please choose a different slug.', 'error')
                return render_template('admin/post_form.html', form=form, post=None)

            # Sanitize HTML content
            clean_content = sanitize_html(form.content.data)

            # Create new post
            post = BlogPost(
                title=form.title.data,
                slug=slug,
                content=clean_content,
                author_id=current_user.id,
                visible=form.visible.data
            )

            # Publish if visible is checked
            if form.visible.data:
                post.publish()

            db.session.add(post)
            db.session.commit()

            flash('Blog post created successfully!', 'success')
            return redirect(url_for('admin_post_edit', post_id=post.id))

        except Exception as e:
            db.session.rollback()
            app.logger.error(f'Error creating blog post: {str(e)}')
            flash('An error occurred while creating the post.', 'error')

    return render_template('admin/post_form.html', form=form, post=None)


@app.route('/admin/posts/<int:post_id>/edit', methods=['GET', 'POST'])
@custom_login_required
def admin_post_edit(post_id):
    """Edit an existing blog post."""
    post = BlogPost.query.get_or_404(post_id)
    form = BlogPostForm(obj=post)

    if form.validate_on_submit():
        try:
            # Generate slug if changed or empty
            slug = form.slug.data.strip()
            if not slug:
                slug = slugify(form.title.data)

            # Check if slug already exists (excluding current post)
            existing_post = BlogPost.query.filter(
                BlogPost.slug == slug,
                BlogPost.id != post_id
            ).first()

            if existing_post:
                flash('A post with this URL slug already exists. Please choose a different slug.', 'error')
                return render_template('admin/post_form.html', form=form, post=post)

            # Update post
            post.title = form.title.data
            post.slug = slug
            post.content = sanitize_html(form.content.data)
            post.visible = form.visible.data

            # Publish if visible is checked and not already published
            if form.visible.data and not post.published_at:
                post.publish()
            elif not form.visible.data:
                post.unpublish()

            db.session.commit()

            flash('Blog post updated successfully!', 'success')
            return redirect(url_for('admin_post_edit', post_id=post.id))

        except Exception as e:
            db.session.rollback()
            app.logger.error(f'Error updating blog post: {str(e)}')
            flash('An error occurred while updating the post.', 'error')

    return render_template('admin/post_form.html', form=form, post=post)


@app.route('/admin/posts/<int:post_id>/delete', methods=['POST'])
@custom_login_required
def admin_post_delete(post_id):
    """Delete a blog post."""
    post = BlogPost.query.get_or_404(post_id)

    try:
        db.session.delete(post)
        db.session.commit()
        flash(f'Blog post "{post.title}" deleted successfully.', 'success')
    except Exception as e:
        db.session.rollback()
        app.logger.error(f'Error deleting blog post: {str(e)}')
        flash('An error occurred while deleting the post.', 'error')

    return redirect(url_for('admin_posts_list'))


# ============================================================================
# ADMIN CONTACT SUBMISSIONS ROUTES
# ============================================================================

@app.route('/admin/contacts')
@custom_login_required
def admin_contacts_list():
    """List all contact submissions with filtering."""
    page = request.args.get('page', 1, type=int)
    status_filter = request.args.get('status', None)
    spam_filter = request.args.get('show', 'inbox')  # inbox or spam

    query = ContactSubmission.query

    # Apply spam filter first
    if spam_filter == 'spam':
        query = query.filter_by(is_spam=True)
        show_spam = True
    else:
        query = query.filter_by(is_spam=False)
        show_spam = False

    # Apply status filter
    if status_filter:
        query = query.filter_by(status=status_filter)

    # Paginate results
    contacts = query.order_by(ContactSubmission.submitted_at.desc()).paginate(
        page=page,
        per_page=20,
        error_out=False
    )

    # Get counts for filter tabs
    counts = {
        'all': ContactSubmission.query.count(),
        'inbox': ContactSubmission.query.filter_by(is_spam=False).count(),
        'spam': ContactSubmission.query.filter_by(is_spam=True).count(),
        'new': ContactSubmission.query.filter_by(status='new', is_spam=False).count(),
        'read': ContactSubmission.query.filter_by(status='read', is_spam=False).count(),
        'responded': ContactSubmission.query.filter_by(status='responded', is_spam=False).count()
    }

    return render_template(
        'admin/contacts_list.html',
        contacts=contacts,
        counts=counts,
        status_filter=status_filter,
        spam_filter=spam_filter,
        show_spam=show_spam,
        endpoint='admin_contacts_list',
        kwargs={}
    )


@app.route('/admin/contacts/<int:contact_id>')
@custom_login_required
def admin_contact_view(contact_id):
    """Get contact submission details (JSON)."""
    contact = ContactSubmission.query.get_or_404(contact_id)

    # Mark as read if it's new
    if contact.status == 'new':
        contact.mark_as_read()

    return jsonify({
        'id': contact.id,
        'name': contact.name,
        'email': contact.email,
        'phone': contact.phone,
        'message': contact.message,
        'submitted_at': contact.submitted_at.strftime('%B %d, %Y at %I:%M %p'),
        'status': contact.status,
        'notes': contact.notes
    })


@app.route('/admin/contacts/<int:contact_id>/status', methods=['POST'])
@custom_login_required
def admin_contact_update_status(contact_id):
    """Update contact submission status."""
    contact = ContactSubmission.query.get_or_404(contact_id)
    data = request.get_json()

    try:
        status = data.get('status')
        if status in ['new', 'read', 'responded']:
            contact.status = status
            db.session.commit()
            return jsonify({'success': True})
        else:
            return jsonify({'success': False, 'error': 'Invalid status'}), 400
    except Exception as e:
        db.session.rollback()
        app.logger.error(f'Error updating contact status: {str(e)}')
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/admin/contacts/<int:contact_id>/notes', methods=['POST'])
@custom_login_required
def admin_contact_update_notes(contact_id):
    """Update contact submission notes."""
    contact = ContactSubmission.query.get_or_404(contact_id)
    data = request.get_json()

    try:
        contact.notes = data.get('notes', '')
        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        app.logger.error(f'Error updating contact notes: {str(e)}')
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/admin/contacts/<int:contact_id>/toggle-spam', methods=['POST'])
@custom_login_required
def admin_contact_toggle_spam(contact_id):
    """Toggle spam status of contact submission."""
    contact = ContactSubmission.query.get_or_404(contact_id)

    try:
        # Toggle spam flag
        contact.is_spam = not contact.is_spam
        db.session.commit()

        action = 'marked as spam' if contact.is_spam else 'marked as not spam'
        app.logger.info(f'Contact {contact_id} {action} by {current_user.username}')

        flash(f'Message {action}', 'success')
        return redirect(url_for('admin_contacts_list'))
    except Exception as e:
        db.session.rollback()
        app.logger.error(f'Error toggling spam status: {str(e)}')
        flash('Error updating spam status', 'error')
        return redirect(url_for('admin_contacts_list'))


@app.route('/admin/contacts/<int:contact_id>/delete', methods=['POST'])
@custom_login_required
def admin_contact_delete(contact_id):
    """Delete contact submission permanently."""
    contact = ContactSubmission.query.get_or_404(contact_id)

    try:
        # Log before deleting
        app.logger.info(f'Contact {contact_id} deleted by {current_user.username}: {contact.name} ({contact.email})')

        db.session.delete(contact)
        db.session.commit()

        flash('Message deleted permanently', 'success')
        return redirect(url_for('admin_contacts_list'))
    except Exception as e:
        db.session.rollback()
        app.logger.error(f'Error deleting contact: {str(e)}')
        flash('Error deleting message', 'error')
        return redirect(url_for('admin_contacts_list'))


# ============================================================================
# ADMIN PAGE EDITOR ROUTES
# ============================================================================

@app.route('/admin/pages')
@custom_login_required
def admin_edit_pages():
    """Admin page editor"""
    content_dir = Path(app.root_path) / 'content'

    # Read current content
    fees_content = ''
    schedule_content = ''

    try:
        with open(content_dir / 'fees.md', 'r', encoding='utf-8') as f:
            fees_content = f.read()
    except FileNotFoundError:
        pass

    try:
        with open(content_dir / 'schedule.md', 'r', encoding='utf-8') as f:
            schedule_content = f.read()
    except FileNotFoundError:
        pass

    # Create forms with current content
    fees_form = PageEditForm()
    fees_form.content.data = fees_content

    schedule_form = PageEditForm()
    schedule_form.content.data = schedule_content

    return render_template('admin/edit_pages.html',
                         fees_form=fees_form,
                         schedule_form=schedule_form)


@app.route('/admin/pages/<page>', methods=['POST'])
@custom_login_required
def admin_edit_page(page):
    """Save edited page content"""
    if page not in ['fees', 'schedule']:
        abort(404)

    form = PageEditForm()

    if form.validate_on_submit():
        content_dir = Path(app.root_path) / 'content'
        content_dir.mkdir(exist_ok=True)

        file_path = content_dir / f'{page}.md'

        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(form.content.data)

            flash(f'{page.title()} page updated successfully!', 'success')
            app.logger.info(f"Page {page}.md updated by {current_user.username}")
        except Exception as e:
            flash(f'Error saving page: {str(e)}', 'danger')
            app.logger.error(f"Error saving {page}.md: {str(e)}")
    else:
        flash('Invalid form submission', 'danger')

    return redirect(url_for('admin_edit_pages'))


# ============================================================================
# ADMIN UTILITY ROUTES
# ============================================================================

@app.route('/admin/generate-slug', methods=['POST'])
@custom_login_required
def generate_slug():
    """Generate URL slug from title."""
    data = request.get_json()
    title = data.get('title', '')
    slug = slugify(title) if title else ''
    return jsonify({'slug': slug})


@app.route('/admin/upload-image', methods=['POST'])
@custom_login_required
def upload_image():
    """Upload image for blog post content."""
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    if not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file type'}), 400

    try:
        # Create upload directory if it doesn't exist
        upload_dir = os.path.join(app.config['UPLOAD_FOLDER'], 'blog', 'inline')
        os.makedirs(upload_dir, exist_ok=True)

        # Save image
        result = save_image(file, upload_dir, resize=True, create_thumbnail=False)

        if result:
            # Save metadata to database
            uploaded_file = UploadedFile(
                filename=result['filename'],
                original_filename=result['original_filename'],
                filepath=result['filepath'],
                file_size=result['file_size'],
                mime_type=file.content_type,
                uploaded_by=current_user.id
            )
            db.session.add(uploaded_file)
            db.session.commit()

            # Return URL for TinyMCE
            file_url = url_for('static', filename=f"../uploads/therapist/blog/inline/{result['filename']}")
            return jsonify({'location': file_url})
        else:
            return jsonify({'error': 'Failed to save image'}), 500

    except Exception as e:
        app.logger.error(f'Error uploading image: {str(e)}')
        return jsonify({'error': str(e)}), 500


# CLI commands for database management
@app.cli.command()
def init_db():
    """Initialize the database."""
    db.create_all()
    print('Database initialized successfully.')


@app.cli.command()
def create_admin():
    """Create an admin user."""
    from shared.models import User

    username = input('Enter username: ')
    email = input('Enter email: ')
    password = input('Enter password: ')

    # Check if user already exists
    if User.query.filter_by(username=username).first():
        print(f'User {username} already exists.')
        return

    # Create admin user
    admin = User(
        username=username,
        email=email,
        role='admin'
    )
    admin.set_password(password)

    db.session.add(admin)
    db.session.commit()

    print(f'Admin user {username} created successfully.')


@app.cli.command()
def test_email():
    """Test email configuration."""
    from shared.email import send_email

    recipient = input('Enter recipient email: ')
    result = send_email(
        subject='Test Email from WebGarden',
        recipients=[recipient],
        text_body='This is a test email to verify email configuration.',
        html_body='<p>This is a test email to verify email configuration.</p>'
    )

    if result:
        print('Test email sent successfully!')
    else:
        print('Failed to send test email. Check logs for details.')


# ============================================================================
# BOT API PROXY
# ============================================================================

@app.route('/api/chat', methods=['POST'])
@csrf.exempt
def bot_chat_proxy():
    """Proxy requests to the local bot API."""
    import requests

    try:
        # Get the request data from the browser
        data = request.get_json()

        # Forward to local bot API
        bot_response = requests.post(
            'http://localhost:5002/api/chat',
            json=data,
            headers={'Content-Type': 'application/json'},
            timeout=30
        )

        # Return the bot's response to the browser
        return jsonify(bot_response.json()), bot_response.status_code

    except requests.exceptions.RequestException as e:
        # Handle connection errors to bot API
        return jsonify({
            'error': 'Bot service temporarily unavailable',
            'details': str(e)
        }), 503
    except Exception as e:
        # Handle other errors
        return jsonify({
            'error': 'Internal server error',
            'details': str(e)
        }), 500


# Development server configuration
if __name__ == '__main__':
    # Only for development - use Gunicorn for production
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=app.config['DEBUG']
    )
