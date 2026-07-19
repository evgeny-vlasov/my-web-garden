from flask import Flask, render_template, send_from_directory

from curriculum import LESSONS, PROJECT_DETAILS, TOPICS


app = Flask(__name__)


PROGRAMS = {
    "scratch": {
        "name": "Scratch & Game Design",
        "short_name": "Scratch",
        "endpoint": "scratch",
        "status": "Active now",
        "status_class": "active",
        "summary": (
            "Beginner-friendly programming through games, animations, "
            "simulations, and interactive stories."
        ),
        "builds": "Games, animations, simulations, and interactive stories",
        "concepts": ["Events", "Coordinates", "Loops", "Conditions", "Variables"],
        "examples": ["Escape from the Giant Pigeon", "Astro-Chicken Rescue"],
    },
    "robotics": {
        "name": "Robotics",
        "short_name": "Robotics",
        "endpoint": "robotics",
        "status": "Active now",
        "status_class": "active",
        "summary": (
            "Command logic, sensors, simple electronics, and physical builds "
            "organized around Sense, Decide, Act."
        ),
        "builds": "Simulations, circuits, sensor challenges, and small physical systems",
        "concepts": ["Commands", "Sensors", "Conditions", "State", "Feedback"],
        "examples": ["Robot Maze Logic", "micro:bit Reaction Timer"],
    },
    "roblox": {
        "name": "Roblox Studio / Lua",
        "short_name": "Roblox",
        "endpoint": "roblox",
        "status": "Available later",
        "status_class": "later",
        "summary": (
            "A future bridge from visual programming to typed scripts, "
            "3D systems, and collaborative game worlds."
        ),
        "builds": "Scripted obstacles, interactive 3D spaces, and game systems",
        "concepts": ["Lua", "Functions", "Events", "3D space", "Game systems"],
        "examples": ["Disappearing Platform Factory", "Museum of Bad Traps"],
    },
    "ai": {
        "name": "AI & Smart Machines",
        "short_name": "AI",
        "endpoint": "ai",
        "status": "Available later",
        "status_class": "later",
        "summary": (
            "A practical, critical look at patterns, prompts, machine decisions, "
            "and where intelligent tools get things wrong."
        ),
        "builds": "Small experiments with prompts, patterns, games, images, and machines",
        "concepts": ["Patterns", "Prompts", "Classification", "Bias", "Verification"],
        "examples": ["Is This AI Guessing?", "Confidently Wrong Machine"],
    },
}


def curriculum_project_card(project_slug):
    project = PROJECT_DETAILS[project_slug]
    return {
        "name": project["name"],
        "program": "Scratch",
        "group": "Scratch",
        "topics": project["topics"][:4],
        "mission": project["card_summary"],
        "status": project["project_type"],
        "status_class": "active" if project["mode"] == "guided" else "lab",
        "endpoint": project["endpoint"],
        "project_type": project["project_type"],
        "difficulty": project["difficulty"],
        "estimated_time": project["estimated_time"],
    }


