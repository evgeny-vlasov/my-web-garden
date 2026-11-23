import io
from pathlib import Path
from tempfile import TemporaryDirectory
from types import SimpleNamespace
import unittest
from unittest.mock import Mock, patch

from flask import Flask
import requests
from werkzeug.datastructures import FileStorage
from PIL import Image

from shared.base_app import create_base_app
from shared.chat_proxy import forward_chat
from shared.image_handler import save_image


class PlatformTests(unittest.TestCase):
    def test_site_configuration_survives_factory_initialization(self):
        class Config:
            SECRET_KEY = 'test-only'
            SQLALCHEMY_DATABASE_URI = 'sqlite://'
            SESSION_COOKIE_SECURE = False
            PERMANENT_SESSION_LIFETIME = 42
            MAIL_USE_TLS = False
            SITE_NAME = 'Configured site'
            MAX_CONTENT_LENGTH = 1024
            UPLOAD_FOLDER = None
        app = create_base_app('psyling', Config)
        self.assertEqual(Path(app.root_path).name, 'psyling')
        self.assertIsNotNone(app.jinja_loader.get_source(app.jinja_env, 'about.html'))
        self.assertFalse(app.config['SESSION_COOKIE_SECURE'])
        self.assertEqual(app.config['PERMANENT_SESSION_LIFETIME'], 42)
        self.assertFalse(app.config['MAIL_USE_TLS'])
        self.assertEqual(app.config['MAX_CONTENT_LENGTH'], 1024)
        self.assertEqual(app.config['SITE_NAME'], 'Configured site')
        self.assertTrue(app.config['UPLOAD_FOLDER'].endswith('/psyling'))

    def test_custom_error_files_preserve_error_status(self):
        app = create_base_app('shared', SimpleNamespace(
            SECRET_KEY='test-only', SQLALCHEMY_DATABASE_URI='sqlite://',
            TESTING=True, PROPAGATE_EXCEPTIONS=False,
        ))
        @app.get('/failure')
        def failure():
            raise RuntimeError('Test failure')
        with TemporaryDirectory() as directory:
            app.static_folder = directory
            errors = Path(directory) / 'errors'
            errors.mkdir()
            (errors / '404.html').write_text('Missing')
            (errors / '500.html').write_text('Failed')
            client = app.test_client()
            self.assertEqual(client.get('/missing').status_code, 404)
            self.assertEqual(client.get('/failure').status_code, 500)

    def test_image_failure_before_file_creation_is_handled(self):
        image = FileStorage(stream=io.BytesIO(b'invalid'), filename='image.jpg')
        with patch('shared.image_handler.os.makedirs', side_effect=PermissionError):
            self.assertIsNone(save_image(image, '/unwritable'))

    def test_production_rejects_the_development_secret(self):
        with self.assertRaisesRegex(RuntimeError, 'SECRET_KEY'):
            create_base_app('psyling', SimpleNamespace(
                FLASK_ENV='production', SECRET_KEY='dev-secret-key-CHANGE-IN-PRODUCTION',
                SQLALCHEMY_DATABASE_URI='sqlite://',
            ))

    def test_image_upload_and_thumbnail_are_readable(self):
        stream = io.BytesIO()
        Image.new('RGBA', (2500, 1000), (30, 100, 80, 128)).save(stream, format='PNG')
        stream.seek(0)
        with TemporaryDirectory() as directory:
            result = save_image(FileStorage(stream=stream, filename='photo.png'), directory,
                                create_thumbnail=True)
            self.assertIsNotNone(result)
            with Image.open(result['filepath']) as image:
                self.assertEqual(image.size, (2000, 800))
            with Image.open(result['thumbnail_path']) as image:
                self.assertEqual(image.size, (300, 120))


class ChatBridgeTests(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.add_url_rule('/api/chat', view_func=lambda: forward_chat(
            'http://127.0.0.1:18081/api/chat'
        ), methods=['POST'])
        self.client = self.app.test_client()

    @patch('shared.chat_proxy.requests.post')
    def test_invalid_inputs_do_not_reach_backend(self, post):
        for data in [[], {}, {'message': []}, {'message': 'x' * 1001},
                     {'message': 'hello', 'conversation_history': [{'role': [], 'content': 'x'}]}]:
            with self.subTest(data=data):
                self.assertEqual(self.client.post('/api/chat', json=data).status_code, 400)
        post.assert_not_called()

    @patch('shared.chat_proxy.requests.post')
    def test_reply_and_session_contract(self, post):
        post.return_value = Mock(status_code=200, json=Mock(return_value={'response': 'Hello'}))
        response = self.client.post('/api/chat', json={'message': ' Hi ', 'session_id': 'session'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['response'], 'Hello')
        payload = post.call_args.kwargs['json']
        self.assertEqual(payload['message'], 'Hi')
        self.assertEqual(payload['session_id'], 'session')

    @patch('shared.chat_proxy.requests.post', side_effect=requests.ConnectionError('private backend URL'))
    def test_failure_hides_backend_details(self, post):
        response = self.client.post('/api/chat', json={'message': 'Hello'})
        self.assertEqual(response.status_code, 503)
        self.assertNotIn(b'private backend', response.data)
