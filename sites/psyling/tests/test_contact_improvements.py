import os
import sys
import tempfile
import unittest
from unittest.mock import patch


SITE_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
REPO_ROOT = os.path.abspath(os.path.join(SITE_ROOT, '../..'))
sys.path.insert(0, SITE_ROOT)
sys.path.insert(0, REPO_ROOT)

os.environ['FLASK_ENV'] = 'development'
os.environ['DATABASE_URL'] = (
    f"sqlite:///{os.path.join(tempfile.gettempdir(), 'psyling_contact_tests.sqlite')}"
)
os.environ['SECRET_KEY'] = 'test-secret'
os.environ['SITE_DOMAIN'] = 'psyling.com'
os.environ['MAIL_DEFAULT_SENDER'] = 'noreply@psyling.test'
os.environ['ADMIN_EMAIL'] = 'admin@psyling.test'

import app as site_app  # noqa: E402
from jinja2 import ChoiceLoader, FileSystemLoader  # noqa: E402
from shared.base_app import db  # noqa: E402
from shared.models import ContactSubmission, User  # noqa: E402

site_app.app.jinja_loader = ChoiceLoader([
    FileSystemLoader(os.path.join(SITE_ROOT, 'templates')),
    FileSystemLoader(os.path.join(REPO_ROOT, 'shared', 'templates')),
])


class ContactImprovementsTest(unittest.TestCase):
    def setUp(self):
        self.app = site_app.app
        self.app.config.update(
            TESTING=True,
            WTF_CSRF_ENABLED=False,
            RATELIMIT_ENABLED=False,
            SERVER_NAME='psyling.com',
            MAIL_SUPPRESS_SEND=True,
        )
        self.ctx = self.app.app_context()
        self.ctx.push()
        db.drop_all()
        db.create_all()
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.ctx.pop()

    def _contact_payload(self, **overrides):
        payload = {
            'name': 'Test Visitor',
            'email': 'visitor@example.com',
            'phone': '647-555-0100',
            'message': 'I would like to ask about booking a therapy session.',
            'website': '',
        }
        payload.update(overrides)
        return payload

    def _login_admin(self):
        admin = User(username='admin', email='admin@example.com', role='admin')
        admin.set_password('password')
        db.session.add(admin)
        db.session.commit()
        with self.client.session_transaction() as session:
            session['_user_id'] = str(admin.id)
            session['_fresh'] = True
        return admin

    @patch.object(site_app, 'send_contact_confirmation', return_value=True)
    @patch.object(site_app, 'send_contact_notification', return_value=True)
    def test_valid_contact_is_stored_and_triggers_admin_notification(
        self, notify_mock, confirm_mock
    ):
        response = self.client.post('/contact', data=self._contact_payload())

        self.assertEqual(response.status_code, 302)
        submission = ContactSubmission.query.one()
        self.assertEqual(submission.email, 'visitor@example.com')
        notify_mock.assert_called_once()
        confirm_mock.assert_called_once()

    @patch.object(site_app, 'send_contact_confirmation', return_value=True)
    @patch.object(site_app, 'send_contact_notification', return_value=True)
    def test_honeypot_spam_is_handled_without_notification(
        self, notify_mock, confirm_mock
    ):
        response = self.client.post(
            '/contact',
            data=self._contact_payload(website='https://spam.example'),
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(ContactSubmission.query.count(), 0)
        notify_mock.assert_not_called()
        confirm_mock.assert_not_called()

    @patch.object(site_app, 'send_contact_confirmation', return_value=True)
    @patch.object(site_app, 'send_contact_notification', side_effect=RuntimeError('smtp down'))
    def test_mail_failure_does_not_lose_inquiry(self, notify_mock, confirm_mock):
        response = self.client.post('/contact', data=self._contact_payload())

        self.assertEqual(response.status_code, 302)
        self.assertEqual(ContactSubmission.query.count(), 1)
        notify_mock.assert_called_once()
        confirm_mock.assert_called_once()

    def test_reply_link_uses_visitor_email(self):
        self._login_admin()
        contact = ContactSubmission(
            name='Reply Person',
            email='reply@example.com',
            message='Please reply to this inquiry.',
        )
        db.session.add(contact)
        db.session.commit()

        response = self.client.get(f'/admin/contacts/{contact.id}')

        self.assertEqual(response.status_code, 200)
        html = response.get_data(as_text=True)
        self.assertIn('Reply by email', html)
        self.assertIn('mailto:reply@example.com', html)
        self.assertIn('subject=Re%3A%20Your%20inquiry%20to%20Psyling', html)

    def test_psychology_today_verification_renders_without_embed_script(self):
        for path in ['/', '/about']:
            with self.subTest(path=path):
                response = self.client.get(path)

                self.assertEqual(response.status_code, 200)
                html = response.get_data(as_text=True)
                self.assertIn('✓ Verified by Psychology Today', html)
                self.assertIn('psychology-today-mobile-link', html)
                self.assertIn('footer-section-quick-links', html)
                self.assertIn('footer-section-connect', html)
                self.assertIn('footer-section-verification', html)
                self.assertIn('Psychology Today profile', html)
                self.assertIn('Psychology Today</span>', html)
                self.assertIn('Verified profile</span>', html)
                self.assertIn('https://www.psychologytoday.com/profile/176232', html)
                self.assertNotIn('https://member.psychologytoday.com/verified-seal.js', html)
                self.assertNotIn('sx-verified-seal', html)
                self.assertEqual(html.count('class="psychology-today-badge"'), 1)
                self.assertGreater(html.index('psychology-today-badge'), html.index('<footer'))

                connect_start = html.index('footer-section-connect')
                verification_start = html.index('footer-section-verification')
                connect_section = html[connect_start:verification_start]
                self.assertIn('Psychology Today profile', connect_section)
                self.assertNotIn('psychology-today-badge', connect_section)

    def test_psychology_today_badge_is_not_inside_about_credentials_card(self):
        response = self.client.get('/about')
        html = response.get_data(as_text=True)
        credentials_index = html.index('Professional Credentials')
        footer_index = html.index('<footer')
        credentials_section = html[credentials_index:footer_index]

        self.assertIn('Psychology Today <a href="https://www.psychologytoday.com/profile/176232"', credentials_section)
        self.assertNotIn('psychology-today-badge', credentials_section)


if __name__ == '__main__':
    unittest.main()
