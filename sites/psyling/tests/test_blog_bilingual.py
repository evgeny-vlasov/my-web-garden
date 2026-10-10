import os
import sys
import tempfile
import unittest
from datetime import datetime, timedelta


SITE_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
REPO_ROOT = os.path.abspath(os.path.join(SITE_ROOT, '../..'))
sys.path.insert(0, SITE_ROOT)
sys.path.insert(0, REPO_ROOT)

os.environ['FLASK_ENV'] = 'development'
os.environ['DATABASE_URL'] = f"sqlite:///{os.path.join(tempfile.gettempdir(), 'psyling_blog_tests.sqlite')}"
os.environ['SECRET_KEY'] = 'test-secret'
os.environ['SITE_DOMAIN'] = 'psyling.com'

import app as site_app  # noqa: E402
from jinja2 import ChoiceLoader, FileSystemLoader  # noqa: E402
from shared.base_app import db  # noqa: E402
from shared.models import BlogPost, User  # noqa: E402

site_app.app.jinja_loader = ChoiceLoader([
    FileSystemLoader(os.path.join(SITE_ROOT, 'templates')),
    FileSystemLoader(os.path.join(REPO_ROOT, 'shared', 'templates')),
])


class BilingualBlogTest(unittest.TestCase):
    def setUp(self):
        self.app = site_app.app
        self.app.config.update(TESTING=True, WTF_CSRF_ENABLED=False, RATELIMIT_ENABLED=False)
        self.ctx = self.app.app_context()
        self.ctx.push()
        db.drop_all()
        db.create_all()
        self.client = self.app.test_client()
        self.admin = User(username='editor', email='editor@example.com', role='admin')
        self.admin.set_password('password')
        db.session.add(self.admin)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.ctx.pop()

    def post(self, title, slug, language='en', visible=True, age=0):
        post = BlogPost(
            title=title, slug=slug, content=f'<p>{title} body text</p>',
            language=language, visible=visible, author_id=self.admin.id,
            published_at=datetime.utcnow() - timedelta(days=age) if visible else None,
        )
        db.session.add(post)
        db.session.commit()
        return post

    def login(self):
        with self.client.session_transaction() as session:
            session['_user_id'] = str(self.admin.id)
            session['_fresh'] = True

    def test_blog_archive_renders_all_and_only_published_posts(self):
        self.post('Published English', 'published-en')
        self.post('Опубликовано', 'published-ru', 'ru', age=1)
        self.post('Private draft', 'draft', visible=False)
        response = self.client.get('/blog')
        html = response.get_data(as_text=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Published English', html)
        self.assertIn('Опубликовано', html)
        self.assertNotIn('Private draft', html)

    def test_homepage_is_prominent_post_feed(self):
        for index in range(5):
            self.post(f'Homepage story {index}', f'home-{index}', age=index)
        html = self.client.get('/').get_data(as_text=True)
        self.assertIn('Psyling Journal', html)
        self.assertEqual(html.count('data-blog-story'), 5)
        self.assertLess(html.index('Homepage story 0'), html.index('The practice'))

    def test_post_language_and_linked_versions_render_and_switch(self):
        english = self.post('English article', 'english', 'en')
        russian = self.post('Русская статья', 'russian', 'ru')
        english.translation = russian
        db.session.commit()
        response = self.client.get('/post/english')
        html = response.get_data(as_text=True)
        self.assertEqual(english.language, 'en')
        self.assertIn('Русский', html)
        self.assertIn('/post/russian', html)
        self.assertIn('hreflang="ru"', html)

    def test_missing_language_is_placeholder_without_empty_post(self):
        self.post('English only', 'english-only', 'en')
        html = self.client.get('/post/english-only').get_data(as_text=True)
        self.assertIn('Русская версия готовится', html)
        self.assertEqual(BlogPost.query.count(), 1)

        russian = self.post('Только по-русски', 'russian-only', 'ru')
        html = self.client.get(f'/post/{russian.slug}').get_data(as_text=True)
        self.assertIn('English version is being prepared', html)

    def test_draft_counterpart_remains_a_public_placeholder(self):
        english = self.post('Public side', 'public-side', 'en')
        russian = self.post('Draft side', 'draft-side', 'ru', visible=False)
        english.translation = russian
        db.session.commit()
        html = self.client.get('/post/public-side').get_data(as_text=True)
        self.assertIn('Русская версия готовится', html)
        self.assertNotIn('href="/post/draft-side"', html)

    def test_unlinked_existing_post_still_renders(self):
        self.post('Legacy article', 'legacy')
        response = self.client.get('/post/legacy')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Legacy article', response.get_data(as_text=True))

    def test_admin_identifies_language_and_counterpart_status(self):
        english = self.post('Admin English', 'admin-en', 'en')
        russian = self.post('Admin Russian Draft', 'admin-ru', 'ru', visible=False)
        english.translation = russian
        db.session.commit()
        self.login()
        list_html = self.client.get('/admin/posts').get_data(as_text=True)
        self.assertIn('EN · English', list_html)
        self.assertIn('RU · Draft', list_html)
        edit_html = self.client.get(f'/admin/posts/{english.id}/edit').get_data(as_text=True)
        self.assertIn('English · editing', edit_html)
        self.assertIn('Русский · draft', edit_html)

    def test_translation_link_rejects_self_same_language_and_existing_pair(self):
        english = self.post('English one', 'english-one', 'en')
        other_english = self.post('English two', 'english-two', 'en')
        russian = self.post('Russian one', 'russian-one', 'ru')
        other_russian = self.post('Russian two', 'russian-two', 'ru')

        with self.assertRaises(ValueError):
            site_app.link_post_translation(english, english.id)
        with self.assertRaises(ValueError):
            site_app.link_post_translation(english, other_english.id)

        site_app.link_post_translation(english, russian.id)
        db.session.commit()
        with self.assertRaises(ValueError):
            site_app.link_post_translation(other_russian, english.id)

        db.session.refresh(english)
        db.session.refresh(russian)
        self.assertEqual(english.counterpart, russian)
        self.assertEqual(russian.counterpart, english)
        self.assertIsNone(other_russian.counterpart)


if __name__ == '__main__':
    unittest.main()
