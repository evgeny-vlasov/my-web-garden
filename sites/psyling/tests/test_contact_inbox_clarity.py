import os
import sys
import tempfile
import unittest
from datetime import datetime


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

    def test_list_has_row_and_bulk_spam_controls(self):
        contact = self._contact('Selectable Visitor')

        html = self.client.get('/admin/contacts').get_data(as_text=True)

        self.assertIn('Select all on this page', html)
        self.assertIn('Mark selected as spam', html)
        self.assertIn('Archive selected', html)
        self.assertIn(f'value="{contact.id}"', html)
        self.assertIn(f'/admin/contacts/{contact.id}/mark-spam', html)

    def test_per_row_mark_spam_preserves_list_location(self):
        contact = self._contact('Row Spam Visitor')

        response = self.client.post(
            f'/admin/contacts/{contact.id}/mark-spam',
            data={
                'return_show': 'unread',
                'return_status': 'new',
                'return_q': 'Visitor',
                'return_page': '3',
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertIn('show=unread', response.headers['Location'])
        self.assertIn('status=new', response.headers['Location'])
        self.assertIn('q=Visitor', response.headers['Location'])
        self.assertIn('page=3', response.headers['Location'])
        db.session.refresh(contact)
        self.assertTrue(contact.is_spam)
        self.assertEqual(contact.status, 'spam')

    def test_bulk_mark_spam_is_idempotent_for_existing_spam(self):
        first = self._contact('First Bulk Visitor')
        second = self._contact('Already Spam Visitor', is_spam=True, status='spam')
        third = self._contact('Third Bulk Visitor')

        response = self.client.post(
            '/admin/contacts/bulk-mark-spam',
            data={
                'contact_ids': [str(first.id), str(second.id), str(third.id)],
                'return_show': 'inbox',
            },
            follow_redirects=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'2 inquiries marked as spam.', response.data)
        for contact in (first, second, third):
            db.session.refresh(contact)
            self.assertTrue(contact.is_spam)
            self.assertEqual(contact.status, 'spam')

    def test_bulk_mark_spam_rejects_nonexistent_id_atomically(self):
        contact = self._contact('Atomic Visitor')

        response = self.client.post(
            '/admin/contacts/bulk-mark-spam',
            data={'contact_ids': [str(contact.id), '999999']},
            follow_redirects=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'no longer exist', response.data)
        db.session.refresh(contact)
        self.assertFalse(contact.is_spam)

    def test_bulk_mark_spam_rejects_malformed_id_atomically(self):
        contact = self._contact('Malformed Selection Visitor')

        response = self.client.post(
            '/admin/contacts/bulk-mark-spam',
            data={'contact_ids': [str(contact.id), 'not-an-id']},
            follow_redirects=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'selected inquiries were invalid', response.data)
        db.session.refresh(contact)
        self.assertFalse(contact.is_spam)

    def test_bulk_action_with_no_selection_changes_nothing(self):
        contact = self._contact('Unselected Visitor')

        response = self.client.post(
            '/admin/contacts/bulk-mark-spam',
            data={},
            follow_redirects=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Select at least one inquiry.', response.data)
        db.session.refresh(contact)
        self.assertFalse(contact.is_spam)

    def test_bulk_action_requires_admin_authentication(self):
        contact = self._contact('Protected Visitor')
        anonymous = self.app.test_client()

        response = anonymous.post(
            '/admin/contacts/bulk-mark-spam',
            data={'contact_ids': str(contact.id)},
        )

        self.assertEqual(response.status_code, 302)
        self.assertIn('/admin/login', response.headers['Location'])
        db.session.refresh(contact)
        self.assertFalse(contact.is_spam)

    def test_bulk_action_requires_csrf_when_enabled(self):
        contact = self._contact('CSRF Visitor')
        self.app.config['WTF_CSRF_ENABLED'] = True
        try:
            response = self.client.post(
                '/admin/contacts/bulk-mark-spam',
                data={'contact_ids': str(contact.id)},
            )
        finally:
            self.app.config['WTF_CSRF_ENABLED'] = False

        self.assertEqual(response.status_code, 400)
        db.session.refresh(contact)
        self.assertFalse(contact.is_spam)

    def test_bulk_archive_soft_deletes_selected_spam_only(self):
        selected = self._contact(
            'Selected Spam Visitor', is_spam=True, status='spam'
        )
        untouched = self._contact(
            'Untouched Spam Visitor', is_spam=True, status='spam'
        )

        response = self.client.post(
            '/admin/contacts/bulk-archive',
            data={'contact_ids': str(selected.id), 'return_show': 'spam'},
            follow_redirects=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'1 inquiry archived.', response.data)
        db.session.refresh(selected)
        db.session.refresh(untouched)
        self.assertIsNotNone(selected.archived_at)
        self.assertIsNone(untouched.archived_at)
        self.assertEqual(ContactSubmission.query.count(), 2)

        spam_html = self.client.get('/admin/contacts?show=spam').get_data(as_text=True)
        archived_html = self.client.get(
            '/admin/contacts?show=archived'
        ).get_data(as_text=True)
        self.assertNotIn(selected.name, spam_html)
        self.assertIn(untouched.name, spam_html)
        self.assertIn(selected.name, archived_html)

    def test_bulk_action_enforces_maximum_batch_size(self):
        contact = self._contact('Batch Limit Visitor')
        too_many = [str(contact.id)] * (site_app.CONTACT_BULK_ACTION_LIMIT + 1)

        response = self.client.post(
            '/admin/contacts/bulk-mark-spam',
            data={'contact_ids': too_many},
            follow_redirects=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Select no more than 100 inquiries', response.data)
        db.session.refresh(contact)
        self.assertFalse(contact.is_spam)

    def test_filters_remain_consistent_after_bulk_actions(self):
        marked = self._contact('Marked From Unread', is_read=False)
        active = self._contact('Still Active', is_read=False)
        archived = self._contact(
            'Already Archived', archived_at=datetime.utcnow(), is_read=False
        )

        self.client.post(
            '/admin/contacts/bulk-mark-spam',
            data={'contact_ids': str(marked.id), 'return_show': 'unread'},
        )

        active_html = self.client.get('/admin/contacts').get_data(as_text=True)
        unread_html = self.client.get('/admin/contacts?show=unread').get_data(as_text=True)
        spam_html = self.client.get('/admin/contacts?show=spam').get_data(as_text=True)
        archived_html = self.client.get(
            '/admin/contacts?show=archived'
        ).get_data(as_text=True)
        self.assertNotIn(marked.name, active_html)
        self.assertNotIn(marked.name, unread_html)
        self.assertIn(marked.name, spam_html)
        self.assertIn(active.name, active_html)
        self.assertIn(active.name, unread_html)
        self.assertIn(archived.name, archived_html)

if __name__ == '__main__':
    unittest.main()
