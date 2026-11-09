import hmac
import os
import secrets
import sqlite3
from datetime import datetime, timezone
from functools import wraps
from pathlib import Path
from zoneinfo import ZoneInfo

from flask import (
    Flask,
    abort,
    current_app,
    flash,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from werkzeug.security import check_password_hash


EDMONTON = ZoneInfo("America/Edmonton")
VALID_STATES = {"draft", "review", "approved", "scheduled", "published", "held"}
VALID_CONTENT_TYPES = {"routine_social", "factual_social", "website_article"}
VALID_APPROVAL_LEVELS = {"green", "amber", "red"}
VALID_FACEBOOK_SLOTS = {"morning", "noon", "evening", "flexible"}


def utc_now():
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY=os.environ.get("SOCCL_SECRET_KEY"),
        ADMIN_PASSWORD_HASH=os.environ.get("SOCCL_ADMIN_PASSWORD_HASH"),
        DATABASE=os.environ.get("SOCCL_DATABASE", "/var/lib/soccl/publisher.db"),
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE="Lax",
        SESSION_COOKIE_SECURE=os.environ.get("SOCCL_SECURE_COOKIE", "0") == "1",
        MAX_CONTENT_LENGTH=2 * 1024 * 1024,
    )
    if test_config:
        app.config.update(test_config)

    if not app.config.get("SECRET_KEY"):
        raise RuntimeError("SOCCL_SECRET_KEY is required")
    if not app.config.get("ADMIN_PASSWORD_HASH"):
        raise RuntimeError("SOCCL_ADMIN_PASSWORD_HASH is required")

    Path(app.config["DATABASE"]).parent.mkdir(parents=True, exist_ok=True)
    app.teardown_appcontext(close_db)

    with app.app_context():
        init_db()

    @app.before_request
    def protect_posts():
        if request.method == "POST":
            expected = session.get("csrf_token", "")
            supplied = request.form.get("csrf_token", "")
            if not expected or not hmac.compare_digest(expected, supplied):
                abort(400, "Invalid form token")

    @app.after_request
    def security_headers(response):
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Referrer-Policy"] = "same-origin"
        response.headers["Cache-Control"] = "no-store"
        return response

    @app.context_processor
    def template_helpers():
        token = session.setdefault("csrf_token", secrets.token_urlsafe(32))
        return {"csrf_token": token, "display_time": display_time}

    @app.get("/health")
    def health():
        return {"status": "ok", "service": "soccl"}

    @app.route("/login", methods=("GET", "POST"))
    def login():
        if session.get("authenticated"):
            return redirect(url_for("dashboard"))
        if request.method == "POST":
            password = request.form.get("password", "")
            if check_password_hash(app.config["ADMIN_PASSWORD_HASH"], password):
                session.clear()
                session["authenticated"] = True
                session["csrf_token"] = secrets.token_urlsafe(32)
                return redirect(url_for("dashboard"))
            flash("The password was not accepted.", "error")
        return render_template("login.html")

    @app.post("/logout")
    @login_required
    def logout():
        session.clear()
        return redirect(url_for("login"))

    @app.get("/")
    @login_required
    def dashboard():
        db = get_db()
        posts = db.execute(
            "SELECT * FROM posts ORDER BY CASE status "
            "WHEN 'review' THEN 0 WHEN 'approved' THEN 1 WHEN 'scheduled' THEN 2 "
            "WHEN 'draft' THEN 3 WHEN 'held' THEN 4 ELSE 5 END, updated_at DESC"
        ).fetchall()
        channels = db.execute("SELECT * FROM channels ORDER BY sort_order").fetchall()
        counts = {
            row["status"]: row["count"]
            for row in db.execute("SELECT status, COUNT(*) AS count FROM posts GROUP BY status")
        }
        featured = next(
            (post for post in posts if post["status"] in {"review", "approved", "scheduled"}),
            posts[0] if posts else None,
        )
        return render_template(
            "dashboard.html",
            posts=posts,
            channels=channels,
            counts=counts,
            featured=featured,
        )

    @app.route("/posts/new", methods=("GET", "POST"))
    @login_required
    def new_post():
        if request.method == "POST":
            values = validate_post_form(request.form)
            if values is not None:
                now = utc_now()
                db = get_db()
                cursor = db.execute(
                    """INSERT INTO posts
                    (title, reason_to_exist, editorial_sentence, content_type,
                     approval_level, facebook_slot, evidence_notes,
                     facebook_body, instagram_body, website_url, status,
                     scheduled_at, created_at, updated_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'draft', NULL, ?, ?)""",
                    (*values, now, now),
                )
                log_activity(db, cursor.lastrowid, "created", "Draft created")
                db.commit()
                flash("Draft created.", "success")
                return redirect(url_for("edit_post", post_id=cursor.lastrowid))
        return render_template("post_form.html", post=None)

    @app.route("/posts/<int:post_id>/edit", methods=("GET", "POST"))
    @login_required
    def edit_post(post_id):
        db = get_db()
        post = get_post_or_404(db, post_id)
        if request.method == "POST":
            values = validate_post_form(request.form)
            if values is not None:
                db.execute(
                    """UPDATE posts SET title = ?, reason_to_exist = ?,
                    editorial_sentence = ?, content_type = ?, approval_level = ?,
                    facebook_slot = ?, evidence_notes = ?, facebook_body = ?,
                    instagram_body = ?, website_url = ?, updated_at = ? WHERE id = ?""",
                    (*values, utc_now(), post_id),
                )
                log_activity(db, post_id, "edited", "Post copy updated")
                db.commit()
                flash("Changes saved.", "success")
                return redirect(url_for("edit_post", post_id=post_id))
        return render_template("post_form.html", post=post)

    @app.post("/posts/<int:post_id>/state")
    @login_required
    def change_state(post_id):
        db = get_db()
        post = get_post_or_404(db, post_id)
        action = request.form.get("action", "")
        target = {
            "submit_review": "review",
            "approve": "approved",
            "hold": "held",
            "return_draft": "draft",
        }.get(action)
        if action in {"submit_review", "approve"}:
            missing = editorial_gate_missing(post)
            if missing:
                flash("Editorial gate is incomplete: " + ", ".join(missing) + ".", "error")
                return redirect(url_for("edit_post", post_id=post_id))
        scheduled_at = None
        if action == "schedule":
            target = "scheduled"
            local_value = request.form.get("scheduled_at", "")
            try:
                local_dt = datetime.fromisoformat(local_value).replace(tzinfo=EDMONTON)
                scheduled_at = local_dt.astimezone(timezone.utc).replace(microsecond=0).isoformat()
            except ValueError:
                flash("Choose a valid Calgary date and time.", "error")
                return redirect(url_for("edit_post", post_id=post_id))
            if local_dt <= datetime.now(EDMONTON):
                flash("The scheduled time must be in the future.", "error")
                return redirect(url_for("edit_post", post_id=post_id))
        if target not in VALID_STATES:
            abort(400, "Unknown state transition")
        db.execute(
            "UPDATE posts SET status = ?, scheduled_at = ?, updated_at = ? WHERE id = ?",
            (target, scheduled_at, utc_now(), post_id),
        )
        log_activity(db, post_id, target, f"State changed from {post['status']} to {target}")
        db.commit()
        flash(f"Post moved to {target}.", "success")
        return redirect(url_for("dashboard"))

    @app.post("/posts/<int:post_id>/publish")
    @login_required
    def publish(post_id):
        db = get_db()
        get_post_or_404(db, post_id)
        connected = db.execute(
            "SELECT COUNT(*) AS count FROM channels WHERE name IN ('Facebook', 'Instagram') AND state = 'connected'"
        ).fetchone()["count"]
        if connected == 0:
            flash("Publishing is locked until a social channel is connected.", "error")
            return redirect(url_for("dashboard"))
        abort(501, "Social delivery adapter is not installed")

    @app.get("/calendar")
    @login_required
    def calendar():
        posts = get_db().execute(
            "SELECT * FROM posts WHERE status = 'scheduled' ORDER BY scheduled_at"
        ).fetchall()
        return render_template("calendar.html", posts=posts)

    @app.get("/channels")
    @login_required
    def channels():
        rows = get_db().execute("SELECT * FROM channels ORDER BY sort_order").fetchall()
        return render_template("channels.html", channels=rows)

    @app.get("/activity")
    @login_required
    def activity():
        rows = get_db().execute(
            """SELECT activity.*, posts.title FROM activity
            LEFT JOIN posts ON posts.id = activity.post_id
            ORDER BY activity.created_at DESC, activity.id DESC LIMIT 100"""
        ).fetchall()
        return render_template("activity.html", activity=rows)

    return app


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(current_app.config["DATABASE"])
        g.db.row_factory = sqlite3.Row
    return g.db


