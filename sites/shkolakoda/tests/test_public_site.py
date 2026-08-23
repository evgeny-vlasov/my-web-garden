import re
import sys
import unittest
from collections import Counter, defaultdict
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit

SITE_ROOT = Path(__file__).resolve().parents[1]
if str(SITE_ROOT) not in sys.path:
    sys.path.insert(0, str(SITE_ROOT))

from app import PROGRAMS, app, public_paths
from blog_content import BLOG_CATEGORIES, BLOG_POSTS
from curriculum import LESSONS, TOPICS
from project_library import PROJECTS


class PageParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ids = []
        self.hrefs = []
        self.images = []
        self.headings = []
        self.title_parts = []
        self.public_text_parts = []
        self.public_attributes = []
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
        if tag == "img":
            self.images.append(attributes)
        for name in ("alt", "aria-label", "placeholder", "title", "value"):
            if attributes.get(name):
                self.public_attributes.append(attributes[name])
        if tag == "meta" and attributes.get("content"):
            self.public_attributes.append(attributes["content"])
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
        self.public_text_parts.append(data)
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
        self.assertEqual(PROGRAMS["roblox"]["status"], "Coming later")
        self.assertEqual(PROGRAMS["ai"]["status"], "Coming later")

    def test_curriculum_records_are_complete_and_honest(self):
        self.assertEqual({topic["status"] for topic in TOPICS.values()}, {"Topic Guide"})

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
                    self.assertEqual(project["status"], "Coming later")
                    self.assertEqual(project["status_class"], "later")
                else:
                    self.assertNotEqual(project["status_class"], "later")

        led_page = self.client.get("/projects/led-traffic-light").get_data(as_text=True)
        self.assertIn("Suggested build order", led_page)
        self.assertNotIn("Computer Lab character", led_page)

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
        stylesheet = self.client.get("/static/css/styles.css")
        self.assertEqual(stylesheet.status_code, 200)
        self.assertIn("text/css", stylesheet.content_type)
        stylesheet.close()

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

    def test_internal_asset_language_is_not_rendered_publicly(self):
        forbidden = (
            "authorized",
            "reference-based",
            "reconstructed campaign",
            "campaign image",
            "provenance",
            "metadata",
            "rights confirmation",
            "workshop derivative",
            "current cohort",
            "historical workshop photograph",
            "production pilot",
            "provisional school of code",
            "public project",
            "public lesson",
            "public gallery",
            "curriculum direction",
            "topic connection",
            "cross-program topic",
            "ready to explore",
            "returns later",
            "complete project and downloads",
            "curriculum examples for now",
            "available later",
            "guided class project",
            "guided demonstration",
            "full learning path",
            "lesson outline",
            "published project",
        )
        pages = {**self.pages}
        response = self.client.get("/404")
        parser = PageParser()
        body = response.get_data(as_text=True).lower()
        parser.feed(body)
        pages["/404"] = (response, parser)

        try:
            for path, (_, page_parser) in pages.items():
                rendered = " ".join(
                    [*page_parser.public_text_parts, *page_parser.public_attributes]
                ).lower()
                for term in forbidden:
                    with self.subTest(path=path, term=term):
                        self.assertNotIn(term, rendered)
        finally:
            response.close()

    def test_empty_campaign_index_is_hidden_and_non_indexable(self):
        self.assertNotIn("/campaigns", self.paths)

        for path, (_, parser) in self.pages.items():
            with self.subTest(path=path):
                self.assertNotIn("/campaigns", parser.hrefs)
                rendered = " ".join(parser.public_text_parts).lower()
                self.assertNotIn("build collections", rendered)
                self.assertNotIn("no build collections yet", rendered)

        response = self.client.get("/campaigns")
        try:
            self.assertEqual(response.status_code, 200)
            body = response.get_data(as_text=True)
            self.assertIn('<meta name="robots" content="noindex,follow">', body)
            self.assertIn("No build collections yet", body)
        finally:
            response.close()

        sitemap = self.client.get("/sitemap.xml")
        try:
            self.assertNotIn("/campaigns", sitemap.get_data(as_text=True))
        finally:
            sitemap.close()

    def test_no_duplicate_ids_or_empty_links(self):
        for path, (_, parser) in self.pages.items():
            with self.subTest(path=path):
                duplicates = [identifier for identifier, count in Counter(parser.ids).items() if count > 1]
                self.assertEqual(duplicates, [])
                self.assertNotIn("", parser.hrefs)
                self.assertNotIn("#", parser.hrefs)

    def test_internal_links_and_fragments(self):
        known_paths = set(self.paths) | {"/robots.txt", "/sitemap.xml", "/favicon.svg"}
        known_paths.update(
            download["url"]
            for project in PROJECTS.values()
            for download in project.get("downloads", [])
        )
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

    def test_images_are_accessible_local_and_intrinsically_sized(self):
        for source_path, (_, parser) in self.pages.items():
            for image in parser.images:
                with self.subTest(source=source_path, image=image.get("src")):
                    self.assertIn("alt", image)
                    self.assertTrue(image.get("src"))
                    split = urlsplit(image["src"])
                    self.assertFalse(split.scheme)
                    self.assertFalse(split.netloc)
                    self.assertTrue(split.path.startswith("/static/"))
                    self.assertGreater(int(image.get("width", 0)), 0)
                    self.assertGreater(int(image.get("height", 0)), 0)
                    response = self.client.get(split.path)
                    self.assertEqual(response.status_code, 200)
                    self.assertTrue(response.content_type.startswith("image/"))
                    response.close()

    def test_shared_visual_instruments_follow_content_types(self):
        home = self.client.get("/").get_data(as_text=True)
        projects = self.client.get("/projects").get_data(as_text=True)
        programs = self.client.get("/programs").get_data(as_text=True)
        topics = self.client.get("/topics").get_data(as_text=True)
        blog = self.client.get("/blog").get_data(as_text=True)

        self.assertEqual(home.count("robot-avatar-96.png"), 1)
        self.assertIn("home-hero-1600.jpg", home)
        self.assertIn("hero-status-line", home)
        self.assertIn("lab-transition-mascot", home)
        for program in ("scratch", "robotics", "roblox", "ai"):
            with self.subTest(program=program):
                self.assertIn(f"project-card-{program}", projects)
                self.assertIn(f"program-card-{program}", programs)
        self.assertEqual(
            projects.count('class="project-instrument"'), len(PROJECTS)
        )
        self.assertEqual(
            programs.count('class="program-instrument"'), len(PROGRAMS)
        )
        rendered_blog_cards = len(
            re.findall(r'<article class="blog-card\b', blog)
        )
        self.assertEqual(
            blog.count('class="blog-card-instrument"'),
            rendered_blog_cards,
        )
        self.assertGreaterEqual(rendered_blog_cards, len(BLOG_POSTS))
        self.assertIn("connection-list", topics)
        self.assertIn("page-hero-library", topics)

    def test_visual_instruments_have_tablet_and_mobile_contracts(self):
        css = (SITE_ROOT / "static" / "css" / "styles.css").read_text(
            encoding="utf-8"
        )
        tablet = re.search(
            r"@media \(max-width: 820px\)(.*?)@media \(max-width: 640px\)",
            css,
            re.DOTALL,
        )
        mobile = re.search(
            r"@media \(max-width: 640px\)(.*?)"
            r"@media \(prefers-reduced-motion: reduce\)",
            css,
            re.DOTALL,
        )
        self.assertIsNotNone(tablet)
        self.assertIsNotNone(mobile)
        self.assertIn(".lab-transition", tablet.group(1))
        for selector in (
            ".board-mascot",
            ".project-instrument",
            ".filter-links",
            ".category-nav",
        ):
            with self.subTest(selector=selector):
                self.assertIn(selector, mobile.group(1))

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
