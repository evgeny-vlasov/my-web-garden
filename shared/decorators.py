"""
WebGarden Custom Decorators
Custom Flask route decorators for authorization and validation.
"""

from functools import wraps
from flask import redirect, url_for, flash, request, abort
from flask_login import current_user


def login_required(f):
    """
    Require user to be logged in.
    Redirects to admin login page if not authenticated.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('admin_login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function


def admin_required(f):
    """
    Require user to be logged in and have admin role.
    Returns 403 if user doesn't have admin permissions.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('admin_login', next=request.url))

        if not current_user.is_admin():
            flash('You do not have permission to access this page.', 'error')
            abort(403)

        return f(*args, **kwargs)
    return decorated_function


def anonymous_required(f):
    """
    Require user to NOT be logged in.
    Redirects to admin dashboard if already authenticated.
    Useful for login/register pages.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.is_authenticated:
            return redirect(url_for('admin_dashboard'))
        return f(*args, **kwargs)
    return decorated_function