PROJECTS = [
    curriculum_project_card("escape-from-the-giant-pigeon"),
    curriculum_project_card("astro-chicken-rescue"),
    {
        "name": "The Floor Is Definitely Lava",
        "program": "Scratch",
        "group": "Scratch",
        "topics": ["Variables", "Sensing", "Game state"],
        "mission": "Turn a simple platform game into a rising-lava emergency with clear win and lose states.",
        "status": "Lab Project",
        "status_class": "lab",
    },
    {
        "name": "Attack of the Angry Snowballs",
        "program": "Scratch",
        "group": "Scratch",
        "topics": ["Clones", "Timing", "Score"],
        "mission": "Design an arcade defense game with waves, difficulty changes, and spectacular misses.",
        "status": "Active",
        "status_class": "active",
    },
    curriculum_project_card("grandmas-intergalactic-taxi"),
    {
        "name": "The Unreasonably Dangerous Elevator",
        "program": "Scratch",
        "group": "Scratch",
        "topics": ["Variables", "Debugging", "State"],
        "mission": "Program floors, doors, passengers, and failure modes in an elevator nobody should trust.",
        "status": "Demonstration",
        "status_class": "demo",
    },
    {
        "name": "Mutant Sandwich Maze",
        "program": "Scratch",
        "group": "Scratch",
        "topics": ["Movement", "Sensing", "Loops"],
        "mission": "Navigate a lunch-based labyrinth, collect ingredients, and detect walls without cheating.",
        "status": "Lab Project",
        "status_class": "lab",
    },
    {
        "name": "Robot Maze Logic",
        "program": "Robotics",
        "group": "Robotics and simple electronics",
        "topics": ["Commands", "Conditions", "State"],
        "mission": "Write and test a movement plan that can survive turns, obstacles, and changed assumptions.",
        "status": "Demonstration",
        "status_class": "demo",
    },
    {
        "name": "LED Traffic Light",
        "program": "Robotics",
        "group": "Robotics and simple electronics",
        "topics": ["Output", "Timing", "Loops"],
        "mission": "Build a clear light sequence, then improve it with pedestrian logic and timing rules.",
        "status": "Active",
        "status_class": "active",
    },
    {
        "name": "Button and Buzzer Alarm",
        "program": "Robotics",
        "group": "Robotics and simple electronics",
        "topics": ["Input", "Conditions", "Output"],
        "mission": "Connect an input to a decision and make the resulting alarm useful rather than merely loud.",
        "status": "Active",
        "status_class": "active",
    },
    {
        "name": "micro:bit Reaction Timer",
        "program": "Robotics",
        "group": "Robotics and simple electronics",
        "topics": ["Input", "Variables", "Timing"],
        "mission": "Measure reaction time, store results, and decide what makes a test fair.",
        "status": "Active",
        "status_class": "active",
    },
    {
        "name": "Robot Patrol Challenge",
        "program": "Robotics",
        "group": "Robotics and simple electronics",
        "topics": ["Movement", "Sensors", "Feedback"],
        "mission": "Plan a patrol, respond to obstacles, and compare simulation logic with physical behaviour.",
        "status": "Lab Project",
        "status_class": "lab",
    },
    {
        "name": "Robot Hamster Security System",
        "program": "Robotics",
        "group": "Robotics and simple electronics",
        "topics": ["Sensors", "Conditions", "Alarm"],
        "mission": "Detect suspicious movement and design a tiny security system with sensible false-alarm rules.",
        "status": "Lab Project",
        "status_class": "lab",
    },
    {
        "name": "Disappearing Platform Factory",
        "program": "Roblox / Lua",
        "group": "Available later",
        "topics": ["Lua", "Events", "3D space"],
        "mission": "Script a platform system that changes state without turning the whole level into chaos.",
        "status": "Available Later",
        "status_class": "later",
    },
    {
        "name": "Is This AI Guessing?",
        "program": "AI",
        "group": "Available later",
        "topics": ["Patterns", "Questions", "Verification"],
        "mission": "Test machine answers, collect mistakes, and learn when confidence is not evidence.",
        "status": "Available Later",
        "status_class": "later",
    },
]


LEARNING_PATH = [
    "Program",
    "Topic",
    "Lesson",
    "Guided Project",
    "Lab Project",
    "Parent Explanation",
    "Gallery / Blog",
]


def render_page(template_name, **context):
    return render_template(
        template_name,
        programs=PROGRAMS,
        projects=PROJECTS,
        topics=TOPICS,
        lessons=LESSONS,
        curriculum_projects=PROJECT_DETAILS,
        learning_path=LEARNING_PATH,
        **context,
    )


@app.get("/")
def home():
    featured_names = {
        "Escape from the Giant Pigeon",
        "The Floor Is Definitely Lava",
        "Robot Hamster Security System",
        "Grandma's Intergalactic Taxi",
    }
    featured_projects = [project for project in PROJECTS if project["name"] in featured_names]
    return render_page("home.html", featured_projects=featured_projects)


