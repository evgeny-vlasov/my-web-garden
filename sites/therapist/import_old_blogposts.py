#!/usr/bin/env python3
"""Merge blog posts from an isolated old PostgreSQL restore into production.

Dry-run is the default. Applying requires both --apply and a fresh, non-empty
production backup supplied with --production-backup.
"""

import argparse
import hashlib
import os
from datetime import datetime, timezone
from pathlib import Path

import psycopg2
from psycopg2.extras import RealDictCursor


MAX_SLUG_LENGTH = 200
BACKUP_MAX_AGE_SECONDS = 24 * 60 * 60


def fingerprint(post):
    values = (
        post.get("title") or "",
        post.get("content") or "",
        post["published_at"].isoformat() if post.get("published_at") else "",
        "1" if post.get("visible") else "0",
    )
    return hashlib.sha256("\0".join(values).encode("utf-8")).hexdigest()


def conflict_slug(original, reserved):
    base = (original or "post").strip("-") or "post"
    counter = 1
    while True:
        suffix = "-old" if counter == 1 else f"-old-{counter}"
        candidate = f"{base[: MAX_SLUG_LENGTH - len(suffix)]}{suffix}"
        if candidate not in reserved:
            return candidate
        counter += 1


def validate_backup(path_value):
    if not path_value:
        raise SystemExit("--apply requires --production-backup PATH")
    path = Path(path_value).resolve()
    stat = path.stat()
    age = datetime.now(timezone.utc).timestamp() - stat.st_mtime
    if stat.st_size <= 0:
        raise SystemExit("Production backup is empty")
    if age < 0 or age > BACKUP_MAX_AGE_SECONDS:
        raise SystemExit("Production backup must be less than 24 hours old")
    return path


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true", help="commit the merge")
    parser.add_argument("--production-backup", help="fresh pre-import pg_dump path")
    parser.add_argument("--old-host", default="/tmp")
    parser.add_argument("--old-port", default=55432, type=int)
    parser.add_argument("--old-db", default="psyling_old_restore")
    parser.add_argument("--author", default="valery")
    return parser.parse_args()


def main():
    args = parse_args()
    production_url = os.environ.get("DATABASE_URL")
    if not production_url:
        raise SystemExit("DATABASE_URL is not set")
    backup = validate_backup(args.production_backup) if args.apply else None

    old = psycopg2.connect(
        host=args.old_host, port=args.old_port, dbname=args.old_db
    )
    production = psycopg2.connect(production_url)
    production.autocommit = False

    try:
        with old.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """SELECT title, slug, content, published_at, updated_at,
                          visible, language
                   FROM blog_posts ORDER BY id"""
            )
            old_posts = cursor.fetchall()

        with production.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SET TRANSACTION ISOLATION LEVEL SERIALIZABLE")
            cursor.execute("SELECT pg_advisory_xact_lock(707731904)")
            cursor.execute(
                "SELECT id, username FROM users WHERE lower(username)=lower(%s)",
                (args.author,),
            )
            authors = cursor.fetchall()
            if len(authors) != 1:
                raise SystemExit(
                    f"Expected exactly one current user named {args.author!r}; "
                    f"found {len(authors)}"
                )
            author = authors[0]

            cursor.execute(
                """SELECT title, slug, content, published_at, updated_at, visible
                   FROM blog_posts"""
            )
            current_posts = cursor.fetchall()

            reserved_slugs = {post["slug"] for post in current_posts}
            fingerprints = {fingerprint(post) for post in current_posts}
            imports = []
            duplicates = []
            conflicts = []

            for post in old_posts:
                post_fingerprint = fingerprint(post)
                if post_fingerprint in fingerprints:
                    duplicates.append(post)
                    continue

                destination_slug = post["slug"]
                if destination_slug in reserved_slugs:
                    destination_slug = conflict_slug(destination_slug, reserved_slugs)
                    conflicts.append((post["slug"], destination_slug))

                imports.append((post, destination_slug))
                reserved_slugs.add(destination_slug)
                fingerprints.add(post_fingerprint)

            print("mode=" + ("APPLY" if args.apply else "DRY-RUN"))
            print(f"old_posts={len(old_posts)}")
            print(f"current_posts={len(current_posts)}")
            print(f"would_import={len(imports)}")
            print(f"would_skip_duplicates={len(duplicates)}")
            print(f"slug_conflicts={len(conflicts)}")
            for source, destination in conflicts:
                print(f"slug_rename={source} -> {destination}")
            print(f"assigned_to_user={author['username']} (current id {author['id']})")
            print("unmapped_fields=language (production has no language column)")
            print("absent_fields=excerpt,status,created_at,tags,categories,image")
            print("mapped_fields=title,slug,content,author_id,published_at,updated_at,visible")

            if args.apply:
                imported_rows = []
                for post, destination_slug in imports:
                    cursor.execute(
                        """INSERT INTO blog_posts
                           (title, slug, content, author_id, published_at,
                            updated_at, visible)
                           VALUES (%s, %s, %s, %s, %s, %s, %s)
                           RETURNING id, slug""",
                        (
                            post["title"],
                            destination_slug,
                            post["content"],
                            author["id"],
                            post["published_at"],
                            post["updated_at"],
                            post["visible"],
                        ),
                    )
                    imported_rows.append(cursor.fetchone())
                production.commit()
                print(f"imported={len(imports)}")
                for row in imported_rows:
                    print(f"imported_row=id:{row['id']} slug:{row['slug']}")
                print(f"production_backup_verified={backup.name}")
            else:
                production.rollback()
                print("committed=no")
    except Exception:
        production.rollback()
        raise
    finally:
        old.close()
        production.close()


if __name__ == "__main__":
    main()
