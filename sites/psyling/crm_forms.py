"""CSRF-protected forms for the small admin contact CRM."""

from flask_wtf import FlaskForm
from wtforms import (
    DateTimeLocalField, EmailField, HiddenField, SelectField, StringField,
    TextAreaField,
)
from wtforms.validators import DataRequired, Length, Optional, Regexp, ValidationError


CONTACT_STATUSES = ("new", "contacted", "booked", "closed", "spam")
STATUS_CHOICES = tuple((status, status.title()) for status in CONTACT_STATUSES)
ACTIVITY_TYPE_CHOICES = (
    ("note", "Note"),
    ("call", "Call"),
    ("email", "Email"),
    ("voicemail", "Voicemail"),
    ("appointment", "Appointment"),
    ("follow_up", "Follow-up"),
    ("other", "Other"),
)


class ContactCRMForm(FlaskForm):
    status = SelectField("Status", choices=STATUS_CHOICES, validate_choice=True)
    notes = TextAreaField(
        "Internal notes",
        validators=[Optional(), Length(max=10000)],
    )
    follow_up_at = DateTimeLocalField(
        "Follow-up date and time",
        format="%Y-%m-%dT%H:%M",
        validators=[Optional()],
    )


class ContactActionForm(FlaskForm):
    """CSRF-only form used for read, spam, archive, and contact actions."""


class ContactReplyForm(FlaskForm):
    subject = StringField(
        "Subject",
        validators=[DataRequired(), Length(max=200)],
    )
    body = TextAreaField(
        "Message",
        validators=[DataRequired(), Length(max=10000)],
    )
    idempotency_key = HiddenField(
        validators=[
            DataRequired(),
            Length(min=32, max=64),
            Regexp(r'^[A-Za-z0-9_-]+$'),
        ]
    )


class ActivityForm(FlaskForm):
    activity_type = SelectField(
        "Activity type", choices=ACTIVITY_TYPE_CHOICES, validate_choice=True
    )
    body = TextAreaField(
        "Private activity note", validators=[DataRequired(), Length(max=10000)]
    )
    due_at = DateTimeLocalField(
        "Follow-up date and time",
        format="%Y-%m-%dT%H:%M",
        validators=[Optional()],
    )


class ActivityCompleteForm(FlaskForm):
    """CSRF-only form for completing an open follow-up."""


CLIENT_STATUS_CHOICES = (
    ("active", "Active"),
    ("inactive", "Inactive"),
    ("archived", "Archived"),
)
PREFERRED_CONTACT_CHOICES = (
    ("none", "Not specified"),
    ("email", "Email"),
    ("phone", "Phone call"),
    ("text", "Text message"),
)
LANGUAGE_CHOICES = (
    ("unknown", "Not specified"),
    ("en", "English"),
    ("ru", "Russian"),
    ("other", "Other"),
)


class ClientForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(), Length(max=100)])
    email = EmailField("Email", validators=[Optional(), Length(max=120)])
    phone = StringField("Phone", validators=[Optional(), Length(max=20)])
    preferred_contact_method = SelectField(
        "Preferred contact method",
        choices=PREFERRED_CONTACT_CHOICES,
        validate_choice=True,
    )
    language = SelectField("Language", choices=LANGUAGE_CHOICES, validate_choice=True)
    status = SelectField("Status", choices=CLIENT_STATUS_CHOICES, validate_choice=True)
    private_notes = TextAreaField(
        "Private notes", validators=[Optional(), Length(max=10000)]
    )

    def validate_preferred_contact_method(self, field):
        if field.data == "email" and not (self.email.data or "").strip():
            raise ValidationError("An email address is required for email contact.")
        if field.data in {"phone", "text"} and not (self.phone.data or "").strip():
            raise ValidationError("A phone number is required for phone or text contact.")
