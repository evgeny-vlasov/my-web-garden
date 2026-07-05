"""CSRF-protected forms for private client messaging."""

from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, TextAreaField
from wtforms.validators import DataRequired, Length, Optional


class ChatRoomCreateForm(FlaskForm):
    client_id = SelectField("Client", coerce=int, validators=[DataRequired()])
    title = StringField("Room title", validators=[Optional(), Length(max=200)])


class ChatMessageForm(FlaskForm):
    body = TextAreaField(
        "Message", validators=[DataRequired(), Length(min=1, max=10000)]
    )


class ChatRoomActionForm(FlaskForm):
    """CSRF-only form for room state and invite actions."""


class ClientRoomAccessForm(FlaskForm):
    token = StringField(
        "Private access token", validators=[DataRequired(), Length(min=32, max=200)]
    )
