import json
import sys
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path


SITE_ROOT = Path(__file__).resolve().parents[1]
if str(SITE_ROOT) not in sys.path:
    sys.path.insert(0, str(SITE_ROOT))

import app as app_module
from publishing import CONTENT, DEFAULT_SCHEMA_PATH, ContentRepository, ContentValidationError


PAST = "2026-01-01T00:00:00Z"
FUTURE = "2036-01-01T00:00:00Z"


def common_record(kind, stable_id, slug, status="published", publish_at=PAST):
    prefix = {"campaign": "/campaigns/", "article": "/blog/", "project": "/projects/"}.get(kind)
    title = f"Test publication {slug}"
    return {
        "schema_version": 1,
        "kind": kind,
        "id": stable_id,
        "slug": slug,
        "title": title,
        "summary": f"A sufficiently detailed summary for the test publication named {slug}.",
        "status": status,
        "publish_at": publish_at,
        "topics": ["Testing"],
        "categories": ["Computer Lab Notes"],
        "seo": {
            "title": f"{title} | School of Code",
            "description": f"A sufficiently detailed search description for the School of Code test publication named {slug}.",
            **({"canonical_path": f"{prefix}{slug}"} if prefix else {}),
        },
        "internal_links": [],
        "image": None,
        "related": {},
        "campaign_id": None,
    }


def project_record(stable_id="test.project.alpha", slug="alpha-project", **overrides):
    record = common_record("project", stable_id, slug)
    record.update(
        {
            "body": [
                {
                    "heading": "Build the test system",
                    "paragraphs": ["This paragraph is long enough to describe a useful project publication test system."],
                }
            ],
            "project": {
                "program_key": "scratch",
                "program": "Scratch & Game Design",
                "project_type": "General Project Page",
                "difficulty": "Builder",
                "estimated_time": "45 minutes",
            },
        }
    )
    record.update(overrides)
    return record


def article_record(stable_id="test.article.alpha", slug="alpha-article", **overrides):
    record = common_record("article", stable_id, slug)
    record.update(
        {
            "author": "School of Code",
            "body": [
                {
                    "heading": "Inspect the practical question",
                    "paragraphs": ["This paragraph is long enough to describe a useful article publication test question."],
                }
            ],
        }
    )
    record.update(overrides)
    return record


def campaign_record(stable_id="test.campaign.alpha", slug="alpha-campaign", **overrides):
    record = common_record("campaign", stable_id, slug)
    record.update(
        {
            "body": [
                {
                    "heading": "Follow the campaign path",
                    "paragraphs": ["This paragraph is long enough to describe a useful campaign publication test path."],
                }
            ]
        }
    )
    record.update(overrides)
    return record


