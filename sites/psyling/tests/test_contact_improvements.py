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
from shared import email as shared_email  # noqa: E402
from shared.base_app import db  # noqa: E402
from shared.models import ContactSubmission, SpamBlocklist, User  # noqa: E402

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
        site_app.limiter.enabled = False
        site_app.limiter.reset()
        self.client = self.app.test_client()

    def tearDown(self):
        site_app.limiter.enabled = False
        site_app.limiter.reset()
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

    def _store_previous_message(self, message):
        contact = ContactSubmission(
            name='Earlier inquiry',
            email='earlier@example.invalid',
            message=message,
        )
        db.session.add(contact)
        db.session.commit()
        return contact

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
        submission = ContactSubmission.query.one()
        self.assertTrue(submission.is_spam)
        self.assertEqual(submission.status, 'spam')
        notify_mock.assert_not_called()
        confirm_mock.assert_not_called()

    @patch.object(site_app, 'send_contact_confirmation', return_value=True)
    @patch.object(site_app, 'send_contact_notification', return_value=True)
    def test_blocklisted_contact_is_retained_for_review_without_email(
        self, notify_mock, confirm_mock
    ):
        db.session.add(
            SpamBlocklist(
                value='Blocked synthetic name',
                type='name',
                reason='Automated test',
            )
        )
        db.session.commit()

        response = self.client.post(
            '/contact',
            data=self._contact_payload(name='Blocked synthetic name'),
        )

        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.headers['Location'].endswith('/contact'))
        submission = ContactSubmission.query.one()
        self.assertTrue(submission.is_spam)
        self.assertEqual(submission.status, 'spam')
        notify_mock.assert_not_called()
        confirm_mock.assert_not_called()

    @patch.object(site_app, 'send_contact_confirmation', return_value=True)
    @patch.object(site_app, 'send_contact_notification', return_value=True)
    def test_legitimate_one_link_inquiry_is_not_quarantined(
        self, notify_mock, confirm_mock
    ):
        response = self.client.post(
            '/contact',
            data=self._contact_payload(
                message=(
                    'Digital marketing work has been stressful; this page explains '
                    'the context: https://www.example.invalid/benefits'
                )
            ),
        )

        self.assertEqual(response.status_code, 302)
        submission = ContactSubmission.query.one()
        self.assertFalse(submission.is_spam)
        self.assertEqual(submission.status, 'new')
        notify_mock.assert_called_once_with(submission)
        confirm_mock.assert_called_once_with(submission)

    @patch.object(site_app, 'send_contact_confirmation', return_value=True)
    @patch.object(site_app, 'send_contact_notification', return_value=True)
    def test_repeated_genuine_follow_up_is_not_quarantined(
        self, notify_mock, confirm_mock
    ):
        message = 'I am following up about availability for a therapy appointment.'
        self._store_previous_message(message)

        response = self.client.post(
            '/contact', data=self._contact_payload(message=message)
        )

        self.assertEqual(response.status_code, 302)
        submission = ContactSubmission.query.order_by(
            ContactSubmission.id.desc()
        ).first()
        self.assertFalse(submission.is_spam)
        self.assertEqual(submission.status, 'new')
        notify_mock.assert_called_once_with(submission)
        confirm_mock.assert_called_once_with(submission)

    @patch.object(site_app, 'send_contact_confirmation', return_value=True)
    @patch.object(site_app, 'send_contact_notification', return_value=True)
    def test_single_commercial_phrase_is_not_quarantined(
        self, notify_mock, confirm_mock
    ):
        response = self.client.post(
            '/contact',
            data=self._contact_payload(
                message='I have a question related to digital marketing stress.'
            ),
        )

        self.assertEqual(response.status_code, 302)
        submission = ContactSubmission.query.one()
        self.assertFalse(submission.is_spam)
        notify_mock.assert_called_once_with(submission)
        confirm_mock.assert_called_once_with(submission)

    @patch.object(site_app, 'send_contact_confirmation', return_value=True)
    @patch.object(site_app, 'send_contact_notification', return_value=True)
    def test_multiple_links_alone_are_not_quarantined(
        self, notify_mock, confirm_mock
    ):
        response = self.client.post(
            '/contact',
            data=self._contact_payload(
                message=(
                    'These two benefit pages explain my question: '
                    'https://example.invalid/one and https://example.invalid/two'
                )
            ),
        )

        self.assertEqual(response.status_code, 302)
        submission = ContactSubmission.query.one()
        self.assertFalse(submission.is_spam)
        notify_mock.assert_called_once_with(submission)
        confirm_mock.assert_called_once_with(submission)

    @patch.object(site_app, 'send_contact_confirmation', return_value=True)
    @patch.object(site_app, 'send_contact_notification', return_value=True)
    def test_repeated_commercial_pitch_is_quarantined_without_email(
        self, notify_mock, confirm_mock
    ):
        previous = 'Our digital marketing service can improve your website.'
        self._store_previous_message(previous)

        response = self.client.post(
            '/contact',
            data=self._contact_payload(
                name='Reviewable submission',
                email='reviewable@example.com',
                message='  OUR digital marketing service can improve your website.  ',
            ),
        )

        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.headers['Location'].endswith('/contact'))
        submission = ContactSubmission.query.order_by(
            ContactSubmission.id.desc()
        ).first()
        self.assertTrue(submission.is_spam)
        self.assertEqual(submission.status, 'spam')
        notify_mock.assert_not_called()
        confirm_mock.assert_not_called()

        self._login_admin()
        spam_page = self.client.get('/admin/contacts?show=spam')
        self.assertIn('Reviewable submission', spam_page.get_data(as_text=True))

        restored = self.client.post(
            f'/admin/contacts/{submission.id}/toggle-spam'
        )
        self.assertEqual(restored.status_code, 302)
        db.session.refresh(submission)
        self.assertFalse(submission.is_spam)
        self.assertEqual(submission.status, 'new')
        active_page = self.client.get('/admin/contacts')
        self.assertIn('Reviewable submission', active_page.get_data(as_text=True))

    @patch.object(site_app, 'send_contact_confirmation', return_value=True)
    @patch.object(site_app, 'send_contact_notification', return_value=True)
    def test_multiple_link_commercial_spam_is_quarantined_without_email(
        self, notify_mock, confirm_mock
    ):
        response = self.client.post(
            '/contact',
            data=self._contact_payload(
                message=(
                    'Our SEO service can improve your ranking. See '
                    'https://example.invalid/one and https://example.invalid/two.'
                )
            ),
        )

        self.assertEqual(response.status_code, 302)
        submission = ContactSubmission.query.one()
        self.assertTrue(submission.is_spam)
        self.assertEqual(submission.status, 'spam')
        notify_mock.assert_not_called()
        confirm_mock.assert_not_called()

    def test_contact_notification_logs_use_id_and_categorical_outcome(self):
        submission = ContactSubmission(
            name='Synthetic visitor',
            email='private-marker@example.invalid',
            message='Synthetic private marker must not enter logs.',
        )
        db.session.add(submission)
        db.session.commit()

        with patch.object(shared_email.mail, 'send'):
            with self.assertLogs(shared_email.logger.name, level='INFO') as captured:
                self.assertTrue(shared_email.send_contact_notification(submission))
                self.assertTrue(shared_email.send_contact_confirmation(submission))

        joined = '\n'.join(captured.output)
        self.assertIn(f'contact submission {submission.id}', joined)
        self.assertNotIn(submission.name, joined)
        self.assertNotIn(submission.email, joined)
        self.assertNotIn(submission.message, joined)

    def test_contact_notification_failures_do_not_log_private_values(self):
        submission = ContactSubmission(
            name='Synthetic visitor',
            email='private-marker@example.invalid',
            message='Synthetic private marker must not enter logs.',
        )
        db.session.add(submission)
        db.session.commit()

        with patch.object(
            shared_email.mail,
            'send',
            side_effect=RuntimeError('private-marker@example.invalid'),
        ):
            with self.assertLogs(shared_email.logger.name, level='ERROR') as captured:
                self.assertFalse(shared_email.send_contact_notification(submission))
                self.assertFalse(shared_email.send_contact_confirmation(submission))

        joined = '\n'.join(captured.output)
        self.assertIn(f'contact submission {submission.id}', joined)
        self.assertNotIn(submission.name, joined)
        self.assertNotIn(submission.email, joined)
        self.assertNotIn(submission.message, joined)

    @patch.object(site_app, 'send_contact_confirmation', return_value=True)
    @patch.object(site_app, 'send_contact_notification', return_value=True)
    def test_contact_specific_rate_limit_applies_to_post_only(
        self, notify_mock, confirm_mock
    ):
        self.app.config['RATELIMIT_ENABLED'] = True
        site_app.limiter.enabled = True
        site_app.limiter.reset()
        try:
            for _ in range(7):
                self.assertEqual(self.client.get('/contact').status_code, 200)

            for number in range(5):
                response = self.client.post(
                    '/contact',
                    data=self._contact_payload(
                        message=f'Unique appointment question number {number}.'
                    ),
                )
                self.assertEqual(response.status_code, 302)

            limited = self.client.post(
                '/contact',
                data=self._contact_payload(
                    message='A sixth unique appointment question.'
                ),
            )
            self.assertEqual(limited.status_code, 429)
            self.assertEqual(ContactSubmission.query.count(), 5)
            self.assertEqual(notify_mock.call_count, 5)
            self.assertEqual(confirm_mock.call_count, 5)
        finally:
            self.app.config['RATELIMIT_ENABLED'] = False
            site_app.limiter.enabled = False
            site_app.limiter.reset()

    @patch.object(site_app, 'send_contact_confirmation', return_value=True)
    @patch.object(site_app, 'send_contact_notification', side_effect=RuntimeError('smtp down'))
    def test_mail_failure_does_not_lose_inquiry(self, notify_mock, confirm_mock):
        response = self.client.post('/contact', data=self._contact_payload())

        self.assertEqual(response.status_code, 302)
        self.assertEqual(ContactSubmission.query.count(), 1)
        notify_mock.assert_called_once()
        confirm_mock.assert_called_once()

    def test_authenticated_contact_detail_is_complete_html_page(self):
        self._login_admin()
        contact = ContactSubmission(
            name='Reply Person',
            email='reply@example.com',
            phone='+1 647-555-0100',
            message='First paragraph.\n\nSecond paragraph with the full request.',
            notes='Call after 5 PM.',
        )
        db.session.add(contact)
        db.session.commit()

        response = self.client.get(f'/admin/contacts/{contact.id}/view')

        self.assertEqual(response.status_code, 200)
        self.assertIn('text/html', response.content_type)
        html = response.get_data(as_text=True)
        self.assertIn('Reply Person', html)
        self.assertIn('First paragraph.\n\nSecond paragraph with the full request.', html)
        self.assertIn('Call after 5 PM.', html)
        self.assertIn('Needs reply', html)
        db.session.refresh(contact)
        self.assertTrue(contact.is_read)
        self.assertEqual(contact.status, 'new')
        self.assertIn('Reply by email', html)
        self.assertIn('mailto:reply@example.com', html)
        self.assertIn('href="tel:+1 647-555-0100"', html)
        self.assertIn('subject=Re%3A%20Your%20inquiry%20to%20Psyling', html)
        self.assertIn('Back to contacts', html)

    def test_contact_list_has_real_detail_link_for_every_contact(self):
        self._login_admin()
        contacts = [
            ContactSubmission(
                name=f'Mobile Visitor {number}',
                email=f'visitor{number}@example.com',
                message=f'Inquiry {number}',
            )
            for number in range(1, 3)
        ]
        db.session.add_all(contacts)
        db.session.commit()

        response = self.client.get('/admin/contacts')

        self.assertEqual(response.status_code, 200)
        html = response.get_data(as_text=True)
        for contact in contacts:
            detail_href = f'href="/admin/contacts/{contact.id}/view"'
            self.assertIn(detail_href, html)
            self.assertIn(contact.name, html)

    def test_unauthorized_contact_detail_redirects_to_login(self):
        contact = ContactSubmission(
            name='Private Visitor',
            email='private@example.com',
            message='This message must stay private.',
        )
        db.session.add(contact)
        db.session.commit()

        response = self.client.get(f'/admin/contacts/{contact.id}/view')

        self.assertEqual(response.status_code, 302)
        self.assertIn('/admin/login', response.headers['Location'])

    def test_legacy_contact_detail_url_still_returns_html(self):
        self._login_admin()
        contact = ContactSubmission(
            name='Bookmarked Visitor',
            email='bookmark@example.com',
            message='An older saved link still works.',
        )
        db.session.add(contact)
        db.session.commit()

        response = self.client.get(f'/admin/contacts/{contact.id}')

        self.assertEqual(response.status_code, 200)
        self.assertIn('text/html', response.content_type)
        self.assertIn('An older saved link still works.', response.get_data(as_text=True))

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
