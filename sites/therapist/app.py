"""
Therapist Site Flask Application
Main application file for the professional psychotherapy website.
"""

import os
import sys
from datetime import datetime
from werkzeug.utils import secure_filename
from slugify import slugify

# Add parent directories to Python path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from flask import render_template, request, flash, redirect, url_for, jsonify, abort
from flask_login import login_user, logout_user, current_user, login_required
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import shared modules
from shared.base_app import create_base_app, db, limiter
from shared.models import ContactSubmission, User, BlogPost, UploadedFile
from shared.forms import ContactForm, LoginForm, BlogPostForm
from shared.email import send_contact_notification, send_contact_confirmation
from shared.decorators import login_required as custom_login_required, admin_required, anonymous_required
from shared.sanitizer import sanitize_html, create_excerpt
from shared.image_handler import save_image, allowed_file
from sites.therapist.config import config
from sites.therapist.cli import register_cli_commands

# Create Flask application
config_name = os.getenv('FLASK_ENV', 'production')
app = create_base_app('therapist', config[config_name])

# Register CLI commands
register_cli_commands(app)

# Context processor to inject current year and site info
@app.context_processor
def inject_globals():
    """Inject global variables into all templates."""
    unread_count = 0
    if current_user.is_authenticated:
        unread_count = ContactSubmission.query.filter_by(status='new').count()

    return {
        'current_year': datetime.now().year,
        'site_name': app.config['SITE_NAME'],
        'site_tagline': app.config['SITE_TAGLINE'],
        'unread_contacts_count': unread_count
    }


# ============================================================================
# PUBLIC ROUTES
# ============================================================================

@app.route('/')
def index():
    """Home page route with recent blog posts."""
    # Get 3 most recent published blog posts
    recent_posts = BlogPost.query.filter_by(visible=True).filter(
        BlogPost.published_at.isnot(None)
    ).order_by(BlogPost.published_at.desc()).limit(3).all()

    # Add excerpts to posts
    for post in recent_posts:
        post.excerpt = create_excerpt(post.content, 150)

    return render_template('index.html', recent_posts=recent_posts)


@app.route('/about')
def about():
    """About page route."""
    return render_template('about.html')


@app.route('/services')
def services():
    """Services page route."""
    return render_template('services.html')


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
    posts = query.order_by(BlogPost.updated_at.desc()).paginate(
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
        posts=posts,
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

    query = ContactSubmission.query

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
        'new': ContactSubmission.query.filter_by(status='new').count(),
        'read': ContactSubmission.query.filter_by(status='read').count(),
        'responded': ContactSubmission.query.filter_by(status='responded').count()
    }

    return render_template(
        'admin/contacts_list.html',
        contacts=contacts,
        counts=counts,
        status_filter=status_filter,
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


# Development server configuration
if __name__ == '__main__':
    # Only for development - use Gunicorn for production
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=app.config['DEBUG']
    )