class RepositoryFixture:
    def __init__(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.content = self.root / "content"
        self.static = self.root / "static"
        for directory in ("campaigns", "articles", "projects", "media"):
            (self.content / directory).mkdir(parents=True, exist_ok=True)
        self.static.mkdir()

    def close(self):
        self.temporary.cleanup()

    def write(self, directory, filename, record):
        path = self.content / directory / filename
        path.write_text(json.dumps(record), encoding="utf-8")
        return path

    def load(self):
        return ContentRepository.load(
            content_root=self.content,
            scratch_root=None,
            schema_path=DEFAULT_SCHEMA_PATH,
            static_root=self.static,
        )


class ContentValidationTest(unittest.TestCase):
    def setUp(self):
        self.fixture = RepositoryFixture()

    def tearDown(self):
        self.fixture.close()

    def test_schema_errors_stop_discovery(self):
        record = project_record()
        del record["summary"]
        self.fixture.write("projects", "invalid.json", record)
        with self.assertRaises(ContentValidationError):
            self.fixture.load()

    def test_duplicate_ids_and_slugs_are_rejected(self):
        first = project_record()
        second = project_record(stable_id="test.project.second")
        self.fixture.write("projects", "one.json", first)
        self.fixture.write("projects", "two.json", second)
        with self.assertRaisesRegex(ContentValidationError, "Duplicate project slug"):
            self.fixture.load()

        self.fixture.close()
        self.fixture = RepositoryFixture()
        second = project_record(stable_id=first["id"], slug="second-project")
        self.fixture.write("projects", "one.json", first)
        self.fixture.write("projects", "two.json", second)
        with self.assertRaisesRegex(ContentValidationError, "Duplicate content id"):
            self.fixture.load()

    def test_missing_media_record_and_file_are_rejected(self):
        record = project_record(image={"media_id": "test.media.missing", "alt": "Missing example artwork"})
        self.fixture.write("projects", "project.json", record)
        with self.assertRaisesRegex(ContentValidationError, "missing media id"):
            self.fixture.load()

        self.fixture.close()
        self.fixture = RepositoryFixture()
        media = common_record("media", "test.media.missing-file", "missing-file")
        media.update(
            {
                "path": "publishing/missing.svg",
                "media_type": "image/svg+xml",
                "alt": "Missing example artwork",
                "credit": None,
            }
        )
        self.fixture.write("media", "media.json", media)
        with self.assertRaisesRegex(ContentValidationError, "missing media file"):
            self.fixture.load()

    def test_invalid_internal_links_and_related_records_are_rejected(self):
        record = project_record()
        record["internal_links"] = [{"label": "Missing page", "target_id": "test.article.missing"}]
        self.fixture.write("projects", "project.json", record)
        with self.assertRaisesRegex(ContentValidationError, "invalid internal link target"):
            self.fixture.load()

        self.fixture.close()
        self.fixture = RepositoryFixture()
        record = project_record()
        record["related"] = {"lessons": ["missing-lesson"]}
        self.fixture.write("projects", "project.json", record)
        repository = self.fixture.load()
        with self.assertRaisesRegex(ContentValidationError, "invalid related lesson"):
            repository.validate_route_compatibility()

    def test_unsafe_media_and_canonical_paths_are_rejected(self):
        media = common_record("media", "test.media.unsafe", "unsafe-media")
        media.update(
            {
                "path": "../outside.svg",
                "media_type": "image/svg+xml",
                "alt": "Unsafe example artwork",
                "credit": None,
            }
        )
        self.fixture.write("media", "media.json", media)
        with self.assertRaisesRegex(ContentValidationError, "unsafe media path"):
            self.fixture.load()

        self.fixture.close()
        self.fixture = RepositoryFixture()
        record = project_record()
        record["seo"]["canonical_path"] = "/projects/../private"
        self.fixture.write("projects", "project.json", record)
        with self.assertRaises(ContentValidationError):
            self.fixture.load()

    def test_scheduled_and_public_visibility(self):
        records = [
            project_record("test.project.draft", "draft-project", status="draft", publish_at=None),
            project_record("test.project.scheduled-past", "scheduled-past", status="scheduled", publish_at=PAST),
            project_record("test.project.scheduled-future", "scheduled-future", status="scheduled", publish_at=FUTURE),
            project_record("test.project.published-past", "published-past", status="published", publish_at=PAST),
            project_record("test.project.published-future", "published-future", status="published", publish_at=FUTURE),
            project_record("test.project.archived", "archived-project", status="archived", publish_at=PAST),
        ]
        for record in records:
            self.fixture.write("projects", f"{record['slug']}.json", record)
        repository = self.fixture.load()
        now = datetime(2026, 7, 20, tzinfo=timezone.utc)
        self.assertEqual(
            {record["slug"] for record in repository.public("project", now)},
            {"scheduled-past", "published-past"},
        )
        self.assertIsNone(repository.public_by_slug("project", "draft-project", now))

    def test_route_collisions_with_legacy_content_are_rejected(self):
        self.fixture.write("projects", "project.json", project_record(slug="legacy-project"))
        repository = self.fixture.load()
        with self.assertRaisesRegex(ContentValidationError, "conflicts with an existing route"):
            repository.validate_route_compatibility(legacy_projects={"legacy-project"})


class PublishingRouteTest(unittest.TestCase):
    def test_default_repository_keeps_draft_campaign_private_and_pilot_compatible(self):
        app_module.app.config.update(TESTING=True)
        client = app_module.app.test_client()
        self.assertEqual(client.get("/campaigns").status_code, 200)
        self.assertEqual(client.get("/campaigns/sample-scratch-build-week").status_code, 404)
        self.assertNotIn("/campaigns/sample-scratch-build-week", app_module.public_paths())
        pilot = client.get("/projects/escape-from-the-giant-pigeon")
        self.assertEqual(pilot.status_code, 200)
        self.assertIn("Start Building", pilot.get_data(as_text=True))

    def test_valid_files_are_discovered_and_rendered_without_route_changes(self):
        fixture = RepositoryFixture()
        try:
            records = [
                ("projects", project_record(slug="automatically-discovered")),
                ("articles", article_record(slug="automatically-discovered")),
                ("campaigns", campaign_record(slug="automatically-discovered")),
            ]
            for directory, record in records:
                fixture.write(directory, f"{record['slug']}.json", record)
            repository = fixture.load()
            original = app_module.CONTENT
            app_module.CONTENT = repository
            try:
                client = app_module.app.test_client()
                expected = {
                    "/projects/automatically-discovered": "Build the test system",
                    "/blog/automatically-discovered": "Inspect the practical question",
                    "/campaigns/automatically-discovered": "Follow the campaign path",
                }
                for path, heading in expected.items():
                    with self.subTest(path=path):
                        response = client.get(path)
                        self.assertEqual(response.status_code, 200)
                        self.assertIn(heading, response.get_data(as_text=True))
                        self.assertIn(path, app_module.public_paths())
            finally:
                app_module.CONTENT = original
        finally:
            fixture.close()


if __name__ == "__main__":
    unittest.main()
