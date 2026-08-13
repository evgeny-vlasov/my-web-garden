"""Privacy-conscious email construction for admin contact replies."""

from flask import current_app
from flask_mail import Message
from markupsafe import escape

from shared.base_app import mail


def _reply_html(body):
    """Turn plain text into a minimal escaped HTML alternative."""
    normalized = body.replace('\r\n', '\n').replace('\r', '\n')
    escaped_body = str(escape(normalized)).replace('\n', '<br>\n')
    return (
        '<!doctype html><html><body>'
        '<div style="font-family:Arial,sans-serif;line-height:1.6;color:#222">'
        f'{escaped_body}'
        '</div></body></html>'
    )


def send_contact_reply_email(recipient, subject, body):
    """Send one admin reply without logging private message or address data."""
    sender = current_app.config.get('MAIL_DEFAULT_SENDER')
    reply_to = current_app.config.get('ADMIN_EMAIL')
    if not sender or not reply_to:
        raise RuntimeError('Psyling reply email configuration is incomplete')

    message = Message(
        subject=subject,
        recipients=[recipient],
        sender=sender,
        reply_to=reply_to,
        body=body,
        html=_reply_html(body),
    )
    mail.send(message)
