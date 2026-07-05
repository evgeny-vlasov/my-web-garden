"""
WebGarden CLI Commands
Flask CLI commands for user and site management.
"""

import click
from flask import current_app
from shared.base_app import db
from shared.models import User
from getpass import getpass


def register_cli_commands(app):
    """Register CLI commands with the Flask app."""

    @app.cli.command('create-admin')
    @click.option('--username', prompt=True, help='Admin username')
    @click.option('--email', prompt=True, help='Admin email address')
    @click.option('--password', prompt=True, hide_input=True, confirmation_prompt=True, help='Admin password')
    def create_admin_user(username, email, password):
        """Create a new admin user."""
        try:
            # Check if user already exists
            if User.query.filter_by(username=username).first():
                click.echo(click.style(f'Error: User "{username}" already exists.', fg='red'))
                return

            if User.query.filter_by(email=email).first():
                click.echo(click.style(f'Error: Email "{email}" is already registered.', fg='red'))
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

            click.echo(click.style(f'✓ Admin user "{username}" created successfully!', fg='green'))
            click.echo(f'Email: {email}')
            click.echo(f'Role: admin')

        except Exception as e:
            db.session.rollback()
            click.echo(click.style(f'Error creating admin user: {str(e)}', fg='red'))

    @app.cli.command('reset-password')
    @click.option('--username', prompt=True, help='Username to reset password for')
    @click.option('--password', prompt=True, hide_input=True, confirmation_prompt=True, help='New password')
    def reset_user_password(username, password):
        """Reset a user's password."""
        try:
            user = User.query.filter_by(username=username).first()

            if not user:
                click.echo(click.style(f'Error: User "{username}" not found.', fg='red'))
                return

            user.set_password(password)
            db.session.commit()

            click.echo(click.style(f'✓ Password reset successfully for user "{username}".', fg='green'))

        except Exception as e:
            db.session.rollback()
            click.echo(click.style(f'Error resetting password: {str(e)}', fg='red'))

    @app.cli.command('list-users')
    def list_all_users():
        """List all users in the system."""
        try:
            users = User.query.order_by(User.created_at.desc()).all()

            if not users:
                click.echo('No users found.')
                return

            click.echo('\nUsers in the system:')
            click.echo('-' * 80)
            click.echo(f'{"ID":<5} {"Username":<20} {"Email":<30} {"Role":<10} {"Created"}')
            click.echo('-' * 80)

            for user in users:
                created = user.created_at.strftime('%Y-%m-%d') if user.created_at else 'N/A'
                click.echo(f'{user.id:<5} {user.username:<20} {user.email:<30} {user.role:<10} {created}')

            click.echo('-' * 80)
            click.echo(f'Total users: {len(users)}')

        except Exception as e:
            click.echo(click.style(f'Error listing users: {str(e)}', fg='red'))

    @app.cli.command('delete-user')
    @click.option('--username', prompt=True, help='Username to delete')
    @click.confirmation_option(prompt='Are you sure you want to delete this user?')
    def delete_user_account(username):
        """Delete a user account."""
        try:
            user = User.query.filter_by(username=username).first()

            if not user:
                click.echo(click.style(f'Error: User "{username}" not found.', fg='red'))
                return

            # Store info before deletion
            user_email = user.email
            user_role = user.role

            db.session.delete(user)
            db.session.commit()

            click.echo(click.style(f'✓ User "{username}" ({user_email}, {user_role}) has been deleted.', fg='green'))

        except Exception as e:
            db.session.rollback()
            click.echo(click.style(f'Error deleting user: {str(e)}', fg='red'))

    @app.cli.command('promote-user')
    @click.option('--username', prompt=True, help='Username to promote to admin')
    def promote_to_admin(username):
        """Promote a user to admin role."""
        try:
            user = User.query.filter_by(username=username).first()

            if not user:
                click.echo(click.style(f'Error: User "{username}" not found.', fg='red'))
                return

            if user.is_admin():
                click.echo(click.style(f'User "{username}" is already an admin.', fg='yellow'))
                return

            user.role = 'admin'
            db.session.commit()

            click.echo(click.style(f'✓ User "{username}" promoted to admin.', fg='green'))

        except Exception as e:
            db.session.rollback()
            click.echo(click.style(f'Error promoting user: {str(e)}', fg='red'))

    @app.cli.command('demote-user')
    @click.option('--username', prompt=True, help='Username to demote from admin')
    def demote_from_admin(username):
        """Demote a user from admin to editor role."""
        try:
            user = User.query.filter_by(username=username).first()

            if not user:
                click.echo(click.style(f'Error: User "{username}" not found.', fg='red'))
                return

            if not user.is_admin():
                click.echo(click.style(f'User "{username}" is not an admin.', fg='yellow'))
                return

            user.role = 'editor'
            db.session.commit()

            click.echo(click.style(f'✓ User "{username}" demoted to editor.', fg='green'))

        except Exception as e:
            db.session.rollback()
            click.echo(click.style(f'Error demoting user: {str(e)}', fg='red'))

    @app.cli.command('create-test-post')
    def create_test_post():
        """Create a test blog post for development."""
        from shared.models import BlogPost
        from slugify import slugify

        try:
            # Check if user exists
            user = User.query.first()
            if not user:
                click.echo(click.style('Error: No users found. Create an admin user first.', fg='red'))
                return

            # Create test post
            post = BlogPost(
                title='Welcome to Our Blog',
                slug=slugify('Welcome to Our Blog'),
                content='<p>This is a test blog post. It demonstrates the blog functionality.</p><p>You can edit or delete this post from the admin panel.</p>',
                author_id=user.id,
                visible=True
            )
            post.publish()

            db.session.add(post)
            db.session.commit()

            click.echo(click.style('✓ Test blog post created successfully!', fg='green'))
            click.echo(f'Title: {post.title}')
            click.echo(f'Slug: {post.slug}')
            click.echo(f'URL: /post/{post.slug}')

        except Exception as e:
            db.session.rollback()
            click.echo(click.style(f'Error creating test post: {str(e)}', fg='red'))
