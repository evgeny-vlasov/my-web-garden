import re
import unittest
from collections import Counter, defaultdict
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit

from app import PROGRAMS, app, public_paths
from blog_content import BLOG_CATEGORIES, BLOG_POSTS
from curriculum import LESSONS, TOPICS
from project_library import PROJECTS


SITE_ROOT = Path(__file__).resolve().parents[1]


class PageParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ids = []
        self.hrefs = []
        self.headings = []
        self.title_parts = []
        self.meta_description = None
        self.canonical = None
        self._in_title = False
        self._heading_level = None
        self._heading_parts = []

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        if "id" in attributes:
            self.ids.append(attributes["id"])
        if tag == "a" and "href" in attributes:
            self.hrefs.append(attributes["href"])
        if tag == "title":
            self._in_title = True
        if tag == "meta" and attributes.get("name", "").lower() == "description":
            self.meta_description = attributes.get("content")
        if tag == "link" and "canonical" in attributes.get("rel", "").split():
            self.canonical = attributes.get("href")
        if re.fullmatch(r"h[1-6]", tag):
            self._heading_level = int(tag[1])
            self._heading_parts = []

    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False
        if self._heading_level and tag == f"h{self._heading_level}":
            text = " ".join("".join(self._heading_parts).split())
            self.headings.append((self._heading_level, text))
            self._heading_level = None
            self._heading_parts = []

    def handle_data(self, data):
        if self._in_title:
            self.title_parts.append(data)
        if self._heading_level:
            self._heading_parts.append(data)

    @property
    def title(self):
        return " ".join("".join(self.title_parts).split())


class PublicSiteTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        app.config.update(TESTING=True)
        cls.client = app.test_client()
        cls.paths = public_paths()
        cls.pages = {}
        for path in cls.paths:
            response = cls.client.get(path)
            parser = PageParser()
            parser.feed(response.get_data(as_text=True))
            cls.pages[path] = (response, parser)

    def test_content_inventory(self):
        self.assertEqual(len(TOPICS), 11)
        self.assertEqual(len(LESSONS), 10)
        self.assertEqual(len(PROJECTS), 18)
        self.assertEqual(len(BLOG_POSTS), 16)
        self.assertEqual(
            set(BLOG_CATEGORIES),
            {
                "Coding for Kids",
                "Robotics for Kids",
                "AI for Kids",
                "Parent Guides",
                "Project-Based Learning",
                "Computer Lab Notes",
                "Calgary STEM Activities",
            },
        )

    def test_current_and_future_program_statuses(self):
        self.assertEqual(PROGRAMS["scratch"]["status"], "Active now")
        self.assertEqual(PROGRAMS["robotics"]["status"], "Active now")
        self.assertEqual(PROGRAMS["roblox"]["status"], "Available later")
        self.assertEqual(PROGRAMS["ai"]["status"], "Available later")

    def test_curriculum_records_are_complete_and_honest(self):
        for slug, topic in TOPICS.items():
            with self.subTest(topic=slug):
                for field in ("summary", "why_it_matters", "logic_kernel", "examples", "common_mistakes", "parent_note"):
                    self.assertTrue(topic[field])
                self.assertIn(topic["lesson_slug"], LESSONS)

        for slug, lesson in LESSONS.items():
            with self.subTest(lesson=slug):
                for field in (
                    "learning_goals",
                    "theory_examples",
                    "checkpoints",
                    "common_mistakes",
                    "challenge_levels",
                    "demonstration_questions",
                    "parent_summary",
                ):
                    self.assertTrue(lesson[field])
                self.assertIn(lesson["topic_slug"], TOPICS)
                self.assertIn(lesson["guided_project"], PROJECTS)

        for slug, project in PROJECTS.items():
            with self.subTest(project=slug):
                for field in (
                    "mission",
                    "what_students_build",
                    "what_students_learn",
                    "needs",
                    "test_questions",
                    "common_mistakes",
                    "challenge_levels",
                    "demonstrate",
                    "parent_explanation",
                    "related_topics",
                ):
                    self.assertTrue(project[field])
                if project["program_key"] in {"roblox", "ai"}:
                    self.assertEqual(project["status"], "Available later")
                    self.assertEqual(project["status_class"], "later")
                else:
                    self.assertNotEqual(project["status_class"], "later")

    def test_blog_posts_are_substantial_and_categories_are_used(self):
        used_categories = set()
        for slug, post in BLOG_POSTS.items():
            with self.subTest(post=slug):
                words = " ".join(
                    [post["introduction"], *(paragraph for _, paragraphs in post["sections"] for paragraph in paragraphs)]
                ).split()
                self.assertGreaterEqual(len(words), 450)
                self.assertGreaterEqual(len(post["sections"]), 5)
                self.assertTrue(post["related"])
            used_categories.update(post["categories"])
        self.assertEqual(set(BLOG_CATEGORIES) - used_categories, set())

    def test_every_public_page_returns_200(self):
        for path, (response, _) in self.pages.items():
            with self.subTest(path=path):
                self.assertEqual(response.status_code, 200)

    def test_infrastructure_routes(self):
        robots = self.client.get("/robots.txt")
        self.assertEqual(robots.status_code, 200)
        self.assertIn("Sitemap: https://shkolakoda.com/sitemap.xml", robots.get_data(as_text=True))
        robots.close()
        self.assertEqual(self.client.get("/sitemap.xml").status_code, 200)
        favicon = self.client.get("/favicon.svg")
        self.assertEqual(favicon.status_code, 200)
        favicon.close()

    def test_custom_404_and_retired_science_paths(self):
        for path in ("/404", "/not-a-public-page", "/camps", "/safety"):
            with self.subTest(path=path):
                response = self.client.get(path)
                self.assertEqual(response.status_code, 404)
                body = response.get_data(as_text=True)
                self.assertIn("Unknown coordinate", body)
                self.assertNotIn("day camp", body.lower())

    def test_titles_descriptions_and_canonicals_are_present_and_unique(self):
        titles = []
        descriptions = []
        for path, (_, parser) in self.pages.items():
            with self.subTest(path=path):
                self.assertTrue(parser.title)
                self.assertTrue(parser.meta_description)
                self.assertEqual(parser.canonical, f"https://shkolakoda.com{path}")
            titles.append(parser.title)
            descriptions.append(parser.meta_description)
        self.assertEqual([title for title, count in Counter(titles).items() if count > 1], [])
        self.assertEqual([description for description, count in Counter(descriptions).items() if count > 1], [])

    def test_heading_order_and_single_h1(self):
        for path, (_, parser) in self.pages.items():
            with self.subTest(path=path):
                levels = [level for level, text in parser.headings if text]
                self.assertEqual(levels.count(1), 1)
                self.assertEqual(levels[0], 1)
                for previous, current in zip(levels, levels[1:]):
                    self.assertLessEqual(current - previous, 1)

    def test_no_duplicate_ids_or_empty_links(self):
        for path, (_, parser) in self.pages.items():
            with self.subTest(path=path):
                duplicates = [identifier for identifier, count in Counter(parser.ids).items() if count > 1]
                self.assertEqual(duplicates, [])
                self.assertNotIn("", parser.hrefs)
                self.assertNotIn("#", parser.hrefs)

    def test_internal_links_and_fragments(self):
        known_paths = set(self.paths) | {"/robots.txt", "/sitemap.xml", "/favicon.svg"}
        for source_path, (_, parser) in self.pages.items():
            for href in parser.hrefs:
                split = urlsplit(href)
                if split.scheme in {"mailto", "tel"}:
                    continue
                if split.scheme in {"http", "https"}:
                    if split.netloc not in {"shkolakoda.com", "www.shkolakoda.com"}:
                        continue
                target_path = split.path or source_path
                with self.subTest(source=source_path, href=href):
                    self.assertIn(target_path, known_paths)
                    if target_path in self.pages and split.fragment:
                        self.assertIn(split.fragment, self.pages[target_path][1].ids)

    def test_every_content_page_has_an_internal_inbound_link(self):
        inbound = defaultdict(set)
        for source_path, (_, parser) in self.pages.items():
            for href in parser.hrefs:
                split = urlsplit(href)
                if split.scheme or not split.path:
                    continue
                inbound[split.path].add(source_path)
        content_paths = {
            *(topic["url"] for topic in TOPICS.values()),
            *(lesson["url"] for lesson in LESSONS.values()),
            *(project["url"] for project in PROJECTS.values()),
            *(post["url"] for post in BLOG_POSTS.values()),
        }
        self.assertEqual(sorted(path for path in content_paths if not inbound[path]), [])

    def test_source_content_integrity_terms(self):
        text = "\n".join(
            path.read_text(encoding="utf-8")
            for path in SITE_ROOT.rglob("*")
            if path.is_file()
            and "venv" not in path.parts
            and "__pycache__" not in path.parts
            and path.suffix in {".py", ".html", ".css", ".md", ".txt"}
            and path != Path(__file__)
        ).lower()
        for forbidden in (
            "daycamp@",
            "schoolofcode@vlasov.ca",
            "lorem ipsum",
            "unlock your potential",
            "future-ready learners",
            'href="#"',
        ):
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(forbidden, text)


if __name__ == "__main__":
    unittest.main()
