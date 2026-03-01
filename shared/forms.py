"""
WebGarden Shared Forms
Common WTForms used across WebGarden sites.
"""

from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField, BooleanField, SelectField
from wtforms.fields import DateField
from wtforms.validators import DataRequired, Email, Length, ValidationError, EqualTo, Optional
from shared.models import User


class ContactForm(FlaskForm):
    """
    Contact form for visitor inquiries.
    Used on contact pages across all sites.
    """
    name = StringField(
        'Name',
        validators=[
            DataRequired(message='Please enter your name.'),
            Length(min=2, max=100, message='Name must be between 2 and 100 characters.')
        ],
        render_kw={'placeholder': 'Your Name', 'class': 'form-control'}
    )

    email = StringField(
        'Email',
        validators=[
            DataRequired(message='Please enter your email address.'),
            Email(message='Please enter a valid email address.'),
            Length(max=120)
        ],
        render_kw={'placeholder': 'your.email@example.com', 'class': 'form-control'}
    )

    phone = StringField(
        'Phone',
        validators=[
            Length(max=20, message='Phone number too long.')
        ],
        render_kw={'placeholder': 'Optional phone number', 'class': 'form-control'}
    )

    message = TextAreaField(
        'Message',
        validators=[
            DataRequired(message='Please enter your message.'),
            Length(min=10, max=5000, message='Message must be between 10 and 5000 characters.')
        ],
        render_kw={
            'placeholder': 'How can we help you?',
            'class': 'form-control',
            'rows': 5
        }
    )


class BookingRequestForm(FlaskForm):
    """
    Booking request form for appointment scheduling.
    Used on schedule page for manual booking requests.
    """
    name = StringField(
        'Name',
        validators=[
            DataRequired(message='Please enter your name.'),
            Length(min=2, max=100, message='Name must be between 2 and 100 characters.')
        ],
        render_kw={'placeholder': 'Your Name', 'class': 'form-control'}
    )

    email = StringField(
        'Email',
        validators=[
            DataRequired(message='Please enter your email address.'),
            Email(message='Please enter a valid email address.'),
            Length(max=120)
        ],
        render_kw={'placeholder': 'your.email@example.com', 'class': 'form-control'}
    )

    phone = StringField(
        'Phone',
        validators=[
            Optional(),
            Length(max=20, message='Phone number too long.')
        ],
        render_kw={'placeholder': '(647) 360-8980', 'class': 'form-control'}
    )

    preferred_date = DateField(
        'Preferred Date',
        validators=[DataRequired(message='Please select a preferred date.')],
        render_kw={'class': 'form-control'}
    )

    preferred_time = SelectField(
        'Preferred Time',
        choices=[
            ('', 'Select a time...'),
            ('09:00', '9:00 AM'),
            ('10:00', '10:00 AM'),
            ('11:00', '11:00 AM'),
            ('13:00', '1:00 PM'),
            ('14:00', '2:00 PM'),
            ('15:00', '3:00 PM'),
            ('16:00', '4:00 PM'),
            ('17:00', '5:00 PM')
        ],
        validators=[DataRequired(message='Please select a preferred time.')],
        render_kw={'class': 'form-control'}
    )

    alternative_date = DateField(
        'Alternative Date',
        validators=[Optional()],
        render_kw={'class': 'form-control'}
    )

    alternative_time = SelectField(
        'Alternative Time',
        choices=[
            ('', 'Select a time...'),
            ('09:00', '9:00 AM'),
            ('10:00', '10:00 AM'),
            ('11:00', '11:00 AM'),
            ('13:00', '1:00 PM'),
            ('14:00', '2:00 PM'),
            ('15:00', '3:00 PM'),
            ('16:00', '4:00 PM'),
            ('17:00', '5:00 PM')
        ],
        validators=[Optional()],
        render_kw={'class': 'form-control'}
    )

    reason = TextAreaField(
        'Reason for Appointment',
        validators=[
            Optional(),
            Length(max=1000, message='Reason must be less than 1000 characters.')
        ],
        render_kw={
            'placeholder': 'Brief description of what you\'d like to discuss (optional)',
            'class': 'form-control',
            'rows': 3
        }
    )

    notes = TextAreaField(
        'Additional Notes',
        validators=[
            Optional(),
            Length(max=1000, message='Notes must be less than 1000 characters.')
        ],
        render_kw={
            'placeholder': 'Any other information I should know (optional)',
            'class': 'form-control',
            'rows': 2
        }
    )


class LoginForm(FlaskForm):
    """
    Admin/editor login form.
    Prepared for Sprint 2.
    """
    username = StringField(
        'Username',
        validators=[
            DataRequired(message='Username is required.'),
            Length(min=3, max=80)
        ],
        render_kw={'placeholder': 'Username', 'class': 'form-control'}
    )

    password = PasswordField(
        'Password',
        validators=[
            DataRequired(message='Password is required.')
        ],
        render_kw={'placeholder': 'Password', 'class': 'form-control', 'type': 'password'}
    )

    remember_me = BooleanField(
        'Remember Me',
        render_kw={'class': 'form-check-input'}
    )


class UserForm(FlaskForm):
    """
    User creation/edit form for admin panel.
    Prepared for Sprint 2.
    """
    username = StringField(
        'Username',
        validators=[
            DataRequired(message='Username is required.'),
            Length(min=3, max=80, message='Username must be between 3 and 80 characters.')
        ],
        render_kw={'class': 'form-control'}
    )

    email = StringField(
        'Email',
        validators=[
            DataRequired(message='Email is required.'),
            Email(message='Please enter a valid email address.'),
            Length(max=120)
        ],
        render_kw={'class': 'form-control'}
    )

    password = PasswordField(
        'Password',
        validators=[
            Length(min=8, message='Password must be at least 8 characters.')
        ],
        render_kw={'class': 'form-control', 'type': 'password'}
    )

    password_confirm = PasswordField(
        'Confirm Password',
        validators=[
            EqualTo('password', message='Passwords must match.')
        ],
        render_kw={'class': 'form-control', 'type': 'password'}
    )

    role = SelectField(
        'Role',
        choices=[('editor', 'Editor'), ('admin', 'Admin')],
        validators=[DataRequired()],
        render_kw={'class': 'form-select'}
    )

    def validate_username(self, username):
        """Validate username is unique."""
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already exists. Please choose a different one.')

    def validate_email(self, email):
        """Validate email is unique."""
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already registered. Please use a different email.')


class BlogPostForm(FlaskForm):
    """
    Blog post creation/edit form.
    Prepared for Sprint 2.
    """
    title = StringField(
        'Title',
        validators=[
            DataRequired(message='Title is required.'),
            Length(min=5, max=200, message='Title must be between 5 and 200 characters.')
        ],
        render_kw={'class': 'form-control'}
    )

    slug = StringField(
        'URL Slug',
        validators=[
            Length(max=200)
        ],
        render_kw={
            'class': 'form-control',
            'placeholder': 'url-friendly-slug'
        }
    )

    content = TextAreaField(
        'Content',
        validators=[DataRequired(message='Content is required.')],
        render_kw={'class': 'form-control', 'rows': 15}
    )

    visible = BooleanField(
        'Published',
        render_kw={'class': 'form-check-input'}
    )
