"""
Flask Application
"""

import os
import sys
from datetime import datetime

# Add parent directories to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
sys.path.insert(0, os.path.dirname(__file__))

from flask import flash, redirect, render_template, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, Optional
from dotenv import load_dotenv

load_dotenv()

# Import shared modules
from shared.base_app import create_base_app, db, limiter, login_manager
from shared.models import ContactSubmission, User
from config import config
from cli import register_cli_commands

# Create Flask application
config_name = os.getenv('FLASK_ENV', 'production')
app = create_base_app('poolemergency', config[config_name])

# Register CLI commands
register_cli_commands(app)


class PoolEmergencyContactForm(FlaskForm):
    """Contact form tailored to small pool liner repair requests."""

    name = StringField(
        'Name',
        validators=[
            DataRequired(message='Please enter your name.'),
            Length(min=2, max=100, message='Name must be between 2 and 100 characters.'),
        ],
    )
    phone = StringField(
        'Phone',
        validators=[
            DataRequired(message='Please enter your phone number.'),
            Length(max=20, message='Phone number too long.'),
        ],
    )
    email = StringField(
        'Email',
        validators=[
            Optional(),
            Email(message='Please enter a valid email address.'),
            Length(max=120),
        ],
    )
    location = StringField(
        'Location or neighbourhood',
        validators=[
            DataRequired(message='Please enter your location or neighbourhood.'),
            Length(max=120),
        ],
    )
    material = StringField(
        'Pool type or material',
        validators=[Optional(), Length(max=160)],
    )
    message = TextAreaField(
        'What happened',
        validators=[
            DataRequired(message='Please describe the problem.'),
            Length(min=10, max=5000, message='Message must be between 10 and 5000 characters.'),
        ],
    )

# User loader for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    """Load user by ID for Flask-Login."""
    return User.query.get(int(user_id))

# Context processor
@app.context_processor
def inject_globals():
    """Inject global variables into all templates."""
    return {
        'current_year': datetime.now().year,
        'site_name': app.config['SITE_NAME']
    }

# Routes
@app.route('/')
def index():
    """Home page."""
    return render_template('index.html')

@app.route('/services')
def services():
    """Services page."""
    return render_template('services.html')

@app.route('/about')
def about():
    """About page."""
    return render_template('about.html')

@app.route('/contact', methods=['GET', 'POST'])
@limiter.limit(app.config.get('CONTACT_FORM_RATE_LIMIT', '5 per hour'))
def contact():
    """Contact page with repair inquiry submission."""
    form = PoolEmergencyContactForm()

    if form.validate_on_submit():
        try:
            details = [
                f"Location/neighbourhood: {form.location.data}",
                f"Pool type/material: {form.material.data or 'Not sure / not provided'}",
                "",
                "What happened:",
                form.message.data,
            ]
            submission = ContactSubmission(
                name=form.name.data,
                email=form.email.data or 'no-email-provided@poolemergency.local',
                phone=form.phone.data,
                message='\n'.join(details),
            )
            db.session.add(submission)
            db.session.commit()
            flash('Thanks. Your repair request was sent. Call or text 403-669-0220 if it is urgent.', 'success')
            return redirect(url_for('contact'))
        except Exception as error:
            db.session.rollback()
            app.logger.error(f'Error saving PoolEmergency contact submission: {str(error)}')
            flash('The form could not be sent right now. Please call or text 403-669-0220.', 'error')

    return render_template('contact.html', form=form)

@app.route('/blog')
def blog():
    """Blog page."""
    return render_template('blog.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=app.config['DEBUG'])
