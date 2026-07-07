import json
import os
from pathlib import Path

from flask import Flask, flash, redirect, render_template, request, url_for

from database import get_storage_mode, save_contact_submission


BASE_DIR = Path(__file__).resolve().parent

app = Flask(__name__, instance_relative_config=True)
INSTANCE_DIR = Path(app.instance_path)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "laic-dev-secret-change-me")
app.config["SITE_NAME"] = "Local AI Collective"
app.config["CONTACT_EMAIL"] = os.getenv("CONTACT_EMAIL", "hello@laic.ca")
app.config["DATABASE_URL"] = os.getenv("DATABASE_URL")
app.config["CONTACT_STORAGE_PATH"] = os.getenv(
    "CONTACT_STORAGE_PATH",
    str(INSTANCE_DIR / "contact_submissions.jsonl"),
)


def build_nav_links():
    return [
        ("Home", "index"),
        ("About", "about"),
        ("Services", "services"),
        ("Microprojects", "microprojects"),
        ("For Nonprofits", "for_nonprofits"),
        ("Contact", "contact"),
    ]


@app.context_processor
def inject_globals():
    return {
        "nav_links": build_nav_links(),
        "storage_mode": get_storage_mode(app.config),
    }


def base_context():
    return {
        "example_projects": [
            {
                "title": "FAQ bot for a small nonprofit website",
                "summary": "Turns public website content into a simple assistant that answers common questions and points people to the right page or program.",
            },
            {
                "title": "Volunteer onboarding helper",
                "summary": "Bundles policies, role descriptions, and orientation notes into one searchable guide for staff and volunteers.",
            },
            {
                "title": "Donation and grant reporting helper",
                "summary": "Drafts report language, summarizes program notes, and helps organize metrics without replacing human review.",
            },
            {
                "title": "Spreadsheet cleanup and reporting workflow",
                "summary": "Standardizes messy exports, finds gaps, and produces cleaner summaries for staff who do not have time for manual cleanup.",
            },
        ]
    }


def validate_contact_form(form_data):
    errors = []
    required_fields = {
        "organization_name": "Organization name",
        "contact_name": "Contact name",
        "email": "Email",
        "organization_type": "Type of organization",
        "problem_to_solve": "What problem you want help with",
    }

    for field, label in required_fields.items():
        if not form_data.get(field, "").strip():
            errors.append(f"{label} is required.")

    email = form_data.get("email", "").strip()
    if email and ("@" not in email or "." not in email.split("@")[-1]):
        errors.append("Enter a valid email address.")

    return errors


@app.get("/")
def index():
    return render_template("index.html", **base_context())


@app.get("/about")
def about():
    return render_template("about.html", **base_context())


@app.get("/services")
def services():
    return render_template("services.html", **base_context())


@app.get("/microprojects")
def microprojects():
    return render_template("microprojects.html", **base_context())


@app.get("/for-nonprofits")
def for_nonprofits():
    return render_template("for_nonprofits.html", **base_context())


@app.route("/contact", methods=["GET", "POST"])
def contact():
    form_data = {
        "organization_name": "",
        "contact_name": "",
        "email": "",
        "organization_type": "",
        "problem_to_solve": "",
        "privacy_sensitive": "",
    }

    if request.method == "POST":
        form_data = {
            "organization_name": request.form.get("organization_name", "").strip(),
            "contact_name": request.form.get("contact_name", "").strip(),
            "email": request.form.get("email", "").strip(),
            "organization_type": request.form.get("organization_type", "").strip(),
            "problem_to_solve": request.form.get("problem_to_solve", "").strip(),
            "privacy_sensitive": "yes" if request.form.get("privacy_sensitive") else "no",
        }
        errors = validate_contact_form(form_data)

        if errors:
            for error in errors:
                flash(error, "error")
        else:
            save_contact_submission(app.config, form_data)
            flash("Thanks. We will review your note and follow up.", "success")
            return redirect(url_for("contact"))

    return render_template("contact.html", form_data=form_data, **base_context())


@app.get("/projects/love-sugar-dough")
def love_sugar_dough():
    return render_template("love_sugar_dough.html", **base_context())


@app.get("/dashboard")
def dashboard():
    return render_template("dashboard.html", **base_context())


@app.get("/health")
def health():
    payload = {
        "status": "ok",
        "site": app.config["SITE_NAME"],
        "contact_storage": get_storage_mode(app.config),
    }
    return app.response_class(
        response=json.dumps(payload),
        status=200,
        mimetype="application/json",
    )


if __name__ == "__main__":
    os.makedirs(INSTANCE_DIR, exist_ok=True)
    app.run(host="127.0.0.1", port=8004, debug=True)
