"""
WebGarden Authentication Helpers
User authentication and session management utilities.
"""

from functools import wraps
from flask import redirect, url_for, flash, request
from flask_login import current_user
from shared.base_app import login_manager
from shared.models import User


@login_manager.user_loader
def load_user(user_id):
    """
    Load user by ID for Flask-Login.

    Args:
        user_id: User ID to load

    Returns:
        User object or None
    """
    return User.query.get(int(user_id))


def admin_required(f):
    """
    Decorator to require admin role for a route.

    Usage:
        @app.route('/admin/sensitive')
        @admin_required
        def sensitive_page():
            return 'Admin only'
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('admin_login', next=request.url))

        if not current_user.is_admin():
            flash('You do not have permission to access this page.', 'error')
            return redirect(url_for('index'))

        return f(*args, **kwargs)
    return decorated_function


def login_required_custom(f):
    """
    Custom login required decorator with redirect to admin login.

    Usage:
        @app.route('/admin/page')
        @login_required_custom
        def admin_page():
            return 'Logged in users only'
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('admin_login', next=request.url))

        return f(*args, **kwargs)
    return decorated_function


def get_redirect_target():
    """
    Get the redirect target from request args or referrer.

    Returns:
        URL string or None
    """
    for target in request.args.get('next'), request.referrer:
        if target:
            return target
    return None


def is_safe_url(target):
    """
    Check if a redirect URL is safe (same domain).

    Args:
        target: URL to check

    Returns:
        True if safe, False otherwise
    """
    from urllib.parse import urlparse, urljoin
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc
