from pathlib import Path
from xml.sax.saxutils import escape

from flask import Flask, Response, abort, render_template, send_from_directory

from blog_content import BLOG_CATEGORIES, BLOG_ORDER, BLOG_POSTS
from curriculum import (
    LESSON_ORDER,
    LESSONS,
    PROGRAM_LINKS,
    TOPIC_ORDER,
    TOPICS,
)
from project_library import PROJECT_ORDER, PROJECTS
from publishing import CONTENT


app = Flask(__name__)

SITE_URL = "https://shkolakoda.com"
SCRATCH_DOWNLOAD_MIME_TYPES = {
    ".sb3": "application/x.scratch.sb3",
    ".zip": "application/zip",
}


PROGRAMS = {
    "scratch": {
        **PROGRAM_LINKS["scratch"],
        "short_name": "Scratch",
        "endpoint": "scratch",
        "summary": "Beginner-friendly programming through original games, animations, simulations, and interactive stories.",
        "builds": "Playable games, animations, simulations, quizzes, and interactive stories",
        "concepts": ["Events", "Coordinates", "Loops", "Conditions", "Variables", "State"],
        "examples": ["Escape from the Giant Pigeon", "Attack of the Angry Snowballs"],
    },
    "robotics": {
        **PROGRAM_LINKS["robotics"],
        "short_name": "Robotics",
        "endpoint": "robotics",
        "summary": "Commands, sensors, simple electronics, simulations, and physical systems organized around Sense, Decide, Act.",
        "builds": "Robot logic, circuits, sensor challenges, microcontroller work, and small physical systems",
        "concepts": ["Commands", "Input", "Sensors", "Conditions", "State", "Feedback"],
        "examples": ["Robot Maze Logic", "micro:bit Reaction Timer"],
    },
    "roblox": {
        **PROGRAM_LINKS["roblox"],
        "short_name": "Roblox",
        "endpoint": "roblox",
        "summary": "A future bridge from visual programming to Lua, 3D objects, events, and larger game systems.",
        "builds": "Scripted obstacles, collectible systems, interactive 3D worlds, and simple NPC behaviour",
        "concepts": ["Lua", "Objects", "Properties", "Events", "Functions", "Game state"],
        "examples": ["Obby Basics", "Coin Collector World"],
    },
    "ai": {
        **PROGRAM_LINKS["ai"],
        "short_name": "AI",
        "endpoint": "ai",
        "summary": "A future practical and critical program about patterns, predictions, prompts, limits, and human judgment.",
        "builds": "Bounded experiments with patterns, prompts, games, images, robot decisions, and error evaluation",
        "concepts": ["Patterns", "Prediction", "Prompts", "Bias", "Verification", "Human judgment"],
        "examples": ["AI Guessing Game", "Chatbot Character Lab"],
    },
}


LEARNING_PATH = [
    "Program",
    "Topic",
    "Lesson",
    "Guided Project",
    "Lab Project",
    "Parent Explanation",
    "Gallery / Blog",
]


CONTENT.validate_route_compatibility(
    legacy_projects=PROJECTS,
    legacy_articles=BLOG_POSTS,
    legacy_lessons=LESSONS,
)


def ordered(mapping, order):
    return [mapping[slug] for slug in order]


def published_projects():
    projects = []
    for record in CONTENT.public("project"):
        if record.get("scratch_pilot"):
            continue
        metadata = record["project"]
        projects.append(
            {
                **CONTENT.present(record),
                "name": record["title"],
                "card_summary": record["summary"],
                "program_key": metadata["program_key"],
                "program": metadata["program"],
                "project_type": metadata["project_type"],
                "difficulty": metadata["difficulty"],
                "estimated_time": metadata["estimated_time"],
                "mode": "publication",
                "status": "Published project",
                "status_class": "active",
            }
        )
    return projects


def published_articles():
    articles = []
    for record in CONTENT.public("article"):
        categories = record.get("categories") or ["Computer Lab Notes"]
        articles.append(
            {
                **CONTENT.present(record),
                "description": record["summary"],
                "category": categories[0],
                "categories": categories,
                "meta_description": record["seo"]["description"],
                "author": record["author"],
            }
        )
    return articles


def all_projects():
    return [*ordered(PROJECTS, PROJECT_ORDER), *published_projects()]


def all_articles():
    return [*ordered(BLOG_POSTS, BLOG_ORDER), *published_articles()]


def related_publications(record):
    related = []
    for slug in record.get("related", {}).get("lessons", []):
        lesson = LESSONS.get(slug)
        if lesson:
            related.append({"title": lesson["title"], "label": "Lesson", "url": lesson["url"]})
    dynamic_projects = {item["slug"]: item for item in CONTENT.public("project")}
    for slug in record.get("related", {}).get("projects", []):
        if slug in PROJECTS:
            project = PROJECTS[slug]
            related.append({"title": project["name"], "label": "Project", "url": project["url"]})
        elif slug in dynamic_projects:
            project = dynamic_projects[slug]
            related.append({"title": project["title"], "label": "Project", "url": CONTENT.url_for(project)})
    dynamic_articles = {item["slug"]: item for item in CONTENT.public("article")}
    for slug in record.get("related", {}).get("articles", []):
        if slug in BLOG_POSTS:
            article = BLOG_POSTS[slug]
            related.append({"title": article["title"], "label": "Article", "url": article["url"]})
        elif slug in dynamic_articles:
            article = dynamic_articles[slug]
            related.append({"title": article["title"], "label": "Article", "url": CONTENT.url_for(article)})
    return related


def render_publication(record):
    publication = CONTENT.present(record)
    return render_page(
        "publication.html",
        publication=publication,
        related_publications=related_publications(record),
    )


def render_page(template_name, **context):
    project_list = all_projects()
    blog_list = all_articles()
    return render_template(
        template_name,
        programs=PROGRAMS,
        topics=TOPICS,
        topic_list=ordered(TOPICS, TOPIC_ORDER),
        lessons=LESSONS,
        lesson_list=ordered(LESSONS, LESSON_ORDER),
        projects=PROJECTS,
        project_list=project_list,
        blog_posts=BLOG_POSTS,
        blog_list=blog_list,
        blog_categories=BLOG_CATEGORIES,
        learning_path=LEARNING_PATH,
        site_url=SITE_URL,
        **context,
    )


@app.get("/")
def home():
    featured_slugs = [
        "escape-from-the-giant-pigeon",
        "attack-of-the-angry-snowballs",
        "robot-maze-logic",
        "robot-patrol-challenge",
        "grandmas-intergalactic-taxi",
        "astro-chicken-rescue",
    ]
    return render_page(
        "home.html",
        featured_projects=[PROJECTS[slug] for slug in featured_slugs],
        featured_posts=[BLOG_POSTS[slug] for slug in BLOG_ORDER[:3]],
    )


@app.get("/programs")
def programs():
    return render_page("programs.html")


@app.get("/programs/scratch")
def scratch():
    scratch_projects = [project for project in ordered(PROJECTS, PROJECT_ORDER) if project["program_key"] == "scratch"]
    scratch_topic_slugs = [
        "events-and-commands",
        "coordinates",
        "loops-and-repetition",
        "conditions-and-decisions",
        "variables-and-state",
        "sensing-and-collision",
        "debugging",
    ]
    return render_page(
        "scratch.html",
        page_projects=scratch_projects,
        program_topics=[TOPICS[slug] for slug in scratch_topic_slugs],
    )


@app.get("/programs/robotics")
def robotics():
    robotics_projects = [project for project in ordered(PROJECTS, PROJECT_ORDER) if project["program_key"] == "robotics"]
    robotics_topic_slugs = [
        "events-and-commands",
        "coordinates",
        "input-and-output",
        "sensors",
        "conditions-and-decisions",
        "loops-and-repetition",
        "variables-and-state",
        "feedback",
        "autonomy",
        "debugging",
    ]
    return render_page(
        "robotics.html",
        page_projects=robotics_projects,
        program_topics=[TOPICS[slug] for slug in robotics_topic_slugs],
    )


@app.get("/programs/roblox")
def roblox():
    return render_page(
        "roblox.html",
        page_projects=[project for project in ordered(PROJECTS, PROJECT_ORDER) if project["program_key"] == "roblox"],
    )


@app.get("/programs/ai")
def ai():
    return render_page(
        "ai.html",
        page_projects=[project for project in ordered(PROJECTS, PROJECT_ORDER) if project["program_key"] == "ai"],
    )


@app.get("/topics")
def topic_index():
    return render_page("topics.html")


@app.get("/topics/<slug>")
def topic_detail(slug):
    topic = TOPICS.get(slug)
    if topic is None:
        abort(404)
    lesson = LESSONS.get(topic.get("lesson_slug"))
    related_projects = [PROJECTS[project_slug] for project_slug in topic.get("related_projects", []) if project_slug in PROJECTS]
    related_topics = [TOPICS[topic_slug] for topic_slug in topic.get("related_topics", []) if topic_slug in TOPICS]
    return render_page(
        "topic_detail.html",
        topic=topic,
        lesson=lesson,
        related_projects=related_projects,
        related_topics=related_topics,
    )


@app.get("/lessons")
def lesson_index():
    return render_page("lessons.html")


@app.get("/lessons/<slug>")
def lesson_detail(slug):
    lesson = LESSONS.get(slug)
    if lesson is None:
        abort(404)
    topic = TOPICS[lesson["topic_slug"]]
    guided_project = PROJECTS.get(lesson.get("guided_project"))
    related_projects = [
        project
        for project in ordered(PROJECTS, PROJECT_ORDER)
        if project.get("lesson_slug") == slug and (guided_project is None or project["slug"] != guided_project["slug"])
    ][:3]
    return render_page(
        "lesson_detail.html",
        lesson=lesson,
        topic=topic,
        guided_project=guided_project,
        related_projects=related_projects,
    )


@app.get("/projects")
def project_index():
    projects = all_projects()
    return render_page(
        "projects.html",
        scratch_projects=[project for project in projects if project["program_key"] == "scratch"],
        robotics_projects=[project for project in projects if project["program_key"] == "robotics"],
        later_projects=[project for project in projects if project["program_key"] in {"roblox", "ai"}],
    )


@app.get("/projects/<slug>")
def project_detail(slug):
    project = PROJECTS.get(slug)
    if project is None:
        publication = CONTENT.public_by_slug("project", slug)
        if publication is None:
            abort(404)
        return render_publication(publication)
    lesson = LESSONS.get(project.get("lesson_slug"))
    related_topics = [TOPICS[topic_slug] for topic_slug in project.get("related_topics", []) if topic_slug in TOPICS]
    related_projects = [
        candidate
        for candidate in ordered(PROJECTS, PROJECT_ORDER)
        if candidate["slug"] != slug
        and candidate["program_key"] == project["program_key"]
        and set(candidate["topics"]) & set(project["topics"])
    ][:3]
    return render_page(
        "project_detail.html",
        project=project,
        lesson=lesson,
        related_topics=related_topics,
        related_projects=related_projects,
    )


@app.get("/projects/<slug>/downloads/<filename>")
def project_download(slug, filename):
    project = PROJECTS.get(slug)
    if project is None or filename not in {item["filename"] for item in project.get("downloads", [])}:
        abort(404)
    suffix = Path(filename).suffix.lower()
    return send_from_directory(
        Path(app.static_folder) / "projects" / slug,
        filename,
        as_attachment=True,
        download_name=filename,
        mimetype=SCRATCH_DOWNLOAD_MIME_TYPES.get(suffix, "application/octet-stream"),
    )


@app.get("/computer-lab")
def computer_lab():
    lab_projects = [project for project in ordered(PROJECTS, PROJECT_ORDER) if project["mode"] == "lab"]
    return render_page("computer_lab.html", lab_projects=lab_projects)


@app.get("/parents")
def parents():
    return render_page("parents.html")


@app.get("/method")
def method():
    return render_page("method.html")


@app.get("/blog")
def blog_index():
    posts = all_articles()
    categories = list(BLOG_CATEGORIES)
    categories.extend(
        category
        for post in posts
        for category in post.get("categories", [post["category"]])
        if category not in categories
    )
    category_groups = [
        (category, [post for post in posts if category in post.get("categories", [post["category"]])])
        for category in categories
    ]
    return render_page("blog.html", category_groups=category_groups, article_count=len(posts))


@app.get("/blog/<slug>")
def blog_post(slug):
    post = BLOG_POSTS.get(slug)
    if post is None:
        publication = CONTENT.public_by_slug("article", slug)
        if publication is None:
            abort(404)
        return render_publication(publication)
    related_posts = [candidate for candidate in ordered(BLOG_POSTS, BLOG_ORDER) if candidate["slug"] != slug and candidate["category"] == post["category"]][:3]
    return render_page("article.html", post=post, related_posts=related_posts)


@app.get("/campaigns")
def campaign_index():
    campaigns = [CONTENT.present(record) for record in CONTENT.public("campaign")]
    return render_page("campaigns.html", campaigns=campaigns)


@app.get("/campaigns/<slug>")
def campaign_detail(slug):
    campaign = CONTENT.public_by_slug("campaign", slug)
    if campaign is None:
        abort(404)
    return render_publication(campaign)


@app.get("/gallery")
def gallery():
    example_slugs = [
        "escape-from-the-giant-pigeon",
        "grandmas-intergalactic-taxi",
        "astro-chicken-rescue",
        "robot-maze-logic",
        "led-traffic-light",
        "microbit-reaction-timer",
    ]
    return render_page("gallery.html", example_projects=[PROJECTS[slug] for slug in example_slugs])


@app.get("/contact")
def contact():
    return render_page("contact.html")


def public_paths():
    paths = [
        "/",
        "/programs",
        "/programs/scratch",
        "/programs/robotics",
        "/programs/roblox",
        "/programs/ai",
        "/projects",
        "/topics",
        "/lessons",
        "/computer-lab",
        "/parents",
        "/method",
        "/blog",
        "/campaigns",
        "/gallery",
        "/contact",
    ]
    paths.extend(topic["url"] for topic in ordered(TOPICS, TOPIC_ORDER))
    paths.extend(lesson["url"] for lesson in ordered(LESSONS, LESSON_ORDER))
    paths.extend(project["url"] for project in ordered(PROJECTS, PROJECT_ORDER))
    paths.extend(post["url"] for post in ordered(BLOG_POSTS, BLOG_ORDER))
    paths.extend(CONTENT.url_for(record) for record in CONTENT.public() if record["kind"] != "media")
    return list(dict.fromkeys(paths))


@app.get("/sitemap.xml")
def sitemap_xml():
    urls = "".join(f"<url><loc>{escape(SITE_URL + path)}</loc></url>" for path in public_paths())
    xml = f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>'
    return Response(xml, mimetype="application/xml")


@app.get("/robots.txt")
def robots_txt():
    return send_from_directory(app.static_folder, "robots.txt", mimetype="text/plain")


@app.get("/favicon.svg")
def favicon_svg():
    return send_from_directory(app.static_folder, "favicon.svg", mimetype="image/svg+xml")


@app.get("/404")
def not_found_preview():
    abort(404)


@app.errorhandler(404)
def page_not_found(error):
    return render_page("404.html"), 404


if __name__ == "__main__":
    app.run(debug=True)
