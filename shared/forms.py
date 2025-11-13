"""
WebGarden Shared Forms
Common WTForms used across WebGarden sites.
"""

from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField, BooleanField, SelectField
from wtforms.validators import DataRequired, Email, Length, ValidationError, EqualTo
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
