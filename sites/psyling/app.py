"""csrf
Psyling Site Flask Application
Main application file for the professional psychotherapy website.
"""

import os
import sys
import hashlib
import secrets
from datetime import datetime, timedelta
from pathlib import Path
from werkzeug.utils import secure_filename
from slugify import slugify
import markdown
import requests
from sqlalchemy import or_

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
from shared.models import (
    BlogPost, ChatMessage, ChatRoom, Client, ContactSubmission, CRMActivity,
    SpamBlocklist, UploadedFile, User,
)
from shared.forms import ContactForm, LoginForm, BlogPostForm, BookingRequestForm
from shared.email import send_contact_notification, send_contact_confirmation
from shared.decorators import login_required as custom_login_required, admin_required, anonymous_required
from shared.sanitizer import sanitize_html, create_excerpt
from shared.image_handler import save_image, allowed_file
from sites.psyling.config import config
from sites.psyling.cli import register_cli_commands
from sites.psyling.crm_forms import (
    ActivityCompleteForm,
    ActivityForm,
    CONTACT_STATUSES,
    ClientForm,
    ContactActionForm,
    ContactCRMForm,
)
from sites.psyling.chat_forms import (
    ChatMessageForm,
    ChatRoomActionForm,
    ChatRoomCreateForm,
    ClientRoomAccessForm,
)

# Additional imports for page editing
from flask_wtf import FlaskForm
from wtforms import TextAreaField
from wtforms.validators import DataRequired

# Create Flask application
config_name = os.getenv('FLASK_ENV', 'production')
app = create_base_app('psyling', config[config_name])

# Register CLI commands
register_cli_commands(app)


@app.after_request
def protect_private_room_responses(response):
    """Prevent client-room pages from being cached, indexed, or leaked as referrers."""
    if request.path == '/room-access' or request.path.startswith('/client-room/'):
        response.headers['X-Robots-Tag'] = 'noindex, nofollow, noarchive'
        response.headers['Cache-Control'] = 'no-store, private'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Referrer-Policy'] = 'no-referrer'
    elif request.path.startswith('/admin/chat-rooms/') and request.path.endswith('/invite'):
        response.headers['Cache-Control'] = 'no-store, private'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Referrer-Policy'] = 'no-referrer'
    return response


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
        unread_count = ContactSubmission.query.filter(
            ContactSubmission.is_read.is_(False),
            ContactSubmission.is_spam.is_(False),
            ContactSubmission.archived_at.is_(None),
        ).count()

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
    """Homepage with recent blog posts."""
    # Get 3 most recent published posts
    recent_posts = BlogPost.query.filter_by(visible=True).order_by(
        BlogPost.published_at.desc()
    ).limit(3).all()

    return render_template('index.html', recent_posts=recent_posts)


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


@app.route('/schedule')
def schedule():
    """Display schedule page with calendar and booking button."""
    return render_template('schedule.html')


