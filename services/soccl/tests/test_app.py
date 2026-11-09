import tempfile
import unittest
from pathlib import Path

from werkzeug.security import generate_password_hash

from app import create_app


class PublishingDeskTests(unittest.TestCase):
    def setUp(self):
        self.tempdir = tempfile.TemporaryDirectory()
        self.database = str(Path(self.tempdir.name) / "publisher.db")
        self.app = create_app(
            {
                "TESTING": True,
                "SECRET_KEY": "test-secret",
                "ADMIN_PASSWORD_HASH": generate_password_hash("correct horse"),
                "DATABASE": self.database,
                "SESSION_COOKIE_SECURE": False,
            }
        )
        self.client = self.app.test_client()

    def tearDown(self):
        self.tempdir.cleanup()

    def csrf(self):
        with self.client.session_transaction() as session:
            return session["csrf_token"]

    def login(self):
        self.client.get("/login")
        return self.client.post(
            "/login",
            data={"password": "correct horse", "csrf_token": self.csrf()},
            follow_redirects=True,
        )

    def test_health_is_public(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["service"], "soccl")

    def test_dashboard_requires_login(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login", response.location)

    def test_login_shows_seeded_queue(self):
        response = self.login()
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"A Computer Lab for Builders", response.data)
        self.assertIn(b"Escape from the Giant Pigeon", response.data)

    def test_wrong_password_is_rejected(self):
        self.client.get("/login")
        response = self.client.post(
            "/login",
            data={"password": "wrong", "csrf_token": self.csrf()},
            follow_redirects=True,
        )
        self.assertIn(b"password was not accepted", response.data)

    def test_new_post_and_review_transition(self):
        self.login()
        response = self.client.post(
            "/posts/new",
            data={
                "csrf_token": self.csrf(),
                "title": "Test post",
                "reason_to_exist": "It answers a real parent question.",
                "editorial_sentence": "A concrete project makes the idea visible.",
                "content_type": "routine_social",
                "approval_level": "green",
                "facebook_slot": "noon",
                "evidence_notes": "Based on a School of Code project.",
                "facebook_body": "A useful Facebook explanation.",
                "instagram_body": "A useful Instagram explanation.",
                "website_url": "https://shkolakoda.com/projects",
            },
            follow_redirects=True,
        )
        self.assertIn(b"Draft created", response.data)
        with self.app.app_context():
            from app import get_db

            post = get_db().execute("SELECT * FROM posts WHERE title = 'Test post'").fetchone()
            post_id = post["id"]
        response = self.client.post(
            f"/posts/{post_id}/state",
            data={"csrf_token": self.csrf(), "action": "submit_review"},
            follow_redirects=True,
        )
        self.assertIn(b"moved to review", response.data)

    def test_factual_post_requires_evidence_notes(self):
        self.login()
        response = self.client.post(
            "/posts/new",
            data={
                "csrf_token": self.csrf(),
                "title": "Research claim",
                "reason_to_exist": "Parents are asking about it.",
                "editorial_sentence": "The evidence needs a careful boundary.",
                "content_type": "factual_social",
                "approval_level": "amber",
                "facebook_slot": "morning",
                "evidence_notes": "",
                "facebook_body": "A claim.",
                "instagram_body": "A claim.",
                "website_url": "",
            },
            follow_redirects=True,
        )
        self.assertIn(b"need evidence notes", response.data)

    def test_legacy_database_gets_editorial_columns(self):
        import sqlite3

        legacy_dir = tempfile.TemporaryDirectory()
        self.addCleanup(legacy_dir.cleanup)
        legacy_db = str(Path(legacy_dir.name) / "legacy.db")
        connection = sqlite3.connect(legacy_db)
        connection.execute(
            """CREATE TABLE posts (
            id INTEGER PRIMARY KEY, title TEXT NOT NULL, facebook_body TEXT NOT NULL,
            instagram_body TEXT NOT NULL, website_url TEXT NOT NULL DEFAULT '',
            status TEXT NOT NULL, scheduled_at TEXT, created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL)"""
        )
        connection.commit()
        connection.close()
        migrated = create_app(
            {
                "TESTING": True,
                "SECRET_KEY": "test-secret",
                "ADMIN_PASSWORD_HASH": generate_password_hash("correct horse"),
                "DATABASE": legacy_db,
                "SESSION_COOKIE_SECURE": False,
            }
        )
        with migrated.app_context():
            from app import get_db

            columns = {row["name"] for row in get_db().execute("PRAGMA table_info(posts)")}
        self.assertIn("reason_to_exist", columns)
        self.assertIn("approval_level", columns)

    def test_publish_is_locked_without_channels(self):
        self.login()
        response = self.client.post(
            "/posts/1/publish",
            data={"csrf_token": self.csrf()},
            follow_redirects=True,
        )
        self.assertIn(b"locked until a social channel is connected", response.data)

    def test_csrf_is_required(self):
        self.login()
        response = self.client.post("/logout", data={})
        self.assertEqual(response.status_code, 400)


if __name__ == "__main__":
    unittest.main()
