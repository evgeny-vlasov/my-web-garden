import os
import sys
import tempfile
import unittest


SITE_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
REPO_ROOT = os.path.abspath(os.path.join(SITE_ROOT, '../..'))
sys.path.insert(0, SITE_ROOT)
sys.path.insert(0, REPO_ROOT)

os.environ['FLASK_ENV'] = 'development'
os.environ['DATABASE_URL'] = (
    f"sqlite:///{os.path.join(tempfile.gettempdir(), 'psyling_inbox_tests.sqlite')}"
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


class ContactInboxClarityTest(unittest.TestCase):
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
        self._login_admin()

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

    def _contact(self, name, **overrides):
        values = {
            'name': name,
            'email': f"{name.lower().replace(' ', '-')}@example.com",
            'message': 'Please tell me about appointment availability.',
        }
        values.update(overrides)
        contact = ContactSubmission(**values)
        db.session.add(contact)
        db.session.commit()
        return contact

    def test_opening_inquiry_marks_read_without_changing_reply_status(self):
        contact = self._contact('Needs Reply Visitor', status='new', is_read=False)

        response = self.client.get(f'/admin/contacts/{contact.id}/view')

        self.assertEqual(response.status_code, 200)
        db.session.refresh(contact)
        self.assertTrue(contact.is_read)
        self.assertEqual(contact.status, 'new')
        html = response.get_data(as_text=True)
        self.assertIn('Needs reply', html)
        self.assertNotIn('<span class="badge bg-danger">Unread</span>', html)
        self.assertIn('Opening an inquiry automatically clears its', html)

    def test_unread_view_and_dashboard_count_use_is_read_only(self):
        unread_contacted = self._contact(
            'Unread Contacted', status='contacted', is_read=False
        )
        read_needs_reply = self._contact(
            'Read Needs Reply', status='new', is_read=True
        )
        archived_unread = self._contact(
            'Archived Unread',
            status='new',
            is_read=False,
            archived_at=site_app.datetime.utcnow(),
        )
        spam_unread = self._contact(
            'Spam Unread', status='spam', is_read=False, is_spam=True
        )

        unread_page = self.client.get('/admin/contacts?show=unread')
        unread_html = unread_page.get_data(as_text=True)
        self.assertIn(unread_contacted.name, unread_html)
        self.assertNotIn(read_needs_reply.name, unread_html)
        self.assertNotIn(archived_unread.name, unread_html)
        self.assertNotIn(spam_unread.name, unread_html)
        self.assertIn('Contacted', unread_html)

        dashboard = self.client.get('/admin/dashboard')
        dashboard_html = dashboard.get_data(as_text=True)
        self.assertIn('Unread inquiries', dashboard_html)
        self.assertIn('href="/admin/contacts?show=unread"', dashboard_html)
        self.assertIn('Unread Contacted', dashboard_html)
        self.assertNotIn('Archived Unread', dashboard_html)
        self.assertNotIn('Spam Unread', dashboard_html)
        self.assertRegex(
            dashboard_html,
            r'(?s)Unread inquiries.*?<h3[^>]*>\s*1\s*</h3>',
        )

    def test_workflow_labels_and_status_filter_are_consistent(self):
        needs_reply = self._contact('Waiting Visitor', status='new', is_read=True)
        contacted = self._contact('Answered Visitor', status='contacted', is_read=True)

        active_page = self.client.get('/admin/contacts')
        active_html = active_page.get_data(as_text=True)
        self.assertIn('Needs reply', active_html)
        self.assertIn('Contacted', active_html)
        self.assertRegex(
            active_html,
            r'(?s)<option value="new"[^>]*>\s*Needs reply\s*</option>',
        )

        needs_reply_page = self.client.get('/admin/contacts?status=new')
        filtered_html = needs_reply_page.get_data(as_text=True)
        self.assertIn(needs_reply.name, filtered_html)
        self.assertNotIn(contacted.name, filtered_html)

        detail = self.client.get(f'/admin/contacts/{contacted.id}/view')
        self.assertIn('>Contacted</span>', detail.get_data(as_text=True))

    def test_archive_removes_from_active_and_restore_returns_it(self):
        contact = self._contact('Archive Visitor', status='new', is_read=True)
        detail = self.client.get(f'/admin/contacts/{contact.id}/view')
        self.assertIn('Archive from active list', detail.get_data(as_text=True))

        archived = self.client.post(f'/admin/contacts/{contact.id}/archive')

        self.assertEqual(archived.status_code, 302)
        self.assertIn('/admin/contacts?show=inbox', archived.headers['Location'])
        db.session.refresh(contact)
        self.assertIsNotNone(contact.archived_at)
        self.assertEqual(ContactSubmission.query.count(), 1)
        self.assertNotIn(
            contact.name,
            self.client.get('/admin/contacts').get_data(as_text=True),
        )
        self.assertIn(
            contact.name,
            self.client.get('/admin/contacts?show=archived').get_data(as_text=True),
        )

        archived_detail = self.client.get(f'/admin/contacts/{contact.id}/view')
        self.assertIn('Restore to active list', archived_detail.get_data(as_text=True))
        restored = self.client.post(f'/admin/contacts/{contact.id}/archive')

        self.assertEqual(restored.status_code, 302)
        db.session.refresh(contact)
        self.assertIsNone(contact.archived_at)
        self.assertIn(
            contact.name,
            self.client.get('/admin/contacts').get_data(as_text=True),
        )

    def test_manual_unread_survives_redirect_to_unread_list(self):
        contact = self._contact('Read Toggle Visitor', is_read=False)
        self.client.get(f'/admin/contacts/{contact.id}/view')
        db.session.refresh(contact)
        self.assertTrue(contact.is_read)

        marked_unread = self.client.post(
            f'/admin/contacts/{contact.id}/toggle-read'
        )

        self.assertEqual(marked_unread.status_code, 302)
        self.assertIn('/admin/contacts?show=unread', marked_unread.headers['Location'])
        db.session.refresh(contact)
        self.assertFalse(contact.is_read)
        self.assertIn(
            contact.name,
            self.client.get(marked_unread.headers['Location']).get_data(as_text=True),
        )

        marked_read = self.client.post(f'/admin/contacts/{contact.id}/toggle-read')
        self.assertEqual(marked_read.status_code, 302)
        db.session.refresh(contact)
        self.assertTrue(contact.is_read)


if __name__ == '__main__':
    unittest.main()
