"""
Therapist Site Flask Application
Main application file for the professional psychotherapy website.
"""

import os
import sys
from datetime import datetime

# Add parent directories to Python path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from flask import render_template, request, flash, redirect, url_for
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import shared modules
from shared.base_app import create_base_app, db, limiter
from shared.models import ContactSubmission
from shared.forms import ContactForm
from shared.email import send_contact_notification, send_contact_confirmation
from sites.therapist.config import config

# Create Flask application
config_name = os.getenv('FLASK_ENV', 'production')
app = create_base_app('therapist', config[config_name])

# Context processor to inject current year and site info
@app.context_processor
def inject_globals():
    """Inject global variables into all templates."""
    return {
        'current_year': datetime.now().year,
        'site_name': app.config['SITE_NAME'],
        'site_tagline': app.config['SITE_TAGLINE']
    }


# Routes
@app.route('/')
def index():
    """Home page route."""
    return render_template('index.html')


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
