import os
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch


class ContactTest(unittest.TestCase):
    def test_contact_saves_using_the_pool_emergency_migration(self):
        site_root = Path(__file__).resolve().parents[1]
        with TemporaryDirectory() as directory:
            database_path = Path(directory) / 'contacts.sqlite'
            with patch.dict(os.environ, {
                'DATABASE_URL': f'sqlite:///{database_path.as_posix()}',
                'FLASK_ENV': 'testing',
                'SECRET_KEY': 'test-only',
            }):
                from app import app, db

            app.config['RATELIMIT_ENABLED'] = False
            result = app.test_cli_runner().invoke(
                args=['db', 'upgrade', '--directory', str(site_root / 'migrations')]
            )
            self.assertEqual(result.exit_code, 0, result.output)

            response = app.test_client().post('/contact', data={
                'name': 'Example Customer',
                'phone': '403-555-0100',
                'location': 'Calgary',
                'message': 'The pool liner has a tear near the steps.',
            })
            self.assertEqual(response.status_code, 302)

            with app.app_context():
                row = db.session.execute(db.text(
                    'SELECT name, email, message, status, is_spam FROM contact_submissions'
                )).one()
                self.assertEqual(row.name, 'Example Customer')
                self.assertEqual(row.email, 'no-email-provided@poolemergency.local')
                self.assertIn('Location/neighbourhood: Calgary', row.message)
                self.assertEqual(row.status, 'new')
                self.assertFalse(row.is_spam)
