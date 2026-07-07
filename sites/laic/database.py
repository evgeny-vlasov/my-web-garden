import json
from datetime import datetime, timezone
from pathlib import Path

import psycopg


def get_storage_mode(config):
    if config.get("DATABASE_URL"):
        return "postgres"
    return "local-file"


def ensure_schema(database_url):
    schema_path = Path(__file__).resolve().parent / "db" / "schema.sql"
    with psycopg.connect(database_url) as connection:
        with connection.cursor() as cursor:
            cursor.execute(schema_path.read_text())
        connection.commit()


def save_contact_submission(config, form_data):
    submitted_at = datetime.now(timezone.utc).isoformat()
    row = {
        "organization_name": form_data["organization_name"],
        "contact_name": form_data["contact_name"],
        "email": form_data["email"],
        "organization_type": form_data["organization_type"],
        "problem_to_solve": form_data["problem_to_solve"],
        "privacy_sensitive": form_data["privacy_sensitive"],
        "submitted_at": submitted_at,
    }

    database_url = config.get("DATABASE_URL")
    if database_url:
        ensure_schema(database_url)
        with psycopg.connect(database_url) as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO contact_submissions (
                        organization_name,
                        contact_name,
                        email,
                        organization_type,
                        problem_to_solve,
                        privacy_sensitive,
                        submitted_at
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """,
                    (
                        row["organization_name"],
                        row["contact_name"],
                        row["email"],
                        row["organization_type"],
                        row["problem_to_solve"],
                        row["privacy_sensitive"] == "yes",
                        submitted_at,
                    ),
                )
            connection.commit()
        return

    storage_path = Path(config["CONTACT_STORAGE_PATH"])
    storage_path.parent.mkdir(parents=True, exist_ok=True)
    with storage_path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(row) + "\n")
