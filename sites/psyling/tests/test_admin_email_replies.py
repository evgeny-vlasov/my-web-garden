import os
import re
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
    f"sqlite:///{os.path.join(tempfile.gettempdir(), 'psyling_reply_tests.sqlite')}"
)
os.environ['SECRET_KEY'] = 'test-secret'
os.environ['SITE_DOMAIN'] = 'psyling.com'
os.environ['MAIL_DEFAULT_SENDER'] = 'website@psyling.test'
os.environ['ADMIN_EMAIL'] = 'valery@psyling.test'

import app as site_app  # noqa: E402
from jinja2 import ChoiceLoader, FileSystemLoader  # noqa: E402
from shared.base_app import db  # noqa: E402
from shared.models import ContactEmailReply, ContactSubmission, User  # noqa: E402
from sites.psyling import email_replies  # noqa: E402


site_app.app.jinja_loader = ChoiceLoader([
    FileSystemLoader(os.path.join(SITE_ROOT, 'templates')),
    FileSystemLoader(os.path.join(REPO_ROOT, 'shared', 'templates')),
])


class AdminEmailRepliesTest(unittest.TestCase):
    def setUp(self):
        self.app = site_app.app
        self.app.config.update(
            TESTING=True,
            WTF_CSRF_ENABLED=False,
            RATELIMIT_ENABLED=False,
            SERVER_NAME='psyling.com',
            MAIL_SUPPRESS_SEND=True,
            MAIL_DEFAULT_SENDER='website@psyling.test',
            ADMIN_EMAIL='valery@psyling.test',
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

    def _login_admin(self):
        admin = User(username='admin', email='admin@example.com', role='admin')
        admin.set_password('password')
        db.session.add(admin)
        db.session.commit()
        with self.client.session_transaction() as session:
            session['_user_id'] = str(admin.id)
            session['_fresh'] = True
        return admin

    def _contact(self, **overrides):
        values = {
            'name': 'Stored Visitor',
            'email': 'stored@example.com',
            'message': 'Please tell me about appointment availability.',
        }
        values.update(overrides)
        contact = ContactSubmission(**values)
        db.session.add(contact)
        db.session.commit()
        return contact

    def _reply_payload(self, token='a' * 32, **overrides):
        values = {
            'subject': 'Re: Your inquiry to Psyling',
            'body': 'Hello,\n\nThank you for getting in touch.',
            'idempotency_key': token,
        }
        values.update(overrides)
        return values

    def test_reply_requires_admin_authentication(self):
        contact = self._contact()

        response = self.client.post(
            f'/admin/contacts/{contact.id}/reply', data=self._reply_payload()
        )

        self.assertEqual(response.status_code, 302)
        self.assertIn('/admin/login', response.headers['Location'])
        self.assertEqual(ContactEmailReply.query.count(), 0)

    def test_reply_rejects_authenticated_non_admin_user(self):
        contact = self._contact()
        user = User(username='client-user', email='client-user@example.com', role='user')
        user.set_password('password')
        db.session.add(user)
        db.session.commit()
        with self.client.session_transaction() as session:
            session['_user_id'] = str(user.id)
            session['_fresh'] = True

        forbidden = self.client.post(
            f'/admin/contacts/{contact.id}/reply',
            data=self._reply_payload(token='z' * 32),
        )
        self.assertEqual(forbidden.status_code, 403)
        self.assertEqual(ContactEmailReply.query.count(), 0)

    def test_reply_requires_csrf_token(self):
        self._login_admin()
        contact = self._contact()
        self.app.config['WTF_CSRF_ENABLED'] = True

        response = self.client.post(
            f'/admin/contacts/{contact.id}/reply', data=self._reply_payload()
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(ContactEmailReply.query.count(), 0)

        page = self.client.get(f'/admin/contacts/{contact.id}/view')
        token_match = re.search(
            r'name="csrf_token"[^>]*value="([^"]+)"',
            page.get_data(as_text=True),
        )
        self.assertIsNotNone(token_match)
        payload = self._reply_payload(token='b' * 32)
        payload['csrf_token'] = token_match.group(1)
        with patch.object(email_replies.mail, 'send') as send_mock:
            accepted = self.client.post(
                f'/admin/contacts/{contact.id}/reply', data=payload
            )
        self.assertEqual(accepted.status_code, 302)
        send_mock.assert_called_once()

    def test_reply_form_validates_subject_and_body_lengths(self):
        self._login_admin()
        contact = self._contact()

        with patch.object(email_replies.mail, 'send') as send_mock:
            response = self.client.post(
                f'/admin/contacts/{contact.id}/reply',
                data=self._reply_payload(subject='x' * 201, body='   '),
            )

        self.assertEqual(response.status_code, 302)
        page = self.client.get(response.headers['Location'])
        self.assertIn('No email was sent', page.get_data(as_text=True))
        self.assertEqual(ContactEmailReply.query.count(), 0)
        send_mock.assert_not_called()

    def test_successful_reply_uses_configured_headers_and_stored_recipient(self):
        admin = self._login_admin()
        contact = self._contact()
        payload = self._reply_payload(recipient='attacker@example.com')

        with patch.object(email_replies.mail, 'send') as send_mock:
            response = self.client.post(
                f'/admin/contacts/{contact.id}/reply', data=payload
            )

        self.assertEqual(response.status_code, 302)
        send_mock.assert_called_once()
        message = send_mock.call_args.args[0]
        self.assertEqual(message.recipients, ['stored@example.com'])
        self.assertEqual(message.sender, 'website@psyling.test')
        self.assertEqual(message.reply_to, 'valery@psyling.test')
        self.assertEqual(message.subject, 'Re: Your inquiry to Psyling')
        self.assertIn('Thank you for getting in touch.', message.body)

        stored = ContactEmailReply.query.one()
        self.assertEqual(stored.contact_submission_id, contact.id)
        self.assertEqual(stored.recipient, 'stored@example.com')
        self.assertEqual(stored.sender_user_id, admin.id)
        self.assertEqual(stored.status, 'sent')
        self.assertIsNotNone(stored.created_at)
        self.assertIsNotNone(stored.sent_at)

        db.session.refresh(contact)
        self.assertEqual(contact.status, 'contacted')
        self.assertTrue(contact.is_read)
        self.assertIsNotNone(contact.last_contacted_at)

    def test_smtp_failure_is_saved_without_false_sent_or_contacted_state(self):
        self._login_admin()
        contact = self._contact()

        with patch.object(
            email_replies.mail, 'send', side_effect=RuntimeError('smtp unavailable')
        ):
            response = self.client.post(
                f'/admin/contacts/{contact.id}/reply', data=self._reply_payload()
            )

        self.assertEqual(response.status_code, 302)
        stored = ContactEmailReply.query.one()
        self.assertEqual(stored.status, 'failed')
        self.assertIsNone(stored.sent_at)
        db.session.refresh(contact)
        self.assertEqual(contact.status, 'new')
        self.assertFalse(contact.is_read)
        self.assertIsNone(contact.last_contacted_at)

    def test_duplicate_submission_sends_only_once(self):
        self._login_admin()
        contact = self._contact()
        payload = self._reply_payload(token='c' * 32)

        with patch.object(email_replies.mail, 'send') as send_mock:
            first = self.client.post(
                f'/admin/contacts/{contact.id}/reply', data=payload
            )
            second = self.client.post(
                f'/admin/contacts/{contact.id}/reply', data=payload
            )

        self.assertEqual(first.status_code, 302)
        self.assertEqual(second.status_code, 302)
        self.assertEqual(ContactEmailReply.query.count(), 1)
        send_mock.assert_called_once()

    def test_reply_html_and_admin_history_escape_user_content(self):
        self._login_admin()
        contact = self._contact()
        payload = self._reply_payload(
            subject='<img src=x onerror=alert(1)>',
            body='<script>alert("private")</script>\nSecond line & more',
        )

        with patch.object(email_replies.mail, 'send') as send_mock:
            self.client.post(f'/admin/contacts/{contact.id}/reply', data=payload)

        message = send_mock.call_args.args[0]
        self.assertNotIn('<script>', message.html)
        self.assertIn('&lt;script&gt;', message.html)
        self.assertIn('<br>', message.html)

        page = self.client.get(f'/admin/contacts/{contact.id}/view')
        html = page.get_data(as_text=True)
        self.assertNotIn('<script>alert("private")</script>', html)
        self.assertIn('&lt;script&gt;alert', html)
        self.assertIn('&lt;img src=x onerror=alert(1)&gt;', html)

    def test_reply_history_is_displayed_in_chronological_order(self):
        admin = self._login_admin()
        contact = self._contact()
        first = ContactEmailReply(
            contact_submission=contact,
            sender_user_id=admin.id,
            subject='First chronological reply',
            body='First body',
            recipient=contact.email,
            status='sent',
            idempotency_key='f' * 32,
            created_at=site_app.datetime(2026, 8, 13, 10, 0),
            sent_at=site_app.datetime(2026, 8, 13, 10, 1),
        )
        second = ContactEmailReply(
            contact_submission=contact,
            sender_user_id=admin.id,
            subject='Second chronological reply',
            body='Second body',
            recipient=contact.email,
            status='failed',
            idempotency_key='g' * 32,
            created_at=site_app.datetime(2026, 8, 13, 11, 0),
        )
        db.session.add_all([second, first])
        db.session.commit()

        page = self.client.get(f'/admin/contacts/{contact.id}/view')
        html = page.get_data(as_text=True)

        self.assertLess(
            html.index('First chronological reply'),
            html.index('Second chronological reply'),
        )

    def test_spam_and_archived_contacts_cannot_be_replied_to(self):
        self._login_admin()
        spam = self._contact(
            email='spam@example.com', is_spam=True, status='spam'
        )
        archived = self._contact(
            email='archived@example.com', archived_at=site_app.datetime.utcnow()
        )

        with patch.object(email_replies.mail, 'send') as send_mock:
            for contact, token in ((spam, 'd' * 32), (archived, 'e' * 32)):
                with self.subTest(contact_id=contact.id):
                    response = self.client.post(
                        f'/admin/contacts/{contact.id}/reply',
                        data=self._reply_payload(token=token),
                    )
                    self.assertEqual(response.status_code, 302)

        self.assertEqual(ContactEmailReply.query.count(), 0)
        send_mock.assert_not_called()


if __name__ == '__main__':
    unittest.main()