@app.get("/programs")
def programs():
    return render_page("programs.html")


@app.get("/programs/scratch")
def scratch():
    scratch_projects = [project for project in PROJECTS if project["group"] == "Scratch"]
    return render_page(
        "scratch.html",
        page_projects=scratch_projects,
        completed_topic=TOPICS["coordinates"],
        completed_lesson=LESSONS["coordinates-and-movement"],
        completed_projects=[
            PROJECT_DETAILS["escape-from-the-giant-pigeon"],
            PROJECT_DETAILS["grandmas-intergalactic-taxi"],
            PROJECT_DETAILS["astro-chicken-rescue"],
        ],
    )


@app.get("/topics/coordinates")
def coordinates_topic():
    return render_page(
        "topic_detail.html",
        topic=TOPICS["coordinates"],
        lesson=LESSONS["coordinates-and-movement"],
        related_projects=[
            PROJECT_DETAILS["escape-from-the-giant-pigeon"],
            PROJECT_DETAILS["grandmas-intergalactic-taxi"],
            PROJECT_DETAILS["astro-chicken-rescue"],
        ],
    )


@app.get("/lessons/coordinates-and-movement")
def coordinates_lesson():
    return render_page(
        "lesson_detail.html",
        lesson=LESSONS["coordinates-and-movement"],
        topic=TOPICS["coordinates"],
        guided_project=PROJECT_DETAILS["escape-from-the-giant-pigeon"],
        lab_projects=[
            PROJECT_DETAILS["grandmas-intergalactic-taxi"],
            PROJECT_DETAILS["astro-chicken-rescue"],
        ],
    )


def render_project(project_slug):
    return render_page(
        "project_detail.html",
        project=PROJECT_DETAILS[project_slug],
        topic=TOPICS["coordinates"],
        lesson=LESSONS["coordinates-and-movement"],
        related_projects=[
            project
            for slug, project in PROJECT_DETAILS.items()
            if slug != project_slug
        ],
    )


@app.get("/projects/escape-from-the-giant-pigeon")
def giant_pigeon_project():
    return render_project("escape-from-the-giant-pigeon")


@app.get("/projects/grandmas-intergalactic-taxi")
def grandmas_taxi_project():
    return render_project("grandmas-intergalactic-taxi")


@app.get("/projects/astro-chicken-rescue")
def astro_chicken_project():
    return render_project("astro-chicken-rescue")


@app.get("/programs/robotics")
def robotics():
    robotics_projects = [
        project for project in PROJECTS if project["group"] == "Robotics and simple electronics"
    ]
    return render_page("robotics.html", page_projects=robotics_projects)


@app.get("/programs/roblox")
def roblox():
    return render_page("roblox.html")


@app.get("/programs/ai")
def ai():
    return render_page("ai.html")


@app.get("/projects")
def projects():
    project_groups = [
        ("Scratch", [project for project in PROJECTS if project["group"] == "Scratch"]),
        (
            "Robotics and simple electronics",
            [project for project in PROJECTS if project["group"] == "Robotics and simple electronics"],
        ),
        (
            "Available later",
            [project for project in PROJECTS if project["group"] == "Available later"],
        ),
    ]
    return render_page("projects.html", project_groups=project_groups)


@app.get("/computer-lab")
def computer_lab():
    return render_page("computer_lab.html")


@app.get("/parents")
def parents():
    return render_page("parents.html")


@app.get("/method")
def method():
    return render_page("method.html")


@app.get("/contact")
def contact():
    return render_page("contact.html")


@app.get("/robots.txt")
def robots_txt():
    return send_from_directory(app.static_folder, "robots.txt", mimetype="text/plain")


@app.get("/favicon.svg")
def favicon_svg():
    return send_from_directory(app.static_folder, "favicon.svg", mimetype="image/svg+xml")


if __name__ == "__main__":
    app.run(debug=True)
