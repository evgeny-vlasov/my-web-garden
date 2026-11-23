import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('create_site', ROOT / 'tools' / 'create_site.py')
creator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(creator)


class CreateSiteTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.brief = {'slug': 'sunny-demo', 'name': '<Sunny>', 'summary': 'Public description',
                      'contact': 'hello@example.com'}

    def test_generated_site_runs_without_repository_or_database(self):
        site = creator.create_site(self.brief, self.directory.name)
        # Execute from the generated site with only its copied dependencies.
        check = """
from app import app
client = app.test_client()
response = client.get('/')
assert response.status_code == 200
assert b'&lt;Sunny&gt;' in response.data
assert client.get('/health').json['site'] == 'sunny-demo'
assert client.post('/api/chat', json={'message':'Hi'}).status_code == 503
"""
        subprocess.run([sys.executable, '-c', check], cwd=site, check=True)
        handoff = json.loads((site / 'bot-handoff.json').read_text())
        self.assertEqual(handoff['public_knowledge'], self.brief['summary'])
        self.assertEqual(handoff['contact'], self.brief['contact'])

    def test_existing_site_is_preserved(self):
        site = creator.create_site(self.brief, self.directory.name)
        original = (site / 'site.json').read_bytes()
        with self.assertRaises(FileExistsError):
            creator.create_site(self.brief, self.directory.name)
        self.assertEqual((site / 'site.json').read_bytes(), original)

    def test_unsafe_brief_is_rejected_without_creating_site(self):
        for changes in [{'slug': '../existing'}, {'contact': 'javascript:alert(1)'},
                        {'name': ''}, {'slug': 'Bad Name'}]:
            with self.subTest(changes=changes), self.assertRaises(ValueError):
                creator.create_site({**self.brief, **changes}, self.directory.name)
        self.assertEqual(list(Path(self.directory.name).iterdir()), [])
