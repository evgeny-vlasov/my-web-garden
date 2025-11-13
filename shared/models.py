"""
WebGarden Shared Database Models
Common models used across all WebGarden sites.
"""

from datetime import datetime
from flask_login import UserMixin
from shared.base_app import db, bcrypt


class User(UserMixin, db.Model):
    """
    User model for admin/editor access.
    Supports authentication and role-based access control.
    """
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default='editor')  # admin, editor
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    last_login = db.Column(db.DateTime)

    # Relationships
    blog_posts = db.relationship('BlogPost', backref='author', lazy='dynamic')
    uploaded_files = db.relationship('UploadedFile', backref='uploader', lazy='dynamic')

    def set_password(self, password):
        """Hash and set user password."""
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        """Verify password against hash."""
        return bcrypt.check_password_hash(self.password_hash, password)

    def update_last_login(self):
        """Update last login timestamp."""
        self.last_login = datetime.utcnow()
        db.session.commit()

    def is_admin(self):
        """Check if user has admin role."""
        return self.role == 'admin'

    def __repr__(self):
        return f'<User {self.username}>'


class ContactSubmission(db.Model):
    """
    Contact form submissions.
    Stores inquiries from website visitors.
    """
    __tablename__ = 'contact_submissions'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20))
    message = db.Column(db.Text, nullable=False)
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)
    status = db.Column(db.String(20), default='new')  # new, read, responded
    notes = db.Column(db.Text)

    def mark_as_read(self):
        """Mark submission as read."""
        if self.status == 'new':
            self.status = 'read'
            db.session.commit()

    def mark_as_responded(self):
        """Mark submission as responded."""
        self.status = 'responded'
        db.session.commit()

    def __repr__(self):
        return f'<ContactSubmission {self.name} - {self.submitted_at}>'


class BlogPost(db.Model):
    """
    Blog post model.
    Prepared for Sprint 2 - minimal implementation for Sprint 1.
    """
    __tablename__ = 'blog_posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(200), unique=True, nullable=False, index=True)
    content = db.Column(db.Text)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    published_at = db.Column(db.DateTime, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    visible = db.Column(db.Boolean, default=False)

    def publish(self):
        """Publish the blog post."""
        if not self.published_at:
            self.published_at = datetime.utcnow()
        self.visible = True
        db.session.commit()

    def unpublish(self):
        """Unpublish the blog post."""
        self.visible = False
        db.session.commit()

    def is_published(self):
        """Check if post is published and visible."""
        return self.visible and self.published_at is not None

    def __repr__(self):
        return f'<BlogPost {self.title}>'


class UploadedFile(db.Model):
    """
    Uploaded files metadata.
    Tracks all files uploaded through the system.
    """
    __tablename__ = 'uploaded_files'

    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    original_filename = db.Column(db.String(255))
    filepath = db.Column(db.String(500), nullable=False)
    file_size = db.Column(db.Integer)
    mime_type = db.Column(db.String(100))
    uploaded_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)

    def __repr__(self):
        return f'<UploadedFile {self.filename}>'
