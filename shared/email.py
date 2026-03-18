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
    Includes Reply-To header so therapist can click Reply to respond directly.

    Args:
        contact_submission: ContactSubmission model instance

    Returns:
        True if email sent successfully, False otherwise
    """
    site_name = current_app.config['SITE_NAME']
    admin_email = current_app.config.get('ADMIN_EMAIL', current_app.config['MAIL_DEFAULT_SENDER'])
    site_domain = current_app.config.get('SITE_DOMAIN', 'localhost')

    subject = f'New Contact Form Submission from {contact_submission.name}'

    text_body = f"""
New contact form submission from {site_domain}:

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

CLIENT INFORMATION:
Name:     {contact_submission.name}
Email:    {contact_submission.email}
Phone:    {contact_submission.phone or 'Not provided'}

MESSAGE:
{contact_submission.message}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

NEXT STEPS:
• Click "Reply" in your email to respond directly to the client
• Client will receive your response at: {contact_submission.email}

View all submissions: https://{site_domain}/admin/dashboard

Timestamp: {contact_submission.submitted_at.strftime('%Y-%m-%d %H:%M:%S %Z')}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{site_name} - Contact Form Automated Notification
    """

    html_body = f"""
    <html>
    <head>
        <style>
            body {{ font-family: 'Segoe UI', Arial, sans-serif; line-height: 1.6; color: #333; background-color: #f5f5f5; }}
            .container {{ max-width: 650px; margin: 20px auto; background-color: white; border-radius: 8px; overflow: hidden; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }}
            .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px 20px; text-align: center; }}
            .header h2 {{ margin: 0; font-size: 24px; font-weight: 600; }}
            .content {{ padding: 30px; }}
            .info-section {{ background-color: #f8f9fa; border-radius: 6px; padding: 20px; margin-bottom: 20px; }}
            .field {{ margin-bottom: 15px; padding-bottom: 15px; border-bottom: 1px solid #e0e0e0; }}
            .field:last-child {{ border-bottom: none; margin-bottom: 0; padding-bottom: 0; }}
            .label {{ font-weight: 600; color: #667eea; font-size: 12px; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 5px; }}
            .value {{ font-size: 15px; color: #333; }}
            .value a {{ color: #667eea; text-decoration: none; }}
            .value a:hover {{ text-decoration: underline; }}
            .message-box {{ background-color: white; padding: 20px; border-left: 4px solid #667eea; border-radius: 4px; margin-top: 10px; white-space: pre-wrap; word-wrap: break-word; }}
            .action-section {{ background-color: #e8f4f8; border-radius: 6px; padding: 20px; margin: 20px 0; }}
            .action-section h3 {{ margin: 0 0 15px 0; color: #2c5aa0; font-size: 16px; }}
            .action-section ul {{ margin: 0; padding-left: 20px; }}
            .action-section li {{ margin-bottom: 8px; color: #555; }}
            .footer {{ text-align: center; padding: 20px; background-color: #f8f9fa; color: #777; font-size: 13px; border-top: 1px solid #e0e0e0; }}
            .admin-link {{ display: inline-block; margin-top: 10px; padding: 10px 20px; background-color: #667eea; color: white; text-decoration: none; border-radius: 4px; }}
            .admin-link:hover {{ background-color: #5568d3; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h2>🔔 New Contact Form Submission</h2>
            </div>
            <div class="content">
                <div class="info-section">
                    <div class="field">
                        <div class="label">Client Name</div>
                        <div class="value">{contact_submission.name}</div>
                    </div>
                    <div class="field">
                        <div class="label">Email Address</div>
                        <div class="value"><a href="mailto:{contact_submission.email}">{contact_submission.email}</a></div>
                    </div>
                    <div class="field">
                        <div class="label">Phone Number</div>
                        <div class="value">{contact_submission.phone or 'Not provided'}</div>
                    </div>
                    <div class="field">
                        <div class="label">Submitted</div>
                        <div class="value">{contact_submission.submitted_at.strftime('%B %d, %Y at %I:%M %p %Z')}</div>
                    </div>
                </div>

                <div class="field">
                    <div class="label">Client Message</div>
                    <div class="message-box">{contact_submission.message}</div>
                </div>

                <div class="action-section">
                    <h3>📋 Next Steps</h3>
                    <ul>
                        <li><strong>Click "Reply"</strong> in your email client to respond directly to {contact_submission.name}</li>
                        <li>Your response will go to: <strong>{contact_submission.email}</strong></li>
                        <li>Typical response time: Within 48 hours</li>
                    </ul>
                </div>

                <div style="text-align: center; margin-top: 25px;">
                    <a href="https://{site_domain}/admin/dashboard" class="admin-link">View Admin Dashboard</a>
                </div>
            </div>
            <div class="footer">
                <p>Automated notification from {site_name}</p>
                <p style="font-size: 11px; color: #999; margin-top: 10px;">This email was sent from {site_domain}</p>
            </div>
        </div>
    </body>
    </html>
    """

    try:
        # Create message with Reply-To header
        msg = Message(
            subject=subject,
            recipients=[admin_email],
            sender=current_app.config['MAIL_DEFAULT_SENDER'],
            reply_to=contact_submission.email  # Critical: allows therapist to click Reply
        )

        msg.body = text_body
        msg.html = html_body

        mail.send(msg)
        logger.info(f'✅ Admin notification sent for submission from {contact_submission.email}')
        return True

    except Exception as e:
        logger.error(f'❌ Failed to send admin notification: {str(e)}')
        logger.error(f'   Submission from {contact_submission.email} saved but email not delivered')
        return False


def send_contact_confirmation(contact_submission):
    """
    Send confirmation email to the person who submitted the contact form.
    Includes emergency contact information for mental health crises.

    Args:
        contact_submission: ContactSubmission model instance

    Returns:
        True if email sent successfully, False otherwise
    """
    site_name = current_app.config['SITE_NAME']

    subject = 'Thank you for contacting Psyling'

    text_body = f"""
Dear {contact_submission.name},

Thank you for reaching out to Psyling. I have received your message and will respond within 48 hours.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
IMPORTANT: If you are experiencing a mental health emergency, please contact:

• Emergency Services: 911
• Toronto Distress Centre: 416-408-HELP (4357)
• Crisis Services Canada: 1-833-456-4566
• Good2Talk (post-secondary students): 1-866-925-5454

These services are available 24/7 for immediate support.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

I look forward to speaking with you soon and discussing how I can support your mental health journey.

Best regards,

Dr. Valery Belyanin
Registered Psychotherapist
College of Registered Psychotherapists of Ontario (CRPO)

Email: psyling@gmail.com
Phone: (647) 360-8980
Web: https://psyling.com

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
This is an automated confirmation. Please do not reply to this email.
To reach me directly, use: psyling@gmail.com
    """

    html_body = f"""
    <html>
    <head>
        <style>
            body {{ font-family: 'Segoe UI', Arial, sans-serif; line-height: 1.6; color: #333; background-color: #f5f5f5; }}
            .container {{ max-width: 650px; margin: 20px auto; background-color: white; border-radius: 8px; overflow: hidden; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }}
            .header {{ background: linear-gradient(135deg, #28a745 0%, #20c997 100%); color: white; padding: 30px 20px; text-align: center; }}
            .header h2 {{ margin: 0; font-size: 24px; font-weight: 600; }}
            .content {{ padding: 30px; }}
            .greeting {{ font-size: 16px; color: #333; margin-bottom: 20px; }}
            .emergency-box {{ background-color: #fff3cd; border: 2px solid #ffc107; border-radius: 6px; padding: 20px; margin: 25px 0; }}
            .emergency-box h3 {{ margin: 0 0 15px 0; color: #856404; font-size: 16px; font-weight: 600; }}
            .emergency-box .crisis-line {{ margin: 10px 0; padding: 10px; background-color: white; border-radius: 4px; }}
            .emergency-box .crisis-line strong {{ color: #d39e00; }}
            .emergency-box p {{ margin: 10px 0; color: #856404; }}
            .message-note {{ background-color: #f8f9fa; padding: 15px; border-radius: 6px; margin: 20px 0; font-size: 14px; color: #666; }}
            .signature {{ margin-top: 30px; padding: 20px; background-color: #f8f9fa; border-radius: 6px; }}
            .signature .name {{ font-size: 16px; font-weight: 600; color: #333; margin-bottom: 5px; }}
            .signature .title {{ color: #667eea; font-size: 14px; margin-bottom: 3px; }}
            .signature .credential {{ color: #777; font-size: 13px; margin-bottom: 15px; }}
            .signature .contact {{ font-size: 14px; color: #555; margin: 5px 0; }}
            .signature .contact a {{ color: #667eea; text-decoration: none; }}
            .signature .contact a:hover {{ text-decoration: underline; }}
            .footer {{ text-align: center; padding: 20px; background-color: #f8f9fa; color: #777; font-size: 13px; border-top: 1px solid #e0e0e0; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h2>✓ Message Received</h2>
            </div>
            <div class="content">
                <div class="greeting">
                    <p>Dear {contact_submission.name},</p>
                    <p>Thank you for reaching out to Psyling. I have received your message and will respond within <strong>48 hours</strong>.</p>
                </div>

                <div class="emergency-box">
                    <h3>⚠️ IMPORTANT: Mental Health Emergency Resources</h3>
                    <p>If you are experiencing a mental health emergency, please contact:</p>
                    <div class="crisis-line"><strong>Emergency Services:</strong> 911</div>
                    <div class="crisis-line"><strong>Toronto Distress Centre:</strong> 416-408-HELP (4357)</div>
                    <div class="crisis-line"><strong>Crisis Services Canada:</strong> 1-833-456-4566</div>
                    <div class="crisis-line"><strong>Good2Talk</strong> (post-secondary students): 1-866-925-5454</div>
                    <p style="margin-top: 15px; font-weight: 600;">These services are available 24/7 for immediate support.</p>
                </div>

                <div class="message-note">
                    <p style="margin: 0;"><strong>Your message has been saved.</strong> I look forward to speaking with you soon and discussing how I can support your mental health journey.</p>
                </div>

                <div class="signature">
                    <div class="name">Dr. Valery Belyanin</div>
                    <div class="title">Registered Psychotherapist</div>
                    <div class="credential">College of Registered Psychotherapists of Ontario (CRPO)</div>
                    <div class="contact">📧 Email: <a href="mailto:psyling@gmail.com">psyling@gmail.com</a></div>
                    <div class="contact">📞 Phone: <a href="tel:+16473608980">(647) 360-8980</a></div>
                    <div class="contact">🌐 Web: <a href="https://psyling.com">psyling.com</a></div>
                </div>
            </div>
            <div class="footer">
                <p><strong>This is an automated confirmation.</strong></p>
                <p style="margin-top: 10px; font-size: 12px;">Please do not reply to this email. To reach Dr. Belyanin directly, use psyling@gmail.com</p>
            </div>
        </div>
    </body>
    </html>
    """

    try:
        result = send_email(
            subject=subject,
            recipients=[contact_submission.email],
            text_body=text_body,
            html_body=html_body
        )

        if result:
            logger.info(f'✅ Auto-reply confirmation sent to {contact_submission.email}')
        else:
            logger.error(f'❌ Failed to send auto-reply to {contact_submission.email}')

        return result

    except Exception as e:
        logger.error(f'❌ Exception sending auto-reply to {contact_submission.email}: {str(e)}')
        return False
