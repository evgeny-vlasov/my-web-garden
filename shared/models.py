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


class Client(db.Model):
    """Minimal admin-only client record for the therapist CRM."""
    __tablename__ = 'clients'
    __table_args__ = (
        db.CheckConstraint(
            "preferred_contact_method IN ('email', 'phone', 'text', 'none')",
            name='ck_clients_preferred_contact_method',
        ),
        db.CheckConstraint(
            "language IN ('en', 'ru', 'other', 'unknown')",
            name='ck_clients_language',
        ),
        db.CheckConstraint(
            "status IN ('active', 'inactive', 'archived')",
            name='ck_clients_status',
        ),
    )

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120))
    phone = db.Column(db.String(20))
    preferred_contact_method = db.Column(
        db.String(20), default='none', server_default='none', nullable=False
    )
    language = db.Column(
        db.String(20), default='unknown', server_default='unknown', nullable=False
    )
    status = db.Column(
        db.String(20), default='active', server_default='active', nullable=False,
        index=True,
    )
    private_notes = db.Column(db.Text)
    created_at = db.Column(
        db.DateTime, default=datetime.utcnow, server_default=db.func.now(), nullable=False
    )
    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        server_default=db.func.now(),
        nullable=False,
    )

    contact_submissions = db.relationship(
        'ContactSubmission', back_populates='client', lazy='dynamic'
    )
    activities = db.relationship(
        'CRMActivity', back_populates='client', lazy='dynamic',
        cascade='all, delete-orphan',
    )

    def __repr__(self):
        return f'<Client id={self.id}>'


class ContactSubmission(db.Model):
    """
    Contact form submissions.
    Stores inquiries from website visitors.
    """
    __tablename__ = 'contact_submissions'
    __table_args__ = (
        db.CheckConstraint(
            "status IN ('new', 'contacted', 'booked', 'closed', 'spam')",
            name='ck_contact_submissions_status',
        ),
    )

    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(
        db.Integer,
        db.ForeignKey('clients.id', ondelete='SET NULL'),
        nullable=True,
        index=True,
    )
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20))
    message = db.Column(db.Text, nullable=False)
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)
    status = db.Column(
        db.String(20), default='new', server_default='new', nullable=False
    )
    notes = db.Column(db.Text)  # Internal admin notes; never shown publicly.
    is_spam = db.Column(db.Boolean, default=False, index=True)
    is_read = db.Column(
        db.Boolean, default=False, server_default=db.false(), nullable=False
    )
    follow_up_at = db.Column(db.DateTime, index=True)
    last_contacted_at = db.Column(db.DateTime)
    archived_at = db.Column(db.DateTime, index=True)
    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        server_default=db.func.now(),
        nullable=False,
    )

    client = db.relationship('Client', back_populates='contact_submissions')
    activities = db.relationship(
        'CRMActivity', back_populates='contact_submission', lazy='dynamic',
        cascade='all, delete-orphan',
    )

    def mark_as_read(self):
        """Mark submission as read."""
        self.is_read = True

    def mark_as_unread(self):
        """Mark submission as unread without changing its workflow status."""
        self.is_read = False

    def mark_as_spam(self):
        """Mark submission as spam."""
        self.is_spam = True
        self.status = 'spam'

    def mark_as_not_spam(self):
        """Mark submission as not spam."""
        self.is_spam = False
        if self.status == 'spam':
            self.status = 'new'

    def __repr__(self):
        return f'<ContactSubmission id={self.id}>'


class CRMActivity(db.Model):
    """Private office/admin activity attached to one CRM record."""
    __tablename__ = 'crm_activities'
    __table_args__ = (
        db.CheckConstraint(
            '(client_id IS NOT NULL) <> (contact_submission_id IS NOT NULL)',
            name='ck_crm_activities_exactly_one_parent',
        ),
        db.CheckConstraint(
            "activity_type IN ('note', 'call', 'email', 'voicemail', "
            "'appointment', 'follow_up', 'other')",
            name='ck_crm_activities_type',
        ),
        db.CheckConstraint(
            "length(trim(body)) > 0",
            name='ck_crm_activities_body_not_blank',
        ),
        db.CheckConstraint(
            "completed_at IS NULL OR due_at IS NOT NULL OR activity_type = 'follow_up'",
            name='ck_crm_activities_completion_relevant',
        ),
    )

    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(
        db.Integer, db.ForeignKey('clients.id', ondelete='CASCADE'), index=True
    )
    contact_submission_id = db.Column(
        db.Integer,
        db.ForeignKey('contact_submissions.id', ondelete='CASCADE'),
        index=True,
    )
    actor_user_id = db.Column(
        db.Integer, db.ForeignKey('users.id', ondelete='SET NULL'), index=True
    )
    activity_type = db.Column(db.String(20), nullable=False)
    body = db.Column(db.Text, nullable=False)
    due_at = db.Column(db.DateTime, index=True)
    completed_at = db.Column(db.DateTime)
    created_at = db.Column(
        db.DateTime, default=datetime.utcnow, server_default=db.func.now(), nullable=False
    )
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow,
        server_default=db.func.now(), nullable=False,
    )

    client = db.relationship('Client', back_populates='activities')
    contact_submission = db.relationship(
        'ContactSubmission', back_populates='activities'
    )
    actor = db.relationship('User')

    def __repr__(self):
        return f'<CRMActivity id={self.id} type={self.activity_type}>'


class SpamBlocklist(db.Model):
    """
    Blocklist for spam names and emails.
    Prevents specific names or email addresses from submitting contact forms.
    """
    __tablename__ = 'spam_blocklist'

    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.String(255), nullable=False, unique=True, index=True)
    type = db.Column(db.String(20), nullable=False)  # 'name' or 'email'
    reason = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_by = db.Column(db.String(100))

    def __repr__(self):
        return f'<SpamBlocklist {self.type}:{self.value}>'


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
