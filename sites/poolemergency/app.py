"""
Flask Application
"""

import os
import sys
from datetime import datetime

# Add parent directories to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
sys.path.insert(0, os.path.dirname(__file__))

from flask import render_template
from dotenv import load_dotenv

load_dotenv()

# Import shared modules
from shared.base_app import create_base_app, db, login_manager
from shared.models import User
from config import config
from cli import register_cli_commands

# Create Flask application
config_name = os.getenv('FLASK_ENV', 'production')
app = create_base_app('poolemergency', config[config_name])

# Register CLI commands
register_cli_commands(app)

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

@app.route('/contact')
def contact():
    """Contact page."""
    return render_template('contact.html')

@app.route('/blog')
def blog():
    """Blog page."""
    return render_template('blog.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=app.config['DEBUG'])

