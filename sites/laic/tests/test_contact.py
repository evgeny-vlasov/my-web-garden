import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import MagicMock, patch

from app import app


class ContactTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        app.config.update(
            TESTING=True, SECRET_KEY='test-only', DATABASE_URL=None,
            CONTACT_STORAGE_PATH=str(Path(self.directory.name) / 'contacts.jsonl'),
        )
        self.client = app.test_client()
        self.form = {
            'organization_name': 'Example nonprofit', 'contact_name': 'Example Person',
            'email': 'example@example.com', 'organization_type': 'Nonprofit',
            'problem_to_solve': 'Help organize volunteer onboarding.',
        }

    def test_local_contact_is_persisted(self):
        response = self.client.post('/contact', data=self.form)
        self.assertEqual(response.status_code, 302)
        row = json.loads(Path(app.config['CONTACT_STORAGE_PATH']).read_text())
        self.assertEqual(row['email'], self.form['email'])

    @patch('database.psycopg.connect')
    def test_postgres_contact_uses_versioned_schema(self, connect):
        app.config['DATABASE_URL'] = 'postgresql://test-only'
        connection = MagicMock()
        connect.return_value.__enter__.return_value = connection
        response = self.client.post('/contact', data=self.form)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(connect.call_count, 2)
        executions = connection.cursor.return_value.__enter__.return_value.execute.call_args_list
        self.assertIn('CREATE TABLE IF NOT EXISTS contact_submissions', executions[0].args[0])
        self.assertIn('INSERT INTO contact_submissions', executions[1].args[0])
        self.assertIn(self.form['email'], executions[1].args[1])