@app.route('/contact', methods=['GET', 'POST'])
@limiter.limit(app.config.get('CONTACT_FORM_RATE_LIMIT', '5 per hour'))
def contact():
    """Contact page with form submission."""
    form = ContactForm()

    if request.method == 'POST':
        # SPAM PREVENTION: Check honeypot field
        honeypot = request.form.get('website', '')
        if honeypot:
            # Bot detected - honeypot was filled
            app.logger.warning('Honeypot spam submission rejected')
            # Return fake success to fool the bot
            flash('Thank you for your message! We will get back to you soon.', 'success')
            return redirect(url_for('contact'))

        # SPAM PREVENTION: Check blocklist
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip().lower()

        # Check if name is blocked
        name_blocked = SpamBlocklist.query.filter_by(value=name, type='name').first()
        if name_blocked:
            app.logger.warning('Blocklisted name submission rejected')
            flash('Thank you for your message!', 'success')
            return redirect(url_for('contact'))

        # Check if email is blocked
        email_blocked = SpamBlocklist.query.filter_by(value=email, type='email').first()
        if email_blocked:
            app.logger.warning('Blocklisted email submission rejected')
            flash('Thank you for your message!', 'success')
            return redirect(url_for('contact'))

        # SPAM PREVENTION: Verify reCAPTCHA token if configured
        recaptcha_token = request.form.get('recaptcha_token', '')
        recaptcha_secret = app.config.get('RECAPTCHA_SECRET_KEY')

        if recaptcha_secret and recaptcha_token:
            try:
                # Verify reCAPTCHA with Google
                recaptcha_response = requests.post(
                    'https://www.google.com/recaptcha/api/siteverify',
                    data={
                        'secret': recaptcha_secret,
                        'response': recaptcha_token,
                        'remoteip': request.remote_addr
                    },
                    timeout=5
                )
                recaptcha_result = recaptcha_response.json()

                # Check if verification was successful
                if not recaptcha_result.get('success', False):
                    app.logger.warning(f'reCAPTCHA verification failed from IP {request.remote_addr}: {recaptcha_result}')
                    flash('reCAPTCHA verification failed. Please try again.', 'error')
                    return render_template('contact.html', form=form)

                # Check score (v3 returns score from 0.0 to 1.0, where 1.0 is very likely a good interaction)
                score = recaptcha_result.get('score', 0)
                if score < 0.5:
                    app.logger.warning(f'reCAPTCHA low score from IP {request.remote_addr}: score={score}')
                    flash('Your submission appears suspicious. Please try again later.', 'error')
                    return render_template('contact.html', form=form)

                app.logger.info(f'reCAPTCHA passed from IP {request.remote_addr}: score={score}')

            except requests.exceptions.RequestException as e:
                # Network error - log but allow submission (don't block legitimate users)
                app.logger.error(f'reCAPTCHA verification error: {str(e)}')
            except Exception as e:
                # Other error - log but allow submission
                app.logger.error(f'Unexpected reCAPTCHA error: {str(e)}')
        elif recaptcha_secret and not recaptcha_token:
            # reCAPTCHA is configured but no token provided - likely a bot
            app.logger.warning(f'No reCAPTCHA token provided from IP {request.remote_addr}')
            flash('Security verification required. Please enable JavaScript and try again.', 'error')
            return render_template('contact.html', form=form)

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

            # Send notification emails after the inquiry is safely saved.
            if not submission.is_spam:
                try:
                    if not send_contact_notification(submission):
                        app.logger.error(
                            'Admin notification delivery failed for contact submission %s; inquiry remains saved',
                            submission.id,
                        )
                except Exception:
                    app.logger.exception(
                        'Unexpected admin notification error for contact submission %s; inquiry remains saved',
                        submission.id,
                    )

            try:
                if not send_contact_confirmation(submission):
                    app.logger.error(
                        'Contact confirmation delivery failed for contact submission %s',
                        submission.id,
                    )
            except Exception:
                app.logger.exception(
                    'Unexpected contact confirmation error for contact submission %s',
                    submission.id,
                )

            flash('Thank you for your message! We will get back to you soon.', 'success')
            return redirect(url_for('contact'))

        except Exception:
            db.session.rollback()
            app.logger.error('Error saving contact submission')
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
@admin_required
def admin_dashboard():
    """Admin dashboard."""
    # Get statistics
    stats = {
        'total_posts': BlogPost.query.count(),
        'total_contacts': ContactSubmission.query.count(),
        'unread_contacts': ContactSubmission.query.filter(
            ContactSubmission.is_read.is_(False),
            ContactSubmission.is_spam.is_(False),
            ContactSubmission.archived_at.is_(None),
        ).count()
    }

    # Get recent posts (5 most recent)
    recent_posts = BlogPost.query.order_by(BlogPost.updated_at.desc()).limit(5).all()

    # Get recent contacts (5 most recent)
    recent_contacts = ContactSubmission.query.order_by(
        ContactSubmission.submitted_at.desc()
    ).limit(5).all()

    open_followups = CRMActivity.query.filter(
        or_(CRMActivity.due_at.isnot(None), CRMActivity.activity_type == 'follow_up'),
        CRMActivity.completed_at.is_(None),
    ).order_by(CRMActivity.due_at.asc().nullslast(), CRMActivity.id.asc()).limit(25).all()

    return render_template(
        'admin/dashboard.html',
        stats=stats,
        recent_posts=recent_posts,
        recent_contacts=recent_contacts,
        open_followups=open_followups,
        now=datetime.utcnow(),
        complete_form=ActivityCompleteForm(),
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
@admin_required
def admin_contacts_list():
    """List contact submissions with privacy-conscious CRM filtering."""
    page = request.args.get('page', 1, type=int)
    status_filter = request.args.get('status', '').strip().lower()
    view_filter = request.args.get('show', 'inbox').strip().lower()
    search = request.args.get('q', '').strip()[:100]

    if status_filter and status_filter not in CONTACT_STATUSES:
        abort(400)
    if view_filter not in {'inbox', 'spam', 'archived'}:
        abort(400)

    query = ContactSubmission.query

    if view_filter == 'archived':
        query = query.filter(ContactSubmission.archived_at.isnot(None))
    else:
        query = query.filter(ContactSubmission.archived_at.is_(None))
        query = query.filter(ContactSubmission.is_spam.is_(view_filter == 'spam'))

    if status_filter:
        query = query.filter_by(status=status_filter)

    if search:
        escaped = search.replace('\\', '\\\\').replace('%', '\\%').replace('_', '\\_')
        pattern = f'%{escaped}%'
        query = query.filter(or_(
            ContactSubmission.name.ilike(pattern, escape='\\'),
            ContactSubmission.email.ilike(pattern, escape='\\'),
            ContactSubmission.phone.ilike(pattern, escape='\\'),
        ))

    contacts = query.order_by(ContactSubmission.submitted_at.desc()).paginate(
        page=page,
        per_page=20,
        error_out=False
    )

    active = ContactSubmission.query.filter(ContactSubmission.archived_at.is_(None))
    counts = {
        'all': ContactSubmission.query.count(),
        'inbox': active.filter(ContactSubmission.is_spam.is_(False)).count(),
        'spam': active.filter(ContactSubmission.is_spam.is_(True)).count(),
        'archived': ContactSubmission.query.filter(
            ContactSubmission.archived_at.isnot(None)
        ).count(),
    }
    counts.update({
        status: active.filter(
            ContactSubmission.is_spam.is_(False),
            ContactSubmission.status == status,
        ).count()
        for status in CONTACT_STATUSES if status != 'spam'
    })

    return render_template(
        'admin/contacts_list.html',
        contacts=contacts,
        pagination=contacts,
        counts=counts,
        statuses=CONTACT_STATUSES,
        status_filter=status_filter,
        view_filter=view_filter,
        search=search,
        endpoint='admin_contacts_list',
        kwargs={'show': view_filter, 'status': status_filter, 'q': search}
    )


@app.route('/admin/contacts/<int:contact_id>/view')
@admin_required
def admin_contact_view(contact_id):
    """Show one contact on a normal, JavaScript-independent HTML page."""
    contact = ContactSubmission.query.get_or_404(contact_id)
    crm_form = ContactCRMForm(obj=contact)
    action_form = ContactActionForm()
    activities = contact.activities.order_by(
        CRMActivity.created_at.desc(), CRMActivity.id.desc()
    ).all()
    return render_template(
        'admin/contact_detail.html',
        contact=contact,
        crm_form=crm_form,
        action_form=action_form,
        activity_form=ActivityForm(),
        complete_form=ActivityCompleteForm(),
        activities=activities,
        now=datetime.utcnow(),
    )


@app.route('/admin/contacts/<int:contact_id>')
@admin_required
def admin_contact_view_legacy(contact_id):
    """Keep old inquiry links working while the explicit HTML route is adopted."""
    return admin_contact_view(contact_id)

@app.route('/admin/contacts/<int:contact_id>/crm', methods=['POST'])
@admin_required
def admin_contact_update_crm(contact_id):
    """Update validated CRM status, notes, and follow-up date."""
    contact = ContactSubmission.query.get_or_404(contact_id)
    form = ContactCRMForm()
    if not form.validate_on_submit():
        flash('Please correct the CRM form fields.', 'error')
        activities = contact.activities.order_by(
            CRMActivity.created_at.desc(), CRMActivity.id.desc()
        ).all()
        return render_template(
            'admin/contact_detail.html',
            contact=contact,
            crm_form=form,
            action_form=ContactActionForm(),
            activity_form=ActivityForm(),
            complete_form=ActivityCompleteForm(),
            activities=activities,
            now=datetime.utcnow(),
        ), 400

    try:
        contact.status = form.status.data
        contact.notes = form.notes.data or None
        contact.follow_up_at = form.follow_up_at.data
        if contact.status == 'spam':
            contact.mark_as_spam()
        elif contact.is_spam:
            contact.mark_as_not_spam()
            contact.status = form.status.data
        db.session.commit()
        app.logger.info('CRM contact %s updated by admin user %s', contact.id, current_user.id)
        flash('Contact updated.', 'success')
    except Exception:
        db.session.rollback()
        app.logger.exception('CRM contact %s update failed', contact.id)
        flash('Contact update failed.', 'error')
    return redirect(url_for('admin_contact_view', contact_id=contact.id))


@app.route('/admin/contacts/<int:contact_id>/toggle-read', methods=['POST'])
@admin_required
def admin_contact_toggle_read(contact_id):
    """Toggle read state independently of workflow status."""
    form = ContactActionForm()
    if not form.validate_on_submit():
        abort(400)
    contact = ContactSubmission.query.get_or_404(contact_id)
    contact.mark_as_unread() if contact.is_read else contact.mark_as_read()
    db.session.commit()
    app.logger.info('CRM contact %s read state changed by admin user %s', contact.id, current_user.id)
    return redirect(url_for('admin_contact_view', contact_id=contact.id))


@app.route('/admin/contacts/<int:contact_id>/mark-contacted', methods=['POST'])
@admin_required
def admin_contact_mark_contacted(contact_id):
    """Record contact activity without sending an email."""
    form = ContactActionForm()
    if not form.validate_on_submit():
        abort(400)
    contact = ContactSubmission.query.get_or_404(contact_id)
    contact.last_contacted_at = datetime.utcnow()
    contact.is_read = True
    if contact.status == 'new':
        contact.status = 'contacted'
    db.session.commit()
    app.logger.info('CRM contact %s marked contacted by admin user %s', contact.id, current_user.id)
    return redirect(url_for('admin_contact_view', contact_id=contact.id))


@app.route('/admin/contacts/<int:contact_id>/toggle-spam', methods=['POST'])
@admin_required
def admin_contact_toggle_spam(contact_id):
    """Toggle spam status of contact submission."""
    form = ContactActionForm()
    if not form.validate_on_submit():
        abort(400)
    contact = ContactSubmission.query.get_or_404(contact_id)

    try:
        if contact.is_spam:
            contact.mark_as_not_spam()
        else:
            contact.mark_as_spam()
        db.session.commit()
        app.logger.info('CRM contact %s spam state changed by admin user %s', contact.id, current_user.id)
        flash('Spam state updated.', 'success')
    except Exception:
        db.session.rollback()
        app.logger.exception('CRM contact %s spam update failed', contact.id)
        flash('Spam update failed.', 'error')
    return redirect(url_for('admin_contact_view', contact_id=contact.id))


@app.route('/admin/contacts/<int:contact_id>/archive', methods=['POST'])
@admin_required
def admin_contact_toggle_archive(contact_id):
    """Archive or restore a contact without deleting private records."""
    form = ContactActionForm()
    if not form.validate_on_submit():
        abort(400)
    contact = ContactSubmission.query.get_or_404(contact_id)
    contact.archived_at = None if contact.archived_at else datetime.utcnow()
    db.session.commit()
    app.logger.info('CRM contact %s archive state changed by admin user %s', contact.id, current_user.id)
    flash('Archive state updated.', 'success')
    return redirect(url_for('admin_contact_view', contact_id=contact.id))


# ============================================================================
# ADMIN CLIENT CRM ROUTES
# ============================================================================

def _apply_client_form(client, form):
    """Apply validated client fields without touching related contact data."""
    client.name = form.name.data.strip()
    client.email = (form.email.data or '').strip() or None
    client.phone = (form.phone.data or '').strip() or None
    client.preferred_contact_method = form.preferred_contact_method.data
    client.language = form.language.data
    client.status = form.status.data
    client.private_notes = form.private_notes.data or None


@app.route('/admin/clients')
@admin_required
def admin_clients_list():
    """List and search minimal client records."""
    page = request.args.get('page', 1, type=int)
    status_filter = request.args.get('status', '').strip().lower()
    search = request.args.get('q', '').strip()[:100]
    allowed_statuses = {'active', 'inactive', 'archived'}
    if status_filter and status_filter not in allowed_statuses:
        abort(400)

    query = Client.query
    if status_filter:
        query = query.filter_by(status=status_filter)
    if search:
        escaped = search.replace('\\', '\\\\').replace('%', '\\%').replace('_', '\\_')
        pattern = f'%{escaped}%'
        query = query.filter(or_(
            Client.name.ilike(pattern, escape='\\'),
            Client.email.ilike(pattern, escape='\\'),
            Client.phone.ilike(pattern, escape='\\'),
        ))

    clients = query.order_by(Client.updated_at.desc(), Client.id.desc()).paginate(
        page=page, per_page=20, error_out=False
    )
    counts = {
        status: Client.query.filter_by(status=status).count()
        for status in allowed_statuses
    }
    counts['all'] = Client.query.count()
    return render_template(
        'admin/clients_list.html',
        clients=clients,
        pagination=clients,
        counts=counts,
        status_filter=status_filter,
        search=search,
        endpoint='admin_clients_list',
        kwargs={'status': status_filter, 'q': search},
    )


@app.route('/admin/clients/new', methods=['GET', 'POST'])
@admin_required
def admin_client_create():
    """Create a client manually."""
    form = ClientForm()
    if form.validate_on_submit():
        client = Client()
        _apply_client_form(client, form)
        try:
            db.session.add(client)
            db.session.commit()
            app.logger.info('CRM client %s created by admin user %s', client.id, current_user.id)
            flash('Client created.', 'success')
            return redirect(url_for('admin_client_view', client_id=client.id))
        except Exception:
            db.session.rollback()
            app.logger.exception('CRM client creation failed')
            flash('Client creation failed.', 'error')
    return render_template('admin/client_form.html', form=form, client=None)


@app.route('/admin/clients/<int:client_id>')
@admin_required
def admin_client_view(client_id):
    """Show a client and linked contact submissions."""
    client = Client.query.get_or_404(client_id)
    contacts = client.contact_submissions.order_by(
        ContactSubmission.submitted_at.desc()
    ).all()
    activities = client.activities.order_by(
        CRMActivity.created_at.desc(), CRMActivity.id.desc()
    ).all()
    chat_rooms = client.chat_rooms.order_by(ChatRoom.updated_at.desc()).all()
    return render_template(
        'admin/client_detail.html', client=client, contacts=contacts,
        activity_form=ActivityForm(), complete_form=ActivityCompleteForm(),
        activities=activities, chat_rooms=chat_rooms, now=datetime.utcnow(),
    )


def _create_activity(form, client=None, contact=None):
    """Persist one validated private activity without logging its content."""
    activity = CRMActivity(
        client=client,
        contact_submission=contact,
        actor_user_id=current_user.id,
        activity_type=form.activity_type.data,
        body=form.body.data.strip(),
        due_at=form.due_at.data,
    )
    db.session.add(activity)
    db.session.commit()
    app.logger.info('CRM activity %s created by admin user %s', activity.id, current_user.id)


@app.route('/admin/clients/<int:client_id>/activities', methods=['POST'])
@admin_required
def admin_client_activity_create(client_id):
    client = Client.query.get_or_404(client_id)
    form = ActivityForm()
    if not form.validate_on_submit():
        flash('Please correct the activity form fields.', 'error')
        return redirect(url_for('admin_client_view', client_id=client.id))
    try:
        _create_activity(form, client=client)
        flash('Activity added.', 'success')
    except Exception:
        db.session.rollback()
        app.logger.exception('CRM client activity creation failed for client %s', client.id)
        flash('Activity could not be added.', 'error')
    return redirect(url_for('admin_client_view', client_id=client.id))


@app.route('/admin/contacts/<int:contact_id>/activities', methods=['POST'])
@admin_required
def admin_contact_activity_create(contact_id):
    contact = ContactSubmission.query.get_or_404(contact_id)
    form = ActivityForm()
    if not form.validate_on_submit():
        flash('Please correct the activity form fields.', 'error')
        return redirect(url_for('admin_contact_view', contact_id=contact.id))
    try:
        _create_activity(form, contact=contact)
        flash('Activity added.', 'success')
    except Exception:
        db.session.rollback()
        app.logger.exception('CRM contact activity creation failed for contact %s', contact.id)
        flash('Activity could not be added.', 'error')
    return redirect(url_for('admin_contact_view', contact_id=contact.id))


@app.route('/admin/activities/<int:activity_id>/complete', methods=['POST'])
@admin_required
def admin_activity_complete(activity_id):
    form = ActivityCompleteForm()
    if not form.validate_on_submit():
        abort(400)
    activity = CRMActivity.query.get_or_404(activity_id)
    if activity.completed_at is None and (
        activity.due_at is not None or activity.activity_type == 'follow_up'
    ):
        activity.completed_at = datetime.utcnow()
        db.session.commit()
        app.logger.info('CRM activity %s completed by admin user %s', activity.id, current_user.id)
        flash('Follow-up completed.', 'success')
    target = request.form.get('next', '')
    if target.startswith('/admin/'):
        return redirect(target)
    if activity.client_id:
        return redirect(url_for('admin_client_view', client_id=activity.client_id))
    return redirect(url_for('admin_contact_view', contact_id=activity.contact_submission_id))


@app.route('/admin/clients/<int:client_id>/edit', methods=['GET', 'POST'])
@admin_required
def admin_client_edit(client_id):
    """Edit a client without modifying linked submissions."""
    client = Client.query.get_or_404(client_id)
    form = ClientForm(obj=client)
    if form.validate_on_submit():
        _apply_client_form(client, form)
        try:
            db.session.commit()
            app.logger.info('CRM client %s updated by admin user %s', client.id, current_user.id)
            flash('Client updated.', 'success')
            return redirect(url_for('admin_client_view', client_id=client.id))
        except Exception:
            db.session.rollback()
            app.logger.exception('CRM client %s update failed', client.id)
            flash('Client update failed.', 'error')
    return render_template('admin/client_form.html', form=form, client=client)


@app.route('/admin/contacts/<int:contact_id>/convert', methods=['GET', 'POST'])
@admin_required
def admin_contact_convert_to_client(contact_id):
    """Create and atomically link one client from one contact submission."""
    contact = ContactSubmission.query.get_or_404(contact_id)
    if contact.client_id:
        flash('This contact is already linked to a client.', 'info')
        return redirect(url_for('admin_client_view', client_id=contact.client_id))

    form = ClientForm()
    if request.method == 'GET':
        form.name.data = contact.name
        form.email.data = contact.email
        form.phone.data = contact.phone
        form.preferred_contact_method.data = (
            'email' if contact.email else ('phone' if contact.phone else 'none')
        )
        form.language.data = 'unknown'
        form.status.data = 'active'

    if form.validate_on_submit():
        try:
            locked_contact = ContactSubmission.query.filter_by(
                id=contact_id
            ).with_for_update().first_or_404()
            if locked_contact.client_id:
                existing_client_id = locked_contact.client_id
                db.session.rollback()
                flash('This contact is already linked to a client.', 'info')
                return redirect(
                    url_for('admin_client_view', client_id=existing_client_id)
                )

            client = Client()
            _apply_client_form(client, form)
            db.session.add(client)
            db.session.flush()
            locked_contact.client_id = client.id
            db.session.commit()
            app.logger.info(
                'CRM contact %s converted to client %s by admin user %s',
                locked_contact.id,
                client.id,
                current_user.id,
            )
            flash('Contact converted to a client.', 'success')
            return redirect(url_for('admin_client_view', client_id=client.id))
        except Exception:
            db.session.rollback()
            app.logger.exception('CRM contact %s conversion failed', contact_id)
            flash('Contact conversion failed.', 'error')

    return render_template(
        'admin/contact_convert.html', contact=contact, form=form
    )


# ============================================================================
# PRIVATE CLIENT CHAT ROOMS
# ============================================================================

def _token_digest(token):
    return hashlib.sha256(token.encode('utf-8')).hexdigest()


def _client_room_granted(room):
    grants = session.get('client_room_access', {})
    return (
        _invite_state(room) == 'active'
        and room.status in {'active', 'closed'}
        and grants.get(str(room.id)) == room.access_version
    )


def _invite_state(room, now=None):
    """Return active, expired, or revoked without exposing token material."""
    now = now or datetime.utcnow()
    if not room.invite_token_hash or not room.client_access_enabled:
        return 'revoked'
    if not room.invite_expires_at or room.invite_expires_at <= now:
        return 'expired'
    return 'active'


def _chat_messages(room):
    return room.messages.order_by(
        ChatMessage.created_at.asc(), ChatMessage.id.asc()
    ).all()


@app.route('/admin/chat-rooms')
@admin_required
def admin_chat_rooms_list():
    rooms = ChatRoom.query.order_by(ChatRoom.updated_at.desc(), ChatRoom.id.desc()).all()
    room_rows = []
    for room in rooms:
        latest = room.messages.order_by(ChatMessage.created_at.desc(), ChatMessage.id.desc()).first()
        unread = room.messages.filter_by(sender_type='client', read_by_admin_at=None).count()
        room_rows.append((room, latest, unread))
    return render_template('admin/chat_rooms_list.html', room_rows=room_rows)


@app.route('/admin/chat-rooms/new', methods=['GET', 'POST'])
@admin_required
def admin_chat_room_create():
    form = ChatRoomCreateForm()
    clients = Client.query.order_by(Client.name.asc(), Client.id.asc()).all()
    form.client_id.choices = [(client.id, f'Client #{client.id} — {client.name}') for client in clients]
    requested_client_id = request.args.get('client_id', type=int)
    if request.method == 'GET' and requested_client_id in {client.id for client in clients}:
        form.client_id.data = requested_client_id
    if form.validate_on_submit():
        client = db.session.get(Client, form.client_id.data)
        if client is None:
            abort(400)
        room = ChatRoom(
            client_id=client.id,
            title=(form.title.data or '').strip() or None,
            created_by_user_id=current_user.id,
        )
        db.session.add(room)
        db.session.commit()
        app.logger.info('Chat room %s created by admin user %s', room.id, current_user.id)
        flash('Private chat room created.', 'success')
        return redirect(url_for('admin_chat_room_view', room_id=room.id))
    return render_template('admin/chat_room_form.html', form=form, clients=clients)


@app.route('/admin/chat-rooms/<int:room_id>')
@admin_required
def admin_chat_room_view(room_id):
    room = ChatRoom.query.get_or_404(room_id)
    now = datetime.utcnow()
    unread = ChatMessage.query.filter_by(
        room_id=room.id, sender_type='client', read_by_admin_at=None
    ).update({'read_by_admin_at': now}, synchronize_session=False)
    if unread:
        db.session.commit()
    return render_template(
        'admin/chat_room_detail.html', room=room, messages=_chat_messages(room),
        message_form=ChatMessageForm(), action_form=ChatRoomActionForm(),
        invite_state=_invite_state(room),
    )


@app.route('/admin/chat-rooms/<int:room_id>/messages', methods=['POST'])
@admin_required
@limiter.limit('30 per minute')
def admin_chat_message_create(room_id):
    room = ChatRoom.query.get_or_404(room_id)
    form = ChatMessageForm()
    if room.status != 'active':
        flash('Reopen the room before sending a message.', 'warning')
    elif form.validate_on_submit():
        message = ChatMessage(
            room_id=room.id, sender_type='admin', sender_user_id=current_user.id,
            body=form.body.data.strip(), read_by_admin_at=datetime.utcnow(),
        )
        room.updated_at = datetime.utcnow()
        db.session.add(message)
        db.session.commit()
        app.logger.info('Chat message %s added to room %s by admin user %s', message.id, room.id, current_user.id)
        flash('Message sent.', 'success')
    else:
        flash('Enter a message of 10,000 characters or fewer.', 'error')
    return redirect(url_for('admin_chat_room_view', room_id=room.id))


@app.route('/admin/chat-rooms/<int:room_id>/invite', methods=['POST'])
@admin_required
@limiter.limit('10 per hour')
def admin_chat_room_invite(room_id):
    room = ChatRoom.query.get_or_404(room_id)
    form = ChatRoomActionForm()
    if not form.validate_on_submit():
        abort(400)
    if room.status == 'archived':
        flash('Reopen the room before generating an invite.', 'warning')
        return redirect(url_for('admin_chat_room_view', room_id=room.id))
    token = secrets.token_urlsafe(32)
    room.invite_token_hash = _token_digest(token)
    now = datetime.utcnow()
    room.invite_created_at = now
    room.invite_expires_at = now + timedelta(days=14)
    room.invite_last_used_at = None
    room.client_access_enabled = True
    room.access_version += 1
    db.session.commit()
    app.logger.info('Chat room %s invite regenerated by admin user %s', room.id, current_user.id)
    invite_url = url_for('client_room_access', _external=True, _scheme='https') + '#' + token
    return render_template('admin/chat_room_invite.html', room=room, invite_url=invite_url)


@app.route('/admin/chat-rooms/<int:room_id>/invite/revoke', methods=['POST'])
@admin_required
def admin_chat_room_invite_revoke(room_id):
    room = ChatRoom.query.get_or_404(room_id)
    form = ChatRoomActionForm()
    if not form.validate_on_submit():
        abort(400)
    room.invite_token_hash = None
    room.invite_expires_at = datetime.utcnow()
    room.client_access_enabled = False
    room.access_version += 1
    db.session.commit()
    app.logger.info('Chat room %s invite revoked by admin user %s', room.id, current_user.id)
    flash('Client invite and active client sessions revoked.', 'success')
    return redirect(url_for('admin_chat_room_view', room_id=room.id))


@app.route('/admin/chat-rooms/<int:room_id>/state/<action>', methods=['POST'])
@admin_required
def admin_chat_room_state(room_id, action):
    room = ChatRoom.query.get_or_404(room_id)
    form = ChatRoomActionForm()
    if not form.validate_on_submit() or action not in {'close', 'reopen', 'archive'}:
        abort(400)
    valid_transition = (
        (action == 'close' and room.status == 'active')
        or (action == 'reopen' and room.status in {'closed', 'archived'})
        or (action == 'archive' and room.status in {'active', 'closed'})
    )
    if not valid_transition:
        abort(400)
    now = datetime.utcnow()
    if action == 'close':
        room.status = 'closed'
        room.closed_at = now
    elif action == 'reopen':
        room.status = 'active'
        room.closed_at = None
        room.archived_at = None
        room.client_access_enabled = (
            room.invite_token_hash is not None
            and room.invite_expires_at is not None
            and room.invite_expires_at > now
        )
    else:
        room.status = 'archived'
        room.archived_at = now
        room.client_access_enabled = False
        room.invite_token_hash = None
        room.invite_expires_at = now
        room.access_version += 1
    room.updated_at = now
    db.session.commit()
    app.logger.info('Chat room %s state changed to %s by admin user %s', room.id, room.status, current_user.id)
    flash(f'Room is now {room.status}.', 'success')
    return redirect(url_for('admin_chat_room_view', room_id=room.id))


@app.route('/room-access', methods=['GET', 'POST'])
@limiter.limit('10 per minute')
def client_room_access():
    form = ClientRoomAccessForm()
    if form.validate_on_submit():
        digest = _token_digest(form.token.data.strip())
        room = ChatRoom.query.filter_by(invite_token_hash=digest).first()
        if room and _invite_state(room) == 'active' and room.status in {'active', 'closed'}:
            session.clear()
            session.permanent = True
            session['client_room_access'] = {str(room.id): room.access_version}
            room.invite_last_used_at = datetime.utcnow()
            db.session.commit()
            app.logger.info('Client access established for chat room %s', room.id)
            return redirect(url_for('client_room_view', room_id=room.id))
        flash('This access link is invalid or no longer active.', 'error')
    return render_template('client_room/access.html', form=form)


@app.route('/client-room/<int:room_id>')
def client_room_view(room_id):
    room = ChatRoom.query.get_or_404(room_id)
    if not _client_room_granted(room):
        abort(404)
    now = datetime.utcnow()
    unread = ChatMessage.query.filter_by(
        room_id=room.id, sender_type='admin', read_by_client_at=None
    ).update({'read_by_client_at': now}, synchronize_session=False)
    if unread:
        db.session.commit()
    return render_template(
        'client_room/room.html', room=room, messages=_chat_messages(room),
        message_form=ChatMessageForm(), action_form=ChatRoomActionForm(),
    )


@app.route('/client-room/<int:room_id>/messages', methods=['POST'])
@limiter.limit('20 per minute')
def client_room_message_create(room_id):
    room = ChatRoom.query.get_or_404(room_id)
    if not _client_room_granted(room):
        abort(404)
    form = ChatMessageForm()
    if room.status != 'active':
        flash('This room is closed and cannot accept new messages.', 'warning')
    elif form.validate_on_submit():
        message = ChatMessage(
            room_id=room.id, sender_type='client', body=form.body.data.strip(),
            read_by_client_at=datetime.utcnow(),
        )
        room.updated_at = datetime.utcnow()
        db.session.add(message)
        db.session.commit()
        app.logger.info('Client chat message %s added to room %s', message.id, room.id)
        flash('Message sent.', 'success')
    else:
        flash('Enter a message of 10,000 characters or fewer.', 'error')
    return redirect(url_for('client_room_view', room_id=room.id))


@app.route('/client-room/logout', methods=['POST'])
def client_room_logout():
    form = ChatRoomActionForm()
    if not form.validate_on_submit():
        abort(400)
    session.pop('client_room_access', None)
    flash('Private room access ended.', 'success')
    return redirect(url_for('client_room_access'))


# ============================================================================
# ADMIN BLOCKLIST ROUTES
# ============================================================================

@app.route('/admin/blocklist')
@admin_required
def admin_blocklist():
    """View spam blocklist"""
    entries = SpamBlocklist.query.order_by(SpamBlocklist.created_at.desc()).all()
    return render_template('admin/blocklist.html', entries=entries)


@app.route('/admin/blocklist/add', methods=['POST'])
@admin_required
def admin_blocklist_add():
    """Add entry to blocklist"""
    value = request.form.get('value', '').strip()
    entry_type = request.form.get('type', 'name')
    reason = request.form.get('reason', '').strip()

    if not value:
        flash('Please enter a name or email to block', 'danger')
        return redirect(url_for('admin_blocklist'))

    # Normalize email addresses to lowercase
    if entry_type == 'email':
        value = value.lower()

    # Check if already exists
    existing = SpamBlocklist.query.filter_by(value=value, type=entry_type).first()
    if existing:
        flash(f'{entry_type.title()} "{value}" is already blocked', 'warning')
        return redirect(url_for('admin_blocklist'))

    # Add to blocklist
    entry = SpamBlocklist(
        value=value,
        type=entry_type,
        reason=reason,
        created_by=current_user.username
    )
    db.session.add(entry)
    db.session.commit()

    app.logger.info('Blocklist entry %s added by admin user %s', entry.id, current_user.id)
    flash(f'Blocked {entry_type}: {value}', 'success')
    return redirect(url_for('admin_blocklist'))


@app.route('/admin/blocklist/delete/<int:id>', methods=['POST'])
@admin_required
def admin_blocklist_delete(id):
    """Remove entry from blocklist"""
    entry = SpamBlocklist.query.get_or_404(id)
    value = entry.value
    entry_type = entry.type

    db.session.delete(entry)
    db.session.commit()

    app.logger.info('Blocklist entry %s removed by admin user %s', id, current_user.id)
    flash(f'Unblocked {entry_type}: {value}', 'success')
    return redirect(url_for('admin_blocklist'))


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
            file_url = url_for('static', filename=f"../uploads/psyling/blog/inline/{result['filename']}")
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
def test_email():
    """Test email configuration without printing secret values."""
    from shared.email import send_email

    recipient = input('Enter recipient email: ')
    required_vars = [
        'MAIL_SERVER',
        'MAIL_PORT',
        'MAIL_USERNAME',
        'MAIL_PASSWORD',
        'MAIL_DEFAULT_SENDER',
        'ADMIN_EMAIL',
    ]
    print('Email configuration:')
    for key in required_vars:
        value = app.config.get(key)
        if key == 'MAIL_PASSWORD':
            display = 'set' if value else 'missing'
        else:
            display = value or 'missing'
        print(f'  {key}: {display}')

    result = send_email(
        subject='Test Email from Psyling',
        recipients=[recipient],
        text_body='This is a test email to verify Psyling email configuration.',
        html_body='<p>This is a test email to verify Psyling email configuration.</p>'
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
