"""CSRF-protected forms for the small admin contact CRM."""

from flask_wtf import FlaskForm
from wtforms import DateTimeLocalField, SelectField, TextAreaField
from wtforms.validators import Length, Optional


CONTACT_STATUSES = ("new", "contacted", "booked", "closed", "spam")
STATUS_CHOICES = tuple((status, status.title()) for status in CONTACT_STATUSES)


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

