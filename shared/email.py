"""
WebGarden Email Utilities
Email sending functionality with Mailgun integration.
"""

from flask import current_app, render_template
from flask_mail import Message
from shared.base_app import mail
import logging

logger = logging.getLogger(__name__)


def send_email(subject, recipients, text_body=None, html_body=None, sender=None):
    """
    Send an email via Flask-Mail (Mailgun).

    Args:
        subject: Email subject line
        recipients: List of recipient email addresses
        text_body: Plain text email body (optional)
        html_body: HTML email body (optional)
        sender: Sender email address (uses default if not provided)

    Returns:
        True if email sent successfully, False otherwise
    """
    try:
        if sender is None:
            sender = current_app.config['MAIL_DEFAULT_SENDER']

        msg = Message(
            subject=subject,
            recipients=recipients if isinstance(recipients, list) else [recipients],
            sender=sender
        )

        if text_body:
            msg.body = text_body
        if html_body:
            msg.html = html_body

        mail.send(msg)
        logger.info(f'Email sent: {subject} to {recipients}')
        return True

    except Exception as e:
        logger.error(f'Failed to send email: {str(e)}')
        return False


def send_contact_notification(contact_submission):
    """
    Send notification email when a contact form is submitted.

    Args:
        contact_submission: ContactSubmission model instance

    Returns:
        True if email sent successfully, False otherwise
    """
    site_name = current_app.config['SITE_NAME']
    admin_email = current_app.config.get('ADMIN_EMAIL', current_app.config['MAIL_DEFAULT_SENDER'])

    subject = f'New Contact Form Submission - {site_name}'

    text_body = f"""
New contact form submission received:

Name: {contact_submission.name}
Email: {contact_submission.email}
Phone: {contact_submission.phone or 'Not provided'}

Message:
{contact_submission.message}

Submitted at: {contact_submission.submitted_at.strftime('%Y-%m-%d %H:%M:%S UTC')}
    """

    html_body = f"""
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background-color: #007bff; color: white; padding: 20px; text-align: center; }}
            .content {{ background-color: #f8f9fa; padding: 20px; margin-top: 20px; }}
            .field {{ margin-bottom: 15px; }}
            .label {{ font-weight: bold; color: #555; }}
            .value {{ margin-top: 5px; }}
            .message {{ background-color: white; padding: 15px; border-left: 4px solid #007bff; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h2>New Contact Form Submission</h2>
            </div>
            <div class="content">
                <div class="field">
                    <div class="label">Name:</div>
                    <div class="value">{contact_submission.name}</div>
                </div>
                <div class="field">
                    <div class="label">Email:</div>
                    <div class="value"><a href="mailto:{contact_submission.email}">{contact_submission.email}</a></div>
                </div>
                <div class="field">
                    <div class="label">Phone:</div>
                    <div class="value">{contact_submission.phone or 'Not provided'}</div>
                </div>
                <div class="field">
                    <div class="label">Message:</div>
                    <div class="message">{contact_submission.message}</div>
                </div>
                <div class="field">
                    <div class="label">Submitted:</div>
                    <div class="value">{contact_submission.submitted_at.strftime('%Y-%m-%d %H:%M:%S UTC')}</div>
                </div>
            </div>
        </div>
    </body>
    </html>
    """

    return send_email(
        subject=subject,
        recipients=[admin_email],
        text_body=text_body,
        html_body=html_body
    )


def send_contact_confirmation(contact_submission):
    """
    Send confirmation email to the person who submitted the contact form.

    Args:
        contact_submission: ContactSubmission model instance

    Returns:
        True if email sent successfully, False otherwise
    """
    site_name = current_app.config['SITE_NAME']

    subject = f'Thank you for contacting {site_name}'

    text_body = f"""
Dear {contact_submission.name},

Thank you for reaching out to us. We have received your message and will respond as soon as possible.

Your message:
{contact_submission.message}

Best regards,
{site_name} Team
    """

    html_body = f"""
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background-color: #28a745; color: white; padding: 20px; text-align: center; }}
            .content {{ padding: 20px; }}
            .message {{ background-color: #f8f9fa; padding: 15px; margin: 20px 0; border-left: 4px solid #28a745; }}
            .footer {{ text-align: center; color: #777; margin-top: 30px; font-size: 0.9em; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h2>Thank You for Contacting Us</h2>
            </div>
            <div class="content">
                <p>Dear {contact_submission.name},</p>
                <p>Thank you for reaching out to us. We have received your message and will respond as soon as possible.</p>
                <div class="message">
                    <strong>Your message:</strong><br>
                    {contact_submission.message}
                </div>
                <p>Best regards,<br>{site_name} Team</p>
            </div>
            <div class="footer">
                <p>This is an automated confirmation email.</p>
            </div>
        </div>
    </body>
    </html>
    """

    return send_email(
        subject=subject,
        recipients=[contact_submission.email],
        text_body=text_body,
        html_body=html_body
    )
