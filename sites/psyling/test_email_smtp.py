#!/usr/bin/env python3
"""
SMTP Connection Test for Psyling Mailgun Setup
Run this to verify email configuration before integrating with contact form

Usage:
    cd /var/www/webgarden/sites/psyling
    source venv/bin/activate
    python3 test_email_smtp.py

This script will:
1. Load environment variables from /etc/webgarden/psyling.env
2. Test SMTP connection to Mailgun
3. Send a test email to ADMIN_EMAIL
4. Provide troubleshooting guidance if errors occur
"""

import os
import sys
from datetime import datetime

# Add parent directory to path to import shared modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from flask import Flask
from flask_mail import Mail, Message


def load_env_file(filepath='/etc/webgarden/psyling.env'):
    """Load environment variables from file"""
    env_vars = {}

    if os.path.exists(filepath):
        with open(filepath) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    # Remove quotes if present
                    value = value.strip('"').strip("'")
                    os.environ[key] = value
                    env_vars[key] = value
        print(f"✅ Loaded environment from {filepath}")
        return env_vars
    else:
        print(f"⚠️  Environment file not found: {filepath}")
        return env_vars


def test_smtp_connection():
    """Test SMTP connection and send test email"""

    print("\n" + "="*70)
    print("PSYLING MAILGUN SMTP TEST")
    print("="*70 + "\n")

    # Load environment variables
    env_vars = load_env_file()

    # Create minimal Flask app
    app = Flask(__name__)

    # Configure email from environment
    app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER', 'smtp.mailgun.org')
    app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', 587))
    app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS', 'True') == 'True'
    app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
    app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER', 'noreply@psyling.com')
    app.config['ADMIN_EMAIL'] = os.getenv('ADMIN_EMAIL', 'psyling@gmail.com')

    # Display configuration (without password)
    print("Current SMTP Configuration:")
    print(f"  Server:   {app.config['MAIL_SERVER']}")
    print(f"  Port:     {app.config['MAIL_PORT']}")
    print(f"  TLS:      {app.config['MAIL_USE_TLS']}")
    print(f"  Username: {app.config['MAIL_USERNAME']}")
    print(f"  Sender:   {app.config['MAIL_DEFAULT_SENDER']}")
    print(f"  Admin:    {app.config['ADMIN_EMAIL']}")

    # Check if password is placeholder
    password = app.config['MAIL_PASSWORD']
    if password and 'PLACEHOLDER' in password:
        print(f"  Password: ⚠️  PLACEHOLDER DETECTED")
    elif password:
        print(f"  Password: {'*' * 20} (SET)")
    else:
        print(f"  Password: ❌ NOT SET")

    print()

    # Validate configuration
    errors = []

    if not password:
        errors.append("MAIL_PASSWORD not set in environment")
    elif 'PLACEHOLDER' in password:
        errors.append("MAIL_PASSWORD is still set to PLACEHOLDER - needs real SMTP password")

    if not app.config['MAIL_USERNAME']:
        errors.append("MAIL_USERNAME not set in environment")

    if errors:
        print("❌ CONFIGURATION ERRORS:\n")
        for error in errors:
            print(f"  • {error}")
        print("\n" + "="*70)
        print("TROUBLESHOOTING STEPS:")
        print("="*70)
        print("1. Verify /etc/webgarden/psyling.env exists and is readable")
        print("2. Add psyling.com domain in Mailgun dashboard:")
        print("   https://app.mailgun.com/app/sending/domains")
        print("3. Get SMTP password from:")
        print("   Domains → psyling.com → SMTP Credentials → Reset Password")
        print("4. Update /etc/webgarden/psyling.env with real SMTP password")
        print("5. Ensure DNS records are added to Cloudflare")
        print("6. Wait 10-60 minutes for DNS propagation")
        print("7. Check domain status shows 'Active' in Mailgun")
        print()
        return False

    # Initialize Flask-Mail
    mail = Mail(app)

    # Attempt to send test email
    admin_email = app.config['ADMIN_EMAIL']

    print(f"Attempting to send test email to: {admin_email}")
    print("Please wait...\n")

    try:
        with app.app_context():
            msg = Message(
                subject='✅ Psyling Email System Test - SUCCESS',
                sender=app.config['MAIL_DEFAULT_SENDER'],
                recipients=[admin_email]
            )

            msg.body = f"""
This is a test email from the Psyling email system.

If you receive this message, the SMTP configuration is working correctly!

Configuration Details:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SMTP Server:   {app.config['MAIL_SERVER']}:{app.config['MAIL_PORT']}
Sending From:  {app.config['MAIL_DEFAULT_SENDER']}
Sent To:       {admin_email}
Timestamp:     {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Next Steps:
1. ✓ Check that this email did NOT go to spam folder
2. ✓ Verify the sender address shows as noreply@psyling.com
3. ✓ Test the contact form integration
4. ✓ Monitor logs during contact form submission

Command to monitor logs:
sudo journalctl -u psyling.service -f

Command to test contact form:
Open https://psyling.com/contact and submit a test inquiry

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Psyling Email System Test - Automated Message
            """

            msg.html = f"""
            <html>
            <head>
                <style>
                    body {{ font-family: 'Segoe UI', Arial, sans-serif; line-height: 1.6; color: #333; background-color: #f5f5f5; }}
                    .container {{ max-width: 650px; margin: 20px auto; background-color: white; border-radius: 8px; overflow: hidden; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }}
                    .header {{ background: linear-gradient(135deg, #28a745 0%, #20c997 100%); color: white; padding: 30px 20px; text-align: center; }}
                    .content {{ padding: 30px; }}
                    .info-box {{ background-color: #f8f9fa; border-radius: 6px; padding: 20px; margin: 20px 0; }}
                    .info-row {{ padding: 8px 0; border-bottom: 1px solid #e0e0e0; }}
                    .info-row:last-child {{ border-bottom: none; }}
                    .label {{ font-weight: 600; color: #667eea; }}
                    .next-steps {{ background-color: #e8f4f8; border-radius: 6px; padding: 20px; margin: 20px 0; }}
                    .next-steps h3 {{ margin: 0 0 15px 0; color: #2c5aa0; }}
                    .next-steps li {{ margin: 8px 0; }}
                    .command {{ background-color: #2d3748; color: #48bb78; padding: 10px; border-radius: 4px; font-family: 'Courier New', monospace; margin: 10px 0; }}
                    .footer {{ text-align: center; padding: 20px; background-color: #f8f9fa; color: #777; font-size: 13px; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h1>✅ Email Test Successful</h1>
                        <p style="margin: 10px 0 0 0; font-size: 16px;">SMTP Configuration Working Correctly</p>
                    </div>
                    <div class="content">
                        <p>If you receive this message, the Psyling email system is configured correctly!</p>

                        <div class="info-box">
                            <h3 style="margin: 0 0 15px 0; color: #333;">Configuration Details</h3>
                            <div class="info-row">
                                <span class="label">SMTP Server:</span> {app.config['MAIL_SERVER']}:{app.config['MAIL_PORT']}
                            </div>
                            <div class="info-row">
                                <span class="label">Sending From:</span> {app.config['MAIL_DEFAULT_SENDER']}
                            </div>
                            <div class="info-row">
                                <span class="label">Sent To:</span> {admin_email}
                            </div>
                            <div class="info-row">
                                <span class="label">Timestamp:</span> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
                            </div>
                        </div>

                        <div class="next-steps">
                            <h3>📋 Next Steps</h3>
                            <ol>
                                <li>✓ Check that this email did NOT go to spam folder</li>
                                <li>✓ Verify the sender address shows as <strong>noreply@psyling.com</strong></li>
                                <li>✓ Test the contact form integration at <a href="https://psyling.com/contact">psyling.com/contact</a></li>
                                <li>✓ Monitor logs during contact form submission</li>
                            </ol>
                        </div>

                        <p><strong>Command to monitor logs:</strong></p>
                        <div class="command">sudo journalctl -u psyling.service -f</div>

                        <p><strong>Test the contact form:</strong></p>
                        <div class="command">Open https://psyling.com/contact and submit a test inquiry</div>
                    </div>
                    <div class="footer">
                        <p>Psyling Email System Test - Automated Message</p>
                        <p style="font-size: 11px; margin-top: 10px;">Do not reply to this email</p>
                    </div>
                </div>
            </body>
            </html>
            """

            mail.send(msg)

            print("="*70)
            print("✅ SUCCESS: Test email sent successfully!")
            print("="*70)
            print(f"\nCheck inbox: {admin_email}")
            print("  • Look in both inbox and spam folder")
            print("  • Verify sender shows as: noreply@psyling.com")
            print("  • Check email arrived within 1-2 minutes")
            print("\nIf email doesn't arrive within 5 minutes, check:")
            print("  • Mailgun dashboard logs: https://app.mailgun.com/logs")
            print("  • DNS records verified in Mailgun")
            print("  • Spam/junk folder")
            print("\nNext: Test contact form at https://psyling.com/contact")
            print()
            return True

    except Exception as e:
        print("="*70)
        print("❌ FAILED: Could not send test email")
        print("="*70)
        print(f"\nError: {str(e)}\n")
        print("TROUBLESHOOTING STEPS:")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print("1. Verify MAIL_PASSWORD is the SMTP password (not API key)")
        print("   • Get from: Mailgun Dashboard → Domains → psyling.com")
        print("   • Click 'SMTP Credentials' → Reset Password")
        print()
        print("2. Check domain verified in Mailgun dashboard")
        print("   • Visit: https://app.mailgun.com/app/sending/domains")
        print("   • psyling.com should show 'Active' status")
        print()
        print("3. Confirm DNS records added to Cloudflare")
        print("   • SPF: v=spf1 include:mailgun.org ~all")
        print("   • DKIM: Check Mailgun for exact value")
        print("   • Wait 10-60 minutes for propagation")
        print()
        print("4. Check DNS propagation:")
        print("   dig TXT psyling.com +short")
        print("   dig TXT smtp._domainkey.psyling.com +short")
        print()
        print("5. Review Mailgun logs for delivery attempts:")
        print("   https://app.mailgun.com/logs")
        print()
        print("COMMON ERRORS:")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print("  • '535 Authentication failed' → Wrong SMTP password")
        print("  • 'Domain not found' → Domain not verified in Mailgun")
        print("  • Connection timeout → Firewall blocking port 587")
        print("  • 'Relay access denied' → Wrong MAIL_USERNAME format")
        print()
        return False


def main():
    """Main function"""
    print("\nPsyling Email System - SMTP Test Script")
    print("Starting email configuration test...\n")

    # Run test
    success = test_smtp_connection()

    # Exit with appropriate code
    if success:
        print("\n" + "="*70)
        print("✅ TEST PASSED - Email system is working!")
        print("="*70)
        print("\nYou can now:")
        print("  1. Test the contact form at https://psyling.com/contact")
        print("  2. Monitor logs: sudo journalctl -u psyling.service -f")
        print("  3. Mark this task as complete")
        print()
        sys.exit(0)
    else:
        print("\n" + "="*70)
        print("❌ TEST FAILED - Fix configuration and retry")
        print("="*70)
        print("\nRun this script again after fixing issues:")
        print("  python3 test_email_smtp.py")
        print()
        sys.exit(1)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrupted by user")
        sys.exit(130)
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