def close_db(_error=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    if "db" not in g:
        g.db = sqlite3.connect(current_app.config["DATABASE"])
        g.db.row_factory = sqlite3.Row
    db = g.db
    db.executescript(
        """
        PRAGMA journal_mode = WAL;
        PRAGMA foreign_keys = ON;
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            reason_to_exist TEXT NOT NULL DEFAULT '',
            editorial_sentence TEXT NOT NULL DEFAULT '',
            content_type TEXT NOT NULL DEFAULT 'routine_social',
            approval_level TEXT NOT NULL DEFAULT 'green',
            facebook_slot TEXT NOT NULL DEFAULT 'flexible',
            evidence_notes TEXT NOT NULL DEFAULT '',
            facebook_body TEXT NOT NULL,
            instagram_body TEXT NOT NULL,
            website_url TEXT NOT NULL DEFAULT '',
            status TEXT NOT NULL CHECK(status IN ('draft','review','approved','scheduled','published','held')),
            scheduled_at TEXT,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS channels (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL UNIQUE,
            handle TEXT NOT NULL DEFAULT '',
            state TEXT NOT NULL CHECK(state IN ('connected','disconnected','available')),
            detail TEXT NOT NULL DEFAULT '',
            sort_order INTEGER NOT NULL
        );
        CREATE TABLE IF NOT EXISTS activity (
            id INTEGER PRIMARY KEY,
            post_id INTEGER REFERENCES posts(id) ON DELETE SET NULL,
            action TEXT NOT NULL,
            detail TEXT NOT NULL,
            created_at TEXT NOT NULL
        );
        """
    )
    ensure_post_columns(db)
    db.executemany(
        "INSERT OR IGNORE INTO channels(name, handle, state, detail, sort_order) VALUES (?, ?, ?, ?, ?)",
        [
            ("Facebook", "@soccl", "disconnected", "Meta authorization will be added later", 1),
            ("Instagram", "@soccl", "disconnected", "Professional account connection required", 2),
            ("Website", "shkolakoda.com", "available", "Git-backed publishing is available", 3),
        ],
    )
    existing = db.execute("SELECT COUNT(*) AS count FROM posts").fetchone()["count"]
    if existing == 0:
        now = utc_now()
        seed_posts = [
            (
                "A Computer Lab for Builders",
                "Introduce the school through the concrete difference between using a computer and building with one.",
                "School of Code gives children a small, serious place to author systems rather than only consume technology.",
                "routine_social",
                "green",
                "evening",
                "School description; no external factual claim.",
                "School of Code Computer Lab is a small Calgary learning project for children who want to build with computers—not only use them. We begin with Scratch game design and robotics. Classes provide a path; labs provide room to alter, test, break, repair, and personalize the idea.\n\nThe class gives the idea. The lab gives the idea a life.\n\nhttps://shkolakoda.com",
                "A computer lab for builders.\n\nScratch games first. Robots beside them. Mathematics hiding inside movement, maps, sensors, scores, and spectacular mistakes.\n\nSchool of Code Computer Lab is being built in Calgary.\n\n#CalgaryKids #CodingForKids #ScratchProgramming #KidsRobotics",
                "https://shkolakoda.com",
                "review",
                None,
                now,
                now,
            ),
            (
                "Not All Screen Time Is the Same",
                "Answer a real parent concern without pretending that every computer activity is automatically educational.",
                "The useful distinction is not screen versus no screen, but passive consumption versus active authorship.",
                "factual_social",
                "amber",
                "morning",
                "Treat developmental claims cautiously; the linked article should carry sources and limitations.",
                "A child watching videos and a child building a game may be looking at the same screen, but they are not doing the same thing. Building asks for decisions, testing, debugging and explanation. The useful question is not simply whether there was a screen. It is whether the child was the author.",
                "Two children can look at the same kind of screen while doing completely different things. One consumes. One builds, tests, chooses, explains and repairs. A computer becomes educational when it becomes a workbench.\n\n#CreativeComputing #CodingForKids #CalgaryParents",
                "https://shkolakoda.com/blog/is-coding-class-just-more-screen-time",
                "draft",
                None,
                now,
                now,
            ),
            (
                "Escape from the Giant Pigeon",
                "Show parents and students how an absurd game premise carries precise programming ideas.",
                "The pigeon is absurd; the coordinate system, collision rules, and debugging are not.",
                "routine_social",
                "green",
                "noon",
                "Based on an existing School of Code project.",
                "Your spaceship has made an emergency landing in a city park. Unfortunately, the park belongs to a pigeon roughly the size of municipal infrastructure. Under the ridiculous emergency are serious ideas: coordinates, collision detection, conditions, state and debugging.",
                "A giant pigeon. A broken spaceship. A maze full of coordinates, conditions and collision rules. The premise is absurd; the programming is not.\n\n#ScratchProgramming #GameDesign #CalgaryKids",
                "https://shkolakoda.com/projects/escape-from-the-giant-pigeon",
                "draft",
                None,
                now,
                now,
            ),
            (
                "A Clock Is a System",
                "Reveal the hidden systems thinking inside a familiar game mechanic.",
                "A countdown becomes educational when a student must connect time, state, fairness, and feedback.",
                "routine_social",
                "green",
                "morning",
                "Concept note; no external factual claim.",
                "A countdown looks simple until a child has to make it fair, readable and connected to everything else in a game. Programming time in Scratch turns an everyday idea into a small laboratory for logic, mathematics, design and debugging.",
                "A timer is more than a number going down. It is sequence, state, rate, fairness and debugging—made visible inside a game.",
                "",
                "held",
                None,
                now,
                now,
            ),
        ]
        db.executemany(
            """INSERT INTO posts
            (title, reason_to_exist, editorial_sentence, content_type,
             approval_level, facebook_slot, evidence_notes,
             facebook_body, instagram_body, website_url, status,
             scheduled_at, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            seed_posts,
        )
        db.execute(
            "INSERT INTO activity(post_id, action, detail, created_at) VALUES (NULL, 'initialized', 'Publishing desk created', ?)",
            (now,),
        )
    db.commit()


def login_required(view):
    @wraps(view)
    def wrapped(**kwargs):
        if not session.get("authenticated"):
            return redirect(url_for("login", next=request.path))
        return view(**kwargs)

    return wrapped


def validate_post_form(form):
    title = form.get("title", "").strip()
    reason = form.get("reason_to_exist", "").strip()
    editorial_sentence = form.get("editorial_sentence", "").strip()
    content_type = form.get("content_type", "routine_social").strip()
    approval_level = form.get("approval_level", "green").strip()
    facebook_slot = form.get("facebook_slot", "flexible").strip()
    evidence_notes = form.get("evidence_notes", "").strip()
    facebook = form.get("facebook_body", "").strip()
    instagram = form.get("instagram_body", "").strip()
    website_url = form.get("website_url", "").strip()
    errors = []
    if not title or len(title) > 160:
        errors.append("Title is required and must be at most 160 characters.")
    if not reason:
        errors.append("Give the post a reason to exist.")
    if not editorial_sentence:
        errors.append("Add one editorial sentence.")
    if content_type not in VALID_CONTENT_TYPES:
        errors.append("Choose a valid content type.")
    if approval_level not in VALID_APPROVAL_LEVELS:
        errors.append("Choose a valid approval level.")
    if facebook_slot not in VALID_FACEBOOK_SLOTS:
        errors.append("Choose a valid Facebook slot.")
    if content_type in {"factual_social", "website_article"} and not evidence_notes:
        errors.append("Factual social posts and website articles need evidence notes.")
    if not facebook:
        errors.append("Facebook copy is required.")
    if not instagram:
        errors.append("Instagram copy is required.")
    if website_url and not website_url.startswith("https://shkolakoda.com"):
        errors.append("Website links must point to shkolakoda.com.")
    for error in errors:
        flash(error, "error")
    return None if errors else (
        title,
        reason,
        editorial_sentence,
        content_type,
        approval_level,
        facebook_slot,
        evidence_notes,
        facebook,
        instagram,
        website_url,
    )


def ensure_post_columns(db):
    """Add editorial fields to an existing publisher database without data loss."""
    columns = {row["name"] for row in db.execute("PRAGMA table_info(posts)")}
    additions = {
        "reason_to_exist": "TEXT NOT NULL DEFAULT ''",
        "editorial_sentence": "TEXT NOT NULL DEFAULT ''",
        "content_type": "TEXT NOT NULL DEFAULT 'routine_social'",
        "approval_level": "TEXT NOT NULL DEFAULT 'green'",
        "facebook_slot": "TEXT NOT NULL DEFAULT 'flexible'",
        "evidence_notes": "TEXT NOT NULL DEFAULT ''",
    }
    for name, declaration in additions.items():
        if name not in columns:
            db.execute(f"ALTER TABLE posts ADD COLUMN {name} {declaration}")


def editorial_gate_missing(post):
    missing = []
    if not post["reason_to_exist"].strip():
        missing.append("reason to exist")
    if not post["editorial_sentence"].strip():
        missing.append("editorial sentence")
    if post["content_type"] in {"factual_social", "website_article"} and not post[
        "evidence_notes"
    ].strip():
        missing.append("evidence notes")
    return missing


def get_post_or_404(db, post_id):
    post = db.execute("SELECT * FROM posts WHERE id = ?", (post_id,)).fetchone()
    if post is None:
        abort(404)
    return post


def log_activity(db, post_id, action, detail):
    db.execute(
        "INSERT INTO activity(post_id, action, detail, created_at) VALUES (?, ?, ?, ?)",
        (post_id, action, detail, utc_now()),
    )


def display_time(value):
    if not value:
        return "—"
    parsed = datetime.fromisoformat(value)
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(EDMONTON).strftime("%b %-d, %Y · %-I:%M %p")
